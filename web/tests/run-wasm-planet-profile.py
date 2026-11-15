from pathlib import Path
import subprocess,json,re,hashlib,statistics,datetime
r=Path(__file__).resolve().parents[2];o=r.parent/'site-tmp/wasm-planet-profile'
inputs={d:r.parent/'site-tmp'/ (f'natural60-day{d}.json' if d!=90 else 'grazing-coupled/arm-0-day90.json') for d in [30,60,90]}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def execute(mode,day,ticks,label):
 dest=o/(label+'.json');log=o/(label+'.log');cmd=([str(o/'native/profile')] if mode=='native' else ['node',str(o/mode/'profile.js')])+[str(inputs[day]),str(o/'graph.json'),str(dest),str(ticks)]
 with log.open('w') as f:p=subprocess.run(cmd,cwd=r,stdout=f,stderr=subprocess.STDOUT)
 assert p.returncode==0,(label,p.returncode)
 return dest,log
proof={}
for day in inputs:
 z,_=execute('plain',day,0,f'gate-zero-{day}');assert json.loads(z.read_text())==json.loads(inputs[day].read_text())
 for ticks in [1,60]:
  a,_=execute('plain',day,ticks,f'gate-plain-{day}-{ticks}');b,_=execute('stages',day,ticks,f'gate-stages-{day}-{ticks}');assert a.read_bytes()==b.read_bytes(),(day,ticks,'instrumentation')
  proof[f'wasm-{day}-{ticks}']=sha(a)
 a,_=execute('native',day,60,f'gate-native-{day}-60');old=r.parent/f'site-tmp/water-stage-production/day{day}/endpoint.json'
 x=json.loads(a.read_text());y=json.loads(old.read_text());diff=[k for k in x if x[k]!=y[k]]
 proof[f'native-{day}']={'equal_EGL_complete_save':not diff,'different_fields':diff,'new_sha256':sha(a),'prior_sha256':sha(old)}
 assert not diff,(day,'headless-vs-EGL',diff)
(o/'integrity.json').write_text(json.dumps(proof,indent=2)+'\n');print('ALL_INTEGRITY_GATES_PASS',flush=True)
records=[];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
for day in inputs:
 for rep in range(3):
  for mode in (['plain','stages'] if rep%2==0 else ['stages','plain']):
   dest,log=execute(mode,day,60,f'timing-{day}-{rep}-{mode}');assert sha(dest)==proof[f'wasm-{day}-60']
   s=log.read_text();line=next(x for x in s.splitlines() if x.startswith('WASM_PLANET'))
   row={k:float(v) for k,v in re.findall(r'(\w+)=([\d.e+\-]+)',line)}
   first=next(x for x in s.splitlines() if x.startswith('FIRST_TICK'))
   row['first_ms']=float(re.search(r'ms=([\d.e+\-]+)',first)[1]);row['remaining_per_tick_ms']=(row['total_ms']-row['first_ms'])/59
   array=lambda t:[float(v.strip()) for v in t.split(',')]
   row['first_stages_ms']=array(re.search(r'stages=\{([^}]+)',first)[1]);row['first_atmosphere_ms']=array(re.search(r'sub=\{([^}]+)',first)[1]);row['atmosphere_substages_ms']=array(re.search(r'ATMOSPHERE_SUBSTAGES ms=\{([^}]+)',s)[1])
   row.update(day=day,repeat=rep,mode=mode,output_sha256=sha(dest));records.append(row);print(json.dumps(row),flush=True)
summary={}
for day in inputs:
 summary[day]={}
 for mode in ['plain','stages']:
  rows=[x for x in records if x['day']==day and x['mode']==mode]
  summary[day][mode]={'median_per_tick_ms':statistics.median(x['total_ms']/60 for x in rows),'median_first_ms':statistics.median(x['first_ms'] for x in rows),'median_remaining_ms':statistics.median(x['remaining_per_tick_ms'] for x in rows),'remaining_range_ms':[min(x['remaining_per_tick_ms'] for x in rows),max(x['remaining_per_tick_ms'] for x in rows)]}
  if mode=='stages':
   names=['temperature_ms','liquid_wind_ms','atmosphere_ms','ecology_ms'];summary[day][mode]['remaining_stage_medians_ms']={name:statistics.median((x[name]-x['first_stages_ms'][i])/59 for x in rows) for i,name in enumerate(names)}
   names=['wind_cache','edge_cache','phase','coefficient','gather'];summary[day][mode]['remaining_atmosphere_medians_ms']={name:statistics.median((x['atmosphere_substages_ms'][i]-x['first_atmosphere_ms'][i])/59 for x in rows) for i,name in enumerate(names)}
 summary[day]['instrumentation_percent']=100*(summary[day]['stages']['median_per_tick_ms']/summary[day]['plain']['median_per_tick_ms']-1)
result={'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'records':records,'summary':summary,'inputs':{str(d):{'path':str(p.relative_to(r.parent)),'sha256':sha(p)}for d,p in inputs.items()},'graph_sha256':sha(o/'graph.json'),'integrity':proof}
(o/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(summary,indent=2),flush=True)
