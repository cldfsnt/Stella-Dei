"""Independent exact binary endpoint accounting for instrumented selected-patch receipts."""
import sys,re,json,struct
from fractions import Fraction as F
f32=lambda x:F.from_float(struct.unpack('f',struct.pack('f',float(x)))[0])
legs=[];rows=[]
for line in open(sys.argv[1]):
 m=re.search(r'PATCH_LEG cell=(\d+) phase=(\w+) before=(\S+) after=(\S+)',line)
 if m:legs.append((int(m[1]),m[2],f32(m[3]),f32(m[4])))
 m=re.search(r'PATCH_RECEIPT fixture=(\d+) tick=(\d+) cell=(\d+) json=(.*)',line)
 if not m:continue
 r=json.loads(m[4]); sums={k:F(0)for k in ('physiology','spread','clamp','grazing')}
 for cell,phase,b,a in legs:
  assert cell==int(m[3]);sums[phase]+=a-b
 exact_net=F(r['after'])-F(r['before']); exact_total=sum(sums.values());reported={k:F(r[k])for k in ('physiology','spread','clamp','grazed')}
 assert reported['physiology']==sums['physiology'];assert reported['spread']==sums['spread'];assert reported['clamp']==sums['clamp'];assert reported['grazed']==-sums['grazing'];assert F(r['net'])==exact_net
 assert F(r['residual'])==exact_net-exact_total
 rows.append(dict(fixture=int(m[1]),tick=int(m[2]),bites=r['bites'],placements=r['placements'],physiology=r['physiology'],grazed=r['grazed'],residual=r['residual']));legs=[]
expected=int(sys.argv[2]) if len(sys.argv)>2 else 120
assert len(rows)==expected and not legs
print(json.dumps(dict(records=len(rows),exact_operand_phase_and_endpoint_checks=True,bites=sum(r['bites']for r in rows),placements=sum(r['placements']for r in rows),nonzero_residuals=sum(r['residual']!=0 for r in rows),fixtures=[dict(fixture=f,physiology=sum(r['physiology']for r in rows if r['fixture']==f),grazed=sum(r['grazed']for r in rows if r['fixture']==f))for f in sorted({r['fixture']for r in rows})]),indent=2))
