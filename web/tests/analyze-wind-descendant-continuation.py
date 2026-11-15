from pathlib import Path
import json,hashlib,collections,struct
from fractions import Fraction as F
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/wind-descendant-continuation'
# Reuse the already independent exact binary-rational receipt oracle, unchanged.
ns={};exec((r/'web/tests/analyze-wind-bulk.py').read_text().split("for arm in ['ordinary','pioneer']:")[0].replace('b=Path(sys.argv[1]);out={}','out={}'),ns);audit=ns['audit'];f=ns['f']
def rows(path):
 for line in path.open():
  if ' {'not in line:continue
  tag,raw=line.split(' ',1)
  try:yield tag,json.loads(raw)
  except json.JSONDecodeError:pass
prior=json.loads((r.parent/'site-tmp/wind-bulk/results.json').read_text());out={}
for arm in ['ordinary','pioneer']:
 history={};cur={};prev={};packets=[];opps=[];ticks=[];checks=[];trace=[];resume_trace=[];arrivals={p['id']for p in prior[arm]['packet_fates']};oldarrivals=set(arrivals);newids=set();lost=[];initial=None;tick=0
 for tag,x in rows(b/(arm+'.log')):
  if initial is None and tag!='INITIAL':continue # Exclude the separate two-tick observer-parity preflight before restored INITIAL.
  if tick==0 and tag.startswith('WIND_'):continue # Observer-parity preflight occurs after INITIAL but before the first TICK_START.
  if tag=='INITIAL':initial=x;births=x['stats']['births']
  elif tag=='INITIAL_COHORT':history[x['cohort']['lineage']]=x;prev[x['cohort']['lineage']]=x
  elif tag=='TICK_START':tick=x['tick'];cur={}
  elif tag=='COHORT':cur[x['cohort']['lineage']]=x
  elif tag=='WIND_OPPORTUNITY':opps.append(dict(x,tick=tick))
  elif tag=='WIND_PACKET':
   pc=history[x['parent']]['cohort'];kind='founder'if pc['parent']==0 else'wind_born_descendant'if pc['lineage']in arrivals else'local_born_descendant';packets.append(dict(x,tick=tick,donor_kind=kind,donor_generation=pc['generation']))
   if x['receipt']['arrived']:arrivals.add(x['receipt']['lineage'])
  elif tag=='WIND_ENDPOINT':
   ce,ne=audit(x);checks.append({'event':x['event'],'C_error':str(ce),'N_error':str(ne),'target_occupied_before':sum(c['biomass']>0 for c in x['before_target']['cohorts']),'outcome':x['receipt']['outcome']})
  elif tag=='TICK':
   born=cur.keys()-prev.keys();assert len(born)==x['births']-births,(arm,tick,'birth reconciliation');births=x['births']
   for i in born:
    c=cur[i]['cohort'];pc=history[c['parent']]['cohort'];domain=0x57494e4447454e31 ^ c['generation'];data=b''.join(int(v).to_bytes(8,'little')for v in [initial['config']['stream_seed'],i,c['parent'],domain]);u=(int.from_bytes(hashlib.sha256(data).digest()[:8],'little')>>11)/9007199254740992;expected=float(f(min(1,max(0,pc.get('aerial_allocation',0)+(u-.5)*.2))));assert expected==float(f(c.get('aerial_allocation',0))),(arm,i,'inheritance');history[i]=cur[i];newids.add(i)
   for i in prev.keys()-cur.keys():lost.append({'id':i,'tick':tick,'wind_born':i in arrivals,'last':prev[i]})
   ticks.append(x);prev=cur
  if tick>90 and tag in ['TICK_START','COHORT','WIND_OPPORTUNITY','WIND_PACKET','WIND_ENDPOINT','TICK']:trace.append((tag,x))
 for tag,x in rows(b/(arm+'-resume.log')):
  if tag in ['TICK_START','COHORT','WIND_OPPORTUNITY','WIND_PACKET','WIND_ENDPOINT','TICK']:resume_trace.append((tag,x))
 assert trace==resume_trace,(arm,'restart trace');assert(b/(arm+'-day10.json')).read_bytes()==(b/(arm+'-resume-day10.json')).read_bytes();assert len(ticks)==180 and len(checks)==len(packets);assert len({x['event']for x in opps})==len(opps)
 descendants=[x for x in cur.values()if x['cohort']['parent']>0];dpack=[p for p in packets if p['donor_kind']!='founder'];new_arrivals=arrivals-oldarrivals
 out[arm]={'initial':initial,'endpoint':ticks[-1],'births':len(newids),'lost':len(lost),'wind_opportunities':len(opps),'paid_packets':len(packets),'outcomes':dict(collections.Counter(x['outcome']for x in opps)),'donor_kind_packets':dict(collections.Counter(x['donor_kind']for x in packets)),'distinct_donor_ids':len({x['parent']for x in packets}),'descendant_packets':dpack,'new_wind_arrivals':len(new_arrivals),'new_wind_survivors':len(new_arrivals&cur.keys()),'descendants_alive':len(descendants),'ready_descendants':sum(x['cohort']['biomass']>=float(f(.02)) and x['cohort']['reproduction_credit']>=float(f(.01)) and x['cohort'].get('aerial_allocation',0)>0 for x in descendants),'max_generation':max(x['cohort']['generation']for x in cur.values()),'competition':dict(collections.Counter(str(x['target_occupied_before'])+' occupied/'+x['outcome']for x in checks)),'C_error':str(sum((F(x['C_error'])for x in checks),F(0))),'N_error':str(sum((F(x['N_error'])for x in checks),F(0))),'carbon_paid':sum(x['receipt']['carbon_paid']for x in packets),'nitrogen_paid':sum(x['receipt']['nitrogen_paid']for x in packets),'checks':checks,'losses':lost,'new_arrival_fates':[{'id':i,'alive':i in cur,'loss':next((l['tick']for l in lost if l['id']==i),None)}for i in sorted(new_arrivals)],'restart_endpoint_and_trace_exact':True,'inheritance_checked':len(newids)}
print(json.dumps(out,indent=2))
