#!/usr/bin/env python3
"""Attribution only: actual rabbit scheduler, no nearest-point algorithm changes."""
from pathlib import Path
import subprocess,sys,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(r/'web/tests/egl-foraging-production-prepare.py'),str(o)],check=True)
(o/'qa_rabbit_cost.zig').write_text('''const std=@import("std");
pub var enabled=false;
pub var nearest_ns:i128=0;pub var nearest_calls:u64=0;pub var ai_ns:i128=0;pub var ai_calls:u64=0;pub var habitat_ns:i128=0;pub var habitat_calls:u64=0;pub var density_checks:u64=0;pub var mate_checks:u64=0;
pub fn reset(on:bool)void{enabled=on;nearest_ns=0;nearest_calls=0;ai_ns=0;ai_calls=0;habitat_ns=0;habitat_calls=0;density_checks=0;mate_checks=0;}
pub fn now()i128{return if(enabled) std.time.nanoTimestamp() else 0;}
''')
p=o/'simulation/life.zig';s=p.read_text();s='const QA=@import("../qa_rabbit_cost.zig");\n'+s
s=s.replace('const idx = planet.getNearestPointTo(self.position);','''const qa_ai=QA.now();defer {if(QA.enabled){QA.ai_ns+=QA.now()-qa_ai;QA.ai_calls+=1;}}
        const qa_nearest=QA.now();const idx = planet.getNearestPointTo(self.position);
        if(QA.enabled){QA.nearest_ns+=QA.now()-qa_nearest;QA.nearest_calls+=1;}''')
s=s.replace('var food = planet.vegetation[idx];','const qa_habitat=QA.now();defer {if(QA.enabled){QA.habitat_ns+=QA.now()-qa_habitat;QA.habitat_calls+=1;}}\n        var food = planet.vegetation[idx];')
s=s.replace('for (planet.lifeforms.items) |other| {','for (planet.lifeforms.items) |other| {\n            if(QA.enabled)QA.density_checks+=1;')
s=s.replace('for (planet.lifeforms.items) |*other| {','for (planet.lifeforms.items) |*other| {\n                if(QA.enabled)QA.mate_checks+=1;');p.write_text(s)
p=o/'main.zig';s=p.read_text();a=s.index('          _=pm;_=pw;');b=s.index('\n        std.debug.print("FORAGING_PRODUCTION_COMPLETE',a)
s=s[:a]+r'''
          _=pm;_=pw;std.debug.assert(state.planet.worldMode==.sandbox);const QA=@import("qa_rabbit_cost.zig");
          const original=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const initial=try std.json.parseFromSlice(saves.schema.Save,a,original,.{.allocate=.alloc_always});
          var reference:[]const u8="";
          for([_]bool{false,true,true,false},0..)|on,arm|{
            try saves.apply(state,initial.value);QA.reset(false);
            for(0..12)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
            const rabbits_before=state.planet.lifeforms.items.len;QA.reset(on);var ticks:[60]u64=undefined;
            for(0..60)|i|{var timer=try std.time.Timer.start();state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;ticks[i]=timer.read();}
            const endpoint=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});if(reference.len==0)reference=endpoint;std.debug.assert(std.mem.eql(u8,reference,endpoint));
            std.debug.print("RABBIT_COST {s}\n",.{try std.json.stringifyAlloc(a,.{.arm=arm,.instrumented=on,.cells=state.planet.transformedPoints.len,.rabbits_before=rabbits_before,.rabbits_after=state.planet.lifeforms.items.len,.ticks_ns=ticks,.nearest_ns=QA.nearest_ns,.nearest_calls=QA.nearest_calls,.ai_ns=QA.ai_ns,.ai_calls=QA.ai_calls,.habitat_ns=QA.habitat_ns,.habitat_calls=QA.habitat_calls,.density_checks=QA.density_checks,.mate_checks=QA.mate_checks,.fullsave_rng_exact=true},.{})});
          }
          QA.reset(false);try saves.apply(state,initial.value);std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.print("RABBIT_COST_PASS original_restored=true no_algorithm_changes=true native_only=true\n",.{});
        }
'''+s[b:];p.write_text(s)
(o.parent/'cost-provenance.json').write_text(json.dumps({'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip(),'input_sha256':hashlib.sha256((r.parent/'site-tmp/foraging-production/warm-actual-end.json').read_bytes()).hexdigest(),'source':{str(f.relative_to(o)):hashlib.sha256(f.read_bytes()).hexdigest()for f in o.rglob('*.zig')}},indent=2))
