#!/usr/bin/env python3
import sys,json,math,struct,gzip
from fractions import Fraction as F
from pathlib import Path

def f32(x):return struct.unpack('f',struct.pack('f',x))[0]
def next32(x,up):
 x=f32(x);b=struct.unpack('I',struct.pack('f',x))[0];return struct.unpack('f',struct.pack('I',b+(1 if up else -1)))[0]
def total(s,conv):return (F(f32(s['liquid']))+F(f32(s['vapor'])))*conv+F(s['soil'])
def frac(x):return F(float(x))
def ratio(actual,request):return float(actual/request)if request>0 else None
def receiver_first_max(target,request_density,conv):
 # Optimistic representable receiver-only bound; NOT a complete two-endpoint algorithm.
 if request_density<=0:return F(0)
 old=F(f32(target));ideal=old+request_density/conv;after=f32(float(ideal))
 if F(after)>ideal:after=next32(after,False)
 return max(F(0),(F(after)-old)*conv)
lines=Path(sys.argv[1]).read_text().splitlines();out=[]
for line in lines:
 if 'HYBRID 'not in line:continue
 x=json.loads(line.split('HYBRID ')[1]);p=x['params'];r=x['result'];s=x['before'];conv=F(1000000000)/F(p['area']);st=[s]+r['stages'];errors=[total(a,conv)-total(b,conv)for a,b in zip(st,st[1:])];legacy=total(s,conv)-total(x['legacy'],conv)
 initial_depth=F(f32(s['liquid']))*conv/1000;category='dry'if initial_depth==0 else 'shallow_0_to_0.2m'if initial_depth<=F(.2)else 'high_standing_over_0.2m'
 warm=p['temperature']>273.15
 evap_want=min(F(f32(s['liquid'])),F(r['request_native']))*conv;evap_actual=(F(f32(s['liquid']))-F(f32(st[1]['liquid'])))*conv
 soil_want=min(F(st[1]['soil']),max(F(0),F(r['request_native'])*conv-evap_actual))if warm and st[1]['liquid']==0 else F(0)
 soil_actual=F(st[1]['soil'])-F(st[2]['soil']);soil_receiver=(F(f32(st[2]['vapor']))-F(f32(st[1]['vapor'])))*conv
 infiltrate_potential=min(max(F(0),F(p['capacity'])-F(st[3]['soil'])),F(p['infiltration_rate'])*F(p['dt']))if warm else F(0)
 infiltrate_want=min(infiltrate_potential,F(f32(st[3]['liquid']))*conv)
 infiltrate_actual=(F(f32(st[3]['liquid']))-F(f32(st[4]['liquid'])))*conv;soil_credit=F(st[4]['soil'])-F(st[3]['soil'])
 drain_want=min(F(st[4]['soil']),F(p['drainage_rate'])*F(p['dt']))if warm else F(0)
 drain_actual=F(st[4]['soil'])-F(st[5]['soil']);drain_receiver=(F(f32(st[5]['liquid']))-F(f32(st[4]['liquid'])))*conv
 data={'name':x['name'],'dt':p['dt'],'temperature':p['temperature'],'category':category,'initial_depth_m':float(initial_depth),'exposed_seconds':r['exposed_seconds'],'legacy_residual':float(legacy),'enabled_phase_residuals':list(map(float,errors)),'enabled_signed':float(sum(errors)),'enabled_sumabs':float(sum(map(abs,errors))),'enabled_minus_legacy_one_step':float(sum(errors)-legacy),'added_soil_phase_sumabs':float(sum(abs(errors[i])for i in [1,3,4])),'standing_evap_requested':float(evap_want),'standing_evap_debit':float(evap_actual),'standing_evap_ratio':ratio(evap_actual,evap_want),'soil_evap_requested':float(soil_want),'soil_evap_debit':float(soil_actual),'soil_evap_receiver_credit':float(soil_receiver),'soil_evap_source_ratio':ratio(soil_actual,soil_want),'soil_evap_receiver_ratio':ratio(soil_receiver,soil_want),'infiltration_capacity_rate_request':float(infiltrate_potential),'infiltration_requested':float(infiltrate_want),'infiltration_actual_source':float(infiltrate_actual),'infiltration_soil_credit':float(soil_credit),'infiltration_ratio':ratio(soil_credit,infiltrate_want),'drainage_requested':float(drain_want),'drainage_debit':float(drain_actual),'drainage_receiver_credit':float(drain_receiver),'drainage_source_ratio':ratio(drain_actual,drain_want),'drainage_receiver_ratio':ratio(drain_receiver,drain_want),'receiver_first_drainage_max_ratio':ratio(receiver_first_max(st[4]['liquid'],drain_want,conv),drain_want),'receiver_first_evap_max_ratio':ratio(receiver_first_max(st[1]['vapor'],soil_want,conv),soil_want)}
 out.append(data)
groups={}
for cat in sorted(set(x['category']for x in out)):
 a=[x for x in out if x['category']==cat];g={'count':len(a),'max_abs_legacy_residual':max(abs(x['legacy_residual'])for x in a),'max_enabled_sumabs':max(x['enabled_sumabs']for x in a),'max_added_soil_sumabs':max(x['added_soil_phase_sumabs']for x in a)}
 for key in ['infiltration_ratio','drainage_receiver_ratio','receiver_first_drainage_max_ratio','soil_evap_receiver_ratio','receiver_first_evap_max_ratio']:
  vals=[x[key]for x in a if x[key]is not None];g[key]={'count':len(vals),'min':min(vals)if vals else None,'max':max(vals)if vals else None,'zero_count':sum(v==0 for v in vals)}
 groups[cat]=g
print(json.dumps({'records':len(out),'interpretation':'same-input one-step attribution, not a whole-engine cumulative error budget; receiver-first is optimistic receiver-only bound, not implemented','groups':groups,'rows':out},indent=2))
