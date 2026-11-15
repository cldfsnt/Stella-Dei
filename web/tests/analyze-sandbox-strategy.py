#!/usr/bin/env python3
"""Read-only frozen Sandbox phenotype/survivor inventory, not causal selection inference."""
import json,sys,hashlib,struct,math
from pathlib import Path
f32=lambda x:struct.unpack('<f',struct.pack('<f',x))[0]
out=[]
for name in sys.argv[1:]:
 p=Path(name);x=json.loads(p.read_text());v=x['vegetation'];alive=[i for i,c in enumerate(v)if c>0];area=f32(4*math.pi*(x['radius']*1000)**2/len(v));conv=f32(1000/area)
 groups=[]
 for label,lo,hi in [('cool_blue',-math.inf,298),('middle_green',298,308.0000000001),('warm_yellow',308.0000000001,math.inf)]:
  ids=[i for i in alive if lo<=x['plants'][i]['optimum']<hi];groups.append({'label':label,'patches':len(ids),'cover':sum(v[i]for i in ids)})
 visible=[i for i in alive if v[i]>=.08 and f32(x['water'][i]*conv)<=.0005]
 out.append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'day':x['game_time']/86400,'living_patches':len(alive),'cover':sum(v),'sprout_eligible_patches':len(visible),'optimum_min':min(x['plants'][i]['optimum']for i in alive),'optimum_max':max(x['plants'][i]['optimum']for i in alive),'max_generation':max(x['plants'][i]['generation']for i in alive),'palette_groups':groups,'live_plant_records':[{'patch':i,'cover':v[i],'temperature':x['temperature'][i],**x['plants'][i]}for i in alive]})
print(json.dumps({'scope':'Palette is thermal optimum, not defensive strategy. Cross-time survival is confounded by location/feeding/weather/colonization.','worlds':out},indent=2))
