#!/usr/bin/env python3
"""Prevent deprecated products returning to active discovery."""
import json
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]
ACTIVE = ('index.html', 'apps/index.html', 'portfolio/index.html', 'trials/index.html', 'blog/index.html')
RETIRED = re.compile(r'nownest|mews(?:-and-| &amp; | & | and )woofs|rung', re.I)
def validate(root=ROOT):
    errors=[]
    for path in ACTIVE:
        if RETIRED.search((root/path).read_text()):
            errors.append(f'deprecated product promoted: {path}')
    manifest=json.loads((root/'source-page-manifest.json').read_text())
    for page in manifest['pages']:
        if not RETIRED.search(page['path']): continue
        path=page['path'].lstrip('/')
        if path.endswith('/'): path+='index.html'
        text=(root/path).read_text()
        if 'deprecated' not in text.lower() or 'noindex' not in text:
            errors.append(f'retirement disclosure missing: {path}')
        if page.get('indexable') is not False:
            errors.append(f'retired page indexable: {path}')
    if RETIRED.search((root/'sitemap.xml').read_text()):
        errors.append('sitemap promotes retired product')
    for path in root.rglob('*.html'):
        text=path.read_text()
        if 'https://rung.edoworks.com' in text: errors.append('failing rung hostname')
        for href in re.findall(r"href=[\"'](/[^\"'#?]*)",text):
            target=root/href.lstrip('/')
            if href.endswith('/'): target=target/'index.html'
            if not target.is_file(): errors.append(f'local link target is missing: {href}')
    return errors
if __name__=='__main__':
    errors=validate()
    print('\n'.join(errors) if errors else 'site claim validation passed')
    raise SystemExit(bool(errors))
