#!/usr/bin/env python3
"""Load actual baseline save, profile, then exercise geometry invalidations; copied sources only."""
from pathlib import Path
import shutil,sys
source=Path(sys.argv[1]);out=Path(sys.argv[2]);shutil.copytree(source,out,dirs_exist_ok=True)
p=out/'main.zig';s=p.read_text()
if '"{s}-{s}.json"' not in s:
 s=s.replace('  phase.enabled=false;', '  if(std.posix.getenv("STELLA_CPU_RESULT_PREFIX"))|prefix|{const name=try std.fmt.allocPrint(a,"{s}-{s}.json",.{prefix,label});try std.fs.cwd().writeFile(.{.sub_path=name,.data=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})});}\n  phase.enabled=false;',1)
needle='    var state = &game.state.Playing;';assert needle in s
s=s.replace(needle,needle+r'''
    if(std.posix.getenv("STELLA_CPU_LOAD"))|path|{
      const saves=@import("save_game.zig");var arena=std.heap.ArenaAllocator.init(allocator);defer arena.deinit();const a=arena.allocator();
      const bytes=try std.fs.cwd().readFileAlloc(a,path,128*1024*1024);const frozen=try saves.schema.parse(a,bytes);try saves.replaceWorld(state,frozen.value);
      render(window);gl.finish();window.swapBuffers();
      try profileFrames("loaded",state,window,allocator);
      if(std.posix.getenv("STELLA_CPU_INVALIDATE")!=null){
       for(0..4)|stage|{
        if(stage==0){state.selectedPoint=0;const old=state.planet.elevation[0];state.pointerOnPlanet=true;std.debug.assert(state.testAction(5));state.pointerOnPlanet=false;std.debug.assert(state.planet.elevation[0]>old);}
        if(stage==1){state.axialTilt+=0.17;}
        if(stage==2){state.selectedPoint=0;_=state.adjustSelectedWater(0,0.1);}
        if(stage==3){try saves.apply(state,frozen.value);}
        render(window);gl.finish();window.swapBuffers();
        for(0..3)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
        if(std.posix.getenv("STELLA_CPU_RESULT_PREFIX"))|prefix|{const name=try std.fmt.allocPrint(a,"{s}-invalidate{d}.json",.{prefix,stage});try std.fs.cwd().writeFile(.{.sub_path=name,.data=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})});}
       }
      }
      loop.pump(1024);return;
    }
''',1);p.write_text(s)
