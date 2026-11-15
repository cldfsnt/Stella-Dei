import json,struct,math,gzip
from pathlib import Path
from fractions import Fraction as F
maxabs=0;exceed=0
f32=lambda x:struct.unpack('f',struct.pack('f',x))[0]
def ulp32(x):
 x=f32(x);b=struct.unpack('I',struct.pack('f',x))[0];return F(struct.unpack('f',struct.pack('I',b+1))[0])-F(x)
for n,l in enumerate(gzip.open(Path(__file__).with_name('records.jsonl.gz'),'rt')):
 d=json.loads(l);s=d['before'];p=d['params'];r=d['result'];factor=F(10**9)/F(p['area']);total=lambda st:(F(f32(st['liquid']))+F(f32(st['vapor'])))*factor+F(st['soil']);previous=s;err=[]
 for st in r['stages']:
  e=total(previous)-total(st);bound=sum((ulp32(z[k]) for z in [previous,st] for k in ['liquid','vapor']),F(0))*factor+8*(F(math.ulp(previous['soil']))+F(math.ulp(st['soil'])));assert abs(e)<=bound;err.append(e);previous=st
 a,b=r['stages'][2:4];debit=(F(f32(a['liquid']))-F(f32(b['liquid'])))*factor;credit=F(b['soil'])-F(a['soil']);assert 0<=credit<=debit
 evap=F(f32(s['liquid']))-F(f32(r['stages'][0]['liquid']));se=F(r['stages'][0]['soil'])-F(r['stages'][1]['soil']);assert 0<=evap+se/factor<=F(r['request_native'])
 actualcondensed=F(f32(r['stages'][1]['vapor']))-F(f32(r['stages'][2]['vapor']));assert F(r['condensed_native'])<=actualcondensed
 if p['temperature']<=273.15:assert r['soil_evap_density']==r['infiltrated_density']==r['drained_density']==0
 aerr=float(sum(map(abs,err),F(0)));maxabs=max(maxabs,aerr);exceed+=aerr>1e-9
print(n+1,'Fraction gates passed; maxSUMABS',maxabs,'above oldlocal1e-9',exceed)
