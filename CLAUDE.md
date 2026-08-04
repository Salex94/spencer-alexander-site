# Spencer Alexander Lawyers — site conventions

This repository **is** the live website (static HTML/CSS/JS, no build step,
deployed by GitHub Pages from `main`). Anything merged to `main` is published.

## Before publishing anything, run the gate

```
python3 scripts/check-publish.py
```

35 mechanical checks covering the publishing specification: JSON-LD validity and
required fields, date consistency across all six surfaces, listing-page
ordering, link and asset resolution, house style, word count, and photograph
uniqueness. **Exit 0 is required to publish.** Fix failures; do not work around
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

So when a new instruction arrives: write it into this file, and if it can be
checked by machine, add it to a script in the same change. A rule that lives
only in a conversation will be lost.

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

### When no photograph is free

As at August 2026 the photo library is at capacity — roughly one photograph per
article, with no spare. **A new article therefore needs a new image added to
`assets/photos/` before it can publish.** Adding one requires either:

- the owner dropping a licensed image into `assets/photos/`, or
- network access to an image host.

Note that in the automated publishing environment **all image hosts are blocked**
by the egress policy (`images.unsplash.com`, `unsplash.com`, `cdn.pixabay.com`,
`live.staticflickr.com`, Wikimedia and the live site itself all fail the proxy
CONNECT with 403). An automated run cannot download a new photo. If the check
script reports no spare photographs, stop and ask the owner for an image rather
than reusing one.

### Adding a new image

- Filename: the source photograph id, e.g. `1609220136736.jpg`. Use a `-2`
  suffix only for an alternate crop of a photograph already present.
- Card/hero crop: 800×500. Article `og:image`: 1200×630.
- Always set descriptive `alt` text; keep it consistent wherever the image is
  reused across listing pages.
- Never hotlink an external image for in-page use — in-page `<img>` must point
  at `assets/photos/`. `og:image` may use the source CDN URL, matching the
  convention in recent articles.

## Other publishing conventions

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
- **`robots.txt` must stay permissive.** Never add rules blocking AI crawlers
  (GPTBot, ClaudeBot, PerplexityBot, Google-Extended) — being crawlable by AI
  systems is deliberate.
- **Surfaces to update with every new article:** the article page,
  `insights.html` (hero + first grid card + `blogPost` JSON-LD), `index.html`
  (3 newest teaser cards), `sitemap.xml`, `feed.xml` (new first item +
  `lastBuildDate`) and `llms.txt`.

## Environment note

The GitHub API is not available to automated sessions in this repo
("GitHub access is not enabled for this session. An org admin must connect the
Claude GitHub App for this organization"), so `gh pr create` and API-based
merges fail. `git push` over the git proxy works. Connecting the Claude GitHub
App would restore the normal pull-request flow.
