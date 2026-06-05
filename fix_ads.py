import os, glob

os.chdir(r"C:\Users\Administrator\payrollfixpro")

OLD_SLOT = (
    ".ad-slot{width:100%;background:#f1f5f9;border:1px dashed #cbd5e1;"
    "border-radius:var(--radius-sm);display:flex;align-items:center;"
    "justify-content:center;color:var(--text3);font-size:12px;"
    "letter-spacing:.5px;text-transform:uppercase}"
)
NEW_SLOT = ".ad-slot{width:100%;min-height:90px;overflow:hidden}"

OLD_SIZES = ".ad-top{height:90px;min-height:90px}.ad-middle{min-height:90px;margin-bottom:24px}.ad-bottom{min-height:90px}"
NEW_SIZES = ".ad-top{min-height:90px}.ad-middle{min-height:90px;margin-bottom:24px}.ad-bottom{min-height:90px}"

files = glob.glob("tools/*.html")
count = 0
for f in files:
    with open(f, "r", encoding="utf-8") as fh:
        content = fh.read()
    new = content.replace(OLD_SLOT, NEW_SLOT).replace(OLD_SIZES, NEW_SIZES)
    if new != content:
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(new)
        count += 1

print(f"Updated {count} tool pages")

# Verify one file
sample = open("tools/salary-calculator.html", encoding="utf-8").read()
print("  no background:", "background:#f1f5f9" not in sample)
print("  no dashed border:", "1px dashed" not in sample)
print("  min-height kept:", "min-height:90px" in sample)
