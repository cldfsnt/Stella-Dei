"""Read-only actual endpoint diagnostics; prospective receipt probes are not extra ticks."""
from pathlib import Path
import json,hashlib,math,numpy as np
r=Path(__file__).resolve().parents[2];base=r.parent/'site-tmp/root-world-qa';out=r/'web/tests/continuation-review/paid-hydration/soil-root-design/root-world-analysis'
A=7669529600.0
rows=[];probes=[]
for label,arm in [('day30',1),('day60',1),('day60',2),('day60',3),('day90',1)]:
 p=base/f'{label}-arm-{arm}.json';s=json.loads(p.read_text());i=12352;co=[x['value'] for x in s['origin']['cells'][i]['sparse'] if x['value']['lineage']==478]
 row={'label':label,'arm':arm,'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'patch':i,'depth_m':s['water'][i]*1e9/A/1000,'temperature':s['temperature'][i],'soil':s['origin']['root_soil'][i],'root478':co}
 if co:
  c=co[0];canopy=c['support_mass']*(1-c['root_fraction']);height=min(.5,.2*canopy/(c['biomass']-c['support_mass']+.01)*(1+.6*(1-c['efficiency'])-.3*c['structure']))
  row.update(height_m_f64_reconstruction=height,exposure=max(0,min(1,(height-row['depth_m'])/height)) if height else 0)
 rows.append(row)
 if arm!=1:continue
 bins={k:{'count':0,'soil_sum':0.,'positive_soil':0,'warm':0,'prospective_request':0.,'prospective_source_debit':0.,'zero_source_receipts':0,'max_quantum_density':0.} for k in ['dry','0_to_20cm','20cm_to_2m','2_to_100m','over100m']}
 for liquid,soil,temp in zip(s['water'],s['origin']['root_soil'],s['temperature']):
  depth=liquid*1e9/A/1000;k='dry' if depth==0 else '0_to_20cm' if depth<.2 else '20cm_to_2m' if depth<2 else '2_to_100m' if depth<100 else 'over100m';b=bins[k];b['count']+=1;b['soil_sum']+=soil;b['positive_soil']+=soil>0
  q=(liquid-float(np.nextafter(np.float32(liquid),np.float32(0))))*1e9/A;b['max_quantum_density']=max(b['max_quantum_density'],q)
  if temp<=273.15:continue
  b['warm']+=1;L=liquid*1e9/A;factor=min(1,L+1-soil);wanted=min(L,1-soil,(1/60)*factor);native=wanted*A/1e9;after=float(np.float32(max(0,liquid-native)))
  if liquid-after>native:after=float(np.nextafter(np.float32(after),np.float32(liquid)))
  paid=(liquid-after)*1e9/A;b['prospective_request']+=wanted;b['prospective_source_debit']+=paid;b['zero_source_receipts']+=wanted>0 and paid==0
 for b in bins.values():b['prospective_delivery_ratio']=b['prospective_source_debit']/b['prospective_request'] if b['prospective_request'] else None
 probes.append({'label':label,'bins':bins})
records=json.loads((base/'enabled-records.json').read_text());summary={'root_patch_endpoints':rows,'endpoint_infiltration_probes':probes,'all_original_final_diagnostics':[x for x in records if x['tick']==60],'scope':'No simulation advanced. F64 reconstructed height and prospective native source-removal probes omit atmospheric phases and last-bit conservative conversion; not actual per-tick local logs. Actual cumulative roots remain zero.'}
(out/'analysis.json').write_text(json.dumps(summary,indent=2)+'\n')
for row in rows:print(row['label'],row['arm'],row['depth_m'],row['soil'],row.get('height_m_f64_reconstruction'),row.get('exposure'))
for p in probes:print(p['label'],[(k,v['prospective_delivery_ratio'],v['zero_source_receipts'],v['max_quantum_density'])for k,v in p['bins'].items()])
