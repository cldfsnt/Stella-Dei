from pathlib import Path
import re,json,statistics
r=Path(__file__).resolve().parent;rows=[]
for p in sorted(r.glob('*-[123]-*.log')):
 stem=p.stem.split('-');width=int(stem[0]);world=stem[1];repeat=int(stem[2]);kind=stem[3]
 for line in p.read_text().splitlines():
  if not line.startswith('FRAME_SUMMARY'):continue
  row={'width':width,'world':world,'repeat':repeat,'kind':kind}
  for k in ['requested_hps','update_mean_ms','render_finish_mean_ms','total_mean_ms','total_p95_ms','total_max_ms']:row[k]=float(re.search(k+r'=([0-9.]+)',line)[1])
  rows.append(row)
(r/'summary.json').write_text(json.dumps(rows,indent=2))
for width in [390,1366]:
 for world in ['early','established30d']:
  for pace in [0,6,24]:
   row=[width,world,pace]
   for kind in ['base','branch']:
    subset=[x for x in rows if x['width']==width and x['world']==world and x['kind']==kind and x['requested_hps']==pace]
    row.extend([statistics.median(x[k] for x in subset) for k in ['render_finish_mean_ms','total_mean_ms']])
   print(*row)
