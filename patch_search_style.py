with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_search = '''  <div class="search-wrap" style="margin-bottom:20px;max-width:480px">
    <svg class="search-icon" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><line x1="16.5" y1="16.5" x2="22" y2="22"/></svg>
    <input type="text" id="search" placeholder="Search 100+ payroll calculators..." oninput="renderTools()" style="width:100%;padding:10px 16px 10px 40px;border:1.5px solid var(--border);border-radius:var(--radius-sm);font-size:14px;outline:none;transition:border-color .15s">
  </div>'''

new_search = '''  <div style="margin-bottom:28px">
    <div style="position:relative;max-width:560px">
      <svg style="position:absolute;left:16px;top:50%;transform:translateY(-50%);width:18px;height:18px;stroke:var(--text3);fill:none;stroke-width:2;stroke-linecap:round" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><line x1="16.5" y1="16.5" x2="22" y2="22"/></svg>
      <input type="text" id="search" placeholder="Search 100+ payroll calculators..." oninput="renderTools()"
        style="width:100%;padding:13px 20px 13px 48px;border:1.5px solid var(--border);border-radius:40px;font-size:15px;font-family:inherit;color:var(--text);background:#fff;outline:none;box-shadow:0 2px 8px rgba(0,0,0,.06);transition:all .2s"
        onfocus="this.style.borderColor='var(--primary)';this.style.boxShadow='0 2px 12px rgba(15,118,110,.15)'"
        onblur="this.style.borderColor='var(--border)';this.style.boxShadow='0 2px 8px rgba(0,0,0,.06)'">
    </div>
  </div>'''

result = content.replace(old_search, new_search)
if result == content:
    print("WARNING: pattern not found, no changes made")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(result)
    print("done")
