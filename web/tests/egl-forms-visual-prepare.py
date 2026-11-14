#!/usr/bin/env python3
"""Controlled morphology rendering fixture, NOT evidence of evolution."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-prepare.py'),str(out),'--mobile','--paused'],check=True)
p=out/'main.zig';s=p.read_text();marker='            const i = state.selectedPoint;'
hook=r'''            if(frame==25){
                state.planet.beginOrigin() catch unreachable;_=state.focusHabitat();
                const center=state.selectedPoint;
                const normal=state.planet.transformedPoints[center].norm();
                const right=normal.cross(za.Vec3.forward()).norm();
                const up=right.cross(normal).norm();
                // Six separated real cells, not immediate neighbours hidden by LOD.
                for(0..6)|j|{
                    const angle=@as(f32,@floatFromInt(j))*std.math.pi/3;
                    const target=normal.add(right.scale(@cos(angle)*0.12)).add(up.scale(@sin(angle)*0.12)).norm();
                    var n:usize=center;var best:f32=-2;
                    for(state.planet.transformedPoints,0..)|point,index|{
                        const score=point.norm().dot(target);if(score>best){best=score;n=index;}
                    }
                    var c: @import("simulation/microbes.zig").Cohort=.{.biomass=0.65,.support_mass=0.1,.organization=0.08,.lineage=j+1,.generation=8};
                    switch(j%6){0=>c.support_mass=0,1=>c.organization=0.01,2=>{},3=>c.efficiency=0.9,4=>c.structure=0.2,5=>c.efficiency=1.1,else=>unreachable}
                    state.planet.microbeCells[n].cohorts[0]=c;
                }
                state.planet.microbeStats.next_lineage=99;
                std.debug.print("CONTROLLED_RENDER_FIXTURE six_forms=true not_evolution_evidence=true\n",.{});
            }
            if(frame==45){state.targetCameraDistance=state.planet.radius*1.6;}
            if(frame==85){state.targetCameraDistance=state.planet.radius+900;}
'''
s=s.replace(marker,hook+marker);p.write_text(s)
