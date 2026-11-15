#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-ecology-pulse-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text();a=s.index('          var found=state.findRecordedFeeding(true);');b=s.index('\n        try originSaveCheck',a)
s=s[:a]+r'''
          _=pw;_=pm;const D=@import("experimental/manual_transplant.zig");const M=@import("simulation/microbes.zig");
          state.paused=true;const from:usize=12344;const slot:usize=3;const co=state.planet.microbeCells[from].cohorts[slot];std.debug.assert(co.lineage==120 and co.support_mass>0);
          var to:?usize=null;for(state.planet.getNeighbours(from))|n|{if(M.biomass(state.planet.microbeCells[n])==0){to=n;break;}}
          const dest=to orelse {std.debug.print("MANUAL no_empty_actual_neighbor\n",.{});return;};
          const frozen=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const parsed=try std.json.parseFromSlice(saves.schema.Save,a,frozen,.{.allocate=.alloc_always});
          var ticket=D.prepare(state,PerformanceDetails.world_serial,from,slot,dest).?;
          // Refuse each invalid ticket/state and freeze current state around the call.
          for(0..6)|case|{
            var wrong=ticket;
            switch(case){0=>wrong.serial+%=1,1=>wrong.time+=1,2=>wrong.id+=1,3=>wrong.owner+%=1,4=>wrong.target.nutrient+=0.01,else=>state.paused=false}
            const pre=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});std.debug.assert(!D.execute(state,PerformanceDetails.world_serial,wrong).ok);std.debug.assert(std.mem.eql(u8,pre,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));state.paused=true;
          }
          const receipt=D.execute(state,PerformanceDetails.world_serial,ticket);std.debug.assert(receipt.ok);
          // Expected state is a parsed independent deep snapshot; alter exactly two slots.
          var expected=try std.json.parseFromSlice(saves.schema.Save,a,frozen,.{.allocate=.alloc_always});
          // Reconstruct expectation through actual runtime copy, never borrowed before oracle.
          const moved=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          try saves.apply(state,expected.value);state.planet.microbeCells[from].cohorts[slot]=.{};state.planet.microbeCells[dest].cohorts[receipt.slot]=co;
          std.debug.assert(std.mem.eql(u8,moved,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          const moved_parsed=try std.json.parseFromSlice(saves.schema.Save,a,moved,.{.allocate=.alloc_always});try saves.apply(state,moved_parsed.value);std.debug.assert(std.mem.eql(u8,moved,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.print("MANUAL_APPLY id=120 from={d} to={d} mass={d} support={d} credit={d} exact_two_slots=true save_roundtrip=true stale_refusals=6\n",.{from,dest,co.biomass,co.support_mass,co.reproduction_credit});
          for(0..2)|arm|{
            try saves.apply(state,parsed.value);state.paused=true;
            if(arm==1){ticket=D.prepare(state,PerformanceDetails.world_serial,from,slot,dest).?;std.debug.assert(D.execute(state,PerformanceDetails.world_serial,ticket).ok);}
            state.paused=false;
            for(0..180)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
            var found:usize=0;for(state.planet.microbeCells,0..)|cell,i|for(cell.cohorts)|c|{if(c.biomass>0 and c.lineage==120){found+=1;std.debug.print("MANUAL_FATE arm={d} id=120 cell={d} biomass={d} support={d} credit={d} relocations={d}\n",.{arm,i,c.biomass,c.support_mass,c.reproduction_credit,c.relocations});}};
            std.debug.print("MANUAL_END arm={d} alive_count={d} from_biomass={d} to_biomass={d} births={d} sim_days=3\n",.{arm,found,M.biomass(state.planet.microbeCells[from]),M.biomass(state.planet.microbeCells[dest]),state.planet.microbeStats.births});
          }
        }
''' +s[b:];s=s.replace('var expected=try std.json.parseFromSlice','const expected=try std.json.parseFromSlice');p.write_text(s)
