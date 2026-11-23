# Fees: what was published, what the preview restores, and what it costs

## The finding that changes the instruction

Spencer asked for the fees that changed in the recent pricing release to go back to the amounts published
immediately before it, which he remembered as lower. The deployment record shows that the release of 16 November
2026 raised six fees, lowered fourteen and left four alone. So restoring every changed fee would raise fourteen
prices, which is the opposite of what he asked for.

The preview therefore restores the six fees that rose, each to the exact amount published before the release, and
holds the fourteen that fell at their current lower amounts for his decision. Those six are the fees his
recollection fits: on the scale of 16 November they sat between 1.0 and 3.5 before the release, and the release
took them to 4. The fourteen sat between 4.2 and well above 5, and the release brought them down to 4.

## Where each amount comes from

GitHub Pages publishes main, and every deployment is recorded with its commit and time. The fees page changed at
these deployments, in Melbourne time.

| Schedule | Live from | Live until | Deployment run | Commit |
|---|---|---|---|---|
| First fee list | Saturday 26 September 2026, 2:13am | 28 September, 6:47pm | 36159296801 | 786dbe6 |
| Wills at $495 and $880 | Monday 28 September, 6:47pm | 29 September, 2:04am | 36399456147 | afaacae |
| The six week schedule, every other fee up 10 per cent | Tuesday 29 September, 2:04am | 9 November, 7:55am | 36448180915 | 4db9dfd |
| The audit round | Monday 9 November, 7:55am | 16 November, 10:53am | 42522502449 | 64d83c9, fees unchanged through 759a5e9 |
| Four out of ten, unrounded | Monday 16 November, 10:53am | 16 November, 11:42am | 43777139869 | 1703007 |
| Four out of ten, ending in 95, live now | Monday 16 November, 11:42am | | 43781899293 | dde13d6 |

The schedule immediately before the recent change is the audit round's, read from fees.html at commit 759a5e9. The
Wayback Machine holds no copy of any page of the site, so the repository and the deployment record are the only
dated sources, and they agree.

Two leads from search results were checked. The estate plan for one person was $1,089 until 16 November and is $995
now. Probate was $1,815 until 9 November, $1,980 until 16 November and is $2,295 now. On 23 November 2026 at 2:41pm
the live fees page and the live wills hub both showed $995 and $2,295, and both matched the repository, so the
other figures were old copies held by a search engine and not a fault on the site.

## The decision table

Every amount is the total including GST. Where a price is a from price it was one in every schedule. No scope,
inclusion, exclusion or GST treatment changed between 9 November and today: the scope text of all 24 rows is
identical word for word.

| Service | Live now | 9 to 16 November | 29 September to 9 November | In the preview | What 16 November did | Decision needed |
|---|---|---|---|---|---|---|
| Probate application | $2,295 | $1,980 | $1,815 | $1,980, restored | Raised by $315 | Whether to go further back to $1,815, the six week price |
| Letters of administration | $2,495 | $2,178 | $2,178 | $2,178, restored | Raised by $317 | None |
| Wills for a couple | $895 | $880 | $880 | $880, restored | Raised by $15 | None |
| Consent orders, agreed property settlement | $3,195 | $3,025 | $3,025 | $3,025, restored | Raised by $170 | None |
| Consent orders, property and parenting together | $4,495 | $3,850 | Not offered | $3,850, restored | Raised by $645 | None |
| Advice on a financial agreement the other party drafted | from $1,595 | from $1,100 | Not offered | from $1,100, restored | Raised by $495 | Whether from $1,100 pays for the risk the certificate carries |
| Single will | $495 | $495 | $495 | $495 | Unchanged | None |
| Enduring power of attorney | $495 | $495 | $495 | $495 | Unchanged | None |
| Medical treatment decision maker appointment | $495 | $495 | $495 | $495 | Unchanged | None |
| Letter of demand | $495 | $495 | $495 | $495 | Unchanged | None |
| Estate plan for one person | $995 | $1,089 | $1,089 | $995, held | Lowered by $94 | Keep $995 or return to $1,089 |
| Estate plan for a couple | $1,595 | $1,980 | $1,980 | $1,595, held | Lowered by $385 | Keep or return |
| Will with a testamentary trust, one person | from $1,595 | from $1,650 | from $1,650 | from $1,595, held | Lowered by $55 | Keep or return |
| Wills with testamentary trusts, a couple | from $2,595 | from $3,025 | from $3,025 | from $2,595, held | Lowered by $430 | Keep or return |
| Divorce application, joint | $995 | $1,089 | $1,089 | $995, held | Lowered by $94 | Keep or return |
| Divorce application, sole | $1,095 | $1,452 | $1,452 | $1,095, held | Lowered by $357 | Keep or return |
| Consent orders, agreed parenting arrangements | $2,895 | $3,025 | $3,025 | $2,895, held | Lowered by $130 | Keep or return |
| Parenting plan | from $1,295 | from $1,452 | from $1,452 | from $1,295, held | Lowered by $157 | Keep or return |
| Binding financial agreement | from $2,895 | from $3,025 | from $3,025 | from $2,895, held | Lowered by $130 | Keep or return |
| Lease review for a tenant | from $795 | from $1,089 | from $1,089 | from $795, held | Lowered by $294 | Keep or return |
| Company set up, ASIC's fee at cost | $495 | $660 | $1,210 with ASIC's fee inside | $495, held | Lowered by $165 | Keep or return to $660 |
| Shareholders agreement | from $1,095 | from $2,420 | from $2,420 | from $1,095, held | Lowered by $1,325 | Keep or return |
| Terms of trade | from $1,195 | from $1,815 | from $1,815 | from $1,195, held | Lowered by $620 | Keep or return |
| Review of a contract to buy a business | from $895 | from $1,210 | from $1,210 | from $895, held | Lowered by $315 | Keep or return |

Each restored row on the preview's fees page is byte for byte the row deployed from 9 to 16 November, and the other
eighteen rows are byte for byte the rows on main. The full earlier schedule, with all twenty changed fees at their
9 to 16 November amounts, is in fees-full-earlier-schedule.json as a list of totals. `python3 scripts/fees.py use`
with that file puts every total into the fee source and applies it. It was applied in a scratch copy, where the gate
passed and every sentence that existed that week carried that week's figures.

## Scope, GST and extras of the six restored fees

| Service | Fixed or from | GST | What the fee includes | What is extra |
|---|---|---|---|---|
| Probate application | Fixed | Included. $1,800 plus GST | A straightforward estate: preparing and filing the application, publishing the notice of intention to apply and paying its $38 fee, the Probate Office's routine questions and the grant | The Supreme Court's filing fee, by the value of the assets in Victoria. Administration after the grant |
| Letters of administration | Fixed | Included. $1,980 plus GST | Everything in the probate fee, plus working out who is entitled and obtaining consents, where nobody disputes who inherits and no surety guarantee is required | The same |
| Wills for a couple | Fixed | Included. $800 plus GST | Two wills that mirror each other, on the single will's terms | Nothing |
| Consent orders, property | Fixed | Included. $2,750 plus GST | Advice, the application and proposed orders, one super split and one property transfer, the notice to the fund, filing and the sealed orders | The Court's $215 filing fee, paid to the Court. A company, trust or business |
| Consent orders, property and parenting | Fixed | Included. $3,500 plus GST | One application covering both, on the assumptions of each | The Court's $215 filing fee |
| Advice on an agreement the other party drafted | From | Included. From $1,000 plus GST | Per party: review, the advice the law requires, a meeting and the certificate | Negotiating changes. A business, company or trust |

## Court and government charges, checked on 23 November 2026

The probate fee has included the notice fee since the first fee list of 26 September, so the only compulsory charge inside any restored
package is that $38. It was $38 when the earlier price was published and is $38 now, so the restored total is
unaffected.

| Charge | Amount from 1 July 2026 | Source read on 23 November 2026 |
|---|---|---|
| Supreme Court, notice of intention to apply | $38 | The Court's Probate Office fee list, item 4.1 |
| Supreme Court, filing for a grant, assets in Victoria under $250,000 | No fee | The same list, item 4.2 |
| $250,000 to under $500,000 | $544 | The same |
| $500,000 to under $1 million | $1,088 | The same |
| $1 million to under $2 million | $2,538.70 | The same |
| $2 million to under $3 million | $5,077.40 | The same |
| $3 million to under $5 million | $7,598.80 | The same |
| $5 million to under $7 million | $12,693.40 | The same |
| $7 million or more | $17,770.80 | The same |
| Federal Circuit and Family Court, divorce application | $1,170, or $390 at the reduced fee | Commonwealth gazette notice C2026G00343 |
| Federal Circuit and Family Court, application for consent orders | $215 | The same notice |
| ASIC, registering a proprietary company | $636 | ASIC's fee list |

The Court's own website could not be reached for the family law fees, so they rest on the gazette notice, which the
Family Court of Western Australia's live page and an archived copy of the Court's page of 12 November 2026 match.
The preview now publishes these charges on the fees page and beside the fees they add to.

## Where the restored fees sit in the market

The survey of 16 November 2026 was read again on 23 November. All 53 prices for these six services were re-read on
the firms' own pages and none had moved. One figure was wrong when recorded: Spirit Legal publishes from $1,800 and
not $1,500, for probate and for letters of administration alike, which lifts the probate average by $27 and the
administration average by $37.50 to $2,856.75. Two firms with Melbourne offices were missed, Gathered Here Legal at
$1,798 plus GST for either grant and Jarrah Legal at $990 plus GST for the advice. With those two counted, four out
of ten would be $2,486.98 for letters of administration and $1,554.30 for the advice, a little under the live $2,495
and from $1,595, so on a survey that includes them the two live fees sit just above four out of ten.

| Service | Firms | Average | Restored fee | Share of average | On the 16 November scale | On the 9 November scale | Rank among surveyed firms |
|---|---|---|---|---|---|---|---|
| Probate application | 11 | $2,580.73 | $1,980 | 77 per cent | 2.7 | 3.8 | 7th cheapest of 12 |
| Letters of administration | 8 | $2,819.25 | $2,178 | 77 per cent | 2.7 | 3.9 | 5th of 9 |
| Wills for a couple | 15 | $1,062.33 | $880 | 83 per cent | 3.3 | 4.1 | Equal 6th of 16 |
| Consent orders, property | 9 | $3,580.00 | $3,025 | 84 per cent | 3.4 | 4.2 | 5th of 10 |
| Consent orders, property and parenting | 4 | $5,087.50 | $3,850 | 76 per cent | 2.6 | 3.8 | Equal 2nd of 5 |
| Advice on an agreement | 6 | $1,833.33 | from $1,100 | 60 per cent | 1.0 | 3.0 | Equal 2nd of 7 |
| Single will, unchanged | 23 | $581.91 | $495 | 85 per cent | 3.5 | 4.3 | 11th of 24 |

Three scores have been in use. The audit of 9 November 2026 defined two: a rank, which is a fee's percentile among
the published prices divided by ten, and a scale with the average at 5 and the dearest price at 10. On 16 November
Spencer defined four out of ten as the average less 10 per cent, so each point is a tenth of the average and 3.5 is
85 per cent of it. The column headed 16 November scale uses that definition and the 16 November survey. The column
headed 9 November scale is five times the fee over the same 16 November average, so it differs from the 9 November
record's own table, which worked on its own survey and printed 4.3 for letters of administration, 4.4 for property
and parenting together and 3.4 for the advice. On rank, the 16 November survey puts the restored probate and
administration fees at the 52nd and 50th percentiles. Probate at $1,815 scored 3.6 on the 9 November scale in that
survey, which is the price his recollection of roughly 3.5 fits best.

The strongest market fact is about probate. Three national online services publish a Victorian grant at $1,980,
$1,999 and $1,798 plus GST, each with government fees on top. Counting the notice fee, they come to between $2,016
and $2,037. The restored $1,980, which includes the notice fee, is a little under all three. The current $2,295 is
about $260 to $280 above them. No other firm found in Box Hill, Doncaster, Blackburn, Ringwood, Camberwell or Glen
Waverley publishes a probate fee at all.

Cheaper online offers exist as well. Making Probate Easy publishes $1,100 for either grant, and Victoria Probate an
assisted grant at $1,100 including GST in which the client files and pays for the notice. Safewill and Bare, at
$1,980 and $1,999, price letters of administration the same as probate, so with the notice fee they come to $2,018
and $2,037, and the restored $2,178 for letters of administration is $141 to $160 above them.

## The fourteen held fees

Holding these keeps nine of the fourteen at the lowest amount the firm has published. Five were lower in the first
fee list, live from 26 to 29 September 2026: the estate plan for one person and the joint divorce application at
$990, the will with a testamentary trust for one person from $1,500, and parenting consent orders and the binding
financial agreement at $2,750 and from $2,750. Returning any of the fourteen to its amount of 9 to 16 November 2026
is a change of one total in `playbooks/fees.json`, and the whole of that schedule is in
fees-full-earlier-schedule.json.

The economics of the restoration are kept in the private business development repository at
`audits/2026-11-23/fee-economics.md`, and in the report.

## What changes off the site on release

The preview changes nothing outside the repository. On the day the restored fees are published, the Business
Profile's services need the same amounts, being probate and letters of administration from $1,980 and property
settlement from $3,025, and the Firm Register's Fees tab needs copying from the new page. The four out of ten rule
in CLAUDE.md, the pricing skill and the Growth desk's monthly recheck would otherwise put the six fees back up, so
the rule needs an exception for them, which the preview's CLAUDE.md records.
