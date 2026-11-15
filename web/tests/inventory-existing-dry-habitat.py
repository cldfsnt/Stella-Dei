#!/usr/bin/env python3
"""Read-only fixed archived climate inventory; approximate source-formula saturation."""
import json,math,struct,hashlib
from pathlib import Path
r=Path(__file__).resolve().parents[3];g=json.loads((r/'site-tmp/wasm-planet-profile/graph.json').read_text());f=lambda x:struct.unpack('f',struct.pack('f',x))[0];rows=[];sets=[]
for day in [30,40,50,60]:
 p=r/f'site-tmp/natural60-day{day}.json';w=json.loads(p.read_text());n=len(w['water']);area=f(4*math.pi*(w['radius']*1000)**2/n);divider=f(area*12000)*18.015/1e12/6.02214076e23
 def saturation(t):
  i=int(t);pressure=lambda v:f(.61078*math.exp(17.27*(v-273.15)/(v+237.3-273.15))*1000)
  return (pressure(i)*(1-(t-i))+pressure(i+1)*(t-i))*divider/(t*1.380649e-23)
 sat=[saturation(t)for t in w['temperature']];dry=[i for i,v in enumerate(w['water'])if v==0];warm=[i for i in dry if 273.15<w['temperature'][i]<355];eligible=[i for i in warm if not w['origin']['cells'][i]['sparse'] and w['vapor'][i]<sat[i]];sets.append(set(eligible))
 rows.append({'day':day,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'game_time':w['game_time'],'day_phase':(w['game_time']/w['rotation_time'])%1,'cells':n,'supersaturated_approx':sum(v>s for v,s in zip(w['vapor'],sat)),'exactly_dry':len(dry),'warm_dry':len(warm),'eligible':[{'cell':i,'temperature_K':w['temperature'][i],'vapor_saturation_ratio_approx':w['vapor'][i]/sat[i],'rain_rate_native_per_day':w['rainfall'][i],'rain_rate_mm_per_day':w['rainfall'][i]*1e9/area,'adjacent_living_patches':sum(bool(w['origin']['cells'][j]['sparse'])for j in g['neighbors'][i])}for i in eligible]})
print(json.dumps({'scope':'Archived four fixed snapshots, no new run. Saturation uses approximate Python implementation of source table interpolation, not bitwise native proof. Candidates far below threshold. Saved rainfall is smoothed rate, not future rainfall.', 'snapshots':rows,'all_four_dry_warm_empty_undersaturated':sorted(set.intersection(*sets))},indent=2))
