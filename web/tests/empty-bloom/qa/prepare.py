#!/usr/bin/env python3
"""Prepare current-engine native QA in isolation; does not edit the checkout."""
from pathlib import Path
import os,sys,subprocess
here=Path(__file__).resolve().parent;root=Path(os.environ['STELLA_SOURCE_ROOT']).resolve();out=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(root/'web/tests/performance/qa/prepare.py'),str(out)],check=True)
if not (out/'empty_bloom.zig').exists():
 subprocess.run(['patch','-p2','--forward','-i',str(here/'empty-bloom.patch')],cwd=out,check=True)
p=out/'states/play.zig';s=p.read_text().replace('@import("builtin").target.cpu.arch == .wasm32','true').replace('@import("builtin").target.cpu.arch != .wasm32','false')
s='pub var qa_force_bloom=false;\n'+s;s=s.replace('const useBloom=!@import','const useBloom=qa_force_bloom or !@import');p.write_text(s)
p=out/'main.zig';s=p.read_text();needle='    if(std.posix.getenv("QA_CLOCK")!=null){';assert needle in s
s=s.replace(needle,(here/'pixels-qa.zig.part').read_text()+needle+'\n        @import("states/play.zig").qa_force_bloom=std.posix.getenv("QA_FORCE_BLOOM")!=null;')
s+='\n'+(here/'pixels-helper.zig.part').read_text()
s=s.replace('var wall=try std.time.Timer.start();var previous:u64=0;', 'var frame_samples:[2048]f64=undefined;var sample_count:usize=0;\n            var wall=try std.time.Timer.start();var previous:u64=0;')
s=s.replace('max_frame=@max(max_frame,@as(f64,@floatFromInt(wall.read()-now))/1e9);frames+=1;', 'const frame_seconds=@as(f64,@floatFromInt(wall.read()-now))/1e9;max_frame=@max(max_frame,frame_seconds);if(sample_count<frame_samples.len){frame_samples[sample_count]=frame_seconds;sample_count+=1;}frames+=1;')
s=s.replace('const elapsed=@as(f64,@floatFromInt(wall.read()))/1e9;', '''const elapsed=@as(f64,@floatFromInt(wall.read()))/1e9;
            std.mem.sort(f64,frame_samples[0..sample_count],{},std.sort.asc(f64));
            std.debug.print("BLOOM_FRAMES target={d} forced_full={} samples={d} p50_ms={d} p95_ms={d} p99_ms={d} max_ms={d}\\n",.{rate,@import("states/play.zig").qa_force_bloom,sample_count,frame_samples[sample_count/2]*1000,frame_samples[@min(sample_count-1,sample_count*95/100)]*1000,frame_samples[@min(sample_count-1,sample_count*99/100)]*1000,max_frame*1000});''')
needle='        state.simulationClock.pending=1440;state.simulationClock.achieved=123;'
s=s.replace(needle,'''        var input_timer=try std.time.Timer.start();qa_pointer(40,28,1);render(window);gl.finish();qa_pointer(40,28,0);render(window);gl.finish();
        std.debug.assert(state.paused);const pause_time=state.gameTime;state.setRawFrameDelta(0.1);state.update(&game,0.1);std.debug.assert(state.gameTime==pause_time);
        std.debug.print("BLOOM_INPUT two_frame_pause_ms={d} paused_without_extra_tick=true\\n",.{@as(f64,@floatFromInt(input_timer.read()))/1e6});
'''+needle)
p.write_text(s);print(out/'main.zig')
