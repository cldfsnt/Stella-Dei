#!/usr/bin/env python3
"""Isolated history schematic, actual natural60 cohorts, matched rendering/save gate."""
from pathlib import Path
import sys,shutil
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve();shutil.copytree(r.parent/'site-tmp/retention-overhead/baseline/src',o,dirs_exist_ok=True)
shutil.copyfile(r/'src/experimental/feeding_marker.zig',o/'feeding_marker.zig')
p=o/'states/play.zig';s=p.read_text();s='pub var qa_history_marker:bool=false;\n'+s;s=s.replace('    fn setOrbitDistance(', '    pub fn setOrbitDistance(')
needle='''                if (biology_visuals.hasFed(self.planet.microbeCells[index].cohorts)) {
                    vg.beginPath(); vg.fillColor(nvg.rgb(255,191,89)); vg.circle(12,0,3); vg.fill();
                }'''
replacement='''                if (qa_history_marker) {
                    const history=@import("../feeding_marker.zig").classify(self.planet.microbeCells[index].cohorts);
                    // Patch-level historical evidence, not animal anatomy or current eating.
                    if(history==.dominant){
                        vg.beginPath();vg.fillColor(nvg.rgba(247,177,65,235));vg.strokeColor(nvg.rgb(66,38,12));vg.strokeWidth(1.7);
                        vg.ellipse(-7,2,6,4.5);vg.ellipse(0,4,6,4.5);vg.ellipse(7,2,6,4.5);vg.fill();vg.stroke();
                        vg.beginPath();vg.strokeColor(nvg.rgb(255,230,166));vg.strokeWidth(1.2);vg.moveTo(-8,2);vg.lineTo(-5,2);vg.moveTo(-1,4);vg.lineTo(2,4);vg.moveTo(6,2);vg.lineTo(9,2);vg.stroke();
                    }else if(history==.mixed){
                        vg.beginPath();vg.strokeColor(nvg.rgb(57,34,13));vg.strokeWidth(4);vg.circle(12,0,4.5);vg.stroke();
                        vg.strokeColor(nvg.rgb(255,191,89));vg.strokeWidth(2);vg.stroke();
                    }
                }else if (biology_visuals.hasFed(self.planet.microbeCells[index].cohorts)) {
                    vg.beginPath(); vg.fillColor(nvg.rgb(255,191,89)); vg.circle(12,0,3); vg.fill();
                }'''
assert s.count(needle)==1;s=s.replace(needle,replacement)
s=s.replace('vg.ellipse(0,4,6,4.5)','vg.ellipse(0,3,6,4)')
s=s.replace('        var count: usize = if(wide)', '        const selected_first:?usize=if(qa_history_marker and wide and self.planet.worldMode==.origin and self.selectedPoint<self.planet.microbeCells.len and Microbes.biomass(self.planet.microbeCells[self.selectedPoint])>=0.001)self.selectedPoint else null;\n        var count: usize = if(wide)',1)
s=s.replace('const index = if(wide) cursor else candidates[cursor];','const index = if(wide) @import("../feeding_marker.zig").orderedIndex(cursor,count,selected_first) else candidates[cursor];',1)
s=s.replace('            const size = (if (origin)', '            const glyph_lod=if(qa_history_marker and origin and index==self.selectedPoint)@max(lod,0.75) else lod;\n            const size = (if (origin)',1)
s=s.replace('if (x < size + 4 or', 'if (qa_history_marker and origin and index==self.selectedPoint and !@import("../feeding_marker.zig").fits(x,y,glyph_lod,width,height,toolBottom))continue;\n            if (x < size + 4 or',1)
s=s.replace('.cell=index,.x=x,.y=y,.scale=lod','.cell=index,.x=x,.y=y,.scale=glyph_lod',1)
s=s.replace('vg.save(); vg.translate(x,y); vg.scale(lod,lod);','vg.save(); vg.translate(x,y); vg.scale(glyph_lod,glyph_lod);',1)
s=s.replace('        var screenPositions: [64]Vec2 = undefined;', '        var screenPositions: [64]Vec2 = undefined;\n        var screenScales: [64]f32 = undefined;\n        var screenSelected: [64]bool = undefined;',1)
s=s.replace('for (screenPositions[0..self.visibleSprouts]) |prior| { if (screen.distance(prior) < @max(14,38*lod)) { crowded = true; break; } }','for (screenPositions[0..self.visibleSprouts],0..) |prior,pi| {\n                const selected_pair=qa_history_marker and ((origin and index==self.selectedPoint) or screenSelected[pi]);\n                if (screen.distance(prior) < @max(14,38*lod) or (selected_pair and @import("../feeding_marker.zig").overlaps(x,y,glyph_lod,prior.x(),prior.y(),screenScales[pi]))) { crowded = true; break; }\n            }',1)
s=s.replace('            screenPositions[self.visibleSprouts] = screen;', '            screenPositions[self.visibleSprouts] = screen;\n            screenScales[self.visibleSprouts] = glyph_lod;\n            screenSelected[self.visibleSprouts] = origin and index==self.selectedPoint;',1)
s=s.replace('const selected_first:?usize=if(qa_history_marker and wide and self.planet.worldMode','const selected_first:?usize=if(qa_history_marker and self.planet.worldMode',1)
s=s.replace('        var cursor: usize = 0;\n        while (cursor < count and self.visibleSprouts < screenPositions.len) : (cursor += 1) {\n            const index = if(wide) @import("../feeding_marker.zig").orderedIndex(cursor,count,selected_first) else candidates[cursor];','        var cursor: usize = 0;\n        var selected_pending = !wide and selected_first != null;\n        while ((selected_pending or cursor < count) and self.visibleSprouts < screenPositions.len) {\n            const prioritized = selected_pending;\n            selected_pending = false;\n            const index = if(prioritized) selected_first.? else if(wide) @import("../feeding_marker.zig").orderedIndex(cursor,count,selected_first) else candidates[cursor];\n            if(!prioritized)cursor+=1;',1)
s=s.replace('            if (!wide) for (self.planet.getNeighbours(index))','            if (!wide and !prioritized) for (self.planet.getNeighbours(index))',1)
s=s.replace('            const origin = self.planet.worldMode == .origin;','            if(!prioritized and !wide and selected_first!=null and index==selected_first.?)continue;\n            const origin = self.planet.worldMode == .origin;',1)
s=s.replace('    /// Close view scans <=512 neighbours; globe view scans real living cells.','    /// Close view scans <=512 neighbours plus selected patch; globe scans real living cells.',1)
p.write_text(s)
p=o/'main.zig';s=p.read_text();start=s.index('          _=pm;\n          const frozen=');end=s.index('\n        try originSaveCheck',start)
block=r'''
          _=pm;const visual=@import("feeding_marker.zig");const play=@import("states/play.zig");
          const original=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const baseline=try std.json.parseFromSlice(saves.schema.Save,a,original,.{.allocate=.alloc_always});
          for([_]visual.Kind{.none,.mixed,.dominant})|kind|{
            try saves.apply(state,baseline.value);var selected:?usize=null;
            for(state.planet.microbeCells,0..)|cell,i|{if(micro.biomass(cell)>0.005 and visual.classify(cell.cohorts)==kind and @abs(state.planet.transformedPoints[i].norm().z())<0.9){selected=i;break;}}
            const cell=selected orelse {std.debug.print("FEEDING_VISUAL_MISSING kind={s}\n",.{@tagName(kind)});continue;};
            state.paused=true;state.watchLife();state.displayMode=.Normal;state.selectedPoint=cell;state.clickedPoint=cell;state.pointerOnPlanet=true;state.targetCameraPos=state.planet.transformedPoints[cell].norm();state.setOrbitDistance(if(std.posix.getenv("QA_MARKER_GLOBE")!=null)state.planet.radius*2.5 else state.planet.transformedPoints[cell].length()+900,true);state.cameraGroundPoint=cell;
            for(0..16)|_|{game.loop.pump(16);render(window);window.swapBuffers();}
            const framed=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const owned=try std.json.parseFromSlice(saves.schema.Save,a,framed,.{.allocate=.alloc_always});var first:?[]const u8=null;
            for([_]bool{false,true})|candidate|{
              try saves.apply(state,owned.value);state.selectedPoint=cell;state.clickedPoint=cell;state.pointerOnPlanet=true;state.cameraGroundPoint=cell;play.qa_history_marker=candidate;
              render(window);gl.finish();window.swapBuffers();std.debug.print("SELECTED_DIAGNOSTIC expected={d} actual={d} ground={d}\n",.{cell,state.selectedPoint,state.cameraGroundPoint});var found=false;for(state.colonyTargets.items[0..state.colonyTargets.count])|target|{if(target.cell==cell){found=true;std.debug.print("EDGE_DIAGNOSTIC selected={d} expected={d} root={any} left={any} right={any}\n",.{state.selectedPoint,cell,state.colonyTargets.pick(target.x,target.y),state.colonyTargets.pick(target.x-21.5*target.scale,target.y-10*target.scale),state.colonyTargets.pick(target.x+21.5*target.scale,target.y-10*target.scale)});if(candidate){std.debug.assert(state.colonyTargets.pick(target.x,target.y)==cell);std.debug.assert(state.colonyTargets.pick(target.x-21.5*target.scale,target.y-10*target.scale)==cell);std.debug.assert(state.colonyTargets.pick(target.x+21.5*target.scale,target.y-10*target.scale)==cell);}std.debug.print("FEEDING_VISUAL_TARGET kind={s} x={d} y={d} scale={d}\n",.{@tagName(kind),target.x,target.y,target.scale});}}if(candidate or std.posix.getenv("QA_MARKER_GLOBE")==null)std.debug.assert(found);std.debug.assert(state.colonyTargets.count<=64);std.debug.print("FEEDING_GLOBE selected_glyph_visible={}\n",.{found});
              const prefix=std.posix.getenv("STELLA_EGL_CAPTURE_PREFIX").?;const path=try std.fmt.allocPrintZ(a,"{s}-{s}-{s}.png",.{prefix,@tagName(kind),if(candidate)"candidate" else "baseline"});qa_capture(path);
              const after=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});if(first)|expected|{std.debug.assert(std.mem.eql(u8,expected,after));}else first=after;
              std.debug.print("FEEDING_VISUAL kind={s} candidate={} cell={d} biomass={d} glyphs={d} time={d}\n",.{@tagName(kind),candidate,cell,micro.biomass(state.planet.microbeCells[cell]),state.colonyTargets.count,state.gameTime});
            }
            state.targetCameraPos=state.planet.transformedPoints[cell].norm().negate();state.setOrbitDistance(state.cameraDistance,true);play.qa_history_marker=true;
            render(window);gl.finish();window.swapBuffers();for(state.colonyTargets.items[0..state.colonyTargets.count])|target|std.debug.assert(target.cell!=cell);
            std.debug.print("FEEDING_HIDDEN selected_backface_no_target=true kind={s}\n",.{@tagName(kind)});
          }
          try saves.apply(state,baseline.value);std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));std.debug.print("FEEDING_VISUAL_PASS actual_saved_world=true matched_full_save=true original_restored=true\n",.{});
        }
'''
s=s[:start]+block+s[end:];p.write_text(s)
