from pathlib import Path
import json,hashlib,shutil
r=Path(__file__).resolve().parents[2];t=r.parent/'site-tmp';b=t/'wasm-protective-cost';b.mkdir(exist_ok=True);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
base=(t/'wasm-root-wind-screen/candidate/src/qa_wasm_land.zig').read_text()
for mode,src,manifest in [('legacy',t/'root-calm/src',r/'web/tests/continuation-review/root-calm-engine/source-hashes.json'),('small',t/'protective-integration/src',r/'web/tests/continuation-review/protective-integration/source-hashes.json')]:
 for k,h in json.loads(manifest.read_text()).items():assert sha(src/k)==h,k
 o=b/mode/'src';shutil.copytree(src,o,dirs_exist_ok=True);s=base
 s=s.replace(' p.refreshTransformedPoints(saved.axial_tilt);',' p.groundThermalLaw=if(saved.ground_thermal)|cfg|cfg.law else 0;\n p.refreshTransformedPoints(saved.axial_tilt);')
 s=s.replace(' try saved.validate();output=', ' saved.ground_thermal=if(p.groundThermalLaw==1).{.law=1}else null;if(p.groundThermalLaw==1)saved.version=S.CALM_VERSION;\n try saved.validate();output=')
 if mode=='small':
  s=s.replace(' p.groundThermalLaw=', ' p.protectiveStrategy=if(saved.protective_strategy)|cfg|cfg.runtime() else .{};\n p.groundThermalLaw=',1)
  s=s.replace(' try saved.validate();output=', ' saved.protective_strategy=if(p.protectiveStrategy.enabled).{.law=1,.mutation_law=1,.stream_seed=p.protectiveStrategy.stream_seed}else null;if(p.protectiveStrategy.enabled)saved.version=S.PROTECTIVE_VERSION;\n try saved.validate();output=')
 (o/'qa_wasm_land.zig').write_text(s);p=o/'simulation/planet.zig';p.write_text('pub var qa_stages:[4]f64=.{0,0,0,0};\npub var qa_substages:[5]f64=.{0,0,0,0,0};\n'+p.read_text())
 (b/mode/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):sha(p)for p in o.rglob('*.zig')},indent=2))
 shutil.copy2(t/'combined-strategy/42-pioneer-day7.json',b/f'off-{mode}.json')
 shutil.copy2(t/'natural-shoreline/final.json',b/f'enabled-{mode}.json')
p=b/'enabled-small.json';v=json.loads(p.read_text());assert v['version']==14
for cell in v['origin']['cells']:
 for c in(cell.get('cohorts')or[x['value']for x in cell.get('sparse',[])or []]):assert c.get('protective_investment',0)==0 and c.get('protective_clock',-1)==-1
v['version']=15;v['protective_strategy']={'law':1,'mutation_law':1,'stream_seed':v['seed']};p.write_text(json.dumps(v,separators=(',',':')))
x=json.loads(p.read_text());x['version']=14;x.pop('protective_strategy');assert x==json.loads((b/'enabled-legacy.json').read_text())
shutil.copy2(t/'wasm-root-wind-screen/graph.json',b/'graph.json');(b/'input-hashes.json').write_text(json.dumps({p.name:sha(p)for p in b.glob('*.json')},indent=2))
