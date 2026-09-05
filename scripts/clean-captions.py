#!/usr/bin/env python3
"""Remove the burned in captions from the home page film master, frame by frame.

Reads raw bgr24 1920x1080 frames on stdin and writes them to stdout, so it sits
between an ffmpeg decode and an ffmpeg encode (scripts/prepare-home-video.py
wires this up). The white caption text is masked, stray highlights such as
shirt buttons are dropped, the soft drop shadow is caught in a second pass,
and every masked pixel is filled by linear interpolation between the nearest
clean pixels above and below in its column, feathered at the edges. Column
interpolation keeps the wall gradient and the shirt stripes intact, which
generic inpainting smears. Frames from the cut frame onward (the end card)
pass through untouched.

Usage: ffmpeg -i master.mp4 -f rawvideo -pix_fmt bgr24 - | python3 scripts/clean-captions.py <cut frame> | ffmpeg -f rawvideo -pix_fmt bgr24 -s 1920x1080 -r 30 -i - ...
Needs numpy and opencv-python-headless (pip install numpy opencv-python-headless).
"""
import cv2, numpy as np
Y0, Y1, X0, X1 = 915, 1075, 260, 1660
H = Y1 - Y0; W = X1 - X0
FEATHER = 5
def text_mask(roi, thr=222, chroma=34, dil=15):
    mn = roi.min(axis=2); mx = roi.max(axis=2)
    m = ((mn > thr) & ((mx - mn) < chroma)).astype(np.uint8)
    if not m.any(): return None
    n, lab, stats, cent = cv2.connectedComponentsWithStats(m, connectivity=8)
    if n <= 1: return None
    boxes = stats[1:, :4]; areas = stats[1:, 4]
    keep = np.ones(n - 1, bool)
    for i in range(n - 1):
        if areas[i] >= 150: continue
        x, y, w, h = boxes[i]
        # keep small pieces only if another piece sits within 40 px horizontally and 30 px vertically
        near = False
        for j in range(n - 1):
            if j == i: continue
            xj, yj, wj, hj = boxes[j]
            if abs((x + w / 2) - (xj + wj / 2)) - (w + wj) / 2 < 40 and abs((y + h / 2) - (yj + hj / 2)) < 30:
                near = True; break
        keep[i] = near
    if not keep.any(): return None
    m2 = np.isin(lab, np.nonzero(keep)[0] + 1).astype(np.uint8)
    if m2.sum() < 40: return None
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dil, dil))
    core = cv2.dilate(m2, k)
    # second pass for the soft drop shadow: in a ring around the text, pixels clearly darker than
    # the column interpolation predicts are shadow, and join the mask
    wide = cv2.dilate(m2, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31)))
    ring = (wide > 0) & (core == 0)
    pred = fill_vertical(roi, wide)
    lum = roi.astype(np.float32).mean(axis=2); plum = pred.mean(axis=2)
    shadow = ring & (lum < plum - 16)
    shadow = cv2.dilate(shadow.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    return np.maximum(core, shadow)
def fill_vertical(roi, m):
    rows = np.arange(H)[:, None].repeat(W, 1)
    clean = m == 0
    above = np.where(clean, rows, -1); above = np.maximum.accumulate(above, axis=0)
    below = np.where(clean, rows, H); below = np.minimum.accumulate(below[::-1], axis=0)[::-1]
    a = np.clip(above, 0, H - 1); b = np.clip(below, 0, H - 1)
    cols = np.arange(W)[None, :].repeat(H, 0)
    va = roi[a, cols].astype(np.float32); vb = roi[b, cols].astype(np.float32)
    da = (rows - above).astype(np.float32); db = (below - rows).astype(np.float32)
    da[above < 0] = 1e6; db[below >= H] = 1e6
    denom = da + db; denom[denom == 0] = 1
    wa = db / denom; wb = 1 - wa
    out = va * wa[..., None] + vb * wb[..., None]
    out[clean] = roi[clean]
    return out
def clean_frame(frame):
    roi = frame[Y0:Y1, X0:X1]
    m = text_mask(roi)
    if m is None: return frame
    filled = fill_vertical(roi, m)
    w = cv2.GaussianBlur(m.astype(np.float32), (0, 0), FEATHER)
    w = np.clip(w * 1.6, 0, 1)[..., None]
    out = roi.astype(np.float32) * (1 - w) + filled * w
    frame[Y0:Y1, X0:X1] = np.clip(out, 0, 255).astype(np.uint8)
    return frame
if __name__ == '__main__':
    import sys
    cut = int(sys.argv[1]) if len(sys.argv) > 1 else 10**9
    fs = 1920 * 1080 * 3; i = 0
    inp = sys.stdin.buffer; outp = sys.stdout.buffer
    while True:
        buf = inp.read(fs)
        if len(buf) < fs: break
        f = np.frombuffer(buf, np.uint8).reshape(1080, 1920, 3).copy()
        if i < cut: f = clean_frame(f)
        outp.write(f.tobytes()); i += 1
    sys.stderr.write('frames %d\n' % i)
