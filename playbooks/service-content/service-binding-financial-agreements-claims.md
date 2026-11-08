# Claims register: service-binding-financial-agreements, 9 November 2026

Page: Binding financial agreements, built on 9 November 2026 (Melbourne) after Spencer approved the site audit of that day, which lifted the service page limit to twelve and named this page second of the four new ones, with "prenup" in the lead and description. Hub: family-law.html, block `svc-binding-financial-agreements`. Matching article: insight-binding-financial-agreements.html. The builder adds the Quick exit link, as on every family law page.

## Version read today, 9 November 2026

- Family Law Act 1975 (Cth), Compilation No. 101, compilation date 10 June 2025, register ID C2025C00341. Both Word volumes were downloaded today from api.prod.legislation.gov.au. The Register lists it as current and latest, with no unincorporated amendments. Working copies are in the session scratchpad under `np/leg/fla/`, outside the repository.

## Legal statements on the page

| Where | Statement | Authority read |
|---|---|---|
| Lead, brief bullet 1 | An agreement can be made before or during a marriage or de facto relationship, or after separation or divorce, and can deal with property, financial resources, superannuation and maintenance. | ss 90B, 90C (with 90C(2A), after breakdown), 90D, 90UB, 90UC and 90UD; superannuation as if property, ss 90XH(1) and 90XHA(1). "Prenup" is the common name, not a legal term. |
| Lead, brief bullet 2, independent advice block, process step 2, FAQ 1 | It generally binds only if all parties sign it, each spouse party received independent legal advice before signing about its effect on their rights and its advantages and disadvantages at that time, each was given the lawyer's signed statement of that advice, a copy of each statement went to the other party or their lawyer, and it has not been terminated or set aside. | s 90G(1)(a) to (d) and s 90UJ(1)(a) to (d). Every limb is stated. "Generally" covers s 90G(1A) and s 90UJ(1A). |
| FAQ 1 | A court can declare an agreement both signed binding where a requirement about the advice or the statements was missed, but only if it would otherwise be unjust and inequitable. | s 90G(1A) to (1C); s 90UJ(1A) to (1C). The signature, missed requirement and unjust and inequitable limbs are stated; the order follows an enforcement application. |
| Brief bullet 3 | Where a binding agreement covers property and financial resources, the court's usual power to divide them does not apply. | s 71A(1) and s 90SA(1). |
| Brief bullet 4, FAQ 2, drafting block, time limits | Grounds for setting aside. | s 90K(1)(a) to (e) and s 90UM(1)(a) to (h), with s 90KA and s 90UN for the general law of contracts, under which duress and undue influence make a contract voidable. Introduced with "such as" and "include", because the superannuation payment flag and unsplittable interest grounds, s 90K(1)(f), (g), are left out. |
| Drafting block | A maintenance provision is void unless it names the person and the amount or value provided; no agreement stops the court ordering maintenance for someone who, when it took effect, could not support themselves without an income tested pension, allowance or benefit. | ss 90E and 90F(1), (1A); ss 90UH(1) and 90UI(1), (2). |
| Ending block | An agreement can be ended only by a later financial agreement or a written termination agreement, made with the same advice and statements. | s 90J(1), (2) and s 90UL(1), (2). |
| Process step 3 | If made before separation, its terms on dividing property take effect only once a separation declaration is signed after separation, or on divorce or death. | s 90DA(1), (1A) and (2) to (4); s 90UF(1) to (5). A de facto couple cannot divorce, so for them only the declaration and death apply, and the page says nothing to the contrary. |
| FAQ 3 | De facto couples make agreements under their own provisions, with the same advice requirement, and an agreement made as de facto partners stops being binding if they later marry each other. | ss 90UB to 90UD, 90UJ(1)(b) and 90UJ(3). The geographical requirement in s 90UA is met by anyone ordinarily resident in Victoria, a participating jurisdiction, and is not stated. |
| FAQ 4 | Consent orders are made by the court, which must be satisfied they are just and equitable; a financial agreement needs no court approval and can be made before a relationship begins. | s 79(2) and s 90SM(2); ss 90B and 90UB. |
| Urgent strip, time limits | After separation, the time to apply for property orders keeps running while you negotiate: generally 12 months from the divorce order taking effect, or two years from the end of a de facto relationship, after which both people's consent or the court's leave is needed, and leave is not guaranteed. | s 44(3), (4), (5)(a)(i), (5)(b) and (6). The extension rule, consent or leave, is stated with the limit. |
| Time limits | If an agreement is set aside or found invalid, you generally have at least 12 months from that date to apply. | s 44(3B) for a divorced couple, 12 months after the later of the divorce taking effect and the setting aside; s 44(5)(a)(ii) for de facto partners. For a married couple who have not divorced, s 44(3) sets no limit, so "at least" holds in every case. |
| Reviewing block | A wedding date is not a legal deadline. | No provision requires an agreement to be signed before a wedding; s 90C covers agreements made during a marriage. |

## Generalised or left out, and why

- Spousal maintenance beyond the two drafting rules, child support agreements, the superannuation splitting procedure in Part VIIIB and stamp duty, s 90L, are not described.
- Cases on duress, undue influence and unconscionable conduct are not named; the page states only that the Act and the general law of contracts allow setting aside on those grounds.
- "Can one lawyer act for both of us?" was cut when the questions were limited to five; it is the spare question below. The independent advice block keeps its substance.
- Practice statements, not law: when people call, that each of you has your own lawyer, that we tell you plainly which instrument suits you, and that we appear in court on either side.
- What to have with you names a list of assets and debts, super, business or trust interests, expected inheritances, any draft agreement and any divorce order, all things a person in this position plainly holds or knows, states no legal requirement, and keeps the line that having little on paper is fine.

## Fees

Copied from fees.html as the central pass of 9 November 2026 leaves it: binding financial agreement from $3,025 per party including GST, with its scope and "costs more" sentence copied from the row, linked to `/fees#fee-binding-financial-agreement`; advice on a binding financial agreement drafted by the other party from $1,100 including GST, with its scope, linked to the central pass's new row id `/fees#fee-advice-on-a-binding-financial-agreement`. Neither is called a fixed fee, and the schema carries no offers because neither is a single figure. Ending, enforcing or challenging an agreement and court proceedings are estimated in writing.

## The brief asked for six questions; the gate requires five

`playbooks/service-pages.md` and the gate still require exactly five questions, so the page carries five. This spare question was read today and can be added if the limit is raised:

- Q: Can one lawyer act for both of us?
- A: No. Each of you needs independent legal advice before signing, so each of you has your own lawyer, and we act for one of you only.
- Authority: s 90G(1)(b) and s 90UJ(1)(b). That one lawyer cannot advise both is a conduct and independence point rather than words of the Act, so the answer rests on the advice being independent.

## Checks run

- Built with `scripts/build-service-page.py`: 1,933 visible words in `<main>`, including the hub's rail cards.
- `scripts/check_style.py` on the page's visible text: PASS, with notes only for the hub's "!" urgent mark and paragraph shape.
- `scripts/check-publish.py` in this branch: no failure of the page's own. It shares the expected failures from files outside this task, the page limit and the hub link, sitemap and llms.txt entries. In a test copy of the central branch with sitemap and llms.txt entries added, the service page checks pass for this page.
