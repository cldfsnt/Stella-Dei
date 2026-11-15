import json,gzip,sys
from fractions import Fraction as F
from pathlib import Path
path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('initial.jsonl.gz')
for n,l in enumerate(gzip.open(path,'rt')):
 d=json.loads(l);s=d['scatter'];g=d['gather'];sp=sum(map(F,s['paid']),F(0));gp=sum(map(F,g['paid']),F(0))
 assert F(d['source'])-F(s['source'])==F(s['target'])-F(d['target'])==sp
 assert F(g['target'])-F(d['target'])==gp
 for i in range(4):
  assert F(d['sources'][i])-F(g['sources'][i])==F(g['paid'][i])
  assert 0<=F(s['paid'][i])<=F(d['wanted'][i])
  assert 0<=F(g['paid'][i])<=min(F(d['wanted'][i]),F(d['sources'][i]))
print(n+1,'exact Fraction global/per-cohort scatter/gather ledgers passed')
