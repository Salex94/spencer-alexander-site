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

## 2026-08-04 — Weekly run blocked: no spare photograph (no article written)

This run re-checked `scripts/check-article-images.py`: still 22 photographs for
22 articles, zero spare. Also re-tested the image-host egress block directly
(`curl` to `images.unsplash.com`, `cdn.pixabay.com`, `commons.wikimedia.org`) —
all three still fail the proxy CONNECT with 403. Both constraints from the
"Open items for the owner" section below are unchanged, so per CLAUDE.md
("Article images... When no photograph is free") this run **stopped without
writing an article**: no new `insight-*.html`, no branch, no PR. Writing one
would have forced a duplicate photo, which is the exact regression this file
already documents from 3 Aug.

`gh pr list`-equivalent check (`list_pull_requests`, state=open) showed no PR
targeting an insight article — only an unrelated Cloudflare Workers config PR
(#2) — so a missing photo, not a duplicate in-flight PR, is the only blocker.

**Correction to "Standing environment constraints" below:** the GitHub API is
no longer disabled for this session. `mcp__github__get_me` and
`mcp__github__list_pull_requests` both succeeded this run (previously they
failed with "GitHub access is not enabled for this session"). The PR flow in
CLAUDE.md/the routine prompt should work once there is an article to publish —
worth re-verifying with an actual `create_pull_request` call the next time a
photo is available.

**Owner action needed before next Monday's run can publish anything:** add at
least one new licensed photograph to `assets/photos/` (see CLAUDE.md, "Adding
a new image" — 800×500 crop for cards, 1200×630 for `og:image`, filename =
source photo id).

---

## 2026-08-04 — CORRECTED: the routine is NOT session-bound (verified against the API)

An earlier version of this entry claimed the weekly trigger had been deleted and
recreated bound to a persistent chat session. **That was wrong.** It was written
from the conversation narrative rather than checked, which is exactly the failure
mode the rest of this file warns about. Corrected after querying the trigger API
directly.

**Owner instruction that prompted it:** "I want you to live in this chat from now
on, so that any updates or anything moving forward can be provided in here. If it
gets capped out, I also want everything we previously discussed and worked on to
survive."

**Verified actual state** (`list_triggers`, 4 Aug 2026 — exactly one cron trigger
exists across all 140 triggers on the account):

| Field | Value |
|---|---|
| id | `trig_01BnmA2SypQV6wtF2Nvtxmzf` |
| name | Weekly insights article — Spencer Alexander Lawyers |
| cron | `0 21 * * 0` UTC = Monday 07:00 Melbourne |
| enabled | true |
| created_at | 2026-07-22 (**never deleted/recreated**; updated in place 4 Aug) |
| next_run_at | 2026-08-09T21:00Z = Mon 10 Aug, 07:00 Melbourne |
| model | `claude-sonnet-5` |
| session binding | **none** — no `persist_session`, no `persistent_session_id` |

**So each Monday's run starts a FRESH session with no memory of any chat.** The
`send_later` triggers on this account do carry `persist_session` +
`persistent_session_id`; this one carries neither. That is the decisive check —
compare those two fields, not the conversation, if this is ever in doubt again.

**This does not lose anything that matters, and the reasoning still stands:**
durability was never going to come from the chat. Long conversations are
summarised (lossy) and sessions die with their container. It comes from this
file, `CLAUDE.md` and `scripts/`, all of which load fresh on every run. A
fresh-session routine reading a good repo is strictly more reliable than a
session-bound one relying on recall.

**Practical consequence:** never write an instruction into the chat and assume
next Monday inherits it. It will not. Write it here.

**Two knobs currently unset on the trigger**, if the owner wants them:
- `model` is `claude-sonnet-5`. Runs do not inherit a model switched inside a
  chat session — changing the routine's model requires updating the trigger.
- `notifications` is unset. Because this trigger is *not* session-bound, built-in
  completion notifications are available to it (they are only unavailable to
  session-bound triggers). Until enabled, runs must call the notification tool
  explicitly, as the 3 and 4 Aug runs did.

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
| GitHub API — **as of 2026-08-04 this is now available** (`get_me`, `list_pull_requests` succeeded). Previously disabled; leave the PR flow live but re-verify `create_pull_request` actually works the next time there's an article to open one for. | PRs should work again; confirm on next successful article. |
| All image hosts blocked (Unsplash, Pixabay, Flickr, Wikimedia, own site) | Cannot download new photos. New images must be added by the owner. |
| Australian legislation/court/government sites blocked | PASS B verification via search only; be conservative with specifics. |

## Open items for the owner

- [ ] **Add photos to `assets/photos/`.** Still 22 photographs for 22 articles —
      zero spare as of the 2026-08-04 run. Every weekly run will keep stopping
      without publishing until this is done. 800×500 for cards, 1200×630 for
      `og:image`.
- [ ] **Swap the child support article's handshake photo** for something
      family-appropriate once images are available.
- [x] ~~Connect the Claude GitHub App~~ — GitHub API access confirmed working
      2026-08-04; no further owner action needed unless it regresses.
- [ ] Decide whether photograph uniqueness should extend to the practice-area
      pages. Currently `1514395462725` (guardianship article) also appears on
      commercial-law.html, and `1517048676732` (shareholder agreements) on
      family-law.html. These are article-to-section-page repeats, which the check
      does not flag.
