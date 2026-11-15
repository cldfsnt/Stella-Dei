#!/usr/bin/env python3
import json,struct,sys,math
from pathlib import Path
from fractions import Fraction as F
P=Path(sys.argv[1])
def f32(x):return struct.unpack('f',struct.pack('f',x))[0]
def rows(mode):return [json.loads(l.split('HYBRID ')[1])for l in (P/(mode+'.log')).read_text().splitlines()if 'HYBRID 'in l]
def endpoints(mode):return [json.loads(l.split('BUCKET_SEVEN_DAY ')[1])for l in (P/(mode+'.log')).read_text().splitlines()if 'BUCKET_SEVEN_DAY 'in l]
def norm(s,mode):return {k:(f32(v)if mode=='hybrid'and k in ['liquid','vapor','rain']else v)for k,v in s.items()}
def total(s,mode,c):s=norm(s,mode);return(F(s['liquid'])+F(s['vapor']))*c+F(s['soil'])
summary={};series={}
for mode in ['hybrid','f64']:
 a=rows(mode);out=[];seq=[]
 for row in a:
  p=row['params'];r=row['result'];conv=F(1000000000)/F(p['area']);states=[norm(row['before'],mode)]+[norm(s,mode)for s in r['stages']];errors=[total(x,mode,conv)-total(y,mode,conv)for x,y in zip(states,states[1:])]
  assert r['drained_density']==0 and states[4]==states[5]
  old,new=states[3:5];debit=(F(old['liquid'])-F(new['liquid']))*conv;credit=F(new['soil'])-F(old['soil']);assert 0<=credit<=debit
  C=F(p['capacity']);L=F(old['liquid'])*conv;W=F(old['soil']);factor=min(F(1),max(F(0),(L+C-W)/C))if C>0 else F(0)
  ideal=min(L,C-W,F(p['infiltration_rate'])*F(p['dt'])*factor)if p['temperature']>273.15 else F(0)
  assert F(r['infiltration_requested_density'])<=ideal and debit<=ideal,(mode,row['name'],debit,ideal)
  standing=(F(states[0]['liquid'])-F(states[1]['liquid']))*conv;soilevap=F(states[1]['soil'])-F(states[2]['soil']);assert standing+soilevap<=F(r['request_native'])*conv,(mode,row['name'],standing+soilevap,F(r['request_native'])*conv)
  if states[1]['liquid']>0 or p['temperature']<=273.15:assert soilevap==0
  data={'name':row['name'],'dt':p['dt'],'phase_errors':list(map(float,errors)),'signed':float(sum(errors)),'sumabs':float(sum(map(abs,errors))),'soil_infiltration':float(credit),'ideal_infiltration':float(ideal),'infiltration_ratio':float(credit/ideal)if ideal>0 else None,'soil_evap':float(soilevap),'final_soil':r['state']['soil']};out.append(data)
  if row['name']=='seven_day_sequence':seq.append(data)
 # Same explicit ordering:3fixtures*3dts, 7*86400/dt records persequence.
 offset=0;sequences=[]
 for fixture in range(3):
  for dt in [360,720,1440]:
   n=int(7*86400/dt);part=seq[offset:offset+n];offset+=n;assert len(part)==n
   sequences.append({'fixture':fixture,'dt':dt,'signed':sum(x['signed']for x in part),'sumabs':sum(x['sumabs']for x in part),'infiltration':sum(x['soil_infiltration']for x in part),'ideal_infiltration_sum':sum(x['ideal_infiltration']for x in part),'soil_evap':sum(x['soil_evap']for x in part)})
 assert offset==len(seq)
 summary[mode]={'records':len(a),'all_source_budget_head_gates_pass':True,'max_step_sumabs':max(x['sumabs']for x in out),'max_step_abs_signed':max(abs(x['signed'])for x in out),'dry_counterfactual_zero_soil':sum(x['name']=='actual_vapor_counterfactual_dry'and x['final_soil']==0 for x in out),'sequences':sequences,'endpoints':endpoints(mode),'one_step_rows':[x for x in out if x['name']!='seven_day_sequence']}
 series[mode]=a
# Initial paired inputs match for nonsequence cases; sequence starts are checked via endpoints.
ha=[x for x in series['hybrid']if x['name'] not in ('seven_day_sequence','cold_warm_cold')];fa=[x for x in series['f64']if x['name'] not in ('seven_day_sequence','cold_warm_cold')];assert len(ha)==len(fa)
for h,f in zip(ha,fa):assert h['name']==f['name']and h['params']==f['params']and norm(h['before'],'hybrid')==f['before'],(h['name'],h['before'],f['before'])
for h,f in zip(summary['hybrid']['endpoints'],summary['f64']['endpoints']):assert norm(h['initial'],'hybrid')==f['initial']
summary['paired_initial_states_match']=True
print(json.dumps(summary,indent=2))
