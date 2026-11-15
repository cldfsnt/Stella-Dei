from pathlib import Path
import json,sys,hashlib
p=Path(sys.argv[1]);arms=[];active=None
for line in (p/'run-traces.log').read_text().splitlines():
 if line.startswith('QUANTUM_ARM '):
  v=dict(x.split('=',1) for x in line.split()[1:]);active={'source':int(v['source']),'policy':int(v['policy']),'attempts':[],'accepted':[]};arms.append(active)
 elif line.startswith('QUANTUM_TRIAL_END '):
  active['ledger']=dict(x.split('=',1) for x in line.split()[1:]);active=None
 elif active is not None and line.startswith(('QUANTUM_ATTEMPT ','QUANTUM_ACCEPT ')):
  v=dict(x.split('=',1) for x in line.split()[1:]);active['accepted' if line.startswith('QUANTUM_ACCEPT ') else 'attempts'].append(v)
for a in arms:
 a['refused']=len(a['attempts'])-len(a['accepted']);a['total_debit_kg_m2']=sum(float(v['debit'])for v in a['accepted']);a['total_actual_credit_kg_m2']=sum(float(v['credited'])for v in a['accepted']);path=p/f"arm-{a['source']}-policy-{a['policy']}.json";a['sha256']=hashlib.sha256(path.read_bytes()).hexdigest();assert path.read_bytes()==(p/'first-pass'/path.name).read_bytes();a['traces_preserve_exact_endpoint']=True
pairs=[]
for source in (3,5):
 x=json.loads((p/f'arm-{source}-policy-0.json').read_text());y=json.loads((p/f'arm-{source}-policy-1.json').read_text());y['origin']['water_receipt_policy']=0
 pairs.append({'source':source,'exact_except_policy':x==y,'water_cells_changed':sum(a!=b for a,b in zip(x['water'],y['water'])),'vapor_cells_changed':sum(a!=b for a,b in zip(x['vapor'],y['vapor'])),'cohorts_exact':all(a.get('sparse',[])==b.get('sparse',[]) for a,b in zip(x['origin']['cells'],y['origin']['cells'])),'stats_exact':x['origin']['stats']==y['origin']['stats']})
print(json.dumps({'trial_ticks':10,'tick_seconds':1440,'continuation_events_excluded':True,'arms':arms,'pairs':pairs},indent=2))
