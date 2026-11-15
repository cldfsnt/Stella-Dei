"""Read-only retrospective analysis of frozen actual full-scheduler checkpoints."""
import json,hashlib,math,itertools,pathlib,sys
base=pathlib.Path(sys.argv[1]); out=pathlib.Path(sys.argv[2]); worlds={}; ids={}; result={'scope':'One natural world, observational checkpoints; no causal trait isolation or unobserved descendant reconstruction','inputs':{},'checkpoints':[],'all_day30_structure_pairs':[]}
for d in [30,40,50,60]:
 path=base/f'natural60-day{d}.json';raw=path.read_bytes();p=json.loads(raw);worlds[d]=p;result['inputs'][str(d)]=hashlib.sha256(raw).hexdigest(); cells=p['origin']['cells']; ids[d]={x['value']['lineage']:(i,x['value']) for i,c in enumerate(cells) for x in c['sparse'] if x['value']['biomass']>0};area=4*math.pi*(p['radius']*1000)**2/len(cells);depth=lambda i:p['water'][i]*1e6/area
 occupied=[(i,c) for i,c in enumerate(cells) if c['sparse']]; co=list(ids[d].values());m=sum(x['biomass'] for i,x in co)
 result['checkpoints'].append({'day':d,'colonies':len(co),'patches':len(occupied),'full4slot_patches':sum(len(c['sparse'])==4 for i,c in occupied),'biomass_sum':m,'nutrient_sum_occupied':sum(c['nutrient'] for i,c in occupied),'nutrient_under_0_001_patches':sum(c['nutrient']<.001 for i,c in occupied),'mass_atleast_0_02':sum(x['biomass']>=.02 for i,x in co),'credit_atleast_0_01':sum(x['reproduction_credit']>=.01 for i,x in co),'both_propagation_gates':sum(x['biomass']>=.02 and x['reproduction_credit']>=.01 for i,x in co),'biomass_capacity_over_0_99_patches':sum(sum(x['value']['biomass'] for x in c['sparse'])>.99 for i,c in occupied),'protected_support_and_structure':sum(x['support_mass']>0 and x['structure']>0 for i,x in co),'occupied_depth_minmax_m':[min(depth(i) for i,c in occupied),max(depth(i) for i,c in occupied)],'stats':p['origin'].get('stats',{})})
for i,c in enumerate(worlds[30]['origin']['cells']):
 for a,b in itertools.combinations([x['value'] for x in c['sparse']],2):
  if a['structure']==b['structure']:continue
  a,b=sorted([a,b],key=lambda x:x['structure']); row={'start_cell':i,'lower_structure_id':a['lineage'],'higher_structure_id':b['lineage'],'baseline_traits':[{k:x[k] for k in ['lineage','structure','organization','support_mass','efficiency','feeding','mobility','optimum','biomass']} for x in [a,b]],'outcomes':[]}
  for d in [30,40,50,60]:
   row['outcomes'].append({'day':d,'originals':[{'id':x['lineage'],'present':x['lineage'] in ids[d],'cell':ids[d][x['lineage']][0] if x['lineage'] in ids[d] else None,'biomass':ids[d][x['lineage']][1]['biomass'] if x['lineage'] in ids[d] else 0} for x in [a,b]]})
  result['all_day30_structure_pairs'].append(row)
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps([{k:v for k,v in c.items() if k!='stats'} for c in result['checkpoints']],indent=2));print('pairs',len(result['all_day30_structure_pairs']))
