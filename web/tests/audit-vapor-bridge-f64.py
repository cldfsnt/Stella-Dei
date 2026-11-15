#!/usr/bin/env python3
"""Exact binary Fraction audit; no floating-point residual acceptance oracle."""
from fractions import Fraction as F
from pathlib import Path
import json,math,sys
counts=dict(rows=0,positive=0,refused_or_zero=0,null=0,reference_positive=0,candidate_extra_refusals=0,changed_positive_outputs=0);maximum=F(0)
def ulp(x):
 ns=[math.nextafter(x,math.inf),math.nextafter(x,-math.inf)]
 if not all(math.isfinite(v)for v in ns):return None
 return max(abs(F(v)-F(x))for v in ns)
for line in Path(sys.argv[1]).read_text().splitlines():
 if 'BRIDGE ' not in line:continue
 x=json.loads(line.split('BRIDGE ',1)[1]);counts['rows']+=1;r=x['result'];old=x['reference'];s,v,a,w=map(F,[x['soil'],x['vapor'],x['area'],x['wanted']])
 old_positive=old is not None and old['paid']>0;counts['reference_positive']+=old_positive
 if r is None:counts['null']+=1;counts['candidate_extra_refusals']+=old_positive;continue
 assert all(math.isfinite(r[k])for k in r)
 if r['paid']==0:
  assert F(r['soil'])==s and F(r['vapor'])==v and r['funded']==0
  counts['refused_or_zero']+=1;counts['candidate_extra_refusals']+=old_positive;continue
 counts['positive']+=1
 debit=s-F(r['soil']);credit=F(r['vapor'])-v
 assert 0<F(r['funded'])<=F(r['paid'])<=debit<=w
 assert debit<=s and credit>0
 assert F(r['funded'])*a<=credit*10**9
 residual=credit*10**9-debit*a;ratio=abs(residual)/(debit*a);maximum=max(maximum,ratio)
 assert ratio<=F(1,2**20)
 vu,su=ulp(r['vapor']),ulp(x['soil']);assert vu is not None and su is not None
 envelope=2*vu*10**9+2*su*a+16*F(1,2**52)*debit*a
 assert abs(residual)<=envelope
 if old_positive:counts['changed_positive_outputs']+=any(r[k]!=old[k]for k in ['soil','vapor','paid','funded'])
 if x['i']<30:assert old_positive and all(r[k]==old[k]for k in ['soil','vapor','paid','funded'])
assert counts['rows']==6326
print(json.dumps(dict(counts=counts,max_relative_error=float(maximum),gate='Exact stored-binary funding and unchanged dual relative/ULP allowance; no universal all-finite proof or scheduler test'),indent=2))
