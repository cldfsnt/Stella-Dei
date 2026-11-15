from pathlib import Path
import json,sys,hashlib
p=Path(sys.argv[1]);result={}
def rows(file,tag):
 return [json.loads(l.split(' ',1)[1]) for l in (p/file).read_text().splitlines() if l.startswith(tag+' ')]
for arm in (0,1):
 main=f'main-{arm}.log';resume=f'resume-{arm}.log'
 assert 'COMPLETE' in (p/main).read_text() and 'COMPLETE' in (p/resume).read_text()
 assert (p/f'arm-{arm}-60.json').read_bytes()==(p/f'resume-arm-{arm}-60.json').read_bytes()
 for tag in ('BIRTH','ROOT_WATER','FATE'):
  assert [x for x in rows(main,tag)if x['tick']>30]==rows(resume,tag),tag
 fate=[x for x in rows(main,'FATE')if x['cohort']['lineage']==524]
 water=[x for x in rows(main,'ROOT_WATER')if x['lineage']==524]
 result[arm]={'setup':rows(main,'SETUP'),'drain':rows(main,'DRAIN'),'fate_ticks':len(fate),'first_fate':fate[:1],'last_fate':fate[-1:],'root_phase_events':len(water),'positive_credit_events':sum(x['credit']>0 for x in water),'credit_sum_kg_m2':sum(x['credit']for x in water),'demand_sum':sum(x['demand']for x in water),'first_water':water[:1],'restart_exact':True,'births':len(rows(main,'BIRTH')),'complete':[l for l in (p/main).read_text().splitlines()if l.startswith('COMPLETE')]}
 for x in water:assert 0<=x['credit']<=x['demand']
a=json.loads((p/'arm-0-0.json').read_text());b=json.loads((p/'arm-1-0.json').read_text());assert a['origin']['cells'][18327]['sparse'][2]['value']['lineage']==524
b['origin']['cells'][18327]['sparse'][2]['value']['root_fraction']=a['origin']['cells'][18327]['sparse'][2]['value']['root_fraction'];assert a==b
(p/'analysis.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
from fractions import Fraction as F
signed=F(0);absolute=F(0);maximum=0.;trace=[]
for x in rows('main-0.log','ROOT_WATER'):
 if x['lineage']!=524:continue
 debit=F(x['soil_before'])-F(x['soil_after']);physical=debit*F(x['area']);received=(F(x['vapor_after'])-F(x['vapor_before']))*10**9;err=received-physical
 assert F(x['credit'])+F(x['bare_credit'])<=debit
 assert F(x['h'])*F(x['demand'])<=F(x['credit'])<=F(x['demand'])
 signed+=err;absolute+=abs(err);maximum=max(maximum,float(abs(err)/physical))
 trace.append({k:x[k]for k in ('tick','demand','credit','h','shared_paid','bare_credit','residual_density','soil_before','soil_after','vapor_before','vapor_after','area','environment')})
(p/'receipt-audit.json').write_text(json.dumps({'source_and_h_funding':True,'shared_residual_signed_kg':float(signed),'shared_residual_sumabs_kg':float(absolute),'max_shared_relative':maximum,'trace':trace},indent=2))
