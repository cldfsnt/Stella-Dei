#!/usr/bin/env python3
import json,sys
from pathlib import Path
root=Path(sys.argv[1])
def records(mode,tag):return [json.loads(x[len(tag)+1:])for x in (root/mode/'run.log').read_text().splitlines()if x.startswith(tag+' ')]
b=records('baseline','TOUGH_DAY');c=records('candidate','TOUGH_DAY');be=records('baseline','TOUGH_ENDPOINT');ce=records('candidate','TOUGH_ENDPOINT')
assert b==[x for x in c if x['d']==0];assert be==[x for x in ce if x['d']==0]
summary={'exact_zero_trait_daily_records':len(b),'exact_zero_trait_full_old_field_rng_endpoints':len(be),'candidate_runs':len(ce),'candidate_days':c,'day14':[x for x in c if x['day']==14],'analytic_uniform_d05':{'maximum_satiety_per_day_at_cover1':.288/(1+2*.5)*(1/(1+.1))*150,'maintenance_satiety_per_day':86400*.00025,'maximum_sustainable_toughness_at_cover1_ignoring_reproduction':(.288*(1/1.1)/(.00025*86400/150)-1)/2},'maximum_actual_undercredit_fraction':max((x['credit_error_abs']/(x['removed']*150)if x['removed']else 0)for x in c)}
print(json.dumps(summary,indent=2))
