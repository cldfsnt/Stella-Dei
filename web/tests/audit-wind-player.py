from pathlib import Path
from fractions import Fraction as F
import json,struct,sys,hashlib
b=Path(sys.argv[1]); out={}
def f32(x):return F(struct.unpack('f',struct.pack('f',x))[0])
def carbon(c):return sum((f32(x['biomass']) for x in c['cohorts']),F(0))+f32(c['detritus'])
def nitrogen(c):return sum((f32(x['biomass']) for x in c['cohorts']),F(0))*f32(.1)+f32(c['nutrient'])
for arm in ['ordinary','pioneer']:
 rows=[]
 for line in (b/(arm+'.log')).read_text().splitlines():
  if ' {' not in line:continue
  tag,raw=line.split(' ',1)
  try: rows.append((tag,json.loads(raw)))
  except json.JSONDecodeError:pass
 controls=[r for t,r in rows if t=='CONTROL_PACKET']; audit=[]
 for r in controls:
  sa,ta=map(F,r['areas']);db,da,tb,tA=[r[n]for n in ['before_donor','after_donor','before_target','after_target']]
  cp=(f32(db['cohorts'][0]['biomass'])-f32(da['cohorts'][0]['biomass']))*sa
  np=cp*f32(.1);cr=(carbon(tA)-carbon(tb))*ta;nr=(nitrogen(tA)-nitrogen(tb))*ta
  returned=(f32(da['detritus'])-f32(db['detritus']))*sa;returned_n=(f32(da['nutrient'])-f32(db['nutrient']))*sa
  ce=cp-cr-returned;ne=np-nr-returned_n
  assert cp>0 and cr>=0 and nr>=0 and ce>=0 and ne>=0,(r,ce,ne)
  assert ce<=F(r['receipt']['carbon_bound']) and ne<=F(r['receipt']['nitrogen_bound'])
  assert f32(da['cohorts'][0]['reproduction_credit'])<f32(db['cohorts'][0]['reproduction_credit'])
  audit.append({'areas':r['areas'],'occupied':r['occupied'],'viable':r['viable'],'carbon_error':str(ce),'nitrogen_error':str(ne)})
 ticks=[r for t,r in rows if t=='TICK'];packets=[r for t,r in rows if t=='WIND_PACKET'];opp=[r for t,r in rows if t=='WIND_OPPORTUNITY'];coh=[r for t,r in rows if t=='COHORT'];initial=json.loads((b/(arm+'-initial.json')).read_text());end=json.loads((b/(arm+'-day7.json')).read_text())
 assert len(ticks)==420
 assert (b/(arm+'-day7.json')).read_bytes()==(b/('resume-'+arm+'-day7.json')).read_bytes()
 outcomes={}
 for r in opp:outcomes[r['outcome']]=outcomes.get(r['outcome'],0)+1
 out[arm]={'founder':next(r for t,r in rows if t=='FOUNDER'),'first_tick':ticks[0],'last_tick':ticks[-1],'packet_count':len(packets),'opportunity_count':len(opp),'outcomes':outcomes,'all_opportunity_serials_unique':len({r['event']for r in opp})==len(opp),'control_exact_audit':audit,'first_newborn':next((r for r in coh if r['cohort']['lineage']>1),None),'last_cohorts':[r for r in coh if r['tick']==420],'restart_exact':True,'day7_sha256':hashlib.sha256((b/(arm+'-day7.json')).read_bytes()).hexdigest()}
print(json.dumps(out,indent=2))
