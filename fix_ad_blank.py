import os, glob, re

os.chdir(r"C:\Users\Administrator\payrollfixpro")

# ══════════════════════════════════════════════════════════════
# TOOL PAGES  (tools/*.html)
# ══════════════════════════════════════════════════════════════
CSS_OLD = ".ad-slot{width:100%;min-height:90px;overflow:hidden}"
CSS_NEW = ".ad-slot{width:100%;overflow:hidden}"

SIZES_OLD = ".ad-top{min-height:90px}.ad-middle{min-height:90px;margin-bottom:24px}.ad-bottom{min-height:90px}"
SIZES_NEW = ".ad-top{}.ad-middle{margin-bottom:0}.ad-bottom{}"

PH_OLD = ".adsense-placeholder{width:100%;min-height:90px}"
PH_NEW = ".adsense-placeholder{width:100%}"

# HTML: ad-top  ─ keep visible, just zero-height until approved
TOP_OLD = '<div class="ad-slot ad-top">'
TOP_NEW = ('<!-- AD_PLACEHOLDER -->\n  '
           '<div class="ad-slot ad-top" '
           'style="min-height:0!important;overflow:hidden;line-height:0;">')

# HTML: ad-middle  ─ hide entirely
MID_OLD = '<div class="ad-slot ad-middle">'
MID_NEW = ('<!-- AD_PLACEHOLDER -->\n  '
           '<div class="ad-slot ad-middle" '
           'style="display:none;min-height:0!important;overflow:hidden;line-height:0;">')

# HTML: ad-bottom  ─ keep visible, zero-height
BOT_OLD = '<div class="ad-slot ad-bottom">'
BOT_NEW = ('<!-- AD_PLACEHOLDER -->\n  '
           '<div class="ad-slot ad-bottom" '
           'style="min-height:0!important;overflow:hidden;line-height:0;">')

tool_files = glob.glob("tools/*.html")
tool_count = 0
tool_css = tool_top = tool_mid = tool_bot = 0

for f in tool_files:
    with open(f, "r", encoding="utf-8") as fh:
        c = fh.read()
    orig = c

    # CSS fixes
    c = c.replace(CSS_OLD, CSS_NEW)
    c = c.replace(SIZES_OLD, SIZES_NEW)
    c = c.replace(PH_OLD, PH_NEW)

    # HTML fixes – only replace once each (avoid double-wrapping on re-run)
    if TOP_OLD in c:
        c = c.replace(TOP_OLD, TOP_NEW, 1); tool_top += 1
    if MID_OLD in c:
        c = c.replace(MID_OLD, MID_NEW, 1); tool_mid += 1
    if BOT_OLD in c:
        c = c.replace(BOT_OLD, BOT_NEW, 1); tool_bot += 1

    if c != orig:
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(c)
        tool_count += 1

print(f"Tool pages updated : {tool_count} / {len(tool_files)}")
print(f"  ad-top patched   : {tool_top}")
print(f"  ad-middle hidden : {tool_mid}")
print(f"  ad-bottom patched: {tool_bot}")

# ══════════════════════════════════════════════════════════════
# INDEX.HTML  (3 ad slots, all different inline styles)
# ══════════════════════════════════════════════════════════════
with open("index.html", "r", encoding="utf-8") as fh:
    idx = fh.read()
orig_idx = idx

# CSS: kill min-height on .ad-slot and .ad-top
idx = idx.replace(
    ".ad-slot{width:100%;min-height:90px}",
    ".ad-slot{width:100%;overflow:hidden}"
)
idx = idx.replace(
    ".ad-top{min-height:90px;margin:24px 0 0}",
    ".ad-top{margin:0}"
)
idx = idx.replace(
    ".adsense-placeholder{width:100%;min-height:90px}",
    ".adsense-placeholder{width:100%}"
)

# HTML slot 1 – banner strip above main (has height:90px inline)
OLD1 = ('<div class="ad-slot" style="height:90px;border-radius:var(--radius-sm)">'
        '<ins class="adsbygoogle"')
NEW1 = ('<!-- AD_PLACEHOLDER -->'
        '\n<div class="ad-slot" style="min-height:0!important;overflow:hidden;line-height:0;">'
        '<ins class="adsbygoogle"')
if OLD1 in idx:
    idx = idx.replace(OLD1, NEW1, 1)

# HTML slot 2 – ad-top inside <div style="margin-bottom:24px">
OLD2 = ('<div class="ad-slot ad-top">\n      '
        '<ins class="adsbygoogle adsense-placeholder"')
NEW2 = ('<!-- AD_PLACEHOLDER -->\n    '
        '<div class="ad-slot ad-top" style="min-height:0!important;overflow:hidden;line-height:0;">\n      '
        '<ins class="adsbygoogle adsense-placeholder"')
if OLD2 in idx:
    idx = idx.replace(OLD2, NEW2, 1)

# HTML slot 3 – mid-page slot (height:90px;margin:8px 0 32px)
OLD3 = ('<div class="ad-slot" style="height:90px;margin:8px 0 32px;border-radius:var(--radius-sm)">'
        '<ins class="adsbygoogle"')
NEW3 = ('<!-- AD_PLACEHOLDER -->'
        '\n<div class="ad-slot" style="min-height:0!important;overflow:hidden;line-height:0;">'
        '<ins class="adsbygoogle"')
if OLD3 in idx:
    idx = idx.replace(OLD3, NEW3, 1)

if idx != orig_idx:
    with open("index.html", "w", encoding="utf-8") as fh:
        fh.write(idx)
    print("index.html         : updated")
else:
    print("index.html         : no changes (already patched?)")

# ══════════════════════════════════════════════════════════════
# VERIFY
# ══════════════════════════════════════════════════════════════
sample = open("tools/salary-calculator.html", encoding="utf-8").read()
print("\nVerify salary-calculator.html:")
print("  CSS min-height removed :", "min-height:90px" not in sample)
print("  ad-top zero-height     :", "min-height:0!important" in sample)
print("  ad-middle display:none :", "display:none" in sample)
print("  AD_PLACEHOLDER comment :", "<!-- AD_PLACEHOLDER -->" in sample)

idx_check = open("index.html", encoding="utf-8").read()
print("\nVerify index.html:")
print("  CSS min-height removed :", "min-height:90px" not in idx_check)
print("  AD_PLACEHOLDER comment :", "<!-- AD_PLACEHOLDER -->" in idx_check)
print("  No bare height:90px    :", "height:90px" not in idx_check)
