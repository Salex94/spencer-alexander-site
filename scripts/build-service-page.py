#!/usr/bin/env python3
"""Build one service page from its content file (added 28 Sep 2026).

    python3 scripts/build-service-page.py playbooks/service-content/service-probate.json

Every service page is assembled from the same parts so that none can drift from
the approved design: the head, top bar, header, menus, footer and phone call bar
are copied from the page's practice hub exactly, with no navigation link marked
active; the rail call card is the hub's own; and the body uses only components
the hubs already use, namely the single column page hero with breadcrumbs, the
urgent strip, the In brief box, section heads with prose, service blocks, the
three step process row, the fee note, related reading, the questions and the
closing call. The content file holds the words; this script holds the design.
The page is written to the repository root as <slug>.html.
"""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.spenceralexander.com.au/"
ARROW = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>')
PHONE = ('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
         'stroke-linejoin="round" aria-hidden="true"><path d="M13.832 16.568a1 1 0 0 0 1.213-.303l.355-.465A2 2 0 0 1 17 15h3a2 2 0 0 1 2 2v3a2 '
         '2 0 0 1-2 2A18 18 0 0 1 2 4a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v3a2 2 0 0 1-.8 1.6l-.468.351a1 1 0 0 0-.292 1.233 14 14 0 0 0 6.392 6.384"/></svg>')
CHEVRON = ('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
           'stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>')
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def text(h):
    """Visible text of an HTML fragment, as the FAQ schema must carry it."""
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h))).strip()


def attr(s):
    return html.escape(s, quote=True)


def main(path, outdir=None):
    c = json.load(open(path, encoding="utf-8"))
    hub = open(os.path.join(ROOT, c["hub"] + ".html"), encoding="utf-8").read()
    slug, url = c["slug"], SITE + c["slug"] + ".html"
    date = c["date"]
    y, m, d = (int(x) for x in date.split("-"))
    month = "%s %d" % (MONTHS[m - 1], y)
    long_date = "%d %s %d" % (d, MONTHS[m - 1], y)
    # A fee note that quotes a price opens by saying whose fees these are, where, in what currency and as at
    # what day, so the paragraph can be quoted alone. It is written here and never in a content file.
    fees_line = ('These are the fees of Spencer Alexander Lawyers in Box Hill, Victoria, in Australian dollars, as at '
                 '<time class="fees-asat" datetime="%s">%s</time>, published by Spencer Alexander, Principal, at '
                 '<a href="/fees">spenceralexander.com.au/fees</a>.' % (date, long_date))
    if re.search(r"\$\d", c["fee"]["p"]):
        c["fee"]["p"] = fees_line + " " + c["fee"]["p"]
    # An answer that quotes one of the firm's fees ends with the same sentence, in the page and in its markup,
    # because an answer is the passage most often lifted for a question about cost.
    # What each figure in an answer is comes from the fee tool, which reads the record of sentences, so a court
    # charge that comes to equal one of the firm's fees is still told from it.
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import fees as fee_tool
    kinds = fee_tool.answer_kinds(path)
    for n, q in enumerate(c["faqs"]):
        a = q["a"].rstrip()
        figures = list(re.finditer(r"\$\d{1,3}(?:,\d{3})*(?:\.\d\d)?", a))
        if n >= len(kinds) or len(kinds[n]) != len(figures):
            raise SystemExit("%s: the fee tool could not match the answer to %r with its reading of the content file. "
                             "Write each question as q and then a, with nothing between them, so that the dated fee "
                             "sentence is never left out of an answer" % (path, q["q"]))
        kind = kinds[n]
        ours = [m for m, k in zip(figures, kind) if k == "fee"]
        if not ours:
            continue
        # the sentence goes straight after the last sentence that quotes one of the firm's own fees
        stop = a.find(". ", ours[-1].end())
        at = len(a) if stop < 0 else stop + 1
        early = [m.group(0) for m, k in zip(figures, kind) if m.start() < at and k in ("charge", "derived")]
        if early:
            raise SystemExit("%s: the answer to %r quotes a court or ASIC charge (%s) before the last of the firm's own "
                             "fees. Put the firm's fees first, so that the sentence that dates them cannot be read as "
                             "covering the charge" % (path, q["q"], ", ".join(early)))
        q["a"] = a[:at] + " " + fees_line + a[at:]

    # ---- head: the hub's, with this page's own title, description and addresses
    head_end = hub.index('  <script type="application/ld+json">')
    head = hub[:head_end]
    t, desc = c["title"], c["description"]
    head = re.sub(r"<title>[^<]*</title>", "<title>%s</title>" % html.escape(t, quote=False), head)
    for k in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        head = re.sub(r'(<meta %s content=")[^"]*(")' % re.escape(k), lambda mm: mm.group(1) + attr(desc) + mm.group(2), head)
    for k in ('property="og:title"', 'name="twitter:title"'):
        head = re.sub(r'(<meta %s content=")[^"]*(")' % re.escape(k), lambda mm: mm.group(1) + attr(t) + mm.group(2), head)
    head = re.sub(r'(<link rel="canonical" href=")[^"]*(")', r"\g<1>%s\2" % url, head)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*(")', r"\g<1>%s\2" % url, head)
    if c.get("og_image"):
        for k in ('property="og:image"', 'name="twitter:image"'):
            head = re.sub(r'(<meta %s content=")[^"]*(")' % re.escape(k), lambda mm: mm.group(1) + attr(c["og_image"]) + mm.group(2), head)
        head = re.sub(r'(<meta property="og:image:alt" content=")[^"]*(")', lambda mm: mm.group(1) + attr(c["og_image_alt"]) + mm.group(2), head)

    # ---- schema: Service with the hub's provider and areaServed, breadcrumbs, FAQPage
    hub_service = json.loads(re.search(r'<script type="application/ld\+json">\s*(\{\s*"@context": "https://schema.org",\s*"@type": "Service".*?)\s*</script>', hub, re.S).group(1))
    service = {"@context": "https://schema.org", "@type": "Service", "@id": url + "#service", "url": url,
               "name": c["service_name"], "serviceType": c["service_name"], "provider": hub_service["provider"],
               "areaServed": hub_service["areaServed"], "description": desc}
    if c.get("offers"):
        # a from price is marked as a minimum, as the fees page marks it, and never as a flat price
        fee_source = fee_tool.load()

        def spec(o):
            fee = fee_tool.offer_fee(fee_source, o["name"])
            key = "minPrice" if fee and fee["from"] else "price"
            return {"@type": "PriceSpecification", key: o["price"], "priceCurrency": "AUD", "valueAddedTaxIncluded": True}
        service["offers"] = [{"@type": "Offer", "name": o["name"], "price": o["price"], "priceCurrency": "AUD",
                              "url": SITE + "fees.html", "priceSpecification": spec(o)} for o in c["offers"]]
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
        {"@type": "ListItem", "position": 2, "name": text(c["hub_label"]), "item": SITE + c["hub"] + ".html"},
        {"@type": "ListItem", "position": 3, "name": c["service_name"], "item": url}]}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "dateModified": date,
           "author": {"@id": SITE + "about.html#spencer-alexander"}, "publisher": {"@id": SITE + "#firm"},
           "mainEntity": [{"@type": "Question", "name": text(q["q"]), "acceptedAnswer": {"@type": "Answer", "text": text(q["a"])}} for q in c["faqs"]]}
    ld = "".join('  <script type="application/ld+json">\n  %s\n  </script>\n' % json.dumps(o, ensure_ascii=False) for o in (service, crumbs, faq))

    # ---- chrome from the hub, no link active
    chrome = re.search(r'<body>.*?</header>\n', hub, re.S).group(0).replace(' class="is-active"', "")
    if c["hub"] == "family-law" and "data-quick-exit" not in chrome:
        chrome = chrome.replace('<a class="skip-link" href="#main">Skip to content</a>\n',
                                '<a class="skip-link" href="#main">Skip to content</a>\n  <a class="quick-exit" href="https://www.bom.gov.au/" data-quick-exit>Quick exit</a>\n', 1)
    tail = hub[hub.index("  <footer class=\"site-footer\">"):]
    rail_call = re.search(r'<div class="rail-card">.*?<p class="rail-card__meta">.*?</p>\n          </div>', hub, re.S).group(0)
    fee_icon = re.search(r'<div class="fee-note">\s*(<span class="icon-chip icon-chip--44">.*?</span>)', hub, re.S).group(1)

    out = [head, ld, "</head>\n", chrome, "\n  <main id=\"main\">\n"]
    # hero
    meta = "".join("<span>%s</span>" % s for s in c["meta"])
    out.append('''    <section class="field-dark">
      <div class="container pagehero">
        <nav class="crumbs" aria-label="Breadcrumb">
          <a href="/">Home</a>
          %s
          <a href="/%s">%s</a>
          %s
          <span>%s</span>
        </nav>
        <span class="eyebrow-light eyebrow-light--repeat">%s</span>
        <h1 class="pagehero__title">%s</h1>
        <p class="pagehero__lead">%s</p>
        <div class="pagehero__actions">
          <a class="btn btn--accent btn--lg" href="tel:+61391258355">
            %s
            Call (03) 9125 8355
          </a>
          <a class="btn btn--ghost btn--lg" href="/contact#enquiry">Send an enquiry</a>
        </div>
        <div class="pagehero__meta">%s</div>
      </div>
    </section>
''' % (CHEVRON, c["hub"], c["hub_label"], CHEVRON, c["crumb"], c["hub_label"],
       c["h1"].replace("Box Hill", '<span class="nowrap">Box Hill</span>'), c["lead"], PHONE, meta))

    # main column
    body = ['    <section class="section section--page">\n      <div class="container hub">\n        <div class="hub__main">\n']
    if c.get("urgent"):
        body.append('''          <div class="reach reach--urgent" style="margin-top:0;margin-bottom:clamp(24px,3vw,32px);">
            <span class="reach__mark" aria-hidden="true">!</span>
            <span class="reach__text"><strong>%s</strong> %s</span>
            <a href="tel:+61391258355">Call (03) 9125 8355 &rarr;</a>
          </div>
''' % (c["urgent"]["strong"], c["urgent"]["text"]))
    # The summary ends by saying who published it, when, and the legislation its statements rest on, so that
    # it can be quoted alone. The names are the page's own Sources, and the line is written here from the page's
    # date and "sources" under "brief" in the content file, each of which must be in the page's Sources line.
    named = c["brief"].get("sources") or []
    if not named:
        raise SystemExit("%s: brief needs sources, the legislation behind the In brief block's statements, taken "
                         "from the page's claims register" % path)
    stray = [a for a in named if ">%s</a>" % a not in c.get("sources", "")]
    if stray:
        raise SystemExit("%s: brief sources not in the page's Sources line: %s" % (path, ", ".join(stray)))
    # the year and the jurisdiction stay on the same line as the last word of the title
    held = [re.sub(r" (\d{4}) \((Vic|Cth)\)$", r"&nbsp;\1&nbsp;(\2)", a) for a in named]
    listed = held[0] if len(held) == 1 else ", ".join(held[:-1]) + " and " + held[-1]
    by = ('Published by Spencer Alexander, Principal, and updated on <time datetime="%s">%s</time>. Legislation: %s.'
          % (date, long_date, listed))
    body.append('          <div class="brief">\n            <span class="brief__k">In brief</span>\n            <p>%s</p>\n            <ul>\n%s            </ul>\n            <p class="brief__by">%s</p>\n          </div>\n'
                % (c["brief"]["entity"], "".join("              <li>%s</li>\n" % b for b in c["brief"]["bullets"]), by))
    for i, sec in enumerate(c["sections"]):
        body.append('''
          <div class="section-head svc-head"%s>
            <hr class="sa-rule">
            <span class="sa-eyebrow">%s</span>
            <h2 class="h2">%s</h2>
          </div>
''' % (' id="%s"' % sec["id"] if sec.get("id") else "", sec["eyebrow"], sec["h2"]))
        if sec.get("items"):
            body.append('          <div class="svc-grid">\n%s          </div>\n' % "".join(
                '            <div class="svc">\n              <h3 class="svc__title">%s</h3>\n              <p>%s</p>\n            </div>\n' % (it["t"], it["p"]) for it in sec["items"]))
        if sec.get("paras"):
            body.append('          <div class="prose">\n%s          </div>\n' % "".join("            <p>%s</p>\n" % p for p in sec["paras"]))
    body.append("        </div>\n\n        <aside class=\"rail\" aria-label=\"Talk to a lawyer\">\n          %s\n" % rail_call)
    if c.get("rail_quiet"):
        q = c["rail_quiet"]
        links = "".join('\n            <a class="card-link" href="%s"%s>%s %s</a>' % (l["href"], ' style="margin-top:10px;"' if j else "", l["label"], ARROW) for j, l in enumerate(q["links"]))
        body.append('          <div class="rail-card rail-card--quiet">\n            <div class="rail-card__t">%s</div>\n            <p class="rail-card__d">%s</p>%s\n          </div>\n' % (q["t"], q["d"], links))
    body.append("        </aside>\n      </div>\n    </section>\n")
    out += body

    # process and fee note
    steps = "".join('''            <div class="step">
              <span class="step__n">%d</span>
              <div class="step__t">%s</div>
              <div class="step__d">%s</div>
            </div>
''' % (i + 1, s["t"], s["d"]) for i, s in enumerate(c["process"]["steps"]))
    out.append('''
    <section class="section section--sunken">
      <div class="container">
        <div class="section-head">
          <hr class="sa-rule">
          <span class="sa-eyebrow">%s</span>
          <h2 class="h2">%s</h2>
        </div>
        <div class="steps process-row">
%s        </div>
        <div class="fee-note">
          %s
          <div>
            <h3 class="fee-note__t">%s</h3>
            <p class="fee-note__d">%s</p>
          </div>
        </div>
      </div>
    </section>
''' % (c["process"]["eyebrow"], c["process"]["h2"], steps, fee_icon, c["fee"]["t"], c["fee"]["p"]))

    # related reading and questions
    rel = "".join('            <a class="related__link" href="%s">%s %s</a>\n' % (r["href"], r["label"], ARROW) for r in c["related"])
    qs = "".join('''          <details class="faq-item">
            <summary class="faq-q">%s<span class="faq-q__ic"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14"/><path d="M5 12h14"/></svg></span></summary>
            <div class="faq-a"><p>%s</p></div>
          </details>
''' % (q["q"], q["a"]) for q in c["faqs"])
    sources = ""
    if c.get("sources"):
        sources = '        <p class="article-sources" style="margin-top:28px;font-size:var(--text-sm);color:var(--text-subtle);">Sources: %s</p>\n' % c["sources"]
    out.append('''
    <section class="section section--page">
      <div class="container">
        <div class="related">
          <span class="sa-eyebrow">Related reading</span>
          <div class="related__links">
%s          </div>
        </div>

        <div class="section-head">
          <hr class="sa-rule">
          <span class="sa-eyebrow">Good to know</span>
          <h2 class="h2">%s</h2>
        </div>
        <div class="faq-grid">
%s        </div>
        <a class="faq-more" href="/faq">More questions answered on our FAQ page %s</a>
%s        <p class="page-close" style="margin-top:28px;font-size:var(--text-sm);color:var(--text-subtle);">Published by Spencer Alexander, Principal, and updated on <time datetime="%s">%s</time>. This page reflects the law applying in Victoria as at %s. It is general information only, not legal advice, and does not take your circumstances into account.</p>
      </div>
    </section>
''' % (rel, c["faq_h2"], qs, ARROW, sources, date, long_date, month))

    # the closing band says how soon an enquiry is answered, and that the first call is free where its lead does not
    promise = "Enquiries are answered within one business day."
    if "first call is free" not in c["cta"]["lead"]:
        promise = "Your first call is free, and you speak with a lawyer. " + promise
    out.append('''
    <section class="field-wine cta">
      <div class="container container--lg">
        <span class="eyebrow-light">%s</span>
        <h2 class="cta__title">%s</h2>
        <p class="cta__lead">%s</p>
        <div class="cta__actions">
          <a class="btn btn--accent btn--lg" href="tel:+61391258355">
            %s
            Call (03) 9125 8355
          </a>
          <a class="btn btn--ghost btn--lg" href="/contact#enquiry">Send an enquiry</a>
        </div>
        <div class="cta__meta">%s</div>
      </div>
    </section>
  </main>

''' % (c["cta"]["eyebrow"], c["cta"]["title"], c["cta"]["lead"], PHONE, promise))
    out.append(tail)
    page = "".join(out)
    open(os.path.join(outdir or ROOT, slug + ".html"), "w", encoding="utf-8").write(page)
    print("built %s.html, %d words visible" % (slug, len(text(re.search(r"<main.*?</main>", page, re.S).group(0)).split())))


if __name__ == "__main__":
    args = sys.argv[1:]
    out = None
    if args and args[0] == "--out":        # build somewhere else, which is how the fee check compares a fresh build
        out, args = args[1], args[2:]
    for p in args:
        main(p, out)
