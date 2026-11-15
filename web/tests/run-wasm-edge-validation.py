from pathlib import Path
import json,subprocess,hashlib,re,statistics,datetime
r=Path(__file__).resolve().parents[2];base=r.parent/'site-tmp/wasm-planet-profile';out=r.parent/'site-tmp/wasm-edge-validation';original=json.loads((base/'results.json').read_text());inputs={int(d):r.parent/v['path'] for d,v in original['inputs'].items()}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def execute(day,kind,stages,label):
 binary=(base if kind=='baseline' else out)/('stages' if stages else 'plain')/'profile.js';dest=out/(label+'.json');log=out/(label+'.log')
 with log.open('w')as f:p=subprocess.run(['node',str(binary),str(inputs[day]),str(base/'graph.json'),str(dest),'60'],cwd=r,stdout=f,stderr=subprocess.STDOUT)
 assert p.returncode==0,(label,p.returncode)
 assert sha(dest)==original['integrity'][f'wasm-{day}-60'],(label,'complete output differs')
 s=log.read_text();line=next(x for x in s.splitlines() if x.startswith('WASM_PLANET'));row={k:float(v)for k,v in re.findall(r'(\w+)=([\d.e+\-]+)',line)};first=next(x for x in s.splitlines()if x.startswith('FIRST_TICK'));row['first_ms']=float(re.search(r'ms=([\d.e+\-]+)',first)[1]);row['remaining_per_tick_ms']=(row['total_ms']-row['first_ms'])/59;row.update(day=day,kind=kind,stage_instrumented=stages,output_sha256=sha(dest))
 if stages:
  arr=lambda x:[float(v.strip())for v in x.split(',')];firstsub=arr(re.search(r'sub=\{([^}]+)',first)[1]);allsub=arr(re.search(r'ATMOSPHERE_SUBSTAGES ms=\{([^}]+)',s)[1]);row['remaining_substages_ms']=[(a-b)/59 for a,b in zip(allsub,firstsub)]
 return row
# Correctness and subphase observations precede uninstrumented fixed pair window.
gates=[execute(day,'candidate',True,f'gate-stage-{day}')for day in inputs]
print('ALL_COMPLETE_OUTPUT_GATES_PASS',flush=True)
records=[];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
for day in inputs:
 for rep in range(3):
  for kind in (['baseline','candidate']if rep%2==0 else ['candidate','baseline']):
   row=execute(day,kind,False,f'timing-{day}-{rep}-{kind}');row['repeat']=rep;records.append(row);print(json.dumps(row),flush=True)
summary={}
for day in inputs:
 med={kind:statistics.median(x['remaining_per_tick_ms']for x in records if x['day']==day and x['kind']==kind)for kind in ['baseline','candidate']}
 pairs=[]
 for rep in range(3):
  p={x['kind']:x['remaining_per_tick_ms']for x in records if x['day']==day and x['repeat']==rep};pairs.append(100*(p['candidate']/p['baseline']-1))
 summary[day]={'remaining_medians_ms':med,'median_change_percent':100*(med['candidate']/med['baseline']-1),'paired_change_percent':pairs}
result={'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'gates':gates,'records':records,'summary':summary};(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(summary,indent=2),flush=True)
