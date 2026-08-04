# Decision log — weekly insights routine

Running record of instructions, decisions and corrections for the automated
weekly article routine. **This file is the source of truth, not the chat.**

A conversation can be summarised when it grows long, or lost with its container.
This file is version-controlled and auto-loaded on every run, so anything
recorded here survives both. When the owner gives a new instruction, write it
here in the same change that implements it — see CLAUDE.md, "Why these files
exist".

Newest entries first.

---

## 2026-08-04 — Routine bound to a persistent chat session

**Owner instruction:** "I want you to live in this chat from now on, so that any
updates or anything moving forward can be provided in here. If it gets capped
out, I also want everything we previously discussed and worked on to survive."

**Done:** the weekly trigger was recreated bound to a persistent session, so each
Monday's run resumes the same conversation instead of starting fresh. The
original trigger (`trig_01H5N5xhWNKTe8KKYtSf3q4s`, created 28 Jul 2026) spawned a
new session per fire and was deleted; schedule (`0 21 * * 0` UTC = Monday 07:00
Melbourne) and prompt were preserved.

**Limitation the owner should know:** session binding gives continuity of
conversation, not durability. Long conversations get summarised, which is lossy,
and a session can be lost with its container. Durability comes from this file,
`CLAUDE.md` and `scripts/` — not from the chat. Anything that matters must be
written down here.

**Side effect:** a session-bound trigger cannot carry the automatic
completion-notification config that the previous fresh-session trigger had. Runs
must therefore send the owner's summary by explicitly calling the notification
tool, as the 3 Aug run did. If notifications stop arriving, this is the cause.

---

## 2026-08-04 — One photograph per article (owner correction)

**Owner instruction:** "every new article published is not a repeat of a previous
one, and that includes photo (there needs to be a different photo for each new
article)."

**What went wrong:** the child support article (3 Aug) shipped using photograph
`1609220136736`, already used by the parenting arrangements article. Uniqueness
had been checked by file checksum. `<id>.jpg` and `<id>-2.jpg` are different
crops of the *same* photograph — different bytes, so a checksum says "distinct"
while a reader sees the same photo. **Uniqueness must be judged on the filename
stem.**

**Fixed:** article reassigned to photograph `1521791136064` across the insights
hero, homepage card, `og:image`, `twitter:image` and JSON-LD.
`scripts/check-article-images.py` added, which groups by stem and fails if any
photograph is used by more than one article; verified it exits 1 on this exact
regression.

**Note:** the replacement is a business handshake — thematically weak for a
Family Law article. It was the only photograph not already claimed. Swap it when
a family-appropriate image is available.

**Contradiction to resolve:** the routine prompt's IMAGES line said "reuse an
appropriate existing image from assets/photos/", which actively pushed toward the
duplication. Corrected when the trigger was recreated on 2026-08-04.

---

## 2026-08-04 — Pre-publish gate added

`scripts/check-publish.py` encodes 35 mechanical checks from the publishing
specification so compliance does not depend on recall: JSON-LD validity and
required fields, date consistency derived from `datePublished` across all six
surfaces, listing-page ordering, the exact-3 homepage teaser, link and asset
resolution, house style, title/description/word-count limits, and photograph
uniqueness. Verified by fault injection (wrong feed date, missing byline, broken
link, leftover TODO, fourth homepage card — all caught).

It deliberately does not check legal accuracy, topic freshness or writing
quality. Those still need the multi-pass human read in the routine brief.

---

## 2026-08-03 — First auto-published article

"How is child support calculated in Australia?" (Family Law), the weekly article
for Mon 3 Aug 2026. Chosen because child support was effectively unwritten —
three passing sentences across 21 articles, and "Services Australia" appeared
nowhere on the site. Practice area rotated to Family Law.

**Published by direct push to `main`, not by merging a PR.** The GitHub API is
not available to automated sessions in this repo ("GitHub access is not enabled
for this session. An org admin must connect the Claude GitHub App for this
organization"), so `gh pr create` and API merges fail. `git push` over the git
proxy works. The claims register went into the commit message instead of a PR
body. **Owner action: connecting the Claude GitHub App would restore the normal
pull-request flow.**

**Verification was indirect.** legislation.gov.au, servicesaustralia.gov.au,
guides.dss.gov.au, fcfcoa.gov.au and art.gov.au are all blocked by the egress
policy (403 on CONNECT), so STEP 5 PASS B ran via search restricted to those
domains rather than by reading the pages. Specifics were treated conservatively
as a result: all dollar figures, the cost-percentage table, per-band night
ranges, the Administrative Review Tribunal commencement date and all reform
commencement dates were omitted rather than risk being wrong.

---

## 2026-07-28 — Standing authorisations (from the routine brief)

- **Auto-publish authorised.** Articles publish without waiting for approval;
  the owner reviews the live site afterwards.
- **SEO explicitly includes AI/answer-engine optimisation** — articles must be
  structured so AI assistants and AI search surfaces can accurately extract,
  quote and cite them, but never by overstating certainty. Accuracy wins every
  trade-off.

---

## Standing environment constraints

| Constraint | Effect |
|---|---|
| GitHub API disabled for automated sessions | No PRs, no API merges. `git push` works. |
| All image hosts blocked (Unsplash, Pixabay, Flickr, Wikimedia, own site) | Cannot download new photos. New images must be added by the owner. |
| Australian legislation/court/government sites blocked | PASS B verification via search only; be conservative with specifics. |

## Open items for the owner

- [ ] **Add photos to `assets/photos/`.** The library is at 22 photographs for 22
      articles — zero spare. The next article cannot publish without a new image,
      and an automated run cannot download one. 800×500 for cards, 1200×630 for
      `og:image`.
- [ ] **Swap the child support article's handshake photo** for something
      family-appropriate once images are available.
- [ ] **Connect the Claude GitHub App** to restore the pull-request flow.
- [ ] Decide whether photograph uniqueness should extend to the practice-area
      pages. Currently `1514395462725` (guardianship article) also appears on
      commercial-law.html, and `1517048676732` (shareholder agreements) on
      family-law.html. These are article-to-section-page repeats, which the check
      does not flag.
