from pathlib import Path
import json,hashlib,sys
root=Path(sys.argv[1]);rows=[]
for arm in range(2):
 prev=None
 for day in range(15):
  p=root/f'arm-{arm}-day-{day}.json';s=json.loads(p.read_bytes());v=s['vegetation'];t=s['plants'];
  row=dict(arm=arm,day=day,rabbits=len(s['rabbits']),rabbit_births=s['rabbit_births'],rabbit_deaths=s['rabbit_deaths'],bites=s['rabbit_meals'],plant_births=s['plant_births'],cover=sum(v),occupied=sum(x>0 for x in v),defended_cover=sum(x for x,z in zip(v,t) if z['toughness']>0),defended_patches=sum(x>0 and z['toughness']>0 for x,z in zip(v,t)),max_generation=max(z['generation'] for x,z in zip(v,t) if x>0),local_zero_crossings=None if prev is None else dict(loss=sum(a>0 and b==0 for a,b in zip(prev,v)),gain=sum(a==0 and b>0 for a,b in zip(prev,v))),patches={str(i):dict(cover=v[i],**t[i],temperature=s['temperature'][i],water_native=s['water'][i])for i in (26790,26788)},sha256=hashlib.sha256(p.read_bytes()).hexdigest())
  rows.append(row);prev=v
(root/'summary.json').write_text(json.dumps(rows,indent=2)+'\n')
for r in rows:
 if r['day'] in (0,1,7,14): print(json.dumps(r))
