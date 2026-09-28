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
  id `1XfXz8fCckvQ3beGULlvFI_B63Zg9vowU`. It holds eight Google Docs, one per page and one for the enquiry acknowledgement email, each a table of
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
  | 7 Enquiry acknowledgement email | `1G66xrbVCXJXiGcpUGpVV0l3u9EGaV0EhgELAufoW7n8` |

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
4. Applies her changes to document 7 to `COPY.zh` in the bd repository's
   `tools/enquiry-autoreply/Code.template.gs`, runs its `build.py` and `test.js`, pushes, and asks
   Spencer to paste the new `Code.gs` into his Enquiry auto reply script with `chineseChecked` set
   to true, so enquiries from the Chinese contact page are acknowledged in Chinese.
5. Records the publication in CLAUDE.md, DECISIONS.md and the bd repository's CLAUDE.md, and tells
   Spencer what changed.

## After publication

The Chinese pages are translations of English pages that change. When a change to the substance of
index.html, contact.html, fees.html or a practice hub is published, the same change is made in the
matching `zh/` page under `BRIEF.md` and flagged to Spencer for her check, or, from a routine, reported
with a proposed Chinese wording as the site health playbook says. The gate refuses a publish in which
the Chinese fees page's prices differ from the English page's.

## English changes since the Chinese pages were translated

The seven Chinese pages were translated from the English pages of 26 Sep 2026. On 28 Sep 2026 the English
pages they translate changed as below, first as corrections published straight away and then as the
preview Spencer approves as a whole. Before the Chinese pages are published, each change is carried into
the matching Chinese page under `BRIEF.md` and sent to the Mandarin reading lawyer as new rows, and the
publishing session checks this list off.

Corrections, live on the English site since 28 Sep 2026:
- **fees.html:** the introduction now explains that a single figure is a fixed fee and a "from" figure
  covers the work described; for consent orders, card holders pay no filing fee and the Court can waive it
  for hardship, and in a joint application both people must qualify; the probate filing fee is nil where
  the estate's gross value is under $250,000; the parenting plan includes one round of changes.
- **family-law.html:** a late property application needs both people's consent or the court's permission;
  best interests are the paramount consideration, not the only question; 12 months runs from the divorce
  order taking effect; the costs heading says before substantive work starts.
- **wills-and-estates.html:** witnesses need not be adults, and video witnessing is possible; an executor
  is protected after six months only without notice of a claim; an enduring power of attorney starts when
  it is signed and accepted unless it says otherwise; a medical treatment decision maker acts when you
  cannot decide yourself.
- **commercial-law.html:** the disclosure statement is due 14 days before the lease; the statutory demand
  wording; prices for defined documents are published prices, confirmed before substantive work.
- **index.html:** the statutory demand and family provision time limits; the description says a fee
  estimate before substantive work; only the three approved service promises in How we work.
- **contact.html and thank-you.html:** a lawyer replies by phone if a number was left, otherwise by email.

The preview, once Spencer approves it: prices on the hub heroes and service blocks, the family cost
question, links to the eight service pages from the hubs and menus, Fees in the navigation and footer,
the fees page as priced rows with call buttons, the rail card's translator line, new hero leads on the
wills and commercial hubs, the Contact page copy, the thank you page's safety net, the quick exit on the
family page with its note, and the call and enquire bar on phones. The Chinese pages carry none of these
yet; the quick exit label and the Enquire button need Chinese wording she approves.

Photographs, in the preview: the commercial hub's hero and process image and the home page's Commercial card
and insight cards now use new photographs. The Chinese pages keep the old files until their alt text is
translated and checked with the rest.

The final round, live on the English site since 28 Sep 2026: contact.html asks whether it is safe to email
or leave a message, with four answers, and the message is optional; index.html shows six reviews, a new
hero lead, a practice introduction on how the three areas meet with the translator line, the second
process step on fixed fees and the engagement letter, the statement on Spencer's experience, the
admission and Law Institute line and the ABN in the firm schema; commercial-law.html has the statutory
demand strip and a FAQ on what to do when a demand arrives; each hub names Melbourne's eastern suburbs,
says a translator is available and links its pills to the service pages; fees.html gives every fee an
anchor and links each service page; the footer says a Box Hill, Melbourne law firm. The Chinese pages
carry none of these yet, apart from the self-hosted fonts and the stylesheet and script versions.

On 28 Sep 2026 main was published without the Chinese pages by commit a851685, which removed `zh/`, the
中文 links, the hreflang links, the Chinese sitemap entries and the llms.txt section. When the pages are
ready, the publishing session carries the lists above into them, has them checked, merges this branch
into main and reverts a851685 in the same push, then runs the gate.
