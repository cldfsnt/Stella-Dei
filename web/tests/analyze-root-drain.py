"""Read-only fixed six-arm root/Water-minus analysis; no counterfactual reruns."""
from pathlib import Path
import json,hashlib,gzip
r=Path(__file__).resolve().parents[2];base=r.parent/'site-tmp/root-drain-qa';out=r/'web/tests/continuation-review/paid-hydration/soil-root-design/root-drain-results';out.mkdir(exist_ok=True)
summary=[];proof={'scope':'three fixed day61 endpoints x untouched/one Water-minus tap;420ticks;no model changes','artifacts':{}}
for label in ['root0','root25k1','root25k10']:
 p=base/(label+'.log');raw=p.read_bytes();(out/(p.name+'.gz')).write_bytes(gzip.compress(raw,mtime=0));proof['artifacts'][str(p)]={'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
 lines=raw.decode().splitlines();ticks=[json.loads(x.split(' ',1)[1])for x in lines if x.startswith('ROOT_DRAIN_TICK ')];fates=[json.loads(x.split(' ',1)[1])for x in lines if x.startswith('ROOT_DRAIN_FATE ')];actions=[json.loads(x.split(' ',1)[1])for x in lines if x.startswith('ROOT_DRAIN_ACTION ')]
 for action in [0,1]:
  rows=[x for x in ticks if x['action']==action];events=[x for x in fates if x['action']==action];assert [x['tick']for x in rows]==list(range(421));last=rows[-1]
  new=[x for x in events if x['event']=='first_observed_alive'];initial=[x for x in events if x['event']=='present_at_start'];lost=[x for x in events if x['event']=='no_longer_observed_alive'];paid=[x for x in rows if x['root']['receipt'] is not None and x['root']['receipt']['paid']>0]
  def founder(x):return next((c for c in x['target']['cohorts']if c['lineage']==478 and c['biomass']>0),None)
  daily=[{'tick':x['tick'],'founder':founder(x),'family_mass':x['family_mass'],'family_alive':x['family_alive'],'target_depth_m':x['target_depth_m'],'target_soil':x['target_soil'],'target_temperature':x['target_temperature']}for x in rows if x['tick']%60==0]
  endpoint=base/f'{label}-action-{action}.json';u=Path(str(endpoint)+'.uninterrupted.json');v=Path(str(endpoint)+'.restored.json');assert u.read_bytes()==v.read_bytes()
  for p in [endpoint,u,v]:proof['artifacts'][str(p)]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
  summary.append({'label':label,'action':action,'action_receipt':next(x for x in actions if x['action']==action),'initial_family':[{'id':x['cohort']['lineage'],'parent':x['cohort']['parent'],'root_fraction':x['cohort']['root_fraction'],'cell':x['cell']}for x in initial],'new_observed_descendants':len(new),'new_rooted_observed':sum(x['cohort']['root_fraction']>0 for x in new),'observed_disappearances':len(lost),'final_founder':founder(last),'final_family_mass':last['family_mass'],'final_family_alive':last['family_alive'],'paid_ticks':[x['tick']for x in paid],'paid_receipts':[{'tick':x['tick'],'root':x['root'],'column':x['column'],'depth_m':x['target_depth_m']}for x in paid],'total_paid':last['audit']['root_paid'],'total_credited':last['audit']['root_credited'],'vapor_receiver_signed':last['audit']['root_receiver_signed'],'vapor_receiver_absolute':last['audit']['root_receiver_absolute'],'receiver_loss_fraction_of_paid':-last['audit']['root_receiver_signed']/last['audit']['root_paid'] if last['audit']['root_paid']else 0,'first_postaction_20cm_tick':next((x['tick']for x in rows if x['tick']>0 and x['target_depth_m']>=.2),None),'min_depth':min(x['target_depth_m']for x in rows),'max_depth':max(x['target_depth_m']for x in rows),'min_temperature':min(x['target_temperature']for x in rows),'max_temperature':max(x['target_temperature']for x in rows),'daily':daily,'final_audit':last['audit'],'water_plus_removed_change':last['water_plus_removed']-rows[0]['water_plus_removed'],'true_restart_exact':True})
for action in [0,1]:
 a=json.loads((base/f'root25k1-action-{action}.json').read_text());b=json.loads((base/f'root25k10-action-{action}.json').read_text());a['origin']['root_config']['conductance']=10;assert a==b
proof['conductance_endpoints_equal_except_config']=True
for p in [r/'web/tests/egl-root-drain-qa.py',r/'web/tests/root-drain-trace-patch.py',base/'drain-provenance.json',base/'build.log',base/'export-audit.json']:
 proof['artifacts'][str(p)]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');(out/'provenance.json').write_text(json.dumps(proof,indent=2)+'\n')
print('PASS:2526 tick records, six endpoints and exact continuation; both conductance pairs equal except config')
