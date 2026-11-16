from pathlib import Path
import json,re,collections,gzip,hashlib,shutil
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/warm-dry-population';o=r/'web/tests/continuation-review/warm-dry-population'
def load(name):
 rows=collections.defaultdict(list);credit=collections.defaultdict(list)
 with(b/(name+'.log')).open()as f:
  for l in f:
   tag,_,body=l.strip().partition(' ')
   if tag=='ROOT_CREDIT':
    m=re.fullmatch(r'tick=(\d+) id=(\d+) kg_m2=(.*)',body);credit[int(m[2])].append([int(m[1]),float(m[3])]);continue
   try:x=json.loads(body)
   except(ValueError,TypeError):continue
   if isinstance(x,dict):rows[tag].append(x)
 return rows,credit
def exact_events(rows,start):
 return sorted([(tag,x)for tag,entries in rows.items()for x in entries if x.get('tick',0)>start],key=lambda z:json.dumps(z,sort_keys=True))
a,ac=load('candidate');z,zc=load('candidate-resume');assert exact_events(a,840)==exact_events(z,840),'restart event mismatch';assert {i:[v for v in vs if v[0]>840]for i,vs in ac.items()if any(v[0]>840 for v in vs)}==dict(zc)
def summary(name):
 rows,credit=load(name);end=json.loads((b/(name+'-final.json')).read_text());alive={v['value']['lineage']:{'point':p,**v['value']}for p,c in enumerate(end['origin']['cells'])for v in c['sparse']if v['value']['biomass']>0}
 # Depth comes from actual per-interval observations, not a guessed save field.
 births={x['cohort']['lineage']:x for x in rows['BIRTH_OR_INITIAL']};deaths={x['id']:x['tick']for x in rows['DEATH']}
 entries={(x['tick'],x['id']):x['data']for x in rows['POP_ENTRY']};per=collections.defaultdict(lambda:dict(upkeep=0.,mortality=0.,growth=0.,dry_growth=0.,film_growth=0.,aquatic_growth=0.,dry_ticks=0,film_ticks=0,aquatic_ticks=0,cleanup=None,max_h=0.))
 for (tick,i),e in entries.items():
  d=e['depth'];per[i]['dry_ticks'if d==0 else'film_ticks'if d<.0002 else'aquatic_ticks']+=1
 for tag,key,field in [('POP_UPKEEP','upkeep','paid'),('POP_MORTALITY','mortality','dead'),('POP_GROWTH','growth','growth')]:
  for x in rows[tag]:
   i=x['id'];v=x['data'];per[i][key]+=v[field]
   if tag=='POP_MORTALITY':
    per[i]['max_h']=max(per[i]['max_h'],v['h'])
    if v['cleanup']:per[i]['cleanup']={'tick':x['tick'],**v}
   if tag=='POP_GROWTH':
    e=entries.get((x['tick'],i));assert e is not None
    per[i]['dry_growth'if e['depth']==0 else'film_growth'if e['depth']<.0002 else'aquatic_growth']+=v['growth']
 funded=[]
 for i,cs in credit.items():
  children=[q for q,x in births.items()if x['cohort']['parent']==i]
  funded.append({'id':i,'birth':births.get(i),'death_tick':deaths.get(i),'alive_final':alive.get(i),'credit_count':len(cs),'credit_kg_m2':sum(c[1]for c in cs),'children_born':children,'children_alive_final':[q for q in children if q in alive],**per[i]})
 day=rows['DAILY'];assert day[-1]['living']==len(alive);assert len(alive)==7+day[-1]['stats']['births']-len(deaths)
 return {'habitat_daily':rows['HABITAT'],'daily':day,'births':len(births)-7,'deaths':len(deaths),'living':len(alive),'credited_lineages':len(funded),'credited_survivors':sum(x['alive_final']is not None for x in funded),'credited_direct_children':sum(len(x['children_born'])for x in funded),'credited_direct_children_alive':sum(len(x['children_alive_final'])for x in funded),'credited_lineage_details':funded,'root_trace_aggregate':{key:sum(v[key]for v in per.values())for key in ['upkeep','mortality','growth','dry_growth','film_growth','aquatic_growth','dry_ticks','film_ticks','aquatic_ticks']},'root_cleanup_count':sum(v['cleanup']is not None for v in per.values())}
out={n:summary(n)for n in ['control','candidate']};out['exact_restart_events']=True
(o/'results.json').write_text(json.dumps(out,indent=2)+'\n')
for n in ['control','candidate','candidate-resume','parity','parity-off']:
 with(b/(n+'.log')).open('rb')as src,gzip.GzipFile(filename=str(o/(n+'.log.gz')),mode='wb',mtime=0)as dst:shutil.copyfileobj(src,dst)
for name in ['source-hashes.json','source-changes.json','state-hashes.json','build.log','execution.log']:shutil.copy2(b/name,o/name)
with(b/'candidate-final.json').open('rb')as src,gzip.GzipFile(filename=str(o/'candidate-final.json.gz'),mode='wb',mtime=0)as dst:shutil.copyfileobj(src,dst)
print(json.dumps({n:{k:v for k,v in out[n].items()if k not in ['daily','habitat_daily','credited_lineage_details']}for n in ['control','candidate']},indent=2))
