#!/usr/bin/env python3
import pathlib,shutil,json,gzip,hashlib
r=pathlib.Path(__file__).resolve().parents[2]; base=r.parent/'site-tmp/root-wind-recovery/src'; out=r.parent/'site-tmp/paid-development-feasibility';out.mkdir(exist_ok=True)
shutil.copytree(base,out/'src',dirs_exist_ok=True)
source=(r/'web/tests/paid-development-feasibility.zig').read_text(); fixtures={}
p=r/'web/tests/continuation-review/combined-origin-acceptance/two-seed-trial'
for arm in ['42-ordinary','42-pioneer','1337-ordinary']:
 with gzip.open(p/(arm+'.log.gz'),'rt') as f:
  row=next(json.loads(x[7:]) for x in f if x.startswith('USED_H '))
 fixtures[arm]=row
 c=','.join('.'+k+'='+repr(v) for k,v in row['cohort'].items())
 source+='\ntest "recorded '+arm+' feasibility" {try probe("'+arm+'",M.Cohort{'+c+'},M.Environment{.temperature='+repr(row['temperature'])+',.depth_km='+repr(row['depth_km'])+',.light='+repr(row['light'])+',.carbon_available=0,.oxygen_carbon_capacity=0});}\n'
(out/'src/paid_development_qa.zig').write_text(source)
e=r/'web/tests/continuation-review/paid-development';e.mkdir(exist_ok=True)
(e/'birth-fixtures.json').write_text(json.dumps(fixtures,indent=2)+'\n')
(e/'source-hashes.json').write_text(json.dumps({str(x.relative_to(out/'src')):hashlib.sha256(x.read_bytes()).hexdigest() for x in sorted((out/'src').rglob('*.zig'))},indent=2)+'\n')
