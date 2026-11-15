#!/usr/bin/env python3
"""Reproduce fixed warm day14→30 summary from immutable native observations."""
import json,sys
from pathlib import Path
p=Path(sys.argv[1]);lines=p.read_text().splitlines();days=[json.loads(x.split(' ',1)[1])for x in lines if x.startswith('WARM30_DAY ')];patches=[json.loads(x.split(' ',1)[1])for x in lines if x.startswith('WARM30_PATCH ')]
last={};recolon=[]
for row in patches:
 prior=last.get(row['patch'])
 if prior and prior['extinctions']>0 and row['recoveries']>prior['recoveries']:recolon.append({'patch':row['patch'],'day':row['day'],'cover':row['after']})
 last[row['patch']]=row
summary={'days':days,'patch_records':len(patches),'confirmed_recolonizations_after_observed_local_extinction':recolon,'peak_rabbits':max(x['peak_rabbits']for x in days),'endpoint_cover_rebound_from_previous_day_fraction':days[-1]['cover']/days[-2]['cover']-1,'feeding_undercredit_fraction':days[-1]['credit_error_abs']/(150*days[-1]['removed']),'day29_grazed':sum(x['grazed']for x in patches if x['day']==29),'day30_grazed':sum(x['grazed']for x in patches if x['day']==30),'gate_pass':any(x.startswith('WARM30_PASS')for x in lines)}
print(json.dumps(summary,indent=2))
