#!/usr/bin/env python3
"""Prepare the home page film assets from an edited master.

Usage:  python3 scripts/prepare-home-video.py <master.mp4> [end_card_start_seconds]

Produces, in assets/video/:
  spencer-alexander-intro-1080.mp4   graded talking head, clean end card, 30 fps
  spencer-alexander-intro-720.mp4    the same at 1280x720 for narrow or slow devices
  poster-1600.jpg                    graded still from the clean first frame, used as the poster
  end-card.jpg                       the ungraded end card frame, shown when playback ends

Not produced here: end-card-small.jpg, the phone sized card rendered from
scripts/end-card-small.html with Playwright (see that file), and the caption
track spencer-alexander-intro.en.vtt, which is written by hand from the
spoken words with cue times from the audio.

The grade is the home page portrait grade translated to video: 22 percent sepia,
a multiply gradient from the wine tint at the top to the deep wine at the bottom,
a darkening toward the base, then a touch of saturation and contrast. It is
applied only up to the end card cut so the card keeps its true brand colours.
The cut time defaults to the one measured on the 5 September 2026 master; pass
the new one (ffmpeg scene detection at threshold 0.04 finds it) for a new edit.

Needs ffmpeg on PATH or the imageio-ffmpeg Python package (pip install
imageio-ffmpeg). Run scripts/check-publish.py afterwards.
"""
import os, shutil, subprocess, sys, tempfile

MIXER = "colorchannelmixer=rr=0.8665:rg=0.169:rb=0.0416:gr=0.0768:gg=0.931:gb=0.037:br=0.0598:bg=0.1175:bb=0.8088"
TOP = (0.841, 0.754, 0.770); BOT = (0.5745, 0.5196, 0.5333); DARK = (0.506, 0.465, 0.476)

def ffmpeg():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()

def gradient(path, w=1920, h=1080):
    rows = []
    for y in range(h):
        f = y / (h - 1)
        k = min(max((f - 0.58) / 0.42, 0.0), 1.0)
        rows.append(bytes(int(round(255 * (TOP[c] + (BOT[c] - TOP[c]) * f) * (1 - k * (1 - DARK[c])))) for c in range(3)) * w)
    with open(path, "wb") as fh:
        fh.write(b"P6\n%d %d\n255\n" % (w, h)); fh.write(b"".join(rows))

def main():
    if len(sys.argv) < 2:
        print(__doc__); return 2
    src = sys.argv[1]; cut = float(sys.argv[2]) if len(sys.argv) > 2 else 51.55
    ff = ffmpeg(); out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "video")
    os.makedirs(out, exist_ok=True)
    tmp = tempfile.mkdtemp(); grad = os.path.join(tmp, "grad.ppm"); gradient(grad)
    graded = "format=rgb24,%s,format=gbrp[base];[1:v]format=gbrp[g];[base][g]blend=all_mode=multiply:shortest=1,format=yuv420p,eq=saturation=1.05:contrast=1.04" % MIXER
    graph = ("[0:v]split=2[va][vb];[va]trim=0:%s,setpts=PTS-STARTPTS,%s[graded];[vb]trim=start=%s,setpts=PTS-STARTPTS,format=yuv420p[card];"
             "[graded][card]concat=n=2:v=1:a=0,fps=30,split=2[full][half];[half]scale=1280:-2[v720]") % (cut, graded, cut)
    common = ["-c:v", "libx264", "-preset", "slow", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", "30", "-movflags", "+faststart", "-c:a", "aac", "-ar", "48000"]
    subprocess.check_call([ff, "-hide_banner", "-loglevel", "error", "-y", "-i", src, "-loop", "1", "-framerate", "30", "-i", grad, "-filter_complex", graph,
        "-map", "[full]", "-map", "0:a", *common, "-crf", "22", "-level", "4.1", "-b:a", "128k", os.path.join(out, "spencer-alexander-intro-1080.mp4"),
        "-map", "[v720]", "-map", "0:a", *common, "-crf", "23", "-level", "4.0", "-b:a", "112k", os.path.join(out, "spencer-alexander-intro-720.mp4")])
    subprocess.check_call([ff, "-hide_banner", "-loglevel", "error", "-y", "-ss", "0", "-i", src, "-loop", "1", "-framerate", "30", "-i", grad, "-filter_complex",
        "[0:v]" + graded + ",scale=1600:-2[out]", "-map", "[out]", "-frames:v", "1", "-q:v", "4", os.path.join(out, "poster-1600.jpg")])
    subprocess.check_call([ff, "-hide_banner", "-loglevel", "error", "-y", "-ss", str(cut + 3.0), "-i", src, "-frames:v", "1", "-q:v", "2", os.path.join(out, "end-card.jpg")])
    shutil.rmtree(tmp, ignore_errors=True)
    for f in ("spencer-alexander-intro-1080.mp4", "spencer-alexander-intro-720.mp4", "poster-1600.jpg", "end-card.jpg"):
        print("%-36s %8.1f KB" % (f, os.path.getsize(os.path.join(out, f)) / 1024))
    print("update the VideoObject duration and uploadDate in index.html if the edit changed, then run scripts/check-publish.py")
    return 0

if __name__ == "__main__":
    sys.exit(main())
