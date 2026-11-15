import json,struct,gzip,math
from pathlib import Path
from fractions import Fraction as F
for n,l in enumerate(gzip.open(Path(__file__).with_name('records.jsonl.gz'),'rt')):
 d=json.loads(l);o=d['before'];z=d['result'];r=z['result'];s=r['state'];a,b,c=[[F(x) for x in d[k]] for k in ['after_infiltration','after_evaporation','after_roots']]
 errors=[F(o['surface'])-a[0]-(a[1]-F(o['soil'])),a[1]-b[1]-(b[2]-a[2]),b[1]-c[1]-(c[2]-b[2]),sum((F(old['water'])-F(new['water']) for old,new in zip(o['cohorts'],s['cohorts'])),F(0))-(F(s['vapor'])-c[2]),c[1]-F(s['soil'])-(F(s['surface'])-c[0])]
 assert sum(map(abs,errors),F(0))<=F(z['ledger']['absolute'])
 assert sum(map(abs,errors),F(0))<=F(z['ledger']['envelope'])
 for error,ends in zip([errors[0],errors[1],errors[2],errors[4]],[[o['surface'],a[0],o['soil'],a[1]],[a[1],b[1],a[2],b[2]],[b[1],c[1],b[2],c[2]],[c[1],s['soil'],c[0],s['surface']]]):
  assert abs(error)<=sum((F(math.ulp(float(x))) for x in ends),F(0))
 rootdebit=b[1]-c[1];credits=sum(map(F,r['root_receipts']),F(0));assert 0<=rootdebit-credits<=F(z['allocation_deficit'])
 for i in range(4):
  root=F(r['root_receipts'][i]);store=F(r['store_receipts'][i]);dem=F(d['params']['demand'][i]);assert 0<=root+store<=dem
  assert store<=F(o['cohorts'][i]['water'])-F(s['cohorts'][i]['water'])
  h=F(struct.unpack('f',struct.pack('f',d['h32'][i]))[0]);assert h*dem<=root+store
  assert F(r['h_paid'][i])*dem<=root+store
print(n+1,'exact Fraction phase error/absolute/envelope and biological funding checks passed')
