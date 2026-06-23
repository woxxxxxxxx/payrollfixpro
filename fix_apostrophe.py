import glob, re

fixed = 0
for fpath in glob.glob('tools/*.html'):
    txt = open(fpath, encoding='utf-8', errors='ignore').read()
    scripts = re.findall(r'(<script>[\s\S]*?</script>)', txt)
    new_txt = txt
    for script in scripts:
        fixed_script = re.sub(r"('[^']*\w)'(s\s)", lambda m: m.group(0).replace("'s ", "\\'s "), script)
        if fixed_script != script:
            new_txt = new_txt.replace(script, fixed_script)
            fixed += 1
    if new_txt != txt:
        open(fpath, 'w', encoding='utf-8').write(new_txt)

print(f"Fixed apostrophes in {fixed} files")
