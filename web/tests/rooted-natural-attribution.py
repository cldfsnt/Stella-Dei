from pathlib import Path
import json,csv,io
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/rooted-natural';summaries=[]
for arm in range(2):
 ls=(b/f'main-{arm}.log').read_text().splitlines();rows=lambda t:[json.loads(l.split(' ',1)[1])for l in ls if l.startswith(t+' ')]
 u={x['tick']:x for x in rows('USED_H')if x['stage']=='mortality'};g={x['tick']:x for x in rows('PAID_GROWTH')};out=[]
 for m in rows('MORTALITY'):
  x=u[m['tick']];out.append(dict(tick=m['tick'],end_hours=m['tick']*.4,temperature_K=x['temperature'],depth_m=x['depth_km']*1000,light=x['light'],fitness=max(0,1-abs(x['temperature']-303)/40),root_fraction=m['cohort']['root_fraction'],support=m['cohort']['support_mass'],raw_h=x['h'],effective_h=m['hydrated'],immersion=m['immersion'],exposed=m['exposed'],mortality_rate=m['mortality'],extra_exposure_rate=3*m['exposed']*(1-m['hydrated']),dead=m['dead'],upkeep=m['upkeep'],paid_growth=g.get(m['tick'],{}).get('actual_carbon',0)))
 with(b/f'attribution-{arm}.csv').open('w')as f:w=csv.DictWriter(f,fieldnames=out[0].keys());w.writeheader();w.writerows(out)
 cold=[x for x in out if x['temperature_K']<=273.15];night=[x for x in out if x['light']==0]
 summaries.append(dict(arm=arm,cold_intervals=[{'tick':x['tick'],'hours':[x['end_hours']-.4,x['end_hours']],'T':x['temperature_K'],'depth_m':x['depth_m'],'immersion':x['immersion'],'effective_h':x['effective_h'],'mortality_rate':x['mortality_rate'],'extra_exposure_rate':x['extra_exposure_rate'],'dead':x['dead']}for x in cold],cold_death=sum(x['dead']for x in cold),all_death=sum(x['dead']for x in out),night_ticks=len(night),night_death=sum(x['dead']for x in night),no_growth_ticks=sum(x['paid_growth']==0 for x in out),positive_growth_ticks=sum(x['paid_growth']>0 for x in out),all_root_fraction_half=all(x['root_fraction']==.5 for x in out),extra_exposure_positive_ticks=sum(x['extra_exposure_rate']>0 for x in out),extra_exposure_rate_max=max(x['extra_exposure_rate']for x in out)))
(b/'attribution.json').write_text(json.dumps(summaries,indent=2));print(json.dumps(summaries,indent=2))
