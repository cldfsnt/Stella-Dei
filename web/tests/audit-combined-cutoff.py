from pathlib import Path
import json,collections,gzip,math
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/combined-day21';old=r.parent/'site-tmp/combined-strategy';out={}
for seed in(42,1337):
 for kind in('ordinary','pioneer'):
  arm=f'{seed}-{kind}';rows=collections.defaultdict(list);started=False
  for line in(b/(arm+'.log')).read_text().splitlines():
   if line.startswith('START '):started=True
   if not started:continue
   try:tag,v=line.split(' ',1);v=json.loads(v)
   except(ValueError,json.JSONDecodeError):continue
   rows[tag].append(v)
  births={x['cohort']['lineage']:x for x in rows['BIRTH']};wind={x['receipt']['lineage']for x in rows['WIND_PACKET']if x['receipt']['arrived']};losses=rows['LOSS'];initial=json.load(open(old/(arm+'-day7.json')));end=json.load(open(b/(arm+'-day21.json')))
  assert len(losses)==end['origin']['stats']['failed_patches']-initial['origin']['stats']['failed_patches']
  # Conservative lower bound from upkeep<=.1344/day; mortality+exposure<=7.99/day.
  # Use much looser .86B rather than exp(-7.99/60)*(1-.1344/60)≈.8733,
  # leaving >.004B margin versus the still-conservative linear exp bound .86489.
  # At .001-scale f32 rounding is many orders smaller. No actual residual claimed.
  groups={}
  for group,pred in [('all',lambda x:True),('new_wind',lambda x:x['cohort']['lineage']in births and x['cohort']['lineage']in wind),('new_nonwind',lambda x:x['cohort']['lineage']in births and x['cohort']['lineage']not in wind)]:
   ls=[x for x in losses if pred(x)];early=[x for x in ls if x['cohort']['lineage']in births and x['tick']-births[x['cohort']['lineage']]['tick']<=60]
   groups[group]={'losses':len(ls),'within_1day':len(early),'last_live_B_min':min((x['cohort']['biomass']for x in ls),default=None),'last_live_B_max':max((x['cohort']['biomass']for x in ls),default=None),'last_live_B_sum':sum(x['cohort']['biomass']for x in ls),'lower_bound_residual_sum':sum(.86*x['cohort']['biomass']for x in ls),'minimum_retained_first_cleanup_at_001':sum(.86*x['cohort']['biomass']>=.001 for x in ls),'early_minimum_retained_first_cleanup_at_001':sum(.86*x['cohort']['biomass']>=.001 for x in early),'last_live_below_001':sum(x['cohort']['biomass']<.001 for x in ls),'last_live_below_0025':sum(x['cohort']['biomass']<.0025 for x in ls)}
  modes=collections.Counter('wind004'if id in wind else 'nonwind004'if abs(x['cohort']['biomass']-.004)<1e-6 else 'nonwind010'if abs(x['cohort']['biomass']-.01)<1e-6 else 'other'for id,x in births.items())
  out[arm]={'groups':groups,'birth_sizes':dict(modes),'new_births':len(births),'observed_living_at21':sum(v['value']['biomass']>0 for c in end['origin']['cells']for v in c['sparse']),'observed_slots':4*len(end['origin']['cells']),'age_hours_wind_loss':[.4*(x['tick']-births[x['cohort']['lineage']]['tick'])for x in losses if x['cohort']['lineage']in wind and x['cohort']['lineage']in births]}
  print(arm,json.dumps(out[arm]['groups']),dict(modes))
p=r/'web/tests/continuation-review/combined-origin-acceptance/cutoff-audit';(p/'results.json').write_text(json.dumps(out,indent=2)+'\n')
