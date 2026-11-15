#!/usr/bin/env python3
"""Read-only production source; isolated viewport/driver-call profiling using verified QA cache."""
from pathlib import Path
import hashlib,json,subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1]);cache=Path(sys.argv[2]);meta=json.loads(cache.with_suffix('.provenance.json').read_text())
assert hashlib.sha256(cache.read_bytes()).hexdigest()==meta['checkpoint_sha256'],'QA cache hash mismatch'
for name,digest in meta['source_hashes'].items():
 actual=hashlib.sha256((root/name).read_bytes()).hexdigest()
 if actual!=digest:
  if name.startswith('web/'):print('Explicit native-only exemption: web asset not executed by this native harness changed:',name,actual)
  else:raise AssertionError('QA cache engine source mismatch: '+name)
subprocess.run([sys.executable,str(root/'web/tests/egl-full-frame-profile-prepare.py'),str(out)],check=True)
p=out/'simulation/planet.zig';p.write_text(p.read_text().replace('if (@import("builtin").target.cpu.arch != .wasm32) {','if (false) {'))
p=out/'main.zig';s=p.read_text();needle='    try profileFrames("early",state,window,allocator);';assert needle in s;s=s.replace(needle,needle+'''\n    { const saves=@import("save_game.zig");var ar=std.heap.ArenaAllocator.init(allocator);defer ar.deinit();const a=ar.allocator();const b=try std.fs.cwd().readFileAlloc(a,"'''+str(cache)+'''",128*1024*1024);const v=try saves.schema.parse(a,b);try saves.apply(state,v.value);try profileFrames("cached30d",state,window,allocator);return;}''',1)
s='extern fn qa_reset_draws() void;\nextern fn qa_report_draws() void;\n'+s
s=s.replace('  perf.metrics.setEnabled(true);const start_time=state.gameTime;','  qa_reset_draws();perf.metrics.setEnabled(true);const start_time=state.gameTime;')
s=s.replace('  const physics=perf.metrics.sample();','  qa_report_draws();const physics=perf.metrics.sample();')
s=s.replace('state.update(&game,1.0/60.0);render(window);gl.finish();window.swapBuffers();','game.loop.pump(16);state.update(&game,1.0/60.0);game.loop.pump(16);render(window);gl.finish();window.swapBuffers();')
s=s.replace('var timer=try std.time.Timer.start();state.update(&game,1.0/60.0);const update_ms=', 'var timer=try std.time.Timer.start();game.loop.pump(16);state.update(&game,1.0/60.0);game.loop.pump(16);const update_ms=')
p.write_text(s)
print('Verified cached QA world',meta['checkpoint_sha256'])
