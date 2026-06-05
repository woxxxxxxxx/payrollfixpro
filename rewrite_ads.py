import os, glob, re

os.chdir(r"C:\Users\Administrator\payrollfixpro")

# ══════════════════════════════════════════════════════════════════
# 新广告占位符模板
# ══════════════════════════════════════════════════════════════════
TPL_INDEX = (
    '<div style="text-align:center;padding:8px 0;margin:16px 0;">\n'
    '  <div style="display:inline-block;width:100%;max-width:728px;height:90px;'
    'border:1px dashed #ccc;background:#fafafa;line-height:90px;text-align:center;'
    'color:#aaa;font-size:12px;letter-spacing:1px;">ADVERTISEMENT</div>\n'
    '</div>'
)

TPL_TOOL = (
    '<div style="text-align:center;padding:8px 0;margin:12px 0;">\n'
    '  <div style="display:inline-block;width:100%;max-width:468px;height:60px;'
    'border:1px dashed #ccc;background:#fafafa;line-height:60px;text-align:center;'
    'color:#aaa;font-size:12px;letter-spacing:1px;">ADVERTISEMENT</div>\n'
    '</div>'
)

# AdSense script 标签（head 里要删除的）
ADSENSE_SCRIPT = ('<script async src="https://pagead2.googlesyndication.com/pagead/js/'
                  'adsbygoogle.js?client=ca-pub-1638874323475457" crossorigin="anonymous">'
                  '</script>\n')

# ══════════════════════════════════════════════════════════════════
# TOOL PAGES：3 个固定广告块 + CSS + head script
# ══════════════════════════════════════════════════════════════════

# 广告块 1 —— 位于 breadcrumb 下面，带外层 wrapper div
TOOL_BLOCK1 = (
    '<div style="max-width:860px;margin:16px auto;padding:0 20px">\n'
    '  <!-- AD_PLACEHOLDER -->\n'
    '  <div class="ad-slot">\n'
    '    Advertisement\n'
    '    <ins class="adsbygoogle adsense-placeholder" style="display:block" '
    'data-ad-client="ca-pub-1638874323475457" data-ad-slot="1234567890" '
    'data-ad-format="auto" data-full-width-responsive="true"></ins>\n'
    '    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>\n'
    '  </div>\n'
    '</div>'
)

# 广告块 2 —— 位于 result-card 下（ad-middle）
TOOL_BLOCK2 = (
    '  <!-- AD_PLACEHOLDER -->\n'
    '  <div class="ad-slot">\n'
    '    Advertisement\n'
    '    <ins class="adsbygoogle adsense-placeholder" style="display:block" '
    'data-ad-client="ca-pub-1638874323475457" data-ad-slot="0987654321" '
    'data-ad-format="auto" data-full-width-responsive="true"></ins>\n'
    '    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>\n'
    '  </div>'
)

# 广告块 3 —— 页面底部（ad-bottom）
TOOL_BLOCK3 = (
    '  <!-- AD_PLACEHOLDER -->\n'
    '  <div class="ad-slot">\n'
    '    Advertisement\n'
    '    <ins class="adsbygoogle adsense-placeholder" style="display:block" '
    'data-ad-client="ca-pub-1638874323475457" data-ad-slot="1122334455" '
    'data-ad-format="auto" data-full-width-responsive="true"></ins>\n'
    '    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>\n'
    '  </div>'
)

# CSS 旧值（要删除）
TOOL_CSS_OLD = (
    '.ad-slot{background:#fff;border:1px dashed #cbd5e1;border-radius:12px;'
    'padding:16px 20px;text-align:center;color:#94a3b8;font-size:12px;'
    'letter-spacing:.5px;text-transform:uppercase;margin:20px 0;'
    'display:flex;align-items:center;justify-content:center;flex-direction:column}\n'
)
TOOL_CSS_PH_OLD = '.adsense-placeholder{display:block;width:100%;height:0;overflow:hidden}\n'
TOOL_CSS_TOP_OLD = '.ad-top{margin-top:0}\n'

tool_files = glob.glob("tools/*.html")
tool_count = 0
tool_fail = []

for f in tool_files:
    with open(f, "r", encoding="utf-8") as fh:
        c = fh.read()
    orig = c

    # 删除 head 里的 AdSense script
    c = c.replace(ADSENSE_SCRIPT, '')
    # 兼容无尾换行的写法
    c = c.replace(ADSENSE_SCRIPT.rstrip('\n'), '')

    # 删除 ad-slot / adsense-placeholder / ad-top CSS
    c = c.replace(TOOL_CSS_OLD, '')
    c = c.replace(TOOL_CSS_PH_OLD, '')
    c = c.replace(TOOL_CSS_TOP_OLD, '')

    # 替换 3 个广告块
    c = c.replace(TOOL_BLOCK1, TPL_TOOL)
    c = c.replace(TOOL_BLOCK2, TPL_TOOL)
    c = c.replace(TOOL_BLOCK3, TPL_TOOL)

    if c != orig:
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(c)
        tool_count += 1
    else:
        tool_fail.append(f)

print(f"Tool pages updated: {tool_count} / {len(tool_files)}")
if tool_fail:
    print(f"  No change (check): {tool_fail[:3]}")

# ══════════════════════════════════════════════════════════════════
# INDEX.HTML：3 个广告块结构不同，逐一处理
# ══════════════════════════════════════════════════════════════════
with open("index.html", "r", encoding="utf-8") as fh:
    idx = fh.read()
orig_idx = idx

# 删除 head AdSense script
idx = idx.replace(ADSENSE_SCRIPT, '')
idx = idx.replace(ADSENSE_SCRIPT.rstrip('\n'), '')

# 删除 .ad-slot CSS（index 版本可能略有不同，用 regex 覆盖）
idx = re.sub(r'\.ad-slot\{[^}]+\}', '', idx)
idx = re.sub(r'\.adsense-placeholder\{[^}]+\}', '', idx)
idx = re.sub(r'\.ad-top\{[^}]+\}', '', idx)

# 广告块 1 —— banner strip 内（带背景色外层 div）
# 整段：<!-- AD_PLACEHOLDER -->\n<div class="ad-slot">...(单行)</div>
IDX_BLOCK1 = (
    '<!-- AD_PLACEHOLDER -->\n'
    '<div class="ad-slot">Advertisement\n'
    '<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-1638874323475457" '
    'data-ad-slot="2345678901" data-ad-format="auto" data-full-width-responsive="true">'
    '</ins><script>(adsbygoogle = window.adsbygoogle || []).push({});</script></div>'
)
idx = idx.replace(IDX_BLOCK1, TPL_INDEX)

# 广告块 2 —— main 内，带 margin-bottom wrapper（多行）
IDX_BLOCK2 = (
    '    <!-- AD_PLACEHOLDER -->\n'
    '    <div class="ad-slot">\n'
    '      <ins class="adsbygoogle adsense-placeholder" style="display:block" '
    'data-ad-client="ca-pub-1638874323475457" data-ad-slot="1234567890" '
    'data-ad-format="auto" data-full-width-responsive="true"></ins>\n'
    '      <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>\n'
    '    </div>'
)
idx = idx.replace(IDX_BLOCK2, TPL_INDEX)

# 广告块 3 —— pagination 下方（单行）
IDX_BLOCK3 = (
    '  <!-- AD_PLACEHOLDER -->\n'
    '<div class="ad-slot">Advertisement\n'
    '<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-1638874323475457" '
    'data-ad-slot="3456789012" data-ad-format="auto" data-full-width-responsive="true">'
    '</ins><script>(adsbygoogle = window.adsbygoogle || []).push({});</script></div>'
)
idx = idx.replace(IDX_BLOCK3, TPL_INDEX)

if idx != orig_idx:
    with open("index.html", "w", encoding="utf-8") as fh:
        fh.write(idx)
    print("index.html        : updated")
else:
    print("index.html        : NO CHANGE — check patterns")

# ══════════════════════════════════════════════════════════════════
# 最终验证
# ══════════════════════════════════════════════════════════════════
def check(path, label):
    c = open(path, encoding="utf-8").read()
    print(f"\n{label}:")
    print(f"  adsbygoogle removed : {'adsbygoogle' not in c}")
    print(f"  ad-slot CSS removed : {'.ad-slot{' not in c}")
    print(f"  ADVERTISEMENT shown : {'ADVERTISEMENT' in c}")
    print(f"  new template used   : {'max-width:728px' in c or 'max-width:468px' in c}")

check("index.html", "index.html")
check("tools/salary-calculator.html", "tools/salary-calculator.html")
check("tools/paycheck-calculator.html", "tools/paycheck-calculator.html")
