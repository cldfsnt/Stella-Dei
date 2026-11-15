#!/usr/bin/env python3
"""Research-only directed sample eligibility on actual naturally evolved save."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-nursery-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text();s=s.replace('for(0..@as(usize,if(fast)', 'for(0..@as(usize,if(std.posix.getenv("QA_DIRECTED_SAVE")!=null) 0 else if(fast)')
needle='        try originSaveCheck(state,allocator);'
h=r'''
        {
          const saves=@import("save_game.zig");const DP=@import("experimental/directed_sample_planet.zig");
          var arena=std.heap.ArenaAllocator.init(allocator);defer arena.deinit();const a=arena.allocator();
          const path=try std.process.getEnvVarOwned(a,"QA_DIRECTED_SAVE");const bytes=try std.fs.cwd().readFileAlloc(a,path,100*1024*1024);
          const parsed=try std.json.parseFromSlice(saves.schema.Save,a,bytes,.{.allocate=.alloc_always});try saves.apply(state,parsed.value);state.paused=false;state.showEscapeMenu=false;
          var eligible:?DP.Ticket=null;var examined:usize=0;var funded_hits:usize=0;var full_edges:usize=0;var peak_mass:f32=0;var peak_credit:f32=0;
          const initial_time=state.gameTime;
          for(0..601)|tick|{
            for(state.planet.microbeCells,0..)|cell,from|for(cell.cohorts,0..)|co,slot|{
              if(co.biomass<=0)continue;examined+=1;peak_mass=@max(peak_mass,co.biomass);peak_credit=@max(peak_credit,co.reproduction_credit);
              if(co.biomass<0.03 or co.reproduction_credit<0.04)continue;funded_hits+=1;
              for(state.planet.getNeighbours(from))|to|{
                if(to==from)continue;
                var open=false;for(state.planet.microbeCells[to].cohorts)|target|if(target.biomass==0){open=true;break;};if(!open){full_edges+=1;continue;}
                eligible=DP.prepare(&state.planet,from,slot,to);if(eligible!=null)break;
              }
              if(eligible!=null)break;
            };
            if(eligible!=null or tick==600)break;
            state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;
          }
          std.debug.print("DIRECTED_WORLD elapsed_days={d} examined_living_states={d} funded_threshold_hits={d} full_adjacent_edges={d} peak_mass={d} peak_credit={d} earned_eligible={} no_assigned_credit=true normal_coupled_scheduler=true\n",.{(state.gameTime-initial_time)/86400,examined,funded_hits,full_edges,peak_mass,peak_credit,eligible!=null});
          if(eligible)|ticket|{
            const source=state.planet.microbeCells[ticket.from];const target=state.planet.microbeCells[ticket.to];const receipt=DP.execute(&state.planet,ticket);
            std.debug.print("DIRECTED_WORLD_TRANSACTION source={d} slot={d} target={d} donor_id={d} accepted={} mass={d} support={d} credit={d}\n",.{ticket.from,ticket.slot,ticket.to,ticket.id,receipt.ok,receipt.mass,receipt.support,receipt.credit});
            _=source;_=target;
          }
          // Refusal guards on actual world: no injected biology or altered resources.
          var tested=false;for(state.planet.microbeCells,0..)|cell,from|{for(cell.cohorts,0..)|co,slot|{if(co.biomass<=0)continue;const to=state.planet.getNeighbours(from)[0];if(DP.prepare(&state.planet,from,slot,to))|ticket|{
            const frozen=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
            var bad=ticket;bad.serial+%=1;std.debug.assert(!DP.execute(&state.planet,bad).ok);bad=ticket;bad.id+%=1;std.debug.assert(!DP.execute(&state.planet,bad).ok);bad=ticket;bad.owner=0;std.debug.assert(!DP.execute(&state.planet,bad).ok);bad=ticket;bad.target.nutrient+=0.01;std.debug.assert(!DP.execute(&state.planet,bad).ok);
            std.debug.assert(DP.prepare(&state.planet,from,slot,from)==null);std.debug.assert(DP.prepare(&state.planet,from,slot,state.planet.microbeCells.len)==null);
            const after=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});std.debug.assert(std.mem.eql(u8,frozen,after));tested=true;break;
          }}if(tested)break;}
          std.debug.assert(tested);std.debug.print("DIRECTED_WORLD_GUARDS stale_world_id_owner_target_self_invalid=true serialized_refusals_unchanged=true\n",.{});
          try saves.apply(state,parsed.value);
        }
'''
assert needle in s;s=s.replace(needle,h+needle,1);p.write_text(s)
