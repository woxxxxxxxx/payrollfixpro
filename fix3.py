import os, glob

os.chdir(r"C:\Users\Administrator\payrollfixpro")

# ── Fix 1: breadcrumb separator in all tool pages ──────────────────────────
tool_files = glob.glob("tools/*.html")
bc_fixed = 0
for f in tool_files:
    with open(f, "r", encoding="utf-8") as fh:
        content = fh.read()
    # Replace the raw › character inside breadcrumb span with &rsaquo;
    new = content.replace("<span>›</span>", "<span>&rsaquo;</span>")
    if new != content:
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(new)
        bc_fixed += 1
print(f"Fix 1 breadcrumb: {bc_fixed} tool pages updated")

# ── Fix 2 + 3: index.html – ad height + btt button ────────────────────────
with open("index.html", "r", encoding="utf-8") as fh:
    idx = fh.read()

# Fix 2: ad-top min-height instead of fixed height
idx = idx.replace(
    ".ad-top{height:90px;margin:24px 0 0}",
    ".ad-top{min-height:90px;margin:24px 0 0}"
)

# Fix 3: btt button – replace old round blue style with new rect teal style
OLD_BTT_CSS = (
    "#btt{position:fixed;bottom:28px;right:28px;width:42px;height:42px;"
    "background:var(--primary);color:#fff;border:none;border-radius:50%;"
    "font-size:18px;cursor:pointer;display:none;z-index:999;"
    "box-shadow:0 2px 8px rgba(15,118,110,.35)}"
)
NEW_BTT_CSS = (
    "#btt{position:fixed;bottom:24px;right:24px;"
    "background:#fff;border:2px solid #0f766e;border-radius:8px;"
    "padding:8px 12px;color:#0f766e;font-size:14px;font-weight:700;"
    "cursor:pointer;display:none;z-index:999;"
    "box-shadow:0 2px 8px rgba(15,118,110,.15);transition:all .15s}"
    "#btt:hover{background:#f0fdfa}"
)
idx = idx.replace(OLD_BTT_CSS, NEW_BTT_CSS)

# Also fix the display toggle: was 'flex', should be 'block'
idx = idx.replace(
    "document.getElementById('btt').style.display=window.scrollY>400?'flex':'none'",
    "document.getElementById('btt').style.display=window.scrollY>400?'block':'none'"
)

with open("index.html", "w", encoding="utf-8") as fh:
    fh.write(idx)
print("Fix 2+3 index.html: ad-top min-height + btt style updated")

# Verify
with open("index.html", "r", encoding="utf-8") as fh:
    check = fh.read()
print("  ad-top min-height:", "min-height:90px" in check)
print("  btt border:2px solid:", "border:2px solid #0f766e" in check)
print("  btt border-radius:8px:", "border-radius:8px" in check)
print("Done.")
