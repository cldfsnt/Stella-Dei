import json,gzip
from pathlib import Path
from fractions import Fraction as F
p=Path(__file__).parent
assert gzip.decompress((p/'safe.jsonl.gz').read_bytes())==gzip.decompress((p/'fast.jsonl.gz').read_bytes())
for n,l in enumerate(gzip.open(p/'safe.jsonl.gz','rt')):
 d=json.loads(l);r=d['result']
 assert F(d['source'])-F(r['source'])==F(r['target'])-F(d['target'])==F(r['paid'])
 assert 0<=F(r['paid'])<=min(F(d['source']),F(d['requested']))
print(n+1,'exact Fraction scalar records and Safe/Fast parity passed')
