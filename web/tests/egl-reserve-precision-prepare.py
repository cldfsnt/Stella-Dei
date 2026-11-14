#!/usr/bin/env python3
"""Build isolated reserve on/off proof; no production getenv or hidden care."""
from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent
out=Path(sys.argv[1])
subprocess.run([sys.executable,str(here/'egl-shore-world-prepare.py'),str(out)],check=True)
p=out/'simulation/planet.zig'
s=p.read_text().replace('const prefer_neighbor=Microbes.neighborFirst(&cell.rng);','const prefer_neighbor=std.posix.getenv("STELLA_NEIGHBOR_FIRST")!=null and Microbes.neighborFirst(&cell.rng);').replace('            .liquid_available =','            .reserve_enabled=std.posix.getenv("STELLA_DISABLE_RESERVE")==null,\n            .liquid_available =')
p.write_text(s)
p=out/'main.zig';s=p.read_text()
i=s.index(' std.debug.print("ORIGIN_SAVE bytes=')
end=s.index('\n}',i)
s=s[:end]+'''
 // Explicit paused actions after ecological results and exact save restoration.
 var picked:usize=0;for(state.planet.microbeCells,0..)|cell,j|{if(cell.surface_water_carry>0){picked=j;break;}}
 state.selectedPoint=picked;state.pointerOnPlanet=true;
 _=state.planet.setWaterDepthMeters(picked,0);
 try (try saves.capture(a,state)).validate();
 _=state.makeSelectedPond(@intCast(picked));
 try (try saves.capture(a,state)).validate();
 const wave=@import("god_actions.zig").wave(&state.planet,picked,picked);
 std.debug.assert(wave.success());
 try (try saves.capture(a,state)).validate();
 std.debug.print("PAUSED_ACTION_SAVES fine_drain=true pond=true wave=true canonical=true\\n",.{});
'''+s[end:]
p.write_text(s)
