"""Chrome propagation (8 Sep 2026). Build the practice menus into index.html's header, quieten the header call button and the top bar, add service ids to the hubs,
then copy the top bar and header from index.html to every other page (chrome propagation rule)."""
import re, glob, html
ROOT='/home/user/spencer-alexander-site'
HUBS={'commercial-law':('Commercial Law','All commercial law services'),'family-law':('Family Law','All family law services'),'wills-and-estates':('Wills &amp; Estates','All wills and estates services')}
def slug(t): return re.sub(r'[^a-z0-9]+','-',html.unescape(re.sub('<[^>]+>','',t)).lower()).strip('-')
menus={}
for hub in HUBS:
    p=f'{ROOT}/{hub}.html'; s=open(p).read(); items=[]
    def add_id(m):
        title=re.sub('<[^>]+>','',m.group(2)).strip(); sid='svc-'+slug(title); items.append((sid,title))
        return m.group(1).replace('<div class="svc">', f'<div class="svc" id="{sid}">')+m.group(2)+m.group(3)
    s2=re.sub(r'(<div class="svc">\s*<h3[^>]*>)(.*?)(</h3>)', add_id, s, flags=re.S)
    if s2!=s: open(p,'w').write(s2)
    menus[hub]=items
    print(hub, len(items), 'services')
idx=open(f'{ROOT}/index.html').read()
def group(hub, label, active=False):
    name, allt = HUBS[hub]
    links=''.join(f'\n          <a href="/{hub}#{sid}">{html.escape(t,quote=False)}</a>' for sid,t in menus[hub])
    cls = ' class="is-active"' if active else ''
    return (f'<div class="site-nav__group"><a href="/{hub}"{cls}>{name}</a>\n        <div class="site-nav__menu"><strong>{name}</strong>{links}\n          <a class="site-nav__all" href="/{hub}">{allt}</a>\n        </div></div>')
old_nav=re.search(r'<nav class="site-nav" aria-label="Primary">.*?</nav>', idx, re.S).group(0)
new_nav=('<nav class="site-nav" aria-label="Primary">\n        '+group('family-law','')+'\n        '+group('wills-and-estates','')+'\n        '+group('commercial-law','')+
         '\n        <a href="/insights">Insights</a>\n        <a href="/faq">FAQ</a>\n        <a href="/about">About</a>\n        <a href="/contact">Contact</a>\n      </nav>')
idx=idx.replace(old_nav,new_nav)
idx=idx.replace('<a class="btn btn--primary" href="tel:+61391258355">','<a class="btn btn--outline" href="tel:+61391258355">',1)
idx=idx.replace('        <a class="topbar__tel" href="tel:+61391258355">(03) 9125 8355</a>\n','',1)
open(f'{ROOT}/index.html','w').write(idx)
# propagate: the top bar and header blocks, marking the active link per page
top=re.search(r'<div class="topbar">.*?</div>\s*</div>\s*</div>', idx, re.S)
hdr=re.search(r'<header class="site-header">.*?</header>', idx, re.S).group(0)
tb=re.search(r'<div class="topbar".*?</header>', idx, re.S).group(0)   # top bar through header end
count=0
import os
SKIP_ARTICLES = os.environ.get('SKIP_ARTICLES') == '1'
for p in sorted(glob.glob(f'{ROOT}/*.html')):
    if p.endswith('/index.html'): continue
    if SKIP_ARTICLES and os.path.basename(p).startswith('insight-'): continue
    s=open(p).read(); m=re.search(r'<div class="topbar".*?</header>', s, re.S)
    if not m: print('no chrome in', p); continue
    page=p.split('/')[-1][:-5]
    block=tb.replace(' class="is-active"','')
    active={'commercial-law':'/commercial-law','family-law':'/family-law','wills-and-estates':'/wills-and-estates','insights':'/insights','faq':'/faq','about':'/about','contact':'/contact'}
    href=active.get(page) or ('/insights' if page.startswith('insight-') or page.startswith('resource') else None)
    if href:
        block=block.replace(f'<a href="{href}">', f'<a href="{href}" class="is-active">',1)
    s=s[:m.start()]+block+s[m.end():]; open(p,'w').write(s); count+=1
print('header propagated to', count, 'pages')
