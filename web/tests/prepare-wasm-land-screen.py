from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];o=r.parent/'site-tmp/wasm-land-screen';o.mkdir(exist_ok=True)
base=(r.parent/'site-tmp/wasm-defense-screen/candidate/src/qa_wasm_nearest.zig').read_text()
base=base.replace(' if(saved.mode!=.sandbox)return error.SandboxOnly;','')
base=base.replace(' p.worldMode=.sandbox;',' p.worldMode=saved.mode;\n if(saved.origin)|origin|{p.microbeCells=try a.alloc(S.Microbes.Cell,n);for(p.microbeCells,origin.cells)|*c,s|c.*=s.runtime();p.microbeStats=origin.stats;}')
base=base.replace(' if(qa_enabled and !p.sandboxDefense.enabled){const receipt=@import("sandbox_defense.zig").enableDefenses(&p);if(receipt.status!=.enabled)return error.EnableFailed;}','')
base=base.replace(' saved.rabbits=rabbits;saved.origin=null;',' saved.rabbits=rabbits;if(p.worldMode==.origin){const sparse=try S.captureSparse(a,p.microbeCells);saved.origin=.{.model_revision=5,.cohort_encoding=.sparse_indexed,.cells=sparse.cells,.stats=p.microbeStats};}else saved.origin=null;')
for arm in ['baseline','candidate']:
 d=o/arm/'src';shutil.copytree(r.parent/f'site-tmp/origin-land-gate/{arm}/src',d,dirs_exist_ok=True)
 s=base
 if arm=='candidate':
  s=s.replace(' p.refreshTransformedPoints(saved.axial_tilt);',' if(saved.beta_origin)|beta|{try p.ensureLandBetaStorage();p.landBeta=beta.config;@memcpy(p.landSoil,beta.soil);@memcpy(p.landVapor,beta.vapor);@memcpy(p.landNewVapor,beta.vapor);}\n p.refreshTransformedPoints(saved.axial_tilt);')
  s=s.replace(' saved.version=S.VERSION;', ' saved.version=if(p.landBeta.enabled) S.VERSION else 7;')
  s=s.replace(' try saved.validate();output=', ' if(p.landBeta.enabled){for(p.waterVaporMass,0..)|*v,i|v.*=p.vaporMass32(i);saved.beta_origin=.{.format=.origin_land_beta_v1,.config=p.landBeta,.soil=p.landSoil,.vapor=p.landVapor};}\n try saved.validate();output=')
  s=s.replace(' var loop=Loop.init();',' std.debug.print("BETA_LAYOUT enabled={} soil_bytes={} vapor_bytes={} scratch_bytes={} cohort_bytes={}\\n",.{p.landBeta.enabled,p.landSoil.len*8,p.landVapor.len*8,p.landNewVapor.len*8+p.landCoefficient.len*8+p.landRootH.len*16,@sizeOf(S.Microbes.Cohort)});\n var loop=Loop.init();')
 (d/'qa_wasm_land.zig').write_text(s)
 p=d/'simulation/planet.zig';p.write_text('pub var qa_stages:[4]f64=.{0,0,0,0};\npub var qa_substages:[5]f64=.{0,0,0,0,0};\n'+p.read_text())
 (o/arm/'source-hashes.json').write_text(json.dumps({str(p.relative_to(d)):hashlib.sha256(p.read_bytes()).hexdigest()for p in d.rglob('*.zig')},indent=2))
shutil.copyfile(r.parent/'site-tmp/wasm-planet-profile/graph.json',o/'graph.json')
b=json.loads((r.parent/'site-tmp/origin-land-gate/beta2.json').read_text());b.pop('beta_origin');b['version']=7
for c in b['origin']['cells']:
 for co in c.get('cohorts',[]):co.pop('root_fraction',None)
 for entry in c.get('entries',[]) or []:entry['value'].pop('root_fraction',None)
# Sparse key is inspected below; zero cohorts in this fixed empty world.
(o/'empty-off.json').write_text(json.dumps(b,separators=(',',':')))
shutil.copyfile(r.parent/'site-tmp/origin-land-gate/beta2.json',o/'empty-beta.json')
