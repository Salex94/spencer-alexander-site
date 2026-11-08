# Claims register: service-shareholder-agreements, 9 November 2026

Page: Shareholder agreements and company set up, built on 9 November 2026 (Melbourne) after Spencer approved the site audit of that day, which lifted the service page limit to twelve and named this page fourth of the four new ones. Hub: commercial-law.html, blocks `svc-shareholder-and-partnership-agreements` and `svc-business-structures-and-formation`. Matching article: insight-shareholder-agreements.html.

## Versions read today, 9 November 2026

Both downloaded today from api.prod.legislation.gov.au, each listed by the Register as current and latest with no unincorporated amendments. Working copies are in the session scratchpad under `np/leg/`, outside the repository.

- Corporations Act 2001 (Cth), Compilation No. 149, 19 September 2026, C2026C00432, all seven volumes.
- Anti-Money Laundering and Counter-Terrorism Financing Act 2006 (Cth), Compilation No. 63, 1 October 2026, C2026C00447.
- Corporations Regulations 2001 (Cth), Compilation No. 214, F2026C00854, searched for an application period under s 1272C(2)(a)(ii); none is prescribed.

## Legal statements on the page

| Where | Statement | Authority read |
|---|---|---|
| Brief bullet 1, FAQ 4 | A proprietary company needs at least one member and at least one director who ordinarily resides in Australia, and can have no more than 50 shareholders who are not employees. | ss 114, 201A(1) and 113(1). A company with crowd sourced funding shareholders needs two directors, s 201A(1A); "at least one" remains true. |
| FAQ 4 | Every director must be at least 18, and a proprietary company does not need a secretary. | ss 201B(1) and 204A(1). |
| Brief bullet 2, process step 1, FAQ 4 | Every director needs a director identification number, or must have applied for one, before being appointed. | s 1272C(1) and (2)(a)(i), with s 1272B(1)(a); no regulation prescribes a later application period. |
| Process step 1 | Each director signs a consent to act before appointment. | s 201D(1) and, on registration, s 117(5). |
| Process step 1 | Before we begin, the AML/CTF Act requires us to verify the identity of our client and of the people who will direct, own or control the company. | AML/CTF Act s 6(5B), Table 6, item 6, under which creating a company is a designated service whose customers include the company's beneficial owners and directors, and s 28(1) to (3). It matches the verified B2 wording for privacy.html. |
| Setting up block, process step 2 | The company exists from the start of the day it is registered, with the members, directors and any secretary named in the application. | ss 117(1), 118(1), 119 and 120(1). |
| Process step 3 | Each member agrees in writing to the constitution before the application is lodged, so the company adopts it on registration. | s 136(1)(a). |
| Brief bullet 3, agreement and constitution section, FAQ 2 | The constitution, with any replaceable rules that apply, is a contract between the company and each member and between the members; it can be changed by special resolution, passed by at least 75 per cent of the votes cast by members entitled to vote. | ss 140(1)(a), (c), 136(2) and 250MA(b). |
| Constitutions block | Without its own constitution, a company's internal management is generally governed by the replaceable rules, under which the directors of a proprietary company can refuse to register a share transfer for any reason, and new shares must be offered first to existing holders of that class in proportion to their holdings unless the members resolve otherwise. | ss 134, 135(1), (2), 1072G and 254D(1), (4). "Generally" covers s 135(1)'s exclusion of a company whose sole director is its sole shareholder, and companies registered before 1 July 1998 that kept their constitution. |
| Brief bullet 4, agreement and constitution section, FAQ 2 | A shareholder agreement is a contract that binds only those who sign it and cannot change the constitution by itself; it usually provides that it prevails between the parties and obliges them to amend the constitution to remove a conflict. | General law of contract, and s 136(2) for amendment. The wording follows the content review's item 48. |
| Co-owners block, FAQ 3 | Where a company's affairs are conducted against the interests of the members as a whole, or oppressively, unfairly prejudicially or unfairly discriminatorily against a member, the court can make a wide range of orders, including a share purchase or winding up; it can also wind up a company where that is just and equitable. | ss 232(a), (d), (e), 233(1)(a), (d) and 461(1)(k). Every limb of s 232(d) and (e) is stated; the page names conduct of the company's affairs, one of the three kinds of conduct in s 232(a) to (c), as a sufficient case rather than the whole test. |
| Agreement and constitution section | With two equal owners neither can outvote the other and decisions can stall. | The verified wording of faq.html's answer on 50/50 companies, which the audit's commercial reviewer confirmed. |
| Who we act for | Many of the disputes that end businesses begin between co-owners who never agreed in writing how decisions are made and how one of them can leave. | The audit's verified A6 wording, a general observation rather than a statement of law. |

## Generalised or left out, and why

- Directors' duties, the sole director and sole shareholder company's special rules, share classes, employee share schemes and investor terms are not described.
- Restraints are named only as a topic an agreement covers; whether a restraint is enforceable is general law that turns on its reasonableness, and nothing about it is stated.
- ASIC's registration fee is not given as a figure, because it rises each 1 July; the page says it is passed on at cost. Whether it attracts GST is not stated.
- Practice statements, not law: when owners call, that equal owners need an agreement most, that a constitution is commonly a standard document, and that we work with your accountant, which is the hub's wording.
- What to have with you names the constitution, an ASIC company extract, any owners' agreement, the latest financial statements, or for a new company the proposed directors, shareholders and shareholdings, all things owners plainly hold or know; it states no legal requirement and keeps the line that having little on paper is fine.
- One spelling throughout: "shareholder agreement", as in the title the brief set, the h1, the hub's block and the article. The fees page names the row "Shareholders agreement"; the content review noted the two forms, and the page links that row by its id.

## Fees

Copied from fees.html as the central pass of 9 November 2026 leaves it: company set up $660 including GST, which is $600 plus GST, a fixed fee, with the row's scope, and ASIC's registration fee passed on at cost, linked to `/fees#fee-company-set-up`; shareholders agreement from $2,420 including GST, never called a fixed fee, with its scope and "costs more" sentence, linked to `/fees#fee-shareholders-agreement`. A dispute between owners is estimated in writing. The schema carries one offer, company set up at $660.

## The brief asked for six questions; the gate requires five

The page carries five, as `playbooks/service-pages.md` and the gate require. A sixth, "What should a shareholder agreement cover?", would repeat the shareholder agreements block, so it is not proposed.

## Checks run

- Built with `scripts/build-service-page.py`: 1,771 visible words in `<main>`, including the hub's rail cards.
- `scripts/check_style.py` on the page's visible text: PASS, with a note only for paragraph shape.
- `scripts/check-publish.py` in this branch: "prices quoted elsewhere match fees.html" fails on $660 only because this branch's fees.html still shows the old $1,210; the central pass's fees.html carries $660 and the check passes there. The page shares the other expected failures from files outside this task, the page limit and the hub link, sitemap and llms.txt entries. In a test copy of the central branch with sitemap and llms.txt entries added, the service page checks pass for this page.
