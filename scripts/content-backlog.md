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

## Scan of 2026-11-06

Rotation note for the Monday article routine, derived mechanically: the area
whose most recent article is oldest is due. Newest article per area: Wills and
Estates 2026-11-02, an executor who will not distribute the estate; Commercial
Law 2026-10-26, terms and conditions, template or lawyer; Family Law
2026-10-19, enforcing property orders. Family Law is therefore due Monday
9 November 2026.

Hire marker: the most recent article, insight-executor-not-distributing-estate.html published 2026-11-02, was not a hire guide.

The derivation was conclusive. The repository was shallow, so it was
unshallowed first with `git fetch --unshallow origin main`; `git log
--diff-filter=A` listed exactly one adding commit, 9ad2440; no shallow
boundary file remained, and `git show --name-status` printed A against the
file. That commit's message carries the line `Article type: ordinary`.
Monday 9 November is therefore due a HIRE GUIDE, in Family Law. Item 2 below,
whether an agreed parenting arrangement needs a lawyer for consent orders, is
the recommendation, re-evidenced this week. Item 3, the first meeting with a
family lawyer, is the fallback. Item 1, misidentification, stays the strongest
ordinary Family Law topic, but its reforms commence no later than 10 November
2026, the day after Monday, so it belongs in the next ordinary Family Law
slot, written once commencement is confirmed in the authorised version.

| # | Topic, in the searcher's words | Demand evidence, source in one line | Intent | Enquiry intent | Practice area | Suggested angle | Added |
|---|---|---|---|---|---|---|---|
| 1 | Re-checked 6 Nov: eastern suburbs Star Mail and Mornington Peninsula News still report the misidentification changes as due by November, and Victoria Legal Aid's explainer still gives no commencement date; first evidenced 25 Sep from Victoria Legal Aid, the Women's Legal Service and the Federation of Community Legal Centres | Carried from 25 Sep: Victoria Legal Aid, the Women's Legal Service and the Federation of Community Legal Centres all published on misidentification through 2026, and the Federation's 16 Sep 2026 response to the reforms keeps it live | article | 3: document, date, choosing a lawyer | Family Law | The respondent's side of an intervention order where the wrong person has been named: why it happens, what the reforms require police and courts to weigh once commenced, which faq.html says is on a day to be proclaimed and no later than 10 November 2026, and local reporting still says by November, why the order must still be obeyed while it stands, and how an order is contested, varied or revoked. FAQ live since 25 Sep. Write it after commencement is confirmed in the authorised version, which may fall in the next Family Law slot | 2026-09-25 |
| 2 | Re-evidenced 6 Nov: Unified Lawyers and Melbourne Family Lawyers consent order pages and the Legal Aid Queensland consent orders guide all answer whether an agreed arrangement needs a lawyer, advising independent advice and careful drafting so the orders can be enforced; first evidenced 2 Oct from Fogarty Oliver and Rothschild, Justice Family Lawyers, MJ Legal and Unified | New on 2 Oct: 2026 consent order cost and process guides from Fogarty Oliver and Rothschild, Justice Family Lawyers, MJ Legal and Unified all leading with whether an agreed parenting arrangement needs a lawyer | hire | 2: date, choosing a lawyer | Family Law | RECOMMENDED for Monday 9 November, the Family Law hire guide. The parenting counterpart to the agreed property settlement hire guide: the difference between a parenting plan and parenting orders, what the court must be satisfied of before it makes consent orders, and what a lawyer checks so the orders work in practice. Keep to the fixed fees fees.html carries; state no court filing fee. PARTIAL OVERLAP: /insight-parenting-arrangements and service-parenting-arrangements.html, so stay on the engagement question | 2026-11-06 |
| 3 | Re-evidenced 6 Nov: Unified Lawyers and Meillon and Bright first appointment guides, both on what to bring and that there is no obligation to engage; first evidenced 25 Sep from 2026 first consultation guides | Carried from 25 Sep: 2026 first consultation guides answering what to bring, how long it takes and whether there is any obligation | hire | 2: document, choosing a lawyer | Family Law | FALLBACK for Monday 9 November. What actually happens in a first family law conversation, what is worth bringing, that a support person is welcome, that it is confidential whether or not you engage, and what you should expect to walk away knowing. PARTIAL OVERLAP: faq.html and family-law.html answer what to bring, and service-property-settlement.html has a what to bring section, so the article must go well beyond the document list | 2026-11-06 |
| 4 | do I need a lawyer for a shareholder dispute, and what will it cost | New on 2 Oct: Melbourne and national dispute pages, namely PCL, MST, Gibbs Wright, A and I Lawyers and Sajen Legal, all frame the engagement question, with early advice before positions harden the common answer | hire | 2: document, choosing a lawyer | Commercial Law | The hire guide counterpart to /insight-business-partner-disputes-victoria, for a later Commercial Law hire slot: what a lawyer does first in a co-owner dispute, why the documents and the company records are read before anything else, what drives cost, which is mostly whether the matter settles or is litigated, and how early advice keeps a negotiated exit open. Keep to a written fee estimate before substantive work; state no rate and none of the litigation cost ranges other firms publish. Not in the very next Commercial Law slot | 2026-10-02 |
| 5 | can I use mum's power of attorney to move her into aged care, and what if she never signed one | New on 9 Oct: the editor of Australian Ageing Agenda accepted on 5 Oct 2026 the PR routine's pitch on enduring powers of attorney at the point of aged care admission, asking for 600 to 800 words; 2026 adviser explainers on attorneys and aged care admission | article | 2: document, date | Wills & Estates | What an attorney for personal and financial matters can and cannot do at an aged care move, and what the family faces where no power was signed, being an application to VCAT for a guardianship or administration order. FAQ added 9 Oct, read against the Powers of Attorney Act 2014 version 007, sections 3, 21, 22 and 23, and the Guardianship and Administration Act 2019 version 010, sections 30 and 31. PARTIAL OVERLAP: /insight-enduring-powers-of-attorney and /insight-guardianship-administration-orders, so the article must stay on the admission moment. State nothing about Commonwealth aged care agreements or fees unless read in the authorised version | 2026-10-09 |
| 6 | what will it cost to contest a will, and who pays the legal costs | New on 16 Oct: Victorian will dispute cost and no win no fee pages from Armstrong Legal and Maurice Blackburn all lead with cost and who bears it, the engagement question for a person considering a claim | hire | 2: date, choosing a lawyer | Wills & Estates | The hire guide counterpart to /insight-contesting-a-will, which has no costs section: what drives the cost of a claim, mostly whether it settles at mediation or runs to trial, that the court decides who bears costs and that they are not always paid from the estate, what a lawyer assesses first, and the six month limit that makes an early call matter. State no cost range and no promise about costs orders; read the Administration and Probate Act and the court rules on costs at writing time and generalise anything uncertain. Keep to a written fee estimate before substantive work | 2026-10-16 |
| 7 | do I need a lawyer to apply for probate, or can I do it myself | New on 16 Oct: the Supreme Court Probate Office says applicants may apply without a lawyer, its fee list effective 1 July 2026 is current, and 2026 Victorian firm guides answer the same do it yourself question | hire | 2: document, choosing a lawyer | Wills & Estates | When an executor can reasonably apply alone and when a lawyer earns the fee: the online application, the advertisement and the affidavits, the inventory, requisitions from the Probate Office, and the personal liability an executor carries for the administration that follows. Quote only the probate application price fees.html carries and no court fee figure. PARTIAL OVERLAP: service-probate.html already says an executor can apply without a lawyer and /insight-probate-victoria has a cost section, so the article must go well beyond both or wait | 2026-10-16 |
| 8 | what do I have to do to make good when my commercial lease ends | New this scan: the Victorian Small Business Commission's retail lease tenant brochure effective 1 July 2026 and its case study of a make good dispute over removing partitions, with LegalVision and other 2026 guides on make good disputes | FAQ addition, article later | 2: document, date | Commercial Law | FAQ added this scan on faq.html, read against the Retail Leases Act 2003 version 027, sections 81 and 87, which send a retail tenancy dispute to the Small Business Commission before VCAT. An article on the end of a lease, make good, the bond or bank guarantee and handing back the premises would need to go well beyond the make good paragraph of /insight-retail-leases-victoria, which is written for the tenant before signing. State no dispute cost figure | 2026-10-23 |
| 9 | commercial and industrial property tax, what will I pay if I buy commercial premises | Carried from 25 Sep: the State Revenue Office's own pages plus 2026 explainers, and LIV LawNews of 17 Sep led with property tax risks | article | 2: document, date | Commercial Law | What a buyer of commercial or industrial premises in Victoria needs to understand about the move from stamp duty to an annual property tax. HIGH ACCURACY RISK: tax, adjacent to the firm's work, and every rate, threshold and transition period changes. Verify each figure against the State Revenue Office at writing time or write without figures, and say plainly that tax advice comes from the client's accountant | 2026-09-25 |
| 10 | can they put that term in the contract, it seems unfair | Re-evidenced 16 Oct: the Treasury release of 29 June 2026 proposing infringement notices and higher penalties for unfair terms, and recent ACCC undertakings from Mable and Aidacare; first evidenced 22 Aug | article | 1: document | Commercial Law | FAQ live since 11 Sep. Fuller article on the unfair terms regime for small business standard form contracts, penalty figures generalised. Treat the proposed penalty increase as a proposal unless the authorised legislation shows it enacted | 2026-10-16 |
| 11 | can I still charge a card surcharge from 1 October | Re-evidenced 16 Oct: the Small Business Ombudsman updated its card surcharging ban guidance on 12 Oct 2026, with Lawpath, ANZ, Xero and Prospa explainers; first evidenced 2 Oct from the Reserve Bank's conclusions on merchant card payment costs and surcharging, with eftpos, Mastercard and Visa introducing no surcharge rules from 1 October 2026 and American Express, UnionPay and PayPal following, and a wave of small business explainers from ANZ, CommBank and Small Business Connections | article | 1: date | Commercial Law | FAQ added 16 Oct on faq.html, read against the Reserve Bank's FAQs on its conclusions and the Ombudsman's page. Article angle: what the end of card surcharging means for a small business's pricing and its customer terms: that the change comes through the card networks' rules after the Reserve Bank's review, that it covers surcharges for paying by card and not weekend, public holiday, booking or service fees, and that the price shown must be the price paid under the Australian Consumer Law. ACCURACY CAUTION: this is payments regulation adjacent to the firm's work; read the Reserve Bank's own pages at writing time and avoid any penalty figure | 2026-10-16 |
| 12 | Re-evidenced 6 Nov: Business Victoria's payday super preparation page, the ATO small business newsroom and CPA Australia on overlapping deadlines remain the leading results for employers; first evidenced 4 Sep from the 1 July 2026 commencement | Carried from 4 Sep: the 1 July 2026 commencement continues to drive employer explainers | article | 1: date | Commercial Law | What payday super means for a small employer in practice, framed as a compliance update. FAQ live since 4 Sep; verify current specifics in the authorised legislation at writing time | 2026-11-06 |
| 13 | can I register a company myself with ASIC or should I use a lawyer | New on 30 Oct: 2026 company registration guides from Sprintlaw, Sleek, Lawpath and Aspire all frame the do it yourself route against a lawyer or accountant, recommending professional help where ownership, trusts or investors are involved | hire | 1: choosing a lawyer | Commercial Law | When registering a company alone is reasonable and when it is not: the choice between a constitution and the replaceable rules, how the shares are issued and to whom, a company acting as trustee, director identification numbers, and why a shareholders agreement belongs at the start rather than after a dispute. Quote only the company set up price fees.html carries, which includes the ASIC registration fee, and no ASIC fee figure of its own, since those index each year and the guides already disagree. PARTIAL OVERLAP: /insight-business-structures and /insight-shareholder-agreements, so stay on the engagement question | 2026-10-30 |
| 14 | are the intervention order laws changing in Victoria | Carried from 25 Sep: the 2026 Act and its staged rollout | faq done | 1: date | Family Law | Covered by the FAQ of 25 Sep. Revisit as an article only once commencement can be stated from the authorised version | 2026-09-25 |

### Page candidates, ideas only and never approval

None. The site carries eight service pages, the limit the playbook sets, so no
page item may be proposed.

### Resource candidates, ideas only that nothing builds automatically

The lead magnet factory was retired on 24 September 2026 and the two published
resources stay. These remain evidenced ideas and nothing more.

1. Small business contract health check checklist, carried from 22 Aug.
2. Director insolvency early warning checklist, carried from 28 Aug.
3. New employer payroll compliance checklist, carried from 4 Sep. Verify every
   listed obligation at build time.
4. Family violence and property settlement records checklist, carried from
   18 Sep, to build only if it can be done responsibly.

### Removed this scan

- "the executor will not distribute and will not tell us anything": covered
  by insight-executor-not-distributing-estate.html, published 2 November 2026.
- "why is probate taking so long in Victoria": added 4 September 2026 and past
  the 60 day window. This scan found only content farm pages and estimates
  that disagree, and no current Probate Office statement, so it was not
  re-evidenced. The FAQs on faq.html stay live.

Item 12, payday super, was re-evidenced this scan and its date moved to
6 November. Items 1, 9 and 14 were first added on 25 September 2026 and leave
the 60 day window on 24 November unless a scan re-evidences them; item 7 was
re-evidenced this week.

### Hire items per practice area

Family Law 2, items 2 and 3; Wills and Estates 2, items 6 and 7;
Commercial Law 2, items 4 and 13. Every area meets the quota with evidence.

### Scan notes, 2026-11-06

Melbourne date established with `TZ=Australia/Melbourne date` before any other
step: Friday 6 November 2026, while the session clock still read 5 November
UTC.

Research run directly with ordinary searches and fetches in the main session,
no subagents: seven searches, one fetch and one Gmail search. Nothing was cut
for budget. News of the fortnight was thin in all three areas. No proclamation
of the intervention order misidentification changes was found; local
reporting still says by November. No November development in Victorian wills,
estates or family law surfaced, and the only new Small Business Commission
item, farm debt mediation changes of 31 October 2026, is outside the firm's
practice. A secondary source claiming unfair contract terms penalties doubled
in March 2026 could not be confirmed and was not used.

Fleet signal: no journalist callout or accepted pitch this week; Gmail held no
pitch from the PR and community routine. The spencer-alexander-bd repository
is not attached to this routine, so its outreach tracker was not read. Client
correspondence was not used as demand evidence. Reddit remains unsearchable by
the search tool.

No FAQ entry was added this scan. Every question with fresh evidence this week
is already answered on faq.html or the family hub, and nothing newly evidenced
could be answered from existing pages without new legal research.

For the Tuesday site accuracy routine: the two faq.html answers on
misidentification say the changes start on a day to be proclaimed and no later
than 10 November 2026. From 10 November that wording is out of date and should
be updated against the authorised Family Violence Protection Act 2008. This
routine only adds and did not touch them.
