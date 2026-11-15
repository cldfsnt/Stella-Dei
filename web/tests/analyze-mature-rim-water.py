#!/usr/bin/env python3
"""Read-only exact dyadic local phase attribution from preserved trace, no rerun."""
import json,sys
from fractions import Fraction as F
from pathlib import Path
lines=Path(sys.argv[1]).read_text().splitlines();arm=None;prev={0:F(0),1:F(0)}
sums={i:{k:F(0)for k in ['between_columns_liquid_transport','column_net','condensed','standing_evaporated','represented_infiltration']}for i in [0,1]};first={};counts={0:0,1:0}
for line in lines:
 if line.startswith('TERRESTRIAL_BEFORE '):arm=json.loads(line.split(' ',1)[1])['arm']
 if line.startswith('TERRESTRIAL_ARM_PASS'):arm=None
 if arm is not None and line.startswith('TERRESTRIAL_COLUMN '):
  x=json.loads(line.split(' ',1)[1]);v=x['result'];a=sums[arm];b=F(x['before']['liquid']);end=F(v['state']['liquid']);a['between_columns_liquid_transport']+=b-prev[arm];a['column_net']+=end-b;a['condensed']+=F(v['condensed_native']);a['standing_evaporated']+=F(v['standing_evap_native']);a['represented_infiltration']+=F(v['stages'][2]['liquid'])-F(v['stages'][3]['liquid']);prev[arm]=end;first.setdefault(arm,x);counts[arm]+=1
for arm in [0,1]:
 assert counts[arm]==60
 assert sums[arm]['between_columns_liquid_transport']+sums[arm]['column_net']==prev[arm]
 assert first[arm]['before']['liquid']==0
print(json.dumps({'native_unit_kg':1e9,'sum_native':{i:{k:float(v)for k,v in a.items()}for i,a in sums.items()},'ending_native':{i:float(v)for i,v in prev.items()},'first_column':first,'scope':'Exact local represented-liquid stage telescoping, not global mass closure; isolated mature-soil model, not production weather prediction.'},indent=2))
