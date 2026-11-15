#!/usr/bin/env python3
"""Final production feeding replay versus frozen experiment, then true continuation."""
from pathlib import Path
import sys,subprocess,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve();subprocess.run([sys.executable,str(r/'web/tests/egl-seed-target-toggle-prepare.py'),str(o)],check=True)
p=o/'main.zig';s=p.read_text().replace('try saves.apply(state,saved_parsed.value);state.paused=false;state.showEscapeMenu=false;', 'try saves.apply(state,saved_parsed.value);state.showEscapeMenu=false;');a=s.index('          _=pm;_=pw;');b=s.index('\n        std.debug.print("SEED_TARGET_COMPLETE',a)
s=s[:a]+r'''
          _=pm;_=pw;std.debug.assert(state.planet.worldMode==.sandbox);
          const original=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const initial=try std.json.parseFromSlice(saves.schema.Save,a,original,.{.allocate=.alloc_always});
          const expected_path=std.posix.getenv("QA_EXPECTED_END") orelse return error.ExpectedEndpointMissing;
          const expected_bytes=try std.fs.cwd().readFileAlloc(a,expected_path,128*1024*1024);
          const expected=try std.json.parseFromSlice(saves.schema.Save,a,expected_bytes,.{.allocate=.alloc_always});
          for(0..840)|_|{loop.pump(16);state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;loop.pump(16);}
          const actual=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          try std.fs.cwd().writeFile(.{.sub_path=std.posix.getenv("QA_ACTUAL_END") orelse "OUTPUT/actual-end.json",.data=actual});
          std.debug.assert(std.mem.eql(u8,actual,try std.json.stringifyAlloc(a,expected.value,.{})));
          const endpoint=try std.json.parseFromSlice(saves.schema.Save,a,actual,.{.allocate=.alloc_always});
          for(0..10)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
          const uninterrupted=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          try saves.apply(state,endpoint.value);std.debug.assert(std.mem.eql(u8,actual,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          for(0..10)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
          std.debug.assert(std.mem.eql(u8,uninterrupted,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          try saves.apply(state,endpoint.value);
          const center=try std.fmt.parseInt(usize,std.posix.getenv("QA_CENTER") orelse "436",10);state.selectedPoint=center;state.selectedTool=.None;state.showEscapeMenu=false;state.showPointDetails=false;state.showPlanetControl=false;
          const point=state.planet.transformedPoints[center];state.cameraPos=point.norm().scale(point.length()+200);state.targetCameraPos=state.cameraPos;state.cameraDistance=state.cameraPos.length();state.targetCameraDistance=state.cameraDistance;state.cameraGroundPoint=center;
          render(window);gl.finish();window.swapBuffers();qa_capture(std.posix.getenv("QA_FINAL_IMAGE") orelse "OUTPUT/final.ppm");
          std.debug.print("FORAGING_PRODUCTION_PASS input={s} expected_endpoint_exact=true endpoint_reload_exact=true uninterrupted_restored_10ticks_exact=true rabbits={} births={} deaths={}\n",.{std.posix.getenv("QA_PULSE_SAVE").?,state.planet.lifeforms.items.len,state.planet.rabbitBirths,state.planet.rabbitDeaths});
          try saves.apply(state,initial.value);std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
        }
''' .replace('OUTPUT',str(o.parent))+s[b:];s=s.replace('SEED_TARGET_COMPLETE','FORAGING_PRODUCTION_COMPLETE');p.write_text(s)
subprocess.run([sys.executable,str(r/'web/tests/audit-zig-exports.py'),str(r/'src/main.zig'),str(p)],check=True,stdout=(o.parent/'export-audit.json').open('w'))
(o.parent/'production-provenance.json').write_text(json.dumps({'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip(),'source':{f:{'production':hashlib.sha256((r/'src'/f).read_bytes()).hexdigest(),'copy':hashlib.sha256((o/f).read_bytes()).hexdigest()}for f in ['simulation/foraging.zig','simulation/life.zig','simulation/planet.zig','simulation/ecology.zig','main.zig']}},indent=2)+'\n')
