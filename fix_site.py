#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PayrollFixPro site fix script.
1. index.html:
   - Hero subtitle text update
   - Add 2 CTA buttons (Calculate Salary / Calculate Tax) with CSS
   - Stats 2024 → 2026
   - Ad placeholder div below hero
   - Ad placeholder div between tool list and About block
   - About text 2024 → 2026
   - Fix footer mojibake (漏 → ©) and 2024 → 2026
   - Fix pagination arrow mojibake
2. All tool pages (tools/*.html):
   - Footer: 漏 → © and 2024 → 2026
   - Breadcrumb separator 鈥?→ ›
   - Mojibake 鈥? → cleaned (remove CJK+?)
   - 2024 references in content → 2026
3. about.html, privacy.html:
   - Footer: 漏 → © and 2024 → 2026
"""

import os, re

SITE_DIR   = r'C:\Users\Administrator\payrollfixpro'
TOOLS_DIR  = os.path.join(SITE_DIR, 'tools')

# CSS to add for hero CTA buttons (injected before first @media or end of style)
HERO_BTN_CSS = (
    '.hero-cta{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:28px}'
    '.btn-cta{padding:12px 28px;border-radius:var(--radius-sm);font-size:15px;font-weight:700;'
    'cursor:pointer;transition:all .2s;border:2px solid #fff;letter-spacing:-.2px}'
    '.btn-cta-primary{background:#fff;color:var(--primary)}'
    '.btn-cta-primary:hover{background:rgba(255,255,255,.9)}'
    '.btn-cta-outline{background:transparent;color:#fff}'
    '.btn-cta-outline:hover{background:rgba(255,255,255,.12)}'
)

# Ad placeholder HTML for between hero and main
HERO_AD = (
    '\n<div style="background:#f8fafc;border-bottom:1px solid #e2e8f0;padding:12px 20px">'
    '<div style="max-width:1100px;margin:0 auto">'
    '<div class="ad-slot" style="height:90px;border-radius:var(--radius-sm)">'
    '<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-1638874323475457"'
    ' data-ad-slot="2345678901" data-ad-format="auto" data-full-width-responsive="true"></ins>'
    '<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'
    '</div></div></div>\n'
)

# Ad placeholder between tool list and About section
MID_AD = (
    '\n  <div class="ad-slot" style="height:90px;margin:8px 0 32px;border-radius:var(--radius-sm)">'
    '<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-1638874323475457"'
    ' data-ad-slot="3456789012" data-ad-format="auto" data-full-width-responsive="true"></ins>'
    '<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'
    '</div>\n'
)

# ── mojibake helpers ───────────────────────────────────────────────────────────
# CJK range used in this site (includes 漏 U+6F0F and 鈥 U+9225)
CJK_CLEANUP = re.compile(r'[一-鿿㐀-䶿豈-﫿]\??')

def clean_mojibake(text):
    """Remove CJK mojibake chars and trailing '?'."""
    # Replace © mojibake (漏, U+6F0F) specifically — keep as literal ©
    text = text.replace('漏', '©')
    # Remove remaining CJK chars + optional trailing '?'
    text = CJK_CLEANUP.sub('', text)
    # Remove U+FFFD replacement chars
    text = text.replace('�', '')
    return text

# ── index.html ─────────────────────────────────────────────────────────────────

def fix_index():
    path = os.path.join(SITE_DIR, 'index.html')
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        t = f.read()

    changes = []

    # 1. Inject hero CTA button CSS before @media or </style>
    if '.btn-cta{' not in t:
        inject_before = '@media(max-width:640px)' if '@media(max-width:640px)' in t else '</style>'
        t = t.replace(inject_before, HERO_BTN_CSS + '\n' + inject_before, 1)
        changes.append('hero_btn_css')

    # 2. Update hero subtitle (p tag inside .hero)
    old_p = '<p>100+ free calculators for paycheck, salary, tax, PTO, freelance rates, and more. No signup required.</p>'
    new_p = '<p>100+ free calculators for employees, HR professionals and freelancers</p>'
    if old_p in t:
        t = t.replace(old_p, new_p)
        changes.append('hero_subtitle')

    # 3. Add CTA buttons after the hero <p> and before <div class="stats">
    #    (works whether or not subtitle was already updated)
    HERO_CTA_HTML = (
        '\n  <div class="hero-cta">'
        '<a href="/tools/annual-salary-calculator.html" class="btn-cta btn-cta-primary">Calculate Salary</a>'
        '<a href="/tools/federal-income-tax-calculator.html" class="btn-cta btn-cta-outline">Calculate Tax</a>'
        '</div>'
    )
    if 'btn-cta-primary' not in t:
        # Insert after the last </p> before <div class="stats">
        stats_pos = t.find('<div class="stats">')
        if stats_pos != -1:
            # find the </p> immediately before stats
            p_end = t.rfind('</p>', 0, stats_pos)
            if p_end != -1:
                insert_at = p_end + len('</p>')
                t = t[:insert_at] + HERO_CTA_HTML + t[insert_at:]
                changes.append('hero_cta_buttons')

    # 4. Stats: 2024 → 2026 (only inside .stat-num)
    old_stat = '<div class="stat-num">2024</div><div class="stat-label">Tax Year Data</div>'
    new_stat = '<div class="stat-num">2026</div><div class="stat-label">Tax Year Data</div>'
    if old_stat in t:
        t = t.replace(old_stat, new_stat)
        changes.append('stat_year')

    # 5. Add ad placeholder below hero div (before <main>)
    if 'data-ad-slot="2345678901"' not in t:
        main_pos = t.find('<main>')
        if main_pos != -1:
            t = t[:main_pos] + HERO_AD + t[main_pos:]
            changes.append('hero_ad')

    # 6. Add ad placeholder between pagination and about block
    if 'data-ad-slot="3456789012"' not in t:
        about_pos = t.find('<div class="about">')
        if about_pos != -1:
            t = t[:about_pos] + MID_AD + t[about_pos:]
            changes.append('mid_ad')

    # 7. About section: 2024 → 2026 (within the about div text)
    about_start = t.find('<div class="about">')
    about_end   = t.find('</div>', about_start + 100) if about_start != -1 else -1
    if about_start != -1:
        old_about_block = t[about_start:]
        new_about_block = old_about_block.replace('2024 tax year', '2026 tax year')
        new_about_block = new_about_block.replace('for the 2024', 'for the 2026')
        if new_about_block != old_about_block:
            t = t[:about_start] + new_about_block
            changes.append('about_year')

    # 8. Fix pagination arrow mojibake in JS
    # Pattern: >鈥?/button> (prev/next arrow buttons)
    # Replace with proper ← and → arrows
    if '>鈥?</button>' in t:
        # Split by occurrences: first is ← (prev), last is → (next)
        parts = t.split('>鈥?</button>')
        if len(parts) == 3:
            t = parts[0] + '>&lsaquo;</button>' + parts[1] + '>&rsaquo;</button>' + parts[2]
            changes.append('pagination_arrows')
    # Fallback: clean any remaining mojibake in JS
    t = clean_mojibake(t)

    # 9. Footer: 漏 → © and 2024 → 2026
    footer_pos = t.rfind('<footer>')
    if footer_pos != -1:
        old_footer = t[footer_pos:]
        new_footer = old_footer.replace('漏 2024', '© 2026').replace('漏2024', '© 2026')
        new_footer = clean_mojibake(new_footer)
        if new_footer != old_footer:
            t = t[:footer_pos] + new_footer
            changes.append('footer_year')

    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(t)

    print('  index.html [{}]'.format(', '.join(changes) if changes else 'no-changes'))


# ── tool pages (100 files) ─────────────────────────────────────────────────────

def fix_tool_page(fpath):
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        t = f.read()

    original = t
    changes = []

    # 1. Fix breadcrumb separator: <span>鈥?/span> → <span>&rsaquo;</span>
    bc_bad  = '<span>鈥?</span>'
    bc_good = '<span>&rsaquo;</span>'
    if bc_bad in t:
        t = t.replace(bc_bad, bc_good)
        changes.append('breadcrumb')

    # 2. Clean mojibake throughout (including footer 漏 → ©)
    cleaned = clean_mojibake(t)
    if cleaned != t:
        t = cleaned
        changes.append('mojibake')

    # 3. Footer: 2024 → 2026
    footer_pos = t.rfind('<footer>')
    if footer_pos != -1:
        old_f = t[footer_pos:]
        new_f = old_f.replace('2024', '2026')
        if new_f != old_f:
            t = t[:footer_pos] + new_f
            changes.append('footer_year')

    # 4. Content 2024 → 2026 in seo-section and faq-section (not in CSS/code)
    #    Replace "2024" in text content sections
    for marker in ['<div class="seo-section">', '<div class="faq-section">',
                   '<p>', 'data-ad']:
        pass  # handled below

    # Replace 2024 in seo/faq text blocks
    for tag_open, tag_cls in [('.seo-section', 'seo-section'), ('.faq-section', 'faq-section')]:
        div_start = t.find('<div class="{}">'.format(tag_cls))
        if div_start == -1:
            continue
        # Find end of section (depth track)
        pos = div_start + 1
        depth = 1
        end = -1
        while pos < len(t) and depth > 0:
            od = t.find('<div', pos)
            cd = t.find('</div>', pos)
            if cd == -1:
                break
            if od != -1 and od < cd:
                depth += 1
                pos = od + 1
            else:
                depth -= 1
                if depth == 0:
                    end = cd + len('</div>')
                pos = cd + 1
        if end != -1:
            section = t[div_start:end]
            new_section = section.replace('2024', '2026')
            if new_section != section:
                t = t[:div_start] + new_section + t[end:]
                if 'content_year' not in changes:
                    changes.append('content_year')

    if t != original:
        with open(fpath, 'w', encoding='utf-8', newline='') as f:
            f.write(t)

    return changes


def fix_simple_page(fpath):
    """Fix about.html, privacy.html: mojibake + footer year."""
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        t = f.read()
    original = t

    t = clean_mojibake(t)

    footer_pos = t.rfind('<footer>')
    if footer_pos != -1:
        old_f = t[footer_pos:]
        new_f = old_f.replace('2024', '2026')
        if new_f != old_f:
            t = t[:footer_pos] + new_f

    if t != original:
        with open(fpath, 'w', encoding='utf-8', newline='') as f:
            f.write(t)
        return True
    return False


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    print('=== PayrollFixPro site fix ===\n')

    # index.html
    print('[index.html]')
    fix_index()

    # about.html, privacy.html
    for fname in ('about.html', 'privacy.html'):
        fpath = os.path.join(SITE_DIR, fname)
        if os.path.exists(fpath):
            changed = fix_simple_page(fpath)
            print('  {} [{}]'.format(fname, 'fixed' if changed else 'no-change'))

    # tool pages
    print('\n[tool pages]')
    tool_files = sorted(f for f in os.listdir(TOOLS_DIR) if f.endswith('.html'))
    fixed = 0
    for fname in tool_files:
        fpath = os.path.join(TOOLS_DIR, fname)
        changes = fix_tool_page(fpath)
        if changes:
            fixed += 1
            print('  OK  {} [{}]'.format(fname.replace('.html',''), ','.join(changes)))

    print('\n  Total tool pages fixed: {}/{}'.format(fixed, len(tool_files)))
    print('\nDone.')

if __name__ == '__main__':
    main()
