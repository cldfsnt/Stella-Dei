#!/usr/bin/env python3
"""Verify live guide progression and actual animal status through the intervention."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2]
out=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/stella-feedback-src')
subprocess.run([sys.executable,str(root/'web/tests/egl-intervention-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text()
s=s.replace('/tmp/stella-intervention-save.json','/tmp/stella-feedback-save.json')
s=s.replace('            const i = state.selectedPoint;',r'''            const feedback=@import("habitat_feedback.zig");
            const f=feedback.facts(state.planet);
            const goal=feedback.stage(f);
            std.debug.print("GOAL frame={d} stage={s} planted={} grown={} descendants={} rabbits={d} meals={d} births={d} instruction={s}\n",.{frame,@tagName(goal),f.planted,f.grown,f.descendants,f.rabbits,f.meals,f.births,feedback.instruction(f)});
            if(frame==55)std.debug.assert(goal==.add_pair);
            if(frame==75)std.debug.assert(goal==.feeding);
            if(frame==76)std.debug.assert(goal==.offspring);
            if(frame==78)std.debug.assert(goal==.living);
            if(frame==80)std.debug.assert(goal==.plant);
            if(frame==85)std.debug.assert(goal==.living);
            for(state.planet.lifeforms.items,0..) |_,index| {
                const status=feedback.inspectRabbit(state.planet,index,state.gameTime).?;
                std.debug.print("ANIMAL index={d} label={s} fullness={d:.2} age_hours={d:.2} gestation_hours={?d} cooldown_hours={d:.2}\n",.{index,@tagName(status.label),status.fullness,status.age_hours,status.gestation_hours,status.cooldown_hours});
            }
            const i = state.selectedPoint;''')
s=s.replace('.Playing => |*state| {', '.Playing => |*state| {\n            state.showPointDetails=false;')
s=s.replace('            const i = state.selectedPoint;', r'''            if ((frame==76 or frame==82) and state.planet.lifeforms.items.len>0) {
                state.clickedPoint=state.planet.getNearestPointTo(state.planet.lifeforms.items[0].position);
                state.showPointDetails=true;
                state.inspectAnimal=true;
                render(game.window);
            }
            const i = state.selectedPoint;''')
p.write_text(s)
