#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-ecology-pulse-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text();needle='    originReport("empty",state);';s=s.replace(needle,needle+'''\n    std.debug.assert(!state.communitySample.valid);_=state.sampleOriginCommunity();std.debug.assert(state.communitySample.valid and state.communitySample.colonies==0 and state.communitySample.patches==0);std.debug.print("COMMUNITY_EMPTY known_zero=true\\n",.{});''',1)
a=s.index('          var found=state.findRecordedFeeding(true);');b=s.index('\n        try originSaveCheck',a)
s=s[:a]+r'''
          _=pw;_=pm;var linebuf:[160]u8=undefined;
          std.debug.assert(!state.communitySample.valid);
          std.debug.assert(std.mem.eql(u8,state.communitySample.line(&linebuf,PerformanceDetails.world_serial,@intFromPtr(state.planet.microbeCells.ptr),state.gameTime),"Global count pending"));
          const dims=window.getFramebufferSize();_=state.findLivingClusterResult(@floatFromInt(dims.width),@floatFromInt(dims.height));render(window);gl.finish();window.swapBuffers();
          const before=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const frozen=try std.json.parseFromSlice(saves.schema.Save,a,before,.{.allocate=.alloc_always});
          _=state.sampleOriginCommunity();std.debug.assert(state.communitySample.colonies==64 and state.communitySample.patches==37);
          render(window);gl.finish();window.swapBuffers();
          const after=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});std.debug.assert(std.mem.eql(u8,before,after));
          const prefix=std.posix.getenv("QA_COMMUNITY_PREFIX") orelse "/workspace/scratch/f67c3ac60ca3/site-tmp/community";
          qa_capture(try std.fmt.allocPrintZ(a,"{s}-global.ppm",.{prefix}));
          const sampled=state.communitySample;var bad=frozen.value;bad.radius=-1;var rejected=false;saves.apply(state,bad) catch {rejected=true;};std.debug.assert(rejected and std.meta.eql(sampled,state.communitySample));
          std.debug.assert(std.mem.eql(u8,before,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          state.colonyPeek.set(13596,state.planet.microbeCells[13596],state.gameTime);
          render(window);gl.finish();window.swapBuffers();std.debug.assert(state.colonyPeek.cell.?==13596);
          qa_capture(try std.fmt.allocPrintZ(a,"{s}-pin.ppm",.{prefix}));
          std.debug.assert(std.mem.eql(u8,before,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          try saves.apply(state,frozen.value);std.debug.assert(!state.communitySample.valid);
          std.debug.print("COMMUNITY_PROOF viewport={d}x{d} natural60=64/37 unknown_before_scan=true known_empty=true sample_render_deep_save_parity=true failed_load_preserves=true successful_load_clears=true local_pin_retained=true\n",.{dims.width,dims.height});
        }
''' +s[b:];p.write_text(s)
