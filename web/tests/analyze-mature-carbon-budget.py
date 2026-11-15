#!/usr/bin/env python3
import json,sys
from pathlib import Path
lines=Path(sys.argv[1]).read_text().splitlines();before={0:[],1:[]};after={0:[],1:[]};temps={0:[],1:[]};arm=None
for l in lines:
 if l.startswith('TERRESTRIAL_BEFORE '):
  x=json.loads(l.split(' ',1)[1]);arm=x['arm'];before[arm].append(x)
 if l.startswith('TERRESTRIAL_AFTER '):
  x=json.loads(l.split(' ',1)[1]);after[x['arm']].append(x)
 if arm is not None and l.startswith('TERRESTRIAL_COLUMN '):temps[arm].append(json.loads(l.split(' ',1)[1])['temperature'])
 if l.startswith('TERRESTRIAL_ARM_PASS'):arm=None
out=[]
for arm in [0,1]:
 b=before[arm];a=after[arm];assert len(b)==len(a)==len(temps[arm])==60
 start=b[0]['cohort'];end=a[-1]['cohort'];credit=end['reproduction_credit']-start['reproduction_credit'];decline=start['biomass']-end['biomass'];upkeep=sum(x['cohort']['support_mass']*.12*(1+.4*max(0,x['cohort']['efficiency']-1))/60 for x in b)
 out.append(dict(arm=arm,credit_increase=credit,biomass_decline=decline,inferred_gross_loss=credit+decline,potential_upkeep_upper=upkeep,upkeep_fraction_of_inferred_loss=upkeep/(credit+decline),grazed_history_increase=end['lifetime_grazed']-start['lifetime_grazed'],credit_decrease_ticks=sum(y['cohort']['reproduction_credit']<x['cohort']['reproduction_credit']for x,y in zip(b,a)),positive_credit_ticks=sum(y['cohort']['reproduction_credit']>x['cohort']['reproduction_credit']for x,y in zip(b,a)),first_two_credit_increments=[y['cohort']['reproduction_credit']-x['cohort']['reproduction_credit']for x,y in zip(b[:2],a[:2])],min_temperature=min(temps[arm]),max_temperature=max(temps[arm]),thermal_fitness_range=[min(max(0,1-abs(t-start['optimum'])/40)for t in temps[arm]),max(max(0,1-abs(t-start['optimum'])/40)for t in temps[arm])]))
print(json.dumps({'units':'carbon kgC/m²; temperature K; credit-derived flux is an inference subject to bounded f32 counter rounding, not logged Flux.fixed','arms':out},indent=2))
