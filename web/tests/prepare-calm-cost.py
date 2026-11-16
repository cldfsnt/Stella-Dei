from pathlib import Path
import json,hashlib,shutil
r=Path(__file__).resolve().parents[2];t=r.parent/'site-tmp';b=t/'wasm-calm-cost';b.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old=json.loads((r/'web/tests/continuation-review/combined-playtest/build/source-freeze.json').read_text())
for k,h in old.items():
 if k.startswith('src/'): assert sha(t/'combined-playtest'/k)==h,k
new=json.loads((r/'web/tests/continuation-review/root-calm-engine/source-hashes.json').read_text())
for k,h in new.items():
 p=t/'root-calm'/k if k.startswith('src/') else t/'root-calm/src'/k
 assert sha(p)==h,k
adapter=(t/'wasm-root-wind-screen/candidate/src/qa_wasm_land.zig').read_text()
adapter=adapter.replace(' const n=saved.water.len;', ' if(saved.version!=13)return error.ExpectedHistorical13;\n const n=saved.water.len;')
for mode,source in [('legacy',t/'combined-playtest/src'),('small',t/'root-calm/src')]:
 o=b/mode/'src';shutil.copytree(source,o,dirs_exist_ok=True)
 s=adapter
 if mode=='small':s=s.replace(' p.refreshTransformedPoints(saved.axial_tilt);',' if(saved.ground_thermal!=null or p.groundThermalLaw!=0)return error.ExpectedThermalOff;\n p.refreshTransformedPoints(saved.axial_tilt);')
 (o/'qa_wasm_land.zig').write_text(s)
 p=o/'simulation/planet.zig';p.write_text('pub var qa_stages:[4]f64=.{0,0,0,0};\npub var qa_substages:[5]f64=.{0,0,0,0,0};\n'+p.read_text())
 (b/mode/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):sha(p)for p in o.rglob('*')if p.is_file()},indent=2))
 inp=t/'combined-strategy/42-pioneer-day7.json';assert sha(inp)=='c25d2b2ce9953137eae1a95542cd73c1c0b3fda6718b482b261a74700e206670';shutil.copy2(inp,b/f'42-{mode}.json')
shutil.copy2(t/'wasm-root-wind-screen/graph.json',b/'graph.json')
print('FROZEN_SOURCE_AND_SAME_INPUT_PASS')
