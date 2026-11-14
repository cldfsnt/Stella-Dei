#!/usr/bin/env python3
"""Actual rendered marker centers plus offset pointer callbacks, no fake biology."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-prepare.py'),str(out),'--mobile','--paused'],check=True)
p=out/'main.zig';s=p.read_text();s+='\nextern fn qa_click(x:f64,y:f64) void;\n';marker='            const i = state.selectedPoint;'
hook=r'''            if(frame==25){
                state.planet.beginOrigin() catch unreachable;
                std.debug.assert(state.focusSeedableHabitat());
                std.debug.assert(state.makeSelectedPond(@intCast(state.selectedPoint))>0);
                state.selectedTool=.PlaceVegetation;state.showPointDetails=false;
            }
            if(frame==45){
                const list=state.seedTargets;
                std.debug.assert(list.count>0);
                const offsets=[_][2]f32{.{0,0},.{22,0},.{-22,0},.{0,22},.{0,-22},.{16,16}};
                for(offsets)|offset|{
                    var tested=false;
                    for(list.items[0..list.count])|target|{
                        if(state.planet.seedEligibility(target.cell)!=.eligible)continue;
                        const x=target.x+offset[0];const y=target.y+offset[1];
                        if(state.pickSeedTarget(x,y)!=target.cell)continue;
                        const before=@import("simulation/microbes.zig").biomass(state.planet.microbeCells[target.cell]);
                        const lineage=state.planet.microbeStats.next_lineage;
                        qa_click(x,y);
                        std.debug.assert(state.selectedPoint==target.cell);
                        std.debug.assert(state.planet.microbeStats.next_lineage==lineage+1);
                        std.debug.assert(@import("simulation/microbes.zig").biomass(state.planet.microbeCells[target.cell])>before);
                        std.debug.print("SEED_HIT actual_callback=true cell={d} x={d} y={d} offset={d},{d} exactly_one=true\n",.{target.cell,x,y,offset[0],offset[1]});
                        tested=true;break;
                    }
                    std.debug.assert(tested);
                }
                // Outside every visible hit region never falls back to ray seeding.
                var rejected=false;
                var y:f32=195;while(y<580):(y+=25){var x:f32=30;while(x<360):(x+=25){
                    if(state.pickSeedTarget(x,y)!=null)continue;
                    const lineage=state.planet.microbeStats.next_lineage;qa_click(x,y);
                    std.debug.assert(state.planet.microbeStats.next_lineage==lineage);rejected=true;break;
                }if(rejected)break;}
                std.debug.assert(rejected);
                // A marker whose slots fill after rendering rejects, never redirects.
                const target=list.items[0];
                while(state.planet.seedEligibility(target.cell)==.eligible){state.selectedPoint=target.cell;_=state.seedSelectedColony(@intCast(target.cell));}
                const lineage=state.planet.microbeStats.next_lineage;qa_click(target.x,target.y);
                std.debug.assert(state.planet.microbeStats.next_lineage==lineage);
                std.debug.assert(state.selectedPoint==target.cell);
                std.debug.print("SEED_HIT outside_rejected=true stale_full_rejected=true wrong_cell_seeds=0\n",.{});
            }
'''
assert marker in s;s=s.replace(marker,hook+marker);p.write_text(s)
