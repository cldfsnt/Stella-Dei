#!/usr/bin/env python3
"""Independent scalar-f32 proxy with exact integer ledger in units2^-149.
Not SIMD machine-code equivalence, concurrency evidence, or a replacement solver.
"""
from pathlib import Path
import json,hashlib,numpy as np
from fractions import Fraction
r=Path(__file__).resolve().parents[2];path=r.parent/'site-tmp/liquid-transport-order/input.json';data=json.loads(path.read_text());f=np.float32
for line in (r.parent/'site-tmp/propagule-graph/graph.jsonl').read_text().splitlines():
 row=json.loads(line)
 if row['kind']=='cell':assert data['neighbors'][row['cell']]==[row['neighbors'][j]for j in [0,3,1,4,2,5]]
mass=np.array(data['mass'],dtype=np.float32);e=np.array(data['elevation'],dtype=np.float32);neighbors=data['neighbors'];factor=f(f(f(.00002)*f(1440))/f(6));km=f(1000/data['area'])
def units(x):
 n,d=float(x).as_integer_ratio();return n<<(149-(d.bit_length()-1))
def record(n):
 q=Fraction(n,1<<149);return {'native':float(q),'exact_numerator':q.numerator,'exact_denominator':q.denominator}
results=[]
for width in [4,16]:
 endpoints=[]
 for reverse in [False,True]:
  out=mass.copy();receiver=accum=subtract=0;incoming_sources=0;incoming_sum=0;excluded=0;excluded_units=0
  for b in (reversed(range(len(mass)//width)) if reverse else range(len(mass)//width)):
   start=b*width;old=out[start:start+width].copy();heights=np.array([f(e[start+j]+f(old[j]*km))for j in range(width)],dtype=np.float32);shared=np.array([f(x*factor)for x in old],dtype=np.float32);removed=np.zeros(width,dtype=np.float32)
   for j,x in enumerate(old):
    if x>mass[start+j]:incoming_sources+=1;incoming_sum+=units(x)-units(mass[start+j])
   for direction in range(6):
    for j in range(width):
     t=neighbors[start+j][direction];target=f(e[t]+f(mass[t]*km));sent=f(min(shared[j],f(f(f(heights[j]-target)/km)*factor))) if heights[j]>target else f(0)
     if start<=t<start+width:
      if sent>0:excluded+=1;excluded_units+=units(sent)
      sent=f(0)
     before=out[t];out[t]=f(before+sent);receiver+=units(out[t])-units(before)-units(sent)
     before=removed[j];removed[j]=f(before+sent);accum+=units(removed[j])-units(before)-units(sent)
   for j in range(width):
    out[start+j]=f(old[j]-removed[j]);subtract+=units(out[start+j])-units(old[j])+units(removed[j])
  delta=sum(map(units,out))-sum(map(units,mass));assert delta==receiver-accum+subtract
  row={'width':width,'reverse':reverse,'exact_world_delta':record(delta),'receiver_add_rounding':record(receiver),'six_edge_accumulator_rounding':record(accum),'donor_subtraction_rounding':record(subtract),'source_cells_with_previous_receipts':incoming_sources,'prior_receipt_amount_seen_by_donors':record(incoming_sum),'suppressed_positive_same_lane_edges':excluded,'suppressed_proposed_amount':record(excluded_units),'tail_cells':len(mass)%width,'output_sha256_f32bytes':hashlib.sha256(out.tobytes()).hexdigest()};results.append(row);endpoints.append(out);print(json.dumps(row),flush=True)
 print('ORDER_DIFFERENCES',width,int(np.sum(endpoints[0]!=endpoints[1])),flush=True)
o=r/'web/tests/continuation-review/legacy-liquid-operation-audit';o.mkdir(exist_ok=True);(o/'results.json').write_text(json.dumps({'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'factor_f32':float(factor),'km_per_native_f32':float(km),'cases':results},indent=2)+'\n')
