"""
Batch A: 差异化重写 ~30 个换皮工具
Groups: Freelance/SE, International, Capital gains/RSU/Stock, Leave, Payroll/HR
"""
import os
os.chdir(r"C:\Users\Administrator\payrollfixpro")

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

def fmt_js(): return """function fmt(n){return'$'+Math.round(n).toLocaleString('en-US');}
function fmtd(n){return'$'+n.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}
function set(id,v){document.getElementById(id).textContent=v;}"""

def fed_tax_js(): return """function calcFedTax(inc,status){
  const std={single:15000,mfj:30000,mfs:15000,hoh:22500};
  const br={
    single:[[11925,.10],[48475,.12],[103350,.22],[197300,.24],[250525,.32],[626350,.35],[Infinity,.37]],
    mfj:   [[23850,.10],[96950,.12],[206700,.22],[394600,.24],[501050,.32],[751600,.35],[Infinity,.37]],
    mfs:   [[11925,.10],[48475,.12],[103350,.22],[197300,.24],[250525,.32],[375800,.35],[Infinity,.37]],
    hoh:   [[17000,.10],[64300,.12],[103350,.22],[197300,.24],[250500,.32],[626350,.35],[Infinity,.37]]
  };
  const taxable=Math.max(0,inc-(std[status]||15000));
  const b=br[status]||br.single;
  let tax=0,prev=0;
  for(let i=0;i<b.length;i++){const[u,r]=b[i];if(taxable<=prev)break;tax+=(Math.min(taxable,u)-prev)*r;prev=u;}
  return tax;
}"""

# ════════════════════════════════════════════════════════
# GROUP 1: Freelance / Self-employed / 1099
# Shared form + script applied to 9 tools
# ════════════════════════════════════════════════════════
SE_FORM = """  <div class="form-card">
    <h2>Enter Your Information</h2>
    <div class="form-grid">
<div class="field"><label>Net Self-Employment Income ($)</label><input id="seinc" type="number" value="80000" step="1000" min="0"></div>
<div class="field"><label>Filing Status</label><select id="status"><option value="single">Single</option><option value="mfj">Married Filing Jointly</option><option value="hoh">Head of Household</option></select></div>
<div class="field"><label>Business Expenses ($)</label><input id="expenses" type="number" value="5000" step="500" min="0"></div>
<div class="field"><label>Retirement Contributions (SEP/Solo 401k $)</label><input id="retire" type="number" value="0" step="500" min="0"></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate</button>
  </div>
  <div class="result-card" id="result">
    <h2>Self-Employment Tax Breakdown</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Net Profit (after expenses)</div><div class="result-value" id="r-profit">—</div></div>
<div class="result-item"><div class="result-label">SE Tax (15.3%)</div><div class="result-value" id="r-se" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">½ SE Tax Deduction</div><div class="result-value" id="r-half">—</div></div>
<div class="result-item"><div class="result-label">Federal Income Tax</div><div class="result-value" id="r-fed" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">Total Tax Burden</div><div class="result-value" id="r-total" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">Est. Net Take-Home</div><div class="result-value" id="r-net">—</div></div>
<div class="result-item"><div class="result-label">Effective Tax Rate</div><div class="result-value" id="r-rate">—</div></div>
<div class="result-item"><div class="result-label">Quarterly Est. Payment</div><div class="result-value" id="r-qtr">—</div></div>
    </div>
  </div>"""

SE_SCRIPT = f"""<script>
{fmt_js()}
{fed_tax_js()}
function calc(){{
  const seinc=parseFloat(document.getElementById('seinc').value)||0;
  const status=document.getElementById('status').value;
  const expenses=parseFloat(document.getElementById('expenses').value)||0;
  const retire=parseFloat(document.getElementById('retire').value)||0;
  const profit=Math.max(0,seinc-expenses);
  // SE tax: 92.35% of net profit × 15.3%
  const seTaxBase=profit*0.9235;
  const seTax=seTaxBase*0.153;
  const halfSE=seTax/2;
  const fedAgi=Math.max(0,profit-halfSE-retire);
  const fedTax=calcFedTax(fedAgi,status);
  const total=seTax+fedTax;
  const net=profit-total;
  const effRate=profit>0?total/profit*100:0;
  set('r-profit',fmt(profit));
  set('r-se',fmt(seTax));
  set('r-half',fmt(halfSE));
  set('r-fed',fmt(fedTax));
  set('r-total',fmt(total));
  set('r-net',fmt(net));
  set('r-rate',effRate.toFixed(1)+'%');
  set('r-qtr',fmt(total/4));
  document.getElementById('result').classList.add('show');
}}
</script>"""

SE_FILES = [
    "tools/1099-tax-calculator.html",
    "tools/billable-hours-calculator.html",
    "tools/freelance-tax-calculator.html",
    "tools/gig-income-calculator.html",
    "tools/independent-contractor-calculator.html",
    "tools/project-rate-calculator.html",
    "tools/self-employed-salary-calculator.html",
    "tools/self-employment-tax-calculator.html",
    "tools/side-hustle-tax-calculator.html",
]

# ════════════════════════════════════════════════════════
# GROUP 2: International
# ════════════════════════════════════════════════════════
def intl_form(country_label, currency, extra_fields=""):
    return f"""  <div class="form-card">
    <h2>Enter Your Information</h2>
    <div class="form-grid">
<div class="field"><label>Annual Gross Salary ({currency})</label><input id="salary" type="number" value="80000" step="1000" min="0"></div>
<div class="field"><label>Filing / Residency Status</label><select id="status"><option value="single">Single / Individual</option><option value="married">Married / Joint</option></select></div>
{extra_fields}
    </div>
    <button class="btn-primary" onclick="calc()">Calculate {country_label} Tax</button>
  </div>
  <div class="result-card" id="result">
    <h2>{country_label} Take-Home Estimate</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Gross Salary</div><div class="result-value" id="r-gross">—</div></div>
<div class="result-item"><div class="result-label">Income Tax</div><div class="result-value" id="r-tax" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">Social Contributions</div><div class="result-value" id="r-social" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">Annual Take-Home</div><div class="result-value" id="r-annual">—</div></div>
<div class="result-item"><div class="result-label">Monthly Take-Home</div><div class="result-value" id="r-monthly">—</div></div>
<div class="result-item"><div class="result-label">Effective Tax Rate</div><div class="result-value" id="r-rate">—</div></div>
    </div>
  </div>"""

# Australia 2025-26 tax brackets (AUD)
AUS_FORM = intl_form("Australia", "AUD",
    '<div class="field"><label>Superannuation Rate (%)</label><input id="super" type="number" value="11.5" step="0.5" min="0" max="30"></div>')
AUS_SCRIPT = f"""<script>
{fmt_js()}
function calcAusTax(inc){{
  const br=[[18200,0],[45000,.19],[120000,.325],[180000,.37],[Infinity,.45]];
  let tax=0,prev=0;
  for(const[u,r]of br){{if(inc<=prev)break;tax+=(Math.min(inc,u)-prev)*r;prev=u;}}
  // Low Income Tax Offset
  let lito=0;
  if(inc<=37500)lito=700;
  else if(inc<=45000)lito=700-(inc-37500)*0.05;
  else if(inc<=66667)lito=325-(inc-45000)*0.015;
  return Math.max(0,tax-lito);
}}
function calc(){{
  const salary=parseFloat(document.getElementById('salary').value)||0;
  const superRate=(parseFloat(document.getElementById('super').value)||0)/100;
  const tax=calcAusTax(salary);
  // Medicare levy 2%
  const medicare=salary*0.02;
  // Superannuation (paid by employer on top, shown as employee cost context)
  const superAmt=salary*superRate;
  const net=salary-tax-medicare;
  document.getElementById('r-gross').textContent='A$'+Math.round(salary).toLocaleString('en-US');
  document.getElementById('r-tax').textContent='A$'+Math.round(tax+medicare).toLocaleString('en-US');
  document.getElementById('r-social').textContent='Super: A$'+Math.round(superAmt).toLocaleString('en-US')+' (employer)';
  document.getElementById('r-annual').textContent='A$'+Math.round(net).toLocaleString('en-US');
  document.getElementById('r-monthly').textContent='A$'+Math.round(net/12).toLocaleString('en-US');
  set('r-rate',(salary>0?(tax+medicare)/salary*100:0).toFixed(1)+'%');
  document.getElementById('result').classList.add('show');
}}
</script>"""

# Canada 2026 federal brackets (CAD) — simplified, no provincial
CAN_FORM = intl_form("Canada", "CAD",
    '<div class="field"><label>Province</label><select id="prov"><option value="0.0505">Ontario (~5.05%)</option><option value="0.10">Quebec (~10%)</option><option value="0.10">British Columbia (~5.06%)</option><option value="0.10">Alberta (10%)</option><option value="0.0879">Manitoba (~8.79%)</option><option value="0.105">Saskatchewan (~10.5%)</option></select></div>')
CAN_SCRIPT = f"""<script>
{fmt_js()}
function calcCanFed(inc){{
  const br=[[57375,.15],[114750,.205],[177882,.26],[253414,.29],[Infinity,.33]];
  const ded=16129; // basic personal amount
  const taxable=Math.max(0,inc-ded);
  let tax=0,prev=0;
  for(const[u,r]of br){{if(taxable<=prev)break;tax+=(Math.min(taxable,u)-prev)*r;prev=u;}}
  return tax;
}}
function calc(){{
  const salary=parseFloat(document.getElementById('salary').value)||0;
  const provRate=parseFloat(document.getElementById('prov').value)||0;
  const fedTax=calcCanFed(salary);
  const provTax=salary*provRate;
  // CPP: 5.95% up to $73,200 (2026 approx); EI: 1.66% up to $63,700
  const cpp=Math.min(salary,73200)*0.0595;
  const ei=Math.min(salary,63700)*0.0166;
  const totalTax=fedTax+provTax+cpp+ei;
  const net=salary-totalTax;
  document.getElementById('r-gross').textContent='C$'+Math.round(salary).toLocaleString('en-US');
  document.getElementById('r-tax').textContent='C$'+Math.round(fedTax+provTax).toLocaleString('en-US');
  document.getElementById('r-social').textContent='CPP+EI: C$'+Math.round(cpp+ei).toLocaleString('en-US');
  document.getElementById('r-annual').textContent='C$'+Math.round(net).toLocaleString('en-US');
  document.getElementById('r-monthly').textContent='C$'+Math.round(net/12).toLocaleString('en-US');
  set('r-rate',(salary>0?totalTax/salary*100:0).toFixed(1)+'%');
  document.getElementById('result').classList.add('show');
}}
</script>"""

# UK 2025-26 (GBP)
UK_FORM = intl_form("UK", "£",
    '<div class="field"><label>Pension Contribution (%)</label><input id="pension" type="number" value="5" step="0.5" min="0" max="100"></div>')
UK_SCRIPT = f"""<script>
{fmt_js()}
function calcUKTax(inc){{
  const PA=12570; // personal allowance
  // taper PA above £100k
  const adjPA=inc>125140?0:inc>100000?Math.max(0,PA-(inc-100000)/2):PA;
  const taxable=Math.max(0,inc-adjPA);
  // Basic 20% up to £37700; Higher 40% up to £125140; Additional 45%
  const basic=Math.min(taxable,37700)*0.20;
  const higher=taxable>37700?Math.min(taxable-37700,125140-12570-37700)*0.40:0;
  const additional=taxable>(125140-adjPA)?(taxable-(125140-adjPA))*0.45:0;
  return basic+higher+additional;
}}
function calc(){{
  const salary=parseFloat(document.getElementById('salary').value)||0;
  const pensionPct=(parseFloat(document.getElementById('pension').value)||0)/100;
  const pension=salary*pensionPct;
  const taxable=salary-pension;
  const tax=calcUKTax(taxable);
  // NI: Class 1 employee — 8% on £12,570–£50,270; 2% above
  const niLow=Math.max(0,Math.min(salary,50270)-12570)*0.08;
  const niHigh=Math.max(0,salary-50270)*0.02;
  const ni=niLow+niHigh;
  const net=salary-tax-ni-pension;
  document.getElementById('r-gross').textContent='£'+Math.round(salary).toLocaleString('en-US');
  document.getElementById('r-tax').textContent='£'+Math.round(tax).toLocaleString('en-US');
  document.getElementById('r-social').textContent='NI: £'+Math.round(ni).toLocaleString('en-US');
  document.getElementById('r-annual').textContent='£'+Math.round(net).toLocaleString('en-US');
  document.getElementById('r-monthly').textContent='£'+Math.round(net/12).toLocaleString('en-US');
  set('r-rate',(salary>0?(tax+ni)/salary*100:0).toFixed(1)+'%');
  document.getElementById('result').classList.add('show');
}}
</script>"""

# Singapore (SGD)
SG_FORM = intl_form("Singapore", "SGD",
    '<div class="field"><label>CPF Contribution Rate</label><select id="cpf"><option value="0.20">Age ≤55 (20%)</option><option value="0.15">Age 56-60 (15%)</option><option value="0.105">Age 61-65 (10.5%)</option><option value="0.075">Age 66-70 (7.5%)</option><option value="0.05">Age >70 (5%)</option></select></div>')
SG_SCRIPT = f"""<script>
{fmt_js()}
function calcSGTax(inc){{
  // Singapore 2024 resident tax rates
  const br=[[20000,0],[10000,.02],[10000,.035],[40000,.07],[40000,.115],[40000,.15],[40000,.18],[40000,.19],[280000,.195],[Infinity,.22]];
  let tax=0,prev=0;
  for(const[band,r]of br){{const upper=prev+band;if(inc<=prev)break;tax+=(Math.min(inc,upper)-prev)*r;prev=upper;}}
  return tax;
}}
function calc(){{
  const salary=parseFloat(document.getElementById('salary').value)||0;
  const cpfRate=parseFloat(document.getElementById('cpf').value)||0;
  // CPF capped at OW ceiling $102,000/yr
  const cpfWages=Math.min(salary,102000);
  const cpf=cpfWages*cpfRate;
  const tax=calcSGTax(salary);
  const net=salary-tax-cpf;
  document.getElementById('r-gross').textContent='S$'+Math.round(salary).toLocaleString('en-US');
  document.getElementById('r-tax').textContent='S$'+Math.round(tax).toLocaleString('en-US');
  document.getElementById('r-social').textContent='CPF: S$'+Math.round(cpf).toLocaleString('en-US');
  document.getElementById('r-annual').textContent='S$'+Math.round(net).toLocaleString('en-US');
  document.getElementById('r-monthly').textContent='S$'+Math.round(net/12).toLocaleString('en-US');
  set('r-rate',(salary>0?(tax+cpf)/salary*100:0).toFixed(1)+'%');
  document.getElementById('result').classList.add('show');
}}
</script>"""

# India (INR) — New Tax Regime FY2025-26
IN_FORM = intl_form("India", "₹",
    '<div class="field"><label>Tax Regime</label><select id="regime"><option value="new">New Regime (default)</option><option value="old">Old Regime</option></select></div>')
IN_SCRIPT = f"""<script>
{fmt_js()}
function calcIndiaTax(inc,regime){{
  if(regime==='new'){{
    // New regime FY26: rebate up to ₹12L net
    const br=[[400000,0],[400000,.05],[400000,.10],[400000,.15],[400000,.20],[Infinity,.30]];
    let tax=0,prev=0;
    for(const[band,r]of br){{const upper=prev+band;if(inc<=prev)break;tax+=(Math.min(inc,upper)-prev)*r;prev=upper;}}
    if(inc<=1200000)tax=0; // rebate Sec 87A for new regime
    return tax*1.04; // 4% cess
  }} else {{
    // Old regime standard deduction ₹50,000
    const taxable=Math.max(0,inc-50000);
    const br=[[250000,0],[250000,.05],[500000,.20],[Infinity,.30]];
    let tax=0,prev=0;
    for(const[band,r]of br){{const upper=prev+band;if(taxable<=prev)break;tax+=(Math.min(taxable,upper)-prev)*r;prev=upper;}}
    return tax*1.04;
  }}
}}
function calc(){{
  const salary=parseFloat(document.getElementById('salary').value)||0;
  const regime=document.getElementById('regime').value;
  const tax=calcIndiaTax(salary,regime);
  // PF: 12% up to ₹1,800/mo = ₹21,600/yr
  const pf=Math.min(salary*0.12,21600);
  const net=salary-tax-pf;
  document.getElementById('r-gross').textContent='₹'+Math.round(salary).toLocaleString('en-IN');
  document.getElementById('r-tax').textContent='₹'+Math.round(tax).toLocaleString('en-IN');
  document.getElementById('r-social').textContent='PF: ₹'+Math.round(pf).toLocaleString('en-IN');
  document.getElementById('r-annual').textContent='₹'+Math.round(net).toLocaleString('en-IN');
  document.getElementById('r-monthly').textContent='₹'+Math.round(net/12).toLocaleString('en-IN');
  set('r-rate',(salary>0?(tax+pf)/salary*100:0).toFixed(1)+'%');
  document.getElementById('result').classList.add('show');
}}
</script>"""

INTL = [
    ("tools/australia-salary-calculator.html", AUS_FORM, AUS_SCRIPT),
    ("tools/canada-salary-calculator.html",    CAN_FORM, CAN_SCRIPT),
    ("tools/uk-salary-calculator.html",        UK_FORM,  UK_SCRIPT),
    ("tools/singapore-salary-calculator.html", SG_FORM,  SG_SCRIPT),
    ("tools/india-salary-calculator.html",     IN_FORM,  IN_SCRIPT),
]

# ════════════════════════════════════════════════════════
# GROUP 3: Capital Gains / RSU / Stock Options
# ════════════════════════════════════════════════════════
CG_FORM = """  <div class="form-card">
    <h2>Enter Your Information</h2>
    <div class="form-grid">
<div class="field"><label>Capital Gain Amount ($)</label><input id="gain" type="number" value="50000" step="1000" min="0"></div>
<div class="field"><label>Holding Period</label><select id="holding"><option value="long">Long-Term (> 1 year)</option><option value="short">Short-Term (≤ 1 year)</option></select></div>
<div class="field"><label>Other Ordinary Income ($)</label><input id="otherinc" type="number" value="80000" step="1000" min="0"></div>
<div class="field"><label>Filing Status</label><select id="status"><option value="single">Single</option><option value="mfj">Married Filing Jointly</option><option value="hoh">Head of Household</option></select></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate Capital Gains Tax</button>
  </div>
  <div class="result-card" id="result">
    <h2>Capital Gains Tax Estimate</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Capital Gain</div><div class="result-value" id="r-gain">—</div></div>
<div class="result-item"><div class="result-label">Tax Rate Applied</div><div class="result-value" id="r-cg-rate">—</div></div>
<div class="result-item"><div class="result-label">Capital Gains Tax</div><div class="result-value" id="r-cg-tax" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">NIIT (3.8%) if applicable</div><div class="result-value" id="r-niit" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">Total Tax on Gain</div><div class="result-value" id="r-total" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">After-Tax Proceeds</div><div class="result-value" id="r-net">—</div></div>
    </div>
  </div>"""

CG_SCRIPT = f"""<script>
{fmt_js()}
function calc(){{
  const gain=parseFloat(document.getElementById('gain').value)||0;
  const holding=document.getElementById('holding').value;
  const otherinc=parseFloat(document.getElementById('otherinc').value)||0;
  const status=document.getElementById('status').value;
  let cgTax=0,rateLabel='';

  if(holding==='short'){{
    // Short-term: ordinary income rates
    const std={{single:15000,mfj:30000,hoh:22500}};
    const br={{
      single:[[11925,.10],[48475,.12],[103350,.22],[197300,.24],[250525,.32],[626350,.35],[Infinity,.37]],
      mfj:   [[23850,.10],[96950,.12],[206700,.22],[394600,.24],[501050,.32],[751600,.35],[Infinity,.37]],
      hoh:   [[17000,.10],[64300,.12],[103350,.22],[197300,.24],[250500,.32],[626350,.35],[Infinity,.37]]
    }};
    // marginal rate on the gain portion
    const taxable1=Math.max(0,otherinc-(std[status]||15000));
    const taxable2=taxable1+gain;
    let t1=0,t2=0,prev=0;
    const b=br[status]||br.single;
    for(const[u,r]of b){{
      if(taxable1>prev)t1+=(Math.min(taxable1,u)-prev)*r;
      if(taxable2>prev)t2+=(Math.min(taxable2,u)-prev)*r;
      prev=u;if(prev===Infinity)break;
    }}
    cgTax=t2-t1;
    rateLabel='Ordinary (up to 37%)';
  }} else {{
    // Long-term LTCG rates 2026
    const ltcg0={{single:48350,mfj:96700,hoh:64750}};
    const ltcg15={{single:533400,mfj:600050,hoh:566700}};
    const threshold0=ltcg0[status]||48350;
    const threshold15=ltcg15[status]||533400;
    const totalInc=otherinc+gain;
    const rate0Gain=Math.max(0,Math.min(totalInc,threshold0)-otherinc);
    const rate15Gain=Math.max(0,Math.min(totalInc,threshold15)-Math.max(otherinc,threshold0));
    const rate20Gain=Math.max(0,gain-rate0Gain-rate15Gain);
    cgTax=rate15Gain*0.15+rate20Gain*0.20;
    const effRate=gain>0?cgTax/gain*100:0;
    rateLabel=effRate.toFixed(1)+'% effective';
  }}

  // NIIT 3.8% on investment income if MAGI > threshold
  const niitThresh={{single:200000,mfj:250000,hoh:200000}};
  const niit=(otherinc+gain)>(niitThresh[status]||200000)?gain*0.038:0;
  const total=cgTax+niit;
  const net=gain-total;

  set('r-gain',fmt(gain));
  set('r-cg-rate',rateLabel);
  set('r-cg-tax',fmt(cgTax));
  set('r-niit',niit>0?fmt(niit):'$0 (below threshold)');
  set('r-total',fmt(total));
  set('r-net',fmt(net));
  document.getElementById('result').classList.add('show');
}}
</script>"""

RSU_FORM = """  <div class="form-card">
    <h2>Enter Your RSU Information</h2>
    <div class="form-grid">
<div class="field"><label>RSU Shares Vesting</label><input id="shares" type="number" value="100" step="10" min="0"></div>
<div class="field"><label>Share Price at Vesting ($)</label><input id="price" type="number" value="150" step="1" min="0"></div>
<div class="field"><label>Other Annual Income ($)</label><input id="otherinc" type="number" value="120000" step="1000" min="0"></div>
<div class="field"><label>Filing Status</label><select id="status"><option value="single">Single</option><option value="mfj">Married Filing Jointly</option><option value="hoh">Head of Household</option></select></div>
<div class="field"><label>Sale Price per Share ($) <em>optional</em></label><input id="saleprice" type="number" value="0" step="1" min="0" placeholder="0 = held, not sold"></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate RSU Tax</button>
  </div>
  <div class="result-card" id="result">
    <h2>RSU Tax Estimate</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Gross RSU Income</div><div class="result-value" id="r-gross">—</div></div>
<div class="result-item"><div class="result-label">Supplemental Fed Tax (22%)</div><div class="result-value" id="r-fed" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">FICA on RSU</div><div class="result-value" id="r-fica" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">After-Tax RSU Value</div><div class="result-value" id="r-net">—</div></div>
<div class="result-item"><div class="result-label">Capital Gain/Loss (if sold)</div><div class="result-value" id="r-cg">—</div></div>
<div class="result-item"><div class="result-label">Shares Needed for Tax</div><div class="result-value" id="r-sharestax">—</div></div>
    </div>
  </div>"""

RSU_SCRIPT = f"""<script>
{fmt_js()}
function calc(){{
  const shares=parseFloat(document.getElementById('shares').value)||0;
  const price=parseFloat(document.getElementById('price').value)||0;
  const otherinc=parseFloat(document.getElementById('otherinc').value)||0;
  const status=document.getElementById('status').value;
  const saleprice=parseFloat(document.getElementById('saleprice').value)||0;
  const grossRSU=shares*price;
  // Supplemental 22% federal withholding (flat rate for supplemental wages)
  const fedTax=grossRSU*0.22;
  // FICA: SS 6.2% if under wage base; Medicare 1.45%
  const ssBase=Math.max(0,Math.min(otherinc+grossRSU,176100)-Math.min(otherinc,176100));
  const fica=ssBase*0.062+grossRSU*0.0145;
  const net=grossRSU-fedTax-fica;
  const cgNote=saleprice>0?fmt((saleprice-price)*shares)+' ('+(saleprice>price?'gain':'loss')+')':'N/A (not sold)';
  const taxRate=(grossRSU>0?(fedTax+fica)/grossRSU:0);
  const sharesForTax=price>0?Math.ceil((fedTax+fica)/price):0;
  set('r-gross',fmt(grossRSU));
  set('r-fed',fmt(fedTax));
  set('r-fica',fmt(fica));
  set('r-net',fmt(net));
  set('r-cg',cgNote);
  set('r-sharestax',sharesForTax+' shares ('+((taxRate*100).toFixed(1))+'%)');
  document.getElementById('result').classList.add('show');
}}
</script>"""

STOCK_FORM = """  <div class="form-card">
    <h2>Enter Your Stock Option Information</h2>
    <div class="form-grid">
<div class="field"><label>Option Type</label><select id="opttype"><option value="nso">NSO (Non-Qualified)</option><option value="iso">ISO (Incentive)</option></select></div>
<div class="field"><label>Number of Options Exercising</label><input id="options" type="number" value="500" step="100" min="0"></div>
<div class="field"><label>Exercise (Strike) Price ($)</label><input id="strike" type="number" value="20" step="1" min="0"></div>
<div class="field"><label>Current FMV per Share ($)</label><input id="fmv" type="number" value="80" step="1" min="0"></div>
<div class="field"><label>Other Annual Income ($)</label><input id="otherinc" type="number" value="100000" step="1000" min="0"></div>
<div class="field"><label>Filing Status</label><select id="status"><option value="single">Single</option><option value="mfj">Married Filing Jointly</option><option value="hoh">Head of Household</option></select></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate Stock Option Tax</button>
  </div>
  <div class="result-card" id="result">
    <h2>Stock Option Tax Estimate</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Spread (Bargain Element)</div><div class="result-value" id="r-spread">—</div></div>
<div class="result-item"><div class="result-label">Exercise Cost</div><div class="result-value" id="r-cost">—</div></div>
<div class="result-item"><div class="result-label">Ordinary Income (NSO)</div><div class="result-value" id="r-ordinary">—</div></div>
<div class="result-item"><div class="result-label">Federal Tax on Exercise</div><div class="result-value" id="r-tax" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">FICA (NSO only)</div><div class="result-value" id="r-fica" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">After-Tax Gain</div><div class="result-value" id="r-net">—</div></div>
    </div>
  </div>"""

STOCK_SCRIPT = f"""<script>
{fmt_js()}
{fed_tax_js()}
function calc(){{
  const opttype=document.getElementById('opttype').value;
  const opts=parseFloat(document.getElementById('options').value)||0;
  const strike=parseFloat(document.getElementById('strike').value)||0;
  const fmv=parseFloat(document.getElementById('fmv').value)||0;
  const otherinc=parseFloat(document.getElementById('otherinc').value)||0;
  const status=document.getElementById('status').value;
  const spread=(fmv-strike)*opts;
  const cost=strike*opts;
  let fedTax=0,fica=0,ordinaryInc=0,note='';
  if(opttype==='nso'){{
    ordinaryInc=spread;
    // marginal federal tax on the spread
    const t1=calcFedTax(otherinc,status);
    const t2=calcFedTax(otherinc+spread,status);
    fedTax=t2-t1;
    const ssBase=Math.max(0,Math.min(otherinc+spread,176100)-Math.min(otherinc,176100));
    fica=ssBase*0.062+spread*0.0145;
  }} else {{
    // ISO: no regular income tax at exercise (AMT may apply — not calculated here)
    ordinaryInc=0;
    fedTax=0; fica=0;
    note='ISO: No regular income tax at exercise. AMT may apply — consult a tax advisor.';
  }}
  const net=spread-fedTax-fica;
  set('r-spread',fmt(spread));
  set('r-cost',fmt(cost));
  set('r-ordinary',opttype==='nso'?fmt(ordinaryInc):'$0 (ISO — see note)');
  set('r-tax',fedTax>0?fmt(fedTax):(opttype==='iso'?'AMT may apply':'$0'));
  set('r-fica',fica>0?fmt(fica):'$0 (ISO)');
  set('r-net',fmt(net));
  document.getElementById('result').classList.add('show');
}}
</script>"""

CAPGAINS = [
    ("tools/capital-gains-tax-calculator.html", CG_FORM,    CG_SCRIPT),
    ("tools/rsu-tax-calculator.html",           RSU_FORM,   RSU_SCRIPT),
    ("tools/stock-options-tax-calculator.html", STOCK_FORM, STOCK_SCRIPT),
]

# ════════════════════════════════════════════════════════
# GROUP 4: Leave / FMLA
# ════════════════════════════════════════════════════════
FMLA_FORM = """  <div class="form-card">
    <h2>Enter Your Information</h2>
    <div class="form-grid">
<div class="field"><label>Annual Salary ($)</label><input id="salary" type="number" value="60000" step="1000" min="0"></div>
<div class="field"><label>FMLA Leave Duration (weeks)</label><input id="weeks" type="number" value="6" step="1" min="0" max="12"></div>
<div class="field"><label>Employer Paid Leave (%)</label><input id="paidpct" type="number" value="0" step="5" min="0" max="100" placeholder="0 = unpaid"></div>
<div class="field"><label>State Paid Family Leave (%)</label><input id="statepct" type="number" value="60" step="5" min="0" max="100" placeholder="e.g. CA/NY/NJ 60-67%"></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate FMLA Pay</button>
  </div>
  <div class="result-card" id="result">
    <h2>FMLA Leave Estimate</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Weekly Salary</div><div class="result-value" id="r-weekly">—</div></div>
<div class="result-item"><div class="result-label">Total Leave Weeks</div><div class="result-value" id="r-weeks">—</div></div>
<div class="result-item"><div class="result-label">Employer Paid Amount</div><div class="result-value" id="r-employer">—</div></div>
<div class="result-item"><div class="result-label">State PFL Benefit</div><div class="result-value" id="r-state">—</div></div>
<div class="result-item"><div class="result-label">Lost Wages (unpaid gap)</div><div class="result-value" id="r-lost" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">Total Received</div><div class="result-value" id="r-total">—</div></div>
    </div>
  </div>"""

FMLA_SCRIPT = """<script>
function fmt(n){return'$'+Math.round(n).toLocaleString('en-US');}
function set(id,v){document.getElementById(id).textContent=v;}
function calc(){
  const salary=parseFloat(document.getElementById('salary').value)||0;
  const weeks=parseFloat(document.getElementById('weeks').value)||0;
  const paidPct=(parseFloat(document.getElementById('paidpct').value)||0)/100;
  const statePct=(parseFloat(document.getElementById('statepct').value)||0)/100;
  const weekly=salary/52;
  const totalLeavePay=weekly*weeks;
  const employerPaid=totalLeavePay*paidPct;
  // State PFL applies to the unpaid remainder
  const unpaidBase=totalLeavePay*(1-paidPct);
  const stateAmt=unpaidBase*statePct;
  const lost=totalLeavePay-employerPaid-stateAmt;
  const total=employerPaid+stateAmt;
  set('r-weekly',fmt(weekly));
  set('r-weeks',weeks+' weeks');
  set('r-employer',fmt(employerPaid));
  set('r-state',fmt(stateAmt));
  set('r-lost',fmt(Math.max(0,lost)));
  set('r-total',fmt(total));
  document.getElementById('result').classList.add('show');
}
</script>"""

MAT_FORM = """  <div class="form-card">
    <h2>Enter Your Information</h2>
    <div class="form-grid">
<div class="field"><label>Annual Salary ($)</label><input id="salary" type="number" value="70000" step="1000" min="0"></div>
<div class="field"><label>Maternity Leave Length (weeks)</label><input id="weeks" type="number" value="12" step="1" min="0" max="52"></div>
<div class="field"><label>Paid Leave by Employer (weeks)</label><input id="paidwks" type="number" value="6" step="1" min="0"></div>
<div class="field"><label>Employer Pay Rate During Leave (%)</label><input id="payrate" type="number" value="100" step="5" min="0" max="100"></div>
<div class="field"><label>State Paid Leave Benefit ($/week)</label><input id="stateamt" type="number" value="0" step="50" min="0" placeholder="0 if no state benefit"></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate Maternity Pay</button>
  </div>
  <div class="result-card" id="result">
    <h2>Maternity Leave Pay Breakdown</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Weekly Base Pay</div><div class="result-value" id="r-weekly">—</div></div>
<div class="result-item"><div class="result-label">Paid Leave Income</div><div class="result-value" id="r-paid">—</div></div>
<div class="result-item"><div class="result-label">State Benefit (unpaid wks)</div><div class="result-value" id="r-state">—</div></div>
<div class="result-item"><div class="result-label">Unpaid Gap</div><div class="result-value" id="r-gap" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">Total Leave Earnings</div><div class="result-value" id="r-total">—</div></div>
<div class="result-item"><div class="result-label">Income Replacement Rate</div><div class="result-value" id="r-rate">—</div></div>
    </div>
  </div>"""

MAT_SCRIPT = """<script>
function fmt(n){return'$'+Math.round(n).toLocaleString('en-US');}
function set(id,v){document.getElementById(id).textContent=v;}
function calc(){
  const salary=parseFloat(document.getElementById('salary').value)||0;
  const totalWks=parseFloat(document.getElementById('weeks').value)||0;
  const paidWks=Math.min(parseFloat(document.getElementById('paidwks').value)||0,totalWks);
  const payRate=(parseFloat(document.getElementById('payrate').value)||0)/100;
  const stateWkAmt=parseFloat(document.getElementById('stateamt').value)||0;
  const weekly=salary/52;
  const paidInc=paidWks*weekly*payRate;
  const unpaidWks=totalWks-paidWks;
  const stateTotal=stateWkAmt*unpaidWks;
  const fullPay=totalWks*weekly;
  const gap=Math.max(0,fullPay-paidInc-stateTotal);
  const total=paidInc+stateTotal;
  const replRate=fullPay>0?total/fullPay*100:0;
  set('r-weekly',fmt(weekly));
  set('r-paid',fmt(paidInc));
  set('r-state',fmt(stateTotal));
  set('r-gap',fmt(gap));
  set('r-total',fmt(total));
  set('r-rate',replRate.toFixed(0)+'%');
  document.getElementById('result').classList.add('show');
}
</script>"""

LEAVE = [
    ("tools/fmla-calculator.html",           FMLA_FORM, FMLA_SCRIPT),
    ("tools/maternity-leave-calculator.html", MAT_FORM,  MAT_SCRIPT),
]

# ════════════════════════════════════════════════════════
# GROUP 5: Payroll / HR / Deductions
# ════════════════════════════════════════════════════════
PAYROLL_FORM = """  <div class="form-card">
    <h2>Enter Payroll Information</h2>
    <div class="form-grid">
<div class="field"><label>Employee Gross Salary ($)</label><input id="salary" type="number" value="60000" step="1000" min="0"></div>
<div class="field"><label>Pay Frequency</label><select id="freq"><option value="26">Biweekly (26/yr)</option><option value="24">Semi-monthly (24/yr)</option><option value="12">Monthly (12/yr)</option><option value="52">Weekly (52/yr)</option></select></div>
<div class="field"><label>Filing Status</label><select id="status"><option value="single">Single</option><option value="mfj">Married Filing Jointly</option><option value="hoh">Head of Household</option></select></div>
<div class="field"><label>401(k) Employee Contribution (%)</label><input id="k401" type="number" value="6" step="0.5" min="0" max="100"></div>
<div class="field"><label>Health Insurance ($/paycheck)</label><input id="health" type="number" value="150" step="10" min="0"></div>
<div class="field"><label>Number of Employees</label><input id="headcount" type="number" value="1" step="1" min="1"></div>
    </div>
    <button class="btn-primary" onclick="calc()">Run Payroll</button>
  </div>
  <div class="result-card" id="result">
    <h2>Per-Paycheck Summary</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Gross Per Paycheck</div><div class="result-value" id="r-gross">—</div></div>
<div class="result-item"><div class="result-label">Federal Withholding</div><div class="result-value" id="r-fed" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">FICA (Employee)</div><div class="result-value" id="r-fica" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">Pre-Tax Deductions</div><div class="result-value" id="r-pretax" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">Net Paycheck</div><div class="result-value" id="r-net">—</div></div>
<div class="result-item"><div class="result-label">Annual Payroll Cost (×employees)</div><div class="result-value" id="r-total">—</div></div>
    </div>
  </div>"""

PAYROLL_SCRIPT = f"""<script>
{fmt_js()}
{fed_tax_js()}
function calc(){{
  const salary=parseFloat(document.getElementById('salary').value)||0;
  const freq=parseInt(document.getElementById('freq').value)||26;
  const status=document.getElementById('status').value;
  const k401=(parseFloat(document.getElementById('k401').value)||0)/100;
  const healthPP=parseFloat(document.getElementById('health').value)||0;
  const headcount=parseFloat(document.getElementById('headcount').value)||1;
  const ann401k=salary*k401;
  const annHealth=healthPP*freq;
  const annPreTax=ann401k+annHealth;
  const annTaxable=Math.max(0,salary-annPreTax);
  const annFed=calcFedTax(annTaxable,status);
  const annSS=Math.min(salary,176100)*0.062;
  const annMed=salary*0.0145;
  const ppGross=salary/freq;
  const ppFed=annFed/freq;
  const ppFica=(annSS+annMed)/freq;
  const ppPreTax=annPreTax/freq;
  const ppNet=ppGross-ppFed-ppFica-ppPreTax;
  set('r-gross',fmt(ppGross));
  set('r-fed',fmt(ppFed));
  set('r-fica',fmt(ppFica));
  set('r-pretax',fmt(ppPreTax));
  set('r-net',fmt(ppNet));
  set('r-total',fmt(salary*headcount));
  document.getElementById('result').classList.add('show');
}}
</script>"""

DEDUCTION_FORM = """  <div class="form-card">
    <h2>Enter Your Deduction Information</h2>
    <div class="form-grid">
<div class="field"><label>Annual Gross Salary ($)</label><input id="salary" type="number" value="75000" step="1000" min="0"></div>
<div class="field"><label>Pay Frequency</label><select id="freq"><option value="26">Biweekly (26/yr)</option><option value="24">Semi-monthly (24/yr)</option><option value="12">Monthly (12/yr)</option><option value="52">Weekly (52/yr)</option></select></div>
<div class="field"><label>401(k) Contribution (%)</label><input id="k401" type="number" value="6" step="0.5" min="0" max="100"></div>
<div class="field"><label>Health Insurance ($/paycheck)</label><input id="health" type="number" value="150" step="10" min="0"></div>
<div class="field"><label>HSA Contribution ($/year)</label><input id="hsa" type="number" value="0" step="100" min="0"></div>
<div class="field"><label>FSA Contribution ($/year)</label><input id="fsa" type="number" value="0" step="100" min="0"></div>
<div class="field"><label>Life Insurance ($/paycheck)</label><input id="life" type="number" value="10" step="5" min="0"></div>
<div class="field"><label>Other Pre-Tax ($/paycheck)</label><input id="other" type="number" value="0" step="10" min="0"></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate Deductions</button>
  </div>
  <div class="result-card" id="result">
    <h2>Payroll Deduction Breakdown</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Gross Per Paycheck</div><div class="result-value" id="r-gross">—</div></div>
<div class="result-item"><div class="result-label">401(k)</div><div class="result-value" id="r-k401" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">Health + HSA + FSA</div><div class="result-value" id="r-health" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">Life + Other</div><div class="result-value" id="r-other" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">Total Pre-Tax Deductions</div><div class="result-value" id="r-total" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">Annual Tax Savings (est.)</div><div class="result-value" id="r-save">—</div></div>
    </div>
  </div>"""

DEDUCTION_SCRIPT = """<script>
function fmt(n){return'$'+n.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}
function set(id,v){document.getElementById(id).textContent=v;}
function calc(){
  const salary=parseFloat(document.getElementById('salary').value)||0;
  const freq=parseInt(document.getElementById('freq').value)||26;
  const k401pct=(parseFloat(document.getElementById('k401').value)||0)/100;
  const healthPP=parseFloat(document.getElementById('health').value)||0;
  const hsa=parseFloat(document.getElementById('hsa').value)||0;
  const fsa=parseFloat(document.getElementById('fsa').value)||0;
  const lifePP=parseFloat(document.getElementById('life').value)||0;
  const otherPP=parseFloat(document.getElementById('other').value)||0;
  const ppGross=salary/freq;
  const ppK401=ppGross*k401pct;
  const ppHealth=healthPP+hsa/freq+fsa/freq;
  const ppLife=lifePP+otherPP;
  const ppTotal=ppK401+ppHealth+ppLife;
  const annPreTax=(ppK401+ppHealth+ppLife)*freq;
  // Estimate tax savings at ~22% marginal rate
  const taxSave=annPreTax*0.22;
  set('r-gross',fmt(ppGross));
  set('r-k401',fmt(ppK401));
  set('r-health',fmt(ppHealth));
  set('r-other',fmt(ppLife));
  set('r-total',fmt(ppTotal));
  set('r-save',fmt(taxSave));
  document.getElementById('result').classList.add('show');
}
</script>"""

BENEFITS_FORM = """  <div class="form-card">
    <h2>Enter Benefits Information</h2>
    <div class="form-grid">
<div class="field"><label>Annual Salary ($)</label><input id="salary" type="number" value="70000" step="1000" min="0"></div>
<div class="field"><label>Employer 401(k) Match (%)</label><input id="match" type="number" value="4" step="0.5" min="0" max="100"></div>
<div class="field"><label>Annual Health Insurance (employer share $)</label><input id="health" type="number" value="6000" step="500" min="0"></div>
<div class="field"><label>Annual Life/Disability Insurance ($)</label><input id="life" type="number" value="500" step="100" min="0"></div>
<div class="field"><label>PTO Days per Year</label><input id="pto" type="number" value="15" step="1" min="0"></div>
<div class="field"><label>Other Benefits ($/year)</label><input id="other" type="number" value="1200" step="100" min="0"></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate Total Benefits Value</button>
  </div>
  <div class="result-card" id="result">
    <h2>Total Compensation Breakdown</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Base Salary</div><div class="result-value" id="r-salary">—</div></div>
<div class="result-item"><div class="result-label">Employer 401(k) Match</div><div class="result-value" id="r-match">—</div></div>
<div class="result-item"><div class="result-label">Health Insurance Value</div><div class="result-value" id="r-health">—</div></div>
<div class="result-item"><div class="result-label">PTO Value</div><div class="result-value" id="r-pto">—</div></div>
<div class="result-item"><div class="result-label">Other Benefits</div><div class="result-value" id="r-other">—</div></div>
<div class="result-item"><div class="result-label">Total Compensation</div><div class="result-value" id="r-total">—</div></div>
<div class="result-item"><div class="result-label">Benefits as % of Salary</div><div class="result-value" id="r-rate">—</div></div>
    </div>
  </div>"""

BENEFITS_SCRIPT = """<script>
function fmt(n){return'$'+Math.round(n).toLocaleString('en-US');}
function set(id,v){document.getElementById(id).textContent=v;}
function calc(){
  const salary=parseFloat(document.getElementById('salary').value)||0;
  const matchPct=(parseFloat(document.getElementById('match').value)||0)/100;
  const health=parseFloat(document.getElementById('health').value)||0;
  const life=parseFloat(document.getElementById('life').value)||0;
  const pto=parseFloat(document.getElementById('pto').value)||0;
  const other=parseFloat(document.getElementById('other').value)||0;
  const matchAmt=salary*matchPct;
  const daily=salary/260;
  const ptoVal=daily*pto;
  const totalBenefits=matchAmt+health+life+ptoVal+other;
  const total=salary+totalBenefits;
  const rate=salary>0?totalBenefits/salary*100:0;
  set('r-salary',fmt(salary));
  set('r-match',fmt(matchAmt));
  set('r-health',fmt(health));
  set('r-pto',fmt(ptoVal));
  set('r-other',fmt(life+other));
  set('r-total',fmt(total));
  set('r-rate',rate.toFixed(1)+'%');
  document.getElementById('result').classList.add('show');
}
</script>"""

EMPCOСТ_FORM = """  <div class="form-card">
    <h2>Enter Employee Cost Information</h2>
    <div class="form-grid">
<div class="field"><label>Employee Annual Salary ($)</label><input id="salary" type="number" value="60000" step="1000" min="0"></div>
<div class="field"><label>Number of Employees</label><input id="headcount" type="number" value="1" step="1" min="1"></div>
<div class="field"><label>Employer Health Insurance ($/employee/yr)</label><input id="health" type="number" value="6000" step="500" min="0"></div>
<div class="field"><label>Employer 401(k) Match (%)</label><input id="match" type="number" value="4" step="0.5" min="0" max="100"></div>
<div class="field"><label>State SUTA Rate (%)</label><input id="suta" type="number" value="2.7" step="0.1" min="0" max="20"></div>
<div class="field"><label>Other Benefits per Employee ($/yr)</label><input id="other" type="number" value="1500" step="100" min="0"></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate Total Employee Cost</button>
  </div>
  <div class="result-card" id="result">
    <h2>Total Employer Cost</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Base Salary</div><div class="result-value" id="r-salary">—</div></div>
<div class="result-item"><div class="result-label">Employer FICA (7.65%)</div><div class="result-value" id="r-fica">—</div></div>
<div class="result-item"><div class="result-label">FUTA + SUTA</div><div class="result-value" id="r-futa">—</div></div>
<div class="result-item"><div class="result-label">Benefits (health+401k+other)</div><div class="result-value" id="r-benefits">—</div></div>
<div class="result-item"><div class="result-label">Cost Per Employee</div><div class="result-value" id="r-per">—</div></div>
<div class="result-item"><div class="result-label">Total Headcount Cost</div><div class="result-value" id="r-total">—</div></div>
    </div>
  </div>"""

EMPCOST_SCRIPT = """<script>
function fmt(n){return'$'+Math.round(n).toLocaleString('en-US');}
function set(id,v){document.getElementById(id).textContent=v;}
function calc(){
  const salary=parseFloat(document.getElementById('salary').value)||0;
  const headcount=parseFloat(document.getElementById('headcount').value)||1;
  const health=parseFloat(document.getElementById('health').value)||0;
  const matchPct=(parseFloat(document.getElementById('match').value)||0)/100;
  const sutaRate=(parseFloat(document.getElementById('suta').value)||0)/100;
  const other=parseFloat(document.getElementById('other').value)||0;
  const fica=(Math.min(salary,176100)*0.062+salary*0.0145);
  const futa=Math.min(salary,7000)*0.006;
  const suta=Math.min(salary,7000)*sutaRate;
  const match=salary*matchPct;
  const benefits=health+match+other;
  const perEmployee=salary+fica+futa+suta+benefits;
  set('r-salary',fmt(salary));
  set('r-fica',fmt(fica));
  set('r-futa',fmt(futa+suta));
  set('r-benefits',fmt(benefits));
  set('r-per',fmt(perEmployee));
  set('r-total',fmt(perEmployee*headcount));
  document.getElementById('result').classList.add('show');
}
</script>"""

PAYROLL_HR = [
    ("tools/payroll-calculator.html",      PAYROLL_FORM,   PAYROLL_SCRIPT),
    ("tools/payroll-cost-calculator.html", PAYROLL_FORM,   PAYROLL_SCRIPT),
    ("tools/headcount-cost-calculator.html", EMPCOСТ_FORM, EMPCOST_SCRIPT),
    ("tools/employee-cost-calculator.html",  EMPCOСТ_FORM, EMPCOST_SCRIPT),
    ("tools/employee-benefits-calculator.html", BENEFITS_FORM, BENEFITS_SCRIPT),
    ("tools/payroll-deduction-calculator.html", DEDUCTION_FORM, DEDUCTION_SCRIPT),
]

# ════════════════════════════════════════════════════════
# APPLY ALL
# ════════════════════════════════════════════════════════
ALL_TOOLS = []
for f in SE_FILES:
    ALL_TOOLS.append((f, SE_FORM, SE_SCRIPT))
for t in INTL:
    ALL_TOOLS.append(t)
for t in CAPGAINS:
    ALL_TOOLS.append(t)
for t in LEAVE:
    ALL_TOOLS.append(t)
for t in PAYROLL_HR:
    ALL_TOOLS.append(t)

print(f"=== Batch A: {len(ALL_TOOLS)} tools ===")
changed=0
for path,new_form,new_script in ALL_TOOLS:
    with open(path,"r",encoding="utf-8") as f: c=f.read()
    fo=OLD_FORM in c; so=OLD_SCRIPT in c
    if fo: c=c.replace(OLD_FORM,new_form,1)
    if so: c=c.replace(OLD_SCRIPT,new_script,1)
    if fo or so:
        with open(path,"w",encoding="utf-8") as f: f.write(c)
        changed+=1
        print(f"  ✓ {path}")
    else:
        print(f"  ✗ {path}: NO MATCH")
print(f"\nDone: {changed}/{len(ALL_TOOLS)}")
