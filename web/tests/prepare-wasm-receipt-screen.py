#!/usr/bin/env python3
from pathlib import Path
import subprocess,shutil,json,hashlib,tarfile,io
r=Path(__file__).resolve().parents[2];o=r.parent/'site-tmp/wasm-receipt-screen';o.mkdir(exist_ok=True)
baseline='a41c3b4';assert not subprocess.check_output(['git','diff',baseline,'cb5ed87^','--','src'],cwd=r)
base=(r.parent/'site-tmp/wasm-defense-screen/candidate/src/qa_wasm_nearest.zig').read_text()
base=base.replace(' if(qa_enabled and !p.sandboxDefense.enabled){const receipt=@import("sandbox_defense.zig").enableDefenses(&p);if(receipt.status!=.enabled)return error.EnableFailed;}','')
for arm in ['baseline','candidate']:
 dest=o/arm;dest.mkdir(exist_ok=True);d=dest/'src'
 if arm=='baseline':
  blob=subprocess.check_output(['git','archive',baseline,'src'],cwd=r)
  with tarfile.open(fileobj=io.BytesIO(blob))as t:t.extractall(dest)
 else:shutil.copytree(r/'src',d,dirs_exist_ok=True)
 s=base
 if arm=='candidate':
  s=s.replace(' p.refreshTransformedPoints(saved.axial_tilt);',' p.refreshTransformedPoints(saved.axial_tilt);\n @import("plant_receipt.zig").enabled=true;@import("plant_receipt.zig").reset();if(qa_enabled)@import("plant_receipt.zig").select(&p,@import("performance_details.zig").world_serial,436);')
  s=s.replace(' const elapsed=emscripten_get_now()-begin;',' const elapsed=emscripten_get_now()-begin;\n if(qa_enabled and ticks>0){const receipt=@import("plant_receipt.zig").view(&p,@import("performance_details.zig").world_serial,436,saved.game_time) orelse return error.ReceiptMissing;std.debug.print("RECEIPT {s}\\n",.{try std.json.stringifyAlloc(a,receipt,.{})});}')
 (d/'qa_wasm_nearest.zig').write_text(s)
 p=d/'simulation/planet.zig';p.write_text('pub var qa_stages:[4]f64=.{0,0,0,0};\npub var qa_substages:[5]f64=.{0,0,0,0,0};\n'+p.read_text())
 (dest/'source-hashes.json').write_text(json.dumps({str(p.relative_to(d)):hashlib.sha256(p.read_bytes()).hexdigest()for p in d.rglob('*.zig')},indent=2))
shutil.copyfile(r.parent/'site-tmp/wasm-planet-profile/graph.json',o/'graph.json')
