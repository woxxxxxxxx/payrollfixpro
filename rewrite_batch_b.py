"""
Batch B: 差异化重写剩余 ~35 个换皮工具
Groups: Salary variants, Tax tools, Specialty pay, Benefits/Other
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

SHARED_JS = """function fmt(n){return'$'+Math.round(n).toLocaleString('en-US');}
function fmtd(n){return'$'+n.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}
function set(id,v){document.getElementById(id).textContent=v;}
function calcFedTax(inc,status){
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

# ────────────────────────────────────────────────────────
# Salary period converter with federal tax estimate (shared)
# ────────────────────────────────────────────────────────
SALARY_FORM = """  <div class="form-card">
    <h2>Enter Your Information</h2>
    <div class="form-grid">
<div class="field"><label>Gross Amount ($)</label><input id="amount" type="number" value="60000" step="1000" min="0"></div>
<div class="field"><label>Pay Period</label><select id="period"><option value="annual">Annual Salary</option><option value="monthly">Monthly</option><option value="biweekly">Biweekly</option><option value="weekly">Weekly</option><option value="hourly">Hourly Rate</option></select></div>
<div class="field"><label>Hours per Week (if hourly)</label><input id="hours" type="number" value="40" step="0.5" min="1" max="80"></div>
<div class="field"><label>Filing Status</label><select id="status"><option value="single">Single</option><option value="mfj">Married Filing Jointly</option><option value="hoh">Head of Household</option></select></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate</button>
  </div>
  <div class="result-card" id="result">
    <h2>Salary Breakdown</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Annual</div><div class="result-value" id="r-annual">—</div></div>
<div class="result-item"><div class="result-label">Monthly</div><div class="result-value" id="r-monthly">—</div></div>
<div class="result-item"><div class="result-label">Biweekly</div><div class="result-value" id="r-biweekly">—</div></div>
<div class="result-item"><div class="result-label">Weekly</div><div class="result-value" id="r-weekly">—</div></div>
<div class="result-item"><div class="result-label">Daily</div><div class="result-value" id="r-daily">—</div></div>
<div class="result-item"><div class="result-label">Hourly</div><div class="result-value" id="r-hourly">—</div></div>
<div class="result-item"><div class="result-label">Est. Federal Tax (annual)</div><div class="result-value" id="r-fed" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">Est. Net Take-Home (annual)</div><div class="result-value" id="r-net">—</div></div>
    </div>
  </div>"""

SALARY_SCRIPT = f"""<script>
{SHARED_JS}
function calc(){{
  const amount=parseFloat(document.getElementById('amount').value)||0;
  const period=document.getElementById('period').value;
  const hours=parseFloat(document.getElementById('hours').value)||40;
  const status=document.getElementById('status').value;
  const wpy=hours*52;
  const mult={{annual:1,monthly:12,biweekly:26,weekly:52,hourly:wpy}};
  const annual=amount*(mult[period]||1);
  const fedTax=calcFedTax(annual,status);
  const fica=Math.min(annual,176100)*0.062+annual*0.0145;
  const net=annual-fedTax-fica;
  set('r-annual',fmt(annual));
  set('r-monthly',fmt(annual/12));
  set('r-biweekly',fmt(annual/26));
  set('r-weekly',fmt(annual/52));
  set('r-daily',fmt(annual/260));
  set('r-hourly',fmtd(annual/wpy));
  set('r-fed',fmt(fedTax));
  set('r-net',fmt(net));
  document.getElementById('result').classList.add('show');
}}
</script>"""

SALARY_FILES = [
    "tools/salary-calculator.html",
    "tools/annual-salary-calculator.html",
    "tools/gross-salary-calculator.html",
    "tools/monthly-salary-calculator.html",
    "tools/biweekly-pay-calculator.html",
    "tools/weekly-pay-calculator.html",
    "tools/net-salary-calculator.html",
    "tools/paycheck-estimator.html",
    "tools/direct-deposit-calculator.html",
]

# ────────────────────────────────────────────────────────
# Part-time salary
# ────────────────────────────────────────────────────────
PT_FORM = """  <div class="form-card">
    <h2>Enter Your Information</h2>
    <div class="form-grid">
<div class="field"><label>Hourly Rate ($)</label><input id="rate" type="number" value="25" step="0.5" min="0"></div>
<div class="field"><label>Hours per Week</label><input id="hours" type="number" value="24" step="1" min="0" max="40"></div>
<div class="field"><label>Weeks per Year</label><input id="weeks" type="number" value="50" step="1" min="1" max="52"></div>
<div class="field"><label>Filing Status</label><select id="status"><option value="single">Single</option><option value="mfj">Married Filing Jointly</option><option value="hoh">Head of Household</option></select></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate Part-Time Pay</button>
  </div>
  <div class="result-card" id="result">
    <h2>Part-Time Pay Estimate</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Annual Gross</div><div class="result-value" id="r-annual">—</div></div>
<div class="result-item"><div class="result-label">Monthly Gross</div><div class="result-value" id="r-monthly">—</div></div>
<div class="result-item"><div class="result-label">Weekly Gross</div><div class="result-value" id="r-weekly">—</div></div>
<div class="result-item"><div class="result-label">FTE Equivalent Salary</div><div class="result-value" id="r-fte">—</div></div>
<div class="result-item"><div class="result-label">Est. Federal Tax</div><div class="result-value" id="r-fed" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">Est. Annual Net Pay</div><div class="result-value" id="r-net">—</div></div>
    </div>
  </div>"""

PT_SCRIPT = f"""<script>
{SHARED_JS}
function calc(){{
  const rate=parseFloat(document.getElementById('rate').value)||0;
  const hours=parseFloat(document.getElementById('hours').value)||0;
  const weeks=parseFloat(document.getElementById('weeks').value)||52;
  const status=document.getElementById('status').value;
  const annual=rate*hours*weeks;
  const fteSalary=rate*40*52;
  const fedTax=calcFedTax(annual,status);
  const fica=Math.min(annual,176100)*0.062+annual*0.0145;
  const net=annual-fedTax-fica;
  set('r-annual',fmt(annual));
  set('r-monthly',fmt(annual/12));
  set('r-weekly',fmt(rate*hours));
  set('r-fte',fmt(fteSalary));
  set('r-fed',fmt(fedTax));
  set('r-net',fmt(net));
  document.getElementById('result').classList.add('show');
}}
</script>"""

# ────────────────────────────────────────────────────────
# Raise / Salary Increase tools
# ────────────────────────────────────────────────────────
RAISE_FORM = """  <div class="form-card">
    <h2>Enter Your Information</h2>
    <div class="form-grid">
<div class="field"><label>Current Annual Salary ($)</label><input id="current" type="number" value="65000" step="1000" min="0"></div>
<div class="field"><label>Raise / Increase (%)</label><input id="raisepct" type="number" value="5" step="0.1" min="0"></div>
<div class="field"><label>Filing Status</label><select id="status"><option value="single">Single</option><option value="mfj">Married Filing Jointly</option><option value="hoh">Head of Household</option></select></div>
<div class="field"><label>Years Until Raise</label><input id="years" type="number" value="0" step="1" min="0" max="10"></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate Raise</button>
  </div>
  <div class="result-card" id="result">
    <h2>Raise Impact</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">New Annual Salary</div><div class="result-value" id="r-new">—</div></div>
<div class="result-item"><div class="result-label">Raise Amount (annual)</div><div class="result-value" id="r-raise">—</div></div>
<div class="result-item"><div class="result-label">Extra Biweekly Pay</div><div class="result-value" id="r-pp">—</div></div>
<div class="result-item"><div class="result-label">Tax on Raise (est.)</div><div class="result-value" id="r-tax" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">Net Raise (after tax)</div><div class="result-value" id="r-net">—</div></div>
<div class="result-item"><div class="result-label">Effective Raise (after tax)</div><div class="result-value" id="r-effpct">—</div></div>
    </div>
  </div>"""

RAISE_SCRIPT = f"""<script>
{SHARED_JS}
function calc(){{
  const current=parseFloat(document.getElementById('current').value)||0;
  const raisePct=(parseFloat(document.getElementById('raisepct').value)||0)/100;
  const status=document.getElementById('status').value;
  const newSalary=current*(1+raisePct);
  const raiseAmt=newSalary-current;
  const taxOld=calcFedTax(current,status);
  const taxNew=calcFedTax(newSalary,status);
  const taxOnRaise=taxNew-taxOld;
  const netRaise=raiseAmt-taxOnRaise;
  const effPct=current>0?netRaise/current*100:0;
  set('r-new',fmt(newSalary));
  set('r-raise',fmt(raiseAmt));
  set('r-pp',fmt(raiseAmt/26));
  set('r-tax',fmt(taxOnRaise));
  set('r-net',fmt(netRaise));
  set('r-effpct',effPct.toFixed(2)+'%');
  document.getElementById('result').classList.add('show');
}}
</script>"""

RAISE_FILES = [
    "tools/raise-calculator.html",
    "tools/salary-increase-calculator.html",
    "tools/promotion-salary-calculator.html",
]

# ────────────────────────────────────────────────────────
# Salary comparison
# ────────────────────────────────────────────────────────
COMP_FORM = """  <div class="form-card">
    <h2>Compare Two Salary Offers</h2>
    <div class="form-grid">
<div class="field"><label>Offer A — Annual Salary ($)</label><input id="salA" type="number" value="80000" step="1000" min="0"></div>
<div class="field"><label>Offer B — Annual Salary ($)</label><input id="salB" type="number" value="95000" step="1000" min="0"></div>
<div class="field"><label>Offer A — Benefits Value ($/yr)</label><input id="benA" type="number" value="15000" step="500" min="0"></div>
<div class="field"><label>Offer B — Benefits Value ($/yr)</label><input id="benB" type="number" value="8000" step="500" min="0"></div>
<div class="field"><label>Filing Status</label><select id="status"><option value="single">Single</option><option value="mfj">Married Filing Jointly</option><option value="hoh">Head of Household</option></select></div>
    </div>
    <button class="btn-primary" onclick="calc()">Compare Offers</button>
  </div>
  <div class="result-card" id="result">
    <h2>Offer Comparison</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Offer A — Net Pay</div><div class="result-value" id="r-netA">—</div></div>
<div class="result-item"><div class="result-label">Offer B — Net Pay</div><div class="result-value" id="r-netB">—</div></div>
<div class="result-item"><div class="result-label">Offer A — Total Comp</div><div class="result-value" id="r-totalA">—</div></div>
<div class="result-item"><div class="result-label">Offer B — Total Comp</div><div class="result-value" id="r-totalB">—</div></div>
<div class="result-item"><div class="result-label">Difference (net pay)</div><div class="result-value" id="r-diff">—</div></div>
<div class="result-item"><div class="result-label">Better Offer (total comp)</div><div class="result-value" id="r-winner">—</div></div>
    </div>
  </div>"""

COMP_SCRIPT = f"""<script>
{SHARED_JS}
function netPay(sal,status){{
  const fed=calcFedTax(sal,status);
  const fica=Math.min(sal,176100)*0.062+sal*0.0145;
  return sal-fed-fica;
}}
function calc(){{
  const salA=parseFloat(document.getElementById('salA').value)||0;
  const salB=parseFloat(document.getElementById('salB').value)||0;
  const benA=parseFloat(document.getElementById('benA').value)||0;
  const benB=parseFloat(document.getElementById('benB').value)||0;
  const status=document.getElementById('status').value;
  const netA=netPay(salA,status);
  const netB=netPay(salB,status);
  const totalA=netA+benA;
  const totalB=netB+benB;
  const diff=netB-netA;
  set('r-netA',fmt(netA));
  set('r-netB',fmt(netB));
  set('r-totalA',fmt(totalA));
  set('r-totalB',fmt(totalB));
  const diffEl=document.getElementById('r-diff');
  diffEl.textContent=(diff>=0?'+':'')+fmt(diff)+'/yr (B vs A)';
  diffEl.style.color=diff>=0?'#16a34a':'#dc2626';
  const winner=totalA>=totalB?'Offer A (total comp)':'Offer B (total comp)';
  set('r-winner',winner);
  document.getElementById('result').classList.add('show');
}}
</script>"""

# ────────────────────────────────────────────────────────
# Salary negotiation
# ────────────────────────────────────────────────────────
NEGO_FORM = """  <div class="form-card">
    <h2>Negotiation Planner</h2>
    <div class="form-grid">
<div class="field"><label>Current / Offer Salary ($)</label><input id="current" type="number" value="75000" step="1000" min="0"></div>
<div class="field"><label>Your Target Salary ($)</label><input id="target" type="number" value="90000" step="1000" min="0"></div>
<div class="field"><label>Walk-Away Minimum ($)</label><input id="minimum" type="number" value="80000" step="1000" min="0"></div>
<div class="field"><label>Filing Status</label><select id="status"><option value="single">Single</option><option value="mfj">Married Filing Jointly</option><option value="hoh">Head of Household</option></select></div>
    </div>
    <button class="btn-primary" onclick="calc()">Analyze Negotiation</button>
  </div>
  <div class="result-card" id="result">
    <h2>Negotiation Analysis</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Current Net Pay (annual)</div><div class="result-value" id="r-curnet">—</div></div>
<div class="result-item"><div class="result-label">Target Net Pay (annual)</div><div class="result-value" id="r-tarnet">—</div></div>
<div class="result-item"><div class="result-label">Net Gain at Target</div><div class="result-value" id="r-gain">—</div></div>
<div class="result-item"><div class="result-label">Walk-Away Net Pay</div><div class="result-value" id="r-minet">—</div></div>
<div class="result-item"><div class="result-label">Negotiation Range</div><div class="result-value" id="r-range">—</div></div>
<div class="result-item"><div class="result-label">Extra Monthly at Target</div><div class="result-value" id="r-monthly">—</div></div>
    </div>
  </div>"""

NEGO_SCRIPT = f"""<script>
{SHARED_JS}
function netPay(sal,status){{
  const fed=calcFedTax(sal,status);
  const fica=Math.min(sal,176100)*0.062+sal*0.0145;
  return sal-fed-fica;
}}
function calc(){{
  const current=parseFloat(document.getElementById('current').value)||0;
  const target=parseFloat(document.getElementById('target').value)||0;
  const minimum=parseFloat(document.getElementById('minimum').value)||0;
  const status=document.getElementById('status').value;
  const curNet=netPay(current,status);
  const tarNet=netPay(target,status);
  const minNet=netPay(minimum,status);
  const gain=tarNet-curNet;
  set('r-curnet',fmt(curNet));
  set('r-tarnet',fmt(tarNet));
  set('r-gain',fmt(gain));
  set('r-minet',fmt(minNet));
  set('r-range',fmt(minimum)+' – '+fmt(target));
  set('r-monthly',fmt(gain/12));
  document.getElementById('result').classList.add('show');
}}
</script>"""

# ────────────────────────────────────────────────────────
# Role-specific salary (manager, nurse, teacher, SWE, exec)
# ────────────────────────────────────────────────────────
def role_form(title, extra_field):
    return f"""  <div class="form-card">
    <h2>Enter Your Information</h2>
    <div class="form-grid">
<div class="field"><label>Annual Base Salary ($)</label><input id="salary" type="number" value="95000" step="1000" min="0"></div>
<div class="field"><label>Annual Bonus ($)</label><input id="bonus" type="number" value="0" step="500" min="0"></div>
{extra_field}
<div class="field"><label>Filing Status</label><select id="status"><option value="single">Single</option><option value="mfj">Married Filing Jointly</option><option value="hoh">Head of Household</option></select></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate {title} Compensation</button>
  </div>
  <div class="result-card" id="result">
    <h2>Total Compensation Breakdown</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Total Gross Income</div><div class="result-value" id="r-total">—</div></div>
<div class="result-item"><div class="result-label">Federal Income Tax</div><div class="result-value" id="r-fed" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">FICA</div><div class="result-value" id="r-fica" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">Annual Net Pay</div><div class="result-value" id="r-net">—</div></div>
<div class="result-item"><div class="result-label">Monthly Net Pay</div><div class="result-value" id="r-monthly">—</div></div>
<div class="result-item"><div class="result-label">Effective Tax Rate</div><div class="result-value" id="r-rate">—</div></div>
    </div>
  </div>"""

ROLE_SCRIPT = f"""<script>
{SHARED_JS}
function calc(){{
  const salary=parseFloat(document.getElementById('salary').value)||0;
  const bonus=parseFloat(document.getElementById('bonus').value)||0;
  const extra=parseFloat(document.getElementById('extra')?.value)||0;
  const status=document.getElementById('status').value;
  const total=salary+bonus+extra;
  const fed=calcFedTax(total,status);
  const fica=Math.min(total,176100)*0.062+total*0.0145;
  const net=total-fed-fica;
  set('r-total',fmt(total));
  set('r-fed',fmt(fed));
  set('r-fica',fmt(fica));
  set('r-net',fmt(net));
  set('r-monthly',fmt(net/12));
  set('r-rate',(total>0?(fed+fica)/total*100:0).toFixed(1)+'%');
  document.getElementById('result').classList.add('show');
}}
</script>"""

MGR_FORM  = role_form("Manager",  '<div class="field"><label>Team Size Bonus ($/report)</label><input id="extra" type="number" value="2000" step="500" min="0"></div>')
NURSE_FORM= role_form("Nurse",    '<div class="field"><label>Overtime / Shift Diff ($/yr)</label><input id="extra" type="number" value="5000" step="500" min="0"></div>')
TEACH_FORM= role_form("Teacher",  '<div class="field"><label>Stipends / Extra Duties ($/yr)</label><input id="extra" type="number" value="1500" step="500" min="0"></div>')
SWE_FORM  = role_form("Engineer", '<div class="field"><label>Equity / RSU Vesting ($/yr)</label><input id="extra" type="number" value="20000" step="1000" min="0"></div>')
EXEC_FORM = role_form("Executive",'<div class="field"><label>Long-Term Incentive / Equity ($/yr)</label><input id="extra" type="number" value="50000" step="5000" min="0"></div>')

ROLE_TOOLS = [
    ("tools/manager-salary-calculator.html",        MGR_FORM,   ROLE_SCRIPT),
    ("tools/nurse-salary-calculator.html",          NURSE_FORM, ROLE_SCRIPT),
    ("tools/teacher-salary-calculator.html",        TEACH_FORM, ROLE_SCRIPT),
    ("tools/software-engineer-salary.html",         SWE_FORM,   ROLE_SCRIPT),
    ("tools/executive-compensation-calculator.html",EXEC_FORM,  ROLE_SCRIPT),
]

# ────────────────────────────────────────────────────────
# Specialty pay: holiday, shift differential, tip, back-pay
# ────────────────────────────────────────────────────────
HOL_FORM = """  <div class="form-card">
    <h2>Enter Your Information</h2>
    <div class="form-grid">
<div class="field"><label>Hourly Wage ($)</label><input id="rate" type="number" value="20" step="0.5" min="0"></div>
<div class="field"><label>Holiday Hours Worked</label><input id="hours" type="number" value="8" step="0.5" min="0"></div>
<div class="field"><label>Holiday Pay Multiplier</label><select id="mult"><option value="2">Double Time (2×)</option><option value="1.5">Time & Half (1.5×)</option><option value="1">Regular (1×)</option></select></div>
<div class="field"><label>Annual Base Salary ($)</label><input id="annual" type="number" value="42000" step="1000" min="0"></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate Holiday Pay</button>
  </div>
  <div class="result-card" id="result">
    <h2>Holiday Pay Breakdown</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Holiday Pay (this day)</div><div class="result-value" id="r-holpay">—</div></div>
<div class="result-item"><div class="result-label">Regular Rate</div><div class="result-value" id="r-reg">—</div></div>
<div class="result-item"><div class="result-label">Premium Earned</div><div class="result-value" id="r-prem">—</div></div>
<div class="result-item"><div class="result-label">Biweekly Base Pay</div><div class="result-value" id="r-biweekly">—</div></div>
    </div>
  </div>"""

HOL_SCRIPT = """<script>
function fmt(n){return'$'+n.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}
function set(id,v){document.getElementById(id).textContent=v;}
function calc(){
  const rate=parseFloat(document.getElementById('rate').value)||0;
  const hours=parseFloat(document.getElementById('hours').value)||0;
  const mult=parseFloat(document.getElementById('mult').value)||2;
  const annual=parseFloat(document.getElementById('annual').value)||0;
  const holPay=rate*mult*hours;
  const regPay=rate*hours;
  const prem=holPay-regPay;
  set('r-holpay',fmt(holPay));
  set('r-reg',fmt(regPay));
  set('r-prem',fmt(prem));
  set('r-biweekly',fmt(annual/26));
  document.getElementById('result').classList.add('show');
}
</script>"""

SHIFT_FORM = """  <div class="form-card">
    <h2>Enter Your Information</h2>
    <div class="form-grid">
<div class="field"><label>Base Hourly Rate ($)</label><input id="rate" type="number" value="20" step="0.5" min="0"></div>
<div class="field"><label>Shift Differential (%)</label><input id="diffpct" type="number" value="15" step="1" min="0" max="100"></div>
<div class="field"><label>Shift Hours per Week</label><input id="shours" type="number" value="40" step="1" min="0" max="80"></div>
<div class="field"><label>Weeks per Year on Shift</label><input id="weeks" type="number" value="50" step="1" min="1" max="52"></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate Shift Differential</button>
  </div>
  <div class="result-card" id="result">
    <h2>Shift Differential Pay</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Effective Hourly Rate</div><div class="result-value" id="r-eff">—</div></div>
<div class="result-item"><div class="result-label">Weekly Differential Premium</div><div class="result-value" id="r-wk">—</div></div>
<div class="result-item"><div class="result-label">Annual Differential Premium</div><div class="result-value" id="r-ann">—</div></div>
<div class="result-item"><div class="result-label">Total Annual Pay (with diff)</div><div class="result-value" id="r-total">—</div></div>
    </div>
  </div>"""

SHIFT_SCRIPT = """<script>
function fmt(n){return'$'+n.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}
function set(id,v){document.getElementById(id).textContent=v;}
function calc(){
  const rate=parseFloat(document.getElementById('rate').value)||0;
  const diffpct=(parseFloat(document.getElementById('diffpct').value)||0)/100;
  const shours=parseFloat(document.getElementById('shours').value)||0;
  const weeks=parseFloat(document.getElementById('weeks').value)||52;
  const eff=rate*(1+diffpct);
  const wkPrem=rate*diffpct*shours;
  const annPrem=wkPrem*weeks;
  const total=rate*shours*weeks+annPrem;
  set('r-eff',fmt(eff));
  set('r-wk',fmt(wkPrem));
  set('r-ann',fmt(annPrem));
  set('r-total',fmt(total));
  document.getElementById('result').classList.add('show');
}
</script>"""

TIP_FORM = """  <div class="form-card">
    <h2>Enter Your Information</h2>
    <div class="form-grid">
<div class="field"><label>Hourly Tipped Wage ($)</label><input id="rate" type="number" value="2.13" step="0.01" min="0"></div>
<div class="field"><label>Average Tips per Hour ($)</label><input id="tips" type="number" value="10" step="0.5" min="0"></div>
<div class="field"><label>Hours per Week</label><input id="hours" type="number" value="35" step="1" min="0" max="80"></div>
<div class="field"><label>Filing Status</label><select id="status"><option value="single">Single</option><option value="mfj">Married Filing Jointly</option><option value="hoh">Head of Household</option></select></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate Tip Income</button>
  </div>
  <div class="result-card" id="result">
    <h2>Tipped Employee Pay</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Annual Wages + Tips</div><div class="result-value" id="r-annual">—</div></div>
<div class="result-item"><div class="result-label">Annual Tips</div><div class="result-value" id="r-tips">—</div></div>
<div class="result-item"><div class="result-label">Federal Tax (est.)</div><div class="result-value" id="r-fed" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">FICA on Total Income</div><div class="result-value" id="r-fica" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">Annual Net Pay</div><div class="result-value" id="r-net">—</div></div>
<div class="result-item"><div class="result-label">Effective Hourly (after tax)</div><div class="result-value" id="r-eff">—</div></div>
    </div>
  </div>"""

TIP_SCRIPT = f"""<script>
{SHARED_JS}
function calc(){{
  const rate=parseFloat(document.getElementById('rate').value)||0;
  const tips=parseFloat(document.getElementById('tips').value)||0;
  const hours=parseFloat(document.getElementById('hours').value)||0;
  const status=document.getElementById('status').value;
  const annual=(rate+tips)*hours*52;
  const annTips=tips*hours*52;
  const fed=calcFedTax(annual,status);
  const fica=Math.min(annual,176100)*0.062+annual*0.0145;
  const net=annual-fed-fica;
  const totalHours=hours*52;
  set('r-annual',fmt(annual));
  set('r-tips',fmt(annTips));
  set('r-fed',fmt(fed));
  set('r-fica',fmt(fica));
  set('r-net',fmt(net));
  set('r-eff',fmtd(totalHours>0?net/totalHours:0)+'/hr');
  document.getElementById('result').classList.add('show');
}}
</script>"""

BACKPAY_FORM = """  <div class="form-card">
    <h2>Enter Your Information</h2>
    <div class="form-grid">
<div class="field"><label>Regular Hourly Rate ($)</label><input id="rate" type="number" value="25" step="0.5" min="0"></div>
<div class="field"><label>Unpaid Hours</label><input id="hours" type="number" value="80" step="1" min="0"></div>
<div class="field"><label>Overtime Hours (of above)</label><input id="ot" type="number" value="20" step="1" min="0"></div>
<div class="field"><label>Interest Rate (% per year)</label><input id="interest" type="number" value="8" step="0.5" min="0"></div>
<div class="field"><label>Months Since Owed</label><input id="months" type="number" value="6" step="1" min="0"></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate Back Pay</button>
  </div>
  <div class="result-card" id="result">
    <h2>Back Pay Estimate</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Regular Back Pay</div><div class="result-value" id="r-reg">—</div></div>
<div class="result-item"><div class="result-label">Overtime Back Pay</div><div class="result-value" id="r-ot">—</div></div>
<div class="result-item"><div class="result-label">Total Back Pay Owed</div><div class="result-value" id="r-total">—</div></div>
<div class="result-item"><div class="result-label">Interest Accrued</div><div class="result-value" id="r-int">—</div></div>
<div class="result-item"><div class="result-label">Liquidated Damages (×2)</div><div class="result-value" id="r-liq">—</div></div>
<div class="result-item"><div class="result-label">Total Potential Claim</div><div class="result-value" id="r-claim">—</div></div>
    </div>
  </div>"""

BACKPAY_SCRIPT = """<script>
function fmt(n){return'$'+n.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}
function set(id,v){document.getElementById(id).textContent=v;}
function calc(){
  const rate=parseFloat(document.getElementById('rate').value)||0;
  const hours=parseFloat(document.getElementById('hours').value)||0;
  const ot=Math.min(parseFloat(document.getElementById('ot').value)||0,hours);
  const regHours=hours-ot;
  const interest=(parseFloat(document.getElementById('interest').value)||0)/100;
  const months=parseFloat(document.getElementById('months').value)||0;
  const regPay=regHours*rate;
  const otPay=ot*rate*1.5;
  const total=regPay+otPay;
  const intAmt=total*(interest/12)*months;
  const liq=total*2;
  const claim=total+intAmt+liq;
  set('r-reg',fmt(regPay));
  set('r-ot',fmt(otPay));
  set('r-total',fmt(total));
  set('r-int',fmt(intAmt));
  set('r-liq',fmt(liq));
  set('r-claim',fmt(claim));
  document.getElementById('result').classList.add('show');
}
</script>"""

# ────────────────────────────────────────────────────────
# Tax-related tools
# ────────────────────────────────────────────────────────
TAXREFUND_FORM = """  <div class="form-card">
    <h2>Estimate Your Tax Refund</h2>
    <div class="form-grid">
<div class="field"><label>Total W-2 Wages ($)</label><input id="wages" type="number" value="65000" step="1000" min="0"></div>
<div class="field"><label>Total Federal Tax Withheld ($)</label><input id="withheld" type="number" value="9000" step="100" min="0"></div>
<div class="field"><label>Filing Status</label><select id="status"><option value="single">Single</option><option value="mfj">Married Filing Jointly</option><option value="mfs">Married Filing Separately</option><option value="hoh">Head of Household</option></select></div>
<div class="field"><label>Child Tax Credit ($)</label><input id="ctc" type="number" value="0" step="2000" min="0" placeholder="$2,000 per child under 17"></div>
<div class="field"><label>Other Credits ($)</label><input id="credits" type="number" value="0" step="100" min="0"></div>
    </div>
    <button class="btn-primary" onclick="calc()">Estimate Refund</button>
  </div>
  <div class="result-card" id="result">
    <h2>Refund / Balance Due Estimate</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Taxable Income</div><div class="result-value" id="r-taxable">—</div></div>
<div class="result-item"><div class="result-label">Tax Before Credits</div><div class="result-value" id="r-before">—</div></div>
<div class="result-item"><div class="result-label">Credits Applied</div><div class="result-value" id="r-credits">—</div></div>
<div class="result-item"><div class="result-label">Tax After Credits</div><div class="result-value" id="r-after">—</div></div>
<div class="result-item"><div class="result-label">Already Withheld</div><div class="result-value" id="r-withheld">—</div></div>
<div class="result-item"><div class="result-label" id="outcome-label">—</div><div class="result-value" id="r-outcome">—</div></div>
    </div>
  </div>"""

TAXREFUND_SCRIPT = f"""<script>
{SHARED_JS}
function calc(){{
  const wages=parseFloat(document.getElementById('wages').value)||0;
  const withheld=parseFloat(document.getElementById('withheld').value)||0;
  const status=document.getElementById('status').value;
  const ctc=parseFloat(document.getElementById('ctc').value)||0;
  const credits=parseFloat(document.getElementById('credits').value)||0;
  const std={{single:15000,mfj:30000,mfs:15000,hoh:22500}};
  const taxable=Math.max(0,wages-(std[status]||15000));
  const before=calcFedTax(wages,status);
  const totalCredits=Math.min(before,ctc+credits);
  const after=Math.max(0,before-totalCredits);
  const diff=withheld-after;
  const isRefund=diff>=0;
  set('r-taxable',fmt(taxable));
  set('r-before',fmt(before));
  set('r-credits',fmt(totalCredits));
  set('r-after',fmt(after));
  set('r-withheld',fmt(withheld));
  document.getElementById('outcome-label').textContent=isRefund?'Estimated Refund':'Balance Due';
  const outEl=document.getElementById('r-outcome');
  outEl.textContent=(isRefund?'+':'-')+fmt(Math.abs(diff));
  outEl.style.color=isRefund?'#16a34a':'#dc2626';
  document.getElementById('result').classList.add('show');
}}
</script>"""

TAXWITH_FORM = """  <div class="form-card">
    <h2>Adjust Your Tax Withholding</h2>
    <div class="form-grid">
<div class="field"><label>Annual Gross Salary ($)</label><input id="salary" type="number" value="70000" step="1000" min="0"></div>
<div class="field"><label>Pay Frequency</label><select id="freq"><option value="26">Biweekly (26/yr)</option><option value="24">Semi-monthly (24/yr)</option><option value="12">Monthly (12/yr)</option><option value="52">Weekly (52/yr)</option></select></div>
<div class="field"><label>Filing Status</label><select id="status"><option value="single">Single</option><option value="mfj">Married Filing Jointly</option><option value="mfs">Married Filing Separately</option><option value="hoh">Head of Household</option></select></div>
<div class="field"><label>Step 3 — Dependent Credits ($)</label><input id="step3" type="number" value="0" step="500" min="0" placeholder="$2,000 per child under 17"></div>
<div class="field"><label>Current Withholding per Period ($)</label><input id="current" type="number" value="0" step="10" min="0" placeholder="from your paystub"></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate Withholding</button>
  </div>
  <div class="result-card" id="result">
    <h2>Withholding Analysis</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Recommended Per Period</div><div class="result-value" id="r-rec">—</div></div>
<div class="result-item"><div class="result-label">Annual Tax Estimate</div><div class="result-value" id="r-annual">—</div></div>
<div class="result-item"><div class="result-label">Current Annual Withholding</div><div class="result-value" id="r-cur">—</div></div>
<div class="result-item"><div class="result-label" id="gap-label">—</div><div class="result-value" id="r-gap">—</div></div>
    </div>
  </div>"""

TAXWITH_SCRIPT = f"""<script>
{SHARED_JS}
function calc(){{
  const salary=parseFloat(document.getElementById('salary').value)||0;
  const freq=parseInt(document.getElementById('freq').value)||26;
  const status=document.getElementById('status').value;
  const step3=parseFloat(document.getElementById('step3').value)||0;
  const current=parseFloat(document.getElementById('current').value)||0;
  const annTax=Math.max(0,calcFedTax(salary,status)-step3);
  const rec=annTax/freq;
  const curAnn=current*freq;
  const gap=curAnn-annTax;
  set('r-rec',fmtd(rec)+'/period');
  set('r-annual',fmt(annTax));
  set('r-cur',fmt(curAnn));
  document.getElementById('gap-label').textContent=gap>=0?'Projected Overpayment (refund)':'Projected Underpayment (owe)';
  const gapEl=document.getElementById('r-gap');
  gapEl.textContent=fmt(Math.abs(gap));
  gapEl.style.color=gap>=0?'#16a34a':'#dc2626';
  document.getElementById('result').classList.add('show');
}}
</script>"""

# paycheck-tax-calculator: gross→net with all taxes
PCTAX_FORM = """  <div class="form-card">
    <h2>Enter Your Information</h2>
    <div class="form-grid">
<div class="field"><label>Annual Gross Salary ($)</label><input id="salary" type="number" value="65000" step="1000" min="0"></div>
<div class="field"><label>Pay Frequency</label><select id="freq"><option value="26">Biweekly (26/yr)</option><option value="24">Semi-monthly (24/yr)</option><option value="12">Monthly (12/yr)</option><option value="52">Weekly (52/yr)</option></select></div>
<div class="field"><label>Filing Status</label><select id="status"><option value="single">Single</option><option value="mfj">Married Filing Jointly</option><option value="hoh">Head of Household</option></select></div>
<div class="field"><label>State Tax Rate (%)</label><input id="state" type="number" value="5" step="0.1" min="0" max="15"></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate Paycheck Tax</button>
  </div>
  <div class="result-card" id="result">
    <h2>Per-Paycheck Tax Breakdown</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Gross Per Paycheck</div><div class="result-value" id="r-gross">—</div></div>
<div class="result-item"><div class="result-label">Federal Income Tax</div><div class="result-value" id="r-fed" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">Social Security</div><div class="result-value" id="r-ss" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">Medicare</div><div class="result-value" id="r-med" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">State Tax</div><div class="result-value" id="r-state" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">Net Paycheck</div><div class="result-value" id="r-net">—</div></div>
    </div>
  </div>"""

PCTAX_SCRIPT = f"""<script>
{SHARED_JS}
function calc(){{
  const salary=parseFloat(document.getElementById('salary').value)||0;
  const freq=parseInt(document.getElementById('freq').value)||26;
  const status=document.getElementById('status').value;
  const stateRate=(parseFloat(document.getElementById('state').value)||0)/100;
  const ppGross=salary/freq;
  const ppFed=calcFedTax(salary,status)/freq;
  const ppSS=Math.min(salary,176100)*0.062/freq;
  const ppMed=salary*0.0145/freq;
  const ppState=salary*stateRate/freq;
  const ppNet=ppGross-ppFed-ppSS-ppMed-ppState;
  set('r-gross',fmtd(ppGross));
  set('r-fed',fmtd(ppFed));
  set('r-ss',fmtd(ppSS));
  set('r-med',fmtd(ppMed));
  set('r-state',fmtd(ppState));
  set('r-net',fmtd(ppNet));
  document.getElementById('result').classList.add('show');
}}
</script>"""

# w4-calculator
W4_FORM = """  <div class="form-card">
    <h2>W-4 Withholding Estimator</h2>
    <div class="form-grid">
<div class="field"><label>Annual Salary (Job 1) ($)</label><input id="job1" type="number" value="75000" step="1000" min="0"></div>
<div class="field"><label>Annual Salary (Job 2, if any) ($)</label><input id="job2" type="number" value="0" step="1000" min="0"></div>
<div class="field"><label>Filing Status</label><select id="status"><option value="single">Single / Separate</option><option value="mfj">Married Filing Jointly</option><option value="hoh">Head of Household</option></select></div>
<div class="field"><label>Number of Children (under 17)</label><input id="children" type="number" value="0" step="1" min="0"></div>
<div class="field"><label>Other Dependents</label><input id="deps" type="number" value="0" step="1" min="0"></div>
<div class="field"><label>Deductions beyond standard ($)</label><input id="extradeds" type="number" value="0" step="500" min="0"></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate W-4 Settings</button>
  </div>
  <div class="result-card" id="result">
    <h2>Recommended W-4 Entries</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Step 3 — Total Credits</div><div class="result-value" id="r-step3">—</div></div>
<div class="result-item"><div class="result-label">Step 4b — Extra Deductions</div><div class="result-value" id="r-step4b">—</div></div>
<div class="result-item"><div class="result-label">Annual Tax Estimate</div><div class="result-value" id="r-tax">—</div></div>
<div class="result-item"><div class="result-label">Withholding per Biweekly Pay</div><div class="result-value" id="r-pp">—</div></div>
    </div>
  </div>"""

W4_SCRIPT = f"""<script>
{SHARED_JS}
function calc(){{
  const job1=parseFloat(document.getElementById('job1').value)||0;
  const job2=parseFloat(document.getElementById('job2').value)||0;
  const status=document.getElementById('status').value;
  const children=parseFloat(document.getElementById('children').value)||0;
  const deps=parseFloat(document.getElementById('deps').value)||0;
  const extradeds=parseFloat(document.getElementById('extradeds').value)||0;
  const totalInc=job1+job2;
  const step3=children*2000+deps*500;
  const annTax=Math.max(0,calcFedTax(totalInc,status)-step3);
  set('r-step3',fmt(step3));
  set('r-step4b',fmt(extradeds));
  set('r-tax',fmt(annTax));
  set('r-pp',fmtd(annTax/26));
  document.getElementById('result').classList.add('show');
}}
</script>"""

# ────────────────────────────────────────────────────────
# Other: SS, Pension, Unemployment, Workers Comp, Wage Garnishment, COL, Living Wage, Min Wage
# ────────────────────────────────────────────────────────
SS_FORM = """  <div class="form-card">
    <h2>Social Security Benefit Estimate</h2>
    <div class="form-grid">
<div class="field"><label>Current Annual Salary ($)</label><input id="salary" type="number" value="75000" step="1000" min="0"></div>
<div class="field"><label>Age Now</label><input id="age" type="number" value="45" step="1" min="22" max="70"></div>
<div class="field"><label>Planned Retirement Age</label><select id="retage"><option value="62">62 (early — reduced)</option><option value="67">67 (full retirement age)</option><option value="70">70 (maximum benefit)</option></select></div>
<div class="field"><label>Years of Work History</label><input id="years" type="number" value="20" step="1" min="0" max="40"></div>
    </div>
    <button class="btn-primary" onclick="calc()">Estimate SS Benefit</button>
  </div>
  <div class="result-card" id="result">
    <h2>Social Security Estimate</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Est. Monthly Benefit at 67</div><div class="result-value" id="r-full">—</div></div>
<div class="result-item"><div class="result-label">Est. Monthly at Chosen Age</div><div class="result-value" id="r-chosen">—</div></div>
<div class="result-item"><div class="result-label">Annual SS Income</div><div class="result-value" id="r-annual">—</div></div>
<div class="result-item"><div class="result-label">SS Taxes Paid (est.)</div><div class="result-value" id="r-paid">—</div></div>
    </div>
  </div>"""

SS_SCRIPT = """<script>
function fmt(n){return'$'+Math.round(n).toLocaleString('en-US');}
function set(id,v){document.getElementById(id).textContent=v;}
function calc(){
  const salary=parseFloat(document.getElementById('salary').value)||0;
  const age=parseFloat(document.getElementById('age').value)||45;
  const retAge=parseInt(document.getElementById('retage').value)||67;
  const years=parseFloat(document.getElementById('years').value)||20;
  // Very simplified SS estimate: ~32% replacement for median wage
  const aime=Math.min(salary,176100)/12;
  let pia=0;
  if(aime<=1226)pia=aime*0.90;
  else if(aime<=7391)pia=1226*0.90+(aime-1226)*0.32;
  else pia=1226*0.90+(7391-1226)*0.32+(aime-7391)*0.15;
  // Bend points approximate for 2026
  const fullBenefit=pia*(Math.min(years,35)/35);
  let chosenBenefit=fullBenefit;
  if(retAge===62)chosenBenefit=fullBenefit*0.70;
  else if(retAge===70)chosenBenefit=fullBenefit*1.24;
  const paid=Math.min(salary,176100)*0.062*(years+(67-age));
  set('r-full',fmt(fullBenefit)+'/mo');
  set('r-chosen',fmt(chosenBenefit)+'/mo');
  set('r-annual',fmt(chosenBenefit*12));
  set('r-paid',fmt(paid));
  document.getElementById('result').classList.add('show');
}
</script>"""

PENSION_FORM = """  <div class="form-card">
    <h2>Pension Benefit Estimate</h2>
    <div class="form-grid">
<div class="field"><label>Final Average Salary ($)</label><input id="salary" type="number" value="80000" step="1000" min="0"></div>
<div class="field"><label>Years of Service</label><input id="years" type="number" value="25" step="1" min="0"></div>
<div class="field"><label>Benefit Multiplier (% per year)</label><input id="mult" type="number" value="1.5" step="0.1" min="0" max="5"></div>
<div class="field"><label>Retirement Age</label><input id="retage" type="number" value="62" step="1" min="50" max="75"></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate Pension</button>
  </div>
  <div class="result-card" id="result">
    <h2>Pension Benefit Estimate</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Annual Pension Benefit</div><div class="result-value" id="r-annual">—</div></div>
<div class="result-item"><div class="result-label">Monthly Pension</div><div class="result-value" id="r-monthly">—</div></div>
<div class="result-item"><div class="result-label">Replacement Rate</div><div class="result-value" id="r-rate">—</div></div>
<div class="result-item"><div class="result-label">Lifetime Value (20 yrs)</div><div class="result-value" id="r-lifetime">—</div></div>
    </div>
  </div>"""

PENSION_SCRIPT = """<script>
function fmt(n){return'$'+Math.round(n).toLocaleString('en-US');}
function set(id,v){document.getElementById(id).textContent=v;}
function calc(){
  const salary=parseFloat(document.getElementById('salary').value)||0;
  const years=parseFloat(document.getElementById('years').value)||0;
  const mult=(parseFloat(document.getElementById('mult').value)||0)/100;
  const annual=salary*years*mult;
  const rate=salary>0?annual/salary*100:0;
  set('r-annual',fmt(annual));
  set('r-monthly',fmt(annual/12));
  set('r-rate',rate.toFixed(1)+'%');
  set('r-lifetime',fmt(annual*20));
  document.getElementById('result').classList.add('show');
}
</script>"""

UNEMP_FORM = """  <div class="form-card">
    <h2>Unemployment Benefit Estimate</h2>
    <div class="form-grid">
<div class="field"><label>Most Recent Weekly Wage ($)</label><input id="weekly" type="number" value="1200" step="50" min="0"></div>
<div class="field"><label>State Benefit Rate (%)</label><input id="rate" type="number" value="50" step="1" min="0" max="70" placeholder="Typically 40-60%"></div>
<div class="field"><label>State Weekly Benefit Cap ($)</label><input id="cap" type="number" value="600" step="50" min="0" placeholder="Varies by state"></div>
<div class="field"><label>Max Benefit Weeks</label><input id="maxwks" type="number" value="26" step="1" min="1" max="52"></div>
    </div>
    <button class="btn-primary" onclick="calc()">Estimate Unemployment Benefits</button>
  </div>
  <div class="result-card" id="result">
    <h2>Unemployment Benefit Estimate</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Weekly Benefit Amount</div><div class="result-value" id="r-weekly">—</div></div>
<div class="result-item"><div class="result-label">Replacement Rate</div><div class="result-value" id="r-rate">—</div></div>
<div class="result-item"><div class="result-label">Monthly Benefit</div><div class="result-value" id="r-monthly">—</div></div>
<div class="result-item"><div class="result-label">Max Total Benefit</div><div class="result-value" id="r-total">—</div></div>
    </div>
  </div>"""

UNEMP_SCRIPT = """<script>
function fmt(n){return'$'+Math.round(n).toLocaleString('en-US');}
function set(id,v){document.getElementById(id).textContent=v;}
function calc(){
  const weekly=parseFloat(document.getElementById('weekly').value)||0;
  const rate=(parseFloat(document.getElementById('rate').value)||0)/100;
  const cap=parseFloat(document.getElementById('cap').value)||600;
  const maxWks=parseFloat(document.getElementById('maxwks').value)||26;
  const benefit=Math.min(weekly*rate,cap);
  const replRate=weekly>0?benefit/weekly*100:0;
  set('r-weekly',fmt(benefit));
  set('r-rate',replRate.toFixed(0)+'%');
  set('r-monthly',fmt(benefit*4.33));
  set('r-total',fmt(benefit*maxWks));
  document.getElementById('result').classList.add('show');
}
</script>"""

GARN_FORM = """  <div class="form-card">
    <h2>Wage Garnishment Calculator</h2>
    <div class="form-grid">
<div class="field"><label>Gross Weekly Pay ($)</label><input id="gross" type="number" value="1000" step="50" min="0"></div>
<div class="field"><label>Garnishment Type</label><select id="type"><option value="consumer">Consumer Debt (25% max)</option><option value="support">Child/Spousal Support (50-65%)</option><option value="tax">Federal Tax Levy</option><option value="student">Student Loan (15%)</option></select></div>
<div class="field"><label>Filing Status</label><select id="status"><option value="single">Single</option><option value="married">Married</option></select></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate Garnishment</button>
  </div>
  <div class="result-card" id="result">
    <h2>Garnishment Estimate</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Maximum Garnishment/Week</div><div class="result-value" id="r-max">—</div></div>
<div class="result-item"><div class="result-label">Disposable Earnings</div><div class="result-value" id="r-disp">—</div></div>
<div class="result-item"><div class="result-label">Take-Home After Garnishment</div><div class="result-value" id="r-net">—</div></div>
<div class="result-item"><div class="result-label">Annual Garnishment Total</div><div class="result-value" id="r-annual">—</div></div>
    </div>
  </div>"""

GARN_SCRIPT = """<script>
function fmt(n){return'$'+n.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}
function set(id,v){document.getElementById(id).textContent=v;}
function calc(){
  const gross=parseFloat(document.getElementById('gross').value)||0;
  const type=document.getElementById('type').value;
  const status=document.getElementById('status').value;
  // Federal min wage weekly protected amount
  const minWage=7.25*30;
  // Disposable earnings ≈ gross minus mandatory deductions (~25%)
  const disposable=gross*0.75;
  let maxGarn=0;
  if(type==='consumer') maxGarn=Math.min(disposable*0.25,Math.max(0,disposable-minWage));
  else if(type==='support') maxGarn=disposable*(status==='single'?0.50:0.60);
  else if(type==='tax') maxGarn=Math.max(0,disposable-(status==='single'?250:300));
  else if(type==='student') maxGarn=Math.min(disposable*0.15,Math.max(0,disposable-minWage));
  const net=gross-maxGarn;
  set('r-max',fmt(maxGarn));
  set('r-disp',fmt(disposable));
  set('r-net',fmt(net));
  set('r-annual',fmt(maxGarn*52));
  document.getElementById('result').classList.add('show');
}
</script>"""

WC_FORM = """  <div class="form-card">
    <h2>Workers' Compensation Estimate</h2>
    <div class="form-grid">
<div class="field"><label>Annual Gross Wages ($)</label><input id="wages" type="number" value="55000" step="1000" min="0"></div>
<div class="field"><label>State WC Rate (per $100 payroll)</label><input id="rate" type="number" value="2.50" step="0.10" min="0" placeholder="Varies by job class & state"></div>
<div class="field"><label>Temporary Disability Benefit (%)</label><input id="tdpct" type="number" value="66.7" step="0.1" min="0" max="100"></div>
<div class="field"><label>Injury Duration (weeks)</label><input id="weeks" type="number" value="0" step="1" min="0"></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate Workers Comp</button>
  </div>
  <div class="result-card" id="result">
    <h2>Workers Comp Estimate</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Annual WC Premium (employer)</div><div class="result-value" id="r-premium">—</div></div>
<div class="result-item"><div class="result-label">Weekly TD Benefit</div><div class="result-value" id="r-td">—</div></div>
<div class="result-item"><div class="result-label">Total TD for Duration</div><div class="result-value" id="r-total">—</div></div>
<div class="result-item"><div class="result-label">Wage Replacement Rate</div><div class="result-value" id="r-rate">—</div></div>
    </div>
  </div>"""

WC_SCRIPT = """<script>
function fmt(n){return'$'+n.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}
function set(id,v){document.getElementById(id).textContent=v;}
function calc(){
  const wages=parseFloat(document.getElementById('wages').value)||0;
  const rate=(parseFloat(document.getElementById('rate').value)||0)/100;
  const tdpct=(parseFloat(document.getElementById('tdpct').value)||0)/100;
  const weeks=parseFloat(document.getElementById('weeks').value)||0;
  const premium=wages*rate;
  const weeklyTD=(wages/52)*tdpct;
  const total=weeklyTD*weeks;
  set('r-premium',fmt(premium));
  set('r-td',fmt(weeklyTD)+'/wk');
  set('r-total',fmt(total));
  set('r-rate',(tdpct*100).toFixed(1)+'%');
  document.getElementById('result').classList.add('show');
}
</script>"""

# severance-tax (separate from severance-pay)
SEVTAX_FORM = """  <div class="form-card">
    <h2>Severance Tax Calculator</h2>
    <div class="form-grid">
<div class="field"><label>Severance Amount ($)</label><input id="sev" type="number" value="50000" step="1000" min="0"></div>
<div class="field"><label>Regular Annual Wages This Year ($)</label><input id="wages" type="number" value="60000" step="1000" min="0"></div>
<div class="field"><label>Filing Status</label><select id="status"><option value="single">Single</option><option value="mfj">Married Filing Jointly</option><option value="hoh">Head of Household</option></select></div>
<div class="field"><label>Withholding Method</label><select id="method"><option value="supp">Supplemental (22% flat)</option><option value="agg">Aggregate (add to wages)</option></select></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate Severance Tax</button>
  </div>
  <div class="result-card" id="result">
    <h2>Severance Tax Breakdown</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Gross Severance</div><div class="result-value" id="r-gross">—</div></div>
<div class="result-item"><div class="result-label">Federal Tax Withheld</div><div class="result-value" id="r-fed" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">FICA (SS + Medicare)</div><div class="result-value" id="r-fica" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">After-Tax Severance</div><div class="result-value" id="r-net">—</div></div>
<div class="result-item"><div class="result-label">Effective Tax Rate</div><div class="result-value" id="r-rate">—</div></div>
    </div>
  </div>"""

SEVTAX_SCRIPT = f"""<script>
{SHARED_JS}
function calc(){{
  const sev=parseFloat(document.getElementById('sev').value)||0;
  const wages=parseFloat(document.getElementById('wages').value)||0;
  const status=document.getElementById('status').value;
  const method=document.getElementById('method').value;
  let fedTax=0;
  if(method==='supp'){{fedTax=sev*0.22;}}
  else{{
    const t1=calcFedTax(wages,status);
    const t2=calcFedTax(wages+sev,status);
    fedTax=t2-t1;
  }}
  const ssBase=Math.max(0,Math.min(wages+sev,176100)-Math.min(wages,176100));
  const fica=ssBase*0.062+sev*0.0145;
  const net=sev-fedTax-fica;
  const rate=(fedTax+fica)/sev*100;
  set('r-gross',fmt(sev));
  set('r-fed',fmt(fedTax));
  set('r-fica',fmt(fica));
  set('r-net',fmt(net));
  set('r-rate',rate.toFixed(1)+'%');
  document.getElementById('result').classList.add('show');
}}
</script>"""

COL_FORM = """  <div class="form-card">
    <h2>Cost of Living Salary Adjustment</h2>
    <div class="form-grid">
<div class="field"><label>Current Salary ($)</label><input id="salary" type="number" value="75000" step="1000" min="0"></div>
<div class="field"><label>Current City COL Index</label><input id="from" type="number" value="100" step="1" min="1" placeholder="100 = US average"></div>
<div class="field"><label>New City COL Index</label><input id="to" type="number" value="120" step="1" min="1" placeholder="NYC ~187, SF ~193, Austin ~110"></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate COL Adjustment</button>
  </div>
  <div class="result-card" id="result">
    <h2>Cost of Living Comparison</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Equivalent Salary in New City</div><div class="result-value" id="r-new">—</div></div>
<div class="result-item"><div class="result-label">Salary Difference</div><div class="result-value" id="r-diff">—</div></div>
<div class="result-item"><div class="result-label">COL Adjustment Factor</div><div class="result-value" id="r-factor">—</div></div>
<div class="result-item"><div class="result-label">Monthly Purchasing Power</div><div class="result-value" id="r-monthly">—</div></div>
    </div>
  </div>"""

COL_SCRIPT = """<script>
function fmt(n){return'$'+Math.round(n).toLocaleString('en-US');}
function set(id,v){document.getElementById(id).textContent=v;}
function calc(){
  const salary=parseFloat(document.getElementById('salary').value)||0;
  const from=parseFloat(document.getElementById('from').value)||100;
  const to=parseFloat(document.getElementById('to').value)||100;
  const factor=to/from;
  const newSal=salary*factor;
  const diff=newSal-salary;
  set('r-new',fmt(newSal));
  const diffEl=document.getElementById('r-diff');
  diffEl.textContent=(diff>=0?'+':'')+fmt(diff);
  diffEl.style.color=diff<0?'#16a34a':'#dc2626';
  set('r-factor',factor.toFixed(2)+'×');
  set('r-monthly',fmt(salary/12)+" buys "+fmt(salary/12/factor)+" in new city");
  document.getElementById('result').classList.add('show');
}
</script>"""

LW_FORM = """  <div class="form-card">
    <h2>Living Wage Calculator</h2>
    <div class="form-grid">
<div class="field"><label>Hourly Wage ($)</label><input id="rate" type="number" value="20" step="0.25" min="0"></div>
<div class="field"><label>Hours per Week</label><input id="hours" type="number" value="40" step="1" min="1" max="80"></div>
<div class="field"><label>Monthly Housing Cost ($)</label><input id="housing" type="number" value="1500" step="100" min="0"></div>
<div class="field"><label>Monthly Other Expenses ($)</label><input id="expenses" type="number" value="2000" step="100" min="0"></div>
    </div>
    <button class="btn-primary" onclick="calc()">Check Living Wage</button>
  </div>
  <div class="result-card" id="result">
    <h2>Living Wage Analysis</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Annual Gross</div><div class="result-value" id="r-annual">—</div></div>
<div class="result-item"><div class="result-label">Monthly Gross</div><div class="result-value" id="r-monthly">—</div></div>
<div class="result-item"><div class="result-label">Monthly Expenses</div><div class="result-value" id="r-exp" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">Monthly Surplus / Shortfall</div><div class="result-value" id="r-surplus">—</div></div>
<div class="result-item"><div class="result-label">Required Hourly for Break-Even</div><div class="result-value" id="r-req">—</div></div>
    </div>
  </div>"""

LW_SCRIPT = """<script>
function fmt(n){return'$'+Math.round(n).toLocaleString('en-US');}
function set(id,v){document.getElementById(id).textContent=v;}
function calc(){
  const rate=parseFloat(document.getElementById('rate').value)||0;
  const hours=parseFloat(document.getElementById('hours').value)||40;
  const housing=parseFloat(document.getElementById('housing').value)||0;
  const other=parseFloat(document.getElementById('expenses').value)||0;
  const annual=rate*hours*52;
  const monthly=annual/12;
  const totalExp=housing+other;
  // Rough net after ~28% taxes
  const monthlyNet=monthly*0.72;
  const surplus=monthlyNet-totalExp;
  const reqHourly=totalExp/0.72/(hours*52/12);
  set('r-annual',fmt(annual));
  set('r-monthly',fmt(monthlyNet)+' (est. net)');
  set('r-exp',fmt(totalExp)+'/mo');
  const surpEl=document.getElementById('r-surplus');
  surpEl.textContent=(surplus>=0?'+':'')+fmt(surplus)+'/mo';
  surpEl.style.color=surplus>=0?'#16a34a':'#dc2626';
  set('r-req','$'+reqHourly.toFixed(2)+'/hr');
  document.getElementById('result').classList.add('show');
}
</script>"""

MINWAGE_FORM = """  <div class="form-card">
    <h2>Minimum Wage Calculator</h2>
    <div class="form-grid">
<div class="field"><label>Hourly Rate ($)</label><input id="rate" type="number" value="15" step="0.25" min="0"></div>
<div class="field"><label>Hours per Week</label><input id="hours" type="number" value="40" step="1" min="0" max="80"></div>
<div class="field"><label>State Minimum Wage ($)</label><input id="minwage" type="number" value="15" step="0.25" min="7.25" placeholder="Federal min: $7.25"></div>
<div class="field"><label>Filing Status</label><select id="status"><option value="single">Single</option><option value="mfj">Married Filing Jointly</option><option value="hoh">Head of Household</option></select></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate</button>
  </div>
  <div class="result-card" id="result">
    <h2>Minimum Wage Analysis</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Annual Gross</div><div class="result-value" id="r-annual">—</div></div>
<div class="result-item"><div class="result-label">vs State Min Wage (annual)</div><div class="result-value" id="r-min">—</div></div>
<div class="result-item"><div class="result-label">Federal Tax</div><div class="result-value" id="r-fed" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">Est. Annual Net Pay</div><div class="result-value" id="r-net">—</div></div>
<div class="result-item"><div class="result-label">Compliance Status</div><div class="result-value" id="r-comply">—</div></div>
    </div>
  </div>"""

MINWAGE_SCRIPT = f"""<script>
{SHARED_JS}
function calc(){{
  const rate=parseFloat(document.getElementById('rate').value)||0;
  const hours=parseFloat(document.getElementById('hours').value)||40;
  const minWage=parseFloat(document.getElementById('minwage').value)||7.25;
  const status=document.getElementById('status').value;
  const annual=rate*hours*52;
  const minAnn=minWage*hours*52;
  const fed=calcFedTax(annual,status);
  const fica=Math.min(annual,176100)*0.062+annual*0.0145;
  const net=annual-fed-fica;
  set('r-annual',fmt(annual));
  set('r-min',fmt(minAnn));
  set('r-fed',fmt(fed));
  set('r-net',fmt(net));
  const comply=rate>=minWage?'Compliant':'BELOW minimum wage!';
  const ce=document.getElementById('r-comply');
  ce.textContent=comply;
  ce.style.color=rate>=minWage?'#16a34a':'#dc2626';
  document.getElementById('result').classList.add('show');
}}
</script>"""

# ────────────────────────────────────────────────────────
# ASSEMBLE ALL
# ────────────────────────────────────────────────────────
ALL_TOOLS = []

for f in SALARY_FILES:
    ALL_TOOLS.append((f, SALARY_FORM, SALARY_SCRIPT))

ALL_TOOLS.append(("tools/part-time-salary-calculator.html", PT_FORM, PT_SCRIPT))

for f in RAISE_FILES:
    ALL_TOOLS.append((f, RAISE_FORM, RAISE_SCRIPT))

ALL_TOOLS += [
    ("tools/salary-comparison-calculator.html", COMP_FORM, COMP_SCRIPT),
    ("tools/salary-negotiation-calculator.html", NEGO_FORM, NEGO_SCRIPT),
]

ALL_TOOLS += ROLE_TOOLS

ALL_TOOLS += [
    ("tools/holiday-pay-calculator.html",   HOL_FORM,     HOL_SCRIPT),
    ("tools/shift-differential-calculator.html", SHIFT_FORM, SHIFT_SCRIPT),
    ("tools/tip-calculator.html",           TIP_FORM,     TIP_SCRIPT),
    ("tools/back-pay-calculator.html",      BACKPAY_FORM, BACKPAY_SCRIPT),
    ("tools/tax-refund-calculator.html",    TAXREFUND_FORM, TAXREFUND_SCRIPT),
    ("tools/tax-withholding-calculator.html", TAXWITH_FORM, TAXWITH_SCRIPT),
    ("tools/paycheck-tax-calculator.html",  PCTAX_FORM,   PCTAX_SCRIPT),
    ("tools/w4-calculator.html",            W4_FORM,      W4_SCRIPT),
    ("tools/social-security-calculator.html", SS_FORM,    SS_SCRIPT),
    ("tools/pension-calculator.html",       PENSION_FORM, PENSION_SCRIPT),
    ("tools/unemployment-calculator.html",  UNEMP_FORM,   UNEMP_SCRIPT),
    ("tools/wage-garnishment-calculator.html", GARN_FORM, GARN_SCRIPT),
    ("tools/workers-comp-calculator.html",  WC_FORM,      WC_SCRIPT),
    ("tools/severance-tax-calculator.html", SEVTAX_FORM,  SEVTAX_SCRIPT),
    ("tools/cost-of-living-calculator.html", COL_FORM,    COL_SCRIPT),
    ("tools/living-wage-calculator.html",   LW_FORM,      LW_SCRIPT),
    ("tools/minimum-wage-calculator.html",  MINWAGE_FORM, MINWAGE_SCRIPT),
]

print(f"=== Batch B: {len(ALL_TOOLS)} tools ===")
changed=0
skipped=[]
for path,new_form,new_script in ALL_TOOLS:
    with open(path,"r",encoding="utf-8") as f: c=f.read()
    fo=OLD_FORM in c; so=OLD_SCRIPT in c
    if fo: c=c.replace(OLD_FORM,new_form,1)
    if so: c=c.replace(OLD_SCRIPT,new_script,1)
    if fo or so:
        with open(path,"w",encoding="utf-8") as f: f.write(c)
        changed+=1
    else:
        skipped.append(path)

print(f"Changed: {changed}/{len(ALL_TOOLS)}")
if skipped: print("Skipped (already rewritten or no match):", skipped)
