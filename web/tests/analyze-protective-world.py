from pathlib import Path
import json,hashlib,gzip
r=Path(__file__).resolve().parents[2];e=r/'web/tests/continuation-review/protective-world';o=r.parent/'site-tmp/protective-world';summary={}
for mode in ['off','on']:
 for arm in [0,1]:
  lines=(e/f'{mode}-{arm}-main.log').read_text().splitlines();acts=[json.loads(l[9:]) for l in lines if l.startswith('ACTIVITY ')];patch=[json.loads(l[6:]) for l in lines if l.startswith('PATCH ')];used=[json.loads(l[7:]) for l in lines if l.startswith('USED_H ')];old={'inactive':False,'entries':0,'wakes':0};inactive=[]
  for tick,s in enumerate(acts,1):
   if old['inactive'] or s['entries']>old['entries']:
    inactive.append(tick)
    for x in used:
     if x['tick']==tick:assert x['credit']==0 and x['entry_demand']==0 and x['current_demand']==0,(mode,arm,tick,x)
    if tick>1:assert patch[tick-1]['cohorts'][0]['reproduction_credit']==patch[tick-2]['cohorts'][0]['reproduction_credit']
   old=s
  summary[f'{mode}-{arm}']={'final_C':patch[-1]['cohorts'][0]['biomass'],'final_credit':patch[-1]['cohorts'][0]['reproduction_credit'],'inactive_ticks':inactive,'state':acts[-1],'death':patch[-1]['cohorts'][0]['biomass']==0,'min_temperature':min(x['temperature'] for x in patch),'max_temperature':max(x['temperature'] for x in patch),'min_depth_m':min(x['depth_m'] for x in patch),'max_depth_m':max(x['depth_m'] for x in patch)}
  for tick in [0,30,60]:
   p=o/mode/f'arm-{arm}-{tick}.json';(e/f'{mode}-{arm}-{tick}.json.gz').write_bytes(gzip.compress(p.read_bytes(),mtime=0))
  for tick in [30,60]:
   p=o/mode/f'arm-{arm}-{tick}.json.activity.json';(e/f'{mode}-{arm}-{tick}.activity.json').write_bytes(p.read_bytes())
(e/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
for p in (o/'on/src').rglob('*.zig'):
 rel=p.relative_to(o/'on/src');old=r.parent/'site-tmp/rooted-natural/src'/rel
 if not old.exists() or p.read_bytes()!=old.read_bytes():(e/(str(rel).replace('/','-')+'.gz')).write_bytes(gzip.compress(p.read_bytes(),mtime=0))
