import os

os.chdir(r"C:\Users\Administrator\payrollfixpro")

# ─────────────────────────────────────────────────────────────
# 公共旧块（3个文件模板一致）
# ─────────────────────────────────────────────────────────────
OLD_FORM = """  <div class="form-card">
    <h2>Enter Your Information</h2>
    <div class="form-grid">
<div class="field"><label>Amount ($)</label><input id="gross" type="number" value="60000" step="1000" min="0"></div>
<div class="field"><label>Pay Period</label><select id="period"><option value="annual">Annual</option><option value="monthly">Monthly</option><option value="biweekly">Biweekly</option><option value="weekly">Weekly</option><option value="hourly">Hourly</option></select></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate</button>
  </div>
  <div class="result-card" id="result">
    <h2>Your Results</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Annual</div><div class="result-value" id="r-annual">—</div></div>
<div class="result-item"><div class="result-label">Monthly</div><div class="result-value" id="r-monthly">—</div></div>
<div class="result-item"><div class="result-label">Biweekly</div><div class="result-value" id="r-biweekly">—</div></div>
<div class="result-item"><div class="result-label">Hourly</div><div class="result-value" id="r-hourly">—</div></div>

    </div>
  </div>"""

OLD_SCRIPT = """<script>

function calc(){
  var gross=parseFloat(document.getElementById('gross').value)||0;
  var period=document.getElementById('period').value;
  var mult={'annual':1,'monthly':12,'biweekly':26,'weekly':52,'hourly':2080};
  var annual=gross*(mult[period]||1);
  var monthly=annual/12;
  var biweekly=annual/26;
  var hourly=annual/2080;
  document.getElementById('r-annual').textContent='$'+annual.toLocaleString('en-US',{maximumFractionDigits:2});
  document.getElementById('r-monthly').textContent='$'+monthly.toLocaleString('en-US',{maximumFractionDigits:2});
  document.getElementById('r-biweekly').textContent='$'+biweekly.toLocaleString('en-US',{maximumFractionDigits:2});
  document.getElementById('r-hourly').textContent='$'+hourly.toFixed(2);
  document.getElementById('result').classList.add('show');
}
</script>"""

# ─────────────────────────────────────────────────────────────
# 共用 JS 计算函数（嵌入每个工具的 <script> 块）
# ─────────────────────────────────────────────────────────────
SHARED_JS_FUNCS = """
// 2026 Federal Tax Brackets + Standard Deductions
function calcFedTax(annualIncome, status) {
  const std = {single:15000, mfj:30000, mfs:15000, hoh:22500};
  const brackets = {
    single: [[11925,.10],[48475,.12],[103350,.22],[197300,.24],[250525,.32],[626350,.35],[Infinity,.37]],
    mfj:    [[23850,.10],[96950,.12],[206700,.22],[394600,.24],[501050,.32],[751600,.35],[Infinity,.37]],
    mfs:    [[11925,.10],[48475,.12],[103350,.22],[197300,.24],[250525,.32],[375800,.35],[Infinity,.37]],
    hoh:    [[17000,.10],[64300,.12],[103350,.22],[197300,.24],[250500,.32],[626350,.35],[Infinity,.37]]
  };
  const taxable = Math.max(0, annualIncome - (std[status]||15000));
  const b = brackets[status] || brackets.single;
  let tax = 0, prev = 0;
  for (let i=0;i<b.length;i++){
    const [upper, rate] = b[i];
    if (taxable <= prev) break;
    tax += (Math.min(taxable, upper) - prev) * rate;
    prev = upper;
  }
  return Math.max(0, tax);
}

// State tax rates (2026 approximate)
const STATE_RATES = {
  "0":    {label:"No State Tax (TX/FL/WA/NV/SD/WY/AK)", rate:0},
  "IL":   {label:"Illinois",          rate:0.0495},
  "PA":   {label:"Pennsylvania",      rate:0.0307},
  "IN":   {label:"Indiana",           rate:0.0315},
  "MI":   {label:"Michigan",          rate:0.0405},
  "CO":   {label:"Colorado",          rate:0.0440},
  "UT":   {label:"Utah",              rate:0.0455},
  "AZ":   {label:"Arizona",           rate:0.0250},
  "MA":   {label:"Massachusetts",     rate:0.0500},
  "NC":   {label:"North Carolina",    rate:0.0475},
  "GA":   {label:"Georgia",           rate:0.0549},
  "VA":   {label:"Virginia",          rate:0.0575},
  "MD":   {label:"Maryland (state)",  rate:0.0500},
  "OH":   {label:"Ohio",              rate:0.0350},
  "NJ":   {label:"New Jersey",        rate:0.0637},
  "NY":   {label:"New York (~mid)",   rate:0.0625},
  "CA":   {label:"California (~mid)", rate:0.0930},
};

function fmt(n){ return '$'+n.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2}); }
function pct(n){ return (n*100).toFixed(2)+'%'; }
function set(id,v){ const e=document.getElementById(id); if(e) e.textContent=v; }
"""

# ─────────────────────────────────────────────────────────────
# 1. PAYCHECK CALCULATOR
# ─────────────────────────────────────────────────────────────
PAYCHECK_FORM = """  <div class="form-card">
    <h2>Enter Your Payroll Details</h2>
    <div class="form-grid">
      <div class="field">
        <label>Annual Gross Salary ($)</label>
        <input id="salary" type="number" value="65000" step="1000" min="0">
      </div>
      <div class="field">
        <label>Pay Frequency</label>
        <select id="freq">
          <option value="26">Biweekly (every 2 weeks)</option>
          <option value="24">Semi-monthly (2× / month)</option>
          <option value="12">Monthly</option>
          <option value="52">Weekly</option>
          <option value="1">Annual lump sum</option>
        </select>
      </div>
      <div class="field">
        <label>Filing Status</label>
        <select id="filing">
          <option value="single">Single</option>
          <option value="mfj">Married Filing Jointly</option>
          <option value="mfs">Married Filing Separately</option>
          <option value="hoh">Head of Household</option>
        </select>
      </div>
      <div class="field">
        <label>State</label>
        <select id="state">
          <option value="0">No State Tax (TX/FL/WA/NV…)</option>
          <option value="AZ">Arizona (2.50%)</option>
          <option value="CA">California (~9.30%)</option>
          <option value="CO">Colorado (4.40%)</option>
          <option value="GA">Georgia (5.49%)</option>
          <option value="IL">Illinois (4.95%)</option>
          <option value="IN">Indiana (3.15%)</option>
          <option value="MA">Massachusetts (5.00%)</option>
          <option value="MD">Maryland (5.00%)</option>
          <option value="MI">Michigan (4.05%)</option>
          <option value="NJ">New Jersey (6.37%)</option>
          <option value="NC">North Carolina (4.75%)</option>
          <option value="NY">New York (~6.25%)</option>
          <option value="OH">Ohio (~3.50%)</option>
          <option value="PA">Pennsylvania (3.07%)</option>
          <option value="UT">Utah (4.55%)</option>
          <option value="VA">Virginia (5.75%)</option>
        </select>
      </div>
      <div class="field">
        <label>401(k) Contribution (%)</label>
        <input id="k401" type="number" value="5" step="0.5" min="0" max="23">
      </div>
      <div class="field">
        <label>Health / Dental / Vision Pre-tax ($/paycheck)</label>
        <input id="health" type="number" value="0" step="10" min="0">
      </div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate Paycheck</button>
  </div>
  <div class="result-card" id="result">
    <h2>Per-Paycheck Breakdown</h2>
    <div class="result-grid">
      <div class="result-item"><div class="result-label">Gross Pay</div><div class="result-value" id="r-gross">—</div></div>
      <div class="result-item"><div class="result-label">401(k) + Benefits</div><div class="result-value" id="r-pretax">—</div></div>
      <div class="result-item"><div class="result-label">Federal Income Tax</div><div class="result-value" id="r-fed">—</div></div>
      <div class="result-item"><div class="result-label">Social Security (6.2%)</div><div class="result-value" id="r-ss">—</div></div>
      <div class="result-item"><div class="result-label">Medicare (1.45%)</div><div class="result-value" id="r-med">—</div></div>
      <div class="result-item"><div class="result-label">State Income Tax</div><div class="result-value" id="r-state">—</div></div>
      <div class="result-item" style="background:var(--primary);border-color:var(--primary)">
        <div class="result-label" style="color:rgba(255,255,255,.8)">Net Take-Home Pay</div>
        <div class="result-value" style="color:#fff" id="r-net">—</div>
      </div>
    </div>
    <div style="margin-top:18px;padding:14px;background:rgba(15,118,110,.06);border-radius:8px;font-size:13px;color:var(--text2);line-height:2">
      <strong>Annual Summary:</strong>
      Gross <span id="a-gross">—</span> &nbsp;|&nbsp;
      Federal <span id="a-fed">—</span> &nbsp;|&nbsp;
      FICA <span id="a-fica">—</span> &nbsp;|&nbsp;
      State <span id="a-state">—</span> &nbsp;|&nbsp;
      <strong>Net <span id="a-net">—</span></strong>
    </div>
  </div>"""

PAYCHECK_SCRIPT = """<script>
""" + SHARED_JS_FUNCS + """
function calc(){
  const salary  = parseFloat(document.getElementById('salary').value)  || 0;
  const freq    = parseInt(document.getElementById('freq').value)       || 26;
  const status  = document.getElementById('filing').value;
  const stKey   = document.getElementById('state').value;
  const stRate  = (STATE_RATES[stKey] || {rate:0}).rate;
  const k401pct = Math.min(23, parseFloat(document.getElementById('k401').value)||0) / 100;
  const healthPP= parseFloat(document.getElementById('health').value)   || 0;

  // Annual pre-tax deductions
  const ann401k   = salary * k401pct;
  const annHealth = healthPP * freq;
  const annPreTax = ann401k + annHealth;

  // Taxable income (pre-tax deductions reduce federal & state base)
  const annTaxable = Math.max(0, salary - annPreTax);

  // Taxes
  const annFed   = calcFedTax(annTaxable, status);
  const ssCap    = 176100; // 2026 SS wage base
  const annSS    = Math.min(salary, ssCap) * 0.062;
  const annMed   = salary * 0.0145 + (salary > 200000 ? (salary - 200000) * 0.009 : 0);
  const annState = annTaxable * stRate;
  const annNet   = salary - annFed - annSS - annMed - annState - annPreTax;

  // Per-paycheck
  const pp = v => fmt(v / freq);
  set('r-gross',  pp(salary));
  set('r-pretax', pp(annPreTax));
  set('r-fed',    pp(annFed));
  set('r-ss',     pp(annSS));
  set('r-med',    pp(annMed));
  set('r-state',  pp(annState));
  set('r-net',    pp(annNet));

  // Annual
  set('a-gross', fmt(salary));
  set('a-fed',   fmt(annFed));
  set('a-fica',  fmt(annSS + annMed));
  set('a-state', fmt(annState));
  set('a-net',   fmt(annNet));

  document.getElementById('result').classList.add('show');
}
</script>"""

# ─────────────────────────────────────────────────────────────
# 2. TAKE-HOME PAY CALCULATOR
# ─────────────────────────────────────────────────────────────
TAKEHOME_FORM = """  <div class="form-card">
    <h2>Enter Your Details</h2>
    <div class="form-grid">
      <div class="field">
        <label>Annual Gross Salary ($)</label>
        <input id="salary" type="number" value="65000" step="1000" min="0">
      </div>
      <div class="field">
        <label>Filing Status</label>
        <select id="filing">
          <option value="single">Single</option>
          <option value="mfj">Married Filing Jointly</option>
          <option value="mfs">Married Filing Separately</option>
          <option value="hoh">Head of Household</option>
        </select>
      </div>
      <div class="field">
        <label>State</label>
        <select id="state">
          <option value="0">No State Tax (TX/FL/WA/NV…)</option>
          <option value="AZ">Arizona (2.50%)</option>
          <option value="CA">California (~9.30%)</option>
          <option value="CO">Colorado (4.40%)</option>
          <option value="GA">Georgia (5.49%)</option>
          <option value="IL">Illinois (4.95%)</option>
          <option value="IN">Indiana (3.15%)</option>
          <option value="MA">Massachusetts (5.00%)</option>
          <option value="MD">Maryland (5.00%)</option>
          <option value="MI">Michigan (4.05%)</option>
          <option value="NJ">New Jersey (6.37%)</option>
          <option value="NC">North Carolina (4.75%)</option>
          <option value="NY">New York (~6.25%)</option>
          <option value="OH">Ohio (~3.50%)</option>
          <option value="PA">Pennsylvania (3.07%)</option>
          <option value="UT">Utah (4.55%)</option>
          <option value="VA">Virginia (5.75%)</option>
        </select>
      </div>
      <div class="field">
        <label>401(k) Contribution (%)</label>
        <input id="k401" type="number" value="5" step="0.5" min="0" max="23">
      </div>
      <div class="field">
        <label>Health Insurance Pre-tax ($/mo)</label>
        <input id="health" type="number" value="0" step="10" min="0">
      </div>
      <div class="field">
        <label>Hours per Week (for hourly rate)</label>
        <input id="hours" type="number" value="40" step="1" min="1" max="80">
      </div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate Take-Home Pay</button>
  </div>
  <div class="result-card" id="result">
    <h2>Your Take-Home Pay</h2>
    <div class="result-grid">
      <div class="result-item" style="background:var(--primary);border-color:var(--primary)">
        <div class="result-label" style="color:rgba(255,255,255,.8)">Annual Take-Home</div>
        <div class="result-value" style="color:#fff" id="r-annual">—</div>
      </div>
      <div class="result-item" style="background:var(--primary-light);border-color:var(--primary)">
        <div class="result-label">Monthly Take-Home</div>
        <div class="result-value" id="r-monthly">—</div>
      </div>
      <div class="result-item">
        <div class="result-label">Biweekly Take-Home</div>
        <div class="result-value" id="r-biweekly">—</div>
      </div>
      <div class="result-item">
        <div class="result-label">Weekly Take-Home</div>
        <div class="result-value" id="r-weekly">—</div>
      </div>
      <div class="result-item">
        <div class="result-label">Daily Take-Home</div>
        <div class="result-value" id="r-daily">—</div>
      </div>
      <div class="result-item">
        <div class="result-label">Hourly Take-Home</div>
        <div class="result-value" id="r-hourly">—</div>
      </div>
    </div>
    <div style="margin-top:18px;padding:14px;background:rgba(15,118,110,.06);border-radius:8px;font-size:13px;color:var(--text2);line-height:2">
      <strong>Deductions from $<span id="d-gross">—</span> gross:</strong>
      Federal <span id="d-fed">—</span> &nbsp;|&nbsp;
      SS + Medicare <span id="d-fica">—</span> &nbsp;|&nbsp;
      State <span id="d-state">—</span> &nbsp;|&nbsp;
      401(k)/Benefits <span id="d-pretax">—</span> &nbsp;|&nbsp;
      <strong>Take-Home Rate <span id="d-rate">—</span></strong>
    </div>
  </div>"""

TAKEHOME_SCRIPT = """<script>
""" + SHARED_JS_FUNCS + """
function calc(){
  const salary  = parseFloat(document.getElementById('salary').value)  || 0;
  const status  = document.getElementById('filing').value;
  const stKey   = document.getElementById('state').value;
  const stRate  = (STATE_RATES[stKey] || {rate:0}).rate;
  const k401pct = Math.min(23, parseFloat(document.getElementById('k401').value)||0) / 100;
  const healthMo= parseFloat(document.getElementById('health').value)  || 0;
  const hours   = parseFloat(document.getElementById('hours').value)   || 40;

  const annHealth = healthMo * 12;
  const ann401k   = salary * k401pct;
  const annPreTax = ann401k + annHealth;
  const annTaxable= Math.max(0, salary - annPreTax);

  const annFed  = calcFedTax(annTaxable, status);
  const ssCap   = 176100;
  const annSS   = Math.min(salary, ssCap) * 0.062;
  const annMed  = salary * 0.0145 + (salary > 200000 ? (salary - 200000) * 0.009 : 0);
  const annState= annTaxable * stRate;
  const annNet  = salary - annFed - annSS - annMed - annState - annPreTax;
  const annHours= hours * 52;

  set('r-annual',   fmt(annNet));
  set('r-monthly',  fmt(annNet / 12));
  set('r-biweekly', fmt(annNet / 26));
  set('r-weekly',   fmt(annNet / 52));
  set('r-daily',    fmt(annNet / 260));
  set('r-hourly',   fmt(annNet / annHours));

  set('d-gross',  salary.toLocaleString('en-US',{maximumFractionDigits:0}));
  set('d-fed',    fmt(annFed));
  set('d-fica',   fmt(annSS + annMed));
  set('d-state',  fmt(annState));
  set('d-pretax', fmt(annPreTax));
  set('d-rate',   (annNet / salary * 100).toFixed(1) + '%');

  document.getElementById('result').classList.add('show');
}
</script>"""

# ─────────────────────────────────────────────────────────────
# 3. FEDERAL WITHHOLDING CALCULATOR
# ─────────────────────────────────────────────────────────────
WITHHOLDING_FORM = """  <div class="form-card">
    <h2>Enter Your W-4 &amp; Pay Information</h2>
    <div class="form-grid">
      <div class="field">
        <label>Gross Wages per Paycheck ($)</label>
        <input id="wages" type="number" value="2500" step="100" min="0">
      </div>
      <div class="field">
        <label>Pay Frequency (periods per year)</label>
        <select id="freq">
          <option value="26">Biweekly — 26 periods</option>
          <option value="24">Semi-monthly — 24 periods</option>
          <option value="12">Monthly — 12 periods</option>
          <option value="52">Weekly — 52 periods</option>
          <option value="4">Quarterly — 4 periods</option>
        </select>
      </div>
      <div class="field">
        <label>Filing Status (W-4 Step 1c)</label>
        <select id="filing">
          <option value="single">Single / Married Filing Separately</option>
          <option value="mfj">Married Filing Jointly (or QSS)</option>
          <option value="hoh">Head of Household</option>
        </select>
      </div>
      <div class="field">
        <label>W-4 Step 3: Dependent Tax Credits ($)</label>
        <input id="step3" type="number" value="0" step="500" min="0"
               placeholder="e.g. 2000 per child under 17">
      </div>
      <div class="field">
        <label>W-4 Step 4b: Extra Deductions above Std. ($, annual)</label>
        <input id="step4b" type="number" value="0" step="500" min="0"
               placeholder="Itemized deductions excess over standard">
      </div>
      <div class="field">
        <label>W-4 Step 4c: Extra Withholding per Period ($)</label>
        <input id="step4c" type="number" value="0" step="10" min="0">
      </div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate Federal Withholding</button>
  </div>
  <div class="result-card" id="result">
    <h2>Federal Withholding Results</h2>
    <div class="result-grid">
      <div class="result-item" style="background:var(--primary);border-color:var(--primary)">
        <div class="result-label" style="color:rgba(255,255,255,.8)">Federal Withholding / Period</div>
        <div class="result-value" style="color:#fff" id="r-pp">—</div>
      </div>
      <div class="result-item">
        <div class="result-label">Annualized Withholding</div>
        <div class="result-value" id="r-ann">—</div>
      </div>
      <div class="result-item">
        <div class="result-label">Effective Withholding Rate</div>
        <div class="result-value" id="r-eff">—</div>
      </div>
      <div class="result-item">
        <div class="result-label">Annualized Gross Wages</div>
        <div class="result-value" id="r-annwages">—</div>
      </div>
      <div class="result-item">
        <div class="result-label">Taxable Wages (after deductions)</div>
        <div class="result-value" id="r-taxable">—</div>
      </div>
      <div class="result-item">
        <div class="result-label">Marginal Tax Bracket</div>
        <div class="result-value" id="r-bracket">—</div>
      </div>
    </div>
    <div style="margin-top:18px;padding:14px;background:rgba(15,118,110,.06);border-radius:8px;font-size:13px;color:var(--text2);line-height:1.9">
      <strong>IRS Pub 15-T Percentage Method (2026)</strong> — Annualized wages minus
      Step 4b deductions and standard deduction, brackets applied, Step 3 credits subtracted,
      divided by pay periods, plus Step 4c extra withholding.
    </div>
  </div>"""

WITHHOLDING_SCRIPT = """<script>
""" + SHARED_JS_FUNCS + """
function getMarginalRate(taxable, status) {
  const brackets = {
    single: [[11925,.10],[48475,.12],[103350,.22],[197300,.24],[250525,.32],[626350,.35],[Infinity,.37]],
    mfj:    [[23850,.10],[96950,.12],[206700,.22],[394600,.24],[501050,.32],[751600,.35],[Infinity,.37]],
    mfs:    [[11925,.10],[48475,.12],[103350,.22],[197300,.24],[250525,.32],[375800,.35],[Infinity,.37]],
    hoh:    [[17000,.10],[64300,.12],[103350,.22],[197300,.24],[250500,.32],[626350,.35],[Infinity,.37]]
  };
  const std = {single:15000,mfj:30000,mfs:15000,hoh:22500};
  const t = Math.max(0, taxable - (std[status]||15000));
  const b = brackets[status] || brackets.single;
  let prev = 0;
  for (let i=0;i<b.length;i++){
    if (t <= b[i][0]) return b[i][1];
    prev = b[i][0];
  }
  return 0.37;
}

function calc(){
  const wages  = parseFloat(document.getElementById('wages').value)  || 0;
  const freq   = parseInt(document.getElementById('freq').value)      || 26;
  const status = document.getElementById('filing').value;
  const step3  = parseFloat(document.getElementById('step3').value)  || 0;
  const step4b = parseFloat(document.getElementById('step4b').value) || 0;
  const step4c = parseFloat(document.getElementById('step4c').value) || 0;

  // IRS Pub 15-T Percentage Method — Annualized Wage Bracket
  const annWages   = wages * freq;
  // Subtract Step 4b additional deductions (annual amount)
  const annAdjWages= Math.max(0, annWages - step4b);
  // Compute tentative annual withholding (calcFedTax handles std deduction internally)
  const annTentative = calcFedTax(annAdjWages, status);
  // Subtract Step 3 credits (annual)
  const annTax     = Math.max(0, annTentative - step3);
  // Per-period withholding + Step 4c extra
  const perPeriod  = annTax / freq + step4c;

  const std = {single:15000,mfj:30000,mfs:15000,hoh:22500};
  const taxable = Math.max(0, annAdjWages - (std[status]||15000));
  const mRate = getMarginalRate(annAdjWages, status);
  const effRate = annWages > 0 ? perPeriod * freq / annWages : 0;

  set('r-pp',       fmt(perPeriod));
  set('r-ann',      fmt(perPeriod * freq));
  set('r-eff',      (effRate * 100).toFixed(2) + '%');
  set('r-annwages', fmt(annWages));
  set('r-taxable',  fmt(taxable));
  set('r-bracket',  (mRate * 100).toFixed(0) + '%');

  document.getElementById('result').classList.add('show');
}
</script>"""

# ─────────────────────────────────────────────────────────────
# 写入函数
# ─────────────────────────────────────────────────────────────
def rewrite(filename, new_form, new_script):
    path = f"tools/{filename}"
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    orig = c

    if OLD_FORM not in c:
        print(f"  WARN: OLD_FORM not found in {filename}")
        return False
    if OLD_SCRIPT not in c:
        print(f"  WARN: OLD_SCRIPT not found in {filename}")
        return False

    c = c.replace(OLD_FORM, new_form, 1)
    c = c.replace(OLD_SCRIPT, new_script, 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(c)

    # 验证
    has_form = 'onclick="calc()"' in c
    has_script = "calcFedTax" in c
    has_result = 'result-card' in c
    print(f"  {filename}: form={has_form} script={has_script} result={has_result}")
    return c != orig

print("=== Rewriting P1 tools ===")
r1 = rewrite("paycheck-calculator.html",         PAYCHECK_FORM,    PAYCHECK_SCRIPT)
r2 = rewrite("take-home-pay-calculator.html",     TAKEHOME_FORM,    TAKEHOME_SCRIPT)
r3 = rewrite("federal-withholding-calculator.html", WITHHOLDING_FORM, WITHHOLDING_SCRIPT)

print(f"\nFiles changed: {sum([r1,r2,r3])}/3")
