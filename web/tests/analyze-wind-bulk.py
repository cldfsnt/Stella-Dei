from pathlib import Path
from fractions import Fraction as F
import json,struct,math,hashlib,collections,sys
b=Path(sys.argv[1]);out={}
def f(x):return F(struct.unpack('f',struct.pack('f',x))[0])
def carbon(c):return sum((f(x['biomass'])for x in c['cohorts']),F(0))+f(c['detritus'])
def nitrogen(c):return sum((f(x['biomass'])for x in c['cohorts']),F(0))*f(.1)+f(c['nutrient'])
def audit(r):
 area=F(r['area']);db,da,tb,ta=[r[k]for k in ['before_donor','after_donor','before_target','after_target']]
 ce=(carbon(db)+carbon(tb)-carbon(da)-carbon(ta))*area;ne=(nitrogen(db)+nitrogen(tb)-nitrogen(da)-nitrogen(ta))*area
 assert ce>=0 and ne>=0,(r['event'],ce,ne)
 assert ce<=F(r['receipt']['carbon_bound']) and ne<=F(r['receipt']['nitrogen_bound']),(r['event'],ce,ne)
 assert sum(f(c['reproduction_credit'])for c in da['cohorts'])<sum(f(c['reproduction_credit'])for c in db['cohorts'])
 return ce,ne
for arm in ['ordinary','pioneer']:
 founders={};prev={};cur={};history={};packets=[];opps=[];events=[];ticks=[];checks=[];new_total=lost_total=moves_total=0;last_births=0;tick=0
 for line in (b/(arm+'.log')).open():
  if ' {' not in line:continue
  tag,raw=line.split(' ',1)
  try:r=json.loads(raw)
  except json.JSONDecodeError:continue
  if tag=='FOUNDER' and r['success']:
   for c in r['after']['cohorts']:
    if c['biomass']>0:founders[c['lineage']]={'cell':r['cell'],'cohort':c};prev[c['lineage']]=founders[c['lineage']]
  elif tag=='TICK_START':tick=r['tick'];cur={}
  elif tag=='COHORT':cur[r['cohort']['lineage']]=r
  elif tag=='WIND_OPPORTUNITY':opps.append(dict(r,tick=tick))
  elif tag=='WIND_PACKET':packets.append(dict(r,tick=tick))
  elif tag=='WIND_ENDPOINT':
   ce,ne=audit(r);checks.append({'event':r['event'],'carbon_error':str(ce),'nitrogen_error':str(ne)});events.append(r)
  elif tag=='TICK':
   new=cur.keys()-prev.keys();lost=prev.keys()-cur.keys();moves=sum(cur[i]['cell']!=prev[i]['cell']for i in cur.keys()&prev.keys());assert len(new)==r['births']-last_births,(arm,tick,len(new),r['births'],last_births)
   for i in new:history[i]={'born_tick':tick,'first_cell':cur[i]['cell'],'cohort':cur[i]['cohort']}
   for i in lost:
    h=history.setdefault(i,{'founder':True});h['lost_tick']=tick;h['last_cell']=prev[i]['cell']
   new_total+=len(new);lost_total+=len(lost);moves_total+=moves;last_births=r['births'];prev=cur;ticks.append(dict(r,new=len(new),lost=len(lost),moves=moves))
 assert len(ticks)==420 and len(events)==len(packets)
 assert (b/(arm+'-day7.json')).read_bytes()==(b/('resume-'+arm+'-day7.json')).read_bytes()
 assert len({r['event']for r in opps})==len(opps)
 bins=[0,100,250,500,1000,2500,5000,float('inf')];dist=[]
 for lo,hi in zip(bins,bins[1:]):
  rr=[r for r in packets if lo<=r['route']['distance_km']<hi];live=[r for r in rr if r['receipt']['arrived']]
  dist.append({'lo':lo,'hi':hi if math.isfinite(hi)else None,'paid_packets':len(rr),'arrivals':len(live),'distance_received_carbon':sum(r['route']['distance_km']*r['receipt']['carbon_received']for r in live)})
 arrival_ids={r['receipt']['lineage']for r in packets if r['receipt']['arrived']};dest=collections.Counter(r['to']for r in packets if r['receipt']['arrived']);packetfates=[]
 for r in packets:
  if not r['receipt']['arrived']:continue
  i=r['receipt']['lineage'];packetfates.append({'id':i,'parent':r['parent'],'tick':r['tick'],'from':r['from'],'to':r['to'],'distance_km':r['route']['distance_km'],'survives_day7':i in cur,'history':history.get(i)})
 # Check aerial inheritance independently from the domain-separated SHA256 formula.
 bad=[]
 for i,h in history.items():
  if 'cohort'not in h:continue
  c=h['cohort'];parent=c['parent'];pc=founders.get(parent,history.get(parent,{})).get('cohort')
  if pc is None:bad.append((i,'missing_parent'));continue
  seed=15021278609987233951;domain=0x57494e4447454e31 ^ c['generation'];data=b''.join(x.to_bytes(8,'little')for x in [seed,i,parent,domain]);u=(int.from_bytes(hashlib.sha256(data).digest()[:8],'little')>>11)/9007199254740992
  expected=float(f(min(1,max(0,pc.get('aerial_allocation',0)+(u-.5)*.2))))
  if expected!=float(f(c.get('aerial_allocation',0))):bad.append((i,expected,c.get('aerial_allocation',0)))
 assert not bad,bad[:10]
 out[arm]={'founder_count':len(founders),'last_tick':ticks[-1],'births':new_total,'losses':lost_total,'moves':moves_total,'founders_alive':len(founders.keys()&cur.keys()),'wind_births':len(arrival_ids),'nonwind_births':new_total-len(arrival_ids),'paid_packets':len(packets),'opportunities':len(opps),'outcomes':dict(collections.Counter(r['outcome']for r in opps)),'wind_children_alive':len(arrival_ids&cur.keys()),'unique_wind_arrival_destinations':len(dest),'repeated_destination_pairs':sum(n*(n-1)//2 for n in dest.values()),'distance_bins':dist,'packet_fates':packetfates,'exact_receipt_audit':checks,'carbon_error_signed_sum':str(sum((F(x['carbon_error'])for x in checks),F(0))),'nitrogen_error_signed_sum':str(sum((F(x['nitrogen_error'])for x in checks),F(0))),'carbon_error_sumabs':str(sum((abs(F(x['carbon_error']))for x in checks),F(0))),'nitrogen_error_sumabs':str(sum((abs(F(x['nitrogen_error']))for x in checks),F(0))),'inheritance_checked':sum('cohort'in h for h in history.values()),'restart_exact':True,'daily':[r for r in ticks if r['tick']%60==0],'last_cohorts':list(cur.values())}
assert (b/'ordinary-preseed.json').read_bytes()==(b/'pioneer-preseed.json').read_bytes()
print(json.dumps(out,indent=2))
