#!/usr/bin/env python3
"""No scheduler execution: reanalyse frozen rows, generate actual-helper probes."""
import gzip,json,pathlib,hashlib
P=pathlib.Path('web/tests/continuation-review/combined-origin-acceptance/two-seed-trial');O=P.parent/'root-bottleneck';O.mkdir(exist_ok=True)
result={}; probes=[]
for arm in ['42-ordinary','42-pioneer','1337-ordinary','1337-pioneer']:
 rows=[]
 with gzip.open(P/(arm+'.log.gz'),'rt') as f:
  for line in f:
   if line.startswith('USED_H '): rows.append(json.loads(line[7:]))
 if not rows:result[arm]={'rows':0};continue
 r={'rows':len(rows),'ticks':[min(x['tick']for x in rows),max(x['tick']for x in rows)]}
 for key in ['depth_km','temperature','light','credit','current_demand','h']:
  r[key]=[min(x[key]for x in rows),max(x[key]for x in rows)]
 for key in ['biomass','organization','support_mass','reproduction_credit']:
  r[key]=[min(x['cohort'][key]for x in rows),max(x['cohort'][key]for x in rows)]
 r['last']=rows[-1];r['positive_support_rows']=sum(x['cohort']['support_mass']>0 for x in rows)
 r['first_positive_support_tick']=next((x['tick']for x in rows if x['cohort']['support_mass']>0),None)
 s=json.load(gzip.open(P/(arm+'-day7.json.gz')))
 r['endpoint']=None
 for i,cell in enumerate(s['origin']['cells']):
  for slot in cell.get('sparse',[]):
   c=slot['value']
   if c['biomass']>0 and c.get('root_fraction',0)>0:r['endpoint']={'cell':i,'cohort':c,'soil':s['beta_origin']['soil'][i]}
 result[arm]=r;probes.append((arm,rows[-1]))
(O/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
lines=['const std=@import("std");const M=@import("simulation/microbes.zig");','pub fn main() !void {']
for arm,row in probes:
 c=row['cohort'];fields=','.join('.'+k+'='+repr(v) for k,v in c.items())
 lines += ['{const c=M.Cohort{'+fields+'};var e=M.Environment{.temperature='+repr(row['temperature'])+',.depth_km='+repr(row['depth_km'])+',.light='+repr(row['light'])+',.carbon_available=0,.oxygen_carbon_capacity=0};',
 'const real=M.rootDemand(c,e,1440);const height=M.producerHeightMeters(c);e.depth_km=0;const dry=M.rootDemand(c,e,1440);',
 'std.debug.print("'+arm+' id={d} height_m={e} root_tissue={e} actual_demand={e} hypothetical_dry_demand={e}\\n",.{c.lineage,height,c.support_mass*c.root_fraction,real,dry});',
 'try std.testing.expectEqual(@as(f64,0),real);try std.testing.expect((dry>0)==(c.support_mass>0));}']
lines+=['}'];path=pathlib.Path('../site-tmp/combined-strategy/src/root_bottleneck_qa.zig');path.write_text('\n'.join(lines)+'\n');(O/'root_bottleneck_qa.zig').write_text(path.read_text())
print(json.dumps({k:{'rows':v['rows'],'first_support':v.get('first_positive_support_tick'),'endpoint':v.get('endpoint')}for k,v in result.items()},indent=2))
