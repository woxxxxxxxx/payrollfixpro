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

# ── SEVERANCE PAY ──────────────────────────────────────────────────────────
SEV_FORM = """  <div class="form-card">
    <h2>Enter Your Information</h2>
    <div class="form-grid">
<div class="field"><label>Annual Base Salary ($)</label><input id="salary" type="number" value="80000" step="1000" min="0"></div>
<div class="field"><label>Years of Service</label><input id="years" type="number" value="5" step="0.5" min="0"></div>
<div class="field"><label>Severance Policy</label><select id="policy"><option value="weeks">Weeks per Year of Service</option><option value="fixed">Fixed Lump Sum</option></select></div>
<div class="field"><label>Weeks per Year <em>or</em> Fixed Amount ($)</label><input id="policyVal" type="number" value="2" step="0.5" min="0"></div>
<div class="field"><label>Filing Status</label><select id="status"><option value="single">Single</option><option value="mfj">Married Filing Jointly</option><option value="hoh">Head of Household</option></select></div>
<div class="field"><label>Other Annual Income This Year ($)</label><input id="otherInc" type="number" value="0" step="1000" min="0" placeholder="salary already earned"></div>
    </div>
    <button class="btn-primary" onclick="calc()">Calculate Severance</button>
  </div>
  <div class="result-card" id="result">
    <h2>Severance Pay Estimate</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Gross Severance</div><div class="result-value" id="r-gross">—</div></div>
<div class="result-item"><div class="result-label">Severance Weeks</div><div class="result-value" id="r-weeks">—</div></div>
<div class="result-item"><div class="result-label">Federal Tax (22% supp.)</div><div class="result-value" id="r-fed" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">FICA (7.65%)</div><div class="result-value" id="r-fica" style="color:#dc2626">—</div></div>
<div class="result-item"><div class="result-label">Est. After-Tax Amount</div><div class="result-value" id="r-net">—</div></div>
<div class="result-item"><div class="result-label">Weekly Equivalent</div><div class="result-value" id="r-weekly">—</div></div>
    </div>
    <div style="margin-top:16px;padding:14px;background:#fff;border-radius:8px;font-size:13px;color:#475569;line-height:1.7" id="r-note"></div>
  </div>"""

SEV_SCRIPT = """<script>
function fmt(n){return'$'+Math.round(n).toLocaleString('en-US');}
function set(id,v){document.getElementById(id).textContent=v;}
function calc(){
  const salary=parseFloat(document.getElementById('salary').value)||0;
  const years=parseFloat(document.getElementById('years').value)||0;
  const policy=document.getElementById('policy').value;
  const pVal=parseFloat(document.getElementById('policyVal').value)||0;
  const status=document.getElementById('status').value;
  const otherInc=parseFloat(document.getElementById('otherInc').value)||0;

  const weeklyPay=salary/52;
  let sevWeeks=0, sevGross=0;
  if(policy==='weeks'){sevWeeks=years*pVal; sevGross=weeklyPay*sevWeeks;}
  else{sevGross=pVal; sevWeeks=salary>0?sevGross/weeklyPay:0;}

  // IRS supplemental wage flat rate 22% for federal withholding on severance
  const fedTax=sevGross*0.22;
  // FICA: SS 6.2% up to $176,100 combined; Medicare 1.45%
  const totalWages=otherInc+sevGross;
  const ssBase=Math.max(0,Math.min(totalWages,176100)-Math.min(otherInc,176100));
  const fica=ssBase*0.062+sevGross*0.0145;
  const net=sevGross-fedTax-fica;

  set('r-gross',fmt(sevGross));
  set('r-weeks',sevWeeks.toFixed(1)+' wks');
  set('r-fed',fmt(fedTax));
  set('r-fica',fmt(fica));
  set('r-net',fmt(net));
  set('r-weekly',fmt(weeklyPay));

  const months=(sevWeeks/4.33).toFixed(1);
  const stdStatuses={single:'$15,000',mfj:'$30,000',hoh:'$22,500'};
  document.getElementById('r-note').innerHTML=
    '<strong>Unemployment eligibility:</strong> Receiving severance may delay or reduce unemployment benefits in many states — check your state\'s rules.<br>'+
    '<strong>Tax note:</strong> The 22% supplemental federal rate is a withholding estimate. Your final tax will be calculated on your full-year income ('+
    stdStatuses[status]+' standard deduction). You may owe more or receive a refund at filing.<br>'+
    '<strong>Severance covers ~'+months+' months</strong> of living expenses at your current salary level.';
  document.getElementById('result').classList.add('show');
}
</script>"""

# ── W-2 CALCULATOR ─────────────────────────────────────────────────────────
W2_FORM = """  <div class="form-card">
    <h2>Enter Your W-2 Box Values</h2>
    <div class="form-grid">
<div class="field"><label>Box 1 — Wages, Tips (Federal Taxable)</label><input id="box1" type="number" value="65000" step="100" min="0"></div>
<div class="field"><label>Box 2 — Federal Income Tax Withheld</label><input id="box2" type="number" value="8500" step="100" min="0"></div>
<div class="field"><label>Box 3 — Social Security Wages</label><input id="box3" type="number" value="68000" step="100" min="0"></div>
<div class="field"><label>Box 4 — SS Tax Withheld</label><input id="box4" type="number" value="4216" step="10" min="0"></div>
<div class="field"><label>Box 5 — Medicare Wages</label><input id="box5" type="number" value="68000" step="100" min="0"></div>
<div class="field"><label>Box 6 — Medicare Tax Withheld</label><input id="box6" type="number" value="986" step="10" min="0"></div>
<div class="field"><label>Box 17 — State Income Tax Withheld</label><input id="box17" type="number" value="3200" step="100" min="0"></div>
<div class="field"><label>Filing Status</label><select id="status"><option value="single">Single</option><option value="mfj">Married Filing Jointly</option><option value="mfs">Married Filing Separately</option><option value="hoh">Head of Household</option></select></div>
    </div>
    <button class="btn-primary" onclick="calc()">Check W-2 &amp; Estimate Refund</button>
  </div>
  <div class="result-card" id="result">
    <h2>W-2 Analysis (2026 Tax Year)</h2>
    <div class="result-grid">
<div class="result-item"><div class="result-label">Taxable Income (after std. ded.)</div><div class="result-value" id="r-taxable">—</div></div>
<div class="result-item"><div class="result-label">2026 Federal Tax Owed</div><div class="result-value" id="r-owed">—</div></div>
<div class="result-item"><div class="result-label">Already Withheld (Box 2)</div><div class="result-value" id="r-withheld">—</div></div>
<div class="result-item"><div class="result-label" id="refund-label">—</div><div class="result-value" id="r-refund">—</div></div>
<div class="result-item"><div class="result-label">SS Withheld Check</div><div class="result-value" id="r-ss-check">—</div></div>
<div class="result-item"><div class="result-label">Medicare Withheld Check</div><div class="result-value" id="r-med-check">—</div></div>
    </div>
    <div style="margin-top:16px;padding:14px;background:#fff;border-radius:8px;font-size:13px;color:#475569;line-height:1.7" id="r-note"></div>
  </div>"""

W2_SCRIPT = """<script>
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
  return{tax,taxable};
}
function fmt(n){return'$'+Math.round(Math.abs(n)).toLocaleString('en-US');}
function set(id,v){document.getElementById(id).textContent=v;}
function calc(){
  const box1=parseFloat(document.getElementById('box1').value)||0;
  const box2=parseFloat(document.getElementById('box2').value)||0;
  const box3=parseFloat(document.getElementById('box3').value)||0;
  const box4=parseFloat(document.getElementById('box4').value)||0;
  const box5=parseFloat(document.getElementById('box5').value)||0;
  const box6=parseFloat(document.getElementById('box6').value)||0;
  const box17=parseFloat(document.getElementById('box17').value)||0;
  const status=document.getElementById('status').value;

  const {tax:fedOwed,taxable}=calcFedTax(box1,status);
  const diff=box2-fedOwed;
  const isRefund=diff>=0;

  // FICA checks
  const ssExpected=Math.min(box3,176100)*0.062;
  const medExpected=box5*0.0145+(box5>200000?(box5-200000)*0.009:0);
  const ssDiff=box4-ssExpected;
  const medDiff=box6-medExpected;

  set('r-taxable','$'+Math.round(taxable).toLocaleString('en-US'));
  set('r-owed',fmt(fedOwed));
  set('r-withheld',fmt(box2));
  document.getElementById('refund-label').textContent=isRefund?'Estimated Refund':'Additional Tax Owed';
  const refundEl=document.getElementById('r-refund');
  refundEl.textContent=(isRefund?'+':'-')+fmt(diff);
  refundEl.style.color=isRefund?'#16a34a':'#dc2626';

  const ssOk=Math.abs(ssDiff)<2;
  const medOk=Math.abs(medDiff)<2;
  set('r-ss-check',ssOk?'✓ Correct ('+fmt(box4)+')':'⚠ Expected '+fmt(ssExpected)+', got '+fmt(box4));
  document.getElementById('r-ss-check').style.color=ssOk?'#16a34a':'#d97706';
  set('r-med-check',medOk?'✓ Correct ('+fmt(box6)+')':'⚠ Expected '+fmt(medExpected)+', got '+fmt(box6));
  document.getElementById('r-med-check').style.color=medOk?'#16a34a':'#d97706';

  const notes=[];
  if(!isRefund)notes.push('<strong>You may owe '+fmt(diff)+' at filing</strong> — consider adjusting your W-4 withholding.');
  if(Math.abs(ssDiff)>=2)notes.push('SS discrepancy of '+fmt(ssDiff)+' detected — verify Box 3 & 4 with your employer.');
  if(Math.abs(medDiff)>=2)notes.push('Medicare discrepancy of '+fmt(medDiff)+' detected — verify Box 5 & 6.');
  if(box5>200000)notes.push('Box 5 exceeds $200,000 — Additional Medicare Tax (0.9%) applies to wages over $200k.');
  if(notes.length===0)notes.push('Your W-2 looks accurate. File by April 15, 2027 for tax year 2026.');
  document.getElementById('r-note').innerHTML=notes.join('<br>');
  document.getElementById('result').classList.add('show');
}
</script>"""

TOOLS = [
    ("tools/severance-pay-calculator.html", SEV_FORM, SEV_SCRIPT),
    ("tools/w2-calculator.html",            W2_FORM,  W2_SCRIPT),
]

print("=== Rewriting P3 tools ===")
changed=0
for path,new_form,new_script in TOOLS:
    with open(path,"r",encoding="utf-8") as f: c=f.read()
    fo=OLD_FORM in c; so=OLD_SCRIPT in c
    if fo: c=c.replace(OLD_FORM,new_form,1)
    if so: c=c.replace(OLD_SCRIPT,new_script,1)
    if fo or so:
        with open(path,"w",encoding="utf-8") as f: f.write(c)
        changed+=1
        print(f"  {path}: form={fo} script={so}")
    else:
        print(f"  {path}: NO MATCH")
print(f"Files changed: {changed}/2")
