from pathlib import Path
import json,struct,hashlib,gzip,shutil,re,collections
from PIL import Image
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/protective-journey';old=r.parent/'site-tmp/natural-shoreline';o=r/'web/tests/continuation-review/protective-natural-journey';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert(b/'final.json').read_bytes()==(b/'resumed.json').read_bytes();assert(b/'parity-on.json').read_bytes()==(b/'parity-off.json').read_bytes()
def clean(x):
 if isinstance(x,dict):return{k:clean(v)for k,v in x.items()if k not in ['protective_strategy','protective_investment','protective_clock']}
 return[clean(v)for v in x]if isinstance(x,list)else x
for n in ['fresh.json','seeded.json']:
 a=json.loads((b/n).read_text());a['version']=14;assert clean(a)==json.loads((old/n).read_text())
rows={};credits=collections.defaultdict(list);used=collections.defaultdict(list);paid=[]
for l in(b/'main.log').read_text().splitlines():
 tag,_,body=l.partition(' ')
 try:rows.setdefault(tag,[]).append(json.loads(body))
 except:
  if tag=='ROOT_CREDIT':m=re.fullmatch(r'tick=(\d+) id=(\d+) kg_m2=(.*)',body);credits[int(m[2])].append([int(m[1]),float(m[3])])
  if tag=='ROOT_USED':m=re.fullmatch(r'tick=(\d+) id=(\d+) h=(.*)',body);used[int(m[2])].append([int(m[1]),float(m[3])])
  if tag=='PROTECTION_PAID':paid.append(body)
f32=lambda v:struct.unpack('<f',struct.pack('<f',v))[0];seed=json.loads((b/'seeded.json').read_text())['protective_strategy']['stream_seed'];known={};positive=negative=rare=0
for x in rows['BIRTH_OR_INITIAL']:
 c=x['cohort'];i=c['lineage'];parent=c['parent'];v=c['protective_investment'];assert c['protective_clock']==-1
 if parent:
  data=bytearray(48);data[:12]=b'STELLA-REST1';struct.pack_into('<QQQI',data,16,seed,parent,i,c['generation']);h=hashlib.sha256(data).digest();rr=int.from_bytes(h[:8],'little')&511==0;u=(int.from_bytes(h[8:16],'little')>>11)/2**53;d=f32(((-1 if h[16]&1==0 else 1)*(.1+.2*u))if rr else(u-.5)*.2);assert max(0,min(1,f32(known[parent]+d)))==v;rare+=rr;positive+=d>0;negative+=d<0
 else:assert v==0
 known[i]=v
births={x['cohort']['lineage']:x for x in rows['BIRTH_OR_INITIAL']};deaths={x['id']:x['tick']for x in rows['DEATH']}
funded=[{'id':i,'birth':births[i],'receipts':v,'used_h':used[i],'death_tick':deaths.get(i)}for i,v in credits.items()]
assert all(x['death_tick']is not None for x in funded);assert rows['DAILY'][-1]['living']==7+rows['DAILY'][-1]['stats']['births']-len(deaths)
summary={k:rows[k]for k in ['DAILY','FOUNDER','WATER_PLUS','POND_TARGET','DRAWDOWN','COMPLETE','VISIT']};summary.update({'funded_root_lineages':funded,'protective_entries':paid,'nonactive_state_count':sum(x['clock']>=0 for x in rows['PROTECTION_STATE']),'independent_mutation':{'births':len(known)-7,'positive':positive,'negative':negative,'rare':rare},'initial_identity_only_exact':True,'restart_exact':True,'observer_exact':True})
(o/'results.json').write_text(json.dumps(summary,indent=2));(o/'state-hashes.json').write_text(json.dumps({p.name:sha(p)for p in b.glob('*.json')if p.name not in ['owner-hashes.json','source-hashes.json']},indent=2))
for n in ['main.log','resume.log','parity-on.log','parity-off.log','final.json']:
 data=(b/n).read_bytes();z=gzip.compress(data,mtime=0);assert gzip.decompress(z)==data and len(z)<8*1024*1024;(o/(n+'.gz')).write_bytes(z)
for n in ['build.log','history13.log','history14.log','owner-hashes.json','source-hashes.json']:shutil.copy2(b/n,o/n)
for law in [13,14]:
 for i in range(1,5):assert(b/f'history-{law}-{i}.json').read_bytes()==(r.parent/f'site-tmp/protective-history-reference/history-{law}-{i}.json').read_bytes()
for n in ['day0','day7','day21']:Image.open(b/(n+'.ppm')).save(o/(n+'.png'))
print('ALL_EXACT_PASS',sha(b/'final.json'),'bytes',sum(p.stat().st_size for p in o.iterdir()if p.is_file()))
