#!/usr/bin/env python3
"""Capture first actual paid arrival/loss in ordinary coupled nursery run."""
from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent;out=Path(sys.argv[1])
subprocess.run([sys.executable,str(here/'egl-propagule-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text();s+='\nextern fn qa_capture(path:[*:0]const u8) void;\n'
needle='        var update_total_ns:u64=0;';assert needle in s;s=s.replace(needle,'        var captured_arrival=false;var captured_failure=false;var last_visual_event:u64=0;\n'+needle,1)
needle='            const tick_ns=tick_timer.read();';assert needle in s
hook=r'''            const newest=state.planet.propaguleFeedback.next_serial-1;
            if(newest>last_visual_event){
                for(state.planet.propaguleFeedback.events)|event|{
                    if(event.serial<=last_visual_event or event.serial>newest)continue;
                    const arrival=event.kind==.arrival;
                    if((arrival and captured_arrival) or (!arrival and captured_failure))continue;
                    // Follow the real event with the camera only. Biology is untouched.
                    const point=state.planet.transformedPoints[event.cell];
                    state.cameraPos=point.norm().scale(state.planet.radius+900);
                    state.targetCameraPos=point.norm().scale(state.planet.radius+900);state.cameraDistance=state.planet.radius+900;state.targetCameraDistance=state.cameraDistance;
                    state.selectedTool=.None;state.pointerOnPlanet=false;
                    render(window);gl.finish();
                    qa_capture(if(arrival) "/tmp/stella-propagule-arrival.ppm" else "/tmp/stella-propagule-failed.ppm");
                    std.debug.print("PROPAGULE_VISUAL actual_kind={s} lineage={d} from={d} to={d} day={d}\n",.{@tagName(event.kind),event.lineage,event.from,event.cell,event.sim_time/86400});
                    if(arrival)captured_arrival=true else captured_failure=true;
                }
                last_visual_event=newest;
            }
'''
s=s.replace(needle,hook+needle,1);p.write_text(s)
