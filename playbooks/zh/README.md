# The Chinese pages: review and publication

Spencer decided on 26 Sep 2026 that the site would have Simplified Chinese versions of seven pages: the
home page, contact, fees, the three practice pages and the thank you page, which is noindex. His
instruction was to say only that a Mandarin translator is available, 可提供普通话翻译, and never that a
lawyer at the firm speaks Mandarin. A lawyer at the firm who reads Mandarin checks every Chinese line
before anything is published.

## Where things are

- The pages are `zh/*.html`. On branch `claude/youthful-bohr-aaeqrx` they sit with the 中文 links on
  every English page and the hreflang links on the six English pages they translate. None of it is on
  main until she has finished.
- Her review is in Spencer's Google Drive, in the folder "Chinese website pages: translation check",
  id `1XfXz8fCckvQ3beGULlvFI_B63Zg9vowU`. It holds seven Google Docs, one per page, each a table of
  numbered rows with the English, the Chinese and a note:

  | Document | Drive id |
  |---|---|
  | 0 Start here, rules and terms | `1OFp2B9lFS0NBqg4Ja9ycYyjQtnXRYN2CwUOr_0RtVJ4` |
  | 1 Home page | `1WEKa6GvO7A9J7wGNTK7ps6xaPFmuJc-5PGvWlWowbes` |
  | 2 Family law page | `13wyxsd0pMiBUwMrJa8XNMy0EMknKwJVmGqfBj7wg-HM` |
  | 3 Wills and estates page | `1ImF04pYunGsxPqWu2QR_Hfe_mIH5sJwURWM7hCV3hR0` |
  | 4 Commercial law page | `142ZSgAeOgE4YBVAGFWc9Bw107tu3wc3kS6CM0dXA0WQ` |
  | 5 Fees page | `12F88pLGMWKHkwMDSzgXBs5uYZcojgLGt3b7DBdLGiTk` |
  | 6 Contact and thank you pages | `1ogvsfVpTNm5yQ_eKlBufqm3ahHvn1HUA845RpiVlxLw` |

- `review-baseline/` holds exactly what each document said when it was sent to her, and `BRIEF.md`
  holds the standard the pages were translated to, with the fixed wordings and the rules.

## When she has finished

Spencer tells a session to publish the Chinese pages. That session:

1. Reads each document with Drive `read_file_content`, with `includeComments` true, and compares every
   row's Chinese with `review-baseline/`. She was asked to work in Suggesting mode; if the read shows
   her suggestions only as pending, ask Spencer to accept them all in each document first, under
   Tools, Review suggested edits, then read again. Every changed row and every comment is a change to
   make or a question to answer.
2. Makes each change in the matching `zh/` page, everywhere that string appears: the visible text,
   the title, the meta, Open Graph and Twitter tags, and the JSON-LD, including FAQ answers, which
   must stay identical to the visible ones. A change to a row in the Start here document is a change
   to the shared header, menus or footer and goes into all seven pages alike. Her answers to the
   questions in "Please look at these first", such as VCAT's name and the 《》 around Act titles, are
   applied across every page; a change to the gate's bracket rule for 《》 needs her say so.
3. Merges main into the branch, keeps the Chinese pages in step with any change to the English pages
   they translate since 26 Sep 2026, runs `python3 scripts/refresh-google-rating.py` and
   `python3 scripts/check-publish.py`, and publishes only on a clean gate, following the site's own
   publishing steps, then runs `python3 scripts/indexnow.py` with every changed .html path, the seven
   `zh/` pages among them.
4. Records the publication in CLAUDE.md, DECISIONS.md and the bd repository's CLAUDE.md, and tells
   Spencer what changed.

## After publication

The Chinese pages are translations of English pages that change. When a change to the substance of
index.html, contact.html, fees.html or a practice hub is published, the same change is made in the
matching `zh/` page under `BRIEF.md` and flagged to Spencer for her check, or, from a routine, reported
with a proposed Chinese wording as the site health playbook says. The gate refuses a publish in which
the Chinese fees page's prices differ from the English page's.
