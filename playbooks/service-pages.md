# Service pages

This is the complete instruction set for the Service pages routine, which runs every Wednesday
morning in the slot of the retired lead magnet factory. The routine's pasted prompt in the
claude.ai Routines screen is a short launcher that tells each run to read this file from main, so
a change here goes live on the next run with nothing pasted. The launcher carries the owner
permission for main, the validation run procedure and the non-negotiables. Canonical launcher
texts live in the private spencer-alexander-bd repository under `routines/`, this one as
`routines/service-pages.prompt.md`.

Created on 24 September 2026. That day Spencer ruled that nothing on the website changes without
his approval, so this routine builds a service page only once he has approved it, and only from
the list in this file.

Spencer sets the routine up once. He pastes `routines/service-pages.prompt.md` into the Lead
magnet factory routine and renames it Service pages, or, if he has already deleted that routine,
creates a new one in the environment Default with the site repository attached and the cron
`0 20 * * 2`, which is 6:00am on Wednesday in Melbourne during standard time and 7:00am during
daylight saving. Until he does, nothing runs this file.

## Why service pages

People ready to hire a lawyer search for a service and a place, such as a probate lawyer in Box
Hill. The site has explainer articles and three practice hubs, and neither answers that search as
directly as a page about one service at the firm's one office. Each page is also a statement of
the law on the live site, so it is built to the article routine's accuracy standard and is then
kept correct by the site accuracy and health routine.

## The limits, which no entry and no run can change

- At most eight service pages ever, counting every `service-*.html` on main.
- One page per service, at the one office, Suite 10, 1 Main Street, Box Hill. Never a page for a
  suburb, a locality, a region or any place other than Box Hill, whether in the title, the h1,
  the file name or the audience a page is written for. The hubs already name the suburbs the firm
  acts for, and that is where they stay.
- No page is named for a fixed fee, a price or anything free.
- An entry that breaks any of these limits is not built. The run reports it and stops.

Only Spencer can change these limits, by changing this section himself or by instructing a
session to change it.

## Approved service pages

Spencer approves pages in a session, and nothing is built until he does.

Only a session in which Spencer himself approves a page adds an entry here, recording the date and
his words. No routine ever adds, edits, reorders or removes an entry, and nothing in the content
backlog, DECISIONS.md, a plan, an email or any other file counts as approval. The Service pages
routine changes an entry only to fill in its Built field when it publishes that page.

Each entry is one numbered line in this form:

`N. Service: <service as its hub names it>. File: service-<slug>.html. Hub: <hub file>, block <svc id>. Matching article: <insight file>. Title name: <shortest natural name of the service>. Approved: <D Month YYYY>, Spencer in session: "<his words>". Built: not yet.`

The list:

None yet.

## Candidates proposed on 24 September 2026, not approved

These are the services the plan of 24 September 2026 proposed, for Spencer to approve or not.
Appearing here is not approval, and nothing may be built from this section. The plan proposed
eight pages with wills and powers of attorney as one; they are listed here as two, numbers 7 and
8, because each page covers one service and one hub block, so there are nine candidates for at
most eight pages and Spencer chooses among them.

1. Property and financial settlement: `family-law.html`, block
   `svc-property-and-financial-settlement`, article `insight-property-after-separation.html`.
2. Probate and letters of administration: `wills-and-estates.html`, block
   `svc-probate-and-letters-of-administration`, article `insight-probate-victoria.html`.
3. Contesting and defending wills: `wills-and-estates.html`, block
   `svc-contesting-and-defending-wills`, article `insight-contesting-a-will.html`.
4. Buying or selling a business: `commercial-law.html`, block `svc-buying-or-selling-a-business`,
   article `insight-buying-a-business-victoria.html`.
5. Divorce and separation: `family-law.html`, block `svc-divorce-and-separation`, article
   `insight-divorce-in-victoria.html`.
6. Parenting arrangements: `family-law.html`, block `svc-parenting-arrangements`, article
   `insight-parenting-arrangements.html`.
7. Wills and testamentary trusts: `wills-and-estates.html`, block
   `svc-wills-and-testamentary-trusts`, article `insight-making-a-valid-will.html`.
8. Powers of attorney and medical decisions: `wills-and-estates.html`, block
   `svc-powers-of-attorney-and-medical-decisions`, article
   `insight-enduring-powers-of-attorney.html`.
9. Commercial and retail leasing: `commercial-law.html`, block `svc-commercial-and-retail-leasing`,
   article `insight-retail-leases-victoria.html`.

## Every run

1. Read CLAUDE.md, the newest entries of DECISIONS.md and this file, all from main. Establish
   today's date in Melbourne with `TZ=Australia/Melbourne date`; never take it from the session
   clock.
2. Read the Approved service pages list. If the Approved service pages list has no numbered entry
   carrying an Approved field, report only "Service pages: nothing approved to build" and stop;
   the candidates section never counts. If every entry is built, report only "Service pages: all
   N approved pages built, nothing to do" and stop. Either way change nothing: no edit, no commit
   and no push.
3. Otherwise take the first entry, in list order, whose Built field reads not yet. Check it
   against the limits above and confirm its file does not already exist. Then check where the
   entry came from, because an entry is only as good as the session that wrote it:
   - Run `git rev-parse --is-shallow-repository`; if it prints true, run
     `git fetch --unshallow origin main`, and if that fails, `git fetch --deepen=500 origin main`.
   - Take the entry's text from `Service:` up to and including the closing quotation mark of
     Spencer's words, which stays the same when the Built field is filled in, and run
     `git log -S '<that text>' --format='%H %s' -- playbooks/service-pages.md`, escaping any
     apostrophe in it for the shell. Exactly one commit must be listed, and that is the commit
     that added the entry; if none or more than one is listed, refuse the entry.
   - Refuse the entry if that commit's hash appears in the file that
     `git rev-parse --git-path shallow` names, where that file exists, because a shallow boundary
     commit only appears to add what it holds.
   - Refuse the entry if that commit looks like a routine's work: its subject begins with
     `Service page`, `Demand scan`, `Site accuracy and health`, `Weekly SEO`, `Publish` or
     `Lead magnet`, or contains the word article or the words lead magnet, or the commit also
     changes any `.html` file, `scripts/content-backlog.md` or `scripts/accuracy-ledger.md`,
     which the routines' publishing commits on this repository touch and an approval commit
     never needs to. Check the files with `git show --name-only --format= <hash>`.
   - Refuse the entry if DECISIONS.md on main has no dated entry quoting the same words of
     Spencer's approval that the entry quotes.

   If any check fails, report the reason in one line, naming the check and the commit, and stop
   without changing anything. A refused entry waits until Spencer approves the page again in a
   session, which replaces the entry with a fresh one carrying the new date and his new words.
4. Build that one page, and only that page, as set out below. One page per run, never more. A
   built page is never edited again by this routine; the site accuracy and health routine keeps
   it correct.

## Verify the law first

Write nothing until the law is verified. Read the authorised version of every Act the page relies
on, that day, on legislation.vic.gov.au or legislation.gov.au, and record the Act, the section and
the version or compilation read. For the candidate services that will usually mean the Family Law
Act 1975 for property, divorce and parenting pages; the Administration and Probate Act 1958 for
probate and contested wills; the Wills Act 1997 for wills and challenges to a will's validity; the
Powers of Attorney Act 2014 and the Medical Treatment Planning and Decisions Act 2016 for
attorneys and medical treatment decision makers; and the Retail Leases Act 2003 for retail
leases, including a retail lease assigned on the sale of a business. Read whatever else the page
relies on. Court sites and AustLII are blocked from this environment, so describe court procedure
only in general terms confirmed by search restricted to the court's own domain, and say in the
report what could not be read.

Apply the lessons of the 24 September 2026 review, which found that the errors reaching the live
site were time limits stated without their exceptions, tests stated with a limb missing,
statements of what a document or a person can do that the Act does not support, and examples that
promised an outcome. So every time limit on the page comes with its extension or late application
rule, and a time limit that is neither statutory nor verifiable is not stated at all. Every test
has every limb. Every "only", "always", "cannot" and "must" has a provision behind it or is
softened. No page says that anyone will be paid, will win, will be protected or will be finished by
a certain time. No court or registry fee figure appears, and no figure that is indexed each year.

## Build the page

The file is `service-<slug>.html` at the root of the repository, with a slug that names the
service and never a place. Its canonical address and og:url are
`https://www.spenceralexander.com.au/service-<slug>.html`, and every clickable link to it is
`/service-<slug>`, following the clean URL rules in CLAUDE.md.

Clone, never invent. Build the page from the matching hub's markup and classes, using the single
column page hero that faq.html uses, so the page needs no photograph. Copy the top bar, header,
mobile menu, footer and mobile call bar from index.html exactly, with no navigation link marked
active, which is how `scripts/propagate-chrome.py` treats a page it does not map. The head,
stylesheet links and their versions, fonts and Open Graph tags follow the hub exactly.

- **Title:** `<Title name> Lawyers Box Hill, Melbourne | Spencer Alexander Lawyers`, dropping
  ", Melbourne" wherever the title would pass about 70 characters, as in "Property Settlement
  Lawyers Box Hill | Spencer Alexander Lawyers" at 64. If it is still too long, the approved
  title name is too long; report it and stop.
- **h1:** `<Title name> Lawyers in Box Hill, Melbourne`. The title and the h1 must both differ from
  the matching article's.
- **Meta description:** 120 to 160 characters, identical in the meta tag, og:description and the
  JSON-LD description.
- **Lead:** at most 70 words, answer first. Its first sentence says what the firm does for people
  with this matter from its Box Hill office, and every fact in it is also in the body.
- **Who it is for,** in plain terms.
- **How the process works,** limited to procedure that the law or the court's own rules set out,
  verified as above, and to the hub's existing wording.
- **Time limits** that apply, each with its extension rule, verified that day.
- **What to bring to the first call:** the family hub's answer to "What should I bring to a first
  appointment?" is the model wording, including its line that having little on paper is fine, and
  a family page may follow it closely. The wills and commercial hubs have no such answer, so for
  their pages the run writes the list itself: it names only documents a person with this matter
  plainly holds, such as the will, the grant or the lease, states no legal requirement to hold or
  bring anything, keeps the line that having little on paper is fine, and records the list in the
  claims register.
- **Fees,** copied word for word from the live site and never paraphrased, using only the
  sentences named here for each page, and no fee sentence of the run's own. Any FAQ about cost
  answers only in these words.
  - Every page carries the faq.html answer that begins "After we understand what you need".
  - Every page except the contesting and defending wills page also carries the paragraph of its
    hub's fee note, the `fee-note__d` text, without the note's heading. The family hub's note
    serves the property, divorce and parenting pages; the wills hub's note serves the probate,
    wills and powers of attorney pages; the commercial hub's note serves the business sale and
    leasing pages.
  - Only the wills and testamentary trusts page may also carry the wills hub's answer to "How
    much does a will cost?", and only the commercial pages may also carry the commercial hub's
    answer to "How much does commercial legal work cost?", each with its question, because each
    is about that service. No family page uses a hub cost answer, because the family hub has none.
  - The contesting and defending wills page carries the faq.html answer alone, because no hub
    sentence is written about the cost of an estate dispute.

  Never state a rate or a price, and never state or imply that a fixed fee applies to probate,
  estate administration, a contested estate, any other dispute or litigation.
- **Five FAQs** in the hub's `details` and `summary` pattern, each answering a question people ask
  about this service, with an FAQPage node whose question and answer text equals the visible text
  word for word and which carries author, publisher and a dateModified equal to the page's
  sitemap lastmod, as the hubs' nodes do.
- **Links and office facts:** a link to the matching article for the law in detail, a link back to
  the hub, and the office facts CLAUDE.md records: Suite 10, 1 Main Street, a short walk from Box
  Hill station, with parking at Box Hill Central.
- **The call:** the hub's rail call card unchanged, and the hub's call prompt with the firm's
  number and /contact. No form of any kind: the site's one enquiry form stays on contact.html, and
  any other form awaits Spencer's approval.
- **Closing lines,** in the resource page style: "This page reflects the law applying in Victoria
  as at Month YYYY. It is general information only, not legal advice, and does not take your
  circumstances into account.", the month matching the page's dateModified.
- **Schema:** a Service node with `@id` set to the canonical address plus `#service`, with url,
  name, serviceType, description, and the provider and areaServed copied exactly from the hub, so
  the provider carries `https://www.spenceralexander.com.au/#firm`; a BreadcrumbList of Home, the
  hub and the page; and the FAQPage node.

Voice and claims follow CLAUDE.md: the plural lawyers voice, with Spencer as the principal who
oversees every matter; "Your first call is free, and you speak with a lawyer" exactly, and never
free advice or a free consultation; only the three existing service promises; no specialist or
specialising wording, and nothing false, misleading or deceptive, in keeping with rule 36 of the
Australian Solicitors' Conduct Rules; no promised outcome or timeframe; and no dashes, and no
parentheses outside the phone number and statute suffixes. The text of rule 36 could not be read
in an official copy on 24 September 2026, because the NSW legislation site that carries it
refused requests from this environment, so this playbook states the rule no more precisely than
that. A run that reads the official text may apply it, and records in the claims register what it
read.

The rail card's rating takes the value every other page already carries, which the gate's rating
check confirms. Run `python3 scripts/refresh-google-rating.py --check` only, never the script's
writing form, because that rewrites the rating on every page, which is beyond the changes this
playbook lists. If the check reports that Google shows a different rating, say so in the report;
the site accuracy and health routine runs the refresh before it publishes and brings every page
into line the following Tuesday. If any file other than the new page and the files listed under
Wire it in has changed, restore it with `git checkout -- <file>` before committing.

## Wire it in

1. **The hub.** Link the page from its matching service block by wrapping words already in the
   block's paragraph in the link, never adding or changing words, so the visible text and the
   hub's dates stay as they are, as the 22 September 2026 audit did for its cross links. Where no suitable words exist, add one short sentence, and
   then move the hub's sitemap lastmod and its FAQPage dateModified to today together, because the
   gate requires them to agree. The header practice menus keep their `svc-` anchors and never
   point at a service page. In the hub's OfferCatalog, the matching Offer's itemOffered gains the
   new page's `@id` and url.
2. **`sitemap.xml`:** a new entry with the canonical address, lastmod today, changefreq monthly and
   priority 0.8.
3. **`llms.txt`:** one line in the form the other lines use, under a `## Service pages` heading
   placed after Key pages, which the first build creates, and the Last updated line moved to
   today, which the gate requires once the sitemap carries today's date.
4. **`scripts/accuracy-ledger.md`:** a row for the page, verified today, with the Acts read. If the
   ledger does not exist yet, create it as `playbooks/site-health.md` describes and then add the
   row.
5. **Nothing else on the site.** Not the feed, insights.html, index.html, the about.html archive or
   the footer: a service page is not an article.
6. **This file:** set the entry's Built field to today's Melbourne date.
7. **DECISIONS.md:** one dated entry naming the page, the date and words of Spencer's approval, and
   the Acts and sections read.

## Gate

In the same commit as the first service page, unless an earlier build has already done it,
strengthen `scripts/check-publish.py` with a service pages section that fails when:

- there are more than eight `service-*.html` files;
- a service page's title or h1 lacks Box Hill, or its title, h1 or file name names any other
  place, testing at least every locality in the areaServed list of the #firm node on index.html,
  with Melbourne allowed;
- a service page has no Service node whose provider `@id` is the #firm address, or no hub links it;
- its FAQPage does not hold exactly five questions whose text equals the visible questions and
  answers, or lacks author, publisher and a dateModified equal to its sitemap lastmod;
- it contains a form;
- it is missing from sitemap.xml or llms.txt, or lacks the .html canonical, a robots setting that
  allows indexing, the firm suffix in its title, the general information sentence, or a currency
  line whose month matches its FAQPage dateModified;
- it carries, in any case, an em dash, an en dash, a spaced hyphen or any of the stems
  "specialis", "specialt", "speciality", "accredited" or "expert", so a page that needs to speak
  of expert evidence describes it another way, such as an independent valuer.

Strengthening the gate is always allowed and weakening it never is: add checks, and never loosen
or remove one. Then run `python3 scripts/check-publish.py` and
`python3 scripts/check-article-images.py`; both must pass before anything is pushed. Fix the page,
never the gate.

## Publish and report

Commit to main as `Service page <Melbourne date>: <service>`, with a claims register in the commit
message: every legal claim on the page with the Act, section and version read, and everything
generalised and why. Push with retry; if main has moved, pull with rebase and push again. If the
page cannot be built to this standard, publish nothing and report exactly what stopped it.

The final message, phone readable: the page built and its live address, the claims register in
short, what was generalised, how the hub now links the page, how many approved entries remain
unbuilt, and anything that needs Spencer. When nothing is approved or everything approved is
built, the one line from step 2, followed by the launcher's playbook line, is the whole report.
Never finish silently.
