# Baseline, recorded on Monday 23 November 2026 before any change

Everything below was observed between 2:35pm and 3:00pm Melbourne time on 23 November 2026, before the first edit
on the branch.

## What was live

The live site was commit 57dad24 of main, the article of 23 November 2026. GitHub Pages deployment run 45059706494
finished at 6:16am Melbourne time that day, and every page answered with the header
`last-modified: Sun, 22 Nov 2026 19:16:02 GMT`, which is the same minute.

The crawl started from sitemap.xml and followed every internal link. It fetched 136 addresses: the 65 in the
sitemap, the same pages at their clean addresses, the 404 page, the two thank you pages, feed.xml, llms.txt,
robots.txt and the contact card. All 136 returned 200. Every page was byte for byte the file in the repository at
57dad24, so the live site and the source agree and nothing is deployed from anywhere else.

| Page type | Pages in the sitemap |
|---|---|
| Home | 1 |
| Practice hubs | 3 |
| Service pages | 12 |
| Articles | 39 |
| Checklists | 2 |
| Other core pages: contact, about, FAQ, fees, insights, resources, referrals, privacy | 8 |
| Total | 65 |

The 404 page and the two thank you pages carry noindex and are rightly left out of the sitemap. Every indexable
page had one h1, a unique title of at most 72 characters, a unique description of 120 to 160 characters and a
canonical address equal to its own .html address. The publishing gate passed with 106 checks and no failure, and
the photograph check passed.

Screenshots of twelve pages at 360, 768 and 1440 pixels, first screen and full page, 72 images in all, were taken
from the live site before any edit. They are the before images in the audit report.

## Lab performance, Lighthouse 12 mobile emulation, live site

| Page | Performance | Accessibility | Best practices | SEO | Largest contentful paint | Layout shift | Blocking time |
|---|---|---|---|---|---|---|---|
| Home | 99 | 96 | 100 | 100 | 2.0 s | 0 | 70 ms |
| Fees | 100 | 95 | 100 | 100 | 1.5 s | 0 | 60 ms |
| Wills and estates hub | 99 | 96 | 100 | 100 | 2.0 s | 0 | 30 ms |
| Probate service page | 99 | 96 | 100 | 100 | 1.9 s | 0 | 30 ms |
| Probate article | 99 | 96 | 100 | 100 | 2.0 s | 0 | 100 ms |
| Contact | 100 | 96 | 100 | 100 | 1.7 s | 0 | 10 ms |

These are lab figures from a simulated phone. No field data was available: the public Chrome user experience
service refused the request without a key, and a site of this size is unlikely to have enough visits to be
included.

## Accessibility, axe 4.10, live site

Twenty pages were scanned at 360 and 1440 pixels against the WCAG 2.0, 2.1 and 2.2 level A and AA rules. Every
page failed one rule and only one: the word Lawyers under the logo is 10 pixel text in #8f6e30 on #fbf9f5, a
contrast of 4.49 to 1 against the 4.5 the standard asks. Text that is part of a logo is exempt from that rule, so
this is a tool finding more than a failure, but it costs nothing to fix.

## Figures about the business

Counts about the business and not about the website are kept privately and are not in this repository.

## What could not be reached

The Search Console interface and its page and query tables, the Business Profile dashboard and any advertising
account. The site carries no analytics, as its privacy page says, so there are no visit, fee view or telephone tap
figures. The Wayback Machine holds no copy of the fees page. Enquiry messages, names and
form contents were deliberately not read.
