from pathlib import Path
import shutil,subprocess,json,hashlib
r=Path(__file__).resolve().parents[2];tmp=r.parent/'site-tmp';o=tmp/'law3-canonical';assert not o.exists();o.mkdir()
base=(tmp/'wasm-land-screen/candidate/src/qa_wasm_land.zig').read_text()
base=base.replace('saved.version=if(p.landBeta.enabled) S.VERSION else 7;', 'saved.version=if(p.landBeta.enabled) (if(p.landBeta.physiology_law==3) @as(u32,10) else if(p.landBeta.physiology_law==2) @as(u32,9) else @as(u32,8)) else 7;')
base=base.replace('.format=.origin_land_beta_v1,.config=p.landBeta', '.format=if(p.landBeta.physiology_law==3).origin_land_beta_v3 else if(p.landBeta.physiology_law==2).origin_land_beta_v2 else .origin_land_beta_v1,.config=p.landBeta')
base=base.replace('p.landRootH.len*16','p.landRootH.len*32+p.landRootOwner.len*32')
base=base.replace(' var loop=Loop.init();',' std.debug.print("ENGINE_MEMORY cell_size={} cohort_size={} cell_array_bytes={} amount_bytes={} owner_bytes={}\\n",.{@sizeOf(S.Microbes.Cell),@sizeOf(S.Microbes.Cohort),p.microbeCells.len*@sizeOf(S.Microbes.Cell),p.landRootH.len*32,p.landRootOwner.len*32});\n var loop=Loop.init();')
for arm in ['baseline','candidate']:
 d=o/arm/'src';shutil.copytree(tmp/'origin-final-demand/src',d)
 if arm=='candidate':subprocess.run(['python3',str(r/'web/tests/patch-origin-land-borrowed.py'),str(d)],check=True)
 # Untimed observer arrays are zero placeholders, not stage instrumentation.
 p=d/'simulation/planet.zig';p.write_text('pub var qa_stages:[4]f64=.{0,0,0,0};\npub var qa_substages:[5]f64=.{0,0,0,0,0};\n'+p.read_text())
 (d/'qa_wasm_land.zig').write_text(base)
 (o/arm/'source-sha256.json').write_text(json.dumps({str(p.relative_to(d)):hashlib.sha256(p.read_bytes()).hexdigest()for p in d.rglob('*.zig')},indent=2)+'\n')
# Separate actual native path applies exact same borrowed patch to frozen QA source.
d=o/'native/src';shutil.copytree(tmp/'origin-final-demand-native/src',d);subprocess.run(['python3',str(r/'web/tests/patch-origin-land-borrowed.py'),str(d)],check=True)
(o/'native/source-sha256.json').write_text(json.dumps({str(p.relative_to(d)):hashlib.sha256(p.read_bytes()).hexdigest()for p in d.rglob('*.zig')},indent=2)+'\n')
shutil.copyfile(tmp/'wasm-land-screen/graph.json',o/'graph.json')
shutil.copyfile(tmp/'wasm-land-screen/empty-off.json',o/'early-off.json')
x=json.loads((tmp/'wasm-land-screen/empty-beta.json').read_text());x['version']=10;x['beta_origin']['format']='origin_land_beta_v3';x['beta_origin']['config']['physiology_law']=3;(o/'early-law3.json').write_text(json.dumps(x,separators=(',',':')))
shutil.copyfile(tmp/'origin-final-demand-shoreline/depth-3-arm-0-0.json',o/'day30-100mm.json')
(o/'input-sha256.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [o/'graph.json',o/'early-off.json',o/'early-law3.json',o/'day30-100mm.json']},indent=2)+'\n')
print(o)
