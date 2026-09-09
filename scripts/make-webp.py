#!/usr/bin/env python3
"""Encode a WebP sibling for every photograph the pages show inline (added 9 Sep 2026).

Every in-page <img src="assets/....jpg"> sits inside a <picture> whose first
<source type="image/webp"> points at the same stem with a .webp extension, so
browsers that can take WebP fetch about half the bytes and every other
browser takes the JPEG. Run this after adding a photograph; it only writes
files that are missing or older than their JPEG. check-publish.py's
"every in-page photograph has a WebP sibling" check fails until they exist.
Quality 78, method 6: measured indistinguishable from the JPEG crops on the
principal's portrait at 2x.
"""
import glob, os, re
from PIL import Image

refs = set()
for f in glob.glob("*.html"):
    s = open(f, encoding="utf-8").read()
    refs.update(re.findall(r'<img[^>]*\ssrc="(assets/[^"]+\.(?:jpg|jpeg|png))"', s))
    refs.update(re.findall(r'<source[^>]*\ssrcset="(assets/[^"]+\.(?:jpg|jpeg|png))"', s))
made = 0
for src in sorted(refs):
    if not os.path.exists(src) or src.startswith("assets/video/"):
        continue
    dst = src.rsplit(".", 1)[0] + ".webp"
    if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
        continue
    Image.open(src).convert("RGB").save(dst, "WEBP", quality=78, method=6)
    made += 1
    print("%s  %d -> %d bytes" % (dst, os.path.getsize(src), os.path.getsize(dst)))
print("webp files written:", made)
