import glob, re, os

TOOL_FILES = sorted(glob.glob('tools/*.html'))

fixed_bc = 0
fixed_logo = 0

for fpath in TOOL_FILES:
    txt = open(fpath, encoding='utf-8', errors='ignore').read()
    orig = txt

    # Fix breadcrumb: add Tools middle level
    # Pattern: <a href="/">Home</a><span>&rsaquo;</span>PAGE_TITLE
    def fix_breadcrumb(m):
        return (m.group(0)
                .replace('<a href="/">Home</a><span>&rsaquo;</span>',
                         '<a href="/">Home</a><span>&rsaquo;</span><a href="/">Tools</a><span>&rsaquo;</span>'))
    new_txt = re.sub(
        r'<div class="breadcrumb"><a href="/">Home</a><span>&rsaquo;</span>(?!<a)',
        fix_breadcrumb,
        txt
    )
    if new_txt != txt:
        txt = new_txt
        fixed_bc += 1

    # Fix tool page header logo: text → img
    old_logo = '<a href="/" class="logo">Payroll<span>Fix</span>Pro</a>'
    new_logo = '<a href="/" class="logo"><img src="/logo.svg" alt="PayrollFixPro" height="38"></a>'
    if old_logo in txt:
        txt = txt.replace(old_logo, new_logo)
        fixed_logo += 1

    if txt != orig:
        open(fpath, 'w', encoding='utf-8').write(txt)

# Also fix about.html / privacy.html breadcrumb if any
for fpath in ['about.html', 'privacy.html', 'index.html']:
    if not os.path.exists(fpath): continue
    txt = open(fpath, encoding='utf-8', errors='ignore').read()
    orig = txt
    old_logo = '<a href="/" class="logo">Payroll<span>Fix</span>Pro</a>'
    new_logo = '<a href="/" class="logo"><img src="/logo.svg" alt="PayrollFixPro" height="38"></a>'
    if old_logo in txt:
        txt = txt.replace(old_logo, new_logo)
    if txt != orig:
        open(fpath, 'w', encoding='utf-8').write(txt)

print(f"Breadcrumb fixed: {fixed_bc} tool pages")
print(f"Header logo fixed: {fixed_logo} tool pages")

# Verify
remaining_bc = 0
remaining_logo = 0
for fpath in TOOL_FILES:
    txt = open(fpath, encoding='utf-8', errors='ignore').read()
    if '<div class="breadcrumb">' in txt:
        bc = re.search(r'<div class="breadcrumb">([\s\S]*?)</div>', txt)
        if bc and 'Tools' not in bc.group(1):
            remaining_bc += 1
    if 'class="logo">Payroll<span>' in txt:
        remaining_logo += 1

print(f"\nVerify — breadcrumb still missing Tools: {remaining_bc}")
print(f"Verify — logo still text: {remaining_logo}")
