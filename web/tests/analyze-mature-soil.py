#!/usr/bin/env python3
import json,sys,struct,math
from fractions import Fraction as F
from pathlib import Path
lines=Path(sys.argv[1]).read_text().splitlines()
roots=[];alloc=[];end={}
for l in lines:
 if l.startswith('SHARED_ROOT '):roots.append(json.loads(l.split(' ',1)[1]))
 if l.startswith('SHARED_ALLOCATION '):alloc.append(json.loads(l.split(' ',1)[1]))
 if l.startswith('TERRESTRIAL_AFTER '):
  x=json.loads(l.split(' ',1)[1]);end[x['arm']]=x
assert len(roots)==len(alloc)
out=[]
for r,a in zip(roots,alloc):
 source=(F(r['soil_before'])-F(r['soil_after']))*F(r['area_m2'])
 receiver=(F(r['vapor_after'])-F(r['vapor_before']))*10**9
 credits=sum(map(F,r['credits']),F(0))+F(a['bare_credit'])
 assert credits<=F(a['funded'])<=F(r['paid'])
 assert F(r['paid'])*F(r['area_m2'])<=source
 assert F(a['funded'])*F(r['area_m2'])<=receiver
 for d,c,bits in zip(r['demands'],r['credits'],r['h_bits']):
  h=struct.unpack('<f',struct.pack('<I',bits))[0]
  assert F(h)*F(d)<=F(c)<=F(d)
 residual=receiver-source
 assert source>0 and abs(residual)<=source/F(2**20)
 ulp=lambda v:max(F(math.nextafter(v,math.inf))-F(v),F(v)-F(math.nextafter(v,-math.inf)))
 envelope=2*ulp(r['vapor_after'])*10**9+2*ulp(r['soil_before'])*F(r['area_m2'])+16*F(2**-52)*source
 assert abs(residual)<=envelope
 out.append(dict(source_kg=float(source),receiver_kg=float(receiver),residual_kg=float(residual),relative_error=float(abs(residual)/source),funded=a['funded'],bare_credit=a['bare_credit'],root_credits=r['credits'],h=[struct.unpack('<f',struct.pack('<I',v))[0] for v in r['h_bits']]))
assert len(end)==2
print(json.dumps(dict(root_receipts=out,endpoints=end,scope='Finite same-call source and receiver funding; not whole-world closure'),indent=2))
