#!/usr/bin/env python3
from pathlib import Path
import json,sys,hashlib,struct
r=Path(sys.argv[1]);lines=(r/'run.log').read_text().splitlines();active=None;events=[];days=[]
for line in lines:
 if line.startswith('ACCESS_START '):active=int(line.split('seed=')[1].split()[0])
 elif line.startswith('ACCESS_HORIZON_END '):active=None
 elif line.startswith('ACCESS_DAY '):days.append(json.loads(line.split(' ',1)[1]))
 elif active is not None and line.startswith('ACCESS_BIRTH '):
  f=dict(t.split('=',1)for t in line.split()[1:]);seed=int(f['stream']);assert seed==active;b=bytearray(48);b[:16]=b'STELLA-TOUGH-V2!';struct.pack_into('<I',b,16,2);struct.pack_into('<Q',b,24,seed);struct.pack_into('<Q',b,32,int(f['event']));struct.pack_into('<I',b,40,int(f['parent_generation']));h=hashlib.sha256(b).digest();p=0 if h[0]&63 else -1/32 if h[1]&1 else 1/32
  assert p==float(f['proposal']);assert float(f['child_d'])==max(0,min(1,float(f['parent_d'])+p));events.append(f)
assert len(days)==21 and sum(l.startswith('ACCESS_PASS ')for l in lines)==3
out={'days':days,'birth_events':events,'summary':[],'snapshots':[]}
for seed in [0,1,42]:
 es=[e for e in events if int(e['stream'])==seed];last=next(d for d in days if d['seed']==seed and d['day']==7);assert last['accepted']==len(es)==last['plant_births'];assert last['calls']>=len(es)
 for key,pred in [('plus',lambda e:float(e['proposal'])>0),('minus',lambda e:float(e['proposal'])<0),('changed',lambda e:e['child_d']!=e['parent_d']),('clipped',lambda e:float(e['proposal'])!=0 and e['child_d']==e['parent_d'])]:assert last[key]==sum(pred(e)for e in es)
 path=r/f'seed-{seed}-end.json';obj=json.loads(path.read_text());assert obj['format']=='sandbox-toughness-v2' and obj['law']==1 and obj['mutation_law']==2 and obj['mutation_enabled'] and obj['stream_seed']==seed
 counts=[0]*33;covers=[0.]*33
 for p,v in zip(obj['state']['plants'],obj['state']['vegetation']):
  d=p['toughness'];assert 0<=d<=1 and d*32==int(d*32)
  if v>0:counts[int(d*32)]+=1;covers[int(d*32)]+=v
 assert counts==last['counts'];assert covers==last['cover'];out['summary'].append(last);out['snapshots'].append({'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size})
for d in days:assert d['credit']<=150*d['removed']
(r/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out['summary'],indent=2))
