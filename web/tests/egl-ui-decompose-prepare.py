#!/usr/bin/env python3
"""v44 isolated same-world NanoVG submission decomposition; never production switches."""
from pathlib import Path
import hashlib,json,subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1]);cache=Path(sys.argv[2]);meta=json.loads(cache.with_suffix('.provenance.json').read_text())
assert hashlib.sha256(cache.read_bytes()).hexdigest()==meta['checkpoint_sha256']
accepted={'src/states/play.zig':'f7386497b7d1ef64a7e943fdbaf2eb517e7ae286a777508c4745e8e0fd0ff884','src/simulation/planet.zig':'1e04d4df20b55c11825ae6c33f500cf3e219fccc8bf3df0c34304a670bf6501b'}
changes={}
for name,old in meta['source_hashes'].items():
 current=hashlib.sha256((root/name).read_bytes()).hexdigest()
 if current!=old:
  assert name.startswith('web/') or accepted.get(name)==current,'Unreviewed engine change '+name
  changes[name]={'checkpoint_source':old,'current_source':current,'reason':'web assets not executed' if name.startswith('web/') else 'explicit v44 label-only Play / parity-tested sparse traversal Planet; QA save loaded into current engine, not regenerated'}
subprocess.run([sys.executable,str(root/'web/tests/egl-full-frame-profile-prepare.py'),str(out)],check=True)
p=out/'simulation/planet.zig';p.write_text(p.read_text().replace('if (@import("builtin").target.cpu.arch != .wasm32) {','if (false) {'))
p=out/'main.zig';s=p.read_text();needle='    try profileFrames("early",state,window,allocator);';assert needle in s;s=s.replace(needle,needle+'''\n    {const saves=@import("save_game.zig");var ar=std.heap.ArenaAllocator.init(allocator);defer ar.deinit();const a=ar.allocator();const b=try std.fs.cwd().readFileAlloc(a,"'''+str(cache)+'''",128*1024*1024);const v=try saves.schema.parse(a,b);try saves.apply(state,v.value);try profileFrames("cached30d",state,window,allocator);return;}''',1)
s='extern fn qa_reset_draws() void;\nextern fn qa_report_draws() void;\n'+s
s=s.replace('  perf.metrics.setEnabled(true);const start_time=state.gameTime;','  qa_reset_draws();@import("qa_ui_timing.zig").reset();perf.metrics.setEnabled(true);const start_time=state.gameTime;')
s=s.replace('  const physics=perf.metrics.sample();','  @import("qa_ui_timing.zig").report();qa_report_draws();const result=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});var digest:[32]u8=undefined;std.crypto.hash.sha2.Sha256.hash(result,&digest,.{});std.debug.print("UI_SAVE stage={s} speed={d} hash={s}\\n",.{label,speed,std.fmt.fmtSliceHexLower(&digest)});const physics=perf.metrics.sample();')
s=s.replace('state.update(&game,1.0/60.0);render(window);gl.finish();window.swapBuffers();','game.loop.pump(16);state.update(&game,1.0/60.0);game.loop.pump(16);render(window);gl.finish();window.swapBuffers();')
s=s.replace('var timer=try std.time.Timer.start();state.update(&game,1.0/60.0);const update_ms=', 'var timer=try std.time.Timer.start();game.loop.pump(16);state.update(&game,1.0/60.0);game.loop.pump(16);const update_ms=');p.write_text(s)
(out/'qa_ui_timing.zig').write_text('''const std=@import("std");pub var enabled=false;var sums=[_]u64{0}**5;var counts=[_]u64{0}**5;
pub fn reset()void{sums=.{0}**5;counts=.{0}**5;enabled=true;}
pub fn begin()?std.time.Timer{return if(enabled) std.time.Timer.start() catch null else null;}
pub fn end(which:usize,value:?std.time.Timer)void{if(value)|v|{var t=v;sums[which]+=t.read();counts[which]+=1;}}
pub fn report()void{enabled=false;for(sums,counts,0..)|s,c,i|std.debug.print("UI_PART part={d} count={d} sum_ms={d:.5}\\n",.{i,c,@as(f64,@floatFromInt(s))/1e6});}
''')
p=out/'states/play.zig';s=p.read_text()
for i,name in enumerate(['renderSeedZones','renderSprouts','renderPropaguleFeedback','renderGodEffects']):
 needle='    fn '+name+'(';start=s.index(needle);brace=s.index('{',start);s=s[:brace+1]+f'\n        const qa_timer=@import("../qa_ui_timing.zig").begin();defer @import("../qa_ui_timing.zig").end({i},qa_timer);'+s[brace+1:]
p.write_text(s)
p=out/'renderer.zig';s=p.read_text();needle='        self.vg.endFrame();';assert needle in s;s=s.replace(needle,'        const qa_timer=@import("qa_ui_timing.zig").begin();\n        if(std.posix.getenv("STELLA_UI_CANCEL")!=null)self.vg.cancelFrame() else self.vg.endFrame();\n        @import("qa_ui_timing.zig").end(4,qa_timer);');p.write_text(s)
(out/'qa-provenance.json').write_text(json.dumps({'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'cache_sha256':meta['checkpoint_sha256'],'explicit_checkpoint_differences':changes,'copied_hashes':{str(p.relative_to(out)):hashlib.sha256(p.read_bytes()).hexdigest() for p in out.rglob('*.zig')}},indent=2)+'\n')
