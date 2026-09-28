@AGENTS.md

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

**Routine playbooks, from 24 Sep 2026.** The three routines that work on this
repository, the Monday article, the Tuesday site accuracy and health routine
and the Friday demand scanner, have short pasted launchers that read their full
instructions from `playbooks/` on main, which `_config.yml` keeps off the public
website. The routine prompt described in point 1 above is therefore a launcher,
and structural changes to a job belong in its playbook, where they go live on
the next run with nothing pasted. The lead magnet factory was retired on
24 Sep 2026 and the Service pages routine that briefly replaced it on 26 Sep
2026; the two published resources stay, and `playbooks/service-pages.md` is
kept only as a record.

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
- **Primary legislation is reachable, from 24 Sep 2026.** `legislation.vic.gov.au`
  and `legislation.gov.au` now return the authorised versions of Victorian and
  Commonwealth Acts from the automated environment: the Victorian site links a
  .docx or .pdf of each version, and the Commonwealth text pages and its API at
  `api.prod.legislation.gov.au` work. Every statutory claim is checked there,
  and the note below applies only to the sites that are still blocked. A review
  against these sources on 24 Sep 2026 found eighteen errors across thirteen
  pages, and the source checks of 26 Sep 2026 found thirty-one more across
  nineteen pages; all forty-nine corrections, with a Sources line on every
  article, were published on 26 Sep 2026 with Spencer's approval. See
  DECISIONS.md.
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
  **Also the About page archive (8 Sep 2026):** `about.html` lists every
  article under "Articles by Spencer" in three practice area groups; add the
  new article's `related__link` to the matching group, label from the
  headline. Enforced by check-publish.py ("every article listed in the
  about.html archive").
  **Template placeholders (8 Sep 2026):** `_article-template.html` now
  carries `{{LEAD}}` (the answer first lead, at most 70 words) separately
  from `{{BODY}}` (everything after the lead), `{{UPDATED_HTML}}` (leave
  empty on first publication; on a later edit it becomes an
  `Updated D Mon YYYY` span with a `<time>` element), an "In this article"
  contents list built from the H2s (`{{H2_SLUG_n}}` and `{{H2_TEXT_n}}`;
  give every H2 an id equal to its slug, and drop the whole `article-toc`
  block when the article has fewer than four H2s), and a related reading
  block with three sibling articles (`{{RELATED_SLUG_n}}` and
  `{{RELATED_HEADLINE_n}}`, the three closest articles by topic, same
  practice area first, labels taken from their headlines). Fill every
  placeholder: the gate's "no template placeholders" check fails on any
  `{{` left behind, and "every article has related reading" and "article
  read times match their length" (read time = max(3, round(body words /
  230))) fail on an article without them. Question and answer pairs in the
  closing section are `<h3 class="article-q">` followed by a paragraph, and
  the Article node carries a `speakable` specification pointing at the lead
  and an author node with `jobTitle` "Principal" and the LinkedIn
  `sameAs`, all of which the template shows.

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
  every page when either file changes materially. The webfonts are self hosted in `assets/fonts` since 28 Sep 2026, declared
  at the top of styles.css, and each page head preloads the three first screen faces;
  never load them from Google again, because the privacy page says no font service
  receives a visitor's details.
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
- **Google rating and client reviews (owner instruction, 5 Sep 2026).** The
  firm's Google Business Profile is place id `ChIJ55iT2dyWG2ERsUO1cPTNK2Y`
  (Maps `cid=7362204465613849521`). Its star rating appears as
  `<span data-google-rating>` in the hero on index.html and contact.html, the
  reviews section on index.html and the rail card on every hub and article,
  always as "5.0 stars on Google". **Never state the number of reviews
  anywhere on the site** (owner instruction, 5 Sep 2026, after the first
  version said "from 7 client reviews"); the gate check "review count never
  stated on the site" enforces it. Run
  `python3 scripts/refresh-google-rating.py` before publishing: it reads the
  rating from Google's public Maps embed and rewrites every marked span, and
  the gate check "Google rating markup consistent" fails if any page drifts.
  The reviews section quotes Google reviews exactly as written, using the
  opening sentences of longer reviews and first name plus initial. Source
  for the text is the Google Business Profile notification emails to
  spencer@spenceralexander.com.au; never invent, edit or paraphrase a review,
  never quote client circumstances, and never add Review or AggregateRating
  schema for the firm's own reviews, which Google treats as self serving.
  Read all reviews link: `https://search.google.com/local/reviews?placeid=ChIJ55iT2dyWG2ERsUO1cPTNK2Y`.
- **Profiles.** LinkedIn company page
  `https://www.linkedin.com/company/spenceralexander` and the Maps listing are
  the firm's `sameAs`; the principal's Person node carries
  `https://www.linkedin.com/in/spenceralexanderlawyer`. The footer links
  LinkedIn and the Google reviews page on every page, so any change goes
  through index.html and chrome propagation.
- **Free first call (owner confirmed, 5 Sep 2026).** The first call is free.
  The site says so in the home and contact heroes, the hub hero meta, the
  process steps and every rail card, in the form "Your first call is free,
  and you speak with a lawyer". Keep that wording; do not extend it to a free
  consultation or free advice.
- **Experience wording (owner correction, 5 Sep 2026).** The firm is not ten
  years old; the principal has more than ten years of experience. Every
  experience claim names Spencer, never the firm, for example "Spencer has
  more than ten years of legal experience". Spencer was admitted as a lawyer
  in 2018 (owner, 26 Sep 2026), so no page says he has practised as a lawyer
  for more than ten years; the ten years is legal experience. He is a Law
  Institute of Victoria member, and about.html and its Person schema say both.
- **Entity name.** The firm is "Spencer Alexander Lawyers" everywhere,
  including privacy.html; never "Pty Ltd".
- **Home page film (owner instruction, 5 Sep 2026, placement 6 Sep 2026).**
  The owner's 58 second introduction is the `.film` section, a dark band
  after the practice areas titled "A minute with Spencer Alexander" and
  nothing else: no lead, no rating line, no buttons (the hero above already
  carries them), no meta line, no transcript disclosure. The home page runs
  dark, light, dark, light: hero, proof bar and practice areas, film,
  reviews, how we work on the sunken tone, the principal statement band,
  time limits, insights on the sunken tone, then the call to action. Keep
  that rhythm when adding sections. The film is
  click to play, never autoplay, self hosted in `assets/video/` because the
  owner does not want YouTube. `spencer-alexander-intro-1080.mp4` and the 720p
  version are graded to match the hero portrait up to the end card cut, and
  the end card keeps its true colours. `poster-1920.jpg` is a graded still
  from an engaged moment of the film, never the first frame (the owner found
  the standing start awkward, 6 Sep 2026); the film itself is trimmed by a
  quarter second and fades in from the wine colour so play opens on him
  speaking. (The film was rebuilt on 8 Sep 2026 without a reshoot; see
  "Second enhancement round" below. The captions and end card rules here
  still apply.) `end-card.jpg` the contact card with the QR code and
  `end-card-small.jpg` a phone sized recomposition of it; the script fades
  the right one over the player when playback ends so the code stays on
  screen, and a "Watch again" and call bar appears beneath. The video
  carries native controls in the markup for visitors without script; the
  script removes them and uses the play overlay, then the play event alone
  sets the playing state so a restart from fullscreen, picture in picture
  or a media key never leaves the card over a running film.
  The master's own burned in captions stay exactly as the owner edited them.
  Two attempts to remove them were rejected on 5 and 6 September 2026: a
  crop to 2 to 1 lost too much of the frame, and frame by frame filling left
  captions flashing white where the mask missed them. Never crop them, fill
  them, add a caption track over them, or add a meta line under the heading.
  `preload="none"`
  means no video bytes load until play; the script picks the 720p file on
  handheld or slow connections. A VideoObject JSON-LD block on index.html
  carries the transcript for search and AI answer engines; nothing textual
  sits under the player (the owner removed the visible transcript
  disclosure and the meta line as clutter that does not convert). The copy
  band carries the heading and the player, nothing more. To replace
  the video, run `python3 scripts/prepare-home-video.py <master.mp4> [cut
  seconds]`, then update the duration and
  uploadDate in the schema and the "58 seconds" copy. The spoken line "if you need that expert advice" was flagged to the
  owner as close to a specialist claim and the owner chose to keep it; do not
  reopen it without a new instruction. Never add a second video, an autoplay
  loop, or a review count to this section.
- **Home page details fixed by the 6 Sep 2026 review fleet, keep them.** The
  hero portrait uses a `<picture>` with a 4 by 3 phone crop
  (`assets/principal-portrait-880x660.jpg`) and the caption sits below the
  image on phones, never over the face. The film's play control sits bottom
  left on the dark gradient so it never covers the presenter, and the poster
  is set from `data-poster` by an IntersectionObserver as the band nears, so
  it does not compete with the first paint. Practice card labels are h3s.
  The proof bar's fourth slot states the one business day reply and after
  hours contact rather than repeating the location. Focus rings are a
  3 pixel wine outline on light grounds and brass on every dark ground
  (field-dark, field-wine, topbar, footer), never a box shadow that a
  component can override. Smooth scrolling is wrapped in
  prefers-reduced-motion: no-preference. Home page photographs on the
  practice cards use the 800 by 500 crops. The gate checks JSON-LD blocks
  for duplicate keys.
- **Confirmed firm facts (owner, 5 Sep 2026).** The firm is an active member
  of the Law Institute of Victoria and its liability is limited by the
  Institute's scheme approved under Professional Standards Legislation, cover
  the firm has purchased (Spencer, 28 Sep 2026), so the footer statement stays; the
  first call is free; enquiries are answered within one business day and
  after hours contact is available for urgent matters. Do not add any further
  service promise, and never a specialist claim. The site is in English
  only and offers no translator or interpreter, on Spencer's instruction of
  28 Sep 2026, which replaced his translator line of 26 Sep 2026; see
  "English only" below. The admission year, 2018, and the Law Institute
  membership are on about.html and in every article's author card.

## Second enhancement round, owner request 8 Sep 2026

The owner asked for an honest view of the site, accepted the assessment,
could not reshoot the film and asked for every other enhancement. These
conventions came out of that round.

- **Firm voice: a firm of lawyers with Spencer as its face (owner instruction,
  8 Sep 2026, twice repeated).** The site speaks of "lawyers", "senior
  lawyers" and "exceptional lawyers", never of one lawyer, a sole
  practitioner, or "the principal handling every matter". Spencer is the
  face: the portrait, the film, the About profile, the author of every
  article and the principal who oversees every matter, and quotes in his
  voice are welcome, but nothing may state or imply that he is the only
  lawyer. The h1 is "Exceptional Melbourne lawyers, for when it matters
  most." (the owner's chosen register); a singular headline was tried on
  8 Sep 2026 and rejected the same day. This supersedes the 5 Sep 2026
  caution about "our lawyers": the owner has confirmed the firm has
  lawyers, so the plural is the accurate form. On phones the text block
  comes before the portrait so the promise is on the first screen.
  Fixed forms that carry the voice (9 Sep 2026): the rail card bullet on
  every hub, article and resource page is "Every matter overseen by the
  principal", never a promise of access to him; the proof bar names its
  subject, "Spencer has more than ten years of legal experience"; the home
  description is "Box Hill, Melbourne lawyers for Family Law, Wills and
  Estates and Commercial Law. Free first call with a lawyer, and a fee
  estimate before substantive work." (corrected 28 Sep 2026: a fee is
  disclosed before substantive work, which is what the Uniform Law and the
  rest of the site say); FAQ question one and the About sign
  off say you speak with a lawyer; the founder Person nodes on index.html
  and about.html say "Principal", matching every article author node. Only
  three service promises exist: the free first call, the one business day
  reply and after hours contact for urgent matters. Do not add a fourth.
- **Box Hill first, Melbourne second.** Hub titles and h1s lead with Box
  Hill ("Family Lawyers Box Hill, Melbourne | Spencer Alexander Lawyers", h1
  "Family Lawyers in Box Hill, Melbourne"); the locality sentence on each hub
  names the office, the station and the eastern suburbs; the firm's
  `areaServed` lists Box Hill, Blackburn, Doncaster, Burwood, Balwyn, Surrey
  Hills, Mont Albert and Ringwood alongside Melbourne and Victoria. The wills
  hub title is "Wills & Estates Lawyers Box Hill, Melbourne | Spencer
  Alexander Lawyers" at 71 characters, accepted as within "about 70" so all
  three hubs share one pattern. Do not build suburb doorway pages. Office facts in use: Suite 10, 1 Main Street is
  a short walk from Box Hill station, with parking at Box Hill Central.
- **Article leads answer first.** The `article__lead` is at most 70 words,
  its first sentence answers the H1 question directly, it names any deadline
  the body states, and every fact in it must already be in the body. All 28
  leads were rewritten to this rule on 8 Sep 2026. Enforced by
  check-publish.py ("article lead at most 70 words (site-wide)").
- **Page descriptions 120 to 160 characters on every indexable page**, not
  only articles. Enforced by check-publish.py ("page descriptions 120-160
  chars (site-wide)"); noindex pages are exempt.
- **Contact form** carries one extra field, "Best time for a call back",
  beside the email field; it posts to the same formsubmit address. Labels
  stay to one line at the paired field width, and `.form-row` bottom aligns
  its fields so a wrapped label cannot misalign the inputs.
  `assets/spencer-alexander-lawyers.vcf` is the firm's contact card, linked
  from the film's after bar on phones and from the contact page.
- **Home page film: the office master (owner's second cut, 8 Sep 2026).**
  The film is the owner's second recording, made in the firm's Box Hill
  offices on a locked off camera with no burned in captions. Nothing is
  matted or composited: the presenter and the room are one shot, which is
  the standard the owner set after a matted rebuild of the first cut read as
  fake. `scripts/prepare-home-video.py` takes the master and, in about four
  minutes, replaces the master's own serif cards with the room behind them
  (a clean frame of the same take, or inpainting where the card is on for
  the whole take), applies a light grade only (warmth, a soft vignette, a
  little contrast; never the heavier portrait grade, which turned the room
  pink), overlays lower thirds in Spectral and Libre Franklin with airy
  spacing over a feathered scrim (name card at the start; from 41.6 seconds
  the phone number as the site writes it, "Your first call is free" and the
  web address), fades in from wine, dips to wine before the owner's contact
  card and fades the card in from wine. Overlays on looped images must carry
  shortest=1 and both branches must be 30 fps before concat, or the card
  never appears. The film is 54 seconds; VideoObject duration PT54S,
  uploadDate 2026-09-09, transcript on index.html. The poster is the 14.6
  second frame. No captions are added: the owner rejected added subtitles
  on 5 Sep 2026. The first cut and its matting pipeline are in git history
  at f106992.
- **Top tier design conventions (8 Sep 2026).** The site is judged against
  the best firm sites in the world, so the component vocabulary is type,
  hairline rules and whitespace: radii are 4 and 6 pixels, no card carries a
  shadow or a hover lift, buttons are flat with a 2 pixel radius, the header
  call button is the outline style so the brass hero button is the one
  emphatic call, the top bar carries hours and email but not the phone
  number, body text is 17 pixels at a 1.6 line height, sections breathe at
  64 to 128 pixels, the reviews band is hairline rules with the rating badge
  and no per card stars, icon chips are not used, every stock photograph
  takes one shared muted grade in CSS, and metric matched font fallbacks are
  declared so the page holds its shape before the webfonts load. The header
  carries a practice menu under each hub link listing its six services
  (anchors to the `svc-` ids on the hub), built from index.html and
  propagated to every page by `scripts/propagate-chrome.py`; longer
  articles open with an "In this article" contents list; every article ends
  with related reading and shows its updated date. Keep new work inside
  this vocabulary.
- **Verification round conventions (9 Sep 2026).** The propagation script
  asserts six services per hub and the gate checks every page's practice
  menus carry them; FAQ schema must equal the visible question and answer
  pairs on every article and hub, not only faq.html; every "as at Month
  YYYY" inside an article must match its currency line; every JSON-LD
  object carrying the #firm @id must agree with the index.html node; the
  FAQ page's visible reviewed date, the FAQPage nodes' dateModified and the
  llms.txt Last updated line must match the sitemap; Open Graph article
  dates must equal the Article schema dates. Article nodes carry @id
  (`<url>#article`), url, isPartOf the website node and wordCount, and
  the insights listing uses the same @ids typed Article. Home title
  "Lawyers in Box Hill, Melbourne | Spencer Alexander Lawyers". Form focus
  is a 3 pixel wine outline, never a box shadow; every id has a 100 pixel
  scroll margin; smooth scrolling applies to `html:focus-within` only;
  the reveal effect never touches first screen content; the phone call
  bar hides while the hero call button is visible (`body.cta-visible`) and
  while the menu is open (`body.menu-open`); a print stylesheet lives in
  site.css; `.mobile-menu a.mobile-menu__call` carries the button colours
  because the menu's link rule outranks `.btn--primary`. Keys: site.css
  v18, styles.css v7, site.js v12.
- **WebP for every inline photograph (9 Sep 2026).** Each in-page
  `<img src="assets/....jpg">` sits inside
  `<picture><source type="image/webp" srcset="assets/....webp"><img ...></picture>`,
  the JPEG staying the canonical file for og:image, the schema image and
  the uniqueness check. After adding a photograph run
  `python3 scripts/make-webp.py` to write the sibling; the gate check
  "every in-page photograph has a WebP sibling" blocks a publish without
  it. The film's poster and end cards stay JPEG (they load through
  script, not through a picture element).

## Third round, owner approval 26 Sep 2026

Spencer approved the website review's recommendations on 26 Sep 2026, apart from
recording each enquiry's source page, making the repository private and
re-dating the early articles, and asked for a list of fixed fees at the low end
of the market. These conventions came out of that round.

- **Enquiry links go to the form.** Every "Send an enquiry" button and link
  points at `/contact#enquiry`, and on contact.html at `#enquiry`. The header,
  menu and footer Contact links stay `/contact`. The template carries the
  anchor, so every new article and page does too.
- **The form takes a phone number or an email.** Neither field is required on
  its own; a few lines in `scripts/site.js` stop a submission that has
  neither. Keep both fields and that check.
- **The design stays as it is (Spencer, 26 Sep 2026): "Make sure the site
  layout, design remains untouched. I believe it looks very good, also the SEO
  and GEO on the site are pretty much as strong as they can possibly be."**
  This round therefore added no new components, styles or layout: every change
  is text, links, schema or behaviour inside the existing components, and
  site.css is unchanged. Proof blocks on the hubs, a portrait in the rail cards,
  quotes on the contact and About pages and a rating strip under article
  bylines were built and then removed on that instruction; do not bring them
  back without his say so. Any later change that would alter how a page looks
  goes to Spencer as a recommendation first.
- **Mid article call prompt.** Every article has one straight after the section
  that states a time limit, or where there is none, where a reader is most
  likely to realise they need help, as well as the closing one.
- **Sources.** Every article ends its body with a Sources line,
  `<p class="article-sources">` in the currency line's own inline style, placed
  before the currency line, naming each Act and the sections or Part its
  statements rely on, linked to the authorised version, and mirrors it in the
  Article schema as `citation` entries of type Legislation. Legislation only,
  never cases, and every provision read in the authorised version first. The
  gate requires it for articles dated from 28 Sep 2026, and every older
  article has carried one since 26 Sep 2026.
- **Fixed fees.** fees.html publishes the firm's fixed fees, set on 26 Sep 2026
  at the low end of what Melbourne firms publish, on Spencer's instruction
  "I want everything to be very affordable. Like on the lowest end of the
  range." Every price is a single figure including GST, as section 48 of the
  Australian Consumer Law requires, with its scope, its assumptions and what
  it excludes, and court, registry and government fees are stated as separate
  and passed on at cost. Only Spencer changes a price. The page is built from
  the privacy page's structure with the article body's own list style, and the
  hub fee notes, the FAQ and the contact page link to it.
- **Maps.** Every map link, the footer address and the contact page's
  directions, opens the firm's own Google listing through the
  `query_place_id` form, never a bare street address pin, which a neighbouring
  firm shares.
- **404.** The 404 page carries the call button, the enquiry button, the three
  hubs and the mobile call bar, and a few lines of script send an address
  typed with a trailing slash to the same address without it.
- **IndexNow.** The key file `25747fcf3f9fd2bc54bf5ee54d16b678.txt` at the site
  root proves the site to Bing and the other IndexNow engines; never delete or
  rename it. After a push that changes pages, `python3 scripts/indexnow.py`
  with their .html paths tells those engines the same day.
- **Firm schema.** The firm's `sameAs` lists the Google listing, the LinkedIn
  company page and the Yellow Pages listing.
- **About.** The articles are described as published under Spencer's name, not
  as written by him each week. About lists no earlier roles, on Spencer's instruction of 28 Sep 2026:
  they are not relevant, because he works at this firm.
- Keys after this round: site.css v18, unchanged, styles.css v7, site.js v13.

## Fourth round, owner request of 28 Sep 2026

Spencer asked for the site to be the strongest it can be for search, AI answers,
conversion, design, layout and content, assessed against a brief he supplied, with
nothing left that would stop an honest yes on each. Six audits ran that day. What
came out of them and is settled:

- **Corrections and fixes publish straight away**, on the same footing as the site
  accuracy and health routine's corrections under Spencer's rules of 24 and 26 Sep
  2026: legal corrections read against the authorised legislation and checked a
  second time, faults in the build such as an unreadable button or a clipped
  header, phone numbers that could not be tapped, claims that were no longer true,
  and wording that contradicted what Spencer had already confirmed. Everything
  else the audits recommended, new pages, copy rewrites, photographs and anything
  that changes how a page looks, goes to Spencer as one preview for his approval.
- **Experience wording** is one form everywhere: more than ten years of legal
  experience, admitted as a lawyer in 2018, member of the Law Institute of
  Victoria, and the two degrees. The author card on every article carries it.
- **The desktop navigation starts at 1100 pixels**, not 960, so the header call
  button is never cut off on a tablet held landscape.
- **Poster.** The film's poster is `assets/video/poster-1920.jpg`, the same 14.6
  second frame exported at full width so it is sharp on high density screens.
- **Prices stay in step.** Wherever a page other than fees.html quotes a fixed
  fee, the figure must be one fees.html carries; the gate's "prices quoted
  elsewhere match fees.html" check fails any other, so a price Spencer changes on
  fees.html must change everywhere it is quoted in the same commit.
- **Lastmod never trails the schema.** The gate fails any page whose sitemap
  lastmod is older than a dateModified in its own schema. Boilerplate such as the
  author card does not move a page's dates; a change to what the page says does.
- **Accessibility fixes that change nothing visible**: on phones a control reached
  by keyboard scrolls clear of the call bar, the top bar and the call bar sit in
  labelled regions, and the enquiry hint is tied to the phone and email fields.
- **Hub hero photographs** offer 800 and 1200 pixel WebP files, so phones take the
  smaller one; `scripts/make-webp.py` writes a WebP for every width in an image's
  srcset. `scripts/propagate-chrome.py` now works in whatever checkout it sits in.
- **Article rail card.** The template's quiet rail card is a generic "Our practice
  areas" card; every article replaces it with its own practice area's card, copied
  from a sibling article in the same area, and the gate's "article rail card
  matches its practice area" check fails an article that keeps the generic one.
- **llms.txt** carries the admission year, the Law Institute membership and
  "published under his name", matching about.html.
- Keys after this round: site.css v19.

## Preview and final round of 28 Sep 2026, published the same day

Spencer asked for a final review so that every category is the best it can be and gave full rein to
implement it: "You have full rein to implement evrything you see fit accordingly". The preview below and
the final round were published to main on 28 Sep 2026; DECISIONS.md records both.

- **Service pages.** Eight `service-*.html` pages, the playbook's cap, built by
  `scripts/build-service-page.py` from content files in `playbooks/service-content/`, which hold the
  words while the script holds the design: head, header, menus, footer, call bar and rail call card
  come from the practice hub, and the body uses only the hubs' own components. To change a page, edit
  its content file and rebuild; never hand edit the page. Each hub service block that has a page ends
  with a "Read more about" link to it, the header practice menus link that page instead of the hub
  anchor, and the hub's OfferCatalog item carries the page's @id and url. The gate's service page
  checks come from `playbooks/service-pages.md`, whose fee rule is replaced: a page quotes the fixed
  fees fees.html carries, in the same figures, and says everything else is estimated in writing.
- **Fees in the chrome.** Fees sits between FAQ and About in the navigation, in the mobile menu and in
  the footer's Firm column as "Fixed fees". The navigation is compact from 1100 to 1279 pixels so the
  header call button always keeps its 24 pixel margin.
- **Prices where people decide.** Each hub hero meta line links its section of the fees page with one
  price, each hub service block ends with its published price, and the family hub's cost question
  replaces what to bring, which the family service pages carry. fees.html sets each price on a
  hairline row, price aligned right, with the hero call buttons, jump links and a closing band.
- **Phones.** The fixed bar offers Call and Enquire side by side; the menu button shows a close mark
  while the menu is open; hub photographs are hidden under 640 pixels so the call to action and the
  urgent strip come first.
- **Quick exit** on the family hub, every Family Law article, the separation checklist and the family
  service pages, leaving for the Bureau of Meteorology site and replacing the page in the history; the
  gate checks it is present. It has no keyboard shortcut, because Escape already closes the menus.
- **Look.** Links inside running text carry a fine underline; the home hero is shorter on laptops so
  its call button sits above the fold; brass text is one step deeper for contrast (`--text-seal` is
  brass 800); resource cards are text cards; the home page shows six reviews; the home hero
  portrait overlay matches About.
- **Enquiries.** The contact form asks, optionally, whether it is safe to email or leave a message,
  in the field `safe_to_contact` whose four answers the auto reply in the bd repository reads, and the
  message is optional. `scripts/site.js` adds the Melbourne date and time to the enquiry's `_subject` on submit, so
  Gmail never groups two enquiries in one thread. Keep the field name and its four answers exactly as
  they are, or change the auto reply's `emailSafe_` in the same change.
- **Paths to a call.** Every fee on fees.html has an id, `fee-<slug>`, and its name links the matching
  service page; faq.html answers carry ids, `q-<slug>`, and a link to one opens it; hub pills link their
  service pages; the commercial hub's urgent strip and a FAQ say what to do the day a statutory demand
  arrives, with an email link for a photo of it.
- **Trust.** The firm node carries the ABN as `taxID`; About links the Register of Lawyers; each hub
  names Melbourne's eastern suburbs.
- **Letters of administration** at $1,980 is always quoted as where there is no will, as fees.html
  prices it. The probate page says nothing about costs being paid from the estate until Spencer gives
  his view on rule 9.01 of the probate rules.
- **Listing read times** on insights.html and index.html must equal each article's own; the gate
  checks it.
- Keys after this round: site.css v21, styles.css v9, site.js v17.

## Spencer's instructions of the evening of 28 Sep 2026

- **His voice is the standard for everything written for the site.** Every article, FAQ answer,
  correction and page is written as the spencer-alexander-voice skill sets out, and AGENTS.md at the
  root carries his writing rules and exemplar for any session without the skill. `scripts/check_style.py`
  is the skill's checker, the same one the bd repository uses; run it on the visible text of anything
  written and fix every failure other than the (Vic) and (Cth) of Act titles and the phone number.
- **Nothing about AI.** "I don't want any comments re AI on the website." No page, article, FAQ,
  schema, llms.txt, feed or contact card mentions AI, artificial intelligence or any AI product, and no
  article is ever about AI. llms.txt keeps its name and its job but no longer says it is for AI systems.
  The gate's "no mention of AI anywhere on the site" check fails any mention.
- **No photo shoots and no new video.** The photographs and the film were assessed that evening: the
  film's titles, colour, loudness at about minus 16 LUFS, fast start and end card QR code, which scans
  to the firm's correct contact card, are right, and every photograph suits its page apart from the
  dying without a will article's, a newspaper chart whose alt text wrongly described a ledger, now a
  family in silhouette on a beach. The handshake, toy house, Lady Justice, motivational sign and office
  laptop spares were deleted so no routine uses them. Never recommend a shoot or a reshoot again.
- **Professional Standards.** The firm is an active Law Institute of Victoria member covered by its
  scheme, which it purchased, so the limitation statement in every footer is correct.
- **ABN.** The firm's main business location is Box Hill 3128, the office address the site uses. The
  public ABN register still showed VIC 3106 on 28 Sep 2026 until Spencer updates it; the site is right.
- **About** lists no earlier roles.
- **Prices, Spencer's instruction of 28 Sep 2026.** A single will is $450 plus GST, $495 in total, and
  wills for a couple $800 plus GST, $880 in total; every other price stayed as it was. fees.html shows
  each price as the total including GST, the prominent figure, with the amount before GST beneath it in
  smaller type, because section 48 of the Australian Consumer Law requires the total to be at least as
  prominent as any part of it. The company set up row states instead that its ASIC fee carries no GST.
  Every other page, the schema, llms.txt and the Business Profile quote the total including GST. The
  gate's "fees page amounts before GST match the totals" check keeps the two figures in step.

## English only, Spencer's instruction of 28 Sep 2026

"We are an Australian law firm based in English and should only provide English content / services, so
let's scrap the mandarin or other language considerations." The seven Simplified Chinese pages built on
26 Sep 2026 were never published and have been deleted, with their review notes, and the line "A Mandarin
translator is available" has been removed from every page, the rail card, the contact form and llms.txt.
Every page is `lang="en-AU"`, with no hreflang, no page in another language and no offer of a translator
or interpreter. Never add one without a new instruction from Spencer. The gate's English only check fails
a `zh/` directory, a page in another language, an hreflang link, text in a non Latin script, any mention of Mandarin or Cantonese,
and any offer of a translator or interpreter; a statement of law about translating documents stays allowed. Keys: site.js v17, English only.

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
