#!/usr/bin/env python3
"""Regression checks for accessible navigation, enquiry routing and article metadata.

Run alongside check-publish.py. No third-party packages are required.
"""
from html.parser import HTMLParser
from html import unescape
from pathlib import Path
from urllib.parse import urlsplit, unquote, unquote_plus
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
BASE = 'https://www.spenceralexander.com.au/'
failures = []
checks = 0


def check(condition, message):
    global checks
    checks += 1
    if not condition:
        failures.append(message)


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.elements = []
        self.ids = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        keys = [key for key, _ in attrs]
        check(len(set(keys)) == len(keys), 'Duplicate attributes on ' + tag)
        attrs = dict(attrs)
        self.elements.append((tag, attrs))
        if 'id' in attrs:
            self.ids.append(attrs['id'])

    def matching(self, tag, **attrs):
        return [element for name, element in self.elements
                if name == tag and all(element.get(key) == value for key, value in attrs.items())]


pages = {p.name: (p.read_text(), Page(p.read_text())) for p in ROOT.glob('*.html')
         if not p.name.startswith('_')}
titles = []
descriptions = []
lastmods = {}
for node in ET.parse(ROOT / 'sitemap.xml').getroot():
    lastmods[node.find('{*}loc').text] = node.find('{*}lastmod').text

for filename, (text, page) in pages.items():
    check(len(page.ids) == len(set(page.ids)), filename + ': duplicate IDs')
    check(len(page.matching('h1')) == 1, filename + ': exactly one primary heading')
    check(len(page.matching('nav', **{'class': 'mobile-contact'})) == 1,
          filename + ': mobile call and enquiry navigation missing')
    check('js-reveal' not in (ROOT / 'scripts/site.js').read_text(), 'Content must appear without reveal delays')
    for link in page.matching('a'):
        href = link.get('href', '')
        parts = urlsplit(href)
        if parts.scheme or parts.netloc or not parts.fragment:
            continue
        target = parts.path.strip('/')
        target = (target if target.endswith('.html') else target + '.html') if target else filename
        if parts.path == '/':
            target = 'index.html'
        check(target in pages and unquote(parts.fragment) in pages[target][1].ids,
              filename + ': unresolved anchor ' + href)
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S):
        try:
            data = json.loads(block)
        except ValueError as error:
            check(False, filename + ': invalid JSON-LD ' + str(error))
            continue
        if data.get('@type') == 'Article':
            check(data['dateModified'] == lastmods.get(data['mainEntityOfPage']), filename + ': article and sitemap dates differ')
            check(data['image'].startswith(BASE + 'assets/'), filename + ': article sharing image must be hosted by the firm')
            for attr, kind in [('og:image', 'property'), ('twitter:image', 'name')]:
                tags = page.matching('meta', **{kind: attr})
                check(len(tags) == 1 and tags[0].get('content') == data['image'], filename + ': sharing images disagree')
    if filename.startswith('insight-'):
        for class_name in ['article-answer', 'article-toc', 'article-sources']:
            check(any(class_name in attrs.get('class', '').split() for _, attrs in page.elements), filename + ': missing ' + class_name)
        refs = re.search(r'<section class="article-sources".*?</section>', text, re.S)
        check(bool(refs and 'href="https://' in refs[0]), filename + ': official references missing')
        check('href="/contact?matter=' in text, filename + ': service context not passed to enquiry')
    robots = page.matching('meta', name='robots')
    if robots and 'noindex' not in robots[0].get('content', ''):
        title = re.search(r'<title>(.*?)</title>', text, re.S)[1]
        description = page.matching('meta', name='description')[0]['content']
        titles.append(title)
        descriptions.append(description)

# Owner's visible-copy policy. Accurate location metadata and llms.txt remain allowed.
def check_address_nodes(node, filename):
    if isinstance(node, dict):
        if node.get('addressLocality') == 'Box Hill':
            check(node.get('@type') == 'PostalAddress' and
                  all(node.get(key) for key in ['streetAddress', 'addressRegion', 'postalCode', 'addressCountry']),
                  filename + ': locality must belong to a complete PostalAddress')
        for value in node.values():
            check_address_nodes(value, filename)
    elif isinstance(node, list):
        for value in node:
            check_address_nodes(value, filename)

for path in list(ROOT.glob('*.html')) + [ROOT / 'llms.txt']:
    source = path.read_text()
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.S):
        check_address_nodes(json.loads(block), path.name)
    if path.suffix == '.html':
        # Check rendered copy, links and image alternatives; search metadata is
        # deliberately excluded by the owner's subsequent SEO/GEO clarification.
        body = re.search(r'<body\b[^>]*>(.*?)</body>', source, re.S)[1]
        body = re.sub(r'<script\b[^>]*>.*?</script>', '', body, flags=re.S)
        normalized = unquote_plus(unescape(body))
        normalized = re.sub(r'<br\s*/?>', ' ', normalized, flags=re.I)
        normalized = re.sub(r'Suite\s+10\s*,?\s*1\s+Main\s+Street\s*,?\s*Box\s+Hill\s+VIC\s+3128', '', normalized, flags=re.I)
        check(not re.search(r'box[\s+]+hill', normalized, re.I), path.name + ': visible Box Hill reference outside a full address')
    for phrase in ['Personal advice from Spencer Alexander', 'Direct access to the principal throughout',
                   'with the principal handling every matter', 'You deal with the principal',
                   'Clients speak directly with the principal', "published under the principal's name"]:
        check(phrase not in source, path.name + ': retired personal-practice promise: ' + phrase)

check(len(titles) == len(set(titles)), 'Indexable pages must have unique titles')
check(len(descriptions) == len(set(descriptions)), 'Indexable pages must have unique descriptions')
contact = pages['contact.html'][1]
forms = contact.matching('form', name='contact')
check(len(forms) == 1, 'Exactly one contact form')
check(forms[0].get('method', '').upper() == 'POST', 'Enquiries must use POST')
check(forms[0].get('action') == 'https://formsubmit.co/contact@spenceralexander.com.au', 'Production delivery endpoint changed')
check(contact.matching('input', name='_next')[0]['value'] == BASE + 'thank-you', 'Production confirmation URL changed')
for field in ['name', 'email', 'message']:
    inputs = contact.matching('textarea' if field == 'message' else 'input', name=field)
    check(len(inputs) == 1 and 'required' in inputs[0], 'Missing required enquiry field: ' + field)
    check(bool(contact.matching('label', **{'for': inputs[0]['id']})), 'Unlabelled field: ' + field)
check(bool(contact.matching('input', name='_honey')), 'Honeypot missing')
check('required' not in contact.matching('input', name='phone')[0], 'Phone should be optional for email replies')
check(bool(contact.matching('select', name='contact_preference')), 'Reply preference missing')

preview = ROOT / 'dist'
if preview.exists():
    for path in preview.glob('*.html'):
        check('content="noindex, nofollow"' in path.read_text(), path.name + ': preview indexing is enabled')
    preview_contact = (preview / 'contact.html').read_text()
    check('formsubmit.co' not in preview_contact, 'Preview must not send enquiries to production')
    check('method="GET"' not in preview_contact, 'Enquiry details must not be put into preview URLs')
    check(not (preview / 'CLAUDE.md').exists(), 'Private operating instructions included in public assets')

if failures:
    print('\n'.join('FAIL: ' + message for message in failures))
    print(f'{len(failures)} failures in {checks} checks')
    sys.exit(1)
print(f'PASS: {checks} checks across {len(pages)} pages, including 28 articles and the enquiry form.')
