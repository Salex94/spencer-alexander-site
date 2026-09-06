# September 2026 design review

This branch strengthens the visual hierarchy and the path to a first enquiry.
The production site continues to deploy through GitHub Pages after a reviewed
merge to main. The Sites project is an owner-private design preview.

## What changed

- A firm-centred opening, an arched portrait frame, three immediate practice
  links, warm typography and clear call and enquiry actions.
- Editorial practice-area rows, larger client quotations, a firm-wide approach
  statement and an asymmetric closing invitation. Shared reading pages retain
  clear typography and restrained styling.
- Melbourne positioning across all public pages and search/AI metadata. Box
  Hill remains only in full physical address contexts and PostalAddress data.
- Firm-centred we/our copy across the home, About, service and contact pages,
  article enquiry rails, FAQ, shared footer and future article template. Genuine
  personal biography, author identity, video transcript and client quotes remain.
- A contact form alongside the introduction on desktop, persistent call and
  enquiry actions on phones, and a reply preference with optional phone entry
  for visitors who prefer email. Service links preselect the relevant matter.
- Original article introductions presented as summaries, accessible static
  section navigation, and relevant official references across all 28 guides.
- First-party article images in social and Article metadata. Existing canonical
  URLs, legal copy, author identity, published dates and entity identifiers are
  preserved. Modification dates reflect this edit.
- Immediate content display, keyboard Escape support for the mobile menu,
  consistent focus states, reduced-motion support and updated article templates.

The existing first-call promise, client quotations, rating without a review
count, fee wording, video and verified firm details remain in place. The added
reference lists are useful further reading. They are not a representation that
this design pass independently reverified every existing legal proposition.

## Review and validation

Run these before merging:

```sh
python3 scripts/check-publish.py
python3 scripts/check-article-images.py
python3 scripts/check-design.py
```

The additional checks cover article and sitemap dates, social images, section
anchors, unique page metadata, labelled enquiry fields, service context and
preview isolation, firm positioning and full-address-only locality references.
They complement the existing publishing gate.

For a local production-behaviour preview, run `python3 scripts/serve.py` and
visit `http://127.0.0.1:4173/`. This serves the production form, so do not send
dummy enquiries. For the owner-private hosted design review, run
`python3 scripts/build-preview.py` before using the Sites packaging helper.
Only the generated `dist` copy has indexing disabled and enquiry submission
disconnected. Do not copy these preview-only settings into production HTML.

No browser automation or form delivery test was performed during this design
pass. Review the homepage, a practice page, an article and the contact page on
desktop and a phone before merging. Actual conversion improvement needs traffic
and enquiry data; search rankings and AI citations cannot be established from
source changes alone.

## Measurement handoff

The site emits optional `sa:conversion` browser events with only an action and
page pathname: `call_click`, `enquiry_click`, and `enquiry_submit_attempt`.
The hook does not send network requests, store visitor data, or include form
values or query strings. No analytics provider is configured by this branch.
A submission attempt is not a confirmed delivery. Confirmed enquiries must be
measured through the delivery provider or an approved server-side integration.

Search Console, Business Profile, analytics access, verified legal credentials,
and any new testimonials remain separate inputs. Do not invent them or add
tracking identifiers without the owner's account details.
