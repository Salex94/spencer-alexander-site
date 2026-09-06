# September 2026 design review

This branch strengthens the visual hierarchy and the path to a first enquiry.
The production site continues to deploy through GitHub Pages after a reviewed
merge to main. The Sites project is an owner-private design preview.

## What changed

- An ivory editorial homepage with oversized serif typography, restrained wine
  accents and a licensed photograph of Melbourne architecture. The former
  arched portrait and offset border are removed.
- A dedicated firm introduction pairs the principal's real portrait with
  firm-centred copy. Image and caption share the same width and left edge.
- Three clear practice routes, preserved client quotations and video, native
  expandable deadline guidance and a prominent closing enquiry invitation.
- Shared navigation, footer and inner-page mastheads follow the new identity.
- Visible copy uses Melbourne positioning. Accurate Box Hill office details
  remain in full addresses and useful search/AI information.
- The branch retains the improved contact form, mobile call/enquiry actions,
  contextual enquiry links, article summaries, contents links and source lists.
- Canonical URLs, legal author identity and original article publication dates
  remain intact. Metadata and templates follow the current owner instructions.

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
preview isolation, firm positioning and full-address-only visible locality references.
They complement the existing publishing gate.

For a local production-behaviour preview, run `python3 scripts/serve.py` and
visit `http://127.0.0.1:4173/`. This serves the production form, so do not send
dummy enquiries. For the owner-private hosted design review, run
`python3 scripts/build-preview.py` before using the Sites packaging helper.
Only the generated `dist` copy has indexing disabled and enquiry submission
disconnected. Do not copy these preview-only settings into production HTML.

The owner authorised desktop and mobile browser testing for this revision.
The current review includes desktop, tablet and phone layout checks, portrait
alignment and overflow measurements, menu/Escape behaviour, enquiry navigation,
reply-preference validation and native deadline expansion. Real enquiries are
not submitted as part of design testing.

Actual conversion improvement needs traffic and enquiry data; search rankings
and AI citations cannot be established from source changes alone.

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


## Melbourne architecture photograph

The homepage photograph shows Melbourne city architecture, not the firm's office.
It is by Arun Clarke: https://unsplash.com/photos/brown-concrete-building-during-daytime-ErfNar7ScsI
Downloaded from the photographer's official Unsplash image URL on 6 September 2026.
Reuse: Unsplash License, https://unsplash.com/license . Source dimensions: 2000 x 1334.
The image is self-hosted at assets/melbourne-architecture.jpg and uses CSS cropping.
