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

## Scan of 2026-11-20

Rotation note for the Monday article routine, derived mechanically: the area
whose most recent article is oldest is due. Newest article per area: Family
Law 2026-11-09, parenting consent orders; Wills and Estates 2026-11-02, an
executor who will not distribute the estate; Commercial Law 2026-11-16, make
good at the end of a commercial lease. Wills and Estates is therefore due
Monday 23 November 2026.

Hire marker: the most recent article, insight-make-good-end-of-commercial-lease.html published 2026-11-16, was not a hire guide.

The derivation was conclusive. The repository was shallow, so it was
unshallowed first with `git fetch --unshallow origin main`; `git log
--diff-filter=A` listed one adding commit, 4a856f9; no shallow boundary file
remained, and `git show --name-status` printed A against the file. That
commit's message carries the line `Article type: ordinary` and no hire guide
line. Monday 23 November is therefore due a HIRE GUIDE, in Wills and Estates.
Item 2, what it costs to contest a will and who pays, is the recommendation;
item 3, applying for probate without a lawyer, is the fallback.

| # | Topic, in the searcher's words | Demand evidence, source in one line | Intent | Enquiry intent | Practice area | Suggested angle | Added |
|---|---|---|---|---|---|---|---|
| 1 | is the wrong person named on my intervention order, and what changed on 10 November | Re-evidenced 13 Nov: the Federation of Community Legal Centres reform pages, Mornington Peninsula News and Parliament's justice reforms page still lead searches on misidentification, and faq.html now states the changes apply from 10 November 2026, read in the authorised version in the 9 Nov audit; first evidenced 25 Sep from Victoria Legal Aid, the Women's Legal Service and the Federation | article | 3: document, date, choosing a lawyer | Family Law | The respondent's side of an intervention order where the wrong person has been named: why it happens, what police and courts must now weigh, why the order must still be obeyed while it stands, and how an order is contested, varied or revoked, with the 21 day leave route for an order made in the respondent's absence. READY for the next ordinary Family Law slot now that commencement is on the site; read the Family Violence Protection Act 2008 in its current authorised version at writing time. PARTIAL OVERLAP: /insight-intervention-orders and two faq.html answers, so the article must go well beyond them | 2026-11-13 |
| 2 | what will it cost to contest a will, and who pays the legal costs | Re-evidenced 20 Nov: Victorian costs pages from Turner Freeman, Armstrong Legal and Maurice Blackburn still lead searches on who pays when a will is contested, each saying the estate does not always bear the costs; first evidenced 16 Oct from Armstrong Legal and Maurice Blackburn cost and no win no fee pages | hire | 2: date, choosing a lawyer | Wills & Estates | RECOMMENDED for Monday 23 November, the Wills and Estates hire guide. The hire guide counterpart to /insight-contesting-a-will, which has no costs section: what drives the cost of a claim, mostly whether it settles at mediation or runs to trial, that the court decides who bears costs and that they are not always paid from the estate, what a lawyer assesses first, and the six month limit that makes an early call matter. PARTIAL OVERLAP: service-contesting-a-will.html already answers who pays the legal costs of a will dispute in one paragraph, so the article must go well beyond it. State no cost range and no promise about costs orders; read the Administration and Probate Act 1958 and the court rules on costs in the authorised version at writing time and generalise anything uncertain. Keep to a written fee estimate before substantive work | 2026-11-20 |
| 3 | do I need a lawyer to apply for probate, or can I do it myself | Re-evidenced 20 Nov: the Supreme Court's probate FAQs, which say an executor named in the will may apply, lead results alongside 2026 do it yourself guides from Willed, Safewill and Bare; first evidenced 16 Oct from the Probate Office's statement that applicants may apply without a lawyer | hire | 2: document, choosing a lawyer | Wills & Estates | FALLBACK for Monday 23 November. When an executor can reasonably apply alone and when a lawyer earns the fee: the online application, the advertisement and the affidavits, the inventory, requisitions from the Probate Office, and the personal liability an executor carries for the administration that follows. Quote the probate application fee and the Court's filing fee exactly as playbooks/fees.json carries them, naming each in the sentence that quotes it. FAQ added 13 Nov on faq.html from the verified wording of service-probate.html. PARTIAL OVERLAP: service-probate.html already says an executor can apply without a lawyer and /insight-probate-victoria has a cost section, so the article must go well beyond both or wait | 2026-11-20 |
| 4 | what happens at a first meeting with a family lawyer, and what should I bring | Re-evidenced 6 Nov: Unified Lawyers and Meillon and Bright first appointment guides, both on what to bring and that there is no obligation to engage; first evidenced 25 Sep from 2026 first consultation guides answering what to bring, how long it takes and whether there is any obligation | hire | 2: document, choosing a lawyer | Family Law | What actually happens in a first family law conversation, what is worth bringing, that a support person is welcome, that it is confidential whether or not you engage, and what you should expect to walk away knowing. PARTIAL OVERLAP: faq.html and family-law.html answer what to bring, and service-property-settlement.html has a what to bring section, so the article must go well beyond the document list | 2026-11-06 |
| 5 | can I use mum's power of attorney to move her into aged care, and what if she never signed one | New on 9 Oct: the editor of Australian Ageing Agenda accepted on 5 Oct 2026 the PR routine's pitch on enduring powers of attorney at the point of aged care admission, asking for 600 to 800 words; 2026 adviser explainers on attorneys and aged care admission | article | 2: document, date | Wills & Estates | What an attorney for personal and financial matters can and cannot do at an aged care move, and what the family faces where no power was signed, being an application to VCAT for a guardianship or administration order. FAQ added 9 Oct, read against the Powers of Attorney Act 2014 version 007, sections 3, 21, 22 and 23, and the Guardianship and Administration Act 2019 version 010, sections 30 and 31. PARTIAL OVERLAP: /insight-enduring-powers-of-attorney and /insight-guardianship-administration-orders, so the article must stay on the admission moment. State nothing about Commonwealth aged care agreements or fees unless read in the authorised version | 2026-10-09 |
| 6 | commercial and industrial property tax, what will I pay if I buy commercial premises | Re-evidenced 13 Nov: the State Revenue Office's commercial and industrial property tax pages and videos lead the results, and Pitcher Partners' note on the Office's 2026 to 27 compliance focus names commercial and industrial land; first evidenced 25 Sep, when LIV LawNews of 17 Sep led with property tax risks | article | 2: document, date | Commercial Law | What a buyer of commercial or industrial premises in Victoria needs to understand about the move from stamp duty to an annual property tax. HIGH ACCURACY RISK: tax, adjacent to the firm's work, and every rate, threshold and transition period changes. Verify each figure against the State Revenue Office at writing time or write without figures, and say plainly that tax advice comes from the client's accountant | 2026-11-13 |
| 7 | do I need a lawyer for a shareholder dispute, and what will it cost | New on 2 Oct: Melbourne and national dispute pages, namely PCL, MST, Gibbs Wright, A and I Lawyers and Sajen Legal, all frame the engagement question, with early advice before positions harden the common answer | hire | 2: document, choosing a lawyer | Commercial Law | The hire guide counterpart to /insight-business-partner-disputes-victoria, for a later Commercial Law hire slot: what a lawyer does first in a co-owner dispute, why the documents and the company records are read before anything else, what drives cost, which is mostly whether the matter settles or is litigated, and how early advice keeps a negotiated exit open. Keep to a written fee estimate before substantive work; state no rate and none of the litigation cost ranges other firms publish. Not in the very next Commercial Law slot | 2026-10-02 |
| 8 | what will a family lawyer cost me, and do I need one at all | New on 13 Nov: 2026 Melbourne cost guides from JB Solicitors, Jameson Law, Melbourne Family Lawyers and Unified Lawyers, and a cost comparison guide updated June 2026, all lead with what family law costs and when a lawyer is needed | hire | 1: choosing a lawyer | Family Law | What drives the cost of a family law matter, which is mostly whether it settles by agreement or runs to court, what the written estimate and costs disclosure tell you before any substantive work, which steps the firm does on fixed fees, and what a client can do to keep the cost down. FAQ added 13 Nov on faq.html on whether a divorce needs a lawyer. State no hourly rate and none of the cost ranges other firms publish; quote only fees.html figures. PARTIAL OVERLAP: the cost sections of /insight-divorce-in-victoria and /insight-agreed-property-settlement, so stay on the whole matter rather than one step | 2026-11-13 |
| 9 | can they put that term in the contract, it seems unfair | Re-evidenced 13 Nov: the Treasury release of 29 June 2026 still leads results, with SmartCompany and Astris Law explainers; on 16 Oct also proposing infringement notices and higher penalties for unfair terms, and recent ACCC undertakings from Mable and Aidacare; first evidenced 22 Aug | article | 1: document | Commercial Law | FAQ live since 11 Sep. Fuller article on the unfair terms regime for small business standard form contracts, penalty figures generalised. Treat the proposed penalty increase as a proposal unless the authorised legislation shows it enacted | 2026-11-13 |
| 10 | can I still charge a card surcharge from 1 October | Re-evidenced 16 Oct: the Small Business Ombudsman updated its card surcharging ban guidance on 12 Oct 2026, with Lawpath, ANZ, Xero and Prospa explainers; first evidenced 2 Oct from the Reserve Bank's conclusions on merchant card payment costs and surcharging, with eftpos, Mastercard and Visa introducing no surcharge rules from 1 October 2026 and American Express, UnionPay and PayPal following, and a wave of small business explainers from ANZ, CommBank and Small Business Connections | article | 1: date | Commercial Law | FAQ added 16 Oct on faq.html, read against the Reserve Bank's FAQs on its conclusions and the Ombudsman's page. Article angle: what the end of card surcharging means for a small business's pricing and its customer terms: that the change comes through the card networks' rules after the Reserve Bank's review, that it covers surcharges for paying by card and not weekend, public holiday, booking or service fees, and that the price shown must be the price paid under the Australian Consumer Law. ACCURACY CAUTION: this is payments regulation adjacent to the firm's work; read the Reserve Bank's own pages at writing time and avoid any penalty figure | 2026-10-16 |
| 11 | what does payday super mean for my business now that it has started | Re-evidenced 6 Nov: Business Victoria's payday super preparation page, the ATO small business newsroom and CPA Australia on overlapping deadlines remain the leading results for employers; first evidenced 4 Sep from the 1 July 2026 commencement | article | 1: date | Commercial Law | What payday super means for a small employer in practice, framed as a compliance update. FAQ live since 4 Sep; verify current specifics in the authorised legislation at writing time | 2026-11-06 |
| 12 | can I register a company myself with ASIC or should I use a lawyer | New on 30 Oct: 2026 company registration guides from Sprintlaw, Sleek, Lawpath and Aspire all frame the do it yourself route against a lawyer or accountant, recommending professional help where ownership, trusts or investors are involved | hire | 1: choosing a lawyer | Commercial Law | When registering a company alone is reasonable and when it is not: the choice between a constitution and the replaceable rules, how the shares are issued and to whom, a company acting as trustee, director identification numbers, and why a shareholders agreement belongs at the start rather than after a dispute. Quote the company set up fee and ASIC's registration fee exactly as playbooks/fees.json carries them, naming each in the sentence that quotes it, and no other ASIC figure, since the guides disagree. PARTIAL OVERLAP: /insight-business-structures and /insight-shareholder-agreements, so stay on the engagement question | 2026-10-30 |
| 13 | I have been served with a statutory demand, what do I do | Evidenced 23 Nov by the audit of that day, playbooks/audit-2026-11-23/article-proposals.md: asked of the answer engines without a country, two answered with the law of England and Wales, and one results list set to Australia returned the Federal Court's information sheet and eight law firm pages titled as the question; the site answers it only inside the debt recovery page, the commercial hub and one FAQ answer | article | 3: document, date, choosing a lawyer | Commercial Law | What a company must do in the 21 days after a statutory demand under the Corporations Act 2001 (Cth) is served: pay, secure or compromise the debt, or apply to set the demand aside with the affidavit filed and served in time, what a genuine dispute and an offsetting claim are, and what follows if nothing is done. Open with a sentence that names Australia, the Act and the deadline. PARTIAL OVERLAP: /insight-debt-recovery-victoria treats the demand from the creditor's side, so this article stays on the recipient's side | 2026-11-23 |
| 14 | how much does probate cost in Victoria with a lawyer | Evidenced 23 Nov by the audit of that day, playbooks/audit-2026-11-23/article-proposals.md: on Google, searched as if from Box Hill, seven of the ten first page results for how much does probate cost Victoria were pages about the cost alone and the firm was not among them; on the answer engines every fee question was answered from pages titled as the cost question, by cost guides and by firms such as Campus Lawyers and Holt and Macdonald | hire | 2: document, choosing a lawyer | Wills & Estates | A hire guide titled as the question. The fixed fee and what it covers and assumes, the Supreme Court's filing fee by the gross value of the assets in Victoria with one worked total, the notice fee, what makes an estate fall outside the fixed fee, and who pays, in the wording settled on 9 Nov 2026 for rule 9.01. Quote every figure exactly as playbooks/fees.json carries it, naming the fee or charge in the same sentence. PARTIAL OVERLAP: /insight-probate-victoria has a cost section and /service-probate a fee note, so the article must go well beyond both, and each then links to it | 2026-11-23 |
| 15 | my ex will not return the children, what can I do | Evidenced 23 Nov by the audit of that day, playbooks/audit-2026-11-23/article-proposals.md: no answer engine returned the firm, and the pages returned were titled as the question, among them Victoria Legal Aid's recovery order material and Family Violence Law Help; the site mentions recovery orders only in passing, on four pages | article | 2: date, choosing a lawyer | Family Law | What a parent can do when a child is not returned: what the parenting orders or plan say, a recovery order under the Family Law Act 1975 (Cth) and who may apply, how urgent applications are heard, when the police act, and safety first. Open with a sentence that names Australia and the Act. PARTIAL OVERLAP: /service-parenting-arrangements and /insight-parenting-arrangements | 2026-11-23 |
| 16 | how much does a will cost in Melbourne | Evidenced 23 Nov by the audit of that day, playbooks/audit-2026-11-23/article-proposals.md: the engines answered from pages titled as the cost question, among them Fogarty Oliver Rothschild's, and quoted the firm's own prices correctly whenever they found the fees page | hire | 1: choosing a lawyer | Wills & Estates | A hire guide titled as the question: a single will, wills for a couple, the two estate plans and the two testamentary trust fees, what each covers, and when a simple will is not enough. Quote every figure exactly as playbooks/fees.json carries it. PARTIAL OVERLAP: /service-wills-and-estate-planning and /insight-trustee-company-or-lawyer-will | 2026-11-23 |
| 17 | how much does a divorce cost in Victoria with a lawyer | Evidenced 23 Nov by the audit of that day, playbooks/audit-2026-11-23/article-proposals.md: one engine answered a Victorian divorce cost question with pages about Victoria in British Columbia, and the firm's fees were quoted correctly by another that found them | hire | 1: choosing a lawyer | Family Law | A hire guide titled as the question: the joint and sole application fees and what each covers, the Court's filing fee and its reduced fee, service, and what is not included, such as property and parenting. Name the Family Law Act 1975 (Cth) and the Federal Circuit and Family Court of Australia in the opening. PARTIAL OVERLAP: /service-divorce and item 8 | 2026-11-23 |
| 18 | how much do consent orders cost with a lawyer | Evidenced 23 Nov by the audit of that day, playbooks/audit-2026-11-23/article-proposals.md: two engines set the firm's consent orders fees in answers beside other firms' published prices, from pages titled for lawyers in Box Hill and not for the question | hire | 1: choosing a lawyer | Family Law | A hire guide titled as the question: the three consent orders fees, what each covers, the Court's filing fee, and what moves a matter outside an agreed application. PARTIAL OVERLAP: /insight-parenting-consent-orders and /insight-agreed-property-settlement | 2026-11-23 |
| 19 | how much does a shareholders agreement cost in Australia | Evidenced 23 Nov by the audit of that day, playbooks/audit-2026-11-23/article-proposals.md: the engines answered from Sprintlaw's and Blaze Business and Legal's pages titled as the question, and one cited the firm's shareholder agreements page for its fee and scope | hire | 1: choosing a lawyer | Commercial Law | A hire guide titled as the question: the fee and its scope of one company, up to three shareholders and agreed terms, what costs more, company set up and ASIC's registration fee. PARTIAL OVERLAP: /insight-shareholder-agreements and item 12 | 2026-11-23 |
| 20 | how much does a lawyer charge to review a commercial lease | Evidenced 23 Nov by the audit of that day, playbooks/audit-2026-11-23/article-proposals.md: one engine said none of its results gave Melbourne pricing, and the pages cited were titled as the question | hire | 1: choosing a lawyer | Commercial Law | A hire guide titled as the question: the fee for reviewing a lease for a tenant and what it covers, what a review looks for, and what costs more. PARTIAL OVERLAP: /service-commercial-leases and /insight-retail-leases-victoria | 2026-11-23 |

### Page candidates, ideas only and never approval

None. The site carries twelve service pages, the cap Spencer approved on
9 November 2026, so no page item may be proposed.

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

- "what do I have to do to make good when my commercial lease ends": covered
  by insight-make-good-end-of-commercial-lease.html, published 16 November
  2026.

Items 2 and 3 were re-evidenced this scan and their dates moved to
20 November. Item 7 leaves the 60 day window on 1 December and item 5 on
8 December unless re-evidenced. Items 4 and 11 had their evidence written in
the topic column; the topic is now in the searcher's words and the evidence
is in its own column.

### Hire items per practice area

Family Law 2, items 4 and 8; Wills and Estates 2, items 2 and 3;
Commercial Law 2, items 7 and 12. Every area meets the quota with evidence.

### Scan notes, 2026-11-20

Melbourne date established with `TZ=Australia/Melbourne date` before any other
step: Friday 20 November 2026, while the session clock still read 19 November
UTC.

Research run directly with ordinary searches in the main session, no
subagents: six searches and one Gmail search. Nothing was cut for budget.
News of the fortnight was thin again: no November development in Victorian
wills and estates, family law or small business law surfaced beyond what the
backlog already carries. New domestic building contract laws from 1 December
2026 surfaced but concern home building rather than the firm's practice
areas, so they were not added. Searches on online wills and on how long after
probate an estate can be distributed showed strong demand, and both questions
are already answered on the site, the second on faq.html and in the executor
guides, so neither became a backlog item.

Fleet signal: no journalist callout or accepted pitch this week; Gmail sent
mail and drafts held no pitch from the PR and community routine. The
spencer-alexander-bd repository is not attached to this routine, so its
outreach tracker was not read. Client correspondence surfaced by the Gmail
search was not read or used as demand evidence. Reddit remains unsearchable
by the search tool.

FAQ added this scan on faq.html, built only from wording already verified on
the site: "Is a will made online or from a will kit valid in Victoria?", from
the will kit and formal validity sections of insight-making-a-valid-will.html,
placed after the trustee company question in the Wills and Estates group.
Evidence: State Trustees Victoria's online wills pages, Lawpath and Willed
guides on whether an online will is valid.
