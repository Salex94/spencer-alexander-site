#!/usr/bin/env python3
"""One maintained source for every fee the site publishes (added 23 Nov 2026).

playbooks/fees.json holds each fee once: its name, its total including GST, whether it
is a "from" price, its scope as the fees page words it, and the phrases that identify it
in a sentence. It also holds what the courts and ASIC charge, with the day each was read
and the day the figures stop being current. This script keeps every rendition in step
with that file, and proves that it is: the rows, the at a glance list, the four prices in
the hero, the table of court and government charges and the OfferCatalog on fees.html,
every sentence that quotes a fee or a charge on any page, every meta description and
JSON-LD string, llms.txt, feed.xml, the service content files and the service pages built
from them.

    python3 scripts/fees.py check               every rendition agrees with the source; exit 1 if not
    python3 scripts/fees.py apply [YYYY-MM-DD]  after editing playbooks/fees.json, rewrite every
                                                rendition and move the dates of the pages that changed
                                                (today in Melbourne when a price changes and no date is given)
    python3 scripts/fees.py stamp YYYY-MM-DD FILE...     move the dates of the named pages to that day
    python3 scripts/fees.py stamp YYYY-MM-DD --since REF  the same for every page whose own words changed since a
                                                git ref; a page that differs only in its header, footer, rail
                                                cards, version keys or dates is left alone
    python3 scripts/fees.py snapshot            record every sentence that quotes a fee or charge, after reading
                                                each new or changed one against playbooks/fees.json
    python3 scripts/fees.py use FILE [YYYY-MM-DD]   put a list of totals, {"totals": {fee id: total}}, into the
                                                source and apply it
    python3 scripts/fees.py where [id]          list every place each fee and charge is quoted
    python3 scripts/fees.py table               print the schedule

Only Spencer changes a price. To change one: edit "total" (and "from" or "scope" if they
change) in playbooks/fees.json, run apply with the Melbourne date of the change, read the
diff, then run scripts/check-publish.py, which runs check as one of its gates. A court or
ASIC charge is changed the same way, in "charges", after reading the body's own schedule.

Every price carries its date. The lead of fees.html says whose fees these are, where, in what currency and
as at what day, and a WebPage node and the sitemap carry the same day; stamp and apply move all three together.
The same sentence, which also says who published the fees and where, opens each service page's fee note that
quotes a price and closes each answer on a service page that quotes one, written by the page builder with the
page's own date. A hub or the FAQ page may carry it by hand at the end of an answer about cost, and stamp and apply
move its day with the page. check fails when any of these is missing or disagrees.

Every sentence that quotes a figure is on record. playbooks/fees-renditions.json holds each such sentence with
its figures replaced by the fee or charge each belongs to. check fails when a sentence that quotes a figure is new,
has changed or has gone, and prints it with the fee each figure was tied to. Read each against playbooks/fees.json,
then run snapshot. That is what catches two fees' figures swapped inside one sentence, a court charge that is right
for another court, and a worked total that no longer adds up, none of which the nearness rule below can see. A change
of price through apply needs no new snapshot, because the record holds the fee and not the amount.

How a quoted amount is tied to its fee. An amount such as $495 belongs to several fees, so
a bare figure is never trusted. A sentence on record keeps the tie the record gives each of
its figures, whatever the amounts become, so two fees that come to share an amount are never
confused. A sentence that is not yet on record is tied by nearness: the script takes the
sentence around the figure, then the paragraph, and looks for the phrases in "terms" of the
fees and charges that carry that amount, and passes the figure only when one of them is
named. check reports such a sentence until it has been read and recorded with snapshot.
Where a figure's fee is named only in the paragraph around its sentence, as in "Each is $495
including GST.", the record holds the paragraph with the sentence, amounts apart, so that a
change to the paragraph is a change to the sentence and it is read again.
apply rewrites only figures the record ties, read as the schedule stood before the edit, and
stops, writing nothing, when the pages and the record differ or when one figure stands for
two fees that have come to differ.

A trial price. apply moves dates as well as figures, so a price tried and then changed back
through apply leaves the pages dated the day of the trial. To drop a trial that was never
published, discard it with git checkout and leave apply out of it.
"""
import glob, html, json, os, re, subprocess, sys, tempfile
from collections import Counter
from html.parser import HTMLParser
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, "playbooks", "fees.json")
SITE = "https://www.spenceralexander.com.au/"
AMOUNT = re.compile(r"\$\d{1,3}(?:,\d{3})*(?:\.\d\d)?")
BLOCK_TAG = re.compile(r"</?(?:p|li|h[1-6]|div|section|ul|ol|td|tr|th|title|item|description|script|dd|dt|"
                       r"figcaption|blockquote|summary|details|button|label|option|header|footer|main|nav|aside|"
                       r"table|caption|thead|tbody)\b[^>]*>", re.I)
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
          "October", "November", "December"]
NOTICES = []        # what the last check wants read soon, for the gate to show


def load():
    return json.load(open(SOURCE, encoding="utf-8"))


def money(n):
    return "${:,}".format(int(n))


def amount_text(value):
    """$1,980 for a whole number of dollars and $2,538.70 where there are cents."""
    v = Decimal(str(value))
    return "${:,.0f}".format(v) if v == v.to_integral() else "${:,.2f}".format(v)


def before_gst(total):
    v = (Decimal(total) / Decimal("1.1")).quantize(Decimal("0.01"), ROUND_HALF_UP)
    return "${:,.0f}".format(v) if v == v.to_integral() else "${:,.2f}".format(v)


def long_date(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return "%d %s %d" % (d, MONTHS[m - 1], y)


def melbourne_today():
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("Australia/Melbourne")).date()
    except Exception:
        return (datetime.utcnow() + timedelta(hours=10)).date()


def real_date(text):
    """A day given on the command line, as YYYY-MM-DD: a real day, and not one that has yet to come."""
    try:
        day = datetime.strptime(text, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        raise SystemExit("%r is not a date. Write the day as YYYY-MM-DD, such as 2026-11-23." % (text,))
    if day.strftime("%Y-%m-%d") != text:
        raise SystemExit("%r is not written as YYYY-MM-DD." % (text,))
    if day > melbourne_today():
        raise SystemExit("%s has not come yet. Give the day the change is published, today in Melbourne at the latest." % text)
    if (day.year, day.month) < (melbourne_today().year, melbourne_today().month):
        raise SystemExit("%s is in a month that has passed. A page is dated the day it is published, so give today's "
                         "date in Melbourne." % text)
    return text


def files():
    """Every file that can carry a fee, in a fixed order."""
    out = sorted(f for f in glob.glob(os.path.join(ROOT, "*.html")) if not os.path.basename(f).startswith("_"))
    # a page in a folder would be published too, so it is read too (none exists; the gate's own rules bar most)
    for sub in sorted(glob.glob(os.path.join(ROOT, "*", "**", "*.html"), recursive=True)):
        top = os.path.relpath(sub, ROOT).split(os.sep)[0]
        if top not in ("playbooks", "scripts", "assets", "styles", "node_modules") and not top.startswith((".", "_")):
            out.append(sub)
    out += [os.path.join(ROOT, "llms.txt"), os.path.join(ROOT, "feed.xml")]
    out += sorted(glob.glob(os.path.join(ROOT, "playbooks", "service-content", "service-*.json")))
    return out


def rel(path):
    return os.path.relpath(path, ROOT)


# ---------------------------------------------------------------- fees.html: generated parts

def row_html(fee):
    name = '<a href="%s">%s</a>' % (fee["link"], fee["name"]) if fee.get("link") else fee["name"]
    pre = "from " if fee["from"] else ""
    return ('<div class="fee" id="fee-%s"><h3 class="fee__name">%s</h3><p class="fee__price">%s%s</p>'
            '<p class="fee__gst">%s%s plus GST</p><p class="fee__scope">%s</p></div>'
            % (fee["id"], name, pre, money(fee["total"]), pre, before_gst(fee["total"]), fee["scope"]))


def catalog(data):
    items = []
    for fee in data["fees"]:
        offered = {"@type": "Service", "name": fee["name"], "provider": {"@id": SITE + "#firm"}}
        if fee.get("schema_url"):
            offered["url"] = fee["schema_url"]
        spec = {"@type": "PriceSpecification", "priceCurrency": "AUD", "valueAddedTaxIncluded": True}
        spec["minPrice" if fee["from"] else "price"] = fee["total"]
        items.append({"@type": "Offer", "itemOffered": offered, "priceCurrency": "AUD", "price": fee["total"],
                      "priceSpecification": spec})
    return {"@context": "https://schema.org", "@type": "OfferCatalog", "@id": SITE + "fees.html#fees",
            "name": "Fixed fees, Spencer Alexander Lawyers", "url": SITE + "fees.html", "itemListElement": items}


def hero_strip(data):
    by_id = {f["id"]: f for f in data["fees"]}
    spans = "".join('<span><a href="#fee-%s">%s %s%s</a></span>'
                    % (fid, by_id[fid]["hero_label"], "from " if by_id[fid]["from"] else "", money(by_id[fid]["total"]))
                    for fid in data.get("hero", []))
    return '<p class="pagehero__meta pagehero__prices">%s</p>' % spans


def glance(data):
    """Every fee at a glance: one short row for each fee, by practice, linking to its full row."""
    cols = []
    for g in data["groups"]:
        rows = "".join('<li><a href="#fee-%s"><span class="fee-index__name">%s</span><span class="fee-index__price">%s%s</span></a></li>'
                       % (f["id"], f.get("short", f["name"]), "from " if f["from"] else "", money(f["total"]))
                       for f in data["fees"] if f["group"] == g["id"])
        cols.append('<div class="fee-index__col"><h3 class="fee-index__h"><a href="#%s">%s</a></h3><ul>%s</ul></div>'
                    % (g["id"], g["name"], rows))
    return '<div class="fee-index">%s</div>' % "".join(cols)


def charges_block(data):
    """The table of what the courts and ASIC charge, with the day it was read and its sources."""
    ch = data["charges"]
    bodies = []
    for g in ch["groups"]:
        rows = ['<tr class="charges__group"><th colspan="2" scope="rowgroup">%s</th></tr>' % g["heading"]]
        for it in ch["items"]:
            if it["group"] != g["id"]:
                continue
            cell = "No fee" if Decimal(it["amount"]) == 0 else amount_text(it["amount"])
            label = it["label"]
            if it.get("note"):
                label += '<span class="charges__note">%s%s</span>' % (it["note"][:1].upper(), it["note"][1:])
            rows.append('<tr id="charge-%s"><th scope="row">%s</th><td>%s</td></tr>' % (it["id"], label, cell))
        bodies.append("<tbody>%s</tbody>" % "".join(rows))
    links = ['<a href="%s" target="_blank" rel="noopener">%s</a>' % (s["url"], s["label"]) for s in ch["sources"]]
    src = links[0] if len(links) == 1 else ", ".join(links[:-1]) + " and " + links[-1]
    return ('<div class="charges-block"><table class="charges"><caption>Court and government charges from %s</caption>'
            '<thead><tr><th scope="col">Charge</th><th scope="col">Amount</th></tr></thead>%s</table>'
            '<p class="charges__source">Read on %s from %s. These charges are set by regulation, not by us, '
            'and usually change on 1 July.</p></div>'
            % (long_date(ch["valid_from"]), "".join(bodies), long_date(ch["read"]), src))


ROW_RX = re.compile(r'<div class="fee" id="fee-([^"]+)">.*?</div>')
ASAT_RX = re.compile(r'(<time class="fees-asat" datetime=")(\d{4}-\d{2}-\d{2})(">)([^<]*)(</time>)')
LEAD_ASAT_RX = re.compile(r'<p class="article__lead">These are the fees of Spencer Alexander Lawyers in Box Hill, Victoria, '
                          r'in Australian dollars, as at <time class="fees-asat" datetime="(\d{4}-\d{2}-\d{2})">[^<]*</time>, '
                          r'published by Spencer Alexander, Principal, at spenceralexander\.com\.au/fees\.')
# The sentence that opens or closes every passage quoting the firm's fees, so that the passage can be quoted alone:
# whose fees, where, the currency, the day, who published them and where. In a page's words the day sits in a
# time element, which ASAT_RX reads, and in its markup the sentence is plain text, which DATED_PLAIN_RX reads.
DATED_PLAIN_RX = re.compile(r"(These are the fees of Spencer Alexander Lawyers in Box Hill, Victoria, in Australian dollars, as at )"
                            r"(\d{1,2} [A-Z][a-z]+ \d{4})(, published by Spencer Alexander, Principal, at spenceralexander\.com\.au/fees\.)")
STRIP_RX = re.compile(r'<p class="pagehero__meta pagehero__prices">.*?</p>')
GLANCE_RX = re.compile(r'<div class="fee-index">.*?</ul></div></div>')
CHARGES_RX = re.compile(r'<div class="charges-block">.*?</div>', re.S)
CAT_RX = re.compile(r'\{"@context": "https://schema.org", "@type": "OfferCatalog".*?(?=\n\s*</script>)', re.S)


def fees_page():
    return open(os.path.join(ROOT, "fees.html"), encoding="utf-8").read()


def strip00(t):
    return t[:-3] if t.endswith(".00") else t


def published_schedule():
    """The amounts fees.html shows now, by fee id: the schedule as it stood before an edit."""
    out = {}
    for fid, price in re.findall(r'<div class="fee" id="fee-([^"]+)">.*?<p class="fee__price">([^<]+)</p>', fees_page()):
        out[fid] = (int(re.sub(r"[^\d]", "", price)), price.startswith("from"))
    return out


def published_charges():
    """The charges fees.html shows now, by charge id, as amount text."""
    out = {}
    for cid, cell in re.findall(r'<tr id="charge-([^"]+)"><th scope="row">.*?</th><td>(.*?)</td></tr>', fees_page()):
        m = AMOUNT.search(cell)
        out[cid] = strip00(m.group(0)) if m else "$0"
    return out


def published_since():
    """The day the charges on fees.html took effect, as the page words it: the date before an edit."""
    m = re.search(r"<caption>Court and government charges from (\d{1,2} [A-Z][a-z]+ \d{4})</caption>", fees_page())
    return m.group(1) if m else None


def render_fees_page(data, text):
    by_id = {f["id"]: f for f in data["fees"]}
    seen = []

    def sub(m):
        seen.append(m.group(1))
        return row_html(by_id[m.group(1)]) if m.group(1) in by_id else m.group(0)
    text = ROW_RX.sub(sub, text)
    missing = [f["id"] for f in data["fees"] if f["id"] not in seen]
    extra = [s for s in seen if s not in by_id]
    twice = sorted(k for k, n in Counter(seen).items() if n > 1)
    if missing or extra or twice:
        raise SystemExit("fees.html rows and playbooks/fees.json disagree: missing rows %s, rows with no fee %s, "
                         "rows that appear twice %s. Add or remove the row by hand, then run again."
                         % (missing, extra, twice))
    cat = json.dumps(catalog(data), ensure_ascii=False)
    if not CAT_RX.search(text):
        raise SystemExit("fees.html has no OfferCatalog block to regenerate")
    text = CAT_RX.sub(lambda m: cat, text, count=1)
    for rx, block in ((STRIP_RX, hero_strip(data)), (GLANCE_RX, glance(data)), (CHARGES_RX, charges_block(data))):
        if not rx.search(text):
            raise SystemExit("fees.html has lost a generated block: %s" % rx.pattern[:44])
        text = rx.sub(lambda m, b=block: b, text, count=1)
    return text


# ---------------------------------------------------------------- everything that carries an amount

def things(data, fee_amounts=None, charge_amounts=None):
    """id -> {amount, value, terms, kind, from}. fee_amounts and charge_amounts override the source,
    which gives the schedule as it stood before an edit."""
    out = {}
    for f in data["fees"]:
        total, frm = (fee_amounts or {}).get(f["id"], (f["total"], f["from"]))
        out[f["id"]] = {"amount": money(total), "value": Decimal(total), "terms": f["terms"], "kind": "fee", "from": frm}
    for it in data.get("charges", {}).get("items", []):
        text = (charge_amounts or {}).get(it["id"], amount_text(it["amount"]))
        out[it["id"]] = {"amount": text, "value": Decimal(text[1:].replace(",", "")), "terms": it["terms"],
                         "kind": "charge", "from": False}
    for dv in data.get("derived", []):
        if all(p in out for p in dv["parts"]):
            value = sum(out[p]["value"] for p in dv["parts"])
            out[dv["id"]] = {"amount": amount_text(value), "value": value, "terms": dv["terms"], "kind": "derived",
                             "from": False}
    return out


# ---------------------------------------------------------------- finding what a figure refers to

def generated_spans(path, text):
    """Regions of fees.html that are generated outright, so are not resolved figure by figure."""
    if os.path.basename(path) != "fees.html":
        return []
    spans = [m.span() for m in ROW_RX.finditer(text)]
    for rx in (CAT_RX, STRIP_RX, GLANCE_RX, CHARGES_RX):
        m = rx.search(text)
        if m:
            spans.append(m.span())
    return spans


def in_json(path, text, pos):
    if path.endswith(".json"):
        return True
    a = text.rfind('<script type="application/ld+json">', 0, pos)
    return a >= 0 and text.find("</script>", a) > pos


def quoted(text, pos, end):
    """The quoted string that holds text[pos:end], honouring backslash escapes."""
    i = pos
    while i > 0:
        i = text.rfind('"', 0, i)
        if i <= 0 or text[i - 1] != "\\":
            break
    j = end
    while True:
        j = text.find('"', j)
        if j < 0 or text[j - 1] != "\\":
            break
        j += 1
    return max(i, 0) + 1, (j if j >= 0 else len(text))


def block_bounds(path, text, pos, end):
    """Start and end of the paragraph, attribute or JSON string holding the figure."""
    if in_json(path, text, pos) or text.rfind("<", 0, pos) > text.rfind(">", 0, pos):
        return quoted(text, pos, end)
    a = 0
    for m in BLOCK_TAG.finditer(text, max(0, pos - 6000), pos):
        a = m.end()
    nl = text.rfind("\n\n", 0, pos)
    if not path.endswith(".html"):
        nl = text.rfind("\n", 0, pos)
    a = max(a, nl + 1)
    m = BLOCK_TAG.search(text, end)
    b = m.start() if m else len(text)
    nl = text.find("\n\n" if path.endswith(".html") else "\n", end)
    if nl >= 0:
        b = min(b, nl)
    return a, b


def plain(s):
    s = re.sub(r"<[^>]*>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s.replace("\\n", " ").replace('\\"', '"')))


def context(path, text, pos, end):
    """(sentence, offset of the figure in it, block, offset in the block) as plain lower case text."""
    a, b = block_bounds(path, text, pos, end)
    marked = plain(text[a:pos]) + "\x00" + plain(text[pos:end]) + "\x00" + plain(text[end:b])
    marked = re.sub(r"\s+", " ", marked)
    i = marked.index("\x00")
    j = marked.index("\x00", i + 1)
    block = (marked[:i] + marked[i + 1:j] + marked[j + 1:]).lower()
    # the sentence: back to the last full stop, question or exclamation mark followed by a space
    left = max(marked.rfind(". ", 0, i), marked.rfind("? ", 0, i), marked.rfind("! ", 0, i))
    right_candidates = [x for x in (marked.find(". ", j), marked.find("? ", j), marked.find("! ", j)) if x >= 0]
    right = min(right_candidates) if right_candidates else len(marked)
    sent = marked[left + 1:right].replace("\x00", "").lower()
    return sent, i - (left + 1), block, i


def pick(all_things, cands, sent, sent_at, block, block_at):
    """The one thing among cands that the sentence, or failing that the paragraph, names."""
    for scope, at in ((sent, sent_at), (block, block_at)):
        hits = []
        for tid in cands:
            best = None
            for term in all_things[tid]["terms"]:
                for m in re.finditer(term, scope):
                    # distance from the figure; a name just before the figure wins a tie
                    d = at - m.end() if m.end() <= at else m.start() - at + 0.5
                    if d >= 0 and (best is None or d < best):
                        best = d
            if best is not None:
                hits.append((best, tid))
        if len(hits) == 1:
            return hits[0][1], None, scope
        if len(hits) > 1:
            hits.sort()
            if hits[0][0] < hits[1][0]:
                return hits[0][1], [h[1] for h in hits], scope
            return None, [h[1] for h in hits], scope
    return None, [], ""


def beside(terms, sent, at, n):
    """True where a fee is named right beside the figure, as in "a single will is $495" or "$495 for a single
    will": the figure is that fee's own, whatever else the sentence goes on to name."""
    for term in terms:
        for m in re.finditer(term, sent):
            if 0 <= at - m.end() <= 12 or 0 <= m.start() - (at + n) <= 8:
                return True
    return False


def occurrences(path, text):
    skip = generated_spans(path, text)
    for m in AMOUNT.finditer(text):
        if any(a <= m.start() < b for a, b in skip):
            continue
        yield m


def is_before_gst(text, m):
    return text[m.end():m.end() + 9] == " plus GST"


def scan(data, all_things, path, text):
    """Yield (match, id or None, note) for every dollar figure outside the generated regions. note is
    "ok", "other", "before-gst", "shared:id,id" or a description of what is wrong."""
    not_fees = set(data.get("other_amounts", []))
    minimum = money(data["minimum"]) if data.get("minimum") else None
    last_fee, last_block = None, (0, 0)
    for m in occurrences(path, text):
        if is_before_gst(text, m):
            same = last_fee and last_block[0] <= m.start() < last_block[1]
            yield m, (last_fee if same else None), "before-gst"
            continue
        shown = strip00(m.group(0))
        cands = [tid for tid, th in all_things.items() if th["amount"] == shown and th["value"] != 0]
        if not cands:
            yield m, None, ("other" if m.group(0) in not_fees or shown in not_fees else "no fee or charge has this amount")
            last_fee = None
            continue
        sent, sat, block, bat = context(path, text, m.start(), m.end())
        if shown == minimum and any(re.search(t, sent) for t in data.get("minimum_terms", [])):
            yield m, None, "other"                     # the firm's minimum, stated as such
            last_fee = None
            continue
        tid, rivals, scope = pick(all_things, cands, sent, sat, block, bat)
        if tid is not None and rivals:
            # "a will and a power of attorney are each $495": several fees at this amount are named, there are
            # fewer such figures than fees, and the words say the figure is shared. Without those words the
            # nearest name wins, as before, because a fee is often named only in passing.
            if (len(re.findall(re.escape(shown) + r"(?!\d|,\d)", scope)) < len(rivals)
                    and re.search(r"\b(?:each|both|either|the same)\b", scope)
                    and not beside(all_things[tid]["terms"], sent, sat, len(shown))):
                tid = None
        if tid is None and (m.group(0) in not_fees or shown in not_fees):
            yield m, None, "other"
        elif tid is None and rivals:
            # one figure stands for more than one fee that carries this amount: it is right for each of them,
            # so check passes it, the record says so, and apply stops if those fees ever come to differ
            rivals = sorted(rivals)
            yield m, rivals[0], "shared:" + ",".join(rivals)
            tid = rivals[0]
        elif tid is None:
            yield m, None, "nothing at this amount is named nearby (at this amount: %s)" % ", ".join(cands)
        else:
            yield m, tid, "ok"
        last_fee = tid if tid and all_things[tid]["kind"] == "fee" else None
        last_block = block_bounds(path, text, m.start(), m.end())


# ---------------------------------------------------------------- every quoting sentence, on record

RENDITIONS = os.path.join(ROOT, "playbooks", "fees-renditions.json")


TOKEN_RX = re.compile(r"\{((?:gst:)?[a-z0-9?|-]+)\}")


def sentences(data, all_things, path, text):
    """Every sentence in a file that quotes a figure, where it stands, as
    {(block start, sentence start): [sentence, [(offset of the figure in it, match, id, note)], paragraph]}.
    The id and note are scan's own reading, which is used only for a sentence that is not on record."""
    found = {}
    for m, tid, note in scan(data, all_things, path, text):
        sent, at, block, block_at = context(path, text, m.start(), m.end())
        start = block_bounds(path, text, m.start(), m.end())[0]
        lead = len(sent) - len(sent.lstrip())
        found.setdefault((start, block_at - at), [sent.strip(), [], block])[1].append((at - lead, m, tid, note))
    return found


PARA = " <<in the paragraph>> "


def mask(block, since):
    """A paragraph with every amount and the day the charges took effect taken out, so that a change of price
    leaves it as it was and any change of words does not."""
    block = re.sub(r"as at \d{1,2} [a-z]+ \d{4}", "as at {day}", AMOUNT.sub("$#", block.strip()))
    return block.replace(since.lower(), "{charges-from}") if since else block


def named_alone(tid, sent, all_things):
    """True where the sentence names this fee or charge in words that are its own: one of its phrases is found
    where no other fee's or charge's phrase covers the same words or more. Consent orders alone names neither the
    property fee nor the parenting fee, and consent orders for an agreed property settlement names the first."""
    others = [(m.start(), m.end()) for other, th in all_things.items() if other != tid
              for term in th["terms"] for m in re.finditer(term, sent)]
    for term in all_things[tid]["terms"]:
        for m in re.finditer(term, sent):
            if not any(a <= m.start() and m.end() <= b for a, b in others):
                return True
    return False


def rests_on_paragraph(template, sent, all_things):
    """True where the fee a figure is tied to is not named in the sentence in words of its own, so the tie rests on
    the paragraph around it. Such a sentence is recorded with its paragraph, and is read again when that changes."""
    for m in TOKEN_RX.finditer(template.partition(PARA)[0]):
        token = m.group(1)
        if token in ("charges-from", "?", "gst:?"):
            continue
        ids = (token[4:] if token.startswith("gst:") else token).split("|")
        if not any(named_alone(one, sent, all_things) for one in ids if one in all_things):
            return True
    return False


def template_of(sent, marks, all_things, since, block=None):
    """A sentence with each figure replaced by what scan tied it to: {fee-id}, {a|b} where one figure stands for
    two fees, {gst:fee-id} for an amount before GST, {?} where nothing could be tied, and the figure itself
    where it is no fee or charge at all. The day the charges took effect becomes {charges-from}. Where a
    figure's fee is named only in the paragraph, the paragraph follows the sentence."""
    charge, words = False, sent
    for at, m, tid, note in sorted(marks, key=lambda k: k[0], reverse=True):
        if note == "ok":
            token = "{%s}" % tid
            charge = charge or all_things[tid]["kind"] != "fee"
        elif note.startswith("shared:"):
            token = "{%s}" % "|".join(note[7:].split(","))
        elif note == "before-gst":
            token = "{gst:%s}" % (tid or "?")
        elif note == "other":
            continue
        else:
            token = "{?}"
        sent = sent[:at] + token + sent[at + len(plain(m.group(0))):]
    if since and charge:
        sent = sent.replace(since.lower(), "{charges-from}")
    if block is not None and rests_on_paragraph(sent, words, all_things):
        sent += PARA + mask(block, since)
    return sent


def token_text(token, all_things, since):
    """What a recorded token reads as under a schedule, or None where it cannot be read: the fees one figure
    stands for have come to differ, or the fee is gone."""
    if token == "charges-from":
        return since.lower() if since else None
    gst = token.startswith("gst:")
    ids = (token[4:] if gst else token).split("|")
    if any(one not in all_things for one in ids):
        return None
    texts = {before_gst(all_things[one]["value"]) if gst else all_things[one]["amount"] for one in ids}
    return texts.pop() if len(texts) == 1 else None


def render(template, all_things, since):
    """(the sentence a recorded template reads as under a schedule, [(start, end, token)]), or (None, [])."""
    template = template.partition(PARA)[0]
    out, spans, last, pos = [], [], 0, 0
    for m in TOKEN_RX.finditer(template):
        word = token_text(m.group(1), all_things, since)
        if word is None:
            return None, []
        lit = template[last:m.start()]
        out.append(lit)
        pos += len(lit)
        spans.append((pos, pos + len(word), m.group(1)))
        out.append(word)
        pos += len(word)
        last = m.end()
    out.append(template[last:])
    return "".join(out), spans


def read_record():
    return json.load(open(RENDITIONS, encoding="utf-8"))["renditions"] if os.path.exists(RENDITIONS) else {}


def recorded_from():
    """The fees that were from prices when the record was made, or None where the record does not say."""
    if not os.path.exists(RENDITIONS):
        return None
    return json.load(open(RENDITIONS, encoding="utf-8")).get("from_prices")


def record_index(recorded, all_things, since):
    """The record as it reads under a schedule: {file: {sentence: [(template, spans, paragraph or None), ...]}},
    and the templates that cannot be read under it, as [(file, template)]."""
    index, unreadable = {}, []
    for name, templates in recorded.items():
        for t in templates:
            sent, spans = render(t, all_things, since)
            if sent is None:
                unreadable.append((name, t))
            else:
                index.setdefault(name, {}).setdefault(sent, []).append((t, spans, t.partition(PARA)[2] or None))
    return index, unreadable


def tie(spans, at):
    """What the record ties the figure at an offset to, as scan's (id, note)."""
    token = next((t for a, b, t in spans if a == at), None)
    if token is None:
        return None, "other"
    if token.startswith("gst:"):
        return (None if token == "gst:?" else token[4:]), "before-gst"
    if token == "?":
        return None, "the record ties this figure to nothing"
    if "|" in token:
        return token.split("|")[0], "shared:" + ",".join(token.split("|"))
    return token, "ok"


CLASH = ("", [], None)


def take(pool, sent, marks, block, all_things, since):
    """The recorded (template, spans, paragraph) for a sentence as it stands on a page, or None where it is not
    on record. A sentence whose tie rests on its paragraph is on record only with that paragraph, word for word.
    CLASH where the same words stand more than once with different fees behind them and the nearness rule reads
    none of the recorded ties, so no one can say which is which."""
    held = pool.get(sent)
    if not held:
        return None
    here = mask(block, since)
    fit = [e for e in held if e[2] == here or (e[2] is None and not rests_on_paragraph(e[0], sent, all_things))]
    if not fit:
        return None
    if len({e[0] for e in fit}) > 1:
        want = template_of(sent, marks, all_things, since, block)
        fit = [e for e in fit if e[0] == want]
        if not fit:
            return CLASH
    held.remove(fit[0])
    return fit[0]


def all_renditions(data, all_things=None, since=None, keep=None):
    """Every sentence that quotes a figure, as templates by file. A sentence already on record keeps the
    template the record gives it, so a tie once read and recorded is never worked out again."""
    all_things = all_things or things(data)
    since = since or (long_date(data["charges"]["valid_from"]) if data.get("charges") else None)
    out = {}
    for path in files():
        pool = {k: list(v) for k, v in (keep or {}).get(rel(path), {}).items()}
        got = []
        for sent, marks, block in sentences(data, all_things, path, open(path, encoding="utf-8").read()).values():
            entry = take(pool, sent, marks, block, all_things, since)
            got.append(entry[0] if entry and entry is not CLASH else template_of(sent, marks, all_things, since, block))
        if got:
            out[rel(path)] = sorted(got)
    return out


def show(template, all_things):
    """A recorded sentence with each figure put back beside the name of what it was tied to."""
    def one(m):
        ids = m.group(1)
        if ids == "?":
            return "[tied to nothing]"
        gst = ids.startswith("gst:")
        ids = ids[4:] if gst else ids
        parts = []
        for tid in ids.split("|"):
            th = all_things.get(tid)
            amount = (before_gst(th["value"]) if gst else th["amount"]) if th else "?"
            parts.append("%s = %s%s" % (amount, tid, " before GST" if gst else ""))
        return "[" + ", ".join(parts) + "]"
    head, _, para = template.partition(PARA)
    return re.sub(r"\{((?!charges-from\})(?:gst:)?[a-z0-9?|-]+)\}", one, head) + (
        " (its fee is named only in its paragraph, so it is recorded with it: %s)" % para if para else "")


def snapshot():
    data = load()
    problems = check(data, quiet=True, strict=False)
    if problems:
        print("Not recorded. Fix these first:")
        for p_ in problems:
            print("  " + p_)
        return 1
    all_things = things(data)
    since = long_date(data["charges"]["valid_from"]) if data.get("charges") else None
    index, unreadable = record_index(read_record(), all_things, since)
    now = all_renditions(data, all_things, since, keep=index)
    json.dump({"about": "Every sentence on the site that quotes a fee or charge, with each figure replaced by the "
                        "fee or charge it belongs to. Written by scripts/fees.py snapshot and never by hand. "
                        "scripts/fees.py check fails when a sentence here is new, has changed or has gone.",
               "from_prices": sorted(f["id"] for f in data["fees"] if f["from"]),
               "renditions": now}, open(RENDITIONS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(RENDITIONS, "a", encoding="utf-8").write("\n")
    print("recorded %d sentences across %d files" % (sum(len(v) for v in now.values()), len(now)))
    return 0


# ---------------------------------------------------------------- built pages

def stale_builds():
    """A service page is whatever its content file builds. One edited by hand, or left behind by a change to
    its content file, to its hub or to the builder, is an error."""
    out = []
    builder = os.path.join(ROOT, "scripts", "build-service-page.py")
    cfs = sorted(glob.glob(os.path.join(ROOT, "playbooks", "service-content", "service-*.json")))
    with tempfile.TemporaryDirectory() as tmp:
        run = subprocess.run([sys.executable, builder, "--out", tmp] + cfs, capture_output=True, text=True)
        if run.returncode != 0:
            return ["the service pages could not be built: %s" % (run.stderr.strip().splitlines() or ["no message"])[-1]]
        for cf in cfs:
            name = os.path.basename(cf)[:-5] + ".html"
            page = os.path.join(ROOT, name)
            built = open(os.path.join(tmp, name), encoding="utf-8").read()
            if not os.path.exists(page) or open(page, encoding="utf-8").read() != built:
                out.append("%s is not what its content file builds: run python3 scripts/build-service-page.py %s, "
                           "and never edit the page by hand" % (name, rel(cf)))
    for path in files():
        if "{as_at}" in open(path, encoding="utf-8").read():
            out.append("%s still carries the placeholder {as_at}" % rel(path))
    return out


# ---------------------------------------------------------------- figures the check cannot read

DISGUISED = re.compile(r"(?:&#0*36;|&#x0*24;|&dollar;)\s?\d|\$\s+\d|\b\d{1,3}(?:,\d{3})+ dollars\b|\b\d{3,} dollars\b"
                       r"|\$\s*(?:<[^>]+>\s*)+\d|\$\s*&#x?[0-9a-f]+;|\bAUD\s?\$?\s?\d|\bA\$\s?\d", re.I)


def unreadable_figures():
    """Amounts written in a way the check cannot read, or in a file it does not read."""
    out = []
    for path in files():
        text = open(path, encoding="utf-8").read()
        for m in DISGUISED.finditer(text):
            out.append("%s:%d %r: write an amount as $1,234 so that it can be checked"
                       % (rel(path), text.count("\n", 0, m.start()) + 1, m.group(0)))
    extra = ([os.path.join(ROOT, "scripts", "site.js")] + sorted(glob.glob(os.path.join(ROOT, "assets", "*.vcf")))
             + sorted(glob.glob(os.path.join(ROOT, "assets", "video", "*.vtt"))))
    for path in extra:
        if os.path.exists(path):
            text = open(path, encoding="utf-8", errors="replace").read()
            for m in list(AMOUNT.finditer(text)) + list(DISGUISED.finditer(text)):
                out.append("%s:%d %s: a price must not be written by a script, a contact card or a caption file, where no check reads it"
                           % (rel(path), text.count("\n", 0, m.start()) + 1, m.group(0)))
    return out


# ---------------------------------------------------------------- what a page says

_VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class _Says(HTMLParser):
    """A page's own words: its title, its description and the text of <main> outside the rail, with the
    dates held in <time> elements left out. Header, menus, footer, rail cards, scripts and version keys are
    the same on every page, so a change to them is not a change to what the page says."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth, self.skip_at, self.in_main, self.in_title, self.parts = 0, None, False, False, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "meta" and a.get("name") == "description":
            self.parts.append(a.get("content") or "")
        if tag in _VOID:
            return
        self.depth += 1
        if tag == "title":
            self.in_title = True
        if tag == "main":
            self.in_main = True
        cls = (a.get("class") or "").split()
        if self.skip_at is None and (tag in ("script", "style", "time", "svg", "aside") or "rail-card" in cls):
            self.skip_at = self.depth

    def handle_endtag(self, tag):
        if tag in _VOID:
            return
        if self.skip_at is not None and self.depth == self.skip_at:
            self.skip_at = None
        if tag == "title":
            self.in_title = False
        if tag == "main":
            self.in_main = False
        self.depth -= 1

    def handle_data(self, data):
        if self.in_title or (self.in_main and self.skip_at is None):
            self.parts.append(data)


def says(text):
    p_ = _Says()
    p_.feed(text)
    out = re.sub(r"\s+", " ", " ".join(p_.parts)).strip()
    return re.sub(r"Last reviewed \d{1,2} [A-Z][a-z]+ \d{4}", "Last reviewed", out)


def changed_since(ref):
    """The pages whose own words differ from the same page at a git ref, and pages that are new."""
    names = subprocess.run(["git", "-C", ROOT, "diff", "--name-only", ref], capture_output=True, text=True,
                           check=True).stdout.split()
    out = []
    for name in names:
        if not name.endswith(".html") or os.path.basename(name).startswith("_") or not os.path.exists(os.path.join(ROOT, name)):
            continue
        old = subprocess.run(["git", "-C", ROOT, "show", "%s:%s" % (ref, name)], capture_output=True, text=True)
        new = open(os.path.join(ROOT, name), encoding="utf-8").read()
        if old.returncode != 0 or says(old.stdout) != says(new):
            out.append(name)
    return out


OFFER_RX = re.compile(r'("name":\s*"([^"]+)",\s*"price":\s*")(\d+)(")')
OFFER_SPEC_RX = re.compile(r'("name":\s*"([^"]+)",\s*"price":\s*"\d+",[^{}]*?"priceSpecification":\s*\{[^{}]*?"(?:price|minPrice)":\s*")(\d+)(")')


def offer_fee(data, name):
    for f in data["fees"]:
        if f["name"].lower() == name.lower() or name.lower() in [a.lower() for a in f.get("offer_names", [])]:
            return f
    return None


# ---------------------------------------------------------------- check

def bad_totals(data):
    """Each fee's total is a whole number of dollars from the minimum to the ceiling."""
    out = []
    low, high = data.get("minimum", 0), data.get("maximum")
    for f in data["fees"]:
        t = f["total"]
        if isinstance(t, bool) or not isinstance(t, int):
            out.append("%s has a total of %r. A total is a whole number of dollars including GST, written as a number "
                       "such as 1980" % (f["id"], t))
        elif t < low:
            out.append("%s is %s, under the %s minimum" % (f["id"], money(t), money(low)))
        elif high is not None and t > high:
            out.append("%s is %s, over the %s ceiling for a listed fee" % (f["id"], money(t), money(high)))
    return out


def typed_prices(data):
    """A dollar figure typed into a scope, a note or a label in the source, other than a threshold listed there."""
    out = []
    for where, value in source_wording(data):
        for m in AMOUNT.finditer(value):
            if m.group(0) not in data.get("other_amounts", []) and strip00(m.group(0)) not in data.get("other_amounts", []):
                out.append("playbooks/fees.json: the %s %r holds %s. A price is never typed into a scope, a note or a "
                           "label there, because it would reach the fees page unread. Say it in a sentence on the page, "
                           "where the check ties it to its fee and records it" % (where, value[:60], m.group(0)))
    return out


def source_wording(data):
    """(where, words) for every piece of wording in the source that reaches a page as it is written."""
    def walk(node, where):
        if isinstance(node, dict):
            for k, v in node.items():
                if k in ("about", "terms", "minimum_terms", "other_amounts", "url", "id", "parts", "read",
                         "valid_from", "valid_to", "hero"):
                    continue
                yield from walk(v, "%s of %s" % (k, node.get("id") or node.get("name") or where))
        elif isinstance(node, list):
            for v in node:
                yield from walk(v, where)
        elif isinstance(node, str):
            yield where, node
    return walk(data, "source")


def check(data=None, quiet=False, with_renditions=True, strict=True):
    """Every problem found, as a list. with_renditions reads the record for each sentence's ties. strict also
    reports a sentence that is new, has changed or has gone, which snapshot leaves out because recording them
    is its job."""
    data = data or load()
    all_things = things(data)
    by_id = {f["id"]: f for f in data["fees"]}
    problems, notices, count = [], [], 0
    # 1. fees.html is exactly what the source generates
    ft = fees_page()
    try:
        if render_fees_page(data, ft) != ft:
            shown = published_schedule()
            diff = [f["id"] for f in data["fees"] if shown.get(f["id"]) != (f["total"], f["from"])]
            problems.append("fees.html differs from what playbooks/fees.json generates%s: run scripts/fees.py apply"
                            % ((" (" + ", ".join(diff[:4]) + ")") if diff else ""))
    except SystemExit as e:
        problems.append(str(e))
    # 1b. the prices carry their date: the fees page says the day they were confirmed, its WebPage node and
    #     the sitemap agree, and every service page that quotes a price dates it in the same sentence
    asat = LEAD_ASAT_RX.search(ft)
    every = ASAT_RX.findall(ft)
    node = re.search(r'"@type": "WebPage".*?"dateModified": "(\d{4}-\d{2}-\d{2})"', ft)
    smap = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
    lmod = re.search(r"<loc>%sfees\.html</loc>\s*<lastmod>(\d{4}-\d{2}-\d{2})</lastmod>" % re.escape(SITE), smap)
    if not (asat and node and lmod):
        problems.append("fees.html must say whose fees these are and the day they were confirmed in the words that "
                        "open its lead, with the same day in a WebPage node, and the sitemap must list the page")
    elif (not (asat.group(1) == node.group(1) == lmod.group(1)) or any(e[1] != asat.group(1) or e[3] != long_date(e[1]) for e in every)):
        problems.append("fees.html dates disagree: the lead says %s, the WebPage node %s, the sitemap %s and the "
                        "page's other as at dates %s: run scripts/fees.py stamp with the day the prices were confirmed"
                        % (asat.group(1), node.group(1), lmod.group(1), sorted({e[1] for e in every})))
    if smap.count("<url>") != smap.count("<lastmod>"):
        problems.append("sitemap.xml has %d pages and %d lastmod dates: each page takes exactly one"
                        % (smap.count("<url>"), smap.count("<lastmod>")))
    problems += stale_builds()
    for path in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
        base = os.path.basename(path)
        if base == "fees.html" or base.startswith("service-") or base.startswith("_"):
            continue                                   # checked above, and by the build
        page = open(path, encoding="utf-8").read()
        tagged = [(m.group(2), m.group(4)) for m in ASAT_RX.finditer(page)]
        plain_days = [m.group(2) for m in DATED_PLAIN_RX.finditer(page)]
        if not tagged and not plain_days:
            continue
        days = {long_date(iso) for iso, _ in tagged} | set(plain_days)
        lm = re.search(r"<loc>%s%s</loc>\s*<lastmod>(\d{4}-\d{2}-\d{2})</lastmod>" % (re.escape(SITE), re.escape(base)), smap)
        if any(shown != long_date(iso) for iso, shown in tagged) or len(days) != 1:
            problems.append("%s: its fee sentences give different days (%s): run scripts/fees.py stamp with the day "
                            "and the page" % (base, ", ".join(sorted(days))))
        elif lm:
            d_, mo_, y_ = days.pop().split(" ")
            iso = "%s-%02d-%02d" % (y_, MONTHS.index(mo_) + 1, int(d_))
            if iso > lm.group(1):
                problems.append("%s: its fee sentences are dated %s, after the page's own date in the sitemap, %s"
                                % (base, iso, lm.group(1)))
    # 2. the minimum and the ceiling, whole dollars, and terms to identify each fee by
    problems += bad_totals(data)
    for f in data["fees"]:
        if not f.get("terms"):
            problems.append("%s has no terms to identify it by" % f["id"])
    # 2a. no price is typed into the source's own wording, where no sentence would be read and recorded
    problems += typed_prices(data)
    # 2b. a fee that has changed between a fixed price and a from price since the record was made
    was_from = recorded_from()
    if with_renditions and was_from is not None:
        for f in data["fees"]:
            if f["from"] != (f["id"] in was_from):
                held = sorted({name for name, ts in read_record().items() for t in ts
                               if re.search(r"\{(?:gst:)?(?:[a-z0-9-]+\|)*%s(?:\|[a-z0-9-]+)*\}" % re.escape(f["id"]), t)})
                problems.append("%s is now %s, and the record was made when it was %s. Reword each sentence that quotes "
                                "it, in %s, and run scripts/fees.py snapshot"
                                % (f["id"], "a from price" if f["from"] else "a fixed price",
                                   "a fixed price" if f["from"] else "a from price", ", ".join(held) or "no file"))
    # 3. the court and government charges are still inside the period they were read for
    ch = data.get("charges")
    if ch:
        today = melbourne_today()
        last = datetime.strptime(ch["valid_to"], "%Y-%m-%d").date()
        how = ("read each source named in charges, update the amounts, valid_from, valid_to and read in "
               "playbooks/fees.json, with the label and address of any source named by its year, and run "
               "scripts/fees.py apply on or after the day the new amounts take effect")
        if today > last + timedelta(days=14):
            problems.append("the court and ASIC charges were read for the period to %s, which passed more than a "
                            "fortnight ago: %s" % (long_date(ch["valid_to"]), how))
        elif today > last:
            notices.append("the court and ASIC charges were read for the period to %s, which has passed. The gate "
                           "fails from %s. Whichever routine runs first must %s"
                           % (long_date(ch["valid_to"]), long_date((last + timedelta(days=15)).isoformat()), how))
        elif (last - today).days <= 21:
            notices.append("the court and ASIC charges are current only to %s. Read each body's schedule for the "
                           "period that follows now, and once it begins %s. apply refuses amounts whose first day "
                           "has not yet come" % (long_date(ch["valid_to"]), how))
        for src in ch.get("sources", []):
            for year in re.findall(r"\b(20\d\d)\b", src.get("label", "")):
                if year != ch["valid_from"][:4]:
                    problems.append("the source %r names %s, and the charges took effect in %s: give the source its "
                                    "label and address for that year" % (src["label"], year, ch["valid_from"][:4]))
    # 4. every quoted figure is tied to a fee or charge that carries it. A sentence on record keeps the tie the
    #    record gives it, so two fees that come to share an amount are never confused. A sentence that is not
    #    on record is tied by the nearness rule, and reported below until it has been read and recorded.
    since_now = long_date(ch["valid_from"]) if ch else None
    recorded = read_record() if with_renditions else {}
    index, unreadable = record_index(recorded, all_things, since_now)
    fresh, gone = [], []
    for name, t in unreadable:
        problems.append("%s: on record, and one figure in it now stands for fees or charges that differ, so the "
                        "sentence needs rewording: %s" % (name, t))
    for path in files():
        text = open(path, encoding="utf-8").read()
        pool = {k: list(v) for k, v in index.get(rel(path), {}).items()}
        for sent, marks, block in sentences(data, all_things, path, text).values():
            entry = take(pool, sent, marks, block, all_things, since_now)
            if entry is CLASH:
                problems.append("%s: these words stand more than once in the file with different fees behind them, "
                                "and nothing near them says which is which, so reword one to name its fee: %s"
                                % (rel(path), sent))
                entry = None
            spans = entry[1] if entry else None
            if spans is None and with_renditions:
                fresh.append((rel(path), template_of(sent, marks, all_things, since_now, block)))
            states_minimum = any(re.search(t, sent) for t in data.get("minimum_terms", []))
            for at, m, tid, note in marks:
                if spans is not None:
                    tid, note = tie(spans, at)
                count += 1
                line = text.count("\n", 0, m.start()) + 1
                if (note == "other" and states_minimum and data.get("minimum")
                        and strip00(m.group(0)) != money(data["minimum"])
                        and m.group(0) not in data.get("other_amounts", [])):
                    problems.append("%s:%d the sentence states a minimum of %s, and the minimum in playbooks/fees.json "
                                    "is %s" % (rel(path), line, m.group(0), money(data["minimum"])))
                if note == "before-gst":
                    if tid is None or m.group(0) != before_gst(by_id[tid]["total"]):
                        problems.append("%s:%d %s plus GST does not match the fee before it" % (rel(path), line, m.group(0)))
                elif note.startswith("shared:") or note == "other":
                    pass
                elif note != "ok":
                    problems.append("%s:%d %s: %s" % (rel(path), line, m.group(0), note))
                elif all_things[tid]["kind"] == "fee" and all_things[tid]["from"]:
                    # a "from" price must not be quoted as a flat fixed fee
                    if "from" not in sent and "start" not in sent:
                        problems.append("%s:%d %s is a from price for %s but the sentence does not say from"
                                        % (rel(path), line, m.group(0), tid))
        gone += [(rel(path), e[0]) for lst in pool.values() for e in lst]
        # 5. Offer prices in service pages and their content files
        if os.path.basename(path) != "fees.html":
            for rx in (OFFER_RX, OFFER_SPEC_RX):
                for m in rx.finditer(text):
                    count += 1
                    f = offer_fee(data, m.group(2))
                    line = text.count("\n", 0, m.start()) + 1
                    if f is None:
                        problems.append("%s:%d Offer %r is not a fee in the source" % (rel(path), line, m.group(2)))
                    elif int(m.group(3)) != f["total"]:
                        problems.append("%s:%d Offer %r shows %s, the source says %s"
                                        % (rel(path), line, m.group(2), m.group(3), f["total"]))
    # 5a. every price in a page's markup is one of the firm's fees, wherever it sits in its Offer
    totals = {str(f["total"]) for f in data["fees"]}
    for path in files():
        if not path.endswith(".html"):
            continue
        text = open(path, encoding="utf-8").read()
        for m in re.finditer(r'"(price|minPrice|maxPrice|lowPrice|highPrice)":\s*"?(\d+(?:\.\d+)?)"?', text):
            if m.group(2) not in totals:
                problems.append("%s:%d the markup gives a %s of %s, which is no fee in the source"
                                % (rel(path), text.count("\n", 0, m.start()) + 1, m.group(1), m.group(2)))
    # 5b. a sentence that quotes a court or ASIC charge and dates it gives the day the charges took effect
    if ch:
        since = long_date(ch["valid_from"]).lower()
        for path in files():
            text = open(path, encoding="utf-8").read()
            seen = set()
            for m, tid, note in scan(data, all_things, path, text):
                if note != "ok" or all_things[tid]["kind"] == "fee":
                    continue
                a, b = block_bounds(path, text, m.start(), m.end())
                if a in seen:
                    continue
                seen.add(a)
                for d_ in re.findall(r"(?:since|from) (\d{1,2} [a-z]+ \d{4})", plain(text[a:b]).lower()):
                    if d_ != since:
                        problems.append("%s:%d a court or ASIC charge is dated %s, and the charges in the source took "
                                        "effect on %s" % (rel(path), text.count("\n", 0, m.start()) + 1, d_, since))
    # 6. no amount is written where, or in a way, the check cannot read it
    problems += unreadable_figures()
    # 7. every sentence that quotes a figure is the sentence on record
    if with_renditions and strict and not problems:
        for name, t in sorted(fresh):
            problems.append("%s: new or changed since the record was made: %s" % (name, show(t, all_things)))
        for name, t in sorted(gone):
            problems.append("%s: on record and no longer on the page: %s" % (name, show(t, all_things)))
        if fresh or gone:
            problems.append("Read each sentence above against playbooks/fees.json, each figure beside the fee it was "
                            "tied to, and when every one is right run: python3 scripts/fees.py snapshot")
    NOTICES[:] = notices
    if not quiet:
        print("fees: %d renditions read across %d files, %d problems" % (count, len(files()), len(problems)))
        for p in problems + ["note: " + n for n in notices]:
            print("  " + p)
    return problems


# ---------------------------------------------------------------- dates

def stamp(path, text, date):
    """Move a changed page's own dates to the day of the change."""
    y, mo, d = (int(x) for x in date.split("-"))
    short = "%d %s %d" % (d, MONTHS[mo - 1][:3], y)
    base = os.path.basename(path)
    if path.endswith(".json"):
        return re.sub(r'("date":\s*")\d{4}-\d{2}-\d{2}(")', r"\g<1>%s\2" % date, text, count=1)
    if not path.endswith(".html"):
        return text
    text = re.sub(r'(<meta property="article:modified_time" content=")[^"]*(")', r"\g<1>%s\2" % date, text)
    text = re.sub(r'("dateModified":\s*")\d{4}-\d{2}-\d{2}(")', r"\g<1>%s\2" % date, text)
    text = re.sub(r'([Uu]pdated <time datetime=")\d{4}-\d{2}-\d{2}(">)[^<]*(</time>)', r"\g<1>%s\g<2>%s\3" % (date, short), text)
    if base == "faq.html":
        text = re.sub(r"(<span>Last reviewed )[^<]*(</span>)", r"\g<1>%s\2" % long_date(date), text)
    text = CURRENCY_RX.sub(lambda m: m.group(1) + month_of(date), text)
    # a hub's closing line, written in the page itself: "updated on" and the long form of the day
    text = re.sub(r'(updated on <time datetime=")\d{4}-\d{2}-\d{2}(">)[^<]*(</time>)',
                  lambda m: m.group(1) + date + m.group(2) + long_date(date) + m.group(3), text)
    # the day a passage that quotes the firm's fees gives, in the page's words and in its markup
    text = ASAT_RX.sub(lambda m: m.group(1) + date + m.group(3) + long_date(date) + m.group(5), text)
    text = DATED_PLAIN_RX.sub(lambda m: m.group(1) + long_date(date) + m.group(3), text)
    return text


def set_lastmod(sitemap, page, date):
    loc = "<loc>%s%s</loc>" % (SITE, "" if page == "index.html" else page)
    i = sitemap.find(loc)
    if i < 0:
        return sitemap
    j = sitemap.find("<lastmod>", i)
    k = sitemap.find("</lastmod>", j)
    return sitemap[:j + 9] + date + sitemap[k:]


def rebuild_service_pages():
    built = []
    for cf in sorted(glob.glob(os.path.join(ROOT, "playbooks", "service-content", "service-*.json"))):
        page = os.path.join(ROOT, os.path.basename(cf)[:-5] + ".html")
        before = open(page, encoding="utf-8").read() if os.path.exists(page) else ""
        subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build-service-page.py"), cf],
                       check=True, stdout=subprocess.DEVNULL)
        if open(page, encoding="utf-8").read() != before:
            built.append(page)
    return built


def move_listing_dates(pages, date):
    """Sitemap lastmod for each changed page, and the llms.txt date."""
    sp = os.path.join(ROOT, "sitemap.xml")
    sm = open(sp, encoding="utf-8").read()
    for p in pages:
        sm = set_lastmod(sm, p, date)
    open(sp, "w", encoding="utf-8").write(sm)
    if not pages:
        return
    lp = os.path.join(ROOT, "llms.txt")
    lt = open(lp, encoding="utf-8").read()
    lt2 = re.sub(r"(?m)^Last updated: .*$", "Last updated: %s." % long_date(date), lt)
    if lt2 != lt:
        open(lp, "w", encoding="utf-8").write(lt2)


CURRENCY_RX = re.compile(r"(reflects the law applying in Victoria as at )([A-Z][a-z]+ \d{4})")


def month_of(iso):
    return "%s %s" % (MONTHS[int(iso[5:7]) - 1], iso[:4])


def law_months(paths, date):
    """Pages whose currency line names a month other than the month of the new date."""
    out = []
    for path in paths:
        page = path
        if path.endswith(".json"):
            page = os.path.join(ROOT, os.path.basename(path)[:-5] + ".html")
        if os.path.exists(page):
            m = CURRENCY_RX.search(open(page, encoding="utf-8").read())
            if m and m.group(2) != month_of(date):
                out.append("%s, %s" % (os.path.basename(page), m.group(2)))
    return out


def refuse_new_month(paths, date, law_read):
    """A page's currency line says when its law was read, and the gate ties it to the page's date. Moving a date
    into another month therefore moves that statement, which is true only if the law was read again."""
    behind = law_months(paths, date)
    if behind and not law_read:
        raise SystemExit("STOPPED, nothing written. %d pages say their law was read in an earlier month:\n  %s\n"
                         "Dating them %s would move that line to %s, which is true only once the law on those "
                         "pages has been read again. Read it, then add --law-read to the command."
                         % (len(behind), "\n  ".join(behind[:12]) + ("\n  and %d more" % (len(behind) - 12) if len(behind) > 12 else ""),
                            date, month_of(date)))


def stamp_files(date, names, law_read=False):
    """Move the dates of the named pages, and of the service pages built from named content files."""
    real_date(date)
    targets = []
    for name in names:
        base = os.path.basename(name)
        path = os.path.join(ROOT, name)
        if base.startswith("service-") and base.endswith(".html"):
            path = os.path.join(ROOT, "playbooks", "service-content", base[:-5] + ".json")
        if os.path.exists(path) and not base.startswith("_"):
            targets.append(path)
    later = []
    for path in targets:
        t_ = open(path, encoding="utf-8").read()
        days = re.findall(r'"date":\s*"(\d{4}-\d{2}-\d{2})"', t_)[:1] if path.endswith(".json") else re.findall(r'"dateModified":\s*"(\d{4}-\d{2}-\d{2})"', t_)
        if days and max(days) > date:
            later.append("%s, %s" % (os.path.basename(path), max(days)))
    if later:
        raise SystemExit("STOPPED, nothing written. A page's date never moves backwards, and these are already dated "
                         "later than %s:\n  %s" % (date, "\n  ".join(later[:12])))
    refuse_new_month(targets, date, law_read)
    pages = []
    for name in names:
        base = os.path.basename(name)
        path = os.path.join(ROOT, name)
        if base.startswith("_"):
            continue
        if base.startswith("service-") and base.endswith(".html"):
            path = os.path.join(ROOT, "playbooks", "service-content", base[:-5] + ".json")
        if not os.path.exists(path):
            continue
        if not (path.endswith(".html") or (path.endswith(".json") and "service-content" in path and base.startswith("service-")
                                           and not base.endswith("-claims.md"))):
            continue
        text = open(path, encoding="utf-8").read()
        new = stamp(path, text, date)
        if new != text:
            open(path, "w", encoding="utf-8").write(new)
        pages.append(os.path.basename(path)[:-5] + ".html" if path.endswith(".json") else base)
    rebuild_service_pages()
    pages = sorted(set(pages))
    move_listing_dates(pages, date)
    print("dates moved to %s on %d pages" % (date, len(pages)))
    return 0


# ---------------------------------------------------------------- apply

def holds_charge(spans, all_things):
    """True where a sentence quotes a court or ASIC charge, or a total worked from one, or gives the day they took
    effect. The check holds every date in such a sentence's paragraph to that day, so apply moves it there."""
    for _, _, t in spans:
        if t == "charges-from":
            return True
        for one in (t[4:] if t.startswith("gst:") else t).split("|"):
            if one in all_things and all_things[one]["kind"] != "fee":
                return True
    return False


def apply(date=None, law_read=False):
    """0 where every rendition now agrees with the source, 1 where pages were written and the check that follows
    reports something, 2 where it stopped before writing anything."""
    data = load()
    if date:
        real_date(date)
    day = date or melbourne_today().isoformat()
    bad = bad_totals(data) + typed_prices(data)
    if bad:
        print("STOPPED, nothing written.")
        for b_ in bad:
            print("  " + b_)
        return 2
    ch = data.get("charges")
    if ch and ch["valid_from"] > day:
        print("STOPPED, nothing written. The charges in playbooks/fees.json take effect on %s, and a charge is "
              "published from the day it applies. Run this on or after that day." % long_date(ch["valid_from"]))
        return 2
    new = things(data)
    old = things(data, published_schedule(), published_charges())
    changed = {tid for tid in new if old[tid]["amount"] != new[tid]["amount"] or old[tid]["from"] != new[tid]["from"]}
    old_since = published_since()
    new_since = long_date(ch["valid_from"]) if ch else None
    moving = bool(changed) or old_since != new_since
    # Each figure is tied through the record, read as the schedule stood before the edit, and never worked out
    # again from the amounts, so two fees that share an amount before or after the change are not confused.
    index, unreadable = record_index(read_record(), old, old_since)
    flips = [tid for tid in changed if old[tid]["from"] != new[tid]["from"]]
    if flips:
        print("These fees change between a fixed price and a from price, so the sentences that quote them "
              "need rewording by hand after this run: %s" % ", ".join(flips))
    pending, stops, strangers, missing = {}, [], [], []
    for path in files():
        base = os.path.basename(path)
        built = base.startswith("service-") and base.endswith(".html")     # rebuilt from its content file below
        text = open(path, encoding="utf-8").read()
        pool = {k: list(v) for k, v in index.get(rel(path), {}).items()}
        edits = []
        for sent, marks, block in sentences(data, old, path, text).values():
            entry = take(pool, sent, marks, block, old, old_since)
            if not entry or entry is CLASH:
                strangers.append("%s: %s" % (rel(path), sent))
                continue
            template, spans, _ = entry
            if built:
                continue
            if holds_charge(spans, old) and old_since and new_since and old_since != new_since:
                a_, b_ = block_bounds(path, text, marks[0][1].start(), marks[0][1].end())
                edits += [(a_ + d.start(), a_ + d.end(), new_since) for d in re.finditer(re.escape(old_since), text[a_:b_])]
            for at, m, _, _ in marks:
                token = next((t for a, b, t in spans if a == at), None)
                if token is None:
                    continue                           # no fee or charge: a threshold, or an amount in an example
                word = token_text(token, new, new_since)
                if word is None:
                    ids = (token[4:] if token.startswith("gst:") else token).split("|")
                    stops.append("%s:%d %s: one figure stands for %s, which now differ"
                                 % (rel(path), text.count("\n", 0, m.start()) + 1, m.group(0), " and ".join(ids)))
                elif word != m.group(0):
                    edits.append((m.start(), m.end(), word))
        missing += ["%s: %s" % (rel(path), show(e[0], old)) for lst in pool.values() for e in lst]
        new_text = text
        for a_, b_, word in sorted(set(edits), reverse=True):
            new_text = new_text[:a_] + word + new_text[b_:]

        def offer_sub(m):
            f = offer_fee(data, m.group(2))
            return m.group(1) + (str(f["total"]) if f else m.group(3)) + m.group(4)
        if built:
            continue
        if base != "fees.html":
            new_text = OFFER_SPEC_RX.sub(offer_sub, OFFER_RX.sub(offer_sub, new_text))
        else:
            new_text = render_fees_page(data, new_text)
        if new_text != text:
            pending[path] = new_text
    # The pages must be the pages on record before any figure is rewritten. Where no amount and no date of the
    # charges changes, no figure is rewritten and there is nothing to guard.
    adrift = (["on a page and not on record: " + x for x in strangers] + ["on record and not on its page: " + x for x in missing]
              + ["on record and unreadable at the amounts the site shows: %s: %s" % x for x in unreadable])
    if moving and adrift:
        print("STOPPED, nothing written. The pages do not match the record of sentences that quote a fee, so apply "
              "cannot be sure which fee each figure belongs to. Put playbooks/fees.json back as it was, run "
              "scripts/fees.py check and put right what it reports, run scripts/fees.py snapshot, then make the "
              "change and apply again. What does not match:")
        for x in adrift[:20]:
            print("  " + x)
        if len(adrift) > 20:
            print("  and %d more" % (len(adrift) - 20))
        return 2
    if stops:
        print("STOPPED, nothing written. Each sentence below gives one figure for two or more fees, which was right "
              "while they were the same amount. Put playbooks/fees.json back as it was, reword each sentence so "
              "every fee has its own figure, run scripts/fees.py check and then snapshot, and make the change again:")
        for s_ in stops:
            print("  " + s_)
        return 2
    # A dry run of the check's own reading, on the pages as they would be written and at the new amounts: every
    # sentence must still be the record's, and no file may hold the same words with different fees behind them.
    after, _ = record_index(read_record(), new, new_since)
    for path, new_text in pending.items():
        pool = {k: list(v) for k, v in after.get(rel(path), {}).items()}
        for sent, marks, block in sentences(data, new, path, new_text).values():
            entry = take(pool, sent, marks, block, new, new_since)
            if entry is CLASH:
                stops.append("%s: at the new amounts these words would stand more than once in the file with different "
                             "fees behind them, so reword one to name its fee: %s" % (rel(path), sent))
            elif entry is None:
                stops.append("%s: at the new amounts this sentence would no longer be the one on record: %s" % (rel(path), sent))
    if stops:
        print("STOPPED, nothing written. Put playbooks/fees.json back as it was, put right what is listed, run "
              "scripts/fees.py check and then snapshot, and make the change again:")
        for s_ in stops:
            print("  " + s_)
        return 2
    if pending and not date:
        date = day
        print("No date was given, so the pages that change are dated today in Melbourne, %s." % date)
    if pending:
        refuse_new_month(list(pending), date, law_read)
    for path, new_text in pending.items():
        open(path, "w", encoding="utf-8").write(stamp(path, new_text, date))
    built = rebuild_service_pages()
    pages = sorted(set([rel(p_) for p_ in pending if p_.endswith(".html")] + [rel(p_) for p_ in built]))
    if date and pages:
        move_listing_dates(pages, date)
    print("fees applied: %d amounts changed (%s); %d files rewritten, %d service pages rebuilt"
          % (len(changed), ", ".join(sorted(changed)) or "none", len(pending), len(built)))
    for p_ in pages:
        print("  " + p_)
    problems = check(data)
    return 1 if problems else 0


def where(only=None):
    data = load()
    all_things = things(data)
    since = long_date(data["charges"]["valid_from"]) if data.get("charges") else None
    index, _ = record_index(read_record(), all_things, since)
    found = {}
    for path in files():
        text = open(path, encoding="utf-8").read()
        pool = {k: list(v) for k, v in index.get(rel(path), {}).items()}
        for sent, marks, block in sentences(data, all_things, path, text).values():
            entry = take(pool, sent, marks, block, all_things, since)
            spans = entry[1] if entry and entry is not CLASH else None
            for at, m, tid, note in marks:
                if spans is not None:
                    tid, note = tie(spans, at)
                ids = note[7:].split(",") if note.startswith("shared:") else ([tid] if tid and note == "ok" else [])
                for one in ids:
                    found.setdefault(one, {}).setdefault(rel(path), 0)
                    found[one][rel(path)] += 1
    for tid, th in all_things.items():
        if only and tid != only:
            continue
        places = found.get(tid, {})
        print("%-52s %s%-11s quoted %3d times in %2d files" % (tid, "from " if th["from"] else "     ", th["amount"],
                                                               sum(places.values()), len(places)))
        if only:
            for p, n in sorted(places.items()):
                print("    %-58s %d" % (p, n))


def table():
    data = load()
    for f in data["fees"]:
        print("%-52s %s%-8s %s plus GST" % (f["name"], "from " if f["from"] else "     ", money(f["total"]),
                                             before_gst(f["total"])))
    ch = data.get("charges")
    if ch:
        print("\nCourt and government charges, %s to %s, read %s" % (ch["valid_from"], ch["valid_to"], ch["read"]))
        for it in ch["items"]:
            print("%-72s %s" % (it["label"], amount_text(it["amount"])))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "check":
        sys.exit(1 if check() else 0)
    elif cmd == "apply":
        args = [a for a in sys.argv[2:] if a != "--law-read"]
        sys.exit(apply(args[0] if args else None, law_read="--law-read" in sys.argv))
    elif cmd == "stamp" and len(sys.argv) > 3:
        names = [a for a in sys.argv[3:] if a != "--law-read"]
        if names and names[0] == "--since":
            names = changed_since(names[1])
        sys.exit(stamp_files(sys.argv[2], names, law_read="--law-read" in sys.argv))
    elif cmd == "snapshot":
        sys.exit(snapshot())
    elif cmd == "use" and len(sys.argv) > 2:
        # put a list of totals into the fee source and apply it: {"totals": {fee id: total including GST}}
        try:
            wanted = json.load(open(sys.argv[2], encoding="utf-8"))["totals"]
        except (OSError, ValueError, KeyError, TypeError):
            raise SystemExit('STOPPED, nothing written. %s is not a list of totals: {"totals": {"fee id": 1980}}' % sys.argv[2])
        wrong = sorted(k for k, v in wanted.items() if isinstance(v, bool) or not isinstance(v, int))
        if not isinstance(wanted, dict) or wrong:
            raise SystemExit("STOPPED, nothing written. A total is a whole number of dollars including GST, written as "
                             "a number such as 1980. Not so: %s" % ", ".join(wrong))
        source = load()
        known = {f["id"] for f in source["fees"]}
        strangers = sorted(set(wanted) - known)
        if strangers:
            raise SystemExit("These are not fees in playbooks/fees.json: %s" % ", ".join(strangers))
        for f in source["fees"]:
            if f["id"] in wanted:
                f["total"] = wanted[f["id"]]
        args = [a for a in sys.argv[3:] if a != "--law-read"]
        if args:
            real_date(args[0])
        before = open(SOURCE, encoding="utf-8").read()
        open(SOURCE, "w", encoding="utf-8").write(json.dumps(source, ensure_ascii=False, indent=2) + "\n")
        try:
            code = apply(args[0] if args else None, law_read="--law-read" in sys.argv)
        except SystemExit:
            open(SOURCE, "w", encoding="utf-8").write(before)      # stopped before any page was written
            raise
        if code == 2:
            open(SOURCE, "w", encoding="utf-8").write(before)
            print("playbooks/fees.json is as it was.")
        sys.exit(code)
    elif cmd == "where":
        where(sys.argv[2] if len(sys.argv) > 2 else None)
    elif cmd == "table":
        table()
    else:
        print(__doc__)
        sys.exit(2)
