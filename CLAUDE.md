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

So when a new instruction arrives: write it into this file, record it in
`DECISIONS.md` with the date and the reasoning, and if it can be checked by
machine, add it to a script — all in the same change. A rule that lives only in
a conversation will be lost.

**Read `DECISIONS.md` at the start of every run.** It is the running record of
instructions, corrections and open items, newest first, and it carries context
that this file's rules alone do not explain.

The routine is bound to a persistent chat session, so a run may appear to have
conversational history. Do not rely on it: long conversations are summarised
(lossy) and sessions can be lost. The repo is the source of truth.

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

## Other publishing conventions

- **Publishing is fully automatic** (owner instruction, 4 Aug 2026): each run
  commits the article directly to `main` and pushes — no PR, no approval
  step. The claims register goes in the commit message, and the owner must be
  notified at the end of every run, success or failure. The active trigger is
  `trig_01MQmCMVChumXYRSauyoiVma` (agent-created, so future runs can update it);
  the original PR-flow trigger `trig_01BnmA2SypQV6wtF2Nvtxmzf` is disabled, not
  deleted — do not re-enable it without owner instruction.
- **Cadence is twice weekly** (owner instruction, 4 Aug 2026): Monday AND
  Thursday at 10:00 Melbourne time. Trigger cron is `0 0 * * 1,4` UTC, which is
  10:00 AEST; during daylight saving (first Sunday of October to first Sunday
  of April) it fires at 11:00 AEDT — flagged to the owner, adjust only on
  owner instruction. **Article date = the run's date in Melbourne** (no longer
  "last article + 7 days"). Duplicate guard: if an `insight-*.html` with
  `datePublished` equal to the target date already exists on `main`, stop
  without publishing.
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

As of 4 Aug 2026 the GitHub API **is** available to automated sessions via the
GitHub MCP tools (earlier notes saying it was disabled are stale). `git push`
over the git proxy also works. Publishing is nonetheless direct-push to `main`
by owner instruction — see "Other publishing conventions" and DECISIONS.md.
Photos pasted into the chat UI arrive view-only, not as files: new images must
reach the repo via GitHub (web upload or a local clone), not via chat.

Egress (last verified 4 Aug 2026): `images.unsplash.com`, `unsplash.com`,
Wikimedia and `live.staticflickr.com` are reachable; `pixabay.com`,
`pexels.com` and `openverse.org` still 403. Australian legislation and
court/government sites remain blocked — verify legal specifics via search
restricted to official domains and stay conservative.
