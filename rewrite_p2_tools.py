import os, re

os.chdir(r"C:\Users\Administrator\payrollfixpro")

# ── 共用：旧表单 + 旧脚本（三个工具相同的模板内容）─────────────────────────
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

# ══════════════════════════════════════════════════════════════════════════════
# 1. NET PAY CALCULATOR
# ══════════════════════════════════════════════════════════════════════════════
NETPAY_FORM = """  <div class="form-card">
    <h2>Enter Your Information</h2>
    <div class="form-grid">
<div class="field"><label>Annual Gross Salary ($)</label><input id="salary" type="number" value="60000" step="1000" min="0"></div>
<div class="field"><label>Filing Status</label><select id="status"><option value="single">Single</option><option value="mfj">Married Filing Jointly</option><option value="mfs">Married Filing Separately</option><option value="hoh">Head of Household</option></select></div>
<div class="field"><label>State</label><select id="state">
<option value="0">No State Tax (TX/FL/WA/NV/WY/SD/AK)</option>
<option value="AL">Alabama (5.00%)</option>
<option value="AZ">Arizona (2.50%)</option>
<option value="AR">Arkansas (4.40%)</option>
<option value="CA">California (~9.30%)</option>
<option value="CO">Colorado (4.40%)</option>
<option value="CT">Connecticut (5.00%)</option>
<option value="DE">Delaware (5.55%)</option>
<option value="GA">Georgia (5.49%)</option>
<option value="HI">Hawaii (7.90%)</option>
<option value="ID">Idaho (5.80%)</option>
<option value="IL">Illinois (4.95%)</option>
<option value="IN">Indiana (3.05%)</option>
<option value="IA">Iowa (3.80%)</option>
<option value="KS">Kansas (5.70%)</option>
<option value="KY">Kentucky (4.00%)</option>
<option value="LA">Louisiana (3.00%)</option>
<option value="ME">Maine (5.80%)</option>
<option value="MD">Maryland (4.75%)</option>
<option value="MA">Massachusetts (5.00%)</option>
<option value="MI">Michigan (4.25%)</option>
<option value="MN">Minnesota (6.80%)</option>
<option value="MS">Mississippi (4.70%)</option>
<option value="MO">Missouri (4.80%)</option>
<option value="MT">Montana (5.90%)</option>
<option value="NE">Nebraska (5.84%)</option>
<option value="NH">New Hampshire (0%)</option>
<option value="NJ">New Jersey (6.37%)</option>
<option value="NM">New Mexico (4.90%)</option>
<option value="NY">New York (~6.25%)</option>
<option value="NC">North Carolina (4.50%)</option>
<option value="ND">North Dakota (1.10%)</option>
<option value="OH">Ohio (3.50%)</option>
<option value="OK">Oklahoma (4.75%)</option>
<option value="OR">Oregon (8.75%)</option>
<option value="PA">Pennsylvania (3.07%)</option>
<option value="RI">Rhode Island (4.75%)</option>
<option value="SC">South Carolina (6.40%)</option>
<option value="UT">Utah (4.55%)</option>
<option value="VT">Vermont (6.60%)</option>
<option value="VA">Virginia (5.75%)</option>
<option value="WV">West Virginia (4.50%)</option>
<option value="WI">Wisconsin (5.30%)</option>
</select></div>
<div class="field"><label>401(k) Contribution (%)</label><input id="k401" type="number" value="5" step="0.5" min="0" max="100"></div>
<div class="field"><label>Health Insurance ($/year)</label><input id="health" type="number" value="2400" step="100" min="0"></div>
<div class="field"><label>Other Pre-Tax Deductions ($/year)</label><input id="other" type="number" value="0" step="100" min="0"></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate Net Pay</button>
  </div>
  <div class="result-card" id="result">
    <h2>Net Pay Breakdown</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Annual Net Pay</div><div class="result-value" id="r-annual">—</div></div>
<div class="result-item"><div class="result-label">Monthly Net Pay</div><div class="result-value" id="r-monthly">—</div></div>
<div class="result-item"><div class="result-label">Biweekly Net Pay</div><div class="result-value" id="r-biweekly">—</div></div>
<div class="result-item"><div class="result-label">Weekly Net Pay</div><div class="result-value" id="r-weekly">—</div></div>
<div class="result-item" style="border-top:2px solid #e2e8f0;padding-top:14px"><div class="result-label">Federal Income Tax</div><div class="result-value" id="r-fed" style="color:#dc2626">—</div></div>
<div class="result-item" style="border-top:2px solid #e2e8f0;padding-top:14px"><div class="result-label">FICA (SS + Medicare)</div><div class="result-value" id="r-fica" style="color:#dc2626">—</div></div>
<div class="result-item" style="border-top:2px solid #e2e8f0;padding-top:14px"><div class="result-label">State Income Tax</div><div class="result-value" id="r-state" style="color:#dc2626">—</div></div>
<div class="result-item" style="border-top:2px solid #e2e8f0;padding-top:14px"><div class="result-label">Pre-Tax Deductions</div><div class="result-value" id="r-pretax" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">Effective Tax Rate</div><div class="result-value" id="r-rate">—</div></div>
    </div>
  </div>"""

NETPAY_SCRIPT = """<script>
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
  for(let i=0;i<b.length;i++){const[upper,rate]=b[i];if(taxable<=prev)break;tax+=(Math.min(taxable,upper)-prev)*rate;prev=upper;}
  return tax;
}
const STATE_RATES={
  "0":0,"AL":0.05,"AZ":0.025,"AR":0.044,"CA":0.093,"CO":0.044,"CT":0.05,
  "DE":0.0555,"GA":0.0549,"HI":0.079,"ID":0.058,"IL":0.0495,"IN":0.0305,
  "IA":0.038,"KS":0.057,"KY":0.04,"LA":0.03,"ME":0.058,"MD":0.0475,
  "MA":0.05,"MI":0.0425,"MN":0.068,"MS":0.047,"MO":0.048,"MT":0.059,
  "NE":0.0584,"NH":0,"NJ":0.0637,"NM":0.049,"NY":0.0625,"NC":0.045,
  "ND":0.011,"OH":0.035,"OK":0.0475,"OR":0.0875,"PA":0.0307,"RI":0.0475,
  "SC":0.064,"UT":0.0455,"VT":0.066,"VA":0.0575,"WV":0.045,"WI":0.053
};
function fmt(n){return'$'+Math.round(n).toLocaleString('en-US');}
function set(id,v){document.getElementById(id).textContent=v;}
function calc(){
  const salary=parseFloat(document.getElementById('salary').value)||0;
  const status=document.getElementById('status').value;
  const stKey=document.getElementById('state').value;
  const k401pct=(parseFloat(document.getElementById('k401').value)||0)/100;
  const health=parseFloat(document.getElementById('health').value)||0;
  const other=parseFloat(document.getElementById('other').value)||0;

  const ann401k=salary*k401pct;
  const annPreTax=ann401k+health+other;
  const annTaxable=Math.max(0,salary-annPreTax);

  const annFed=calcFedTax(annTaxable,status);
  const annSS=Math.min(salary,176100)*0.062;
  const annMed=salary*0.0145+(salary>200000?(salary-200000)*0.009:0);
  const annFica=annSS+annMed;
  const stRate=STATE_RATES[stKey]||0;
  const annState=annTaxable*stRate;

  const annNet=salary-annFed-annFica-annState-annPreTax;

  set('r-annual',fmt(annNet));
  set('r-monthly',fmt(annNet/12));
  set('r-biweekly',fmt(annNet/26));
  set('r-weekly',fmt(annNet/52));
  set('r-fed',fmt(annFed)+'/yr');
  set('r-fica',fmt(annFica)+'/yr');
  set('r-state',fmt(annState)+'/yr');
  set('r-pretax',fmt(annPreTax)+'/yr');
  const effRate=salary>0?((annFed+annFica+annState)/salary*100):0;
  set('r-rate',effRate.toFixed(1)+'%');
  document.getElementById('result').classList.add('show');
}
</script>"""

NETPAY_RESULT_IDS = ['r-annual','r-monthly','r-biweekly','r-weekly','r-fed','r-fica','r-state','r-pretax','r-rate']

# ══════════════════════════════════════════════════════════════════════════════
# 2. PAYROLL TAX CALCULATOR (雇主视角)
# ══════════════════════════════════════════════════════════════════════════════
PAYROLLTAX_FORM = """  <div class="form-card">
    <h2>Enter Employee & Payroll Information</h2>
    <div class="form-grid">
<div class="field"><label>Employee Gross Wages ($)</label><input id="wages" type="number" value="5000" step="100" min="0"></div>
<div class="field"><label>Pay Frequency</label><select id="freq"><option value="26">Biweekly (26/yr)</option><option value="24">Semi-monthly (24/yr)</option><option value="12">Monthly (12/yr)</option><option value="52">Weekly (52/yr)</option><option value="1">Annual (1/yr)</option></select></div>
<div class="field"><label>YTD Wages Paid So Far ($)</label><input id="ytd" type="number" value="0" step="1000" min="0" placeholder="0 if first paycheck"></div>
<div class="field"><label>State SUTA Rate (%)</label><input id="suta" type="number" value="2.7" step="0.1" min="0" max="20" placeholder="e.g. 2.7"></div>
<div class="field"><label>State SUTA Wage Base ($)</label><input id="sutaBase" type="number" value="7000" step="500" min="0" placeholder="varies by state"></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate Employer Taxes</button>
  </div>
  <div class="result-card" id="result">
    <h2>Employer Tax Costs — This Paycheck</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Employer SS (6.2%)</div><div class="result-value" id="r-ss">—</div></div>
<div class="result-item"><div class="result-label">Employer Medicare (1.45%)</div><div class="result-value" id="r-med">—</div></div>
<div class="result-item"><div class="result-label">FUTA (0.6% eff.)</div><div class="result-value" id="r-futa">—</div></div>
<div class="result-item"><div class="result-label">SUTA (State)</div><div class="result-value" id="r-suta">—</div></div>
<div class="result-item"><div class="result-label">Total Employer Tax</div><div class="result-value" id="r-total">—</div></div>
<div class="result-item"><div class="result-label">Total Cost Per Employee</div><div class="result-value" id="r-cost">—</div></div>
<div class="result-item"><div class="result-label">Annual Employer SS+Med</div><div class="result-value" id="r-ann-fica">—</div></div>
    </div>
  </div>"""

PAYROLLTAX_SCRIPT = """<script>
function fmt(n){return'$'+n.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});}
function set(id,v){document.getElementById(id).textContent=v;}
function calc(){
  const wages=parseFloat(document.getElementById('wages').value)||0;
  const freq=parseInt(document.getElementById('freq').value)||26;
  const ytd=parseFloat(document.getElementById('ytd').value)||0;
  const sutaRate=(parseFloat(document.getElementById('suta').value)||0)/100;
  const sutaBase=parseFloat(document.getElementById('sutaBase').value)||7000;

  // Social Security: 6.2% up to $176,100 annual wage base
  const SS_BASE=176100;
  const ytdAfter=ytd+wages;
  const ssWages=Math.max(0,Math.min(ytdAfter,SS_BASE)-Math.min(ytd,SS_BASE));
  const empSS=ssWages*0.062;

  // Medicare: 1.45% (no cap, employer never pays Additional Medicare Tax)
  const empMed=wages*0.0145;

  // FUTA: 6% on first $7,000 per employee per year; effective rate 0.6% after state credit
  const FUTA_BASE=7000;
  const futaWages=Math.max(0,Math.min(ytdAfter,FUTA_BASE)-Math.min(ytd,FUTA_BASE));
  const empFuta=futaWages*0.006; // effective after full state credit

  // SUTA
  const sutaWages=Math.max(0,Math.min(ytdAfter,sutaBase)-Math.min(ytd,sutaBase));
  const empSuta=sutaWages*sutaRate;

  const totalTax=empSS+empMed+empFuta+empSuta;
  const totalCost=wages+totalTax;

  // Annualized SS + Med (assuming full year at this wage)
  const annWages=wages*freq;
  const annSS=Math.min(annWages,SS_BASE)*0.062;
  const annMed=annWages*0.0145;
  const annFica=annSS+annMed;

  set('r-ss',fmt(empSS));
  set('r-med',fmt(empMed));
  set('r-futa',fmt(empFuta));
  set('r-suta',fmt(empSuta));
  set('r-total',fmt(totalTax));
  set('r-cost',fmt(totalCost));
  set('r-ann-fica',fmt(annFica));
  document.getElementById('result').classList.add('show');
}
</script>"""

# ══════════════════════════════════════════════════════════════════════════════
# 3. STATE TAX CALCULATOR — 全50州真实税率
# ══════════════════════════════════════════════════════════════════════════════
STATETAX_FORM = """  <div class="form-card">
    <h2>Enter Your Information</h2>
    <div class="form-grid">
<div class="field"><label>Annual Income ($)</label><input id="income" type="number" value="75000" step="1000" min="0"></div>
<div class="field"><label>Filing Status</label><select id="status"><option value="single">Single</option><option value="mfj">Married Filing Jointly</option><option value="hoh">Head of Household</option></select></div>
<div class="field full"><label>State</label><select id="state">
<option value="AK">Alaska — No Income Tax</option>
<option value="FL">Florida — No Income Tax</option>
<option value="NV">Nevada — No Income Tax</option>
<option value="SD">South Dakota — No Income Tax</option>
<option value="TN">Tennessee — No Income Tax</option>
<option value="TX">Texas — No Income Tax</option>
<option value="WA">Washington — No Income Tax</option>
<option value="WY">Wyoming — No Income Tax</option>
<option value="NH">New Hampshire — 0% (wages)</option>
<option value="AL">Alabama</option>
<option value="AZ">Arizona</option>
<option value="AR">Arkansas</option>
<option value="CA">California</option>
<option value="CO">Colorado</option>
<option value="CT">Connecticut</option>
<option value="DE">Delaware</option>
<option value="GA">Georgia</option>
<option value="HI">Hawaii</option>
<option value="ID">Idaho</option>
<option value="IL">Illinois</option>
<option value="IN">Indiana</option>
<option value="IA">Iowa</option>
<option value="KS">Kansas</option>
<option value="KY">Kentucky</option>
<option value="LA">Louisiana</option>
<option value="ME">Maine</option>
<option value="MD">Maryland</option>
<option value="MA">Massachusetts</option>
<option value="MI">Michigan</option>
<option value="MN">Minnesota</option>
<option value="MS">Mississippi</option>
<option value="MO">Missouri</option>
<option value="MT">Montana</option>
<option value="NE">Nebraska</option>
<option value="NJ">New Jersey</option>
<option value="NM">New Mexico</option>
<option value="NY">New York</option>
<option value="NC">North Carolina</option>
<option value="ND">North Dakota</option>
<option value="OH">Ohio</option>
<option value="OK">Oklahoma</option>
<option value="OR">Oregon</option>
<option value="PA">Pennsylvania</option>
<option value="RI">Rhode Island</option>
<option value="SC">South Carolina</option>
<option value="UT">Utah</option>
<option value="VT">Vermont</option>
<option value="VA">Virginia</option>
<option value="WV">West Virginia</option>
<option value="WI">Wisconsin</option>
</select></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate State Tax</button>
  </div>
  <div class="result-card" id="result">
    <h2>State Tax Estimate</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">State</div><div class="result-value" id="r-state-name">—</div></div>
<div class="result-item"><div class="result-label">Taxable Income</div><div class="result-value" id="r-taxable">—</div></div>
<div class="result-item"><div class="result-label">Annual State Tax</div><div class="result-value" id="r-annual">—</div></div>
<div class="result-item"><div class="result-label">Monthly State Tax</div><div class="result-value" id="r-monthly">—</div></div>
<div class="result-item"><div class="result-label">Biweekly State Tax</div><div class="result-value" id="r-biweekly">—</div></div>
<div class="result-item"><div class="result-label">Effective State Rate</div><div class="result-value" id="r-rate">—</div></div>
    </div>
  </div>"""

STATETAX_SCRIPT = """<script>
// State tax data: [brackets_single, brackets_mfj, std_ded_single, std_ded_mfj, label]
// Flat-rate states stored as [[Infinity, rate]]
// Progressive states use actual 2025/2026 brackets
const ST={
  AK:{label:"Alaska",flat:true,rate:0},
  FL:{label:"Florida",flat:true,rate:0},
  NV:{label:"Nevada",flat:true,rate:0},
  SD:{label:"South Dakota",flat:true,rate:0},
  TN:{label:"Tennessee",flat:true,rate:0},
  TX:{label:"Texas",flat:true,rate:0},
  WA:{label:"Washington",flat:true,rate:0},
  WY:{label:"Wyoming",flat:true,rate:0},
  NH:{label:"New Hampshire",flat:true,rate:0},
  // Flat-rate states
  IL:{label:"Illinois",flat:true,rate:0.0495,std:{single:2775,mfj:5550,hoh:2775}},
  IN:{label:"Indiana",flat:true,rate:0.0305,std:{single:1000,mfj:2000,hoh:1000}},
  KY:{label:"Kentucky",flat:true,rate:0.04,std:{single:3160,mfj:3160,hoh:3160}},
  MA:{label:"Massachusetts",flat:true,rate:0.05,std:{single:4400,mfj:8800,hoh:6800}},
  MI:{label:"Michigan",flat:true,rate:0.0425,std:{single:5000,mfj:10000,hoh:5000}},
  NC:{label:"North Carolina",flat:true,rate:0.045,std:{single:12750,mfj:25500,hoh:19125}},
  PA:{label:"Pennsylvania",flat:true,rate:0.0307,std:{single:0,mfj:0,hoh:0}},
  UT:{label:"Utah",flat:true,rate:0.0455,std:{single:886,mfj:1772,hoh:886}},
  CO:{label:"Colorado",flat:true,rate:0.044,std:{single:14600,mfj:29200,hoh:14600}},
  // Progressive states (simplified brackets, single / mfj)
  AL:{label:"Alabama",std:{single:3000,mfj:8500,hoh:4700},
    br:{single:[[500,.02],[2500,.04],[Infinity,.05]],mfj:[[1000,.02],[6000,.04],[Infinity,.05]],hoh:[[500,.02],[2500,.04],[Infinity,.05]]}},
  AZ:{label:"Arizona",std:{single:14600,mfj:29200,hoh:14600},
    br:{single:[[28653,.025],[Infinity,.025]],mfj:[[57305,.025],[Infinity,.025]],hoh:[[28653,.025],[Infinity,.025]]}},
  AR:{label:"Arkansas",std:{single:2200,mfj:4400,hoh:2200},
    br:{single:[[4300,.02],[8500,.04],[Infinity,.044]],mfj:[[4300,.02],[8500,.04],[Infinity,.044]],hoh:[[4300,.02],[8500,.04],[Infinity,.044]]}},
  CA:{label:"California",std:{single:5540,mfj:11080,hoh:11640},
    br:{single:[[10756,.01],[25499,.02],[40245,.04],[55866,.06],[70606,.08],[360659,.093],[432787,.103],[721314,.113],[Infinity,.123]],
       mfj:[[21512,.01],[50998,.02],[80490,.04],[111732,.06],[141212,.08],[721318,.093],[865574,.103],[1000000,.123],[Infinity,.133]],
       hoh:[[21527,.01],[51038,.02],[65744,.04],[81364,.06],[96107,.08],[490493,.093],[588593,.103],[1000000,.123],[Infinity,.133]]}},
  CT:{label:"Connecticut",std:{single:0,mfj:0,hoh:0},
    br:{single:[[10000,.03],[50000,.05],[100000,.055],[200000,.06],[250000,.065],[500000,.069],[Infinity,.0699]],
       mfj:[[20000,.03],[100000,.05],[200000,.055],[400000,.06],[500000,.065],[1000000,.069],[Infinity,.0699]],
       hoh:[[16000,.03],[80000,.05],[160000,.055],[320000,.06],[400000,.065],[800000,.069],[Infinity,.0699]]}},
  DE:{label:"Delaware",std:{single:3250,mfj:6500,hoh:3250},
    br:{single:[[2000,0],[5000,.022],[10000,.039],[20000,.048],[25000,.052],[60000,.055],[Infinity,.066]],
       mfj:[[2000,0],[5000,.022],[10000,.039],[20000,.048],[25000,.052],[60000,.055],[Infinity,.066]],
       hoh:[[2000,0],[5000,.022],[10000,.039],[20000,.048],[25000,.052],[60000,.055],[Infinity,.066]]}},
  GA:{label:"Georgia",std:{single:12000,mfj:24000,hoh:18000},
    br:{single:[[Infinity,.0549]],mfj:[[Infinity,.0549]],hoh:[[Infinity,.0549]]}},
  HI:{label:"Hawaii",std:{single:2200,mfj:4400,hoh:3212},
    br:{single:[[2400,.014],[4800,.032],[9600,.055],[14400,.064],[19200,.068],[24000,.072],[36000,.076],[48000,.079],[Infinity,.11]],
       mfj:[[4800,.014],[9600,.032],[19200,.055],[28800,.064],[38400,.068],[48000,.072],[72000,.076],[96000,.079],[Infinity,.11]],
       hoh:[[3600,.014],[7200,.032],[14400,.055],[21600,.064],[28800,.068],[36000,.072],[54000,.076],[72000,.079],[Infinity,.11]]}},
  ID:{label:"Idaho",std:{single:14600,mfj:29200,hoh:14600},
    br:{single:[[Infinity,.058]],mfj:[[Infinity,.058]],hoh:[[Infinity,.058]]}},
  IA:{label:"Iowa",std:{single:14600,mfj:29200,hoh:14600},
    br:{single:[[6210,.044],[31050,.0482],[Infinity,.057]],mfj:[[6210,.044],[31050,.0482],[Infinity,.057]],hoh:[[6210,.044],[31050,.0482],[Infinity,.057]]}},
  KS:{label:"Kansas",std:{single:3500,mfj:8000,hoh:6000},
    br:{single:[[15000,.031],[30000,.0525],[Infinity,.057]],mfj:[[30000,.031],[60000,.0525],[Infinity,.057]],hoh:[[15000,.031],[30000,.0525],[Infinity,.057]]}},
  LA:{label:"Louisiana",std:{single:4500,mfj:9000,hoh:4500},
    br:{single:[[12500,.185],[50000,.035],[Infinity,.0425]],mfj:[[25000,.185],[100000,.035],[Infinity,.0425]],hoh:[[12500,.185],[50000,.035],[Infinity,.0425]]}},
  ME:{label:"Maine",std:{single:14600,mfj:29200,hoh:14600},
    br:{single:[[26050,.058],[61600,.0675],[Infinity,.0715]],mfj:[[52100,.058],[123200,.0675],[Infinity,.0715]],hoh:[[39075,.058],[92400,.0675],[Infinity,.0715]]}},
  MD:{label:"Maryland",std:{single:2400,mfj:4800,hoh:2800},
    br:{single:[[1000,.02],[2000,.03],[3000,.04],[100000,.0475],[125000,.05],[150000,.0525],[250000,.055],[Infinity,.0575]],
       mfj:[[1000,.02],[2000,.03],[3000,.04],[150000,.0475],[175000,.05],[225000,.0525],[300000,.055],[Infinity,.0575]],
       hoh:[[1000,.02],[2000,.03],[3000,.04],[125000,.0475],[150000,.05],[175000,.0525],[250000,.055],[Infinity,.0575]]}},
  MN:{label:"Minnesota",std:{single:14575,mfj:29150,hoh:21825},
    br:{single:[[31690,.0535],[104090,.068],[174400,.0785],[Infinity,.0985]],
       mfj:[[46330,.0535],[184040,.068],[321450,.0785],[Infinity,.0985]],
       hoh:[[39090,.0535],[157110,.068],[261040,.0785],[Infinity,.0985]]}},
  MS:{label:"Mississippi",std:{single:2300,mfj:4600,hoh:3400},
    br:{single:[[10000,0],[Infinity,.047]],mfj:[[10000,0],[Infinity,.047]],hoh:[[10000,0],[Infinity,.047]]}},
  MO:{label:"Missouri",std:{single:14600,mfj:29200,hoh:14600},
    br:{single:[[1207,.015],[2414,.02],[3621,.025],[4828,.03],[6035,.035],[7242,.04],[8432,.045],[Infinity,.048]],
       mfj:[[1207,.015],[2414,.02],[3621,.025],[4828,.03],[6035,.035],[7242,.04],[8432,.045],[Infinity,.048]],
       hoh:[[1207,.015],[2414,.02],[3621,.025],[4828,.03],[6035,.035],[7242,.04],[8432,.045],[Infinity,.048]]}},
  MT:{label:"Montana",std:{single:5540,mfj:11080,hoh:8810},
    br:{single:[[20500,.047],[Infinity,.059]],mfj:[[41000,.047],[Infinity,.059]],hoh:[[30750,.047],[Infinity,.059]]}},
  NE:{label:"Nebraska",std:{single:7900,mfj:15800,hoh:7900},
    br:{single:[[3700,.246],[22170,.351],[35730,.0501],[Infinity,.0584]],
       mfj:[[7390,.246],[44350,.351],[71460,.0501],[Infinity,.0584]],
       hoh:[[3700,.246],[22170,.351],[35730,.0501],[Infinity,.0584]]}},
  NJ:{label:"New Jersey",std:{single:0,mfj:0,hoh:0},
    br:{single:[[20000,.014],[35000,.0175],[40000,.035],[75000,.0553],[500000,.0637],[1000000,.0897],[Infinity,.1075]],
       mfj:[[20000,.014],[50000,.0175],[70000,.0245],[80000,.035],[150000,.0553],[500000,.0637],[1000000,.0897],[Infinity,.1075]],
       hoh:[[20000,.014],[50000,.0175],[70000,.0245],[80000,.035],[150000,.0553],[500000,.0637],[1000000,.0897],[Infinity,.1075]]}},
  NM:{label:"New Mexico",std:{single:14600,mfj:29200,hoh:14600},
    br:{single:[[5500,.017],[11000,.032],[16000,.047],[210000,.049],[Infinity,.059]],
       mfj:[[8000,.017],[16000,.032],[24000,.047],[315000,.049],[Infinity,.059]],
       hoh:[[8000,.017],[16000,.032],[24000,.047],[315000,.049],[Infinity,.059]]}},
  NY:{label:"New York",std:{single:8000,mfj:16050,hoh:11200},
    br:{single:[[17150,.04],[23600,.045],[27900,.0525],[161550,.0585],[323200,.0625],[2155350,.0685],[5000000,.0965],[25000000,.103],[Infinity,.109]],
       mfj:[[27900,.04],[43000,.045],[161550,.0525],[323200,.0585],[2155350,.0625],[5000000,.0965],[25000000,.103],[Infinity,.109]],
       hoh:[[17650,.04],[28500,.045],[107650,.0525],[269300,.0585],[2155350,.0625],[5000000,.0965],[25000000,.103],[Infinity,.109]]}},
  ND:{label:"North Dakota",std:{single:14600,mfj:29200,hoh:14600},
    br:{single:[[44725,.011],[225975,.0204],[Infinity,.0264]],
       mfj:[[74750,.011],[275100,.0204],[Infinity,.0264]],
       hoh:[[59850,.011],[250450,.0204],[Infinity,.0264]]}},
  OH:{label:"Ohio",std:{single:0,mfj:0,hoh:0},
    br:{single:[[26050,0],[46100,.02765],[92150,.03226],[115300,.03688],[Infinity,.03990]],
       mfj:[[26050,0],[46100,.02765],[92150,.03226],[115300,.03688],[Infinity,.03990]],
       hoh:[[26050,0],[46100,.02765],[92150,.03226],[115300,.03688],[Infinity,.03990]]}},
  OK:{label:"Oklahoma",std:{single:6350,mfj:12700,hoh:9350},
    br:{single:[[1000,.005],[2500,.01],[3750,.02],[4900,.03],[7200,.04],[Infinity,.0475]],
       mfj:[[2000,.005],[5000,.01],[7500,.02],[9800,.03],[12200,.04],[Infinity,.0475]],
       hoh:[[2000,.005],[5000,.01],[7500,.02],[9800,.03],[12200,.04],[Infinity,.0475]]}},
  OR:{label:"Oregon",std:{single:2745,mfj:5495,hoh:4120},
    br:{single:[[4050,.0475],[10200,.0675],[125000,.0875],[Infinity,.099]],
       mfj:[[8100,.0475],[20400,.0675],[250000,.0875],[Infinity,.099]],
       hoh:[[6075,.0475],[15300,.0675],[187500,.0875],[Infinity,.099]]}},
  RI:{label:"Rhode Island",std:{single:10550,mfj:21100,hoh:10550},
    br:{single:[[77450,.0375],[176050,.0475],[Infinity,.0599]],
       mfj:[[77450,.0375],[176050,.0475],[Infinity,.0599]],
       hoh:[[77450,.0375],[176050,.0475],[Infinity,.0599]]}},
  SC:{label:"South Carolina",std:{single:14600,mfj:29200,hoh:14600},
    br:{single:[[3460,0],[17330,.03],[Infinity,.064]],
       mfj:[[3460,0],[17330,.03],[Infinity,.064]],
       hoh:[[3460,0],[17330,.03],[Infinity,.064]]}},
  VT:{label:"Vermont",std:{single:6500,mfj:13000,hoh:9750},
    br:{single:[[45400,.0335],[110050,.066],[229550,.076],[Infinity,.0875]],
       mfj:[[75850,.0335],[183400,.066],[236350,.076],[Infinity,.0875]],
       hoh:[[60625,.0335],[146725,.066],[232950,.076],[Infinity,.0875]]}},
  VA:{label:"Virginia",std:{single:8000,mfj:16000,hoh:8000},
    br:{single:[[3000,.02],[5000,.03],[17000,.05],[Infinity,.0575]],
       mfj:[[3000,.02],[5000,.03],[17000,.05],[Infinity,.0575]],
       hoh:[[3000,.02],[5000,.03],[17000,.05],[Infinity,.0575]]}},
  WV:{label:"West Virginia",std:{single:0,mfj:0,hoh:0},
    br:{single:[[10000,.0236],[25000,.0315],[Infinity,.0465]],
       mfj:[[10000,.0236],[25000,.0315],[Infinity,.0465]],
       hoh:[[10000,.0236],[25000,.0315],[Infinity,.0465]]}},
  WI:{label:"Wisconsin",std:{single:13260,mfj:24690,hoh:16210},
    br:{single:[[14320,.035],[28640,.044],[315310,.053],[Infinity,.0765]],
       mfj:[[19090,.035],[38190,.044],[420420,.053],[Infinity,.0765]],
       hoh:[[14320,.035],[28640,.044],[315310,.053],[Infinity,.0765]]}}
};
function calcStateTax(income,stKey,status){
  const s=ST[stKey];
  if(!s)return 0;
  if(s.flat){
    if(s.rate===0)return 0;
    const ded=(s.std&&s.std[status])||0;
    return Math.max(0,income-ded)*s.rate;
  }
  // progressive
  const ded=(s.std&&s.std[status])||0;
  const taxable=Math.max(0,income-ded);
  const brackets=s.br[status]||s.br.single;
  let tax=0,prev=0;
  for(let i=0;i<brackets.length;i++){
    const[upper,rate]=brackets[i];
    if(taxable<=prev)break;
    tax+=(Math.min(taxable,upper)-prev)*rate;
    prev=upper;
  }
  return tax;
}
function fmt(n){return'$'+Math.round(n).toLocaleString('en-US');}
function set(id,v){document.getElementById(id).textContent=v;}
function calc(){
  const income=parseFloat(document.getElementById('income').value)||0;
  const status=document.getElementById('status').value;
  const stKey=document.getElementById('state').value;
  const s=ST[stKey];
  const stateName=s?s.label:stKey;
  const tax=calcStateTax(income,stKey,status);
  const ded=s&&s.std?((s.std[status])||0):0;
  const taxable=Math.max(0,income-ded);
  const effRate=income>0?(tax/income*100):0;
  set('r-state-name',stateName);
  set('r-taxable',fmt(taxable));
  set('r-annual',fmt(tax));
  set('r-monthly',fmt(tax/12));
  set('r-biweekly',fmt(tax/26));
  set('r-rate',effRate.toFixed(2)+'%');
  document.getElementById('result').classList.add('show');
}
</script>"""

# ══════════════════════════════════════════════════════════════════════════════
# 执行替换
# ══════════════════════════════════════════════════════════════════════════════
TOOLS = [
    ("tools/net-pay-calculator.html",       NETPAY_FORM,     NETPAY_SCRIPT),
    ("tools/payroll-tax-calculator.html",   PAYROLLTAX_FORM, PAYROLLTAX_SCRIPT),
    ("tools/state-tax-calculator.html",     STATETAX_FORM,   STATETAX_SCRIPT),
]

print("=== Rewriting P2 tools ===")
changed = 0
for path, new_form, new_script in TOOLS:
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()

    form_ok = OLD_FORM in c
    script_ok = OLD_SCRIPT in c

    if form_ok:
        c = c.replace(OLD_FORM, new_form, 1)
    if script_ok:
        c = c.replace(OLD_SCRIPT, new_script, 1)

    if form_ok or script_ok:
        with open(path, "w", encoding="utf-8") as f:
            f.write(c)
        changed += 1
        print(f"  {path}: form={form_ok} script={script_ok}")
    else:
        print(f"  {path}: NO MATCH — check OLD_FORM/OLD_SCRIPT")

print(f"\nFiles changed: {changed}/3")
