#!/usr/bin/env python3
"""Package the existing static site for a private design review.

Production remains GitHub Pages from the repository root. Only dist receives
preview indexing protection and a non-sending enquiry form.
"""
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'dist'
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()

for path in ROOT.glob('*.html'):
    if path.name.startswith('_'):
        continue
    text = path.read_text()
    text = re.sub(r'<meta name="robots" content="[^"]+">',
                  '<meta name="robots" content="noindex, nofollow">', text)
    if path.name == 'contact.html':
        text = text.replace('<form class="form"', '<p class="preview-notice" role="note">Design preview: enquiries entered here are not sent.</p>\n            <form class="form"')
        text = text.replace('action="https://formsubmit.co/contact@spenceralexander.com.au"', 'action="/thank-you"')
        text = text.replace('<script src="scripts/site.js?v=11"></script>', '<script src="scripts/site.js?v=11"></script>\n  <script src="scripts/preview.js"></script>')
        # POST keeps any values out of URLs even in a script-disabled browser.
        # This static preview has no POST handler and no connection to FormSubmit.
    elif path.name == 'thank-you.html':
        text = text.replace("Thank you, we'll be in touch.", 'This is a design preview.')
        text = re.sub(r'(<p class="cta__lead">).*?(</p>)', r'\1No enquiry was sent from this preview. To contact the firm, please use the live website or call (03) 9125 8355.\2', text, count=1, flags=re.S)
    (OUT / path.name).write_text(text)

for directory in ['styles', 'assets']:
    shutil.copytree(ROOT / directory, OUT / directory)
(OUT / 'scripts').mkdir()
for filename in ['site.js', 'image-slot.js']:
    shutil.copy2(ROOT / 'scripts' / filename, OUT / 'scripts' / filename)
for filename in ['sitemap.xml', 'feed.xml', 'llms.txt']:
    shutil.copy2(ROOT / filename, OUT / filename)
(OUT / 'robots.txt').write_text('User-agent: *\nDisallow: /\n')
(OUT / '_headers').write_text('/*\n  X-Robots-Tag: noindex, nofollow\n')
(OUT / 'scripts' / 'preview.js').write_text('''(function () {
  var form = document.querySelector("[data-enquiry-form]");
  if (!form) return;
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var note = document.querySelector(".preview-notice");
    note.textContent = "This is a design preview. Your enquiry has not been sent.";
    note.setAttribute("role", "status");
    note.setAttribute("tabindex", "-1");
    note.focus();
  });
})();
''')
with (OUT / 'styles' / 'site.css').open('a') as css:
    css.write('\n.preview-notice { padding: 12px 16px; margin-bottom: 20px; background: #f0ece4; border-left: 2px solid #977540; color: #542c39; font-size: .875rem; line-height: 1.5; }\n')
print('Private preview built in dist. Production form and indexing settings are unchanged.')
