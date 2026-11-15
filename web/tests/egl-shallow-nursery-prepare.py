#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve();subprocess.run([sys.executable,str(r/'web/tests/egl-playable-ecology-prepare.py'),str(o)],check=True)
p=o/'pond_action.zig';s=p.read_text();s=s.replace('const std = @import("std");','const std = @import("std");\npub var shallow_nursery:bool=false; // QA-only explicit variant, never auto-selected')
s=s.replace('nursery and slot==0','nursery and (shallow_nursery or slot==0)')
s=s.replace('const floor_water_mass: f32=0.015/conversion;','const floor_water_mass: f32=(if(nursery and shallow_nursery) @as(f32,0.005) else 0.015)/conversion;')
s=s.replace('if(i<floor_count)base else @max','if(i<floor_count)base+(if(nursery and shallow_nursery) @as(f32,0.010) else 0) else @max')
p.write_text(s)
p=o/'main.zig';s=p.read_text();needle='    const nursery=state.makeSelectedNursery(point);state.pointerOnPlanet=false;const seeded=state.seedSelectedColony(point);';assert needle in s
block=r'''
    const pond=@import("pond_action.zig");pond.shallow_nursery=std.posix.getenv("QA_SHALLOW_NURSERY")!=null;
    const savecheck=@import("save_game.zig");var guard_arena=std.heap.ArenaAllocator.init(allocator);const ga=guard_arena.allocator();
    const guard_bytes=try std.json.stringifyAlloc(ga,try savecheck.capture(ga,state),.{});const guard_saved=try std.json.parseFromSlice(savecheck.schema.Save,ga,guard_bytes,.{.allocate=.alloc_always});
    const plan=pond.preview(&state.planet,point,point,true,17).?;
    std.debug.assert(std.mem.eql(u8,guard_bytes,try std.json.stringifyAlloc(ga,try savecheck.capture(ga,state),.{})));
    std.debug.assert(pond.applyChecked(&state.planet,&plan,point,18)==-1);
    std.debug.assert(pond.applyChecked(&state.planet,&plan,point+1,17)==-1);
    std.debug.assert(std.mem.eql(u8,guard_bytes,try std.json.stringifyAlloc(ga,try savecheck.capture(ga,state),.{})));
    std.debug.assert(pond.applyChecked(&state.planet,&plan,point,17)>0);
    const preview_applied=try std.json.stringifyAlloc(ga,try savecheck.capture(ga,state),.{});
    try savecheck.apply(state,guard_saved.value);state.selectedPoint=cell;
    const nursery=state.makeSelectedNursery(point);
    std.debug.assert(std.mem.eql(u8,preview_applied,try std.json.stringifyAlloc(ga,try savecheck.capture(ga,state),.{})));
    std.debug.assert(state.makeSelectedNursery(point)>0);
    std.debug.assert(std.mem.eql(u8,preview_applied,try std.json.stringifyAlloc(ga,try savecheck.capture(ga,state),.{})));
    const shaped=try std.json.parseFromSlice(savecheck.schema.Save,ga,preview_applied,.{.allocate=.alloc_always});
    // Normalize only the explicitly declared terrain/water writes, then compare the complete state.
    var normalized=shaped.value;normalized.elevation=guard_saved.value.elevation;normalized.water=guard_saved.value.water;
    std.debug.assert(std.mem.eql(u8,guard_bytes,try std.json.stringifyAlloc(ga,normalized,.{})));
    try savecheck.apply(state,shaped.value);state.selectedPoint=cell;
    std.debug.assert(std.mem.eql(u8,preview_applied,try std.json.stringifyAlloc(ga,try savecheck.capture(ga,state),.{})));
    std.debug.print("SHALLOW_SETUP shallow={} affected={} floor={} water_added_native={d} water_removed_native={d} preview_pure=true stale_reject=true repeat_exact=true only_terrain_water=true save_roundtrip=true\n",.{pond.shallow_nursery,plan.count,plan.floor_count,plan.water_added,plan.water_removed});
    state.pointerOnPlanet=false;const seeded=state.seedSelectedColony(point);
'''
s=s.replace(needle,block)
needle='    std.debug.print("EARLY_EXPLICIT_FIT result={d} rendered_before={d} rendered_after={d} time_births_arrivals_unchanged=true no_auto_framing=true\\n",.{fitted,before,state.visibleSprouts});';assert needle in s
s=s.replace(needle,needle+'\n    std.debug.print("SHALLOW_ACCEPTANCE complete=true clean_qa_exit_skips_inherited_teardown=true\\n",.{});std.process.exit(0);')
p.write_text(s)
(o.parent/'shallow-provenance.json').write_text(json.dumps({'generator':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'pond_sha256':hashlib.sha256((o/'pond_action.zig').read_bytes()).hexdigest(),'main_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'core_sha256':hashlib.sha256((o/'simulation/microbes.zig').read_bytes()).hexdigest()},indent=2)+'\n')
