import glob, re, os

TOOL_FILES = sorted(glob.glob('tools/*.html'))
ALL_FILES = TOOL_FILES + ['index.html', 'about.html', 'privacy.html']

issues = {k: [] for k in ['ga_inline','old_template','seo_bad_url','no_canonical','breadcrumb','no_btt','no_print','logo_text','asset_missing']}
fixed = {k: 0 for k in issues}

# ─── SCAN ───────────────────────────────────────────────────────────────────

for fpath in TOOL_FILES:
    txt = open(fpath, encoding='utf-8', errors='ignore').read()
    fname = os.path.basename(fpath)

    # 1. GA inline functions
    for m in re.finditer(r'<script[^>]+src=[^>]+>', txt):
        after = txt[m.end():]
        close = after.find('</script>')
        if close != -1 and re.search(r'function\s+\w+', after[:close]):
            issues['ga_inline'].append(fpath)
            break

    # 2. Old template: reads totals from DOM textContent
    if re.search(r"getElementById\(['\"](?:subtotal|taxAmt|totalAmt)['\"].*?textContent", txt):
        issues['old_template'].append(fpath)

    # 3. SEO bad URLs
    for tag_pat in [r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']',
                    r'<meta[^>]+property=["\']og:url["\'][^>]+content=["\']([^"\']+)["\']']:
        for url in re.findall(tag_pat, txt):
            if re.search(r'localhost|127\.0\.0\.1|C:[/\\]Users|file://', url, re.I):
                issues['seo_bad_url'].append((fpath, url)); break

    # 4. Breadcrumb missing Tools level
    if 'breadcrumb' in txt:
        bc = re.search(r'class=["\']breadcrumb["\'][^>]*>([\s\S]*?)</(?:nav|div|ol|ul)', txt)
        if bc and not re.search(r'Tools', bc.group(1)):
            issues['breadcrumb'].append(fpath)

    # 5. No back-to-top
    if 'id="btt"' not in txt:
        issues['no_btt'].append(fpath)

    # 6. No @media print
    if '@media print' not in txt:
        issues['no_print'].append(fpath)

for fpath in ['about.html', 'privacy.html']:
    if not os.path.exists(fpath): continue
    txt = open(fpath, encoding='utf-8', errors='ignore').read()
    # 8. Logo img check
    logo_a = re.search(r'<a[^>]+class=["\']logo["\'][^>]*>([\s\S]*?)</a>', txt)
    if logo_a and '<img' not in logo_a.group(1):
        issues['logo_text'].append(fpath)

# 9. Assets
for asset in ['logo.svg', 'favicon.svg']:
    if not os.path.exists(asset):
        issues['asset_missing'].append(asset)

print("=== SCAN RESULTS ===")
for k, v in issues.items():
    print(f"  {k:<20} {len(v)} issues")

# ─── FIX ────────────────────────────────────────────────────────────────────

BTT_CSS = """
#btt{position:fixed;bottom:28px;right:24px;width:42px;height:42px;background:var(--primary,#0891b2);color:#fff;border:none;border-radius:50%;font-size:20px;cursor:pointer;display:none;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(0,0,0,.15);transition:all .2s;z-index:99}
#btt.show{display:flex}
#btt:hover{background:var(--primary-dark,#0e7490);transform:translateY(-2px)}"""

BTT_HTML = '\n<button id="btt" onclick="window.scrollTo({top:0,behavior:\'smooth\'})" title="Back to top">&#8679;</button>'

BTT_JS = "\nwindow.addEventListener('scroll',function(){var b=document.getElementById('btt');if(b)b.classList.toggle('show',window.scrollY>300);});"

PRINT_CSS = "@media print{header,footer,.ad-slot,.ad-top,.ad-middle,.ad-bottom,.form-card,.tool-hero,.breadcrumb,.seo-section,.faq-section,.related-section,.affiliate-section,.download-row,#btt{display:none!important}body{background:#fff!important}main{padding:0!important}.result-card,#output,#result{display:block!important;box-shadow:none!important;border:none!important;padding:0!important}}"

for fpath in TOOL_FILES:
    txt = open(fpath, encoding='utf-8', errors='ignore').read()
    orig = txt

    # Fix 1: GA inline → separate script tag
    def fix_ga_inline(m):
        open_tag, close_tag = m.group(1), m.group(3)
        inner = m.group(2).strip()
        if not inner:
            return m.group(0)
        return f'{open_tag}{close_tag}\n<script>\n{inner}\n</script>'
    txt = re.sub(r'(<script[^>]+src=["\'][^"\']+["\'][^>]*>)([\s\S]*?)(</script>)', fix_ga_inline, txt)

    # Fix 3: SEO bad canonical
    def fix_url(m):
        url = m.group(1)
        if re.search(r'localhost|127\.0\.0\.1|C:[/\\]Users|file://', url, re.I):
            slug = os.path.basename(fpath)
            return m.group(0).replace(url, f'https://payrollfixpro.com/tools/{slug}')
        return m.group(0)
    txt = re.sub(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', fix_url, txt)
    txt = re.sub(r'(<meta[^>]+property=["\']og:url["\'][^>]+content=["\'])([^"\']+)(["\'])',
                 lambda m: m.group(1) + (f'https://payrollfixpro.com/tools/{os.path.basename(fpath)}'
                            if re.search(r'localhost|127\.|C:[/\\]|file://', m.group(2), re.I) else m.group(2)) + m.group(3), txt)

    # Fix 5: Back-to-top
    if 'id="btt"' not in txt:
        if '</style>' in txt:
            txt = txt.replace('</style>', BTT_CSS + '\n</style>', 1)
        if '</footer>' in txt:
            txt = txt.replace('</footer>', '</footer>' + BTT_HTML, 1)
        if '</script>' in txt:
            pos = txt.rfind('</script>')
            txt = txt[:pos] + BTT_JS + '\n</script>' + txt[pos+9:]
        fixed['no_btt'] += 1

    # Fix 6: @media print
    OLD_PRINTS = [
        '@media print{header,footer,.ad-slot,.download-row,.related-section,.seo-section{display:none!important}.preview-card,.form-card{box-shadow:none!important;border:none!important}}',
        '@media print{body>*{display:none!important}main{display:block!important}main>*{display:none!important}#output{display:block!important;margin:0!important;padding:0!important;border:none!important;box-shadow:none!important}.download-row{display:none!important}}',
    ]
    if '@media print' not in txt:
        if '</style>' in txt:
            txt = txt.replace('</style>', PRINT_CSS + '\n</style>', 1)
        fixed['no_print'] += 1
    else:
        for op in OLD_PRINTS:
            if op in txt:
                txt = txt.replace(op, PRINT_CSS)
                fixed['no_print'] += 1
                break

    if txt != orig:
        open(fpath, 'w', encoding='utf-8').write(txt)

# Fix 8: about.html / privacy.html logo
for fpath in ['about.html', 'privacy.html']:
    if not os.path.exists(fpath): continue
    txt = open(fpath, encoding='utf-8', errors='ignore').read()
    orig = txt
    # Replace text logo in anchor
    txt = re.sub(
        r'(<a[^>]+class=["\']logo["\'][^>]*>)[^<]*(?:<span[^>]*>[^<]*</span>[^<]*)*</a>',
        r'<a href="/" class="logo"><img src="/logo.svg" alt="PayrollFixPro" height="38"></a>',
        txt
    )
    # Fix brand name in footer
    txt = re.sub(r'Payroll<span>Fix</span>Pro|InvoiceFix|BillingFix',
                 lambda m: 'Payroll<span>Fix</span>Pro', txt)
    if txt != orig:
        open(fpath, 'w', encoding='utf-8').write(txt)
        fixed['logo_text'] += 1

# Check logo.svg exists
if not os.path.exists('logo.svg'):
    issues['asset_missing'].append('logo.svg (NEEDS CREATION)')

print("\n=== FIX SUMMARY ===")
for k, v in fixed.items():
    if v > 0:
        print(f"  {k:<20} fixed {v}")

# Recount remaining issues
remaining = {}
for fpath in TOOL_FILES:
    txt = open(fpath, encoding='utf-8', errors='ignore').read()
    if 'id="btt"' not in txt: remaining.setdefault('no_btt',[]).append(fpath)
    if '@media print' not in txt: remaining.setdefault('no_print',[]).append(fpath)
    for m in re.finditer(r'<script[^>]+src=[^>]+>', txt):
        after = txt[m.end():]
        close = after.find('</script>')
        if close != -1 and re.search(r'function\s+\w+', after[:close]):
            remaining.setdefault('ga_inline',[]).append(fpath); break

print("\n=== REMAINING ISSUES ===")
total_remaining = sum(len(v) for v in remaining.values())
if total_remaining == 0:
    print("  ALL CLEAN")
else:
    for k, v in remaining.items():
        print(f"  {k}: {len(v)} files")
        for f in v[:3]: print(f"    {f}")
