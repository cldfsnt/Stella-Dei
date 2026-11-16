#!/usr/bin/env python3
import pathlib,shutil,gzip,json,hashlib
r=pathlib.Path(__file__).resolve().parents[2]; out=r.parent/'site-tmp/shoreline-climate-feasibility';src=r.parent/'site-tmp/root-wind-recovery/src';shutil.copytree(src,out/'src',dirs_exist_ok=True)
e=r/'web/tests/continuation-review/shoreline-climate-feasibility';e.mkdir(exist_ok=True)
p=r/'web/tests/continuation-review/rooted-founder/natural-margin-trial';weather=[];founder=None
for a in range(2):
 rows=[json.loads(l[7:]) for l in gzip.open(p/f'main-{a}.log.gz','rt') if l.startswith('USED_H ')];rows=[x for x in rows if x['stage']=='mortality'];assert len(rows)==60
 weather.append([{k:x[k] for k in ['temperature','depth_km','light']} for x in rows])
 if a==0:
  receipt=next(json.loads(l[8:]) for l in gzip.open(p/'main-0.log.gz','rt') if l.startswith('FOUNDER '));founder=dict(rows[0]['cohort']);founder['biomass']=receipt['carbon_kg_m2'];founder['support_mass']=receipt['support_kg_c_m2'];founder['reproduction_credit']=0
hardy=dict(founder,structure=.5)
natural=json.loads((r/'web/tests/continuation-review/combined-origin-acceptance/root-bottleneck/summary.json').read_text())['1337-ordinary']['endpoint']['cohort']
phen=[founder,hardy,natural]
(e/'inputs.json').write_text(json.dumps({'weather':weather,'phenotypes':phen},indent=2)+'\n')
fields=lambda d:','.join('.'+k+'='+repr(v) for k,v in d.items())
s='const M=@import("simulation/microbes.zig");\npub const names=[_] []const u8{"rooted","hardy","natural125"};\npub const phenotypes=[_]M.Cohort{'+','.join('.{'+fields(c)+'}' for c in phen)+'};\n'
s+='pub const weather=[2][60]M.Environment{'+','.join('.{'+','.join('.{'+fields(c)+',.carbon_available=0,.oxygen_carbon_capacity=0}' for c in row)+'}' for row in weather)+'};\n'
(out/'src/climate_fixtures.zig').write_text(s);shutil.copy2(r/'web/tests/shoreline-climate-feasibility.zig',out/'src/climate_qa.zig')
(e/'source-hashes.json').write_text(json.dumps({str(p.relative_to(out/'src')):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((out/'src').rglob('*.zig'))},indent=2)+'\n')
