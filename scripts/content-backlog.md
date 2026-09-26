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

## Scan of 2026-09-25

Rotation note for the Monday article routine, derived mechanically (the area
whose most recent article is oldest is due). Newest article per area:
Wills and Estates 2026-09-21 (misuse of a power of attorney), Commercial Law
2026-09-07 (safe harbour and small business restructuring), Family Law
2026-08-31 (grandparents rights). Family Law is therefore due Monday
28 September 2026.

Hire marker: the most recent article, insight-power-of-attorney-misuse.html published 2026-09-21, was not a hire guide.

The derivation was conclusive. The repository was shallow, so it was
unshallowed first; `git log --diff-filter=A` listed exactly one adding commit,
5585142; no shallow boundary file remained, and `git show --name-status`
printed A against the file. That commit's message carries no
`Article type: hire guide` line, which for an article published before the
rule existed means an ordinary article. Monday 28 September is therefore due a
HIRE GUIDE, in Family Law. Items 5 and 6 below are the two evidenced Family
Law hire candidates, and item 5 is the recommendation.

| # | Topic (searcher's words) | Demand evidence (source, one line) | Intent | Enquiry intent | Practice area | Suggested angle | Added |
|---|---|---|---|---|---|---|---|
| 1 | police named me as the respondent but I am the one being abused | New this scan: Victoria Legal Aid, the Women's Legal Service and the Federation of Community Legal Centres all published on misidentification through 2026, and the Parliament of Victoria justice reforms page describes the new duty on police and courts to consider it | article | 3: document, date, choosing a lawyer | Family Law | The respondent's side of an intervention order where the wrong person has been named: why it happens, what the reforms require police and courts to weigh, what evidence shows the longer pattern, why the order must still be obeyed while it stands, and how an order is contested, varied or revoked. FAQ added this scan. The word misidentification appeared nowhere on the site before today, so this is genuinely open ground next to /insight-intervention-orders | 2026-09-25 |
| 2 | how much does probate cost in Victoria | New this scan: 2026 Victorian cost guides (Bare, National Probate, Making Probate Easy, Holt Mac, Campus Lawyers, MST on the fee changes) plus the Supreme Court's own probate fees page, a consistently heavy commercial intent search | hire | 3: document, date, choosing a lawyer | Wills & Estates | What drives the cost of a grant: the court filing fee scaled to the gross value of the Victorian estate, the advertising charge, and legal fees that turn on the shape of the estate. Keep to what the site already says about fees, that probate and estate administration are estimated in writing once the shape of the estate is known, and state no figure, since court fees are reviewed each financial year. FAQ added this scan; the article is the fuller treatment | 2026-09-25 |
| 3 | what does a lawyer actually check when I buy a business | New this scan: 2026 due diligence guides (Sprintlaw, Parke, Dettmanns, Bentleys, Xero, Business Queensland) all answering the same question, with the share sale versus asset sale distinction leading | hire | 3: document, date, choosing a lawyer | Commercial Law | What legal due diligence covers and why a buyer pays for it: ownership of the assets, the lease, contracts and licences, employees, disputes and what liabilities follow the business, and why the share sale and asset sale distinction changes the whole risk picture. REHASH CAUTION: /insight-buying-a-business-victoria already covers buying a business and carries a "Do I need a lawyer to buy a business in Victoria?" FAQ, so this only works as a hire guide if it stays on the engagement question, what the work involves and what drives its cost | 2026-09-25 |
| 4 | should I get a lawyer to look at my lease before I sign | New this scan: 2026 lease review guides (LegalVision, Sprintlaw, Gladwin, Allied, Madison Marcus, Whelan) all answering it, with the retail versus commercial characterisation point and "get advice before the letter of offer" leading | hire | 3: document, date, choosing a lawyer | Commercial Law | When to bring a lawyer into a lease and what a review covers: that whether a lease is retail or commercial turns on the facts and not the label, and changes the tenant's rights; that the time to ask is before the letter of offer or heads of agreement, not after. REHASH CAUTION: /insight-retail-leases-victoria covers what a tenant must check and commercial-law.html carries a "What should I check before signing a commercial lease?" FAQ, so this must stay on the engagement question. NOTE: the held corrections branch rewrites the repairs material in that article, so avoid repairs entirely until those are published | 2026-09-25 |
| 5 | we have agreed how to split everything, do we still need lawyers | New this scan: 2026 property settlement cost guides (Fogarty Oliver and Rothschild, Aitken, Patterson, Clarity, Lander, Joliman) all leading with the DIY question and the risk that an informal agreement binds nobody | hire | 2: date, choosing a lawyer | Family Law | RECOMMENDED FOR MONDAY 28 SEP as the Family Law hire guide. What a lawyer does when a couple has already agreed: that a handshake or a signed letter is not binding and does not stop a later claim, that consent orders or a binding financial agreement are the two routes that are, what each involves, that a binding financial agreement requires independent legal advice for each person, and the time limits that sit over all of it. Keep to a written fee estimate before substantive work begins; state no rate and no court fee figure. Builds on /insight-property-after-separation and /insight-binding-financial-agreements without repeating them | 2026-09-25 |
| 6 | what happens at a first meeting with a family lawyer and what do I bring | New this scan: 2026 first consultation guides (Turnbull Hill, Go To Court, Strategic, Michael Lynch, Australian Family Lawyers, Gramelis) answering what to bring, how long it takes and whether there is any obligation | hire | 2: document, choosing a lawyer | Family Law | The alternative Family Law hire guide if item 5 is taken: what actually happens in a first family law conversation, what is worth bringing and what is not needed, that a support person is welcome, that it is confidential whether or not you engage, and what you should expect to walk away knowing. PARTIAL OVERLAP: faq.html carries "What should I prepare before my first appointment?" and family-law.html "What should I bring to a first appointment?", so the article must go well beyond the document list | 2026-09-25 |
| 7 | my business partner stopped working but keeps their shares | Carried from 4 Sep and still evidenced: 2026 guides continue to name founder fallout and inactive equity as the live dispute pattern in Australian small companies | article | 2: document, choosing a lawyer | Commercial Law | Dispute side companion to /insight-shareholder-agreements: deadlock, the co-owner who stops contributing but keeps their stake, the oppression remedy, buyout orders, mediation. FAQ live since 4 Sep; the article remains the fuller treatment | 2026-08-22 |
| 8 | the executor will not distribute and will not tell us anything | New this scan: the standing Whirlpool estate threads (Dispute between Executor and Beneficiary, Deceased estate siblings taking advantage, and the executor's year discussion in the probate thread) are the clearest recurring beneficiary side pattern in Australian consumer forums | article | 2: document, date | Wills & Estates | The beneficiary's side, which the site answers only as a short FAQ: what a beneficiary is and is not entitled to see, the expectation that an estate is administered within about a year and what that does and does not mean, how to ask for accounts, and what the court can do where an executor will not act. Distinct from /insight-executor-duties, which is written for the executor. Verify every remedy carefully, and generalise any timing | 2026-09-25 |
| 9 | why is probate taking so long in Victoria | Carried from 18 Sep and still evidenced: 2026 Victorian guides continue to describe rising volumes, requisitions and digital lodgement backlogs, with grants commonly taking some weeks | faq done, article later | 2: document, date | Wills & Estates | FAQs live since 11 Sep (probate timing, what an executor can do while waiting). A short update to /insight-probate-victoria only if published timeframes clearly worsen; the article as written remains accurate | 2026-09-04 |
| 10 | commercial and industrial property tax, what will I pay if I buy commercial premises | New this scan: the State Revenue Office's own CIPT pages plus 2026 explainers (RSM, marshalls dent wilmoth, LPLC, Tickbox), and the firm's own LIV LawNews of 17 Sep led with "Property tax changes create risks for clients" | article | 2: document, date | Commercial Law | What a buyer of commercial or industrial premises in Victoria needs to understand about the move from stamp duty to an annual property tax, and the transition that follows the first qualifying transaction. HIGH ACCURACY RISK: this is tax, adjacent to the firm's work rather than inside it, and every rate, threshold and transition period is a figure that changes. Either verify each one against the State Revenue Office at writing time or write it without figures, and say plainly that tax advice comes from the client's accountant | 2026-09-25 |
| 11 | is coercive control a crime in Victoria now | Carried from 18 Sep: the Victorian Parliament passed the government's family violence reforms on 10 September 2026 (Premier's media release), creating a standalone coercive control offence for intimate partner relationships, with commencement reported for 2028 | article | 1: date | Family Law | The strongest ordinary (non hire) Family Law article candidate, in the shape of the fraudulent calumny update: what the new offence covers, that it is not yet in force, that commencement is expected in 2028, and what protects people now. The faq.html answer was refreshed 18 Sep. Reported penalty figures vary between the bills, so generalise or verify hard at writing time | 2026-08-28 |
| 12 | are the intervention order laws changing in Victoria | New this scan: the Justice Legislation Amendment (Family Violence, Stalking and Other Matters) Act 2026 is Act 1/2026 on legislation.vic.gov.au, and Victoria Legal Aid, the Women's Legal Service and Victorian community papers through August and September 2026 describe the changes rolling out in stages | faq done | 1: date | Family Law | Covered by the FAQ added this scan, which describes the changes and says plainly that they commence in stages and some are not yet in force. Revisit as an article only once commencement is certain and can be stated from the authorised version of the Act; the secondary sources disagree enough on timing that no date should be published yet | 2026-09-25 |
| 13 | should I use the public trustee or a lawyer for my will | Carried from 11 Sep: 2026 comparison guides plus the standing Whirlpool threads, a consistent decision stage question | hire | 1: choosing a lawyer | Wills & Estates | The choices for drafting a will and appointing an executor (trustee company, lawyer, family member), fee models generalised, even handed and with no disparagement of anyone. An FAQ was added 11 Sep 2026; the article remains the fuller treatment | 2026-08-22 |
| 14 | is a will kit valid, or do I need a lawyer | Re-evidenced this scan: 2026 DIY will guides (Lawpath, Legal123, Will Hero, Taylor and Scott, Moneysmart) all answering the same validity question, one of the highest volume wills searches | hire | 1: choosing a lawyer | Wills & Estates | Factual about what makes a will valid in Victoria, in writing, signed, and witnessed by two adults present at the same time, and about where kit wills actually fail: witnessing errors, wording that means two things, blended families, and assets a will cannot deal with. Never disparage kits as such. PARTIAL OVERLAP: wills-and-estates.html carries "Can I just use a will kit?" and /insight-making-a-valid-will carries "Can I write my own will in Victoria?", so the article must be substantially more than those two answers, which is why no FAQ was added this scan | 2026-09-25 |
| 15 | do employers have to pay super every payday now | Carried from 4 Sep and still evidenced: the 1 July 2026 commencement continues to drive employer explainers | article | 1: date | Commercial Law | What payday super means for a small employer in practice, framed as a compliance update. FAQ live since 4 Sep; verify current specifics at writing time | 2026-09-04 |
| 16 | can they put that term in the contract, it seems unfair | Carried from 11 Sep: ACCC enforcement priorities keep unfair contract terms named, with continuing enforcement reported through 2026 | article | 1: document | Commercial Law | FAQ live since 11 Sep. Fuller article on the unfair terms regime for small business standard form contracts, penalty figures generalised | 2026-08-22 |

### Page candidates (ideas only, never approval)

1. **Probate and letters of administration, Box Hill** (new this scan). A
   dedicated service page for the firm's probate service at Suite 10, 1 Main
   Street, Box Hill. Evidence: items 2 and 9 above, where the commercial
   intent is a person who holds a will and a death certificate, wants to know
   what a grant costs and how long it takes, and is choosing who to instruct.
   The article format serves the explanation but not the engagement. The site
   carries no service-*.html page yet, so this would be the first of the
   eight the playbook allows. **Builds only if Spencer approves it in a
   session and it appears in the Approved service pages list in
   playbooks/service-pages.md. Nothing in this file is approval.**

### Resource candidates (ideas only; nothing builds these automatically)

The lead magnet factory was retired on 24 September 2026 and the two published
resources stay. These remain evidenced ideas and nothing more.

1. Small business contract health check checklist (carried from 22 Aug): a one
   page review list for standard form contracts and unfair terms exposure.
2. Director insolvency early warning checklist (carried from 28 Aug, follows
   the 7 Sep safe harbour article).
3. New employer payroll compliance checklist (carried from 4 Sep). Verify every
   listed obligation at build time.
4. Family violence and property settlement records checklist (carried from
   18 Sep): handle with full accuracy severity and a safety framing, and build
   only if it can be done responsibly.

### Removed this scan

- "attorney misusing power of attorney": covered by
  insight-power-of-attorney-misuse.html, published 21 September 2026.
- "time limit for property settlement after separation": answered by the
  faq.html entry added 18 September 2026, and the divorce and de facto
  articles carry the limits in depth. Nothing further is needed.

Nothing was dropped for age this scan. The oldest carried items were added
22 August 2026 and pass out of the 60 day window in late October.

### Scan notes, 2026-09-25

Melbourne date established with `TZ=Australia/Melbourne date` before any other
step; the session clock still read Thursday 24 September UTC.

Research run directly with ordinary searches in the main session per the
standing rule, no workflow subagents. Roughly fourteen searches and fetches
across the signal categories. Nothing was cut for budget.

The week's defining signal is the staged rollout of the Justice Legislation
Amendment (Family Violence, Stalking and Other Matters) Act 2026. The Act
itself was confirmed on the authorised source, legislation.vic.gov.au, as Act
1/2026, which is the first statutory claim this routine has been able to check
against primary legislation since the egress note changed on 24 September; the
landing page does not show assent or commencement, so the commencement timing
rests on secondary sources, which disagree. Victoria Legal Aid reported the
passage in February 2026 without a commencement date, while Victorian
community papers in August 2026 and the Parliament of Victoria justice reforms
page report further changes beginning in November. Both FAQ answers added this
scan were therefore written to describe the substance and to say that the
changes commence in stages with some not yet in force, and no date was
published. If a later run can read the commencement provisions from the
authorised version, an article becomes possible.

Misidentification is the strongest genuinely open topic found this scan. The
word appears nowhere on the site, the demand is well documented by Victoria
Legal Aid, the Women's Legal Service and the Federation of Community Legal
Centres, and the searcher scores the full three on enquiry intent: they hold
court papers, they face a hearing date, and they need a lawyer now.

Hire items: two evidenced candidates were found in each of the three practice
areas, so the playbook's quota is met without inventing anything. The two
commercial hire items both carry a rehash caution, because the site already
covers buying a business and retail leases as articles and answers the
engagement question for each as an FAQ. They are recorded honestly rather than
dropped, but the Monday routine should treat the overlap as real.

Fleet signal, from the firm's own outbound pitching rather than from search.
Eastsider News has accepted the pitch on dying without a will in Boroondara
and Whitehorse. The publication date is 13 November 2026 with a copy deadline
of 10 November 2026, and the AGM referred to in that thread is 13 October,
which Spencer has said he cannot attend. A journalist wanting the topic is
demand evidence, but the site already covers it at
insight-dying-without-a-will.html, so it earns no backlog row; it earns a
diary note. A second pitch, six questions before signing a business contract,
went to SmartCompany on 20 September and has no reply yet; /insight-contracts-for-business
already covers that ground.

Client correspondence was deliberately not used as demand evidence. The
Gmail search surfaced live client matters, and this file is in a public
repository even though `_config.yml` keeps it off the website, so nothing from
a client file appears here.

Site restricted searches for reddit.com again failed outright, this time with
the search tool reporting that reddit.com is not accessible to its user agent,
so that is a hard tooling limitation rather than an absence of discussion.
Whirlpool remains searchable but returns undated archive threads, so item 8
rests on the recurrence of the pattern rather than on threads from the last
month, and is described that way.
