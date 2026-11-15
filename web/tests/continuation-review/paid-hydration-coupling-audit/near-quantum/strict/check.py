import gzip,json,struct
from fractions import Fraction as F
from pathlib import Path
p=Path(__file__).parent
assert gzip.decompress((p/'safe.jsonl.gz').read_bytes())==gzip.decompress((p/'fast.jsonl.gz').read_bytes())
n=0
for line in gzip.open(p/'safe.jsonl.gz','rt'):
 d=json.loads(line); f32=lambda x:F(struct.unpack('f',struct.pack('f',x))[0])
 paid=(f32(d['source'])-f32(d['pool']))*F(d['conversion'])
 credited=sum((F(b)-F(a) for a,b in zip(d['stores'],d['receivers'])),F(0))
 excess=F(d['after'])-F(d['before'])
 assert paid==credited+excess and 0<=excess<=credited
 assert all(F(s)<=F(r)<=F(c) for s,r,c in zip(d['stores'],d['receivers'],d['caps']))
 n+=1
print(n,'exact rational ledgers passed; Safe/Fast byte parity')
