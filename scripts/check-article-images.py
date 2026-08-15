#!/usr/bin/env python3
"""Verify that every insight article uses its own distinct photograph.

Run from the repo root:  python3 scripts/check-article-images.py

Why this exists
---------------
Photos in assets/photos/ are named after the source photograph, with an
optional "-N" suffix for an alternate crop of the SAME photograph, e.g.
    1609220136736.jpg      <- source photograph 1609220136736
    1609220136736-2.jpg    <- different crop, still the same photograph
Those two files have different bytes but look identical to a reader, so
uniqueness must be judged on the filename stem (the source photograph),
never on a checksum. Getting that wrong once shipped two articles with
visibly the same photo.

Exit status: 0 if every article has its own photograph, 1 otherwise.
"""

import glob
import os
import re
import sys
from collections import defaultdict

LISTING_PAGES = ("insights.html", "index.html")


def stem(filename):
    """Source photograph id: strip the directory, extension and -N crop suffix."""
    return re.sub(r"-\d+$", "", os.path.splitext(os.path.basename(filename))[0])


def article_photos():
    """Map source photograph -> set of insight articles whose card uses it."""
    used = defaultdict(set)
    for page in LISTING_PAGES:
        if not os.path.exists(page):
            continue
        html = open(page, encoding="utf-8").read()
        # Each card/hero is an <a href="/insight-*"> (clean URL, no .html since
        # 15 Aug 2026; the old .html form is still accepted) shortly followed
        # by its <img>.
        for m in re.finditer(
            r'href="/?(insight-[^"#?]+?)(?:\.html)?"[\s\S]{0,400}?src="assets/photos/([^"]+)"',
            html,
        ):
            used[stem(m.group(2))].add(m.group(1) + ".html")
    return used


def main():
    if not os.path.isdir("assets/photos"):
        print("error: run this from the repo root (assets/photos not found)")
        return 1

    all_photos = {stem(p) for p in glob.glob("assets/photos/*.jpg")}
    used = article_photos()
    articles = {a for arts in used.values() for a in arts}
    failures = []

    # 1. No photograph may be shared by two or more articles.
    for photo, arts in sorted(used.items()):
        if len(arts) > 1:
            failures.append(
                "photograph %s is used by %d articles: %s"
                % (photo, len(arts), ", ".join(sorted(arts)))
            )

    # 2. Every article that exists on disk should appear on the listing pages.
    on_disk = {os.path.basename(p) for p in glob.glob("insight-*.html")}
    missing = sorted(on_disk - articles)

    spare = sorted(all_photos - set(used))

    print("photographs in assets/photos : %d" % len(all_photos))
    print("insight articles with a card : %d" % len(articles))
    print("photographs free for reuse   : %d %s" % (len(spare), spare if spare else ""))
    if missing:
        print("articles with no listing card: %s" % ", ".join(missing))

    if failures:
        print("\nFAIL - duplicate photographs:")
        for f in failures:
            print("  - %s" % f)
        print(
            "\nFix: give the newer article its own photograph. If none is free, a new\n"
            "image must be added to assets/photos/ before that article can publish."
        )
        return 1

    print("\nPASS - every article has its own photograph.")
    if not spare:
        print(
            "WARNING: no spare photographs remain. The next new article needs a new\n"
            "image added to assets/photos/ (see CLAUDE.md, 'Article images')."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
