#!/usr/bin/env python3
"""Experimental real-world fire assay; never injects fuel or modifies player saves."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-nursery-watch-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text();needle='        try originSaveCheck(state,allocator);';assert needle in s
hook=r'''        {
            const Save=@import("save_game.zig");const M=@import("simulation/microbes.zig");const Fire=@import("experimental/planet_ignition.zig");
            var fire_arena=std.heap.ArenaAllocator.init(allocator);defer fire_arena.deinit();const fa=fire_arena.allocator();
            const original=try std.json.stringifyAlloc(fa,try Save.capture(fa,state),.{});
            const parsed=try std.json.parseFromSlice(Save.schema.Save,fa,original,.{});
            var patch:usize=0;var dry_fuel:usize=0;
            for(state.planet.microbeCells,0..)|cell,k|{if(cell.detritus>state.planet.microbeCells[patch].detritus)patch=k;if(cell.detritus>0 and state.planet.waterMass[k]==0)dry_fuel+=1;}
            std.debug.assert(state.planet.microbeCells[patch].detritus>0);
            std.debug.print("FIRE_START patch={d} naturally_dry_fuel_patches={d} earned_detritus={d} depth_m={d}\n",.{patch,dry_fuel,state.planet.microbeCells[patch].detritus,state.planet.waterMass[patch]*state.planet.getKmPerWaterMass()*1000});
            for(0..3)|branch|{
                try Save.apply(state,parsed.value);state.selectedPoint=patch;state.pointerOnPlanet=false;
                var taps:usize=0;
                if(branch>0){state.pointerOnPlanet=true;while(state.planet.waterMass[patch]>0 and taps<128):(taps+=1){std.debug.assert(state.testAction(2));}std.debug.assert(state.planet.waterMass[patch]==0);state.pointerOnPlanet=false;}
                const before=try std.json.stringifyAlloc(fa,try Save.capture(fa,state),.{});
                const predicted=Fire.preview(&state.planet,patch,patch);
                std.debug.assert(std.mem.eql(u8,before,try std.json.stringifyAlloc(fa,try Save.capture(fa,state),.{})));
                std.debug.print("FIRE_PREVIEW branch={d} drain_taps={d} receipt={s}\n",.{branch,taps,try std.json.stringifyAlloc(fa,predicted,.{})});
                if(branch==0)std.debug.assert(!predicted.success());
                if(branch==2){const applied=Fire.ignite(&state.planet,patch,patch);std.debug.assert(applied.success());std.debug.print("FIRE_APPLIED receipt={s}\n",.{try std.json.stringifyAlloc(fa,applied,.{})});
                    const frozen=try std.json.stringifyAlloc(fa,try Save.capture(fa,state),.{});const burned_save=try std.json.parseFromSlice(Save.schema.Save,fa,frozen,.{});try Save.apply(state,burned_save.value);std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(fa,try Save.capture(fa,state),.{})));
                }
                state.paused=false;state.timeScale=86400;state.simulationClock.reset();const start=state.gameTime;
                for(0..600)|tick|{state.update(&game,1.0/60.0);if(tick+1==60 or tick+1==600){
                    const cell=state.planet.microbeCells[patch];std.debug.assert(M.validCell(cell,state.planet.microbeStats.next_lineage));
                    std.debug.print("FIRE_FOLLOWUP branch={d} elapsed_days={d} biomass={d} detritus={d} temperature={d} depth_m={d} nutrient={d} CO2={d} O2={d}\n",.{branch,(state.gameTime-start)/86400,M.biomass(cell),cell.detritus,state.planet.temperature[patch],state.planet.waterMass[patch]*state.planet.getKmPerWaterMass()*1000,cell.nutrient,state.planet.averageCarbonDioxideMass,state.planet.averageOxygenMass});
                }}
            }
            try Save.apply(state,parsed.value);std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(fa,try Save.capture(fa,state),.{})));
            std.debug.print("FIRE_RESTORE exact_original=true user_save_used=false fuel_injected=false\n",.{});
        }
'''
p.write_text(s.replace(needle,hook+needle,1))
