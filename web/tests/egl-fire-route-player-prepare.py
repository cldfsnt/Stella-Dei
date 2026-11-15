#!/usr/bin/env python3
"""Current finder to deliberate one-tap exposure and actual earned-fuel ignition."""
from pathlib import Path
import subprocess,sys,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve();subprocess.run([sys.executable,str(r/'web/tests/egl-fire-route-audit-prepare.py'),str(o)],check=True)
p=o/'main.zig';s=p.read_text();n='          try saves.apply(state,saved.value);std.debug.assert(std.mem.eql(u8,before,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));'
add=r'''
          std.debug.assert(result==3 and selected_depth>0 and selected_depth<=1);
          const wet_bytes=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const wet_save=try std.json.parseFromSlice(saves.schema.Save,a,wet_bytes,.{.allocate=.alloc_always});
          const blocked=state.applyIgnition(selected);std.debug.assert(!blocked.success());std.debug.assert(std.mem.eql(u8,wet_bytes,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          state.pointerOnPlanet=true;std.debug.assert(state.testAction(2));std.debug.assert(state.planet.waterMass[selected]==0);
          const dry_bytes=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const dry_save=try std.json.parseFromSlice(saves.schema.Save,a,dry_bytes,.{.allocate=.alloc_always});
          const water_check=try std.json.parseFromSlice(saves.schema.Save,a,dry_bytes,.{.allocate=.alloc_always});@constCast(water_check.value.water)[selected]=wet_save.value.water[selected];std.debug.assert(std.mem.eql(u8,wet_bytes,try std.json.stringifyAlloc(a,water_check.value,.{})));
          const preview=state.previewIgnition(selected);std.debug.assert(preview.success());std.debug.assert(std.mem.eql(u8,dry_bytes,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          const direct=@import("experimental/planet_ignition.zig").ignite(&state.planet,selected,selected);const direct_save=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          try saves.apply(state,dry_save.value);state.selectedPoint=selected;const burn=state.applyIgnition(selected);std.debug.assert(std.meta.eql(preview,burn) and std.meta.eql(direct,burn));std.debug.assert(std.mem.eql(u8,direct_save,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          const point=state.planet.transformedPoints[selected];state.cameraPos=point.norm().scale(point.length()+200);state.targetCameraPos=state.cameraPos;state.cameraDistance=state.cameraPos.length();state.targetCameraDistance=state.cameraDistance;state.showEscapeMenu=false;state.showPointDetails=false;state.showPlanetControl=false;
          render(window);gl.finish();window.swapBuffers();qa_capture("OUTPUT/ignited.ppm");
          const burned=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const burned_save=try std.json.parseFromSlice(saves.schema.Save,a,burned,.{.allocate=.alloc_always});try saves.apply(state,burned_save.value);std.debug.assert(std.mem.eql(u8,burned,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.print("FIRE_PLAYER_ROUTE_PASS selected={} one_actual_drain=true external_removed_native={d} fuel_kg={d} delta_K={d} preview_pure=true wet_refusal_pure=true selected_water_only=true exact_existing_ignition=true saved_roundtrip_exact=true\n",.{selected,wet_save.value.water[selected],burn.burned_carbon_kg,burn.temperature_delta});
'''.replace('OUTPUT',str(o.parent))+n
assert n in s;s=s.replace(n,add);p.write_text(s)
subprocess.run([sys.executable,str(r/'web/tests/audit-zig-exports.py'),str(r/'src/main.zig'),str(p)],check=True,stdout=(o.parent/'export-audit.json').open('w'))
(o.parent/'source-hashes.json').write_text(json.dumps({f:hashlib.sha256((o/f).read_bytes()).hexdigest()for f in ['main.zig','states/play.zig','detritus_finder.zig']},indent=2)+'\n')
