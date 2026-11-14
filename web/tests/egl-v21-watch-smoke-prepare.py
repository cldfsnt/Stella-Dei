#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-prepare.py'),str(out),'--mobile','--paused'],check=True)
p=out/'main.zig';s=p.read_text()+'\nvar watchSelected:usize=0;\n';s=s.replace('            const i = state.selectedPoint;',r'''            if(frame==25){
                state.planet.beginOrigin() catch unreachable;
                std.debug.assert(state.focusSeedableHabitat());
                std.debug.assert(state.makeSelectedPond(@intCast(state.selectedPoint))>0);
                std.debug.assert(state.seedSelectedColony(@intCast(state.selectedPoint))>0);
                const camera=state.targetCameraPos;const distance=state.targetCameraDistance;
                state.timeScale=21600;state.paused=true;
                state.watchLife();watchSelected=state.selectedPoint;
                std.debug.assert(state.watchLifeView and state.selectedTool==.None and state.seedTargets.count==0);
                std.debug.assert(state.targetCameraDistance==distance and state.targetCameraPos.eql(camera));
                std.debug.assert(state.paused and state.timeScale==21600);
            }
            if(frame==35 or frame==45 or frame==55 or frame==85)std.debug.assert(state.selectedPoint==watchSelected);
            if(frame==35){std.debug.assert(state.watchLifeView and !state.paused and !state.showPointDetails);std.debug.print("WATCH pause_button_actual=true no_inspect_clickthrough=true\n",.{});}
            if(frame==45){std.debug.assert(state.watchLifeView and state.paused);}
            if(frame==55){state.mobileFeedbackSeconds=0;std.debug.assert(state.watchLifeView and state.timeScale==86400 and !state.showPointDetails);std.debug.print("WATCH speed_button_actual=true compact=true\n",.{});}
            if(frame==59){std.debug.assert(state.watchLifeView);std.debug.print("WATCH_FOOTER actual_arrivals={d} tracked_losses={d} lifetime_births={d}\n",.{state.planet.propaguleArrivals,state.planet.propaguleTrackedLosses,state.planet.microbeStats.births});}
            if(frame==85){std.debug.assert(!state.watchLifeView and state.paused and state.timeScale==86400 and !state.showPointDetails);std.debug.print("WATCH tools_restores_full=true pause_and_pace_preserved=true\n",.{});}
            const i = state.selectedPoint;''');p.write_text(s)
