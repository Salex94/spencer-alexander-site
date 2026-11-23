# What the preview changes, 23 November 2026

Everything here is on the branch and nothing is live. Changes that alter how a page looks are marked, because
Spencer's rule of 26 September 2026 is that those need his approval, and the release is where he gives it.

## Fees

- Six fees are back at the amounts published from 9 to 16 November 2026: probate application $1,980, letters of
  administration $2,178, wills for a couple $880, consent orders for an agreed property settlement $3,025, consent
  orders for property and parenting together $3,850 and advice on a binding financial agreement the other party
  drafted from $1,100. Each row is byte for byte the row deployed that week. The other eighteen are unchanged.
- `playbooks/fees.json` is now the one source of every fee, and `scripts/fees.py` keeps every rendition in step with
  it. The gate runs its check.
- `playbooks/fees-renditions.json` records every sentence that quotes a fee or a charge, with each figure tied to its
  fee. The check fails a sentence that is new, changed or gone until someone has read it and recorded it.
- The fees page publishes what the Supreme Court, the Federal Circuit and Family Court and ASIC charge, with the day
  each was read, and the pages that quote a fee quote the charge that adds to it.

## Changes a visitor can see

| Where | Change | Why |
|---|---|---|
| Fees page | Four prices in the hero, above the two buttons | A phone visitor met three screens of introduction before the first price |
| Fees page | A band listing every fee at a glance, one short row each, with per person or per party where it applies | The same. It replaces the three jump links the hero carried, and each column heading links to its section |
| Fees page | A table of court and ASIC charges, and one worked total | An executor could not total the cost of probate from any page |
| Fees page | A note under the probate row naming the Court's separate filing fee, and a note under each estate plan giving what its documents come to bought separately | The reviewer's executor stalled at the probate row. The comparison is the page's own prices added up |
| Fees page | The lead opens with one sentence: whose fees these are, where, in Australian dollars, as at what day, who published them and where | Two answer engines quoted a price from before 9 November, and one gave a fee in American dollars |
| Service pages | Each fee note opens with the same sentence and the page's date, each answer that quotes one of the firm's fees carries it straight after those fees, and each page closes with who published it and when | The same. An answer is the passage most often lifted for a question about cost |
| Family hub, wills hub and the FAQ page | The five answers to questions about cost end with the same sentence | The same |
| Hubs | Each ends its questions with a Sources line and a closing line, in the service pages' form | The hubs stated law with no source and no date |
| Hubs | The In brief block ends with one line: Published by Spencer Alexander, Principal, the day the page was updated and, after the word Legislation, the Acts the block rests on | A summary quoted by itself named no publisher, date or source, and the service pages' summaries already end this way |
| Home page | One line under the rating: fixed fees are published in full, with two of them | The first screen said nothing of the firm's clearest difference |
| Home page, tablets | From 768 to 900 pixels the hero sets its text beside the portrait | The portrait stacked beneath the text with half the width empty |
| Hubs and service pages, phones | Service descriptions, the fee note and the time limit cards are 16 pixels in place of 14 | Four of five local firms set this text at 16 to 18 |
| Hubs, service pages and the FAQ page, desktops | Running text, the In brief summary and the answers keep to about 62 to 84 characters a line. The fee note is 16 pixels at every size and keeps the same measure, where it was 14 pixels and ran to about 115 characters | Lines ran to 92 characters in the text and 123 in the answers |
| Every page, phones | The call bar stays until the hero's call button is wholly on screen | On two pages a cut off button showed with no bar |
| Every page, narrow phones | The header and footer wordmarks scale below 400 pixels | The menu button was cut off at 320 pixels, and so was the footer wordmark |
| Every page | The word Lawyers under the wordmark is brass 800 | It measured 4.49 to 1 against the 4.5 the standard asks |
| Rail cards and the fees page | Enquiries are answered within one business day | Sixteen of eighteen high intent pages did not say how soon a reply comes |
| Family hub | The urgent strip names 1800RESPECT, and both numbers can be tapped | It named 000 and the firm alone, as plain text |
| Family pages | A sentence beside the closing buttons says the form lets a visitor choose how it is safe to be contacted | No family page said so before the form |
| Contact page | The Quick exit, as on the family pages | It is where a family law visitor types a name and a number |
| Contact form | The button says Sending your enquiry and ignores a second press, and frees itself after twenty seconds with the number to call | A second press on a slow connection sent the enquiry twice |
| Service pages | Each In brief summary ends with who published the page, the day it was updated and the legislation it cites | A summary quoted by itself named its Act and its court but not its author, date or source |
| The three hubs, the FAQ page and five service pages | Sentences that state a rule name their Act, court or State, such as In Victoria on the wills hub and Under the Corporations Act 2001 (Cth) on the statutory demand answers | An engine placed a statutory demand under British law and a Victorian rule in no State at all |
| Probate, divorce, property, parenting and shareholder pages, the probate article, the executor checklist and one FAQ answer | The court or ASIC charge is quoted beside the fee it adds to, with one worked total of $3,068 on the probate page and the article | No page let a reader total the cost |
| Shareholder agreements page | The fee note says that where a company falls outside the description the first call says so and the fee is confirmed in writing | Nothing said what happens when a company does not fit the price |
| Probate article | Two sentences on how long a grant and an estate take are reworded so the two periods cannot be merged, and the article shows it was updated on the day | An engine merged them into one figure the firm never gave |
| Seven service pages | The urgent strip opens with the name of its Act, such as Under the Administration and Probate Act 1958 (Vic) | A time limit lifted by itself did not say whose law it was, and these limits differ between States |
| Divorce page | The fee note and four answers name the Federal Circuit and Family Court of Australia where they said the Court | An answer lifted by itself did not say which court |
| Divorce, parenting and property pages | The Court's filing fee is given as the amount under the Commonwealth's notice of family law fees | The passage gave the figure without saying where it is published |
| Shareholder agreements page | The answer about cost gives the firm's two fees first and ASIC's fee after them | The sentence that dates the firm's fees must not be read as covering ASIC's |
| Shareholder agreements page | The line under the hero buttons gives the shareholder agreement fee, from $1,095, where it gave the company set up fee | The page is about shareholder agreements, and the line gave another service's fee |
| Home page and contact page | The step about fees adds that the fees page says what each fee covers and what costs more | The step sent a reader to the fees page without saying what is there |
| Commercial hub | Its search description opens Commercial and small business lawyers, and no longer lists disputes | Small business is how owners search for this work, and the description must fit in 160 characters |
| Home page, phones under 360 pixels | The long call button under How we work wraps onto two lines | Its label hung outside the button |
| Home page film | A caption track that a visitor can switch on in the player's own controls while the film plays. Nothing shows unless it is switched on | Speech in a film with no captions fails a level A accessibility rule. Spencer removed an earlier caption track on 6 September 2026 because the captions then showed, so this one is for him to keep or strike |
| Wills hub | The sentence that gives the $495 fee names the enduring power of attorney and the appointment of a medical treatment decision maker | It read Each document, straight after a sentence about an advance care directive, which has no fixed fee |
| Powers of attorney page, wills page and the powers of attorney article | Four sentences give the power of attorney and the medical appointment a figure each | They said one fee was the same as the other, which a change to either price would have left untrue |

## Changes a visitor cannot see

- Keyboard focus no longer lands under the sticky header or on a block that has yet to fade in, and a call bar
  control that takes focus comes back into view.
- The powers of attorney page says the regulations prescribe the form, which is what the law says.
- The contact page's schema carries the ABN. Four Article nodes carry a correct word count.
- The gate has 113 checks where it had 106: the fee check, the notice on the yearly charges, the currency line on
  every page, the word count, the stylesheet and script keys on every page, the rail card's closing line, and each
  hub's closing line, whose day follows the page's date and whose month for its law is no later.

## How it was checked

A reviewer who had not made the changes tested the preview and reported faults in keyboard focus, in the form's
new lock, in the reply time missing from sixteen pages, in the first screen of the fees page on short phones, in
the footer at 320 pixels and in the fee check itself. Two further passes tested the fee history, every rendition,
the fee tool, the wording and the law in each changed sentence. Each fault confirmed is fixed in the preview, and
the reviewer's own tests were run again against the result. A final pass then tried the release and the fee tool
end to end. It found that the tool confused two fees once they shared an amount, so that the whole earlier schedule
would not apply, that the release steps failed as written, and that next year's court charges could be published
early. The tool now takes each figure's tie from the record of sentences, and records a sentence with its paragraph
where the fee is named only there. The earlier schedule applies and returns with the gate passing each way, and the
steps were corrected. What the checks could not settle is in the report.
