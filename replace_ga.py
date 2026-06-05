import os, glob

GA_CODE = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-PLWJ8VEN8D"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-PLWJ8VEN8D');
</script>"""

os.chdir(r"C:\Users\Administrator\payrollfixpro")
files = glob.glob("*.html") + glob.glob("tools/*.html")
count = 0
for f in files:
    with open(f, "r", encoding="utf-8") as fh:
        content = fh.read()
    if "<!-- GA_PLACEHOLDER -->" in content:
        content = content.replace("<!-- GA_PLACEHOLDER -->", GA_CODE)
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(content)
        count += 1

print(f"Updated {count} files with GA ID G-PLWJ8VEN8D")
