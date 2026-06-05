import os, glob

os.chdir(r"C:\Users\Administrator\payrollfixpro")

# ─── CSS 修复：去掉 min-height，ins 元素折叠到 0 高度 ───────────────────────

# 工具页 .ad-slot（带 min-height:90px）
OLD_TOOL_CSS = (
    ".ad-slot{background:#fff;border:1px dashed #cbd5e1;border-radius:12px;"
    "padding:20px;text-align:center;color:#94a3b8;font-size:12px;"
    "letter-spacing:.5px;text-transform:uppercase;margin:24px 0;"
    "min-height:90px;display:flex;align-items:center;justify-content:center;"
    "flex-direction:column;gap:8px}"
)
NEW_TOOL_CSS = (
    ".ad-slot{background:#fff;border:1px dashed #cbd5e1;border-radius:12px;"
    "padding:16px 20px;text-align:center;color:#94a3b8;font-size:12px;"
    "letter-spacing:.5px;text-transform:uppercase;margin:20px 0;"
    "display:flex;align-items:center;justify-content:center;"
    "flex-direction:column}"
)

# adsense-placeholder：未渲染时高度折叠为 0
OLD_PH = ".adsense-placeholder{width:100%;display:block}"
NEW_PH = ".adsense-placeholder{display:block;width:100%;height:0;overflow:hidden}"

# index.html 的 .ad-slot CSS 不同（margin 不同）
# 同样去掉 min-height
OLD_IDX_CSS = (
    ".ad-slot{background:#fff;border:1px dashed #cbd5e1;border-radius:12px;"
    "padding:20px;text-align:center;color:#94a3b8;font-size:12px;"
    "letter-spacing:.5px;text-transform:uppercase;margin:24px 0;"
    "min-height:90px;display:flex;align-items:center;justify-content:center;"
    "flex-direction:column;gap:8px}"
)
NEW_IDX_CSS = NEW_TOOL_CSS   # 相同样式

# ─── 处理工具页（100 个）──────────────────────────────────────────────────
tool_files = glob.glob("tools/*.html")
tool_count = 0

for f in tool_files:
    with open(f, "r", encoding="utf-8") as fh:
        c = fh.read()
    orig = c
    c = c.replace(OLD_TOOL_CSS, NEW_TOOL_CSS)
    c = c.replace(OLD_PH, NEW_PH)
    if c != orig:
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(c)
        tool_count += 1

print(f"Tool pages updated : {tool_count} / {len(tool_files)}")

# ─── 处理 index.html ──────────────────────────────────────────────────────
with open("index.html", "r", encoding="utf-8") as fh:
    idx = fh.read()
orig_idx = idx

idx = idx.replace(OLD_IDX_CSS, NEW_IDX_CSS)
idx = idx.replace(OLD_PH,      NEW_PH)

# index.html 的 adsense-placeholder 可能是另一个写法
idx = idx.replace(
    ".adsense-placeholder{width:100%;display:block}",
    NEW_PH
)

changed_idx = idx != orig_idx
if changed_idx:
    with open("index.html", "w", encoding="utf-8") as fh:
        fh.write(idx)
    print("index.html         : updated")
else:
    print("index.html         : no change (CSS pattern may differ, check below)")

# ─── 验证 ─────────────────────────────────────────────────────────────────
s = open("tools/salary-calculator.html", encoding="utf-8").read()
print("\nVerify tools/salary-calculator.html:")
print("  min-height removed      :", "min-height:90px" not in s)
print("  ins height:0            :", "height:0;overflow:hidden" in s)
print("  dashed border kept      :", "border:1px dashed #cbd5e1" in s)
print("  padding kept            :", "padding:16px 20px" in s)
print("  Advertisement text kept :", "Advertisement" in s)

ix = open("index.html", encoding="utf-8").read()
print("\nVerify index.html:")
print("  min-height removed      :", "min-height:90px" not in ix)
print("  ins height:0            :", "height:0;overflow:hidden" in ix)
