#!/usr/bin/env python3
"""Day20 interventions forked from one actual serialized world, one day followup."""
from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent;out=Path(sys.argv[1])
subprocess.run([sys.executable,str(here/'egl-starter-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text();needle='            var tick_timer=try std.time.Timer.start();'
s=s.replace(needle,'''            if(i==1200){
                const Save=@import("save_game.zig");
                var arena=std.heap.ArenaAllocator.init(std.heap.page_allocator);defer arena.deinit();
                const captured=try Save.capture(arena.allocator(),state);
                const json=try std.json.stringifyAlloc(arena.allocator(),captured,.{});
                const parsed=try std.json.parseFromSlice(Save.schema.Save,arena.allocator(),json,.{});
                {var deep:usize=0;for(state.planet.waterMass,0..)|water,k|{if(water>state.planet.waterMass[deep])deep=k;}
                 state.selectedPoint=deep;const deep_receipt=state.applyGodAction(.wave,deep);std.debug.print("GOD_DEEP status={s} moved={d}\\n",.{@tagName(deep_receipt.failure),deep_receipt.moved_mass});}
                for(0..3)|branch|{
                    try Save.apply(state,parsed.value);state.selectedPoint=idx;state.pointerOnPlanet=false;
                    const before_mass=@import("simulation/microbes.zig").biomass(state.planet.microbeCells[idx]);
                    const before_temp=state.planet.temperature[idx];
                    if(branch>0){const receipt=state.applyGodAction(if(branch==1).wave else .lightning,idx);std.debug.assert(receipt.success());std.debug.print("GOD_BRANCH_EVENT branch={d} moved={d} heatJ={d} cells={d}\\n",.{branch,receipt.moved_mass,receipt.heat_joules,receipt.count});}
                    for(0..60)|_|state.update(&game,1.0/60.0);
                    std.debug.print("GOD_BRANCH_DAY21 branch={d} initial_biomass={d} biomass={d} initial_temp={d} temp={d} depth_m={d} births={d}\\n",.{branch,before_mass,@import("simulation/microbes.zig").biomass(state.planet.microbeCells[idx]),before_temp,state.planet.temperature[idx],state.planet.waterMass[idx]*state.planet.getKmPerWaterMass()*1000,state.planet.microbeStats.births});
                }
                try Save.apply(state,parsed.value);state.selectedPoint=idx;state.pointerOnPlanet=true;
            }
'''+needle,1);assert 'GOD_BRANCH_DAY21' in s;p.write_text(s)
