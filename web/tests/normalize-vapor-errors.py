#!/usr/bin/env python3
"""Read-only normalization of frozen failures; no new acceptance decisions."""
import json,struct,math,sys
from pathlib import Path
from fractions import Fraction as F
root=Path(sys.argv[1]);x=json.load(open(root/'exact-stage-analysis.json'));out={}
def arr(mode,t,label,fmt='d'):
 return [F.from_float(v[0]) for v in struct.iter_unpack('<'+fmt,(root/f'{mode}-{t}-{label}.bin').read_bytes())]
for mode,r in x.items():
 roots=[]
 for e in r['root_events']:
  debit=(F(e['soil_before'])-F(e['soil_after']))*F(e['area_m2']);received=(F(e['vapor_after'])-F(e['vapor_before']))*10**9;loss=debit-received
  roots.append({'source_kg':float(debit),'received_kg':float(received),'loss_kg':float(loss),'loss_fraction_of_source':float(loss/debit) if debit else None,'vapor_inventory_kg':e['vapor_before']*1e9,'vapor_ulp_kg':math.ulp(e['vapor_after'])*1e9,'loss_in_vapor_ulps':float(loss)/(math.ulp(e['vapor_after'])*1e9),'signal_quantization_fraction_near_one':2**-24})
 phaseflow=F();phaseerror=F();advnet=F();advabsnet=F();advlower=F();inventory=[];steps=[]
 for t,s in enumerate(r['steps'],1):
  before=arr(mode,t,'prephase-vapor');after=arr(mode,t,'postphase-vapor');adv=arr(mode,t,'postadvection-vapor');liq=arr(mode,t,'prephase-liquid','f');soil=arr(mode,t,'prephase-soil')
  exchange=sum((abs(b-a) for a,b in zip(before,after)),F())*10**9
  lower=sum((abs(b-a) for a,b in zip(after,adv)),F())*10**9/2
  net=(sum(adv,F())-sum(after,F()))*10**9
  total=(sum(liq,F())+sum(before,F()))*10**9+sum(soil,F())*7669529600
  err=F(s['phase']['sumabs_kg_exact']);phaseflow+=exchange;phaseerror+=err;advnet+=net;advabsnet+=abs(net);advlower+=lower;inventory.append(float(total))
  steps.append({'serial':t,'phase_represented_vapor_exchange_kg':float(exchange),'phase_sumabs_over_exchange':float(err/exchange) if exchange else None,'advection_net_kg':float(net),'advection_endpoint_half_l1_kg':float(lower),'abs_advection_net_over_lowerbound':float(abs(net)/lower) if lower else None,'water_inventory_kg':float(total),'phase_sumabs_over_inventory':float(err/total),'abs_advection_net_over_inventory':float(abs(net)/total)})
 paid=sum((F(e['soil_before'])-F(e['soil_after']))*F(e['area_m2']) for e in r['root_events']);loss=sum(((F(e['soil_before'])-F(e['soil_after']))*F(e['area_m2'])-(F(e['vapor_after'])-F(e['vapor_before']))*10**9)for e in r['root_events'])
 out[mode]={'root_events':roots,'root_total_source_kg':float(paid),'root_total_loss_kg':float(loss),'root_aggregate_loss_fraction':float(loss/paid)if paid else None,'phase_represented_exchange_kg':float(phaseflow),'phase_sumabs_error_kg':float(phaseerror),'phase_sumabs_over_exchange':float(phaseerror/phaseflow),'advection_signed_net_kg':float(advnet),'advection_sum_abs_tick_net_kg':float(advabsnet),'advection_endpoint_half_l1_total_kg':float(advlower),'advection_abs_tick_net_over_endpoint_lowerbound':float(advabsnet/advlower),'steps':steps}
print(json.dumps(out,indent=2))
