#!/usr/bin/env python3
"""Ordinary generated-world acceptance; no assigned habitats/organisms/events."""
from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent;out=Path(sys.argv[1])
subprocess.run([sys.executable,str(here/'egl-grazing-world-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text();s=s.replace('        var low_t:f32=10000;','        var update_total_ns:u64=0;var update_max_ns:u64=0;var update_count:u64=0;\n        var low_t:f32=10000;')
s=s.replace('            state.update(&game,1.0/60.0);','            var tick_timer=try std.time.Timer.start();\n            state.update(&game,1.0/60.0);\n            const tick_ns=tick_timer.read();update_total_ns+=tick_ns;update_max_ns=@max(update_max_ns,tick_ns);update_count+=1;')
marker='        try originSaveCheck(state,allocator);\n        return;'
extra='''        var seen=std.AutoHashMap(u64,usize).init(allocator);defer seen.deinit();
        var capable_movers:usize=0;var recorded_movers:usize=0;var resident_moves:u64=0;
        for(state.planet.microbeCells,0..)|cell,index|for(cell.cohorts)|co|{if(co.biomass>0){
            const entry=try seen.getOrPut(co.lineage);std.debug.assert(!entry.found_existing);entry.value_ptr.*=index;
            if(co.mobility>0)capable_movers+=1;
            if(co.relocations>0){recorded_movers+=1;resident_moves+=co.relocations;std.debug.assert(co.last_to==index and co.last_from!=co.last_to and co.last_move_time<=state.gameTime);}
        }};
        std.debug.assert(resident_moves<=state.planet.microbeStats.relocations);
        std.debug.print("MOTILITY_WORLD capable={d} resident_movers={d} total_moves={d} movement_respired_kgC={d} unique_lineages={d} mean_update_ms={d} max_update_ms={d}\\n",.{capable_movers,recorded_movers,state.planet.microbeStats.relocations,state.planet.microbeStats.movement_respired_carbon,seen.count(),@as(f64,@floatFromInt(update_total_ns))/@as(f64,@floatFromInt(update_count))/1e6,@as(f64,@floatFromInt(update_max_ns))/1e6});
'''
assert marker in s;s=s.replace(marker,extra+marker);p.write_text(s)
