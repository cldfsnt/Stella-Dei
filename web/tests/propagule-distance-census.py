#!/usr/bin/env python3
"""Exact graph counts and integer six-slot walk multiplicity; no simulation changes."""
import json,sys,math,collections,gzip,hashlib
from pathlib import Path
path=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
with path.open() as f:meta=json.loads(next(f));cells=[json.loads(s) for s in f]
assert len(cells)==meta['cells'];assert all(c['cell']==i and len(c['neighbors'])==6 for i,c in enumerate(cells))
for i,c in enumerate(cells):
 for n in c['neighbors']:assert 0<=n<len(cells) and i in cells[n]['neighbors']
occupied=[c['cell'] for c in cells if c['biomass']>0]
sources=collections.defaultdict(list);ready=[]
for c in cells:
 for co in c['cohorts']:
  if co['biomass']>=.02:
   sources[c['cell']].append(co['lineage'])
   if co['reproduction_credit']>=.01:ready.append({'cell':c['cell'],'id':co['lineage']})
def bfs(source,maxd=8):
 d={source:0};q=collections.deque([source])
 while q:
  i=q.popleft()
  if d[i]>=maxd:continue
  for n in cells[i]['neighbors']:
   if n not in d:d[n]=d[i]+1;q.append(n)
 return d
def categories(weights):
 r=collections.Counter();nut=0.;minimum=None;maximum=None
 for i,w in weights.items():
  c=cells[i];r['total']+=w;r['habitable' if c['habitable'] else 'harsh']+=w
  alive=sum(x['biomass']>0 for x in c['cohorts']);r['occupied' if alive else 'empty']+=w
  if c['habitable'] and not alive:r['empty_habitable']+=w
  if alive<4 and c['biomass']<=.99:r['slot_and_mass_capacity']+=w
  n=c['nutrient'];nut+=n*w;minimum=n if minimum is None else min(minimum,n);maximum=n if maximum is None else max(maximum,n)
  r['nutrient_'+('zero' if n<=0 else 'to_1e-4' if n<=1e-4 else 'to_1e-3' if n<=1e-3 else 'to_1e-2' if n<=1e-2 else 'above_1e-2')]+=w
 return {**dict(r),'nutrient_mean':nut/r['total'] if r['total'] else None,'nutrient_min':minimum,'nutrient_max':maximum}
rows=[];targets=[]
for source,ids in sorted(sources.items()):
 distances=bfs(source);weights={source:1}
 for step in range(1,9):
  nxt=collections.Counter()
  for i,w in weights.items():
   for n in cells[i]['neighbors']:nxt[n]+=w
  weights=nxt;assert sum(weights.values())==6**step
  if step not in [1,2,4,8]:continue
  ball={i:1 for i,d in distances.items() if 0<d<=step};ring={i:1 for i,d in distances.items() if d==step};far={i:w for i,w in weights.items() if distances[i]>1}
  row={'source':source,'potential_donor_ids':ids,'hops':step,'ball':categories(ball),'ring':categories(ring),'walk_paths':categories(weights),'farther_than_one_walk_paths':categories(far),'return_paths':weights.get(source,0),'path_count':6**step,'distinct_endpoints':len(weights),'max_endpoint_paths':max(weights.values()),'effective_endpoints':(6**step)**2/sum(w*w for w in weights.values())}
  rows.append(row)
  for i,w in sorted(weights.items()):
   c=cells[i];p=cells[source]['point'];v=c['point'];dot=sum(a*b for a,b in zip(p,v))/math.sqrt(sum(a*a for a in p)*sum(b*b for b in v));km=meta['radius_km']*math.acos(max(-1,min(1,dot)))
   targets.append({'source':source,'hops':step,'target':i,'shortest_hops':distances[i],'paths':w,'great_circle_km':km,'habitable':c['habitable'],'depth_m':c['depth_m'],'temperature':c['temperature'],'nutrient':c['nutrient'],'biomass':c['biomass'],'living_slots':sum(x['biomass']>0 for x in c['cohorts'])})
union={}
for h in [1,2,4,8]:
 ends=collections.Counter()
 for source in occupied:
  for i,d in bfs(source).items():
   if 0<d<=h:ends[i]+=1
 union[h]={'unique_targets':categories({i:1 for i in ends}),'source_target_incidence':categories(ends),'max_sources_sharing_target':max(ends.values())}
summary={'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'metadata':meta,'currently_funded_ready':ready,'mass_qualified_cohorts':sum(map(len,sources.values())),'mass_qualified_source_patches':len(sources),'occupied_source_patches':len(occupied),'pentagon_self_slots':sum(c['neighbors'].count(c['cell']) for c in cells),'source_rows':rows,'occupied_union':union}
(out/'census.json').write_text(json.dumps(summary,indent=2)+'\n');(out/'all-targets.json.gz').write_bytes(gzip.compress(json.dumps(targets,separators=(',',':')).encode(),mtime=0))
for h in [1,2,4,8]:
 r=[x for x in rows if x['hops']==h];total=sum(x['path_count'] for x in r);print(h,'sources',len(r),'mean unique empty habitable',sum(x['ball'].get('empty_habitable',0) for x in r)/len(r),'walk empty habitable probability',sum(x['walk_paths'].get('empty_habitable',0) for x in r)/total,'far empty habitable probability',sum(x['farther_than_one_walk_paths'].get('empty_habitable',0) for x in r)/total,'return',sum(x['return_paths'] for x in r)/total,'occupied union empty habitable',union[h]['unique_targets'].get('empty_habitable',0))
print('PASS exact path totals, reciprocal native adjacency, all endpoints retained; ready',len(ready))
