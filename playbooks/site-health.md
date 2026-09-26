# Site accuracy and health

This is the complete instruction set for the site accuracy and health routine, which runs every
Tuesday morning. It replaced the weekly SEO and GEO audit on 24 September 2026. The routine's
pasted prompt in the claude.ai Routines screen is a short launcher that tells each run to read
this file from main, so a change here goes live on the next run with nothing pasted.

## Why it changed

The weekly audit had found the site structurally clean for weeks in a row, while nothing re-read
what the pages say about the law. A full legal review on 24 September 2026, checking every page
against the authorised legislation, led to eighteen corrections across
thirteen pages, among them a statement that an attorney under an enduring power "acts only
at your direction" while the principal has capacity, which the Powers of Attorney Act 2014 does
not say, and a retail leases answer that left repairs to the lease when section 52 of the Retail
Leases Act 2003 puts them on the landlord. Every one of those pages had been published by the
article routine with no human review. Legal accuracy is the firm's first priority on the website
as much as in advice, so this routine now spends most of its effort re-verifying the law on the
live site and correcting it, and does the structural audit once a month.

## Rules

- Read CLAUDE.md and the newest entries of DECISIONS.md first. Establish today's date in
  Melbourne with `TZ=Australia/Melbourne date`; never take it from the session clock.
- Verify against primary sources. legislation.vic.gov.au and legislation.gov.au are reachable:
  read the authorised version of every Act you rely on and record the Act, section and version.
  Court sites and AustLII are blocked; confirm case law by search restricted to official or
  reputable legal sources and say plainly when a judgment itself could not be read.
- Never invent an authority, a section number, a figure or a case. Never introduce a specific you
  have not read this run. When a claim cannot be verified either way, generalise it so the page
  stays useful and true.
- Never promise an outcome, never claim a specialism, and never describe the firm as having more
  lawyers than CLAUDE.md records.
- Change as little as possible. Correct the sentence that is wrong, keep the voice of the page,
  follow every house style rule, and never touch styles or layout.

**From 26 September 2026.** After any push that changes a page, run `python3 scripts/indexnow.py`
with the .html path of every page changed, as the article playbook sets out. Never change a price,
its scope or its exclusions on fees.html: the prices are Spencer's, so a price that looks wrong, or a
statement about court or registry fees that the law has overtaken, goes in the report for him, never
into the page. Each week, check that every article dated from 28 September 2026 carries its Sources
line, and that every provision in any Sources line on a page you check still says what the article
relies on it for.

**Chinese pages, from 26 September 2026.** Simplified Chinese versions of the home, contact, fees
and three practice pages wait on branch `claude/youthful-bohr-aaeqrx` until the firm's Mandarin
reading lawyer has checked them, and nothing on main is held for them. Once they are published in
`zh/`, a run never edits their Chinese text: when it corrects a statement on index.html,
contact.html, fees.html or a practice hub, its report names the matching `zh/` page and the
sentence, with a proposed Chinese wording, for Spencer to have checked.

## Every run: the accuracy sweep

1. The ledger is `scripts/accuracy-ledger.md`. Create it on the first run with one row per page
   that states the law, meaning every `insight-*.html`, every `resource-*.html`, every
   `service-*.html`, `faq.html` and the three practice hubs, each with the date last verified and
   the outcome. The review of 24 September 2026 and the source checks of 26 September 2026
   corrected twenty-four pages, all published on 26 September 2026, and DECISIONS.md names them in
   its entries of those two dates: seed those pages as verified on 26 September 2026 and every other
   page as never verified. On every later run, first add a row for any legal page the ledger lacks: a page
   published on or after 24 September 2026 takes its publication date as the date last verified,
   because the article and service pages routines verify every claim against the authorised
   legislation before they publish, and any other page is never verified.
2. Count the legal pages in the ledger this run, divide by 13 and round up: that is how many
   pages this run verifies, taking those verified longest ago, never verified first, oldest
   article first. Thirteen weeks make a quarter, so every legal page is re-verified at least once
   a quarter however many pages the site gains: 36 legal pages means three a week, and 44 means
   four. Never carry last week's number forward, and state the count and the number verified in
   the report.
3. For each page, extract the visible text and the FAQ JSON-LD, list every legal proposition,
   and check each against its primary source: time limits and their exceptions, thresholds,
   who may apply, which court or tribunal, what the Act requires, and every named statute,
   section and case. Also check anything the law has changed since the page's currency line,
   including Acts that have passed but not yet commenced.
4. Where something is wrong, out of date, or omits an exception a reader could be hurt by
   missing, correct it on the page, keeping visible FAQ answers and FAQPage JSON-LD identical.
   Then set dateModified and any Open Graph modified time to today, update the currency line
   and every "as at" to the current month, show the updated date as the template does, and move
   the page's sitemap `lastmod` to today.
5. Where everything checks out, refresh nothing but the ledger row. The page's own dates change
   only when its words change.
6. Record every correction in the DECISIONS.md entry for the run: page, old sentence, new
   sentence, the source and section read.

## First run of each Melbourne month: the structural audit

Also carry out the structural audit the weekly SEO and GEO routine used to do: every internal link
resolves; unique titles and descriptions within the limits in CLAUDE.md; canonical tags;
JSON-LD parses and is complete; sitemap, feed and llms.txt current; robots.txt still permissive to
AI crawlers; honest alt text; sane heading hierarchy; orphan pages; and up to ten natural cross
links between genuinely related pages. Fix mechanical defects directly. Anything that would
restructure a page or change design goes into the report as a recommendation, never applied.
If a Drive folder named "Search Console exports" holds a recent performance export, let its
queries steer which pages get attention first.

## Publish and report

First run `python3 scripts/refresh-google-rating.py`, as CLAUDE.md requires before publishing, so
a rating change that the Service pages routine reported but may not apply reaches every page. Then
run `python3 scripts/check-publish.py` and `python3 scripts/check-article-images.py`; both must
pass, and the scripts may be strengthened but never weakened. Commit to main as
"Site accuracy and health <Melbourne date>: <summary>" and push with retry. A run that changed
nothing still commits the ledger and its DECISIONS.md line.

The final message, phone readable: the number of legal pages and the weekly number it gives,
the pages verified and the outcome for each, every correction
in one line with its source, the structural audit result when it ran, and anything that needs
Spencer. Never finish silently.
