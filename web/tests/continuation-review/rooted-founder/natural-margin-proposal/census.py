"""Read-only fixed whole-world census; no scheduler or model mutation."""
import json,struct,hashlib
from pathlib import Path
r=Path(__file__).resolve().parents[5];p=r.parent/'site-tmp/wetlands-day21/day-21.json';s=json.loads(p.read_text());f=lambda x:struct.unpack('f',struct.pack('f',x))[0]
# Actual existing native mean-area receipt, radius5000/subdivision6,40962points.
area=7669529600.;conversion=f(1000/area)
categories={k:[]for k in ['dry','0-20mm','20-200mm','200-500mm','500mm-50m']}
for i,(w,t,c,soil) in enumerate(zip(s['water'],s['temperature'],s['origin']['cells'],s['beta_origin']['soil'])):
 d=f(f(w*conversion)*1000);k='dry'if d==0 else '0-20mm'if d<=.02 else '20-200mm'if d<.2 else '200-500mm'if d<=.5 else '500mm-50m'if d<=50 else None
 if k:categories[k].append(dict(cell=i,depth_m=d,temperature=t,soil=soil,slots=len(c['sparse']),nutrient=c['nutrient']))
out={'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'area_m2':area,'conversion_km_per_native':conversion,'criteria':'293.15<=T<=313.15; empty sparse; soil>0; N>=.002; not a claim of full public eligibility or future climate','bins':{}}
for k,rows in categories.items():
 warm=[x for x in rows if 293.15<=x['temperature']<=313.15];eligible=[x for x in warm if x['slots']==0 and x['soil']>0 and x['nutrient']>=.002]
 out['bins'][k]={'all':len(rows),'warm':len(warm),'empty_soil_n':len(eligible),'candidates':eligible}
print(json.dumps(out,indent=2))
