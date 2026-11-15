#!/usr/bin/env python3
"""Read-only necessary funding gate from actual saved f32 values; no mutations."""
import json,struct,hashlib,sys
from pathlib import Path
root=Path(__file__).resolve().parents[2]
code=(root/'src/simulation/microbes.zig').read_text();directed=(root/'src/experimental/directed_sample.zig').read_text()
assert 'return reproduceSized(donor,which,destination,stats,mutate,0.01,0.03,0.04);' in code
assert 'if(!M.reproduce(&source,slot,&target,&next,false))return .{};' in directed
f32=lambda x:struct.unpack('f',struct.pack('f',x))[0]
result=[]
for day in [40,50,60]:
 p=Path(sys.argv[1])/f'natural60-day{day}.json';b=p.read_bytes();s=json.loads(b)
 rows=[]
 for cell,c in enumerate(s['origin']['cells']):
  for entry in c['sparse']:
   co=entry['value']
   if co['biomass']>0:rows.append({'cell':cell,'slot':entry['index'],'id':str(co['lineage']),'biomass':co['biomass'],'credit':co['reproduction_credit'],'support':co['support_mass']})
 mass=[r for r in rows if r['biomass']>=f32(.03)];credit=[r for r in rows if r['credit']>=f32(.04)]
 hits=[r for r in mass if r['credit']>=f32(.04)]
 result.append({'day':day,'source_sha256':hashlib.sha256(b).hexdigest(),'living':len(rows),'mass_gate':len(mass),'credit_gate':len(credit),'both':hits,'max_mass':max(r['biomass'] for r in rows),'max_credit':max(r['credit'] for r in rows),'rows':rows})
print(json.dumps(result,indent=2))
