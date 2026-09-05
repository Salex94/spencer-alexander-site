#!/usr/bin/env python3
"""Refresh the Google rating and review count shown across the site.

The site shows the firm's Google star rating in several places, marked up
as <span data-google-rating>5.0</span> (the hero on index.html and
contact.html, the reviews section on index.html and the rail card on every
hub and article). The number must match what a visitor sees on Google, so
this script reads it from Google's public Maps embed for the listing (no API
key needed) and rewrites every marked span. The review count is read for
information only and is never written to the site: the owner does not want
the number of reviews stated anywhere (5 Sep 2026).

Usage:  python3 scripts/refresh-google-rating.py          # fetch and update
        python3 scripts/refresh-google-rating.py --check  # compare only

Exit 0 when the site matches Google (after updating, unless --check), exit 1
when --check finds a difference, exit 2 when Google could not be read. The
script never guesses: if the fetch or the parse fails it changes nothing.
"""
import glob, re, sys, urllib.request

EMBED = "https://maps.google.com/maps?q=Spencer+Alexander+Lawyers+Box+Hill&output=embed&hl=en"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
PAT = re.compile(r'"Spencer Alexander Lawyers",\[[^\]]*\],(\d+(?:\.\d+)?),"(\d+) reviews?"')

def live():
    req = urllib.request.Request(EMBED, headers={"User-Agent": UA, "Accept-Language": "en-AU,en;q=0.9"})
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read().decode("utf-8", "replace")
    m = PAT.search(body)
    if not m:
        raise RuntimeError("rating pattern not found in the embed page")
    return "%.1f" % float(m.group(1)), m.group(2)

def main():
    check = "--check" in sys.argv
    try:
        rating, count = live()
    except Exception as e:
        print("could not read Google:", e)
        return 2
    print("Google says: rating %s from %s reviews" % (rating, count))
    changed = []
    for f in sorted(glob.glob("*.html")):
        s = open(f, encoding="utf-8").read()
        s2 = re.sub(r'(<[a-z]+ [^>]*data-google-rating[^>]*>)[^<]*(</)', r'\g<1>' + rating + r'\g<2>', s)
        if s2 != s:
            changed.append(f)
            if not check:
                open(f, "w", encoding="utf-8").write(s2)
    if not changed:
        print("site already matches Google")
        return 0
    print(("would update" if check else "updated") + " %d files: %s" % (len(changed), ", ".join(changed)))
    print("remember to bump sitemap lastmod for the changed pages")
    return 1 if check else 0

if __name__ == "__main__":
    sys.exit(main())
