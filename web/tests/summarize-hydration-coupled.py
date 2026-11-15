from pathlib import Path
import json,sys
records=[]
for line in Path(sys.argv[1]).read_text().splitlines():
 if line.startswith('HYDRATION_COUPLED '):
  r=json.loads(line.split(' ',1)[1]);r['total_carbon_kg']=r['carbon_sum']*7669529600+r['co2_mass']*40962*1e9*(12/44);r['total_nutrient_kg']=r['nutrient_sum']*7669529600;records.append(r)
for arm in sorted({r['arm'] for r in records}):
 a=[r for r in records if r['arm']==arm];first=a[0]
 for r in a:
  r['carbon_residual_kg']=r['total_carbon_kg']-first['total_carbon_kg'];r['nutrient_residual_kg']=r['total_nutrient_kg']-first['total_nutrient_kg'];r['water_residual_including_removed_1e9kg']=r['water1e9kg']+r['external_removed1e9kg']-first['water1e9kg']
print(json.dumps({'units':'Actual frozen40k uniformarea7669529600m2,40962points; water billionkg, C/Nkg. Residuals include inherited hydrology/float error, no topup.','records':records},indent=2))
