#!/usr/bin/env python3
"""Set each article's sitemap <lastmod> to its JSON-LD dateModified.

Run after any batch edit of insight articles (added 8 Sep 2026 when every
lead was rewritten in one pass); check-publish.py's "sitemap lastmod matches
dateModified" check fails until the two agree. Core pages are not touched:
their lastmod is bumped by hand to the Melbourne date of the change.
"""
import glob, re

sm = open("sitemap.xml", encoding="utf-8").read(); changed = 0
for f in sorted(glob.glob("insight-*.html")):
    m = re.search(r'"dateModified":\s*"(\d{4}-\d{2}-\d{2})"', open(f, encoding="utf-8").read())
    if not m:
        continue
    loc = "<loc>https://www.spenceralexander.com.au/%s</loc>" % f
    i = sm.find(loc)
    if i < 0:
        print("not in sitemap:", f); continue
    j = sm.find("<lastmod>", i); k = sm.find("</lastmod>", j)
    if sm[j + 9:k] != m.group(1):
        sm = sm[:j + 9] + m.group(1) + sm[k:]; changed += 1
open("sitemap.xml", "w", encoding="utf-8").write(sm)
print("sitemap entries updated:", changed)
