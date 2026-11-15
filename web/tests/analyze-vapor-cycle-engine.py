#!/usr/bin/env python3
import json,struct,sys,hashlib
from pathlib import Path
from fractions import Fraction as F
root=Path(sys.argv[1]); area=F(7669529600); native=F(10**9)
def read(mode,t,label,fmt='d'):
 p=root/f'{mode}-{t}-{label}.bin';b=p.read_bytes();return [F.from_float(x[0]) for x in struct.iter_unpack('<'+fmt,b)]
def report(values):
 total=sum(values,F());ab=sum(map(abs,values),F());return {'signed_kg_exact':str(total),'sumabs_kg_exact':str(ab),'signed_kg':float(total),'sumabs_kg':float(ab),'maxabs_kg':float(max(map(abs,values),default=F())),'nonzero_cells':sum(x!=0 for x in values)}
result={}
for mode in ['diagnostic','strict']:
 logs={tag:[] for tag in ['VAPOR_ROOT','VAPOR_FIXED_PULSE','VAPOR_TICK']}
 for line in (root/f'{mode}.log').read_text().splitlines():
  for tag in logs:
   if line.startswith(tag+' '):logs[tag].append(json.loads(line[len(tag)+1:]))
 (root/f'{mode}-root-events.json').write_text(json.dumps(logs['VAPOR_ROOT'],indent=2)+'\n')
 steps=[]
 for t in range(1,7):
  l0=read(mode,t,'prephase-liquid','f');l1=read(mode,t,'postphase-liquid','f');v0=read(mode,t,'prephase-vapor');v1=read(mode,t,'postphase-vapor');s0=read(mode,t,'prephase-soil');s1=read(mode,t,'postphase-soil');va=read(mode,t,'postadvection-vapor');vr=read(mode,t,'postroot-vapor');sr=read(mode,t,'postroot-soil')
  phase=report([(b-a+d-c)*native+(f-e)*area for a,b,c,d,e,f in zip(l0,l1,v0,v1,s0,s1)])
  roots=report([(b-a)*native+(d-c)*area for a,b,c,d in zip(va,vr,s1,sr)])
  adv=(sum(va,F())-sum(v1,F()))*native
  liquid_stage=None
  if t not in (1,4):
   previous=read(mode,t-1,'postphase-liquid','f'); delta=(sum(l0,F())-sum(previous,F()))*native;liquid_stage={'signed_kg_exact':str(delta),'signed_kg':float(delta),'scope':'liquid transport between recorded ticks; no root/soil liquid writes after prior phase'}
  steps.append({'liquid_transport':liquid_stage,'serial':t,'action':int(t>3),'tick':(t-1)%3+1,'phase':phase,'root':roots,'advection_signed_kg_exact':str(adv),'advection_signed_kg':float(adv),'advection_note':'global net only; per-cell redistribution is not an error'})
 result[mode]={'steps':steps,'fixed_pulses':logs['VAPOR_FIXED_PULSE'],'root_events':logs['VAPOR_ROOT'],'ticks':[{'action':x['action'],'tick':x['tick'],'liquid_native':x['liquid'],'vapor_native':x['vapor'],'soil_density':x['soil'],'root_paid':x['audit']['root_paid'],'root_demand':x['audit']['root_demand'],'root_credited':x['audit']['root_credited'],'biomass478':next(c['biomass'] for c in x['cohorts']['cohorts'] if c['lineage']==478)} for x in logs['VAPOR_TICK']]}
(root/'exact-stage-analysis.json').write_text(json.dumps(result,indent=2)+'\n')
(root/'raw-hashes.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.glob('*.bin'))},indent=2)+'\n')
print(json.dumps({m:{'phase_signed_kg':sum(s['phase']['signed_kg'] for s in r['steps']),'phase_sumabs_kg':sum(s['phase']['sumabs_kg'] for s in r['steps']),'root_sumabs_kg':sum(s['root']['sumabs_kg']for s in r['steps']),'advection_signed_kg':sum(s['advection_signed_kg']for s in r['steps'])} for m,r in result.items()},indent=2))
