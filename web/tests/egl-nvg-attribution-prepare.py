#!/usr/bin/env python3
"""Current-source read-only NanoVG attribution, isolated dependency copy."""
from pathlib import Path
import subprocess,sys,shutil
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(r/'web/tests/egl-natural60-prepare.py'),str(o)],check=True)
d=o/'qa-nanovg';shutil.copytree(r/'deps/nanovg/src',d,dirs_exist_ok=True)
p=d/'nanovg_gl.zig';s=p.read_text();s='''pub var qa_enabled=false;
pub var qa_counts=[_]u64{0}**10;
var qa_last_image:i32=-1;
pub fn qaReset(enabled:bool)void{qa_enabled=enabled;qa_counts=.{0}**10;qa_last_image=-1;}
pub fn qaReport()void{std.debug.print("NVG_COUNTS flush/calls/draws/uniforms/image_requests/repeated_image/blend/repeated_blend/flush_ns/get_error={any}\\n",.{qa_counts});}
'''+s
s=s.replace('        const err = gl.getError();','        if(qa_enabled)qa_counts[9]+=1;\n        const err = gl.getError();')
s=s.replace('    const frag = &ctx.uniforms.items[uniform_offset];','    if(qa_enabled){qa_counts[3]+=1;if(image!=0){qa_counts[4]+=1;if(image==qa_last_image)qa_counts[5]+=1;qa_last_image=image;}}\n    const frag = &ctx.uniforms.items[uniform_offset];')
s=s.replace('fn renderFlush(uptr: *anyopaque) void {','fn renderFlush(uptr: *anyopaque) void {\n    var qa_timer=std.time.Timer.start() catch unreachable;defer if(qa_enabled){qa_counts[8]+=qa_timer.read();};\n    qa_last_image=-1;var qa_blend:?Blend=null;')
s=s.replace('        // Setup required GL state.','        if(qa_enabled){qa_counts[0]+=1;qa_counts[1]+=ctx.calls.items.len;}\n        // Setup required GL state.')
s=s.replace('            gl.blendFuncSeparate(call.blend_func.src_rgb,','            if(qa_enabled){qa_counts[6]+=1;if(qa_blend)|last|{if(std.meta.eql(last,call.blend_func))qa_counts[7]+=1;}qa_blend=call.blend_func;}\n            gl.blendFuncSeparate(call.blend_func.src_rgb,')
s=s.replace('gl.drawArrays(', 'qaDrawArrays(')
s+='''\nfn qaDrawArrays(mode:gl.GLenum,first:gl.GLint,count:gl.GLsizei)void{if(qa_enabled)qa_counts[2]+=1;gl.drawArrays(mode,first,count);}\n''';p.write_text(s)
p=o/'simulation/planet.zig';p.write_text(p.read_text().replace('if (@import("builtin").target.cpu.arch != .wasm32) {','if (false) {'))
p=o/'main.zig';s=p.read_text();a=s.index('          const start_time=state.gameTime;');b=s.index('\n        try originSaveCheck',a)
s=s[:a]+r'''
          const ng=@import("nanovg").gl;
          state.paused=true;_=state.findLivingClusterResult(390,700);
          for(0..60)|_|{render(window);gl.finish();window.swapBuffers();}
          const frozen=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const initial=try std.json.parseFromSlice(saves.schema.Save,a,frozen,.{.allocate=.alloc_always});
          for([_]bool{false,true})|coupled|{
            var expected:?[]const u8=null;
            for([_]bool{false,true,true,false},0..)|enabled,trial|{
              try saves.apply(state,initial.value);ng.qaReset(false);
              const context:*ng.GLContext=@ptrCast(@alignCast(renderer.vg.ctx.params.user_ptr));context.options.debug=enabled;
              for(0..12)|_|{render(window);gl.finish();window.swapBuffers();}
              ng.qaReset(true);var updates:u64=0;var renders:u64=0;var timer=try std.time.Timer.start();
              for(0..60)|_|{
                var part=try std.time.Timer.start();
                if(coupled){state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
                updates+=part.read();part.reset();render(window);gl.finish();window.swapBuffers();renders+=part.read();
              }
              const total=timer.read();ng.qaReport();ng.qaReset(false);
              const endpoint=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
              if(expected)|e|{std.debug.assert(std.mem.eql(u8,e,endpoint));}else expected=endpoint;
              const prefix=std.posix.getenv("QA_NVG_OUT") orelse "/tmp/nvg";
              const image=try std.fmt.allocPrintZ(a,"{s}-{d}-{d}.ppm",.{prefix,@intFromBool(coupled),trial});qa_capture(image);
              std.debug.print("NVG_FRAME coupled={} debug={} trial={d} frames=60 update_ms={d} render_finish_ms={d} total_ms={d} fullsave_exact=true\n",.{coupled,enabled,trial,@as(f64,@floatFromInt(updates))/60e6,@as(f64,@floatFromInt(renders))/60e6,@as(f64,@floatFromInt(total))/60e6});
            }
          }
          try saves.apply(state,initial.value);std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.print("NVG_ATTRIBUTION_PASS original_restored=true\n",.{});
        }
'''+s[b:];s=s.replace('_=pw;_=pm;const micro=@import("simulation/microbes.zig");','_=pw;_=pm;');p.write_text(s)
