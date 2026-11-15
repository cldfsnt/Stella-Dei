from pathlib import Path
import json,math,sys
b=Path(sys.argv[1]);g=json.loads((b/'ordinary-geometry.json').read_text());v=[p['data']for p in g];n=[math.sqrt(sum(t*t for t in p))for p in v]
def distance(i,j):return 5000*math.acos(max(-1,min(1,sum(a*c for a,c in zip(v[i],v[j]))/n[i]/n[j])))
output={}
for arm in ['ordinary','pioneer']:
 founders={};prev={};cur={};births=[];packets=[]
 for line in (b/(arm+'.log')).open():
  if not line.startswith(('FOUNDER ','COHORT ','TICK_START ','TICK ','WIND_PACKET ')):continue
  tag,raw=line.split(' ',1);r=json.loads(raw)
  if tag=='FOUNDER' and r['success']:
   for c in r['after']['cohorts']:
    if c['biomass']>0:founders[c['lineage']]=r['cell'];prev[c['lineage']]={'cell':r['cell'],'cohort':c}
  elif tag=='TICK_START':cur={}
  elif tag=='COHORT':cur[r['cohort']['lineage']]=r
  elif tag=='WIND_PACKET':packets.append(r)
  elif tag=='TICK':
   for i in cur.keys()-prev.keys():
    c=cur[i]['cohort'];p=cur.get(c['parent'],prev.get(c['parent']));births.append({'id':i,'cell':cur[i]['cell'],'parent_cell':p['cell'],'distance':distance(p['cell'],cur[i]['cell'])})
   prev=cur
 ids={r['receipt']['lineage']for r in packets if r['receipt']['arrived']};local=[r for r in births if r['id']not in ids];cells={c['cell']for c in cur.values()};initial=set(founders.values());new=cells-initial
 output[arm]={'final_new_occupied':len(new),'initial_occupied_lost':len(initial-cells),'max_distance_final_new_to_nearest_initial_km':max((min(distance(i,j)for j in initial)for i in new),default=0),'same_patch_nonwind_births':sum(c['cell']==c['parent_cell']for c in local),'different_patch_nonwind_births':sum(c['cell']!=c['parent_cell']for c in local),'max_nonwind_birth_distance_km':max((c['distance']for c in local),default=0),'wind_parent_ids':sorted({r['parent']for r in packets}),'wind_onehop_arrivals':sum(r['route']['hops']==1 and r['receipt']['arrived']for r in packets),'wind_multihop_arrivals':sum(r['route']['hops']>1 and r['receipt']['arrived']for r in packets)}
print(json.dumps(output,indent=2))
