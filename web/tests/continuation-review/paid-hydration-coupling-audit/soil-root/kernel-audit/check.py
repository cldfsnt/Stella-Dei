import json,gzip
from pathlib import Path
from fractions import Fraction as F
p=Path(__file__).parent
for name in ['ample','mixed-scarce']:
 n=0
 for line in gzip.open(p/(name+'.jsonl.gz'),'rt'):
  d=json.loads(line[4:]);b=d['before'];r=d['result'];a=r['state'];pms=d['params']
  def total(s):return sum((F(s[k]) for k in ['surface','soil','vapor']),F(0))+sum((F(c['water']) for c in s['cohorts']),F(0))
  assert total(b)==total(a)
  assert 0<=F(a['soil'])<=F(pms['capacity'])
  for i in range(4):
   root=F(r['root_receipts'][i]);store=F(r['store_receipts'][i]);demand=F(pms['demand'][i]);assert 0<=root+store<=demand
   assert F(b['cohorts'][i]['water'])-F(a['cohorts'][i]['water'])==store
   assert sum((F(r[k][i]) for k in ['root_carbon','reservoir_carbon','canopy_carbon']),F(0))==F(b['cohorts'][i]['support'])
  n+=1
 print(name,n,'exact Fraction water, support, and no-double-spend ledgers passed')
