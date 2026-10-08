# Content backlog: demand scanner

Maintained by the Friday demand scanner routine. Read by the Monday article
routine. Items are ranked by enquiry intent score first and by strength of
observed demand second, because a searcher who holds a document, faces a date
or is choosing a lawyer is the one most likely to call this week. Everything
here rests on evidence recorded in the row; nothing in this file is invented,
and nothing in this file is approval to build anything. Items covered by the
site, older than 60 days, or out of scope are removed on each scan.

Enquiry intent is scored 0 to 3, one point each for: the searcher holds a
document, the searcher faces a date, the searcher is choosing a lawyer.

## Scan of 2026-10-09

Rotation note for the Monday article routine, derived mechanically (the area
whose most recent article is oldest is due). Newest article per area:
Commercial Law 2026-10-05 (business partner disputes), Family Law 2026-09-28
(agreed property settlement), Wills and Estates 2026-09-21 (misuse of a power
of attorney). Wills and Estates is therefore due Monday 12 October 2026.

Hire marker: the most recent article, insight-business-partner-disputes-victoria.html published 2026-10-05, was not a hire guide.

The derivation was conclusive. The repository was shallow, so it was
unshallowed first with `git fetch --unshallow origin main`; `git log
--diff-filter=A` listed exactly one adding commit, f91d879; no shallow
boundary file remained, and `git show --name-status` printed A against the
file. That commit's message carries the line `Article type: ordinary` and no
line reading `Article type: hire guide`. Monday 12 October is therefore due a
HIRE GUIDE, in Wills and Estates. Item 16 below, will kit or lawyer, is the
recommendation, with item 15 as the alternative.

| # | Topic (searcher's words) | Demand evidence (source, one line) | Intent | Enquiry intent | Practice area | Suggested angle | Added |
|---|---|---|---|---|---|---|---|
| 1 | police named me as the respondent but I am the one being abused | Carried from 25 Sep: Victoria Legal Aid, the Women's Legal Service and the Federation of Community Legal Centres all published on misidentification through 2026, and the Federation's 16 Sep 2026 response to the reforms keeps it live | article | 3: document, date, choosing a lawyer | Family Law | The respondent's side of an intervention order where the wrong person has been named: why it happens, what the reforms require police and courts to weigh once commenced, which faq.html says is on a day to be proclaimed and no later than 10 November 2026, why the order must still be obeyed while it stands, and how an order is contested, varied or revoked. FAQ live since 25 Sep. Write it after commencement is confirmed in the authorised version, which may fall in the next Family Law slot | 2026-09-25 |
| 2 | my ex will not sign the transfer or comply with our property orders | New on 2 Oct: the Federal Circuit and Family Court's practice direction starting a National Enforcement List for financial and property orders from 21 September 2026, reported by the Queensland Law Society's Proctor in August 2026, plus a steady run of firm guides on an ex who stalls after orders (Coutts, Marino, Gloria, Cudmore) | article | 2: document, choosing a lawyer | Family Law | What happens when final property orders are made and ignored: enforcement applications, the court's power under section 106A of the Family Law Act to appoint someone to sign a document in the refusing party's name, the new National Enforcement List, and costs. FAQ added 2 Oct, read against the Family Law Act compilation 101, sections 105, 106A and 107. Distinct from /insight-agreed-property-settlement and /insight-property-after-separation, which stop at the making of orders. Do not state any filing fee, and read the practice direction itself at writing time if the court's site is reachable | 2026-10-02 |
| 3 | do I need a lawyer for a shareholder dispute, and what will it cost | New on 2 Oct: Melbourne and national dispute pages (PCL, MST, Gibbs Wright, A and I Lawyers, Sajen Legal) all frame the engagement question, with early advice before positions harden the common answer | hire | 2: document, choosing a lawyer | Commercial Law | The hire guide counterpart to /insight-business-partner-disputes-victoria, for a later Commercial Law hire slot: what a lawyer does first in a co-owner dispute, why the documents and the company records are read before anything else, what drives cost, which is mostly whether the matter settles or is litigated, and how early advice keeps a negotiated exit open. Keep to a written fee estimate before substantive work; state no rate and none of the litigation cost ranges other firms publish. Not in the very next Commercial Law slot | 2026-10-02 |
| 4 | the executor will not distribute and will not tell us anything | Carried from 25 Sep: the standing Whirlpool estate threads are the clearest recurring beneficiary side pattern in Australian consumer forums | article | 2: document, date | Wills & Estates | The beneficiary's side, which the site answers only as a short FAQ: what a beneficiary is and is not entitled to see, the expectation that an estate is administered within about a year and what that does and does not mean, how to ask for accounts, and what the court can do where an executor will not act. Distinct from /insight-executor-duties, which is written for the executor. Verify every remedy carefully, and generalise any timing | 2026-09-25 |
| 5 | can I use mum's power of attorney to move her into aged care, and what if she never signed one | New this scan: the editor of Australian Ageing Agenda accepted on 5 Oct 2026 the PR routine's pitch on enduring powers of attorney at the point of aged care admission, asking for 600 to 800 words; 2026 adviser explainers on attorneys and aged care admission | article | 2: document, date | Wills & Estates | What an attorney for personal and financial matters can and cannot do at an aged care move, and what the family faces where no power was signed, being an application to VCAT for a guardianship or administration order. FAQ added this scan, read against the Powers of Attorney Act 2014 version 007, sections 3, 21, 22 and 23, and the Guardianship and Administration Act 2019 version 010, sections 30 and 31. PARTIAL OVERLAP: /insight-enduring-powers-of-attorney and /insight-guardianship-administration-orders, so the article must stay on the admission moment. State nothing about Commonwealth aged care agreements or fees unless read in the authorised version | 2026-10-09 |
| 6 | what happens at a first meeting with a family lawyer and what do I bring | Carried from 25 Sep: 2026 first consultation guides answering what to bring, how long it takes and whether there is any obligation | hire | 2: document, choosing a lawyer | Family Law | What actually happens in a first family law conversation, what is worth bringing, that a support person is welcome, that it is confidential whether or not you engage, and what you should expect to walk away knowing. PARTIAL OVERLAP: faq.html and family-law.html answer what to bring, and service-property-settlement.html has a what to bring section, so the article must go well beyond the document list | 2026-09-25 |
| 7 | do we need a lawyer for parenting consent orders if we already agree | New on 2 Oct: 2026 consent order cost and process guides (Fogarty Oliver and Rothschild, Justice Family Lawyers, MJ Legal, Unified) all leading with whether an agreed parenting arrangement needs a lawyer | hire | 2: date, choosing a lawyer | Family Law | The parenting counterpart to the agreed property settlement hire guide: the difference between a parenting plan and parenting orders, what the court must be satisfied of before it makes consent orders, and what a lawyer checks so the orders work in practice. Keep to the fixed fees fees.html carries; state no court filing fee. PARTIAL OVERLAP: /insight-parenting-arrangements and service-parenting-arrangements.html, so stay on the engagement question | 2026-10-02 |
| 8 | commercial and industrial property tax, what will I pay if I buy commercial premises | Carried from 25 Sep: the State Revenue Office's own pages plus 2026 explainers, and LIV LawNews of 17 Sep led with property tax risks | article | 2: document, date | Commercial Law | What a buyer of commercial or industrial premises in Victoria needs to understand about the move from stamp duty to an annual property tax. HIGH ACCURACY RISK: tax, adjacent to the firm's work, and every rate, threshold and transition period changes. Verify each figure against the State Revenue Office at writing time or write without figures, and say plainly that tax advice comes from the client's accountant | 2026-09-25 |
| 9 | why is probate taking so long in Victoria | Carried from 4 Sep and still evidenced: 2026 Victorian guides continue to describe requisitions and lodgement backlogs | faq done, article later | 2: document, date | Wills & Estates | FAQs live since 11 Sep. A short update to /insight-probate-victoria only if published timeframes clearly worsen; the article as written remains accurate | 2026-09-04 |
| 10 | is coercive control a crime in Victoria now | Carried from 18 Sep and re-evidenced: the Justice Legislation Amendment (Family Violence, Stalking and Other Matters) Act 2026 reforms were reported again this fortnight, and faq.html records assent on 22 Sep 2026 with the offence starting on a day to be proclaimed and no later than 1 March 2028 | article | 1: date | Family Law | The strongest ordinary Family Law candidate after item 2, in the shape of an update: what the new offence covers, that it is not yet in force, and what protects people now. Verify the offence and its commencement in the authorised version; reported penalty figures vary, so generalise | 2026-08-28 |
| 11 | can I still charge a card surcharge from 1 October | New on 2 Oct: the Reserve Bank's conclusions on merchant card payment costs and surcharging, with eftpos, Mastercard and Visa introducing no surcharge rules from 1 October 2026 and American Express, UnionPay and PayPal following, and a wave of small business explainers (ANZ, CommBank, Small Business Connections) | article | 1: date | Commercial Law | What the end of card surcharging means for a small business's pricing and its customer terms: that the change comes through the card networks' rules after the Reserve Bank's review, that it covers surcharges for paying by card and not weekend, public holiday, booking or service fees, and that the price shown must be the price paid under the Australian Consumer Law. ACCURACY CAUTION: this is payments regulation adjacent to the firm's work; read the Reserve Bank's own pages at writing time and avoid any penalty figure | 2026-10-02 |
| 12 | do employers have to pay super every payday now | Carried from 4 Sep: the 1 July 2026 commencement continues to drive employer explainers | article | 1: date | Commercial Law | What payday super means for a small employer in practice, framed as a compliance update. FAQ live since 4 Sep; verify current specifics in the authorised legislation at writing time | 2026-09-04 |
| 13 | can I use a template for my terms and conditions or do I need a lawyer | New on 2 Oct: 2026 guides from Sprintlaw, LegalVision, Progressive Legal, Legal123 and Somerville all answering template against lawyer for business terms | hire | 1: choosing a lawyer | Commercial Law | When a template is a reasonable start and when it is not: terms that must fit how the business actually trades, payment and retention of title terms, limitation of liability, and the unfair contract terms regime for standard form contracts with consumers and small businesses. Factual and even handed about templates. fees.html carries a terms of trade price, so quote only that figure if any. PARTIAL OVERLAP: /insight-contracts-for-business and the unfair terms FAQ, so stay on the engagement question | 2026-10-02 |
| 14 | can they put that term in the contract, it seems unfair | Carried from 22 Aug: ACCC enforcement priorities keep unfair contract terms named | article | 1: document | Commercial Law | FAQ live since 11 Sep. Fuller article on the unfair terms regime for small business standard form contracts, penalty figures generalised. Falls out of the 60 day window on 21 Oct unless re-evidenced | 2026-08-22 |
| 15 | should I use the public trustee or a lawyer for my will | Re-evidenced this scan: State Trustees' 2026 executor services brochure and its pages on choosing it as executor, and a live Choice community thread on trustee company fees | hire | 1: choosing a lawyer | Wills & Estates | The choices for drafting a will and appointing an executor, fee models generalised, even handed and with no disparagement of anyone. FAQ live since 11 Sep. The alternative W&E hire guide for Monday 12 Oct | 2026-10-09 |
| 16 | is a will kit valid, or do I need a lawyer | Carried from 25 Sep and re-evidenced this scan: Choice's will kit reviews and Victoria Legal Aid's will guide both frame kit against lawyer | hire | 1: choosing a lawyer | Wills & Estates | RECOMMENDED FOR MONDAY 12 OCT as the Wills and Estates hire guide. Factual about what makes a will valid in Victoria and where kit wills actually fail. Never disparage kits as such. PARTIAL OVERLAP: wills-and-estates.html and /insight-making-a-valid-will carry short answers, so the article must be substantially more | 2026-09-25 |
| 17 | are the intervention order laws changing in Victoria | Carried from 25 Sep: the 2026 Act and its staged rollout | faq done | 1: date | Family Law | Covered by the FAQ of 25 Sep. Revisit as an article only once commencement can be stated from the authorised version | 2026-09-25 |

### Page candidates (ideas only, never approval)

None. The site carries eight service pages, the limit the playbook sets, so no
page item may be proposed.

### Resource candidates (ideas only; nothing builds these automatically)

The lead magnet factory was retired on 24 September 2026 and the two published
resources stay. These remain evidenced ideas and nothing more.

1. Small business contract health check checklist (carried from 22 Aug).
2. Director insolvency early warning checklist (carried from 28 Aug).
3. New employer payroll compliance checklist (carried from 4 Sep). Verify every
   listed obligation at build time.
4. Family violence and property settlement records checklist (carried from
   18 Sep): build only if it can be done responsibly.

### Removed this scan

- "my business partner and I own the company 50/50 and cannot agree": covered
  by insight-business-partner-disputes-victoria.html, published 5 October 2026.
  Item 3, its hire counterpart, stays but should not run in the next
  Commercial Law slot straight after it.

Nothing was dropped for age. Item 14 leaves the 60 day window on 21 October
2026 unless re-evidenced; item 15 was re-evidenced this scan and redated.

### Hire items per practice area

Family Law 2 (items 6 and 7), Wills and Estates 2 (items 15 and 16),
Commercial Law 2 (items 3 and 13). Every area meets the quota with evidence.

### Scan notes, 2026-10-09

Melbourne date established with `TZ=Australia/Melbourne date` before any other
step: Friday 9 October 2026, while the session clock still read 8 October UTC.

Research run directly with ordinary searches in the main session, no
subagents, about eight searches and a Gmail search. Nothing was cut for
budget. A search for Victorian estates news of the fortnight found nothing
new. The intervention order misidentification reforms are still reported as
starting in November 2026, so item 1 waits for commencement to be confirmed
in the authorised version.

Fleet signal: on 5 October 2026 the editor of Australian Ageing Agenda replied
to the PR routine's follow up and accepted the pitch on enduring powers of
attorney at aged care admission, at 600 to 800 words. That is the week's one
journalist signal and it is demand evidence for item 5. The Money and Life
and Tax Institute follow ups of 1 October have no reply yet.

The FAQ added this scan was read in the authorised versions downloaded from
legislation.vic.gov.au: Powers of Attorney Act 2014 version 007, sections 3,
21, 22 and 23; Guardianship and Administration Act 2019 version 010,
sections 30 and 31.

Client correspondence was not used as demand evidence. Reddit remains
unsearchable by the search tool.
