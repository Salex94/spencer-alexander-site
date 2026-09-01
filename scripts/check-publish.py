#!/usr/bin/env python3
"""Pre-publish gate for a new insight article.

    python3 scripts/check-publish.py            # checks the newest article
    python3 scripts/check-publish.py <slug>     # e.g. child-support-australia

Encodes the mechanical parts of the weekly publishing specification so
compliance does not depend on anyone remembering them. Every check that can be
verified by machine is verified here. Exit status 0 = safe to publish.

Judgement calls this CANNOT check, which still need a human or a careful read:
  - whether every legal claim is actually true
  - whether the topic genuinely avoids rehashing an existing article
  - whether the writing is any good
"""

import glob
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

PHONE_TEL = "tel:+61391258355"
PHONE_TEXT = "(03) 9125 8355"
EMAIL = "contact@spenceralexander.com.au"
BASE = "https://www.spenceralexander.com.au/"

results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))


def read(path):
    return open(path, encoding="utf-8").read()


def jsonld(html):
    out = []
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            out.append(json.loads(block))
        except json.JSONDecodeError as e:
            out.append(e)
    return out


def newest_article():
    best = (None, "")
    for f in glob.glob("insight-*.html"):
        m = re.search(r'"datePublished":\s*"(\d{4}-\d{2}-\d{2})"', read(f))
        if m and m.group(1) > best[1]:
            best = (f, m.group(1))
    return best[0]


def main():
    if not os.path.exists("insights.html"):
        print("error: run from the repo root")
        return 1

    page = ("insight-%s.html" % sys.argv[1]) if len(sys.argv) > 1 else newest_article()
    if not page or not os.path.exists(page):
        print("error: article not found: %s" % page)
        return 1

    art = read(page)
    ins = read("insights.html")
    idx = read("index.html")
    feed = read("feed.xml")
    smap = read("sitemap.xml")
    url = BASE + page          # canonical .html URL (SEO surfaces keep this)
    purl = "/" + page[:-len(".html")]  # clean URL used by clickable links

    # ---- JSON-LD -------------------------------------------------------
    blocks = jsonld(art)
    bad = [b for b in blocks if isinstance(b, json.JSONDecodeError)]
    check("article JSON-LD parses", not bad, str(bad[0]) if bad else "%d blocks" % len(blocks))
    types = [b.get("@type") for b in blocks if isinstance(b, dict)]
    check("article has Article + BreadcrumbList", "Article" in types and "BreadcrumbList" in types, str(types))

    article_ld = next((b for b in blocks if isinstance(b, dict) and b.get("@type") == "Article"), {})
    iso = article_ld.get("datePublished", "")
    check("datePublished present", bool(iso), iso)
    check("dateModified >= datePublished", article_ld.get("dateModified", "") >= iso if iso else False,
          article_ld.get("dateModified", ""))
    check('inLanguage is en-AU', article_ld.get("inLanguage") == "en-AU", str(article_ld.get("inLanguage")))
    check("articleSection set", article_ld.get("articleSection") in
          ("Family Law", "Wills & Estates", "Commercial Law"), str(article_ld.get("articleSection")))
    author = article_ld.get("author", {})
    check("author @id + url present",
          author.get("@id") == BASE + "about.html#spencer-alexander" and bool(author.get("url")),
          str(author.get("@id")))
    check("mainEntityOfPage matches canonical", article_ld.get("mainEntityOfPage") == url,
          str(article_ld.get("mainEntityOfPage")))

    for b in blocks:
        if isinstance(b, dict) and b.get("@type") == "FAQPage":
            body = re.sub(r"<[^>]+>", " ", art)
            body = re.sub(r"\s+", " ", body.replace("&#39;", "'").replace("&amp;", "&"))
            missing = [q["name"] for q in b.get("mainEntity", [])
                       if q.get("name", "").replace("&", "&")[:45] not in body]
            check("FAQ questions appear in visible body", not missing, "; ".join(missing[:2]))

    # ---- dates consistent across every surface --------------------------
    if iso:
        d = datetime.strptime(iso, "%Y-%m-%d")
        visible = "%d %s %d" % (d.day, MONTHS[d.month - 1], d.year)
        utc = d.replace(hour=9) - timedelta(hours=10)
        rfc = "%s, %02d %s %d %02d:00:00 +0000" % (
            ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][utc.weekday()],
            utc.day, MONTHS[utc.month - 1], utc.year, utc.hour)
        check("visible date in article meta", visible in art, visible)
        check("sitemap lastmod", "<loc>%s</loc>" % url in smap and "<lastmod>%s</lastmod>" % iso in smap, iso)
        check("feed pubDate (09:00 +1000 as UTC)", rfc in feed, rfc)
        check("feed lastBuildDate matches", "<lastBuildDate>%s</lastBuildDate>" % rfc in feed, rfc)
        check("insights blogPost datePublished", '"%s", "datePublished": "%s"' % (page, iso) in
              ins.replace(BASE, ""), iso)

    # ---- listing surfaces ----------------------------------------------
    check("article is insights.html hero", ('class="featured" href="%s"' % purl) in ins)
    check("article first in feed.xml", feed.index(page) < (feed.index("insight-", feed.index("<item>"))
          if "<item>" in feed else len(feed)) or feed.count(page) > 0)
    first_item = feed.split("<item>")[1] if "<item>" in feed else ""
    check("article is FIRST feed item", page in first_item)
    check("article in llms.txt", page in read("llms.txt") if os.path.exists("llms.txt") else True)

    # Owner approval 1 Sep 2026: every article is linked from the Related
    # reading list of its practice-area page (its internal-authority hub).
    hub = {"Family Law": "family-law.html",
           "Wills & Estates": "wills-and-estates.html",
           "Commercial Law": "commercial-law.html"}.get(article_ld.get("articleSection"))
    check("article linked from its practice page",
          bool(hub) and ('href="%s"' % purl) in read(hub), hub or "unknown section")

    teaser = idx[idx.find("Guidance you can use."):]
    teaser = teaser[:teaser.find("Read all insights")]
    check("homepage teaser has exactly 3 cards", teaser.count('class="post-card"') == 3,
          str(teaser.count('class="post-card"')))
    cards = re.findall(r'href="(/insight-[^"#?]+)"', teaser)
    check("article is FIRST homepage card", bool(cards) and cards[0] == purl, str(cards[:3]))

    order = re.findall(r'"datePublished": "(\d{4}-\d{2}-\d{2})"', ins)
    check("insights blogPost newest-first", order == sorted(order, reverse=True), str(order[:3]))

    # ---- well-formedness, links, assets ---------------------------------
    for f in ("feed.xml", "sitemap.xml"):
        try:
            ET.parse(f)
            check("%s well-formed" % f, True)
        except ET.ParseError as e:
            check("%s well-formed" % f, False, str(e))

    # Clean links ("/contact") are served by GitHub Pages from contact.html,
    # so resolve them against the file that will actually be served.
    def resolves(href):
        path = href.split("#")[0].split("?")[0]
        if path in ("", "/"):
            return os.path.exists("index.html")
        path = path.lstrip("/")
        return os.path.exists(path) or ("." not in os.path.basename(path)
                                        and os.path.exists(path + ".html"))

    broken = [h for h in set(re.findall(r'href="(?!https?:|tel:|mailto:)([^"]+)"', art))
              if not resolves(h)]
    check("internal links resolve", not broken, ", ".join(broken))
    missing_img = [s for s in set(re.findall(r'src="(?!https?:)([^"]+)"', art))
                   if not os.path.exists(s.split("?")[0])]
    check("local assets exist", not missing_img, ", ".join(missing_img))
    check("no external in-page <img>", not re.search(r'<img[^>]+src="https?:', art))

    # Owner instruction 15 Aug 2026 (confirmed same day: applies to every
    # future edit and new page): clickable links show clean URLs with no
    # .html ("/contact", "/insight-<slug>"), while canonical, og:url, JSON-LD,
    # sitemap, feed and llms.txt keep the indexed .html addresses. GitHub
    # Pages serves both forms, so the indexed URLs never move.
    leaky = []
    for f in sorted(glob.glob("*.html")):
        n = len(re.findall(r'<a\s[^>]*href="(?!https?:)[^"]*\.html', read(f)))
        if n:
            leaky.append("%s: %d" % (f, n))
    check("clickable links extension-free (site-wide)", not leaky, "; ".join(leaky))
    check("canonical + og:url keep .html", ('rel="canonical" href="%s"' % url) in art
          and ('content="%s"' % url) in art, url)

    # The article template ships with a noindex robots meta (the template page
    # itself must not be indexed). A published article must have flipped it,
    # or the article silently never appears in search.
    rmeta = re.search(r'<meta name="robots" content="([^"]+)"', art)
    check("article robots meta allows indexing",
          bool(rmeta) and "index" in rmeta.group(1) and "noindex" not in rmeta.group(1),
          rmeta.group(1) if rmeta else "missing")

    # ---- house style ----------------------------------------------------
    check("byline present", 'Spencer Alexander</a>, Principal' in art)
    check("phone + email match site", PHONE_TEL in art and PHONE_TEXT in art and EMAIL in art)
    check("disclaimer present", "general information only, not legal advice" in art)
    ref = read(sorted(glob.glob("insight-*.html"), key=os.path.getmtime)[-1])
    check("stylesheet links match a current article",
          re.findall(r'<link rel="stylesheet"[^>]+>', art) == re.findall(r'<link rel="stylesheet"[^>]+>', ref))
    placeholders = [p for p in ("TODO", "Lorem", "{{", "PLACEHOLDER", "XXX") if p in art]
    check("no template placeholders", not placeholders, ", ".join(placeholders))

    # Owner instruction 6 Aug 2026: no dashes in the writing. Em dashes, en
    # dashes and spaced hyphens are banned everywhere in the article (title,
    # description, body, JSON-LD). Hyphenated compound words are still fine.
    # Articles published on or before 2026-08-06 predate the rule.
    if iso > "2026-08-06":
        dashes = [d for d in ("—", "–", " - ") if d in art]
        check("no dashes in writing (em/en/spaced hyphen)", not dashes,
              ", ".join(repr(d) for d in dashes))

    title = re.search(r"<title>(.*?)</title>", art)
    desc = re.search(r'<meta name="description" content="(.*?)">', art)
    check("title ends with firm suffix", title and title.group(1).endswith("| Spencer Alexander Lawyers"))
    check("meta description 120-170 chars", desc and 120 <= len(desc.group(1)) <= 170,
          str(len(desc.group(1)) if desc else 0))

    m = re.search(r'<div class="article__body">(.*?)<p style="margin-top:28px', art, re.S)
    if m:
        words = len(re.sub(r"<[^>]+>", " ", m.group(1)).split())
        check("body word count 1100-1900", 1100 <= words <= 1900, "%d words" % words)

    # ---- one photograph per article -------------------------------------
    rc = os.system("python3 scripts/check-article-images.py >/dev/null 2>&1")
    check("every article has its own photograph", rc == 0,
          "run scripts/check-article-images.py for detail")

    # ---- resource pages (added 1 Sep 2026: the gate was blind to them) ---
    for rf in sorted(glob.glob("resource-*.html")):
        res = read(rf)
        rurl = BASE + rf
        rblocks = jsonld(res)
        rbad = [b for b in rblocks if isinstance(b, json.JSONDecodeError)]
        rtypes = [b.get("@type") for b in rblocks if isinstance(b, dict)]
        check("%s JSON-LD parses" % rf, not rbad, str(rbad[0]) if rbad else "%d blocks" % len(rblocks))
        check("%s has BreadcrumbList + a main type" % rf,
              "BreadcrumbList" in rtypes and any(t in rtypes for t in ("HowTo", "FAQPage", "Article")),
              str(rtypes))
        check("%s canonical + og:url keep .html" % rf,
              ('rel="canonical" href="%s"' % rurl) in res and ('content="%s"' % rurl) in res, rurl)
        rmeta2 = re.search(r'<meta name="robots" content="([^"]+)"', res)
        check("%s robots meta allows indexing" % rf,
              bool(rmeta2) and "noindex" not in rmeta2.group(1), rmeta2.group(1) if rmeta2 else "missing")
        rtitle = re.search(r"<title>(.*?)</title>", res)
        check("%s title ends with firm suffix" % rf,
              rtitle and rtitle.group(1).endswith("| Spencer Alexander Lawyers"))
        check("%s disclaimer present" % rf, "general information only, not legal advice" in res)
        check("%s in sitemap" % rf, ("<loc>%s</loc>" % rurl) in smap)
        check("%s in llms.txt" % rf, rf in read("llms.txt") if os.path.exists("llms.txt") else True)
        check("%s listed on resources hub" % rf,
              os.path.exists("resources.html") and rf[:-len(".html")] in read("resources.html"))
        rdate = re.search(r'"datePublished":\s*"(\d{4}-\d{2}-\d{2})"', res)
        if rdate and rdate.group(1) > "2026-08-06":
            rdashes = [d for d in ("—", "–", " - ") if d in res]
            check("%s no dashes in writing" % rf, not rdashes, ", ".join(repr(d) for d in rdashes))

    # ---- faq.html schema (added 1 Sep 2026: edited weekly, was ungated) --
    if os.path.exists("faq.html"):
        fq = read("faq.html")
        fblocks = jsonld(fq)
        fbad = [b for b in fblocks if isinstance(b, json.JSONDecodeError)]
        check("faq.html JSON-LD parses", not fbad, str(fbad[0]) if fbad else "")
        fpage = next((b for b in fblocks if isinstance(b, dict) and b.get("@type") == "FAQPage"), {})
        qs = fpage.get("mainEntity", [])
        visible = len(re.findall(r"<details", fq))
        check("faq.html question count matches visible entries", len(qs) == visible,
              "%d in JSON-LD, %d visible" % (len(qs), visible))
        unanswered = [q.get("name", "?")[:40] for q in qs
                      if not q.get("acceptedAnswer", {}).get("text", "").strip()]
        check("faq.html every question answered", not unanswered, "; ".join(unanswered[:2]))
        names = [q.get("name", "").strip().lower() for q in qs]
        dups = sorted({n for n in names if names.count(n) > 1})
        check("faq.html no duplicate questions", not dups, "; ".join(dups[:2]))

    # ---- site-wide link and asset resolution (added 1 Sep 2026) ----------
    wide_broken, wide_missing = [], []
    for f in sorted(glob.glob("*.html")):
        if f == "_article-template.html":
            continue
        body = read(f)
        for h in set(re.findall(r'href="(?!https?:|tel:|mailto:|#)([^"]+)"', body)):
            if not resolves(h):
                wide_broken.append("%s -> %s" % (f, h))
        for s in set(re.findall(r'src="(?!https?:|data:)([^"]+)"', body)):
            if not os.path.exists(s.split("?")[0].lstrip("/")):
                wide_missing.append("%s -> %s" % (f, s))
    check("internal links resolve (site-wide)", not wide_broken, "; ".join(wide_broken[:4]))
    check("local assets exist (site-wide)", not wide_missing, "; ".join(wide_missing[:4]))

    # ---- report ----------------------------------------------------------
    width = max(len(n) for n, _, _ in results)
    failed = 0
    print("Pre-publish gate: %s\n" % page)
    for name, ok, detail in results:
        print("  %s  %-*s  %s" % ("ok  " if ok else "FAIL", width, name, detail))
        failed += not ok
    print("\n%d checks, %d failed" % (len(results), failed))
    if failed:
        print("DO NOT PUBLISH until these are fixed.")
    else:
        print("Mechanical checks pass. Accuracy and freshness still need a human read.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
