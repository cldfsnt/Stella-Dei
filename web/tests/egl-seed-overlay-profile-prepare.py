#!/usr/bin/env python3
"""One fixed order-balanced paused-world overlay attribution; no simulation/device claim."""
from pathlib import Path
import subprocess,sys,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(r/'web/tests/egl-seed-target-toggle-prepare.py'),str(o)],check=True)
p=o/'main.zig';s=p.read_text();a=s.index('          const original=try std.json.stringifyAlloc');b=s.index('\n        std.debug.print("SEED_TARGET_COMPLETE',a)
s=s[:a]+r'''
          // Stabilize the camera and driver before freezing this exact view.
          for(0..12)|_|{render(window);gl.finish();window.swapBuffers();}
          const original=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          std.debug.print("SEED_PROFILE_PLATFORM renderer={s} version={s} viewport=390x700 debug=false simulation_ticks=0\n",.{std.mem.span(gl.getString(gl.RENDERER).?),std.mem.span(gl.getString(gl.VERSION).?)});
          for([_]bool{true,false,false,true},0..)|visible,block|{
            _=stella_seed_targets(if(visible)1 else 0);
            for(0..12)|_|{render(window);gl.finish();window.swapBuffers();}
            @import("states/play.zig").qaSeedNs=0;PerformanceDetails.metrics.setEnabled(true);
            var frames:[30]f64=undefined;var total:f64=0;
            for(0..30)|i|{var timer=try std.time.Timer.start();render(window);gl.finish();window.swapBuffers();frames[i]=@as(f64,@floatFromInt(timer.read()))/1e6;total+=frames[i];}
            const sample=PerformanceDetails.metrics.sample();const context=PerformanceDetails.metrics.context;PerformanceDetails.metrics.setEnabled(false);
            std.mem.sort(f64,&frames,{},std.sort.asc(f64));
            std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
            std.debug.print("SEED_PROFILE block={} shown={} targets={} colonies={} candidates={} frames=30 mean_ms={d} median_ms={d} p95_ms={d} min_ms={d} max_ms={d} seed_cpu_mean_ms={d} terrain_ms={d} scene_ms={d} post_ms={d} ui_ms={d} bloom={} passes={} full_save_rng_exact=true\n",.{block,visible,state.seedTargets.count,state.visibleSprouts,state.sproutCandidates,total/30,(frames[14]+frames[15])/2,frames[28],frames[0],frames[29],@as(f64,@floatFromInt(@import("states/play.zig").qaSeedNs))/30e6,sample.stage_sum[0]/30,sample.stage_sum[1]/30,sample.stage_sum[2]/30,sample.stage_sum[3]/30,context.bloom_active,context.bloom_passes});
          }
          _=stella_seed_targets(1);
          std.debug.print("SEED_PROFILE_PASS fixed_blocks=4 simulation_ticks=0 full_save_rng_exact=true\n",.{});
        }
'''+s[b:];s=s.replace('SEED_TARGET_COMPLETE','SEED_PROFILE_COMPLETE');p.write_text(s)
p=o/'states/play.zig';s=p.read_text();needle='        self.renderSeedZones(vg, vp, width, height, toolBottom);';assert s.count(needle)==1;s=s.replace(needle,'        const qa_seed_start=std.time.nanoTimestamp();\n'+needle+'\n        qaSeedNs+=@intCast(@max(0,std.time.nanoTimestamp()-qa_seed_start));');s+='\npub var qaSeedNs:u64=0;\n';p.write_text(s)
p=o/'renderer.zig';s=p.read_text();a=s.index('            .debug = @import("render_diagnostics_policy.zig")');b=s.index('\n',s.index('else false),',a));s=s[:a]+'            .debug = false, // QA: match shipped per-draw diagnostic policy.'+s[b:];p.write_text(s)
(o.parent/'profile-provenance.json').write_text(json.dumps({'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip(),'sequence':[True,False,False,True],'warmup_per_block':12,'timed_per_block':30,'input_sha256':hashlib.sha256((r.parent/'site-tmp/sunlit14/day-14.json').read_bytes()).hexdigest(),'copied':{str(x.relative_to(o)):hashlib.sha256(x.read_bytes()).hexdigest()for x in [o/'main.zig',o/'states/play.zig',o/'renderer.zig']}},indent=2)+'\n')
