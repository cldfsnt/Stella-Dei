"""Isolated legitimate prior-view geometry -> load -> one physics tick witness."""
from pathlib import Path
import subprocess,sys,json,hashlib
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1]);subprocess.run([sys.executable,str(root/'web/tests/egl-natural60-prepare.py'),str(out)],check=True)
(out/'simulation/planet.zig').write_text((root/'src/simulation/planet.zig').read_text())
p=out/'main.zig';s=p.read_text();start=s.index('          const start_time=state.gameTime;');end=s.index('\n        try originSaveCheck',start)
s=s[:start]+r'''
          _=micro;
          const frozen=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const target=try std.json.parseFromSlice(saves.schema.Save,a,frozen,.{.allocate=.alloc_always});
          var results:[2][]const u8=undefined;
          for(0..2)|arm|{
            // Legitimate prior world: editable tilt and the ordinary terrain brush,
            // followed by a real render. No manual writes to derived geometry.
            try saves.apply(state,target.value);state.paused=true;state.axialTilt=45;
            state.selectedPoint=12352;state.pointerOnPlanet=true;std.debug.assert(state.testAction(5));
            render(window);gl.finish();window.swapBuffers();game.loop.pump(1024);
            try saves.apply(state,target.value);
            const restored=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
            std.debug.assert(std.mem.eql(u8,frozen,restored));
            const prior=state.planet.transformedPoints[12352];
            if(arm==0){state.planet.upload(game.loop,state.displayMode,state.axialTilt);game.loop.pump(1024);}
            const actual=state.planet.transformedPoints[12352];
            // Upload changes only derived/render state, never the saved model.
            std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
            std.debug.print("LOAD_GEOMETRY arm={d} refreshed={} point_before={any} point_after={any} old_state_exact=true\n",.{arm,arm==0,prior.data,actual.data});
            state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;
            results[arm]=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
            const name=try std.fmt.allocPrint(a,"OUTPUT/arm-{d}.json",.{arm});try std.fs.cwd().writeFile(.{.sub_path=name,.data=results[arm]});
          }
          std.debug.print("LOAD_GEOMETRY_RESULT full_saved_state_equal={} partitions={d}\n",.{std.mem.eql(u8,results[0],results[1]),game.loop.getParallelCount()});
          try saves.apply(state,target.value);state.planet.upload(game.loop,state.displayMode,state.axialTilt);game.loop.pump(1024);
          std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.print("LOAD_GEOMETRY_RESTORED true\n",.{});
        }
'''.replace('OUTPUT',str(out.parent))+s[end:]
# Undo the inherited unrelated legacy nursery substitution in the pond export.
def body(t,name):
 a=t.index('export fn '+name+'(');b=t.index('{',a);depth=1;i=b+1
 while depth:depth+=(t[i]=='{')-(t[i]=='}');i+=1
 return a,i,t[a:i]
original=(root/'src/main.zig').read_text();a,b,_=body(s,'stella_make_pond');s=s[:a]+body(original,'stella_make_pond')[2]+s[b:];p.write_text(s)
subprocess.run([sys.executable,str(root/'web/tests/audit-zig-exports.py'),str(root/'src/main.zig'),str(p)],check=True)
(out.parent/'provenance.json').write_text(json.dumps({'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'files':{str(x.relative_to(root)):hashlib.sha256(x.read_bytes()).hexdigest() for x in [root/'src/save_game.zig',root/'src/simulation/planet.zig',root/'src/states/play.zig',root/'src/main.zig']},'copy_main':hashlib.sha256(p.read_bytes()).hexdigest()},indent=2)+'\n')
