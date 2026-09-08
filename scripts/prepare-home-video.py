#!/usr/bin/env python3
"""Prepare the home page film assets from the owner's edited office master.

Usage:  python3 scripts/prepare-home-video.py <master.mp4> [poster_seconds]

Produces, in assets/video/:
  spencer-alexander-intro-1080.mp4   the finished film, 30 fps, faststart
  spencer-alexander-intro-720.mp4    the same at 1280x720 for handheld or slow devices
  poster-1600.jpg                    a graded still from the film, no cards over it

Not produced here: end-card.jpg and end-card-small.jpg, the owner's contact
card frames, which stay as they are (recipes in DECISIONS.md, 5 Sep 2026).

The master (owner's second cut, supplied 8 Sep 2026): filmed in the firm's
Box Hill offices on a locked off camera, the presenter slightly off centre,
no burned in captions, the owner's own serif name card over the first
seconds and a "Speak with Spencer" card from about 41 seconds, then a short
dissolve into the owner's contact card at about 48 seconds. Nothing is
matted or composited: the presenter and the room are one shot, which is what
the owner asked for after the 5 Sep master's rebuild read as a composite.

What this script does:
 1. Finds the end card (the first frame that matches the settled card) and
    the frames where the master's own cards are on (wine text in the top
    left), and the take boundary at about 41 seconds.
 2. Replaces the master's cards with the room behind them. The camera never
    moves, so for the name card the room is copied from a later frame of the
    same take; the second take has its card on throughout, so that region is
    inpainted once from the blurred room around it. Each patch is feathered
    and applied only while its card is on, and a check confirms the
    presenter never enters either region.
 3. A light grade so the room sits with the site: a touch of warmth, a soft
    vignette, a little contrast. Nothing heavier: the room is the point.
 4. Lower thirds in the site's typography (Spectral and Libre Franklin in
    cream and brass over a soft feathered scrim): the name card over the
    opening seconds and, from 41.6 seconds, the phone number as the site
    writes it, "Your first call is free" and the web address.
 5. A fade in from the site's wine, the last clean frame held while the
    picture dips to wine so his final word finishes on screen, the owner's
    card fading in from wine (the master's own dissolve frames are skipped),
    and both encodes.

Dependencies: numpy, opencv-python, Pillow, imageio-ffmpeg. The two font
families are fetched into scripts/.cache/ on first run (git ignored). The
whole run takes about four minutes. Run scripts/check-publish.py afterwards
and update the VideoObject duration, uploadDate and transcript on
index.html if the master changed.
"""
import json, os, re, shutil, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
CACHE = os.path.join(HERE, ".cache")
OUT = os.path.join(ROOT, "assets", "video")
W, H, FPS = 1920, 1080, 30
DIP = 0.3                    # seconds of fade to wine either side of the cut to the end card
WINE = "0x1A070C"
NAME_CARD = (1.0, 0.5, 5.6, 0.5)   # fade in start, length, fade out start, length
CALL_CARD = (41.6, 0.5, 0.4)       # fade in start, length, fade out length (it leaves with the picture)
HOLD = 0.4                   # the last clean frame is held this long and the dip to wine runs over the hold
FONTS = {
    "Spectral-Medium.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/spectral/Spectral-Medium.ttf",
    "LibreFranklin[wght].ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/librefranklin/LibreFranklin%5Bwght%5D.ttf",
}
GRADE = ("format=rgb24,colorchannelmixer=rr=0.93:rg=0.09:rb=0.02:gr=0.04:gg=0.96:gb=0.02:br=0.03:bg=0.06:bb=0.9,"
         "vignette=angle=PI/4.4,eq=saturation=1.02:contrast=1.05:brightness=-0.02")


def ffmpeg():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def ensure_fonts():
    os.makedirs(CACHE, exist_ok=True)
    for name, url in FONTS.items():
        path = os.path.join(CACHE, name)
        if not os.path.exists(path):
            print("fetching", url); urllib.request.urlretrieve(url, path)


def duration(ff, path):
    info = subprocess.run([ff, "-hide_banner", "-i", path], capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", info)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def analyse(src):
    """End card frame, the master's card intervals and the frame before its dissolve into the card."""
    import cv2, numpy as np
    cap = cv2.VideoCapture(src); n = int(cap.get(7))
    white, wine = [], []
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        rgb = fr[..., ::-1].astype(np.int16)
        white.append(float((rgb.min(axis=2) > 235).mean()))
        tl = rgb[20:300, 40:800]; r, g, b = tl[..., 0], tl[..., 1], tl[..., 2]
        wine.append(int(((r > 70) & (r < 180) & (g < 100) & (b < 110) & (r - g > 35)).sum()))
    white = np.array(white); card = int(np.argmax(white > 0.5))
    def frame(i):
        cap.set(1, i); ok, f = cap.read(); return f
    settled = frame(min(card + 60, n - 1)).astype(np.int16)
    for i in range(card, max(card - 60, 0), -1):          # walk back through the master's dissolve
        if np.abs(frame(i).astype(np.int16) - settled).mean() > 100:
            talk_end = i + 1; break
    else:
        talk_end = card
    for i in range(card, n):                                # first frame that matches the settled card
        if np.abs(frame(i).astype(np.int16) - settled).mean() < 1.0:
            card_start = i; break
    on = np.array(wine) > 150; segs, s = [], None
    for k, v in enumerate(on[:card]):
        if v and s is None:
            s = k
        if not v and s is not None:
            segs.append((s, k - 1)); s = None
    if s is not None:
        segs.append((s, card - 1))
    segs = [sg for sg in segs if sg[1] - sg[0] > 5]
    return dict(n=n, card=card, talk_end=talk_end, card_start=card_start, segs=segs)


def feather(patch, f=16):
    import numpy as np
    h, w = patch.shape[:2]; a = np.ones((h, w), np.float32)
    for k in range(f):
        v = (k + 1) / (f + 1)
        a[k, :] = np.minimum(a[k, :], v); a[h - 1 - k, :] = np.minimum(a[h - 1 - k, :], v)
        a[:, k] = np.minimum(a[:, k], v); a[:, w - 1 - k] = np.minimum(a[:, w - 1 - k], v)
    return np.dstack([patch, (a * 255).astype(np.uint8)])


def card_patch(src, seg, work, name, clean_frame=None):
    """A patch of the room where the master's card sits: copied from a clean frame of the same take when
    one exists, otherwise inpainted from the blurred room around the text. Returns (png path, x, y)."""
    import cv2, numpy as np
    cap = cv2.VideoCapture(src)
    def frame(i):
        cap.set(1, i); ok, f = cap.read(); return f
    sample = frame(seg[0] + min(30, (seg[1] - seg[0]) // 2))
    reg = (slice(30, 460), slice(0, 900)); sub = sample[reg]
    rgb = sub[..., ::-1].astype(np.int16); r, g = rgb[..., 0], rgb[..., 1]
    diff = np.abs(sub.astype(np.int16) - cv2.medianBlur(sub, 31).astype(np.int16)).mean(axis=2)
    mask = cv2.dilate(((diff > 14) | ((r - g > 35) & (g < 110))).astype(np.uint8), np.ones((7, 7), np.uint8))
    ys, xs = np.where(mask > 0); pad = 26
    x0, x1 = max(xs.min() - pad, 0), min(xs.max() + pad, sub.shape[1] - 1)
    y0, y1 = max(ys.min() - pad, 0), min(ys.max() + pad, sub.shape[0] - 1)
    if clean_frame is not None:
        patch = frame(clean_frame)[reg][y0:y1 + 1, x0:x1 + 1]
    else:
        inp = cv2.GaussianBlur(cv2.inpaint(sub, mask, 7, cv2.INPAINT_TELEA), (0, 0), 2.0)
        patch = inp[y0:y1 + 1, x0:x1 + 1]
    X0, Y0 = x0 + reg[1].start, y0 + reg[0].start
    worst = 0
    for i in range(seg[0], seg[1] + 1, 3):
        d = np.abs(frame(i)[Y0:Y0 + patch.shape[0], X0:X0 + patch.shape[1]].astype(np.int16) - patch.astype(np.int16)).mean(axis=2)
        d[mask[y0:y1 + 1, x0:x1 + 1] > 0] = 0
        worst = max(worst, int(cv2.erode((d > 40).astype(np.uint8), np.ones((7, 7), np.uint8)).sum()))
    if worst > 200:
        raise SystemExit("the presenter enters the %s card region (%d px); choose a tighter region" % (name, worst))
    path = os.path.join(work, "patch_%s.png" % name); cv2.imwrite(path, feather(patch))
    return path, X0, Y0


def lower_thirds(work):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    cream, brass, soft = (251, 249, 245), (206, 168, 96), (236, 229, 220)
    def franklin(size, weight):
        f = ImageFont.truetype(os.path.join(CACHE, "LibreFranklin[wght].ttf"), size); f.set_variation_by_axes([weight]); return f
    def spectral(size):
        return ImageFont.truetype(os.path.join(CACHE, "Spectral-Medium.ttf"), size)
    def card(lines, out, x=112, y=84):
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); cy = y; right = x
        for text, font, col, tracking, gap in lines:
            if tracking:
                cx = x
                for ch in text:
                    d.text((cx, cy), ch, font=font, fill=col); cx += font.getlength(ch) + tracking
                right = max(right, cx)
            else:
                d.text((x, cy), text, font=font, fill=col); right = max(right, x + font.getlength(text))
            bb = font.getbbox("Hg"); cy += (bb[3] - bb[1]) + gap
        bottom = cy - lines[-1][4]
        d.rectangle([x - 40, y + 10, x - 37, bottom + 8], fill=brass)
        scrim = Image.new("L", (W, H), 0); ImageDraw.Draw(scrim).rounded_rectangle([x - 130, y - 70, right + 120, bottom + 80], radius=90, fill=118)
        dark = Image.new("RGBA", (W, H), (26, 12, 14, 0)); dark.putalpha(scrim.filter(ImageFilter.GaussianBlur(70)))
        Image.alpha_composite(dark, im).save(out)
    card([("Spencer Alexander", spectral(88), cream, 0, 32), ("PRINCIPAL", franklin(30, 600), brass, 8, 24),
          ("Spencer Alexander Lawyers, Box Hill", franklin(42, 400), soft, 0, 0)], os.path.join(work, "lt_name.png"))
    card([("Speak with Spencer", spectral(80), cream, 0, 28), ("(03) 9125 8355", franklin(72, 600), cream, 2, 24),
          ("YOUR FIRST CALL IS FREE", franklin(32, 600), brass, 8, 24), ("spenceralexander.com.au", franklin(46, 400), soft, 0, 0)],
         os.path.join(work, "lt_call.png"))


def assemble(ff, src, work, a, patches, poster_at):
    os.makedirs(OUT, exist_ok=True)
    talk = a["talk_end"] / FPS; card_start = a["card_start"] / FPS; master = duration(ff, src)
    total = round(talk + HOLD + (master - card_start), 3)
    n_in, n_len, n_out, n_olen = NAME_CARD; c_in, c_len, c_olen = CALL_CARD; c_out = round(talk - c_olen, 3)
    (p1, x1, y1), (p2, x2, y2) = patches
    s1, s2 = a["segs"][0], a["segs"][1]
    graph = (f"[1:v]format=rgba[p1];[2:v]format=rgba[p2];"
             f"[3:v]format=rgba,fade=t=in:st={n_in}:d={n_len}:alpha=1,fade=t=out:st={n_out}:d={n_olen}:alpha=1[n];"
             f"[4:v]format=rgba,fade=t=in:st={c_in}:d={c_len}:alpha=1,fade=t=out:st={c_out}:d={c_olen}:alpha=1[c];"
             f"[0:v]trim=0:{talk},setpts=PTS-STARTPTS[t0];"
             f"[t0][p1]overlay={x1}:{y1}:enable='between(t,0,{round(s1[1] / FPS + 0.15, 3)})':shortest=1[t1];"
             f"[t1][p2]overlay={x2}:{y2}:enable='between(t,{round(s2[0] / FPS - 0.15, 3)},{talk})':shortest=1[t2];"
             f"[t2]{GRADE}[t3];[t3][n]overlay=0:0:shortest=1[t4];[t4][c]overlay=0:0:shortest=1,"
             f"tpad=stop_mode=clone:stop_duration={HOLD},fade=t=in:st=0:d=0.9:color={WINE},fade=t=out:st={talk}:d={HOLD}:color={WINE},format=yuv420p,fps={FPS}[talk];"
             f"[5:v]setpts=PTS-STARTPTS,fps={FPS},fade=t=in:st=0:d=0.6:color={WINE},format=yuv420p[cardv];"
             f"[talk][cardv]concat=n=2:v=1:a=0,split=2[full][half];[half]scale=1280:-2[v720];"
             f"[0:a]atrim=0:{total},afade=t=in:st=0:d=0.04,asplit=2[aud1][aud2]")
    common = ["-c:v", "libx264", "-preset", "slow", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", str(FPS), "-movflags", "+faststart", "-c:a", "aac", "-ar", "48000", "-t", str(total)]
    loop = ["-loop", "1", "-framerate", str(FPS), "-i"]
    subprocess.check_call([ff, "-hide_banner", "-loglevel", "error", "-y", "-i", src, *loop, p1, *loop, p2, *loop, os.path.join(work, "lt_name.png"), *loop, os.path.join(work, "lt_call.png"),
        "-ss", str(card_start), "-i", src, "-filter_complex", graph,
        "-map", "[full]", "-map", "[aud1]", *common, "-crf", "21", "-level", "4.1", "-b:a", "128k", os.path.join(OUT, "spencer-alexander-intro-1080.mp4"),
        "-map", "[v720]", "-map", "[aud2]", *common, "-crf", "22", "-level", "4.0", "-b:a", "112k", os.path.join(OUT, "spencer-alexander-intro-720.mp4")])
    subprocess.check_call([ff, "-hide_banner", "-loglevel", "error", "-y", "-ss", str(poster_at), "-i", os.path.join(OUT, "spencer-alexander-intro-1080.mp4"),
                           "-frames:v", "1", "-vf", "scale=1600:-2", "-q:v", "4", os.path.join(OUT, "poster-1600.jpg")])
    return total


def main():
    if len(sys.argv) < 2:
        print(__doc__); return 2
    src = os.path.abspath(sys.argv[1]); poster_at = float(sys.argv[2]) if len(sys.argv) > 2 else 14.6
    ff = ffmpeg(); ensure_fonts(); work = os.path.join(CACHE, "work"); os.makedirs(work, exist_ok=True)
    print("analysing"); a = analyse(src); print("  ", json.dumps(a))
    if len(a["segs"]) != 2:
        raise SystemExit("expected two card intervals in the master, found %d: %s" % (len(a["segs"]), a["segs"]))
    print("patches")
    clean = (a["segs"][0][1] + a["segs"][1][0]) // 2        # a frame of the first take with no card on it
    patches = [card_patch(src, a["segs"][0], work, "name", clean_frame=clean), card_patch(src, a["segs"][1], work, "call")]
    lower_thirds(work)
    print("assembling"); total = assemble(ff, src, work, a, patches, poster_at)
    for f in ("spencer-alexander-intro-1080.mp4", "spencer-alexander-intro-720.mp4", "poster-1600.jpg"):
        print("  %-36s %9d bytes" % (f, os.path.getsize(os.path.join(OUT, f))))
    print("film length %.2f s: update the VideoObject duration on index.html if it changed" % total)
    return 0


if __name__ == "__main__":
    sys.exit(main())
