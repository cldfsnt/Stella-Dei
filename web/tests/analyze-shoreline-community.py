from pathlib import Path
import json,sys
base=Path(sys.argv[1]);result={}
def cohorts(save,index):return [x['value'] for x in save['origin']['cells'][index]['sparse'] if x['value']['biomass']>0]
def living(save):return {c['lineage']:(i,c)for i in range(len(save['origin']['cells']))for c in cohorts(save,i)}
for law,folder in [(1,'origin-shoreline'),(2,'origin-basal-shoreline'),(3,'origin-final-demand-shoreline')]:
 p=base/folder;before=json.loads((p/'depth-3-arm-0-0.json').read_text());after=json.loads((p/'depth-3-arm-0-60.json').read_text());lines=(p/'main-3-0.log').read_text().splitlines();patch=[json.loads(l[6:])for l in lines if l.startswith('PATCH ')];births=[json.loads(l[6:])for l in lines if l.startswith('BIRTH ')];assert len(patch)==60
 start=cohorts(before,18327);end=cohorts(after,18327);seen={c['lineage']:c for c in start};last={c['lineage']:{'tick':0,'cohort':c}for c in start};first={c['lineage']:0 for c in start};events=[];prev={c['lineage'] for c in start};trace=[]
 for row in patch:
  live=[c for c in row['cohorts']if c['biomass']>0];ids={c['lineage']for c in live};arrive=ids-prev;depart=prev-ids
  if arrive or depart:events.append({'tick':row['tick'],'arrivals':sorted(arrive),'departures':sorted(depart)})
  for c in live:seen[c['lineage']]=c;last[c['lineage']]={'tick':row['tick'],'cohort':c};first.setdefault(c['lineage'],row['tick'])
  trace.append({'tick':row['tick'],'count':len(live),'biomass':sum(c['biomass']for c in live),'depth_m':row['depth_m'],'temperature':row['temperature']});prev=ids
 world0=living(before);world1=living(after);b0=before['origin']['stats']['births'];b1=after['origin']['stats']['births'];assert b1-b0==len(births)
 local_new=[b for b in births if b['child']['lineage']in first and first[b['child']['lineage']]>0];local_parent=[b for b in births if b['child']['parent']in first]
 details=[]
 for ident in first:
  initial=next((c for c in start if c['lineage']==ident),None);lastc=last[ident]['cohort'];baseline=initial or next((b['child']for b in births if b['child']['lineage']==ident),None)
  details.append({'lineage':ident,'first_tick':first[ident],'last_tick':last[ident]['tick'],'initial':initial,'last':lastc,'endpoint_location':world1[ident][0]if ident in world1 else None,'observed_grazed_increment':lastc['lifetime_grazed']-baseline['lifetime_grazed']if baseline else None})
 result[law]={'initial_count':len(start),'end_count':len(end),'initial_biomass':sum(c['biomass']for c in start),'end_biomass':sum(c['biomass']for c in end),'min_biomass':min(x['biomass']for x in trace),'max_biomass':max(x['biomass']for x in trace),'events':events,'lineages':details,'local_new_birth_records':local_new,'births_parent_observed_here':local_parent,'patch_trace':trace,'initial_cell':before['origin']['cells'][18327],'end_cell':after['origin']['cells'][18327],'world':{'initial_living':len(world0),'end_living':len(world1),'paid_births':b1-b0,'implied_identity_losses':len(world0)+(b1-b0)-len(world1),'stats_delta':{k:after['origin']['stats'][k]-v for k,v in before['origin']['stats'].items()}}}
print(json.dumps(result,indent=2))
