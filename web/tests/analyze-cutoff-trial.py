from pathlib import Path
import json,collections,hashlib,struct,math
from fractions import Fraction as F
f=lambda x:struct.unpack("f",struct.pack("f",x))[0]
r=Path(__file__).resolve().parents[2];base=r.parent/'site-tmp/cutoff-trial';old=r.parent/'site-tmp/combined-strategy'
def alive(s):return {v['value']['lineage']:(i,v['value'])for i,c in enumerate(s['origin']['cells'])for v in c['sparse']if v['value']['biomass']>0}
results={}
for seed in (42,1337):
 for mode in ('legacy','small'):
  kind='pioneer';b=base/mode;arm=f'{seed}-{kind}';initial=json.load(open(old/f'{arm}-day7.json'));end=json.load(open(b/f'{arm}-day14.json'))['state'];a=alive(initial);z=alive(end);rows=collections.defaultdict(list);started=False
  for line in (b/f'{arm}.log').read_text().splitlines():
   if line.startswith('START '):started=True
   if not started:continue
   try:t,v=line.split(' ',1);v=json.loads(v)
   except(ValueError,json.JSONDecodeError):continue
   rows[t].append(v)
  births=rows['BIRTH'];losses=rows['LOSS'];assert len(z)==len(a)+len(births)-len(losses)
  assert len(births)==end['origin']['stats']['births']-initial['origin']['stats']['births']
  packets=rows['WIND_PACKET'];arrivals=[x for x in packets if x['receipt']['arrived']];loss={x['cohort']['lineage']:x['tick']for x in losses};born={x['cohort']['lineage']:x for x in births};roots=[x for x in births if x['cohort']['root_fraction']>0]
  for x in packets:
   q=x['receipt'];assert q['carbon_residual']>=0 and q['carbon_residual']<=q['carbon_bound'];assert q['nitrogen_residual']>=0 and q['nitrogen_residual']<=q['nitrogen_bound']
  area=f(4*math.pi*(end['radius']*1000)**2/len(end['water']));conversion=f(1000/area)
  def detail(i,c):
   height=min(.5,.2*c['support_mass']*(1-c['root_fraction'])/(max(0,c['biomass']-c['support_mass'])+.01)*(1+.6*(1-c['efficiency'])-.3*c['structure']))
   return {'cell':i,'cohort':c,'soil':end['beta_origin']['soil'][i],'temperature':end['temperature'][i],'depth_m':f(end['water'][i]*conversion)*1000,'architecture_m_approx':height,'basal_height_m_approx':max(height,c['biomass']/100),'root_tissue':c['support_mass']*c['root_fraction']}

  rooted=[detail(i,c)for i,c in z.values()if c['root_fraction']>0]
  ancestors={id:c['parent']for id,(i,c)in a.items()};ancestors.update({x['cohort']['lineage']:x['cohort']['parent']for x in births})
  def desc(id,ancestor):
   seen=set()
   while id in ancestors and id not in seen:
    if id==ancestor:return True
    seen.add(id);id=ancestors[id]
   return id==ancestor
  lineage_foci={str(id):{'alive':id in z,'death_tick':loss.get(id),'living_descendants':[x for x in z if x!=id and desc(x,id)]}for id in ({"42-ordinary":(421,),"1337-ordinary":(125,),"1337-pioneer":(95,97)}.get(arm,()))if id in a}
  traits={id:c for id,(i,c)in a.items()};worldseed=initial['seed']
  for x in births:
   c=x['cohort'];i=c['lineage'];parent=traits[c['parent']];d=bytearray(44);d[:12]=b'STELLA-ROOT1';d[16:24]=worldseed.to_bytes(8,'little');d[24:32]=c['parent'].to_bytes(8,'little');d[32:40]=i.to_bytes(8,'little');d[40:44]=c['generation'].to_bytes(4,'little');h=hashlib.sha256(d).digest();step=(1/32 if h[1]&1==0 else -1/32)if h[0]&63==0 else 0;assert c['root_fraction']==f(min(1,max(0,f(parent.get('root_fraction',0)+step))))
   expected=0.
   if kind=='pioneer':
    d=b''.join(v.to_bytes(8,'little')for v in(worldseed,i,c['parent'],0x57494e4447454e31^c['generation']));u=(int.from_bytes(hashlib.sha256(d).digest()[:8],'little')>>11)/9007199254740992;expected=f(min(1,max(0,parent.get('aerial_allocation',0)+(u-.5)*.2)))
   assert c.get('aerial_allocation',0)==expected;traits[i]=c
  def carbon(c):return sum((F(x['biomass'])for x in c['cohorts']),F(c['detritus']))
  def nitrogen(c):return sum((F(x['biomass'])for x in c['cohorts']),F(0))*F(f(.1))+F(c['nutrient'])
  for x in rows['WIND_ENDPOINT']:
   db,da,tb,ta=[x[k]for k in('before_donor','after_donor','before_target','after_target')];ce=(carbon(db)+carbon(tb)-carbon(da)-carbon(ta))*F(x['area']);ne=(nitrogen(db)+nitrogen(tb)-nitrogen(da)-nitrogen(ta))*F(x['area']);assert 0<=ce<=F(x['receipt']['carbon_bound'])and 0<=ne<=F(x['receipt']['nitrogen_bound'])
  assert len(rows['WIND_ENDPOINT'])==len(packets)
  for x in rows['ROOT_WATER']:assert F(x['credit'])+F(x['bare_credit'])<=F(x['soil_before'])-F(x['soil_after'])
  for x in rows['USED_H']:assert x['owner']==x['lineage']and F(x['h'])*F(max(x['entry_demand'],x['current_demand']))<=F(x['credit'])
  r1={'initial_living':len(a),'final_living':len(z),'births':len(births),'losses':len(losses),'initial_survivors':len(set(a)&set(z)),'daily':rows['DAY'],'root_births':roots,'rooted_endpoint':rooted,'lineage_foci':lineage_foci,'opportunities':len(rows['WIND_OPPORTUNITY']),'outcomes':dict(collections.Counter(x['outcome']for x in rows['WIND_OPPORTUNITY'])),'paid_packets':len(packets),'arrivals':len(arrivals),'arrivals_alive':sum(x['receipt']['lineage']in z for x in arrivals),'descendant_donors':sorted({x['parent']for x in packets if (a.get(x['parent'],(None,{}))[1].get('generation',0)>0 or x['parent']in born)}),'root_physical_credits':sum(x['credit']for x in rows['ROOT_WATER']),'positive_consumption_rows':len(rows['USED_H']),'positive_consumption_ids':sorted({x['lineage']for x in rows['USED_H']}),'arrival_fates':[{'id':x['receipt']['lineage'],'parent':x['parent'],'time':x['time'],'cell':x['to'],'distance_km':x['route']['distance_km'],'alive':x['receipt']['lineage']in z,'loss_tick':loss.get(x['receipt']['lineage'])}for x in arrivals]}
  r1['world_flux_deltas']={k:end['origin']['stats'][k]-v for k,v in initial['origin']['stats'].items()if isinstance(v,(float,int))};r1['initial_occupied']=len({i for i,c in a.values()});r1['new_occupied_since_day7']=len({i for i,c in z.values()}-{i for i,c in a.values()});r1['lost_occupied_since_day7']=len({i for i,c in a.values()}-{i for i,c in z.values()});r1['cleanup_count']=len(rows['CLEANUP']);r1['cleanup_remaining_sum']=sum(x['after_mortality']['biomass']for x in rows['CLEANUP']);r1['cleanup_remaining_range']=[min((x['after_mortality']['biomass']for x in rows['CLEANUP']),default=0),max((x['after_mortality']['biomass']for x in rows['CLEANUP']),default=0)];r1['cleanup_continuous_dead_sum']=sum(x['continuous_dead']for x in rows['CLEANUP']);r1['weak_day14']=sum(c['biomass']<.0025 for i,c in z.values());r1['weak_supported_day14']=sum(c['biomass']<.0025 and c['support_mass']>0 for i,c in z.values());r1['births_surviving']=sum(x['cohort']['lineage']in z for x in births);r1['cleanup_early_day']=sum(x['lineage']in born and x['tick']-born[x['lineage']]['tick']<=60 for x in rows['CLEANUP']);results[f'{seed}-{mode}']=r1
  print(seed,mode,json.dumps({k:v for k,v in r1.items()if k not in ['daily','root_births','rooted_endpoint','arrival_fates']}),flush=True)
(base/'results.json').write_text(json.dumps(results,indent=2))
