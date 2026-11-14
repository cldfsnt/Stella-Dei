from pathlib import Path
import re,json
for p in sorted(Path(__file__).parent.joinpath('results').glob('seed-*.log')):
 s=p.read_text();days=[]
 for m in re.finditer(r'PROPAGULE_DAY day=(\d+) grow_seconds=(\d+) occupied=(\d+) biomass=([\d.e+-]+) attempts=(\d+) arrivals=(\d+) tracked_colony_losses=(\d+)',s):
  vals=m.groups();days.append(dict(day=int(vals[0]),nominal_seconds=int(vals[1]),occupied=int(vals[2]),biomass=float(vals[3]),attempts=int(vals[4]),arrivals=int(vals[5]),losses=int(vals[6])))
 out={'seed':p.stem,'days_recorded':len(days),'first_spread':next((d for d in days if d['occupied']>1),None),'first_loss':next((d for d in days if d['losses']>0),None),'final':days[-1] if days else None}
 for label,pattern in [('forms',r'FORMS_DAY day=30 living=(\d+) counts=\{([^}]+)\}'),('performance',r'MOTILITY_WORLD[^\n]+'),('save',r'ORIGIN_SAVE[^\n]+')]:
  m=re.search(pattern,s);out[label]=m.group(0) if m else None
 print(json.dumps(out,indent=2))
