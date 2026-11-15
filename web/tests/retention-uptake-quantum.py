from pathlib import Path
import json,struct,hashlib,sys
path=Path(sys.argv[1]);s=json.loads(path.read_text());rows=[];area=7669529600
for i,cell in enumerate(s['origin']['cells']):
 for item in cell.get('sparse',[]):
  c=item['value']
  if c.get('retention_allocation',0)<=0 or c['biomass']<=0:continue
  liquid=s['water'][i];bits=struct.unpack('<I',struct.pack('<f',liquid))[0];prior=struct.unpack('<f',struct.pack('<I',max(0,bits-1)))[0]
  quantum=(liquid-prior)*1e9/area;capacity=c['support_mass']*c['retention_allocation']*10
  rows.append({'id':c['lineage'],'patch':i,'liquid_1e9kg':liquid,'prior_f32_liquid_1e9kg':prior,'one_quantum_kg_per_m2':quantum,'capacity_kg_per_m2':capacity,'stored_kg_per_m2':c['stored_water'],'capacity_below_quantum':capacity<quantum,'paid_support':c['support_mass']})
print(json.dumps({'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'uniform_actual_area_m2':area,'endpoint_only_not_entire_trajectory_causality':True,'rows':rows},indent=2))
