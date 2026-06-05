#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Replace .ad-slot CSS in all payrollfixpro HTML files:
- Remove background, border, display:flex, etc.
- Keep only width:100%;min-height:90px (transparent, no border)
"""
import os, re

SITE_DIR  = r'C:\Users\Administrator\payrollfixpro'
TOOLS_DIR = os.path.join(SITE_DIR, 'tools')

# Pattern to match .ad-slot{...} CSS block (greedy, same line)
OLD_PAT = re.compile(
    r'\.ad-slot\{[^}]*background[^}]*\}',
)
NEW_CSS = '.ad-slot{width:100%;min-height:90px}'

def fix_file(fpath):
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()
    new_text = OLD_PAT.sub(NEW_CSS, text)
    if new_text != text:
        with open(fpath, 'w', encoding='utf-8', newline='') as f:
            f.write(new_text)
        return True
    return False

fixed = 0
total = 0

# index.html, about.html, privacy.html
for fname in ('index.html', 'about.html', 'privacy.html'):
    fpath = os.path.join(SITE_DIR, fname)
    if os.path.exists(fpath):
        total += 1
        if fix_file(fpath):
            fixed += 1
            print(f'  fixed  {fname}')

# tools/*.html
for fname in sorted(os.listdir(TOOLS_DIR)):
    if not fname.endswith('.html'):
        continue
    fpath = os.path.join(TOOLS_DIR, fname)
    total += 1
    if fix_file(fpath):
        fixed += 1
        print(f'  fixed  tools/{fname}')

print(f'\nDone: {fixed}/{total} files updated')
