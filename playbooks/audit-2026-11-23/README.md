# Audit of 23 November 2026

Spencer asked for the site to be audited and improved for design, usability, search, AI answers, acquisition and
conversion, and for the fees that changed in the recent pricing release to go back to the amounts published
immediately before it. Later the same day he asked that everything the audit supports be implemented as well. The
work is on the branch `claude/affectionate-einstein-xytjjz`, as one commit, and nothing here is live until it is
released. The report he reads is a private page, and its address is kept with the private part of the record.

## What is in this folder

- acceptance-tests.md: the ten tests, written before any change, that the signoff table in the report answers.
- baseline.md: what was live on 23 November 2026, with the lab and accessibility figures taken before the first edit.
- fees.md: every fee's history from the deployment record, the decision table, the scope of the restored fees, the
  court and government charges as read, and where the restored fees sit in the market.
- fees-full-earlier-schedule.json: the totals of all 24 fees as published from 9 to 16 November 2026.
  `python3 scripts/fees.py use playbooks/audit-2026-11-23/fees-full-earlier-schedule.json` puts them all back.
- changes.md: what the preview changes, with every change a visitor can see set out for Spencer's approval.
- release-message.txt: the commit message for the release, which step 5 below uses.
- article-proposals.md: the eight article topics now in the backlog, why they were chosen, and one service page the
  evidence supports that waits for his approval because the cap is twelve.

This repository is public. The parts of the record that are about the business are kept in the private business
development repository at `audits/2026-11-23/`, with the research files.

## Release

One release, as a single commit on main, on Spencer's word.

1. Bring main into the branch: `git fetch origin main`, then `git merge origin/main` on the branch. If main has not
   moved since 23 November 2026 there is nothing to merge. If a routine has run, keep the later date wherever both
   sides changed one, and keep both DECISIONS.md entries with the newest first. In `scripts/content-backlog.md`
   keep main's rows, then add the branch's rows 13 to 20 and its change to row 3 again, and correct the company
   registration row if it still quotes a figure. An article published since then needs four things by hand, and
   the gate fails until each is done: the stylesheet and script keys v25 and v19, the rail card's closing line as
   `_article-template.html` has it, its Article schema wordCount set to the count the gate prints, and any fee it
   quotes changed to the amount in `playbooks/fees.json`, because it was written from the amounts then live. Then
   run `python3 scripts/fees.py check`. If it reports a sentence as new, read it against
   `playbooks/fees.json` and run `python3 scripts/fees.py snapshot`.
2. Date the pages: `python3 scripts/fees.py stamp YYYY-MM-DD --since origin/main` with the day of release in
   Melbourne. It moves the pages whose own words changed and no others. In a month after November 2026 it stops and
   names the pages whose law must be read again first.
3. Run `python3 scripts/check-publish.py`. Every check must pass.
4. Commit whatever the merge and the stamp changed on the branch, so the working tree is clean. With main unmoved
   and the day still 23 November 2026 there is nothing to commit.
5. Publish as one commit: `git checkout -B main origin/main`, `git merge --squash claude/affectionate-einstein-xytjjz`
   and `git commit -F playbooks/audit-2026-11-23/release-message.txt`, which is the message for the release.
   Run `python3 scripts/check-publish.py` again on main, and only when every check passes
   `git push origin HEAD:main`.
6. Run `python3 scripts/indexnow.py` with the .html path of every page that changed, which
   `git diff --name-only HEAD~1 HEAD -- '*.html' ':(exclude)_*' ':(exclude)404.html' ':(exclude)thank-you*.html'` lists on main after the
   release commit, leaving out the template and the pages that are not indexed, and ask Google to index the fees
   page and the probate page in Search Console.
7. The same day, through Chrome on the Mac mini: on the Business Profile set probate and letters of administration to
   From $1,980 and property settlement to From $3,025, and read each priced service's description for a total that
   has changed, being letters of administration $2,178, wills for a couple $880, property and parenting together
   $3,850 and advice on a financial agreement from $1,100. Copy the Firm Register's Fees tab from the new page.
8. Merge the same branch of the business development repository into its main, so that the Saturday scoreboard
   starts the new counts.
9. Spencer sends one enquiry through the live form with his own details and confirms one notification arrives. No
   session can make that check.

To undo the whole release, run `git revert` on the release commit and push. To undo the six fees alone, set their
totals back in `playbooks/fees.json` and run `python3 scripts/fees.py apply`. From 1 December 2026 apply stops until
the law on the pages that quote those fees has been read again and `--law-read` is given, because a page's date and
the month its law was read move together.

The effect of the six fees cannot be read apart from the effect of the page changes when both are released together.
To read the fees alone, release with the six totals left at the amounts live on 23 November 2026 and restore them
later with one edit to `playbooks/fees.json` and `python3 scripts/fees.py apply`. Inside November 2026 that is all it
takes. From 1 December 2026 it also takes the reading described above, of about eighteen pages, so a restoration a
fortnight after release carries that cost.

apply is for a change meant to stand. A price tried and then changed back through apply returns every figure but
leaves each page that quotes it dated the day of the trial, so a trial that was never published is dropped with
`git checkout`.

After release the three weekly routines run against the new gate. The Monday routine dates a hub with
`python3 scripts/fees.py stamp` and the hub's file name once it has added its link, which moves the hub's day and
leaves the month its law was read, and that was rehearsed with the clock at 7 and 14 December 2026 and 4 January 2027.
A new article that quotes a fee is reported by the fee check until its sentence has been read and recorded with
`python3 scripts/fees.py snapshot`, and so is any fee sentence whose paragraph, heading or question a routine changes.
