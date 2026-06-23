import glob, re

problems = []
for fpath in glob.glob('tools/*.html'):
    txt = open(fpath, encoding='utf-8', errors='ignore').read()
    scripts = re.findall(r'<script>([\s\S]*?)</script>', txt)
    for script in scripts:
        matches = re.findall(r"'[^']*\b\w+'s\s\w[^']*'", script)
        if matches:
            problems.append((fpath, matches[0][:80]))

if problems:
    print(f"FOUND {len(problems)} files with apostrophe issues:")
    for f, m in problems:
        print(f"  {f}: {m}")
else:
    print("ALL CLEAN")
