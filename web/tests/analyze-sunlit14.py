#!/usr/bin/env python3
"""Read-only summary of fixed daily observations, not a causal intervention assay."""
from pathlib import Path
import json,sys
p=Path(sys.argv[1]);lines=(p/'first-run.log').read_text().splitlines();patches=[json.loads(x.split(' ',1)[1])for x in lines if x.startswith('PLAYABLE_PATCH ')];days=[]
for day in range(1,15):
 rows=[r for r in patches if r['day']==day];cs=[(r['cell'],c)for r in rows for c in r['patch']['cohorts']if c['biomass']>0];live={c['lineage']:(cell,c)for cell,c in cs};ds=next(json.loads(x.split(' ',1)[1])for x in lines if x.startswith('SUNLIT14_DAY ')and json.loads(x.split(' ',1)[1])['day']==day)
 days.append(dict(day=day,living=len(cs),occupied=len(rows),biomass_sum=sum(c['biomass']for _,c in cs),max_generation=max(c['generation']for _,c in cs),forms=ds['forms'],stats=ds['stats'],supported=ds['supported'],feeding_history=ds['feeding_history'],founder=live.get(1),depth_range_m=[min(r['depth']for r in rows),max(r['depth']for r in rows)],full_four_slot_patches=sum(sum(c['biomass']>0 for c in r['patch']['cohorts'])==4 for r in rows),living_parent_child_pairs=[dict(parent=c['parent'],child=c['lineage'],parent_cell=live[c['parent']][0],child_cell=cell)for cell,c in cs if c['parent']in live]))
print(json.dumps(dict(days=days,patches=patches,notes=['Daily snapshots omit within-day lifetimes.','forms order: mat,cushion,rosette,ribbon,branching,canopy','Integrated carbon counters kgC; biomass_sum sums density kgC/m2 across patches, not total kg.','Exposure and competition covary, not a causal trait effect.']),indent=2))
