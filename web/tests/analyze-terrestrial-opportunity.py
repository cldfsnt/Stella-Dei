"""Fixed all-world read-only habitat/phenotype census; no simulation or site edits."""
from pathlib import Path
import json,math,hashlib,numpy as np
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp';out=r/'web/tests/continuation-review/paid-hydration/soil-root-design/terrestrial-opportunity'
paths={'day30':b/'natural60-day30.json','day60':b/'natural60-day60.json','day90':b/'grazing-coupled/arm-0-day90.json'}
gpath=b/'propagule-graph/graph.jsonl';graph={};meta=None
for line in gpath.open():
 q=json.loads(line)
 if q['kind']=='metadata':meta=q
 else:graph[q['cell']]=sorted(set(q['neighbors'])-{q['cell']})
A=meta['area_m2'];summaries=[];sets={};provenance={'graph_sha256':hashlib.sha256(gpath.read_bytes()).hexdigest(),'inputs':{}}
def stats(xs):return {'count':len(xs),'min':min(xs)if xs else None,'max':max(xs)if xs else None,'mean':sum(xs)/len(xs)if xs else None}
def height(c):
 f=np.float32;frond=f(max(0,f(c['biomass'])-f(c['support_mass'])));slender=f(f(1)+f(f(.6)*f(f(1)-f(c['efficiency'])))-f(f(.3)*f(c['structure'])));return float(min(f(.5),f(f(f(.2)*f(c['support_mass']))/f(frond+f(.01)))*slender))
for label,path in paths.items():
 s=json.loads(path.read_text());n=len(s['water']);assert n==len(graph)==meta['cells'] and s['radius']==meta['radius_km'] and s['subdivisions']==6
 provenance['inputs'][label]={'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'schema':s['version'],'model':s['origin']['model_revision']}
 depth=[w*1e9/A/1000 for w in s['water']];warm={i for i,t in enumerate(s['temperature'])if 273.15<t<355};dry={i for i,d in enumerate(depth)if d==0};shallow={i for i,d in enumerate(depth)if 0<d<.2};hab={i for i,d in enumerate(depth)if .2<=d<=50 and 260<s['temperature'][i]<355};occupied=set();live=[]
 bins={k:{'cells':0,'warm':0,'rain_positive':0,'nutrient_sum':0.}for k in ['dry','positive_under20cm','20cm_to50m','over50m']}
 for i,cell in enumerate(s['origin']['cells']):
  d=depth[i];k='dry'if d==0 else'positive_under20cm'if d<.2 else'20cm_to50m'if d<=50 else'over50m';bins[k]['cells']+=1;bins[k]['warm']+=i in warm;bins[k]['rain_positive']+=s['rainfall'][i]>0;bins[k]['nutrient_sum']+=cell['nutrient']
  for entry in cell['sparse']:
   c=entry['value']
   if c['biomass']<=0:continue
   occupied.add(i);h=height(c);live.append({'cell':i,'id':c['lineage'],'parent':c['parent'],'generation':c['generation'],'biomass':c['biomass'],'support':c['support_mass'],'height_m':h,'depth_m':d,'warm':i in warm,'exposed':h>d,'dry':d==0,'organization':c['organization'],'feeding':c['feeding'],'mobility':c['mobility'],'structure':c['structure']})
 exposed=[x for x in live if x['exposed']];adjacent=set().union(*(set(graph[i])for i in occupied))if occupied else set();fixed=12352
 source_head32=float(np.float32(np.float32(s['elevation'][fixed])+np.float32(depth[fixed]/1000)));drained_head32=float(np.float32(np.float32(s['elevation'][fixed])+np.float32(max(0,depth[fixed]-1)/1000)))
 neighbors=[]
 for j in graph[fixed]:
  h32=float(np.float32(np.float32(s['elevation'][j])+np.float32(depth[j]/1000)));neighbors.append({'cell':j,'terrain_km':s['elevation'][j],'depth_m':depth[j],'head32_before_minus_source_m':(h32-source_head32)*1000,'head32_afterdrain_minus_source_m':(h32-drained_head32)*1000,'head64_afterdrain_minus_source_m':(s['elevation'][j]+depth[j]/1000-s['elevation'][fixed]-max(0,depth[fixed]-1)/1000)*1000})
 row={'label':label,'bins':bins,'living_colonies':len(live),'occupied_patches':len(occupied),'living':live,'living_depth':stats([x['depth_m']for x in live]),'living_height':stats([x['height_m']for x in live]),'living_exposed_count':len(exposed),'living_dry_count':sum(x['dry']for x in live),'warm_dry_cells':len(warm&dry),'warm_shallow_cells':len(warm&shallow),'aquatic_habitable_cells':len(hab),'occupied_adjacent_warm_dry':len(adjacent&warm&dry),'occupied_adjacent_warm_shallow':len(adjacent&warm&shallow),'warm_dry_rain_positive':sum(s['rainfall'][i]>0 for i in warm&dry),'warm_dry_rain':stats([s['rainfall'][i]for i in warm&dry]),'fixed_patch':{'cell':fixed,'terrain_km':s['elevation'][fixed],'depth_m':depth[fixed],'water_source_ulp_density':(s['water'][fixed]-float(np.nextafter(np.float32(s['water'][fixed]),np.float32(0))))*1e9/A,'native_head_quantum_m':float(np.nextafter(np.float32(s['elevation'][fixed]),np.float32(math.inf))-np.float32(s['elevation'][fixed]))*1000,'neighbors':neighbors}}
 summaries.append(row);sets[label]={'warm_dry':warm&dry,'warm_shallow':warm&shallow,'occupied':occupied}
intersection={key:sorted(set.intersection(*(v[key]for v in sets.values())))for key in ['warm_dry','warm_shallow','occupied']}
result={'worlds':summaries,'repeat_snapshot_intersections':{'counts':{k:len(v)for k,v in intersection.items()},'indices':intersection},'provenance':provenance,'caveat':'Snapshot intersections are not continuous exposure. Legacy soil absent; no assumed stored soilwater. Heads/height reconstructed with explicit f32 arithmetic, not extra scheduler run.'}
(out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
for x in summaries:print(x['label'],'bins',x['bins'],'live',x['living_colonies'],x['living_depth'],x['living_height'],'exposed',x['living_exposed_count'],'dry',x['warm_dry_cells'],'adjacentdry',x['occupied_adjacent_warm_dry'],'neighbors',x['fixed_patch']['neighbors'])
print('repeat intersections',result['repeat_snapshot_intersections']['counts'])
