#!/usr/bin/env python3
"""Read-only fixed-snapshot precision inventory; no simulated selection."""
import json,math,struct,hashlib,gzip
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];TMP=ROOT.parent/'site-tmp';OUT=ROOT/'web/tests/continuation-review/paid-hydration/soil-root-design/precision-inventory'
AREA=7669529600.;CONV=1e9/AREA
FILES=[TMP/'natural60-day30.json',TMP/'natural60-day60.json',TMP/'grazing-coupled/arm-0-day90.json']+[TMP/f'retention-coupled/arm-{i}.json'for i in range(6)]
def f32(x):return struct.unpack('f',struct.pack('f',x))[0]
def ulp32(x):
 b=struct.unpack('I',struct.pack('f',x))[0];return struct.unpack('f',struct.pack('I',b+1))[0]-x

def stats(a):
 a=sorted(a)
 return {'count':len(a),'min':a[0]if a else None,'median':a[len(a)//2]if a else None,'max':a[-1]if a else None}
def cohorts(c):
 if 'cohorts'in c:return list(enumerate(c['cohorts']))
 return [(x['index'],x['value'])for x in c.get('sparse',[])]
def differror(before,after,requested):return float(F(before)-F(after)-F(requested))
reports=[];rows=[]
for path in FILES:
 d=json.loads(path.read_text());cells=d['origin']['cells'];pools={};counts={'live':0,'supported':0,'empty_slots':0};case={}
 for kind,key in [('surface','water'),('vapor','vapor')]:
  native=d[key];density=[x*CONV for x in native]
  pools[kind]={'density':stats(density),'f32_native_ulp_as_density':stats([ulp32(x)*CONV for x in native]),'f64_native_ulp_as_density':stats([math.ulp(x)*CONV for x in native]),'f64_density_ulp':stats([math.ulp(x)for x in density]),'conversion_error_abs':stats([abs(float(F(y)-F(x)*F(1000000000)/F(AREA)))for x,y in zip(native,density)])}
 for idx,c in enumerate(cells):
  live=[(slot,co)for slot,co in cohorts(c)if co.get('biomass',0)>0];counts['empty_slots']+=4-len(live)
  for slot,co in live:
   counts['live']+=1;support=co.get('support_mass',0);counts['supported']+=support>0
   frond=max(0,co['biomass']-support);r=co.get('retention_allocation',0);depth=d['water'][idx]*CONV/1000
   for u in [0,1/32,1/4]:
    if u+r>1:continue
    height=min(.5,.2*support*(1-u-r)/(frond+.01)*(1+.6*(1-co['efficiency'])-.3*co['structure']))
    exposure=max(0,min(1,(height-depth)/height))if height>0 else float(depth==0)
    for dt in [360,720,1440]:
     dry=.1*frond*dt/86400;actual=dry*exposure
     key=f'u={u}:dt={dt}';s=case.setdefault(key,{'actual_demand':[],'hypothetical_dry_demand':[],'supported_dry_demand':[],'vapor_ulp_over_dry_demand':[]})
     if actual>0:s['actual_demand'].append(actual)
     if dry>0:s['hypothetical_dry_demand'].append(dry);s['vapor_ulp_over_dry_demand'].append(math.ulp(d['vapor'][idx]*CONV)/dry)
     if dry>0 and support>0:s['supported_dry_demand'].append(dry)
     # Diagnostic source-funded root flow at already-tested .25 soil wetness.
     # No soil exists in snapshots: this is a representability probe only.
     for k in [1,10]:
      wanted=min(dry,support*u*k*.25*dt/86400)
      if wanted<=0:continue
      soil=.25;after=soil-wanted;vapor=d['vapor'][idx]*CONV;after_v=vapor+wanted
      debit=F(soil)-F(after);credit=F(after_v)-F(vapor)
      rows.append({'world':path.name,'cell':idx,'slot':slot,'lineage':co['lineage'],'u':u,'dt':dt,'k':k,'request':wanted,'source':soil,'source_after':after,'receiver':vapor,'receiver_after':after_v,'actual_source_debit':float(debit),'actual_receiver_credit':float(credit),'signed_error':float(debit-credit),'relative_error':float(abs(debit-credit)/F(wanted)),'source_debit_zero':debit==0,'receiver_credit_zero':credit==0,'source_debit_exceeds_request':debit>F(wanted)})
 reports.append({'path':str(path.relative_to(TMP)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'pools':pools,'counts':counts,'demand':{k:{n:stats(v)for n,v in val.items()}for k,val in case.items()}})
# Preserved actual local assay daily-state operand probes, not additional evolution.
local=[]
for folder in ['physiology','physiology-corrected']:
 p=OUT.parent/folder/'run.log.gz'
 for line in gzip.decompress(p.read_bytes()).decode().splitlines():
  if 'SOIL_PHYSIOLOGY 'not in line:continue
  d=json.loads(line.split('SOIL_PHYSIOLOGY ')[1]);soil=d['soil'];v=d['vapor'];co=d['cell']['cohorts'][1]
  frond=max(0,co['biomass']-co['support_mass']);wanted=min(.1*frond*d['dt']/86400,co['support_mass']*d['root']*d['conductance_per_day']*soil*d['dt']/86400)
  if wanted<=0:continue
  debit=F(soil)-F(soil-wanted);credit=F(v+wanted)-F(v)
  local.append({'assay':folder,'root':d['root'],'k':d['conductance_per_day'],'regime':d['regime'],'dt':d['dt'],'day':d['day'],'request':wanted,'source':soil,'receiver':v,'source_debit_zero':debit==0,'receiver_credit_zero':credit==0,'signed_error':float(debit-credit),'relative_error':float(abs(debit-credit)/F(wanted))})
summary={'source_note':'Fixed observed world pools; prescribed root fractions/dry demand are geometry/precision probes, not new organisms or simulated selection. Soil .25 in root-flow probe is hypothetical diagnostic only. area is native meanarea from frozen harness.','area_m2':AREA,'worlds':reports,'root_probe_count':len(rows),'root_probe_errors':{k:stats([abs(x[k])for x in rows])for k in ['signed_error','relative_error']},'root_source_zero':sum(x['source_debit_zero']for x in rows),'root_receiver_zero':sum(x['receiver_credit_zero']for x in rows),'root_source_overrequest':sum(x['source_debit_exceeds_request']for x in rows),'actual_local_probes':local,'actual_local_error':stats([abs(x['signed_error'])for x in local]),'actual_local_relative_error':stats([x['relative_error']for x in local])}
OUT.mkdir(parents=True,exist_ok=True);(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');(OUT/'root-probes.jsonl.gz').write_bytes(gzip.compress(('\n'.join(json.dumps(x)for x in rows)+'\n').encode(),mtime=0))
print(json.dumps({k:summary[k]for k in ['root_probe_count','root_probe_errors','root_source_zero','root_receiver_zero','root_source_overrequest','actual_local_error','actual_local_relative_error']},indent=2))
