#!/usr/bin/env python3
"""One ABBA actual pre/post all-point seed coupled frame proxy; no device claim."""
from pathlib import Path
import subprocess,sys,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve();subprocess.run([sys.executable,str(r/'web/tests/egl-auto-seed-prepare.py'),str(o)],check=True)
p=o/'main.zig';s=p.read_text();a=s.index('          _=pm;_=pw;');b=s.index('\n        std.debug.print("AUTO_SEED_GATE',a)
s=s[:a]+r'''
          _=pm;_=pw;state.paused=true;state.showEscapeMenu=false;state.showPointDetails=false;state.showPlanetControl=false;state.selectedTool=.None;state.watchLifeView=true;
          const AS=@import("auto_seed.zig");const world=@import("performance_details.zig").world_serial;
          for(0..12)|_|{render(window);gl.finish();window.swapBuffers();}
          const original=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const initial=try std.json.parseFromSlice(saves.schema.Save,a,original,.{.allocate=.alloc_always});
          var response=try std.json.parseFromSlice(std.json.Value,a,AS.start(state,world,world),.{.allocate=.alloc_always});const ticket:u32=@intCast(response.value.object.get("token").?.integer);
          while(std.mem.eql(u8,response.value.object.get("phase").?.string,"planning")){response=try std.json.parseFromSlice(std.json.Value,a,AS.step(state,world,ticket),.{.allocate=.alloc_always});std.debug.assert(response.value.object.get("ok").?.bool);}
          const receipt=try a.dupe(u8,AS.apply(state,world,ticket));std.debug.assert(std.mem.indexOf(u8,receipt,"\"ok\":true")!=null);
          const populated=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const seeded=try std.json.parseFromSlice(saves.schema.Save,a,populated,.{.allocate=.alloc_always});
          std.debug.print("AUTO_PROFILE_PLATFORM renderer={s} version={s} viewport=390x700 debug=false receipt={s}\n",.{std.mem.span(gl.getString(gl.RENDERER).?),std.mem.span(gl.getString(gl.VERSION).?),receipt});
          var references=[_]([]const u8){"",""};
          for([_]bool{false,true,true,false},0..)|after,arm|{
            try saves.apply(state,if(after)seeded.value else initial.value);state.selectedTool=.None;state.watchLifeView=true;
            for(0..30)|_|{render(window);gl.finish();window.swapBuffers();}
            var start_living:usize=0;for(state.planet.microbeCells)|cell|for(cell.cohorts)|co|{if(co.biomass>0)start_living+=1;};
            const glyphs_before=state.visibleSprouts;
            qa_capture(if(after) "OUTPUT/populated.ppm" else "OUTPUT/before.ppm");
            var physics_ns:[60]u64=undefined;var render_ns:[60]u64=undefined;var full_ns:[60]u64=undefined;
            for(0..60)|i|{var timer=try std.time.Timer.start();state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;physics_ns[i]=timer.read();render(window);gl.finish();window.swapBuffers();full_ns[i]=timer.read();render_ns[i]=full_ns[i]-physics_ns[i];}
            const endpoint=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const kind:usize=if(after)1 else 0;if(references[kind].len==0)references[kind]=endpoint;std.debug.assert(std.mem.eql(u8,references[kind],endpoint));
            var end_living:usize=0;for(state.planet.microbeCells)|cell|for(cell.cohorts)|co|{if(co.biomass>0)end_living+=1;};
            std.debug.print("AUTO_PROFILE {s}\n",.{try std.json.stringifyAlloc(a,.{.arm=arm,.populated=after,.start_living=start_living,.end_living=end_living,.glyphs_before=glyphs_before,.glyphs_after=state.visibleSprouts,.physics_ns=physics_ns,.render_ns=render_ns,.full_ns=full_ns,.same_variant_full_save_rng_exact=true},.{})});
          }
          try saves.apply(state,initial.value);std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
        }
'''.replace('OUTPUT',str(o.parent))+s[b:];p.write_text(s.replace('AUTO_SEED_GATE','AUTO_PROFILE_COMPLETE'))
p=o/'renderer.zig';s=p.read_text();a=s.index('            .debug = @import("render_diagnostics_policy.zig")');b=s.index('\n',s.index('else false),',a));s=s[:a]+'            .debug = false, // Match shipped web diagnostic policy.'+s[b:];p.write_text(s)
(o.parent/'profile-provenance.json').write_text(json.dumps({'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip(),'input_sha256':hashlib.sha256((r.parent/'site-tmp/natural60-day60.json').read_bytes()).hexdigest(),'sequence':['before','populated','populated','before'],'render_warmup_per_arm':30,'coupled_frames_per_arm':60,'seconds_per_tick':1440,'hashes':{f:hashlib.sha256((o/f).read_bytes()).hexdigest()for f in ['main.zig','renderer.zig','auto_seed.zig','states/play.zig','simulation/planet.zig']}},indent=2)+'\n')
