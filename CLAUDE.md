# Spencer Alexander Lawyers — site conventions

This repository **is** the live website (static HTML/CSS/JS, no build step,
deployed by GitHub Pages from `main`). Anything merged to `main` is published.

## Before publishing anything, run the gate

```
python3 scripts/check-publish.py
```

About 55 mechanical checks (the exact count varies with conditional checks
and page counts) covering the publishing specification: JSON-LD validity and
required fields, date consistency across all seven surfaces, listing-page
ordering, site-wide link and asset resolution, clean-URL link style, house
style, word count, photograph uniqueness, resource page validity and the
faq.html FAQ schema (extended 1 Sep 2026; strengthening the gate is always
allowed, weakening never). **Exit 0 is required to publish.** Fix failures; do not work around
them.

It deliberately does **not** check the three things that matter most and cannot
be automated: whether every legal claim is true, whether the topic genuinely
avoids rehashing an existing article, and whether the writing is good. Those
still need the multi-pass read described in the routine brief.

## Why these files exist (read this before adding a rule)

Instructions given in conversation do not survive to the next scheduled run —
each run starts with no memory of previous chats. Only three things persist:

1. **The routine prompt** — the standing task brief, owned and edited by the
   owner outside this repo. Structural changes to the job belong there.
2. **This file** — auto-loaded from the repo on every run. Conventions,
   corrections and hard-won lessons belong here.
3. **`scripts/`** — anything mechanically checkable belongs here, because a
   failing check does not depend on anyone remembering the rule.

So when a new instruction arrives: write it into this file, record it in
`DECISIONS.md` with the date and the reasoning, and if it can be checked by
machine, add it to a script — all in the same change. A rule that lives only in
a conversation will be lost.

**Read `DECISIONS.md` at the start of every run.** It is the running record of
instructions, corrections and open items, newest first, and it carries context
that this file's rules alone do not explain.

## Melbourne dates, always (owner rule, 27 Aug 2026)

Every scheduled run fires while UTC is still the previous day (Monday 6:00am
AEST is Sunday 8:00pm UTC), and the session clock shows UTC, so a run that
takes "today" from it operates a day behind Melbourne. This is how the first
lead magnet (`resource-separation-first-30-days.html`, actually published
Wednesday 26 Aug 2026 Melbourne) came to carry `datePublished` 2026-08-25,
and how the 25 Aug SEO audit stamped its commit 2026-08-24; the article
routine escaped only because its prompt already insists the article date is
TODAY in Melbourne. Standing rule: at the start of every run, establish
today's date in Australia/Melbourne (for example `TZ=Australia/Melbourne
date`) and use Melbourne dates for everything: article and resource dates,
feed pubDates, sitemap lastmod, commit messages, DECISIONS entries, subject
lines and summaries. Never take the date from the session clock. The
misdated resource keeps its published date (it is already indexed and one
day of drift is not worth a metadata rewrite); this rule prevents the next
one. The `spencer-alexander-bd` repo carries the same rule as its CLAUDE.md
section 7.

Each scheduled run starts a fresh session with no memory of previous chats
(corrected 1 Sep 2026: an earlier note wrongly said the routine was bound to
a persistent session). Never rely on conversational history existing. The
repo is the source of truth.

If this file and the routine prompt ever conflict, the scripts are the
tie-breaker in practice — they block the publish either way. Flag the conflict
to the owner so the routine prompt can be corrected.

## Article images — every article gets its own photograph

**Rule: no photograph may appear on more than one insight article.** Each new
article must use a photograph that no existing article uses. This applies to the
`insights.html` featured hero, the `insights.html` grid card, the `index.html`
teaser card, and the article's own `og:image` / `twitter:image` / JSON-LD
`image`.

Before publishing, run:

```
python3 scripts/check-article-images.py
```

It must print `PASS`. Treat a `FAIL` as a blocker, not a warning.

### The trap that caused this rule

Files in `assets/photos/` are named after the **source photograph**, with an
optional `-N` suffix for an alternate crop of the same photograph:

```
1609220136736.jpg      <- source photograph 1609220136736
1609220136736-2.jpg    <- a different crop of the SAME photograph
```

Those two files have **different bytes** but look identical to a reader. A
checksum comparison says they are distinct; a human says they are the same
photo. Always judge uniqueness on the filename stem (strip the `-N` suffix),
which is what the check script does. Comparing by checksum is how the child
support article (3 Aug 2026) shipped with the same photo as the parenting
arrangements article.

### When no photograph is free — source one yourself (owner instruction, 4 Aug 2026)

The owner has instructed runs to **source photographs autonomously** ("you find
the legitimate photo, from anywhere on the internet"). Preference order:

1. **Use a spare from `assets/photos/`** if `check-article-images.py` reports
   one free (a pool of spares was committed 4 Aug 2026).
2. **Download a new photo from Unsplash** (`images.unsplash.com` became
   reachable on 4 Aug 2026 — earlier notes saying all image hosts are blocked
   are stale; `pixabay.com`, `pexels.com` and `openverse.org` were still
   blocked when last tested). Unsplash's licence permits free commercial use
   and is the site's existing photo source. Process that works without an API
   key: construct `https://images.unsplash.com/photo-<id>?q=80&w=800&h=500&fit=crop&fm=jpg`,
   confirm HTTP 200 (a wrong id 404s), download, and **visually inspect the
   image before use** — confirm the subject genuinely suits the article and is
   professional in tone. Never commit an image you have not looked at.
3. If neither works (hosts blocked again, nothing suitable), **stop without
   publishing and notify the owner** — never reuse an existing article's
   photograph.

Only use photos under a licence that clearly permits commercial use without
attribution (Unsplash licence, CC0). Never use images of identifiable private
individuals as though they were clients, and avoid recognisable logos.

### Adding a new image

- Filename: the source photograph id, e.g. `1609220136736.jpg`. Use a `-2`
  suffix only for an alternate crop of a photograph already present.
- Card/hero crop: 800×500. Article `og:image`: 1200×630.
- Always set descriptive `alt` text; keep it consistent wherever the image is
  reused across listing pages.
- Never hotlink an external image for in-page use — in-page `<img>` must point
  at `assets/photos/`. `og:image` may use the source CDN URL, matching the
  convention in recent articles.

## Article priorities (owner-confirmed, 4 Aug 2026)

When choosing and writing each article, the priority order is:

1. **Accuracy above everything — paramount.** A claim only survives if it is
   certainly correct; anything uncertain is generalised or dropped, even when
   the specific version would rank or convert better. Never trade accuracy
   for any priority below.
2. **No repeats** — genuinely new ground against every existing article.
3. **Practice-area rotation** — cycle Family Law, Wills & Estates, Commercial
   Law; rotate away from the most recent articles' areas.
4. **Search demand** — within the due practice area, pick the subtopic with
   the strongest real search intent and a clear primary keyword.
5. **AI/answer-engine optimisation** — structure articles so AI assistants
   and AI search surfaces can accurately extract, quote and cite them
   (question-style headings, direct answers) — never by overstating certainty.
6. **Persuasiveness and client acquisition** — every article should read as a
   reason to call the firm: confident plain-English authority, practical value
   that demonstrates competence, and a natural call to action to
   (03) 9125 8355. Persuasive framing must stay within what is accurate;
   accuracy wins every trade-off.

## Clean URLs: clickable links drop .html, canonical URLs keep it (owner instruction, 15 Aug 2026)

The owner does not want `.html` visible in any clickable link. Every internal
`<a href>` on every page (navigation, mobile menu, footer, breadcrumbs, cards,
in-article cross links, CTAs, the article template) uses the clean
root-relative form:

- `/commercial-law`, `/family-law`, `/wills-and-estates`, `/insights`, `/faq`,
  `/about`, `/contact`, `/insight-<slug>`; home is `/`.
- Never add a trailing slash (`/contact/` returns 404 on GitHub Pages).
- The contact form's `_next` redirect is `https://www.spenceralexander.com.au/thank-you`.

This works because GitHub Pages serves `name.html` for a request to `/name`
automatically (verified live on this domain, 15 Aug 2026: both `/about` and
`/about.html` return 200). No redirects exist or are needed; both URL forms
keep working.

**The SEO and GEO surfaces are deliberately unchanged and must stay that
way:** `rel="canonical"`, `og:url`, every JSON-LD URL (`mainEntityOfPage`,
BreadcrumbList items, author `@id`/`url`, the insights `blogPost` list),
`sitemap.xml`, `feed.xml` and `llms.txt` all keep the full
`https://www.spenceralexander.com.au/<page>.html` addresses. Those are the
URLs Google and AI answer engines have indexed. A crawler that follows a clean
link finds a canonical tag pointing at the `.html` address it already knows,
so nothing is re-indexed or migrated. (Search Console may report clean URLs as
"Alternate page with proper canonical tag"; that is expected and harmless.)

**Do not migrate canonicals to extensionless URLs without an explicit owner
instruction.** That would change every indexed URL and, since GitHub Pages
cannot issue redirects, would rely on canonical hints alone: real ranking
risk for zero visible gain.

**This applies to every future edit and every new page** (owner confirmation,
15 Aug 2026), not just insight articles: any page added to the site gets clean
clickable links and a `.html` canonical, with the same split as above.

Enforced by check-publish.py ("clickable links extension-free (site-wide)"
scans every `*.html` file in the repo; "canonical + og:url keep .html"; the
link resolver understands clean links). check-article-images.py finds listing
cards by the clean href form and still accepts the old `.html` form.

## Other publishing conventions

- **Publishing is fully automatic** (owner instruction, 4 Aug 2026): each run
  commits the article directly to `main` and pushes — no PR, no approval
  step. The claims register goes in the commit message, and the owner must be
  notified at the end of every run, success or failure. The active routine is
  `trig_011EeJwAxwjysuSDRYyzCCUb` ("Weekly website insights article"), an
  owner-created routine built in the claude.ai Routines UI on 13 Aug 2026.
  Agents cannot edit or fire it; flag any needed schedule or prompt change to
  the owner. The old agent-created triggers, including
  `trig_01MQmCMVChumXYRSauyoiVma`, were deleted in the 13 Aug rebuild.
- **Cadence is weekly** (owner decision, 13 Aug 2026): every Monday at 6:00am
  Melbourne time, replacing the earlier twice weekly Monday and Thursday
  10:00 cadence. The routine's cron is `0 20 * * 0` UTC, which is Monday
  6:00 AEST; during daylight saving (first Sunday of October to first Sunday
  of April) it fires at 7:00 AEDT. The schedule lives in the owner-created
  routine, which agents cannot edit; flag timing drift to the owner instead
  of adjusting anything. **Article date = the run's date in Melbourne** (no longer
  "last article + 7 days"). Duplicate guard: if an `insight-*.html` with
  `datePublished` equal to the target date already exists on `main`, stop
  without publishing.
- **No dashes in the writing** (owner instruction, 6 Aug 2026). The owner
  finds dash punctuation informal and does not want it. No em dashes, no en
  dashes, no hyphens used as sentence punctuation (a hyphen with spaces
  around it) anywhere in a new article: title, meta description, visible
  body, image alt text and JSON-LD. Restructure the sentence with a comma,
  colon, full stop or parentheses instead. Hyphenated compound words such as
  "12-month rule" or "court-appointed" are normal formal English and remain
  allowed. Apply the same style to owner-facing notification text. Enforced
  by check-publish.py for articles dated after 2026-08-06 (earlier articles
  predate the rule and are exempt; do not rewrite them without owner
  instruction).
- **No topic rehashes.** A new article must not substantially overlap an
  existing one in substance, even under a different title. The exception is a
  genuine change in the law, which must be framed as an update, substantiated,
  and linked to the earlier article.
- **Accuracy outranks everything.** Never invent case names, statutes, section
  numbers or figures. If a specific is not certain, generalise it — the article
  must stay useful without it. Figures that index annually (thresholds, minimum
  rates, fee scales) are safest omitted.
- **Verification note:** Australian legislation and court/government sites
  (`legislation.gov.au`, `servicesaustralia.gov.au`, `guides.dss.gov.au`,
  `fcfcoa.gov.au`, `art.gov.au`, `vcat.vic.gov.au`) are also blocked by the
  egress policy in the automated environment. Verify via search restricted to
  those domains and be correspondingly conservative with specifics.
- **Sitemap lastmod moves with the page** (1 Sep 2026): any run that changes
  a page's visible content bumps that page's `<lastmod>` to the Melbourne
  date of the change in the same commit. Pages without article schema
  (faq.html, index.html, insights.html, the practice hubs, resources.html)
  have no other freshness signal; two SEO audits missed months of staleness
  before this rule.
- **Privacy page and email capture** (1 Sep 2026): `privacy.html` is linked
  from every footer's Firm column and NOWHERE else: never the navigation menu
  or the mobile menu (owner correction, 1 Sep 2026, after a careless sweep
  put it in both; enforced by check-publish.py "privacy link never in
  navigation"). The page itself mirrors faq.html's structure exactly (same
  header, pagehero and article body classes); never build a new page from
  invented class names, clone an existing page. It describes the contact
  form's third party delivery (formsubmit.co) and the no-analytics reality;
  keep it true when either changes. Resource pages carry the "Email me this checklist" subscribe block
  (formsubmit, `_subject` "New insights subscriber"); the monthly newsletter
  routine reads those submissions, and every new resource copies the block.
- **No specialist claims** (1 Sep 2026): the firm holds no accredited
  specialisation, so site copy says "practice areas", never "specialist
  areas" or "areas of speciality" (footers and the home page were reworded).
  Factual uses of the word inside article content (a medical specialist, a
  specialist court list) are fine.
- **`robots.txt` must stay permissive.** Never add rules blocking AI crawlers
  (GPTBot, ClaudeBot, PerplexityBot, Google-Extended) — being crawlable by AI
  systems is deliberate.
- **Surfaces to update with every new article:** the article page,
  `insights.html` (hero + first grid card + `blogPost` JSON-LD), `index.html`
  (3 newest teaser cards), `sitemap.xml`, `feed.xml` (new first item +
  `lastBuildDate`), `llms.txt`, and the Related reading list of the article's
  practice-area page (owner approval, 1 Sep 2026: every article is linked from
  its hub, `family-law.html`, `commercial-law.html` or
  `wills-and-estates.html`, matching its `articleSection`; add one
  `related__link` entry before the "All insights" line, label drawn from the
  article's own headline, no dashes). Enforced by check-publish.py ("article
  linked from its practice page").

## Site design v3 and site-wide house style, owner review 5 Sep 2026

The owner had the whole site reviewed and redesigned on 5 Sep 2026: legal
accuracy, advertising compliance, visual design, content weight, conversion,
SEO and GEO. The conventions below came out of that work and apply to every
future edit, every new page and every new article.

- **Chrome is propagated from index.html.** The top bar, header, navigation,
  mobile menu, footer and mobile call bar on every page are copies of the
  index.html versions. To change any of them, edit index.html first and then
  copy the same markup to every other page. check-publish.py enforces "footer
  identical on every page" and "exactly one skip link + main landmark on every
  page". Never hand edit one page's header or footer in isolation.
- **Stylesheets.** `styles/styles.css` is one flattened file of tokens and
  base styles with no @import chain, and `styles/site.css` carries every
  component. Both are linked with `?v=3`; bump the version on both links on
  every page when either file changes materially. Google Fonts load through a
  preload link with a noscript fallback. Keep both arrangements.
- **No dashes anywhere on the site.** The 6 Aug 2026 article rule now applies
  to every page, every JSON-LD block, feed.xml and llms.txt: no em dash, no en
  dash, no spaced hyphen. check-publish.py enforces "no dashes on core pages"
  and the article check for anything dated after 2026-08-06. New prose also
  avoids parentheses, apart from statute citations such as the Vic and Cth
  suffixes and the phone number.
- **Titles and descriptions.** Title tag at most about 70 characters including
  the " | Spencer Alexander Lawyers" suffix. Meta description between 120 and
  160 characters, identical in the meta tag, og:description and the JSON-LD
  description.
- **Article layout.** Every article uses the `.article-layout` grid: the body,
  an aside rail holding the practice-area card, the author card and the call
  prompt, and an `.article-foot` block with related reading. New articles copy
  `_article-template.html`, which carries that layout, the article figure,
  the author and publisher `@id` links and the currency line.
- **Currency line.** Every article body ends with "This guide reflects the law
  applying in Victoria as at Month YYYY." The month must match the article's
  `dateModified`; check-publish.py enforces "currency line month matches
  dateModified". Any change to an article's substance updates the currency
  line, `dateModified` and the sitemap `lastmod` in the same commit.
- **Schema.** The firm node is `https://www.spenceralexander.com.au/#firm`, a
  LegalService on index.html with an embedded founder Person, `assets/logo.png`,
  an E.164 telephone and hasMap. Every Article and HowTo publisher references
  that `@id`, and every author references the principal's Person node at
  `about.html#spencer-alexander`. Hubs carry Service, OfferCatalog, FAQPage and
  BreadcrumbList; faq.html's FAQPage carries author, publisher and
  dateModified.
- **Portraits and logo.** `assets/logo.png` is the schema logo.
  `assets/principal-portrait-880.jpg` is the home hero portrait and
  `assets/principal-portrait-240.jpg` the author card portrait.
- **Hub pattern.** Urgent time limit strip first, then an "In brief" entity
  sentence, one paragraph of prose, six service blocks that each link an
  article and end in a call prompt, pills for the remaining matters, a sticky
  rail with the call card, six FAQs, and a compact related reading list. Keep
  new hub content inside that pattern rather than adding sections.
- **Claims that stay generic until the owner confirms them.** See the
  DECISIONS.md entry for 2026-09-05. Do not add a free first call promise, a
  response time promise, a years of experience figure, a scheme membership
  statement or a specialist claim beyond what is already on the site.

## Permission prompts (owner wants zero — see DECISIONS.md 2026-08-06)

The owner has asked that runs never require their input. Two facts every run
must know:

- A run **cannot** write `.claude/settings.json` or otherwise grant itself
  permissions — the Auto Mode classifier hard-blocks it. Do not retry or work
  around it. The prepared allowlist lives at
  `scripts/preapproved-claude-settings.json`; only the owner can activate it
  (rename to `.claude/settings.json` on GitHub, or add the repo as a source in
  the environment settings). If `.claude/settings.json` exists, the owner has
  activated it — never edit or weaken it without owner instruction.
- If a run is blocked waiting on a permission the owner has not granted,
  proceed with whatever else is possible; if publishing itself is blocked,
  stop without degrading and tell the owner exactly which approval was missing
  (per the standing notify-on-every-run rule).

## Environment note

As of 4 Aug 2026 the GitHub API **is** available to automated sessions via the
GitHub MCP tools (earlier notes saying it was disabled are stale). `git push`
over the git proxy also works. Publishing is nonetheless direct-push to `main`
by owner instruction — see "Other publishing conventions" and DECISIONS.md.
Photos pasted into the chat UI arrive view-only, not as files: new images must
reach the repo via GitHub (web upload or a local clone) or the owner's Google
Drive, never via chat. The Drive path (proven 1 Sep 2026 with the new
principal portrait): the owner uploads the photo to Drive; a session holding
the Drive connector can download files under 10 MB with
`download_file_content`. For larger files, ask the owner to set the file to
"Anyone with the link", then fetch
`https://drive.google.com/uc?export=download&id=<fileId>` directly
(drive.google.com egress works). Remind the owner to set the file back to
Restricted afterwards. Gmail attachments are not downloadable; do not promise
that route.

Egress (last verified 4 Aug 2026): `images.unsplash.com`, `unsplash.com`,
Wikimedia and `live.staticflickr.com` are reachable; `pixabay.com`,
`pexels.com` and `openverse.org` still 403. Australian legislation and
court/government sites remain blocked — verify legal specifics via search
restricted to official domains and stay conservative.
