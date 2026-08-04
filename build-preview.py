#!/usr/bin/env python3
"""Fakes the Jekyll build well enough to eyeball the design in a browser.
Not used by the published site. Inlines the CSS and images so each page is a
single self-contained file."""
import base64, os, re, sys, yaml

SITE = '.'; OUT = '_preview'
cfg = yaml.safe_load(open(f'{SITE}/_config.yml'))
layout = open(f'{SITE}/_layouts/default.html').read()
css = open(f'{SITE}/assets/css/main.css').read()

def datauri(path, mime):
    return f'data:{mime};base64,' + base64.b64encode(open(path,'rb').read()).decode()
MARK = datauri(f'{SITE}/assets/img/ches-mark.png', 'image/png')
ICON = datauri(f'{SITE}/favicon.ico', 'image/x-icon')

URLMAP = {'/':'index.html'}
pages = []
for f in sorted(os.listdir(SITE)):
    if not f.endswith('.md'): continue
    raw = open(f'{SITE}/{f}').read()
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', raw, re.S)
    if not m:                      # README and other notes aren't pages
        continue
    fm, body = yaml.safe_load(m.group(1)), m.group(2)
    URLMAP[fm['permalink']] = ('index.html' if fm['permalink']=='/'
                               else fm['permalink'].strip('/')+'.html')
    pages.append((fm, body))

# nav targets we don't have source for — stub them so the header is clickable
stubs = [i['url'] for i in cfg['nav'] if i['url'] not in URLMAP]
for u in stubs:
    URLMAP[u] = u.strip('/')+'.html'

def resolve(path):
    if path in URLMAP: return URLMAP[path]
    if path.startswith('/assets/img/'): return os.path.basename(path)
    if path == '/favicon.ico': return ICON
    return path

def render(fm, body):
    page_url = fm['permalink']
    desc = fm.get('description') or cfg['description']
    title = (f"{fm['title']} — {cfg['title']}" if page_url != '/' else cfg['title'])
    ogtitle = fm['title'] if page_url != '/' else cfg['title']

    nav = []
    for it in cfg['nav']:
        cur = ' aria-current="page"' if page_url == it['url'] else ''
        nav.append(f'          <li>\n            <a href="{resolve(it["url"])}"'
                   f'\n               {cur.strip()}>{it["title"]}</a>\n          </li>')
    out = layout

    out = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', out, flags=re.S)
    out = re.sub(r'(<meta name="description" content=").*?(">)', rf'\1{desc}\2', out, flags=re.S)
    out = re.sub(r'(<meta property="og:title" content=").*?(">)', rf'\1{ogtitle}\2', out, flags=re.S)
    out = out.replace('{%- assign og_desc = page.description | default: site.description -%}\n', '')
    out = out.replace('{{ og_desc }}', desc)
    out = out.replace('{{ site.url }}{{ page.url }}', cfg['url'] + page_url)
    out = re.sub(r'\{%\s*for item in site\.nav\s*%\}.*?\{%\s*endfor\s*%\}',
                 '\n'.join(nav), out, flags=re.S)
    out = re.sub(r'\{%\s*if site\.goatcounter_code.*?%\}(.*?)\{%\s*endif\s*%\}',
                 r'\1', out, flags=re.S)

    out = out.replace('{{ content }}', body)
    # stylesheet -> inline
    out = re.sub(r'<link rel="stylesheet" href="[^"]*">', f'<style>{css}</style>', out)
    out = out.replace("{{ '/assets/img/ches-mark.png' | relative_url }}", MARK)

    for m in set(re.findall(r"\{\{\s*'([^']+)'\s*\|\s*(?:relative_url|absolute_url)\s*\}\}", out)):
        for filt in ('relative_url','absolute_url'):
            tgt = cfg['url']+m if filt=='absolute_url' else resolve(m)
            out = re.sub(r"\{\{\s*'"+re.escape(m)+r"'\s*\|\s*"+filt+r"\s*\}\}", tgt.replace('\\','\\\\'), out)
    for k, v in cfg.items():
        if isinstance(v, str):
            out = out.replace('{{ site.%s }}' % k, v)
    return out

os.makedirs(OUT, exist_ok=True)
for fm, body in pages:
    name = URLMAP[fm['permalink']]
    open(f'{OUT}/{name}','w').write(render(fm, body))
    print(f'  {name}')
for u in stubs:
    fm = {'permalink': u, 'title': u.strip("/"), 'description': 'Preview stub.'}
    body = ('<section class="pagehead"><div class="wrap"><p class="label">Preview stub</p>'
            f'<h1>{u}</h1><p class="lede">This file was not in the project knowledge, so the '
            'preview builder stubbed it to keep the header links working. Your real '
            f'<code>{u.strip("/")}.md</code> is untouched.</p></div></section>')
    open(f'{OUT}/{URLMAP[u]}','w').write(render(fm, body))
    print(f'  {URLMAP[u]}  (stub)')
for img in ('og-image.png','apple-touch-icon.png'):
    open(f'{OUT}/{img}','wb').write(open(f'{SITE}/assets/img/{img}','rb').read())
