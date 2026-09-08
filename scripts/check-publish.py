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


def html_unescape(t):
    import html as _h
    return _h.unescape(t)


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
        # The sitemap entry for THIS article must carry a lastmod equal to
        # the article's dateModified (strengthened 5 Sep 2026: the old check
        # only looked for the published date anywhere in the file).
        entry = re.search(r"<url>\s*<loc>%s</loc>\s*<lastmod>([^<]+)</lastmod>" % re.escape(url), smap)
        want = article_ld.get("dateModified", iso)
        check("sitemap lastmod matches dateModified", bool(entry) and entry.group(1) == want,
              "%s vs %s" % (entry.group(1) if entry else "missing", want))
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

    # Currency line: "as at <Month YYYY>" must be the month of dateModified
    # (added 5 Sep 2026: the template literal had propagated "July 2026" onto
    # articles published in March and onto ones modified in September).
    cm = re.search(r"reflects the law applying in Victoria as at ([A-Z][a-z]+ \d{4})", art)
    dm = article_ld.get("dateModified", iso)
    want_month = "%s %s" % (["January", "February", "March", "April", "May", "June", "July",
                              "August", "September", "October", "November", "December"][int(dm[5:7]) - 1], dm[:4]) if dm else ""
    check("currency line month matches dateModified", bool(cm) and cm.group(1) == want_month,
          "%s vs %s" % (cm.group(1) if cm else "missing", want_month))

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

    # Site chrome and house style on the core pages (added 5 Sep 2026 with the
    # v3 redesign): every page shares one footer and mobile call bar, carries a
    # skip link and a main landmark, no page describes the firm as a
    # specialist (the firm holds no accredited specialisation), and the core
    # pages carry no dash punctuation (owner instruction 6 Aug 2026, applied
    # site-wide in the 5 Sep 2026 review).
    core = ["index.html", "family-law.html", "wills-and-estates.html", "commercial-law.html",
            "about.html", "contact.html", "faq.html", "insights.html", "resources.html",
            "privacy.html", "thank-you.html", "404.html", "_article-template.html"]
    ref_foot = re.search(r'<footer class="site-footer">.*?</footer>', idx, re.S)
    odd_foot, no_skip, specialist, dashed = [], [], [], []
    for f in sorted(glob.glob("*.html")):
        body = read(f)
        foot = re.search(r'<footer class="site-footer">.*?</footer>', body, re.S)
        if ref_foot and (not foot or foot.group(0) != ref_foot.group(0)):
            odd_foot.append(f)
        if body.count('class="skip-link"') != 1 or body.count('<main id="main">') != 1:
            no_skip.append(f)
        if f in core:
            if re.search(r"specialis", body, re.I):
                specialist.append(f)
            if "\u2014" in body or "\u2013" in body:
                dashed.append(f)
    check("footer identical on every page", not odd_foot, ", ".join(odd_foot[:4]))
    check("exactly one skip link + main landmark on every page", not no_skip, ", ".join(no_skip[:4]))
    check("no specialist wording on core pages", not specialist, ", ".join(specialist[:4]))
    check("no dashes on core pages", not dashed, ", ".join(dashed[:4]))

    # Meta descriptions on indexable pages other than articles sit between
    # 120 and 160 characters (added 8 Sep 2026: eight pages had drifted to
    # between 165 and 180 and were being truncated in results).
    off_desc = []
    for f in sorted(glob.glob("*.html")):
        if f.startswith("insight-") or f == "_article-template.html":
            continue
        body = read(f)
        if re.search(r'<meta name="robots" content="[^"]*noindex', body):
            continue
        d = re.search(r'<meta name="description" content="(.*?)">', body)
        if not d or not 120 <= len(d.group(1)) <= 160:
            off_desc.append("%s (%d)" % (f, len(d.group(1)) if d else 0))
    check("page descriptions 120-160 chars (site-wide)", not off_desc, ", ".join(off_desc[:4]))

    # Every article lead answers the title question first and stays short:
    # at most 70 words in the article__lead paragraph (added 8 Sep 2026 when
    # every lead was rewritten to open with the direct answer).
    long_lead = []
    for f in sorted(glob.glob("insight-*.html")):
        m = re.search(r'<p class="article__lead">(.*?)</p>', read(f), re.S)
        words = len(re.sub(r"<[^>]+>", " ", m.group(1)).split()) if m else 0
        if not m or words > 70:
            long_lead.append("%s (%d)" % (f, words))
    check("article lead at most 70 words (site-wide)", not long_lead, ", ".join(long_lead[:4]))

    # The About page carries an archive of every article (added 8 Sep 2026):
    # a new article must be added to its practice area list there.
    about = read("about.html")
    unlisted = [f for f in sorted(glob.glob("insight-*.html")) if 'href="/%s"' % f[:-5] not in about]
    check("every article listed in the about.html archive", not unlisted, ", ".join(unlisted[:4]))

    # Every article carries a related reading block and an honest read time
    # (added 8 Sep 2026 with the top tier benchmark round).
    no_related, bad_time = [], []
    for f in sorted(glob.glob("insight-*.html")):
        body = read(f)
        if 'class="related__link"' not in body:
            no_related.append(f)
        m = re.search(r'<div class="article__body">(.*?)<p style="margin-top:28px', body, re.S)
        rt = re.search(r"(\d+) min read", body)
        if m and rt:
            words = len(re.sub(r"<[^>]+>", " ", m.group(1)).split())
            want = max(3, round(words / 230))
            if abs(int(rt.group(1)) - want) > 1:
                bad_time.append("%s (%s vs %d)" % (f, rt.group(1), want))
    check("every article has related reading", not no_related, ", ".join(no_related[:4]))
    check("article read times match their length", not bad_time, ", ".join(bad_time[:4]))

    # FAQ schema answers must be the visible answers, word for word (added 8 Sep
    # 2026: an answer engine that finds the schema and the page disagreeing
    # trusts neither).
    faq = read("faq.html"); drift = []
    def plain(t):
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html_unescape(t))).strip()
    ld = [b for b in jsonld(faq) if isinstance(b, dict) and b.get("@type") == "FAQPage"]
    items = re.findall(r'<summary class="faq-q">(.*?)<span class="faq-q__ic">.*?<div class="faq-a">(.*?)</div>\s*</details>', faq, re.S)
    visible = {plain(q): plain(a) for q, a in items}
    for q in (ld[0].get("mainEntity", []) if ld else []):
        name = plain(q.get("name", "")); ans = plain(q.get("acceptedAnswer", {}).get("text", ""))
        if name not in visible:
            drift.append("missing on page: %s" % name[:40])
        elif visible[name] != ans:
            drift.append("differs: %s" % name[:40])
    check("FAQ schema answers match the visible answers", ld and not drift, "; ".join(drift[:3]))

    # ---- 9 Sep 2026: GEO verification round ------------------------------
    # The same FAQ equality on every article (h3.article-q + p) and hub.
    sdrift = []
    for f in sorted(glob.glob("insight-*.html")) + ["family-law.html", "commercial-law.html", "wills-and-estates.html"]:
        h = read(f)
        if f.startswith("insight-"):
            pairs = re.findall(r'<h3 class="article-q"[^>]*>(.*?)</h3>\s*<p>(.*?)</p>', h, re.S)
        else:
            pairs = re.findall(r'<summary class="faq-q">(.*?)<span class="faq-q__ic">.*?<div class="faq-a">(.*?)</div>\s*</details>', h, re.S)
        vis = {plain(q): plain(a) for q, a in pairs}
        for b in jsonld(h):
            if isinstance(b, dict) and b.get("@type") == "FAQPage":
                for q in b.get("mainEntity", []):
                    name = plain(q.get("name", "")); ans = plain(q.get("acceptedAnswer", {}).get("text", ""))
                    if name not in vis:
                        sdrift.append("%s missing: %s" % (f, name[:30]))
                    elif vis[name] != ans:
                        sdrift.append("%s differs: %s" % (f, name[:30]))
    check("FAQ schema answers match the visible answers (site-wide)", not sdrift, "; ".join(sdrift[:3]))

    # The header practice menus list each hub's six services on every page
    # (the propagation script once matched a pattern the hubs no longer had
    # and pushed empty menus to every page; nobody noticed for a day).
    svc_ids = {hub: re.findall(r'<div class="svc" id="(svc-[^"]+)"', read(hub + ".html"))
               for hub in ("family-law", "wills-and-estates", "commercial-law")}
    menu_bad = []
    for f in sorted(glob.glob("*.html")):
        h = read(f)
        if '<nav class="site-nav"' not in h:
            continue
        for hub, ids in svc_ids.items():
            links = re.findall(r'href="/%s#(svc-[^"]+)"' % hub, h)
            if len(ids) != 6 or links != ids:
                menu_bad.append("%s %s %d" % (f, hub, len(links)))
    check("practice menus list six services on every page", not menu_bad, "; ".join(menu_bad[:3]))

    # Any other "as at Month YYYY" inside an article must agree with its
    # currency line (the child support article once carried two months).
    cur_bad = []
    for f in sorted(glob.glob("insight-*.html")):
        h = read(f)
        cm = re.search(r"reflects the law applying in Victoria as at ([A-Z][a-z]+ \d{4})", h)
        others = set(re.findall(r"\bas at ([A-Z][a-z]+ \d{4})", h))
        if cm and others - {cm.group(1)}:
            cur_bad.append("%s: %s" % (f, ", ".join(sorted(others - {cm.group(1)}))))
    check("every dated currency phrase matches the currency line", not cur_bad, "; ".join(cur_bad[:3]))

    # One firm entity: every JSON-LD object carrying the #firm @id must agree
    # with the full node on index.html on every property it repeats.
    FIRM = BASE + "#firm"
    canon = next((b for b in jsonld(read("index.html")) if isinstance(b, dict) and b.get("@id") == FIRM), None)
    def _walk(o, out):
        if isinstance(o, dict):
            if o.get("@id") == FIRM and len(o) > 1:
                out.append(o)
            for v in o.values():
                _walk(v, out)
        elif isinstance(o, list):
            for v in o:
                _walk(v, out)
    firm_bad = []
    for f in sorted(glob.glob("*.html")):
        nodes = []
        _walk(jsonld(read(f)), nodes)
        for n in nodes:
            for k, v in n.items():
                if k in ("@id", "@context") or canon is None or k not in canon:
                    continue
                if isinstance(v, dict) and set(v) == {"@id"}:
                    continue
                if canon[k] != v:
                    firm_bad.append("%s %s" % (f, k))
    check("firm node consistent across pages", canon is not None and not firm_bad, "; ".join(sorted(set(firm_bad))[:4]))

    # Dates that answer engines read: the FAQ page's visible reviewed date,
    # the FAQPage nodes on faq.html and the hubs against the sitemap, the
    # llms.txt Last updated line, and the Open Graph article dates.
    FULL = ["January", "February", "March", "April", "May", "June", "July",
            "August", "September", "October", "November", "December"]
    smap_all = read("sitemap.xml")
    fq = read("faq.html")
    fld = next((b for b in jsonld(fq) if isinstance(b, dict) and b.get("@type") == "FAQPage"), {})
    rv = re.search(r"Last reviewed (\d{1,2}) ([A-Z][a-z]+) (\d{4})", fq)
    got = "%s-%02d-%02d" % (rv.group(3), FULL.index(rv.group(2)) + 1, int(rv.group(1))) if rv and rv.group(2) in FULL else ""
    check("faq.html reviewed date matches its FAQPage dateModified", got and got == fld.get("dateModified"),
          "%s vs %s" % (got, fld.get("dateModified")))
    hub_bad = []
    for hub in ("faq.html", "family-law.html", "commercial-law.html", "wills-and-estates.html"):
        fp = next((b for b in jsonld(read(hub)) if isinstance(b, dict) and b.get("@type") == "FAQPage"), {})
        entry = re.search(r"<url>\s*<loc>%s</loc>\s*<lastmod>([^<]+)</lastmod>" % re.escape(BASE + hub), smap_all)
        if not (fp.get("dateModified") and fp.get("author") and fp.get("publisher") and entry and entry.group(1) == fp["dateModified"]):
            hub_bad.append(hub)
    check("FAQPage nodes carry author, publisher and the sitemap date", not hub_bad, ", ".join(hub_bad))
    lu = re.search(r"Last updated: (\d{1,2}) ([A-Z][a-z]+) (\d{4})", read("llms.txt"))
    lu_iso = "%s-%02d-%02d" % (lu.group(3), FULL.index(lu.group(2)) + 1, int(lu.group(1))) if lu and lu.group(2) in FULL else ""
    newest = max(re.findall(r"<lastmod>(\d{4}-\d{2}-\d{2})</lastmod>", smap_all))
    check("llms.txt Last updated matches the newest sitemap lastmod", lu_iso == newest, "%s vs %s" % (lu_iso, newest))
    og_bad = []
    for f in sorted(glob.glob("insight-*.html")):
        h = read(f)
        a = next((b for b in jsonld(h) if isinstance(b, dict) and b.get("@type") == "Article"), {})
        pt = re.search(r'property="article:published_time" content="([^"]+)"', h)
        mt = re.search(r'property="article:modified_time" content="([^"]+)"', h)
        if not (pt and mt and pt.group(1) == a.get("datePublished") and mt.group(1) == a.get("dateModified", a.get("datePublished"))):
            og_bad.append(f)
    check("Open Graph article dates match the Article schema", not og_bad, ", ".join(og_bad[:3]))

    # Google rating markup: every page that shows the rating must show the same
    # number, in the shape scripts/refresh-google-rating.py rewrites, and no
    # page may state the number of reviews (owner instruction, 5 Sep 2026).
    ratings, pages, counted = set(), 0, []
    for f in sorted(glob.glob("*.html")):
        h = read(f)
        r = re.findall(r'data-google-rating[^>]*>([^<]*)<', h)
        if r:
            pages += 1
        ratings.update(r)
        if "data-google-reviews" in h or re.search(r"\b\d+ (client )?reviews\b", h):
            counted.append(f)
    ok = pages > 0 and len(ratings) == 1 and re.fullmatch(r"\d\.\d", next(iter(ratings)))
    check("Google rating markup consistent (site-wide)", ok, "%d pages, ratings %s" % (pages, sorted(ratings)))
    check("review count never stated on the site", not counted, ", ".join(counted[:4]))

    # JSON-LD objects must not repeat a key: parsers keep only the last value silently
    def _no_dup(pairs):
        seen = set()
        for k, _ in pairs:
            if k in seen:
                raise ValueError("duplicate JSON-LD key: " + k)
            seen.add(k)
        return dict(pairs)
    dups = []
    for f in sorted(glob.glob("*.html")):
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', read(f), re.S):
            try:
                json.loads(block, object_pairs_hook=_no_dup)
            except ValueError as e:
                dups.append("%s: %s" % (f, e))
    check("JSON-LD has no duplicate keys (site-wide)", not dups, "; ".join(dups[:3]))
    check("index.html reviews section links to Google reviews", "search.google.com/local/reviews?placeid=" in read("index.html") and 'class="review-card"' in read("index.html"))

    # Privacy link placement (owner correction 1 Sep 2026: footer Firm column
    # only, exactly once, never the navigation or mobile menu).
    nav_priv, foot_priv = [], []
    for f in sorted(glob.glob("*.html")):
        body = read(f)
        for pat in (r'<nav class="site-nav".*?</nav>', r'<nav class="mobile-menu".*?</nav>'):
            for b in re.findall(pat, body, re.S):
                if "/privacy" in b:
                    nav_priv.append(f)
        if 'footer-col__h">Firm' in body:
            foot = re.search(r'<footer class="site-footer".*?</footer>', body, re.S)
            n = foot.group(0).count('<a href="/privacy">') if foot else 0
            if n != 1:
                foot_priv.append("%s: %d" % (f, n))
    check("privacy link never in navigation", not nav_priv, ", ".join(nav_priv[:4]))
    check("privacy link exactly once per footer", not foot_priv, ", ".join(foot_priv[:4]))

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
