from pathlib import Path
from fractions import Fraction as F
import json,struct,hashlib,collections
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/combined-strategy';out={};f=lambda x:struct.unpack('f',struct.pack('f',x))[0]
for seed in(42,1337):
 for kind in('ordinary','pioneer'):
  name=f'{seed}-{kind}';res=[];N=[];pack=[];tick=0;taghash=hashlib.sha256();resumehash=hashlib.sha256()
  for line in(b/(name+'.log')).open():
   if line.startswith('FOUNDER '):
    x=json.loads(line.split(' ',1)[1]);area=F(x['area']);db=sum(F(c['biomass'])for c in x['after']['cohorts'])-sum(F(c['biomass'])for c in x['before']['cohorts']);source=(F(x['co2_before'])-F(x['co2_after']))*40962*10**9*F(12,44);res.append(source-db*area);N.append((F(x['before']['nutrient'])-F(x['after']['nutrient'])-db*F(f(.1)))*area)
   if line.startswith('TICK_START '):tick=json.loads(line.split(' ',1)[1])['tick']
   if tick>180 and line.startswith(('COHORT ','WIND_PACKET ','WIND_OPPORTUNITY ','WIND_ENDPOINT ','ROOT_WATER ','USED_H ')):taghash.update(line.encode())
   if tick and line.startswith('WIND_PACKET '):pack.append(json.loads(line.split(' ',1)[1]))
  for line in(b/(name+'-resume.log')).open():
   if line.startswith(('COHORT ','WIND_PACKET ','WIND_OPPORTUNITY ','WIND_ENDPOINT ','ROOT_WATER ','USED_H ')):resumehash.update(line.encode())
  assert taghash.digest()==resumehash.digest(),name
  bins=[]
  for lo,hi in[(0,100),(100,250),(250,500),(500,1000),(1000,2500),(2500,5001)]:
   p=[x for x in pack if lo<=x['route']['distance_km']<hi];bins.append({'lo':lo,'hi':hi,'paid':len(p),'arrivals':sum(x['receipt']['arrived']for x in p)})
  out[name]={'founder_source_C_minus_created_signed_kg':str(sum(res,F(0))),'founder_C_error_min_kg':str(min(res)),'founder_C_error_max_kg':str(max(res)),'founder_N_debit_minus_stored_required_signed_kg':str(sum(N,F(0))),'founder_N_error_min_kg':str(min(N)),'continuation_trace_sha256':taghash.hexdigest(),'distance_bins_actual_km':bins,'requested_distance_range_km':[min((x['route']['requested_km']for x in pack),default=0),max((x['route']['requested_km']for x in pack),default=0)],'actual_distance_range_km':[min((x['route']['distance_km']for x in pack),default=0),max((x['route']['distance_km']for x in pack),default=0)]}
(b/'ledger.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));print('ALL_CONTINUATION_TRACE_EXACT_PASS')
