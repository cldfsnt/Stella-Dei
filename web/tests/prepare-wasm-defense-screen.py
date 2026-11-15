from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2]; o=r.parent/'site-tmp/wasm-defense-screen';o.mkdir(exist_ok=True)
base=(r.parent/'site-tmp/wasm-nearest-sandbox/src/qa_wasm_nearest.zig').read_text()
base=base[:base.index('\nexport fn qa_set_candidate')]+ '\nvar qa_enabled:bool=false;\nexport fn qa_set_candidate(on:u32)void{qa_enabled=on!=0;}\n'
for name,source in [('baseline',r/'src'),('candidate',r.parent/'site-tmp/sandbox-defense-integration/src')]:
 d=o/name/'src';shutil.copytree(source,d,dirs_exist_ok=True);s=base
 if name=='candidate':
  s=s.replace(' p.worldMode=.sandbox;', ''' p.worldMode=.sandbox;
 p.sandboxDefense=saved.sandbox_defense orelse .{};
 if(qa_enabled and !p.sandboxDefense.enabled){const receipt=@import("sandbox_defense.zig").enableDefenses(&p);if(receipt.status!=.enabled)return error.EnableFailed;}''')
  s=s.replace(' saved.rabbits=rabbits;saved.origin=null;', ' saved.version=S.VERSION;saved.sandbox_defense=if(p.sandboxDefense.enabled)p.sandboxDefense else null;\n saved.rabbits=rabbits;saved.origin=null;')
 s=s.replace(' var loop=Loop.init();', ' std.debug.print("LAYOUT plant={d} planet={d} cells={d}\\n",.{@sizeOf(S.Plant),@sizeOf(P),n});\n var loop=Loop.init();')
 (d/'qa_wasm_nearest.zig').write_text(s)
 p=d/'simulation/planet.zig';p.write_text('pub var qa_stages:[4]f64=.{0,0,0,0};\npub var qa_substages:[5]f64=.{0,0,0,0,0};\n'+p.read_text())
 (o/name/'source-hashes.json').write_text(json.dumps({str(p.relative_to(d)):hashlib.sha256(p.read_bytes()).hexdigest() for p in d.rglob('*.zig')},indent=2))
shutil.copyfile(r.parent/'site-tmp/wasm-planet-profile/graph.json',o/'graph.json')
