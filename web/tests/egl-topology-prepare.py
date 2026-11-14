#!/usr/bin/env python3
"""Actual-engine topology6/new and v8 topology7 save compatibility QA."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2]
out=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/stella-topology-src')
subprocess.run([sys.executable,str(root/'web/tests/egl-prepare.py'),str(out),'--mobile','--paused'],check=True)
p=out/'main.zig';s=p.read_text().replace('            const i = state.selectedPoint;','            if (frame == 75) qa_topology(state) catch |err| @panic(@errorName(err));\n            const i = state.selectedPoint;')
s+=r'''
fn qa_topology(state: *PlayState) !void {
    const saves=@import("save_game.zig");
    var arena=std.heap.ArenaAllocator.init(game.allocator); defer arena.deinit();
    const a=arena.allocator();
    if(state.planet.numSubdivisions!=6 or state.planet.vertices.len!=40962) return error.NewWorldNotLightweight;
    const found=state.focusLand();
    if(!found) return error.NoLandInTestWorld;
    const originalDistance=state.targetCameraDistance;
    state.zoom(1);
    if(!(state.targetCameraDistance<originalDistance)) return error.ZoomNotCloser;
    state.resetView();
    _=state.focusLand();
    state.showEscapeMenu=false;state.showPlanetControl=false;state.showPointDetails=false;
    state.pointerOnPlanet=true;
    const beforeRabbits=state.planet.lifeforms.items.len;
    state.selectedTool=.PlaceLife;
    state.mousePressed(&game,.left);
    if(state.planet.lifeforms.items.len!=beforeRabbits+2) return error.RabbitPlacementFailed;
    if(!state.testAction(3)) return error.PlantBrushFailed;
    game.loop.pump(1024);
    const save6=try saves.capture(a,state);
    const bytes6=try std.json.stringifyAlloc(a,save6,.{});
    const parsed6=try saves.schema.parse(a,bytes6);
    const bytes7=try std.fs.cwd().readFileAlloc(a,"/tmp/stella-day5-topology7-save.json",128*1024*1024);
    const parsed7=try saves.schema.parse(a,bytes7);
    if(parsed7.value.subdivisions!=7) return error.ExpectedV8Save;
    const originalPointer=state.planet.elevation.ptr;
    {
        const priorJob=state.planet.normalComputeJob;
        const pending=try Job(void).create(game.loop);
        defer {state.planet.normalComputeJob=priorJob;pending.deinit();}
        state.planet.normalComputeJob=pending;
        if(saves.replaceWorld(state,parsed7.value)) |_| { return error.PendingJobLoadAccepted; } else |err| {
            if(err!=error.WorldBusy)return err;
        }
        if(state.planet.elevation.ptr!=originalPointer or state.planet.numSubdivisions!=6)return error.BusyLoadChangedLiveWorld;
    }
    var corrupt=parsed7.value;corrupt.elevation=corrupt.elevation[0..1];
    if(saves.replaceWorld(state,corrupt)) |_| { return error.CorruptSaveAccepted; } else |_| {}
    if(state.planet.elevation.ptr!=originalPointer or state.planet.numSubdivisions!=6) return error.FailedLoadChangedLiveWorld;
    const afterFailure=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
    if(!std.mem.eql(u8,bytes6,afterFailure))return error.FailedLoadChangedBytes;
    try saves.replaceWorld(state,parsed7.value);
    const restored7=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
    if(state.planet.vertices.len!=163842 or !std.mem.eql(u8,bytes7,restored7))return error.V8SaveChanged;
    // Force growth through the committed arena to detect stale allocator copies.
    const traitsBefore=state.planet.plantTraits[100];
    try state.planet.lifeforms.ensureTotalCapacity(state.planet.simulationArena.allocator(),state.planet.lifeforms.capacity+1000);
    if(!std.meta.eql(traitsBefore,state.planet.plantTraits[100]))return error.ArenaStorageOverlap;
    try saves.replaceWorld(state,parsed6.value);
    const restored6=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
    if(state.planet.vertices.len!=40962 or !std.mem.eql(u8,bytes6,restored6))return error.LightweightSaveChanged;
    std.debug.print("TOPOLOGY PASS new6=40962points dryland={} zoomcloser=true rabbitsadded=2; pendingjob rejected; invalid7 kept live6 exact; v8 saved7=163842points exactJSON={d}bytes; capacitygrowth kepttraits; restored6 exactJSON={d}bytes\n",.{found,bytes7.len,bytes6.len});
}
''';p.write_text(s)
