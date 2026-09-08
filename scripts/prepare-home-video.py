#!/usr/bin/env python3
"""Prepare the home page film assets from the owner's edited master.

Usage:  python3 scripts/prepare-home-video.py <master.mp4> [end_card_start_seconds]

Produces, in assets/video/:
  spencer-alexander-intro-1080.mp4   the rebuilt film, 30 fps, faststart
  spencer-alexander-intro-720.mp4    the same at 1280x720 for handheld or slow devices
  poster-1600.jpg                    a graded still from an engaged moment inside a caption gap, so no caption
                                     and no caption ghost in the foreground estimate

Not produced here: end-card.jpg and end-card-small.jpg, the owner's contact
card frames, which stay as they are (recipes in DECISIONS.md, 5 Sep 2026).

The rebuild (8 Sep 2026). The master is a phone recording against a bare
beige wall in flat light, with the owner's burned in captions and two
serif lower thirds. The owner cannot reshoot, so this script rebuilds the
picture around the presenter instead:

 1. Matting. Robust Video Matting (mobilenetv3, temporal memory) separates
    the presenter from the wall frame by frame and returns a clean
    foreground estimate and alpha, so hair and hands keep soft edges.
 2. Wall reference. The median of every pixel the presenter never covers
    and no caption ever lights is the static wall. Each caption's text mask
    is taken from its full opacity frames in a pre pass, and inside that
    mask a caption pixel's alpha is how far it stands above the wall, so
    the master's own caption fades survive and the master's lower thirds
    vanish with the wall behind them.
 3. Composite. The presenter sits on a studio backdrop designed by how it
    should look after the grade (the portrait's warm grey pool behind the
    head, dark corners, a darker base) and inverse graded, with a soft cast
    shadow, a gentle key from camera left on the presenter, the portrait
    grade over the whole frame (22 percent sepia, the wine multiply
    gradient, a touch of saturation and contrast) and fine grain so the
    backdrop and the phone footage share one texture. The captions are
    then laid back on top in white with a soft shadow under the strokes.
 4. Lower thirds in the site's typography (Spectral and Libre Franklin in
    cream and brass): the name card from 0.9 to 5.9 seconds and the call
    card from 44.7 seconds until just before the cut, carrying the phone
    number as the site writes it, the free first call and the web address.
 5. Trim the first quarter second, fade in from the site's wine, dip to
    wine into the owner's end card (never a cross dissolve, which put his
    face over the QR code). The card is taken from after the master's own
    short dissolve into it, so no ghost of the beige wall survives, and its
    hold is trimmed so the length holds at 57 seconds.

The master's captions stay exactly as the owner edited them: they are
neither cropped nor filled, only carried across. Never crop them, fill
them or add a caption track over them (rejected 5 and 6 Sep 2026).

Dependencies: numpy, opencv-python, Pillow, imageio-ffmpeg and a CPU build
of torch (pip install --index-url https://download.pytorch.org/whl/cpu
torch). The RVM source, its weights and the two font families are fetched
into scripts/.cache/ on first run (git ignored). The matting pass takes
about seven minutes and the composite about twenty on four cores.
Run scripts/check-publish.py afterwards and update the VideoObject
duration and uploadDate on index.html if they change.
"""
import os, re, shutil, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
CACHE = os.path.join(HERE, ".cache")
OUT = os.path.join(ROOT, "assets", "video")
W, H, FPS = 1920, 1080, 30
SKIP = 8                     # frames trimmed from the start, the presenter standing still
POSTER_AT = 29.57            # seconds into the master: eyes to camera, hands open, inside a caption gap (frame 887)
DIP = 0.3                    # seconds of fade to wine either side of the cut to the end card
CARD_SKIP = 0.3              # the master dissolves into its card over about a quarter second; the card is taken after that
CARD_TRIM = 0.2              # seconds taken off the end card hold so the film length holds at 57 seconds
NAME_CARD = (0.9, 0.5, 5.4, 0.5)   # fade in start, fade in length, fade out start, fade out length
CALL_CARD = (44.7, 0.5)            # fade in start, fade in length; it fades out before the dip
WINE = "0x1A070C"
RVM_REPO = "https://github.com/PeterL1n/RobustVideoMatting.git"
RVM_WEIGHTS = "https://github.com/PeterL1n/RobustVideoMatting/releases/download/v1.0.0/rvm_mobilenetv3.pth"
FONTS = {
    "Spectral-Medium.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/spectral/Spectral-Medium.ttf",
    "LibreFranklin[wght].ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/librefranklin/LibreFranklin%5Bwght%5D.ttf",
}
# the home page portrait grade, unchanged since 5 Sep 2026
MIXER = [[0.8665, 0.169, 0.0416], [0.0768, 0.931, 0.037], [0.0598, 0.1175, 0.8088]]
TOP = (0.841, 0.754, 0.770); BOT = (0.5745, 0.5196, 0.5333); DARK = (0.506, 0.465, 0.476)


def ffmpeg():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def fetch(url, path):
    if not os.path.exists(path):
        print("fetching", url)
        urllib.request.urlretrieve(url, path)
    return path


def ensure_cache():
    os.makedirs(CACHE, exist_ok=True)
    rvm = os.path.join(CACHE, "RobustVideoMatting")
    if not os.path.isdir(rvm):
        subprocess.check_call(["git", "clone", "--quiet", "--depth", "1", RVM_REPO, rvm])
    fetch(RVM_WEIGHTS, os.path.join(CACHE, "rvm_mobilenetv3.pth"))
    for name, url in FONTS.items():
        fetch(url, os.path.join(CACHE, name))
    return rvm


def reader(ff, path, pix, ch):
    import numpy as np
    p = subprocess.Popen([ff, "-hide_banner", "-loglevel", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", pix, "-"], stdout=subprocess.PIPE, bufsize=10 ** 8)
    n = W * H * ch
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield np.frombuffer(b, np.uint8).reshape((H, W, ch) if ch > 1 else (H, W))
    p.stdout.close(); p.wait()


def matte_pass(ff, src, cut_frame, work, rvm):
    """Robust Video Matting over the talking head, writing foreground and alpha as lossless FFV1."""
    import numpy as np, cv2, torch
    sys.path.insert(0, rvm)
    from model import MattingNetwork
    torch.set_num_threads(max(1, os.cpu_count() or 1))
    model = MattingNetwork("mobilenetv3").eval()
    model.load_state_dict(torch.load(os.path.join(CACHE, "rvm_mobilenetv3.pth"), map_location="cpu"))
    enc = ["-f", "rawvideo", "-pix_fmt", None, "-s", "%dx%d" % (W, H), "-r", str(FPS), "-i", "-", "-c:v", "ffv1", "-level", "3", "-threads", "2", "-y"]
    def spawn(pix, out):
        return subprocess.Popen([ff, "-hide_banner", "-loglevel", "error"] + [a if a is not None else pix for a in enc] + [out], stdin=subprocess.PIPE)
    pf = spawn("rgb24", os.path.join(work, "fgr.mkv")); pa = spawn("gray", os.path.join(work, "alpha.mkv"))
    cap = cv2.VideoCapture(src); rec = [None] * 4; i = 0
    with torch.no_grad():
        while i < cut_frame:
            ok, fr = cap.read()
            if not ok:
                break
            rgb = cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)
            s = torch.from_numpy(rgb).permute(2, 0, 1).float().div(255).unsqueeze(0)
            fgr, pha, *rec = model(s, *rec, downsample_ratio=0.25)
            pf.stdin.write((fgr[0].permute(1, 2, 0).numpy() * 255).round().astype(np.uint8).tobytes())
            pa.stdin.write((pha[0, 0].numpy() * 255).round().astype(np.uint8).tobytes())
            i += 1
            if i % 300 == 0:
                print("  matted", i, "frames", flush=True)
    pf.stdin.close(); pa.stdin.close(); pf.wait(); pa.wait()
    return i


def wall_reference(ff, src, work, n):
    """Median of every pixel the presenter never covers and no caption ever lights: the static wall."""
    import numpy as np
    frames, masks, i = [], [], 0
    for s, a in zip(reader(ff, src, "rgb24", 3), reader(ff, os.path.join(work, "alpha.mkv"), "gray", 1)):
        if i % 36 == 0:
            frames.append(s.copy()); masks.append(a <= 10)
        i += 1
        if i >= n:
            break
    F = np.stack(frames); M = np.stack(masks)
    ref = np.zeros((H, W, 3), np.uint8); valid = np.zeros((H, W), bool)
    for y0 in range(0, H, 90):
        f = F[:, y0:y0 + 90].astype(np.float32)
        f[~(M[:, y0:y0 + 90] & (F[:, y0:y0 + 90].max(axis=3) < 226))] = np.nan   # never the presenter, never caption text
        med = np.nanmedian(f, axis=0); v = ~np.isnan(med[..., 0])
        ref[y0:y0 + 90] = np.nan_to_num(med, nan=0).astype(np.uint8); valid[y0:y0 + 90] = v
    return ref.astype(np.float32).max(axis=2), valid


def caption_masks(src, n):
    """Every caption interval in the master and a dilated mask of its text, from its full opacity frames."""
    import cv2, numpy as np
    cap = cv2.VideoCapture(src); counts = []; frames = {}; i = 0
    while i < n:
        ok, c = cap.read()
        if not ok:
            break
        rgb = c[..., ::-1].astype(np.int16); lum = rgb.max(axis=2); sat = lum - rgb.min(axis=2)
        m = (lum > 238) & (sat < 40); m[:880] = False
        counts.append(int(m.sum())); frames[i] = m; i += 1
    intervals, s = [], None
    for k, full in enumerate(x >= 30 for x in counts):
        if full and s is None:
            s = k
        if not full and s is not None:
            intervals.append((s, k - 1)); s = None
    if s is not None:
        intervals.append((s, len(counts) - 1))
    intervals = [iv for iv in intervals if iv[1] - iv[0] >= 3]
    kernel = np.ones((9, 9), np.uint8); masks = []
    for a, b in intervals:
        u = np.zeros((H, W), bool)
        for p in sorted(set([a + 1, (a + b) // 2, b - 1])):
            u |= frames[p]
        masks.append(cv2.dilate(u.astype(np.uint8), kernel) > 0)
    # each frame carries the masks of the captions on either side of it, so fades and gaps are covered
    active = [[] for _ in range(n)]
    for j in range(len(intervals)):
        lo = intervals[j - 1][1] + 1 if j > 0 else 0
        hi = intervals[j + 1][0] - 1 if j + 1 < len(intervals) else n - 1
        for i in range(max(lo, 0), min(hi, n - 1) + 1):
            active[i].append(j)
    return masks, active


def lower_thirds(work):
    """The two overlays in the site's typography, full frame PNGs with alpha."""
    from PIL import Image, ImageDraw, ImageFont
    cream, brass, soft = (251, 249, 245), (201, 162, 90), (232, 224, 214)
    def franklin(size, weight):
        f = ImageFont.truetype(os.path.join(CACHE, "LibreFranklin[wght].ttf"), size); f.set_variation_by_axes([weight]); return f
    def spectral(size):
        return ImageFont.truetype(os.path.join(CACHE, "Spectral-Medium.ttf"), size)
    def card(lines, out, x=96, y=68):
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); cy = y
        for text, font, col, tracking, gap in lines:
            if tracking:
                cx = x
                for ch in text:
                    d.text((cx, cy), ch, font=font, fill=col); cx += font.getlength(ch) + tracking
            else:
                d.text((x, cy), text, font=font, fill=col)
            bb = font.getbbox("Hg"); cy += (bb[3] - bb[1]) + gap
        d.rectangle([x - 36, y + 8, x - 31, cy - lines[-1][4] + 12], fill=brass)
        im.save(out)
    card([("Spencer Alexander", spectral(80), cream, 0, 26), ("PRINCIPAL", franklin(30, 600), brass, 5, 14),
          ("Spencer Alexander Lawyers, Box Hill", franklin(42, 400), soft, 0, 0)], os.path.join(work, "lt_name.png"))
    card([("Speak with Spencer", spectral(72), cream, 0, 22), ("(03) 9125 8355", franklin(62, 500), cream, 1, 16),
          ("YOUR FIRST CALL IS FREE", franklin(30, 600), brass, 5, 14), ("spenceralexander.com.au", franklin(42, 400), soft, 0, 0)],
         os.path.join(work, "lt_call.png"))


def compose(ff, src, work, n, wall_lum, wall_valid, masks, active, poster_frame):
    """Presenter over the backdrop, keyed, graded and grained, captions carried as alpha with a shadow, lower thirds overlaid."""
    import numpy as np, cv2
    M = np.array(MIXER, np.float32); MI = np.linalg.inv(M).astype(np.float32); LW = np.array([0.299, 0.587, 0.114], np.float32)
    fy = (np.arange(H, dtype=np.float32) / (H - 1))[:, None, None]
    k = np.clip((fy - 0.58) / 0.42, 0, 1)
    grad = (np.array(TOP, np.float32) + (np.array(BOT, np.float32) - np.array(TOP, np.float32)) * fy) * (1 - k * (1 - np.array(DARK, np.float32)))
    def grade(x):
        x = (x @ M.T) * grad
        lum = x @ LW
        x = lum[..., None] + (x - lum[..., None]) * 1.05
        return np.clip((x - 128) * 1.04 + 128, 0, 255)
    def ungrade(y):
        y = (y - 128) / 1.04 + 128
        lum = y @ LW
        y = lum[..., None] + (y - lum[..., None]) / 1.05
        return (y / grad) @ MI.T
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    def backdrop_target(centre=(0.5, 0.36), pool=(140, 136, 132), edge=(74, 70, 68), base=(46, 43, 43)):
        """How the backdrop should look after the grade: the portrait's warm grey pool behind the head,
        darker corners, a darker base, with a wide soft falloff so his position within it does not matter."""
        dx = xx / W - centre[0]; dy = (yy / H - centre[1]) * (H / W) * 1.15
        kk = np.clip(np.sqrt(dx * dx + dy * dy) / 0.78, 0, 1) ** 1.25
        img = np.empty((H, W, 3), np.float32)
        for c in range(3):
            img[..., c] = pool[c] + (edge[c] - pool[c]) * kk
        f = np.clip((yy / H - 0.60) / 0.40, 0, 1) ** 1.2
        for c in range(3):
            img[..., c] = img[..., c] * (1 - f) + np.minimum(img[..., c], base[c]) * f
        return img
    bg = ungrade(backdrop_target())
    key = ((1.04 - 0.10 * (xx / W)) * (1 - 0.10 * np.clip((yy / H - 0.55) / 0.45, 0, 1)))[..., None]
    def shift(img, dx, dy):
        out = np.zeros_like(img); h, w = img.shape[:2]
        out[max(dy, 0):h + min(dy, 0), max(dx, 0):w + min(dx, 0)] = img[max(-dy, 0):h - max(dy, 0), max(-dx, 0):w - max(dx, 0)]
        return out
    def frame(i, fgr, alpha, s, captions=True):
        a = alpha.astype(np.float32)[..., None] / 255
        small = cv2.resize(a[..., 0], (W // 4, H // 4), interpolation=cv2.INTER_AREA)
        sh = cv2.resize(shift(cv2.GaussianBlur(small, (0, 0), 7.5), 8, 6), (W, H), interpolation=cv2.INTER_LINEAR)[..., None]
        comp = grade(fgr.astype(np.float32) * key * a + bg * (1 - 0.40 * sh) * (1 - a))
        comp = comp + np.random.default_rng(i).standard_normal(comp.shape, dtype=np.float32) * 2.0
        if captions and active[i]:
            m = np.zeros((H, W), bool)
            for j in active[i]:
                m |= masks[j]
            s = s.astype(np.float32); lum = s.max(axis=2); sat = lum - s.min(axis=2)
            ta = np.where(wall_valid, np.clip((lum - wall_lum - 8) / np.maximum(255 - wall_lum - 8, 20), 0, 1), np.clip((lum - 238) / 12, 0, 1))
            ta = ta * np.clip((70 - sat) / 30, 0, 1) * m
            shadow = cv2.GaussianBlur(cv2.dilate(ta, np.ones((5, 5), np.uint8)), (0, 0), 1.5)[..., None]
            ta = ta[..., None]
            comp = comp * (1 - 0.45 * shadow * (1 - ta))
            comp = comp * (1 - ta) + 255 * ta
        return np.clip(comp, 0, 255).astype(np.uint8)
    name, call = NAME_CARD, CALL_CARD
    call_out = round((n - SKIP) / FPS - DIP - 0.45, 3)
    graph = ("[1:v]format=rgba,fade=t=in:st=%s:d=%s:alpha=1,fade=t=out:st=%s:d=%s:alpha=1[n];"
             "[2:v]format=rgba,fade=t=in:st=%s:d=%s:alpha=1,fade=t=out:st=%s:d=0.4:alpha=1[c];"
             "[0:v][n]overlay=0:0:shortest=1[a];[a][c]overlay=0:0:shortest=1,fade=t=in:st=0:d=0.6:color=%s,format=yuv420p[v]") % (name + call + (call_out, WINE))
    talk = os.path.join(work, "talk.mkv")
    enc = subprocess.Popen([ff, "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (W, H), "-r", str(FPS), "-i", "-",
                            "-loop", "1", "-framerate", str(FPS), "-i", os.path.join(work, "lt_name.png"), "-loop", "1", "-framerate", str(FPS), "-i", os.path.join(work, "lt_call.png"),
                            "-filter_complex", graph, "-map", "[v]", "-c:v", "libx264", "-preset", "faster", "-crf", "12", "-pix_fmt", "yuv420p", "-r", str(FPS),
                            "-t", str((n - SKIP) / FPS), talk], stdin=subprocess.PIPE)
    i = 0
    for f, a, s in zip(reader(ff, os.path.join(work, "fgr.mkv"), "rgb24", 3), reader(ff, os.path.join(work, "alpha.mkv"), "gray", 1), reader(ff, src, "rgb24", 3)):
        if i >= n:
            break
        if i == poster_frame:
            cv2.imwrite(os.path.join(work, "poster-full.png"), cv2.cvtColor(frame(i, f, a, s, captions=False), cv2.COLOR_RGB2BGR))
        if i >= SKIP:
            enc.stdin.write(frame(i, f, a, s).tobytes())
        i += 1
        if i % 300 == 0:
            print("  composed", i, "frames", flush=True)
    enc.stdin.close(); enc.wait()
    return talk, (i - SKIP) / FPS


def assemble(ff, src, work, talk, talk_len, cut, master_len):
    os.makedirs(OUT, exist_ok=True)
    card_start = cut + CARD_SKIP; card_len = master_len - card_start
    total = round(talk_len + card_len - CARD_TRIM, 3)
    graph = ("[0:v]format=yuv420p,setpts=PTS-STARTPTS,fps=%d,fade=t=out:st=%s:d=%s:color=%s[a];"
             "[1:v]format=yuv420p,setpts=PTS-STARTPTS,fps=%d,trim=0:%s,setpts=PTS-STARTPTS,fade=t=in:st=0:d=%s:color=%s[b];"
             "[a][b]concat=n=2:v=1:a=0,split=2[full][half];[half]scale=1280:-2[v720];"
             "[2:a]afade=t=in:st=0:d=0.2,atrim=0:%s,asplit=2[aud1][aud2]") % (FPS, round(talk_len - DIP, 3), DIP, WINE, FPS, round(card_len - CARD_TRIM, 3), DIP, WINE, total)
    common = ["-c:v", "libx264", "-preset", "slow", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", str(FPS), "-movflags", "+faststart", "-c:a", "aac", "-ar", "48000", "-t", str(total)]
    subprocess.check_call([ff, "-hide_banner", "-loglevel", "error", "-y", "-i", talk, "-ss", str(card_start), "-i", src, "-ss", str(SKIP / FPS), "-i", src, "-filter_complex", graph,
        "-map", "[full]", "-map", "[aud1]", *common, "-crf", "22", "-level", "4.1", "-b:a", "128k", os.path.join(OUT, "spencer-alexander-intro-1080.mp4"),
        "-map", "[v720]", "-map", "[aud2]", *common, "-crf", "23", "-level", "4.0", "-b:a", "112k", os.path.join(OUT, "spencer-alexander-intro-720.mp4")])
    subprocess.check_call([ff, "-hide_banner", "-loglevel", "error", "-y", "-i", os.path.join(work, "poster-full.png"), "-vf", "scale=1600:-2", "-q:v", "4", os.path.join(OUT, "poster-1600.jpg")])
    return total


def duration(ff, path):
    info = subprocess.run([ff, "-hide_banner", "-i", path], capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", info)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def main():
    if len(sys.argv) < 2:
        print(__doc__); return 2
    src = os.path.abspath(sys.argv[1]); cut = float(sys.argv[2]) if len(sys.argv) > 2 else 51.55
    ff = ffmpeg(); rvm = ensure_cache()
    work = os.path.join(CACHE, "work"); os.makedirs(work, exist_ok=True)
    cut_frame = int(round(cut * FPS)); poster_frame = int(round(POSTER_AT * FPS))
    print("matting", src)
    n = matte_pass(ff, src, cut_frame, work, rvm)
    print("wall reference"); wall_lum, wall_valid = wall_reference(ff, src, work, n)
    print("caption masks"); masks, active = caption_masks(src, n)
    lower_thirds(work)
    print("compositing"); talk, talk_len = compose(ff, src, work, n, wall_lum, wall_valid, masks, active, poster_frame)
    print("assembling"); total = assemble(ff, src, work, talk, talk_len, cut, duration(ff, src))
    for f in ("spencer-alexander-intro-1080.mp4", "spencer-alexander-intro-720.mp4", "poster-1600.jpg"):
        print("  %-36s %9d bytes" % (f, os.path.getsize(os.path.join(OUT, f))))
    print("film length %.2f s: update the VideoObject duration on index.html if it changed" % total)
    return 0


if __name__ == "__main__":
    sys.exit(main())
