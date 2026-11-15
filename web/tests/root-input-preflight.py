#!/usr/bin/env python3
"""Read-only inventory. Acceptance here is root-only input scope, not native validation."""
import argparse,hashlib,json,math,pathlib
p=argparse.ArgumentParser();p.add_argument('savedir',type=pathlib.Path);a=p.parse_args()
paths=['natural60-day30.json','natural60-day60.json','grazing-coupled/arm-0-day90.json']+[f'retention-coupled/arm-{i}.json' for i in range(6)]
def count_field(items,key):
 vals=[x[key] for x in items if key in x]; nums=[v for v in vals if isinstance(v,(int,float)) and not isinstance(v,bool)]
 return dict(present=len(vals),absent=len(items)-len(vals),explicit_zero=sum(v==0 for v in vals),nonzero=sum(v!=0 for v in vals),nonfinite=sum(not math.isfinite(v) for v in nums),sum=math.fsum(nums),minimum=min(nums,default=None),maximum=max(nums,default=None))
rows=[]
for name in paths:
 raw=(a.savedir/name).read_bytes();d=json.loads(raw);o=d['origin'];cells=o['cells'];co=[];occupied=0;duplicates=0
 for c in cells:
  if c.get('sparse') is not None:
   entries=c['sparse'];indices=[x['index'] for x in entries];duplicates+=len(indices)-len(set(indices));vals=[x['value'] for x in entries]
  else: vals=c.get('cohorts',[])
  co+=vals;occupied+=any(x.get('biomass',0)>0 for x in vals)
 known_co={'biomass','organization','support_mass','optimum','efficiency','structure','feeding','mobility','relocations','last_from','last_to','last_move_time','lifetime_grazed','generation','lineage','parent','reproduction_credit'}
 extra_co=sorted(set().union(*(set(c) for c in co))-known_co)
 extra_cell=sorted(set().union(*(set(c) for c in cells))-{'cohorts','sparse','nutrient','detritus','rng'})
 reasons=[]
 if (d.get('version'),o.get('model_revision'))!=(6,5):reasons.append('unsupported schema/model identity; no field-dropping migration')
 if d.get('mode')!='origin':reasons.append('not Origin')
 if extra_co or extra_cell or 'retention_mutation' in o:reasons.append('experimental cohort/cell/config fields present')
 rows.append(dict(path=name,sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),version=d.get('version'),model_revision=o.get('model_revision'),mode=d.get('mode'),encoding=o.get('cohort_encoding'),game_time=d['game_time'],days=d['game_time']/86400,cells=len(cells),serialized_cohorts=len(co),living=sum(x.get('biomass',0)>0 for x in co),occupied=occupied,duplicate_sparse_indices=duplicates,cohort_fields=sorted(set().union(*(set(c) for c in co))),extra_cohort_fields=extra_co,extra_cell_fields=extra_cell,origin_keys=sorted(o),retention_mutation_present='retention_mutation'in o,retention_mutation=o.get('retention_mutation'),cohort_inventory={k:count_field(co,k) for k in ['biomass','support_mass','root_fraction','retention_allocation','stored_water']},cell_inventory={k:count_field(cells,k) for k in ['nutrient','detritus','soil_water','liquid_return','vapor_return']},physical_inventory={k:count_field([{'x':v} for v in d[k]],'x') for k in ['water','vapor']},accepted_input_scope=not reasons,reasons=reasons))
print(json.dumps(rows,indent=2,allow_nan=False))
