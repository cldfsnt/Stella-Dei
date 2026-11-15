#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(r/'web/tests/egl-foraging-production-prepare.py'),str(o)],check=True)
p=o/'simulation/planet.zig';s=p.read_text();s='pub var qa_nearest_prune=false;\n'+s
needle='pub fn getNearestPointTo(self: Planet, position: Vec3) usize {';assert s.count(needle)==1
s=s.replace(needle,needle+'\n        if(qa_nearest_prune)return @import("../experimental/nearest_sqrt_prune.zig").nearest(self.transformedPoints,position);');p.write_text(s)
p=o/'main.zig';s=p.read_text();a=s.index('          _=pm;_=pw;');b=s.index('\n        std.debug.print("FORAGING_PRODUCTION_COMPLETE',a)
s=s[:a]+r'''
          _=pm;_=pw;std.debug.assert(state.planet.worldMode==.sandbox);const PM=@import("simulation/planet.zig");const N=@import("experimental/nearest_sqrt_prune.zig");
          const original=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const initial=try std.json.parseFromSlice(saves.schema.Save,a,original,.{.allocate=.alloc_always});
          if(std.posix.getenv("QA_QUERY_CONTROLS")!=null){
            PM.qa_nearest_prune=false;
            for(state.planet.transformedPoints)|point|std.debug.assert(state.planet.getNearestPointTo(point)==N.nearest(state.planet.transformedPoints,point));
            for(state.planet.lifeforms.items)|animal|std.debug.assert(state.planet.getNearestPointTo(animal.position)==N.nearest(state.planet.transformedPoints,animal.position));
            for([_]@TypeOf(state.cameraPos){state.cameraPos,state.targetCameraPos,state.cameraPos.scale(2),state.cameraPos.scale(0.5)})|query|std.debug.assert(state.planet.getNearestPointTo(query)==N.nearest(state.planet.transformedPoints,query));
            const old=state.planet.transformedPoints[0];state.planet.transformedPoints[0]=state.planet.transformedPoints[1];for(state.planet.lifeforms.items)|animal|std.debug.assert(state.planet.getNearestPointTo(animal.position)==N.nearest(state.planet.transformedPoints,animal.position));state.planet.transformedPoints[0]=old;
            std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
            std.debug.print("NEAREST_CONTROLS points={} rabbits={} camera_queries=4 geometry_edit=true original_exact=true\n",.{state.planet.transformedPoints.len,state.planet.lifeforms.items.len});
          }else{
            var reference:[]const u8="";
            for([_]bool{false,true,true,false},0..)|candidate,arm|{
              try saves.apply(state,initial.value);PM.qa_nearest_prune=candidate;
              for(0..12)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
              const rabbits_before=state.planet.lifeforms.items.len;var ticks:[60]u64=undefined;
              for(0..60)|i|{var timer=try std.time.Timer.start();state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;ticks[i]=timer.read();}
              const endpoint=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});if(reference.len==0)reference=endpoint;std.debug.assert(std.mem.eql(u8,reference,endpoint));
              std.debug.print("NEAREST_PAIR {s}\n",.{try std.json.stringifyAlloc(a,.{.arm=arm,.candidate=candidate,.rabbits_before=rabbits_before,.rabbits_after=state.planet.lifeforms.items.len,.ticks_ns=ticks,.baseline_candidate_fullsave_rng_exact=true},.{})});
            }
            PM.qa_nearest_prune=false;try saves.apply(state,initial.value);std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
            std.debug.print("NEAREST_PAIR_PASS original_restored=true native_simulation_only=true\n",.{});
          }
        }
'''+s[b:];p.write_text(s)
(o.parent/'provenance.json').write_text(json.dumps({'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip(),'input_sha256':hashlib.sha256((r.parent/'site-tmp/foraging-production/warm-actual-end.json').read_bytes()).hexdigest(),'source':{str(f.relative_to(o)):hashlib.sha256(f.read_bytes()).hexdigest()for f in o.rglob('*.zig')}},indent=2))
