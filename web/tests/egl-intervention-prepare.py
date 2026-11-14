#!/usr/bin/env python3
"""Actual handlers + full simulation ecological disturbance and recovery scenario."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2]
out=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/stella-intervention-src')
subprocess.run([sys.executable,str(root/'web/tests/egl-prepare.py'),str(out),'--mobile','--paused','--ecosystem'],check=True)
p=out/'main.zig';s=p.read_text()
s=s.replace('const goal = state.gameTime + 43200;', 'const goal = state.gameTime + @as(f64, if (frame == 79 or frame == 80) 43200 else 86400);')
s=s.replace('/tmp/stella-day5-save.json','/tmp/stella-intervention-save.json')
marker='            if (frame >= 76 and frame <= 85) {'
s=s.replace(marker,r'''            if (frame == 79) {
                const center = state.selectedPoint;
                var flooded: usize = 0;
                for (state.planet.vegetation, 0..) |cover, idx| {
                    if (cover < 0.01) continue;
                    state.selectedPoint = idx;
                    state.pointerOnPlanet = true;
                    // Ten ordinary 1m Water+ tap actions per planted cell.
                    for (0..10) |_| _ = state.testAction(1);
                    flooded += 1;
                }
                state.selectedPoint = center;
                std.debug.print("INTERVENTION flood cells={d} center_depth_m={d:.3}\n", .{flooded, state.planet.waterMass[center]*state.planet.getKmPerWaterMass()*1000});
            }
            if (frame == 81) {
                const center = state.selectedPoint;
                // Drain the local patch through the same editor handler.
                _ = state.testAction(2);
                for (state.planet.getNeighbours(center)) |idx| { state.selectedPoint = idx; _ = state.testAction(2); }
                state.selectedPoint = center;
                _ = state.testAction(3);
                state.selectedTool = .PlaceLife;
                state.pointerOnPlanet = true;
                state.mousePressed(&game, .left);
                std.debug.print("INTERVENTION recover depth_m={d:.3} cover={d:.3} rabbits={d}\n", .{state.planet.waterMass[center]*state.planet.getKmPerWaterMass()*1000,state.planet.vegetation[center],state.planet.lifeforms.items.len});
            }
'''+marker)
p.write_text(s)

# Expose the unchanged shared handler only in the isolated native QA copy.
p=out/'states/play.zig';p.write_text(p.read_text().replace('    fn applySelectedTool(', '    pub fn applySelectedTool('))
p=out/'main.zig';s=p.read_text()
s=s.replace('            if (frame == 75) {', r'''            if (frame == 75) {
                const center = state.selectedPoint;
                const scale = state.timeScale;
                const original_height = state.planet.elevation[center];
                var neighbor_heights: [6]f32 = undefined;
                const ns = state.planet.getNeighbours(center);
                for (ns,0..) |n,k| neighbor_heights[k]=state.planet.elevation[n];
                for ([_]u32{15,60}) |fps| {
                    for ([_]f32{3600,86400}) |speed| {
                        state.timeScale=speed;
                        state.pointerOnPlanet=true;
                        _=state.testAction(2);
                        _=state.testAction(1);
                        _=state.testAction(5);
                        for (0..fps*2) |_| {
                            _=state.applySelectedTool(.EmitWater,false,1/@as(f32,@floatFromInt(fps)));
                            _=state.applySelectedTool(.RaiseTerrain,false,1/@as(f32,@floatFromInt(fps)));
                        }
                        const depth=state.planet.waterMass[center]*state.planet.getKmPerWaterMass();
                        const raised=state.planet.elevation[center]-original_height;
                        std.debug.assert(@abs(depth-0.011)<0.000001);
                        std.debug.assert(@abs(raised-1.1)<0.03); // f32 terrain coordinates near5000km
                        std.debug.print("BRUSH_HOLD PASS fps={d} speed={d} water_m={d:.4} raised_m={d:.3}\n",.{fps,speed,depth*1000,raised*1000});
                        _=state.testAction(2);
                        state.planet.elevation[center]=original_height;
                        for(ns,0..) |n,k| state.planet.elevation[n]=neighbor_heights[k];
                    }
                }
                state.timeScale=scale;
            }
            if (frame == 75) {''')
p.write_text(s)
