#!/usr/bin/env python3
import sys,json,struct,math
from fractions import Fraction as F
from pathlib import Path
p=Path(sys.argv[1]);records=[json.loads(l.split('HYBRID ')[1])for l in p.read_text().splitlines()if 'HYBRID 'in l]
def f32(x):return struct.unpack('f',struct.pack('f',x))[0]
def u32(x):
 x=f32(x);n=struct.unpack('I',struct.pack('f',x))[0];return F(struct.unpack('f',struct.pack('I',n+1))[0])-F(x)
def total(s,c):return (F(f32(s['liquid']))+F(f32(s['vapor'])))*c+F(s['soil'])
rows=[]
for row in records:
 s=row['before'];r=row['result'];params=row['params'];conv=F(1000000000)/F(params['area']);previous=s;errors=[]
 for i,state in enumerate(r['stages']):
  error=total(previous,conv)-total(state,conv)
  envelope=(u32(previous['liquid'])+u32(state['liquid'])+u32(previous['vapor'])+u32(state['vapor']))*conv+8*(F(math.ulp(previous['soil']))+F(math.ulp(state['soil'])))
  assert abs(error)<=envelope,(row['name'],i,error,envelope)
  errors.append(error);previous=state
 a,b=r['stages'][2:4];native_debit=F(f32(a['liquid']))-F(f32(b['liquid']));soil_credit=F(b['soil'])-F(a['soil']);assert 0<=soil_credit<=native_debit*conv,(row['name'],soil_credit,native_debit*conv)
 ev=F(f32(s['liquid']))-F(f32(r['stages'][0]['liquid']));soil_ev=F(r['stages'][0]['soil'])-F(r['stages'][1]['soil']);assert ev>=0 and soil_ev>=0 and ev+soil_ev/conv<=F(r['request_native']),(ev,soil_ev/conv,r['request_native'])
 if params['temperature']<=273.15:assert soil_ev==0 and r['infiltrated_density']==0 and r['drained_density']==0
 if r['stages'][0]['liquid']>0:assert soil_ev==0
 rows.append({'name':row['name'],'dt':params['dt'],'temperature':params['temperature'],'soil_initial':s['soil'],'saturation':params['saturation'],'phase_signed_errors':[float(x)for x in errors],'signed':float(sum(errors)),'sum_abs':float(sum(map(abs,errors))),'infiltration_soil_credit':float(soil_credit),'infiltration_native_debit_density':float(native_debit*conv),'standing_evap_density':float(ev*conv),'soil_evap_density':float(soil_ev),'exposed_seconds':r['exposed_seconds']})
summary={'records':len(records),'all_structural_fraction_gates_pass':True,'max_sumabs_per_step':max(x['sum_abs']for x in rows),'max_abs_signed_per_step':max(abs(x['signed'])for x in rows),'steps_exceed_local_f64_1e_minus9_gate':sum(x['sum_abs']>1e-9 for x in rows),'rows':rows}
print(json.dumps(summary,indent=2))
