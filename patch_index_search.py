with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. header 里移除 search-wrap，只保留 logo
old_header = '''    <a href="/" class="logo">Payroll<span>Fix</span>Pro</a>
    <div class="search-wrap">
      <svg class="search-icon" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><line x1="16.5" y1="16.5" x2="22" y2="22"/></svg>
      <input type="text" id="search" placeholder="Search calculators..." oninput="renderTools()">
    </div>'''

new_header = '''    <a href="/" class="logo"><img src="/logo.svg" alt="PayrollFixPro" height="36"></a>'''

content = content.replace(old_header, new_header)

# 2. 分类标签上方插入搜索框
old_cattabs = '''  <div class="cat-tabs" id="catTabs">'''

new_search_and_tabs = '''  <div class="search-wrap" style="margin-bottom:20px;max-width:480px">
    <svg class="search-icon" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><line x1="16.5" y1="16.5" x2="22" y2="22"/></svg>
    <input type="text" id="search" placeholder="Search 100+ payroll calculators..." oninput="renderTools()" style="width:100%;padding:10px 16px 10px 40px;border:1.5px solid var(--border);border-radius:var(--radius-sm);font-size:14px;outline:none;transition:border-color .15s">
  </div>
  <div class="cat-tabs" id="catTabs">'''

content = content.replace(old_cattabs, new_search_and_tabs)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("done")
