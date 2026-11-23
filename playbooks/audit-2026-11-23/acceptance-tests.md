# Acceptance tests, set on 23 November 2026 before any change to the site

These tests were written while the branch was still identical to main at commit 57dad24, the version live at
https://www.spenceralexander.com.au since Monday 23 November 2026 at 6:16am Melbourne time. Each row of the signoff
table at the end of the audit answers one of them. A test is passed only on evidence that can be shown again. It is
failed where the evidence goes against it, and it is unverified where the access, the signoff or the live
observations it needs are missing. No test is reworded afterwards to make it easier to pass.

## 1. Visual design

Does every page type look right at 360, 768 and 1440 pixels wide, and is it at least the equal of the local
competitors named in the audit?

The pages are the home page, the three hubs, the fees page, three service pages, an article and the contact page.
Each must show no clipped, overlapping or misaligned element and no sideways scroll. The first screen must say who
the firm is, what it does, where it is and how to reach it, and on the fees page it must show at least one price.
A reviewer who did not make the changes compares each page with the same page type on each competitor for
typography, hierarchy, spacing and clarity. The firm's palette, typefaces and components must be unchanged.

## 2. Mobile and desktop usability

Can each of three people finish their task from a search landing page without a dead end?

The executor finds the firm's probate fee and what the Supreme Court charges separately, and can add the two. The
separating parent finds a discreet way to make contact, can say whether a message may be left, and can leave the
page quickly. The business owner can tell whether the shareholders agreement fee covers their circumstances and what
happens if it does not. Every telephone and email link on the pages walked must be valid. The menus must work by
touch and by keyboard, and the form must validate, recover from an error and confirm.

## 3. Accessibility

Does the site meet WCAG 2.2 at level AA on the checks that were run?

The automated check is an axe scan of twenty pages at 360 and 1440 pixels, which must report no violation. The
manual checks cover the home page, a hub, the fees page, a service page and the contact page. Every control must be
reachable and operable by keyboard in a sensible order, with a visible focus ring that is never hidden, and the skip
link must work. Text must stay readable at 200 per cent zoom and at 320 pixels wide without sideways scroll. Touch
targets must be at least 24 by 24 pixels and text contrast at least 4.5 to 1. Motion must stop when reduced motion
is requested. Every form field must carry a label, with its hint and any error tied to it. The automated and manual
results are reported separately, with what each covered.

## 4. Accurate restoration and consistency of the historical fees

Does every restored fee show exactly the amount published before the release of 16 November 2026, and does every
rendition of every fee agree?

The reference is fees.html at commit 759a5e9, the last version of the fees page deployed before that release. A
restored fee must match it in amount, in its treatment of GST, in its fixed or from wording and in its scope,
inclusions and extras. Every rendition of every fee must agree with the one maintained source: the fee row, the
OfferCatalog, each hub, service page, article, checklist and FAQ answer, each meta description and JSON-LD string,
llms.txt and feed.xml. Three checks decide it. `python3 scripts/fees.py check` reports no problem. A search of every
public file finds no superseded amount beside the name of a restored fee. Each restored row equals the row at
759a5e9. A fee that is not restored must be unchanged from main, with the reason it was held recorded for Spencer.

## 5. Current fee competitiveness

Does each restored fee sit at or below 3.5 on the scale, on current evidence?

The scale is the one set on 16 November 2026, where the average published price less 10 per cent is 4, so 3.5 is
85 per cent of the average. The evidence is the survey of Victorian firms read on 16 November 2026, compared like
for like on GST, scope and court charges, and rechecked on 23 November 2026 for any material change in the market.
A fee above that level is reported as it stands and is not adjusted to pass.

## 6. Legal and factual accuracy

Is every statement of law and every factual claim on the high intent pages supported by a source?

The pages are the fees page, the three hubs, the twelve service pages, the home page, the contact page and the two
checklists. Every statement of law, time limit, threshold and court or government charge is checked against the
provision as read on 23 November 2026 in the authorised version. An error is corrected from the source, or left
marked for Spencer where the correction needs his judgement. Every claim about credentials, reviews, prices,
experience and availability is either supported by a source that can be named or listed for Spencer to confirm.
References to more than one lawyer are counted and set beside the fact that Spencer is the only lawyer. That wording
is left as it is for his decision, because his instruction of 9 November 2026 governs it.

## 7. Technical and local search

Is the site technically sound for search, fast on a phone, and consistent about who and where the firm is?

Every URL in the sitemap must return 200 with one h1, a title of at most about 70 characters, a description of 120
to 160 characters where the page is indexable, a canonical address that is its own .html address, JSON-LD that
parses and internal links that all resolve. The publishing gate's checks must all pass. A Lighthouse mobile lab run
must score at least 90 for performance on the home page, a hub, the fees page, a service page, an article and the
contact page, with a largest contentful paint under 2.5 seconds, layout shift under 0.1 and blocking time under 200
milliseconds. Field data is reported separately from lab data. The firm's name, address, telephone number and hours
must agree between the visible pages and the schema. Differences on Google Business Profile and directories are
listed for Spencer, because he keeps external accounts.

## 8. Readiness for AI answers

Has the site been tested on real answer engines, and can its key passages be quoted accurately on their own?

At least twelve unbranded questions across the three practices are put to every answer engine that can be reached.
The engine, the date, the pages cited and the accuracy of anything said about the firm are recorded. Search crawlers
and training crawlers must each be permitted as the firm's policy intends. The key passage on the fees page, the
probate page, the shareholder agreement page and the divorce page must be quotable alone with its jurisdiction,
scope, exceptions, author, date and source intact. A citation on the day is recorded as an observation and never as
proof that the firm will be recommended.

## 9. Client acquisition

Is every observable entry point traced to a fitting landing page with a clear next step, and is there a plan to
measure it?

The entry points are organic search, the Business Profile, referrers and returning clients, for each practice. The
referrer page must work. There must be a baseline with named sources and a plan to measure at 30, 60 and 90 days.
Whether acquisition improves can only be shown by the live figures, so that part stays unverified until they exist.

## 10. Enquiry conversion

Can a visitor on every high intent page see what they need to decide, and reach the firm from that point?

The visitor must be able to see the price where one is published, what the first call covers, who answers, how soon
a reply comes and when costs can rise, and must be able to call or write from the point where their question is
answered. The form must send one message for one successful enquiry and none for a failed one. The safe contact
answer must arrive unchanged at a test destination, and nothing may be sent to any analytics service. Whether more
visitors enquire can only be shown by the live figures, so that part stays unverified until they exist.
