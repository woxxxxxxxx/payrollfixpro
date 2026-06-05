import os, glob, re

os.chdir(r"C:\Users\Administrator\payrollfixpro")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# VestCalc 广告样式（PayrollFixPro 主色 #0f766e）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NEW_AD_CSS = (
    ".ad-slot{background:#fff;border:1px dashed #cbd5e1;border-radius:12px;"
    "padding:20px;text-align:center;color:#94a3b8;font-size:12px;"
    "letter-spacing:.5px;text-transform:uppercase;margin:24px 0;"
    "min-height:90px;display:flex;align-items:center;justify-content:center;"
    "flex-direction:column;gap:8px}"
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TOOL PAGES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
tool_files = glob.glob("tools/*.html")

# CSS 旧值 → 新值
CSS_PAIRS = [
    # 上一轮修复留下的空 CSS
    (".ad-slot{width:100%;overflow:hidden}",            NEW_AD_CSS),
    # 上一轮修复留下的尺寸 CSS
    (".ad-top{}.ad-middle{margin-bottom:0}.ad-bottom{}", ""),
    # adsense-placeholder
    (".adsense-placeholder{width:100%}",                ".adsense-placeholder{width:100%;display:block}"),
]

# HTML: 移除所有 inline style 覆盖，统一用 class="ad-slot"
# 同时 ad-middle 恢复显示，更换 class 为纯 ad-slot
HTML_PAIRS = [
    # ad-top: 去掉 inline style
    (
        'class="ad-slot ad-top" style="min-height:0!important;overflow:hidden;line-height:0;"',
        'class="ad-slot"'
    ),
    # ad-middle: 去掉 display:none 及 inline style（恢复显示）
    (
        'class="ad-slot ad-middle" style="display:none;min-height:0!important;overflow:hidden;line-height:0;"',
        'class="ad-slot"'
    ),
    # ad-bottom: 去掉 inline style
    (
        'class="ad-slot ad-bottom" style="min-height:0!important;overflow:hidden;line-height:0;"',
        'class="ad-slot"'
    ),
    # 万一有未匹配的旧 class 名残留
    ('class="ad-slot ad-top"',    'class="ad-slot"'),
    ('class="ad-slot ad-middle"', 'class="ad-slot"'),
    ('class="ad-slot ad-bottom"', 'class="ad-slot"'),
]

# 在 <ins> 前面插入 "Advertisement" 文字节点（如果还没有的话）
INS_TAG = '<ins class="adsbygoogle'
ADV_PREFIX = 'Advertisement\n    '

tool_updated = 0
for f in tool_files:
    with open(f, "r", encoding="utf-8") as fh:
        c = fh.read()
    orig = c

    for old, new in CSS_PAIRS:
        c = c.replace(old, new)

    for old, new in HTML_PAIRS:
        c = c.replace(old, new)

    # 插入 Advertisement 文字（只在还没有的情况下）
    if INS_TAG in c and ADV_PREFIX not in c:
        c = c.replace(INS_TAG, ADV_PREFIX + INS_TAG)

    if c != orig:
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(c)
        tool_updated += 1

print(f"Tool pages updated: {tool_updated} / {len(tool_files)}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INDEX.HTML  (ad 结构略有不同，单独处理)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with open("index.html", "r", encoding="utf-8") as fh:
    idx = fh.read()
orig_idx = idx

# CSS 修复
IDX_CSS_PAIRS = [
    (".ad-slot{width:100%;overflow:hidden}",   NEW_AD_CSS),
    (".ad-top{margin:0}",                      ".ad-top{margin-top:0}"),
    (".adsense-placeholder{width:100%}",       ".adsense-placeholder{width:100%;display:block}"),
]
for old, new in IDX_CSS_PAIRS:
    idx = idx.replace(old, new)

# HTML: 去掉带 height:90px 的内联样式（上轮修改结果）
IDX_HTML_PAIRS = [
    # slot 1: banner strip 外层 div
    (
        '<div class="ad-slot" style="min-height:0!important;overflow:hidden;line-height:0;">',
        '<div class="ad-slot">'
    ),
    # slot 2: ad-top
    (
        '<div class="ad-slot ad-top" style="min-height:0!important;overflow:hidden;line-height:0;">',
        '<div class="ad-slot">'
    ),
    # slot 2 (alt – no inline style left from earlier patch)
    ('<div class="ad-slot ad-top">',  '<div class="ad-slot">'),
]
for old, new in IDX_HTML_PAIRS:
    idx = idx.replace(old, new)

# 插入 Advertisement 文字（index 里的 ins 节点）
if '<ins class="adsbygoogle"' in idx and 'Advertisement\n' not in idx:
    idx = idx.replace('<ins class="adsbygoogle"', 'Advertisement\n<ins class="adsbygoogle"')

if idx != orig_idx:
    with open("index.html", "w", encoding="utf-8") as fh:
        fh.write(idx)
    print("index.html        : updated")
else:
    print("index.html        : no change")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# VERIFY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
s = open("tools/salary-calculator.html", encoding="utf-8").read()
print("\nVerify tools/salary-calculator.html:")
print("  dashed border CSS      :", "border:1px dashed #cbd5e1" in s)
print("  min-height:90px        :", "min-height:90px" in s)
print("  display:flex centered  :", "display:flex;align-items:center" in s)
print("  no ad-top/mid/bot class:", "ad-top" not in s and "ad-middle" not in s and "ad-bottom" not in s)
print("  no display:none        :", "display:none" not in s)
print("  Advertisement text     :", "Advertisement" in s)

ix = open("index.html", encoding="utf-8").read()
print("\nVerify index.html:")
print("  dashed border CSS      :", "border:1px dashed #cbd5e1" in ix)
print("  no height:90px inline  :", 'height:90px' not in ix)
