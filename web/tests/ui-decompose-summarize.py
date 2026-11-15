#!/usr/bin/env python3
from pathlib import Path
import re,json,statistics,gzip,hashlib
p=Path(__file__).parent/'continuation-review/ui-decomposition';rows=[];parity=[]
def read(name):
 f=p/name
 return f.read_text() if f.exists() else gzip.decompress(f.with_suffix('.log.gz').read_bytes()).decode()
for rep in range(1,4):
 a=re.findall(r'UI_SAVE (.*)',read(f'on-{rep}.log'));b=re.findall(r'UI_SAVE (.*)',read(f'off-{rep}.log'));assert len(a)==6 and a==b;parity+=a
 for arm in ('on','off'):
  parts=[];gl={}
  for line in read(f'{arm}-{rep}.log').splitlines():
   if line.startswith('UI_PART'):parts.append(float(re.search(r'sum_ms=(\S+)',line)[1])/60)
   if line.startswith('GL_CALLS'):gl=dict(re.findall(r'(\w+)=([^ ]+)',line))
   if line.startswith('FRAME_SUMMARY'):
    row=dict(re.findall(r'(\w+)=([^ ]+)',line));row.update(arm=arm,rep=rep,parts=parts[-5:],gl=gl);rows.append(row)
summary=[]
for stage in ('early','cached30d'):
 for rate in ('0','6','24'):
  for arm in ('on','off'):
   rr=[r for r in rows if r['stage']==stage and r['requested_hps']==rate and r['arm']==arm]
   summary.append(dict(stage=stage,target_hps=rate,arm=arm,total_ms=statistics.median(float(r['total_mean_ms']) for r in rr),render_finish_ms=statistics.median(float(r['render_finish_mean_ms']) for r in rr),parts_ms=[statistics.median(r['parts'][i] for r in rr) for i in range(5)],draws_per_frame=statistics.median(float(r['gl']['draws'])/60 for r in rr)))
(p/'summary.json').write_text(json.dumps({'exact_world_parity_pairs':18,'paired_hashes':parity,'median_rows':summary,'raw_rows':rows},indent=2)+'\n')
