from pathlib import Path
from fractions import Fraction as F
import json,sys,hashlib
p=Path(sys.argv[1]);base=json.load(open(p/'arm-0-action.json'));rows=[];effects=[]
for arm in range(5):
 action=json.load(open(p/f'arm-{arm}-action.json'));changes={}
 for key in action:
  if action[key]!=base[key]:changes[key]=[i for i,(a,b)in enumerate(zip(action[key],base[key]))if a!=b] if isinstance(action[key],list)else 'scalar'
 effects.append(dict(arm=arm,changed_fields=changes,water_native_inventory_change=float(sum((F(a)-F(b)for a,b in zip(action['water'],base['water'])),F(0))),target_cover_removed=float(F(base['vegetation'][26788])-F(action['vegetation'][26788])),target_temperature_change=action['temperature'][26788]-base['temperature'][26788]))
 for day in range(8):
  f=p/f'arm-{arm}-day-{day}.json';s=json.loads(f.read_bytes());rows.append(dict(arm=arm,day=day,cover=sum(s['vegetation']),occupied=sum(v>0 for v in s['vegetation']),rabbits=len(s['rabbits']),births=s['rabbit_births'],deaths=s['rabbit_deaths'],plant_births=s['plant_births'],target=dict(cover=s['vegetation'][26788],temperature=s['temperature'][26788],water_native=s['water'][26788],**s['plants'][26788]),tender_cover=s['vegetation'][26790],sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
(p/'analysis.json').write_text(json.dumps(dict(immediate=effects,daily=rows),indent=2)+'\n')
print(json.dumps(effects,indent=2));print('ENDPOINTS',json.dumps([r for r in rows if r['day']==7]))
