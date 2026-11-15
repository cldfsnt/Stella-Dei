from pathlib import Path
import json,subprocess,hashlib,re,statistics,datetime,math
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp';o=b/'liquid-gather-wasm';base=b/'wasm-planet-profile';controls=json.loads((o/'controls.json').read_text());original=json.loads((base/'results.json').read_text());h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Caller must have accepted all independent numerical audits before starting this fixed window.
records=[];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
for day in [30,60,90]:
 input=r.parent/original['inputs'][str(day)]['path']
 for rep in range(3):
  for kind in (['baseline','candidate']if rep%2==0 else ['candidate','baseline']):
   binary=base/'plain/profile.js'if kind=='baseline'else o/'candidate/profile.js';label=f'timing-{day}-{rep}-{kind}';dest=o/(label+'.json');log=o/(label+'.log')
   with log.open('w')as f:p=subprocess.run(['node',str(binary),str(input),str(base/'graph.json'),str(dest),'60'],cwd=r,stdout=f,stderr=subprocess.STDOUT)
   assert p.returncode==0,(label,p.returncode)
   expected=controls['worlds'][str(day)]['baseline60_sha256'if kind=='baseline'else'candidate60_sha256'];assert h(dest)==expected,(label,'same-law output mismatch')
   s=log.read_text();line=next(x for x in s.splitlines()if x.startswith('WASM_PLANET'));row={k:float(v)for k,v in re.findall(r'(\w+)=([\d.e+\-]+)',line)};first=next(x for x in s.splitlines()if x.startswith('FIRST_TICK'));row['first_ms']=float(re.search(r'ms=([\d.e+\-]+)',first)[1]);row['remaining_per_tick_ms']=(row['total_ms']-row['first_ms'])/59;row.update(day=day,repeat=rep,kind=kind,output_sha256=h(dest));records.append(row);print(json.dumps(row),flush=True)
summary={};ratios=[]
for day in [30,60,90]:
 med={kind:statistics.median(x['remaining_per_tick_ms']for x in records if x['day']==day and x['kind']==kind)for kind in ['baseline','candidate']};ratio=med['candidate']/med['baseline'];ratios.append(ratio)
 pairs=[]
 for rep in range(3):
  d={x['kind']:x['remaining_per_tick_ms']for x in records if x['day']==day and x['repeat']==rep};pairs.append(d['candidate']/d['baseline'])
 summary[day]={'remaining_medians_ms':med,'median_ratio':ratio,'within_5_percent':ratio<=1.05,'paired_ratios':pairs}
geometric=math.exp(sum(math.log(x)for x in ratios)/3);passed=all(x<=1.05 for x in ratios)and geometric<=1.03
result={'started_utc':start,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'records':records,'summary':summary,'geometric_ratio':geometric,'performance_pass':passed};(o/'timing-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'summary':summary,'geometric_ratio':geometric,'performance_pass':passed},indent=2),flush=True)
