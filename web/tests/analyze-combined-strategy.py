from pathlib import Path
from fractions import Fraction as F
import json,hashlib,struct,collections,math
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/combined-strategy';out={}
f=lambda x:struct.unpack('f',struct.pack('f',x))[0]
def carbon(c):return sum((F(x['biomass'])for x in c['cohorts']),F(c['detritus']))
def nitrogen(c):return sum((F(x['biomass'])for x in c['cohorts']),F(0))*F(f(.1))+F(c['nutrient'])
for seed in (42,1337):
 for kind in ('ordinary','pioneer'):
  name=f'{seed}-{kind}';initial=json.load(open(b/(name+'-initial.json')));worldseed=initial['seed'];founders={};allco={};prev={};cur={};history={};packets=[];opps=[];ticks=[];events=[];births=[];root_credit=0.;root_residual=F(0);usedpositive=set();tick=0;last_births=0;deaths=0;moves=0;started=False
  for line in(b/(name+'.log')).open():
   if not line.startswith(('FOUNDER ','TICK_START ','COHORT ','TICK ','WIND_PACKET ','WIND_OPPORTUNITY ','WIND_ENDPOINT ','ROOT_WATER ','USED_H ')):continue
   tag,raw=line.split(' ',1);x=json.loads(raw)
   if tag=='FOUNDER':
    if not x['success']:continue
    for c in x['after']['cohorts']:
     if c['biomass']>0:founders[c['lineage']]={'cell':x['cell'],'cohort':c};prev[c['lineage']]=founders[c['lineage']];allco[c['lineage']]=c
    continue
   if tag=='TICK_START':tick=x['tick'];started=True;cur={};continue
   if not started:continue
   if tag=='COHORT':cur[x['cohort']['lineage']]=x
   elif tag=='WIND_PACKET':packets.append(dict(x,tick=tick))
   elif tag=='WIND_OPPORTUNITY':opps.append(dict(x,tick=tick))
   elif tag=='WIND_ENDPOINT':
    db,da,tb,ta=[x[k]for k in ('before_donor','after_donor','before_target','after_target')];ce=(carbon(db)+carbon(tb)-carbon(da)-carbon(ta))*F(x['area']);ne=(nitrogen(db)+nitrogen(tb)-nitrogen(da)-nitrogen(ta))*F(x['area']);assert 0<=ce<=F(x['receipt']['carbon_bound']) and 0<=ne<=F(x['receipt']['nitrogen_bound']);events.append({'event':x['event'],'carbon_residual':str(ce),'nitrogen_residual':str(ne)})
   elif tag=='ROOT_WATER':
    debit=F(x['soil_before'])-F(x['soil_after']);assert F(x['credit'])+F(x['bare_credit'])<=debit;root_credit+=x['credit'];root_residual+=(F(x['vapor_after'])-F(x['vapor_before']))*10**9-debit*F(x['area'])
   elif tag=='USED_H':
    assert x['owner']==x['lineage'] and F(x['h'])*F(max(x['entry_demand'],x['current_demand']))<=F(x['credit'])
    if x['h']>0:usedpositive.add((tick,x['lineage']))
   elif tag=='TICK':
    new=cur.keys()-prev.keys();lost=prev.keys()-cur.keys();assert len(new)==x['births']-last_births,(name,tick);last_births=x['births'];deaths+=len(lost);moves+=sum(cur[i]['cell']!=prev[i]['cell']for i in cur.keys()&prev.keys())
    for i in sorted(new):
     c=cur[i]['cohort'];parent=allco[c['parent']];d=bytearray(44);d[:12]=b'STELLA-ROOT1';d[16:24]=worldseed.to_bytes(8,'little');d[24:32]=c['parent'].to_bytes(8,'little');d[32:40]=i.to_bytes(8,'little');d[40:44]=c['generation'].to_bytes(4,'little');h=hashlib.sha256(d).digest();step=(1/32 if h[1]&1==0 else -1/32)if h[0]&63==0 else 0;expected=f(min(1,max(0,f(parent.get('root_fraction',0)+step))));assert c['root_fraction']==expected,(name,i,'root')
     expected=0.
     if kind=='pioneer':
      d=b''.join(v.to_bytes(8,'little')for v in (worldseed,i,c['parent'],0x57494e4447454e31^c['generation']));u=(int.from_bytes(hashlib.sha256(d).digest()[:8],'little')>>11)/9007199254740992;expected=f(min(1,max(0,parent.get('aerial_allocation',0)+(u-.5)*.2)))
     assert c.get('aerial_allocation',0)==expected,(name,i,'aerial');allco[i]=c;history[i]={'born_tick':tick,'first_cell':cur[i]['cell'],'parent':c['parent'],'root_fraction':c['root_fraction'],'aerial_allocation':c.get('aerial_allocation',0)};births.append(dict(history[i],id=i))
    for i in lost:history.setdefault(i,{'founder':True})['lost_tick']=tick
    ticks.append(x);prev=cur
  assert len(ticks)==420 and len(events)==len(packets);assert len(opps)==len({x['event']for x in opps})==ticks[-1]['serial'];assert(b/(name+'-day7.json')).read_bytes()==(b/('resume-'+name+'-day7.json')).read_bytes()
  arr=[x for x in packets if x['receipt']['arrived']];arrivalids={x['receipt']['lineage']for x in arr};fates=[]
  for x in arr:
   i=x['receipt']['lineage'];h=history[i];fates.append(dict(id=i,parent=x['parent'],tick=x['tick'],distance_km=x['route']['distance_km'],alive_day7=i in cur,alive_1tick=None if x['tick']+1>420 else h.get('lost_tick',421)>x['tick']+1,alive_1day=None if x['tick']+60>420 else h.get('lost_tick',421)>x['tick']+60))
  geom=json.load(open(b/(name+'-geometry.json')));v=[x['data']for x in geom];norm=lambda z:math.sqrt(sum(q*q for q in z));n=[norm(z)for z in v]
  def dist(i,j):return 5000*math.acos(max(-1,min(1,sum(x*y for x,y in zip(v[i],v[j]))/n[i]/n[j])))
  initialcells={x['cell']for x in founders.values()};cells={x['cell']for x in cur.values()};newcells=cells-initialcells;dest=collections.Counter(x['to']for x in arr)
  out[name]={'worldseed':worldseed,'founders':len(founders),'founders_alive':len(founders.keys()&cur.keys()),'last':ticks[-1],'births':len(births),'deaths':deaths,'moves':moves,'opportunities':len(opps),'outcomes':dict(collections.Counter(x['outcome']for x in opps)),'paid_packets':len(packets),'arrivals':len(arr),'arrival_alive_day7':len(arrivalids&cur.keys()),'nonwind_births':len(births)-len(arr),'wind_releasing_founders':len({x['parent']for x in packets}&founders.keys()),'wind_releasing_descendants':len({x['parent']for x in packets}-founders.keys()),'root_positive_born':sum(x['root_fraction']>0 for x in births),'root_positive_alive':sum(x['cohort']['root_fraction']>0 for x in cur.values()),'root_credit':root_credit,'positive_root_h_lineage_ticks':len(usedpositive),'root_signed_residual_kg':str(root_residual),'new_occupied':len(newcells),'lost_founder_patches':len(initialcells-cells),'farthest_new_patch_from_nearest_founder_km':max((min(dist(i,j)for j in initialcells)for i in newcells),default=0),'unique_arrival_destinations':len(dest),'repeated_destination_pairs':sum(c*(c-1)//2 for c in dest.values()),'arrival_fates':fates,'packet_audit':events,'births_ledger':births,'daily':[x for x in ticks if x['tick']%60==0]}
(b/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:{a:v for a,v in x.items()if a not in ('arrival_fates','packet_audit','births_ledger','daily')}for k,x in out.items()},indent=2));print('ALL_FIXED_PAIRS_RESTART_MUTATION_PACKET_FUNDING_PASS')
