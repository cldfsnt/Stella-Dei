#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,sys
p=Path(sys.argv[1]);records=[];runs=[];inputs=[];endpoints=[]
for f in sorted(p.glob('seed-*.log')):
 ls=f.read_text().splitlines();records += [json.loads(x.split(' ',1)[1])for x in ls if x.startswith('FORAGING_DAY ')];runs.append(dict(path=str(f),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),gates=[x for x in ls if x.startswith(('FORAGING_SETUP','FORAGING_ARM_PASS','FORAGING_PASS'))]))
for f in sorted(p.glob('input-*.json')):
 s=json.loads(f.read_text());ids=[i for i,v in enumerate(s['vegetation'])if v>0];inputs.append(dict(path=str(f),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),generated_seed=s['seed'],painted_ids=ids,cover_sum=sum(s['vegetation']),painted_temperature=[min(s['temperature'][i]for i in ids),max(s['temperature'][i]for i in ids)],painted_water_native=[min(s['water'][i]for i in ids),max(s['water'][i]for i in ids)],rabbits=len(s['rabbits'])))
for f in sorted(p.glob('end-*.json')):endpoints.append(dict(path=str(f),sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
print(json.dumps(dict(records=records,endpoints=[d for d in records if d['day']==14],runs=runs,inputs=inputs,snapshot_hashes=endpoints,interpretation=['Actual19brush taps paint37cells; original19patch assumption failed, not retroactively preregistered.','Seed42cold climate confounds grazing outcomes; all runs retained.','Raw meal counts now count small feeding events and are timestep-sensitive, not comparable meal-size totals.','No exact total ecosystem carbon conservation claim: existing Sandbox cover/satiety model.']),indent=2))
