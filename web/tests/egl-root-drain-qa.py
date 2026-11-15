#!/usr/bin/env python3
"""Six fixed Water-minus/control trials; copy only, never execute during preparation."""
from pathlib import Path
import sys,shutil,subprocess,hashlib,json
r=Path(__file__).resolve().parents[2];source=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();assert source!=out
shutil.copytree(source,out,dirs_exist_ok=True)
subprocess.run([sys.executable,str(r/'web/tests/root-drain-trace-patch.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text();needle='          std.debug.print("ROOT_ONLY_COPY_READY no_model_activation=true\\n",.{});';assert s.count(needle)==1
block=r'''
          const micro=@import("simulation/microbes.zig");const audit=@import("simulation/root_scheduler_audit.zig");
          const label=try std.process.getEnvVarOwned(a,"QA_ROOT_DRAIN_LABEL");
          std.debug.assert(std.mem.eql(u8,label,"root0") or std.mem.eql(u8,label,"root25k1") or std.mem.eql(u8,label,"root25k10"));
          const frozen=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const baseline=try std.json.parseFromSlice(saves.schema.Save,a,frozen,.{.allocate=.alloc_always});
          std.debug.assert(state.planet.rootConfig.enabled and state.planet.rootConfig.law==1);
          const original_next=state.planet.microbeStats.next_lineage;
          for(0..2)|action|{
            try saves.apply(state,baseline.value);state.selectedPoint=12352;state.pointerOnPlanet=true;state.paused=true;
            var family=std.AutoHashMap(u64,void).init(a);try family.put(478,{});
            var found_initial=true;while(found_initial){found_initial=false;for(state.planet.microbeCells)|cell|for(cell.cohorts)|co|{
              if(co.biomass>0 and family.contains(co.parent) and !family.contains(co.lineage)){try family.put(co.lineage,{});found_initial=true;}
            };}
            const prior_known_family=family.count();
            var last_alive=std.AutoHashMap(u64,usize).init(a);
            const action_before=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
            const expected=try std.json.parseFromSlice(saves.schema.Save,a,action_before,.{.allocate=.alloc_always});
            const old_water=state.planet.waterMass[12352];const old_soil=state.planet.rootSoil[12352];
            if(action==1)std.debug.assert(state.testAction(2));
            const external_removed=@as(f64,old_water)-state.planet.waterMass[12352];
            if(action==1)std.debug.assert(external_removed>0 and state.planet.waterMass[12352]==0) else std.debug.assert(external_removed==0);
            @constCast(expected.value.water)[12352]=state.planet.waterMass[12352];
            std.debug.assert(state.planet.rootSoil[12352]==old_soil);
            const action_after=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
            std.debug.assert(std.mem.eql(u8,action_after,try std.json.stringifyAlloc(a,expected.value,.{})));
            std.debug.print("ROOT_DRAIN_ACTION {s}\n",.{try std.json.stringifyAlloc(a,.{.label=label,.action=action,.external_removed_native=external_removed,.soil_unchanged=old_soil,.exact_only_selected_water_changed=true,.prior_known_family=prior_known_family},.{})});
            audit.current=.{};audit.resetTarget();
            for(0..421)|tick|{
              if(tick>0){audit.resetTarget();state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
              var added=true;while(added){added=false;for(state.planet.microbeCells)|cell|for(cell.cohorts)|co|{
                if(co.biomass>0 and co.lineage>=original_next and family.contains(co.parent) and !family.contains(co.lineage)){try family.put(co.lineage,{});added=true;}
              };}
              var alive=std.AutoHashMap(u64,usize).init(a);var family_mass:f64=0;var living_total:usize=0;var carbon:f64=0;var nitrogen:f64=0;var liquid:f64=0;var vapor:f64=0;var soil:f64=0;
              for(state.planet.microbeCells,0..)|cell,i|{
                std.debug.assert(micro.validCell(cell,state.planet.microbeStats.next_lineage));carbon+=cell.detritus;nitrogen+=cell.nutrient;liquid+=state.planet.waterMass[i];vapor+=state.planet.waterVaporMass[i];soil+=state.planet.rootSoil[i];
                for(cell.cohorts)|co|if(co.biomass>0){living_total+=1;carbon+=co.biomass;nitrogen+=@as(f64,co.biomass)*micro.nutrient_per_carbon;if(family.contains(co.lineage)){
                  family_mass+=co.biomass;try alive.put(co.lineage,i);
                  if(!last_alive.contains(co.lineage))std.debug.print("ROOT_DRAIN_FATE {s}\n",.{try std.json.stringifyAlloc(a,.{.label=label,.action=action,.tick=tick,.event=if(tick==0)"present_at_start"else"first_observed_alive",.cell=i,.cohort=co},.{})});
                }};
              }
              var old_iter=last_alive.iterator();while(old_iter.next())|entry|if(!alive.contains(entry.key_ptr.*))std.debug.print("ROOT_DRAIN_FATE {s}\n",.{try std.json.stringifyAlloc(a,.{.label=label,.action=action,.tick=tick,.event="no_longer_observed_alive",.id=entry.key_ptr.*,.last_cell=entry.value_ptr.*},.{})});
              last_alive.deinit();last_alive=alive;
              const target=state.planet.microbeCells[12352];var heights:[4]f32=.{0,0,0,0};for(audit.target_root.cohorts,0..)|co,i|heights[i]=micro.producerHeightMeters(co);
              std.debug.print("ROOT_DRAIN_TICK {s}\n",.{try std.json.stringifyAlloc(a,.{.label=label,.action=action,.tick=tick,.time=state.gameTime,.config=state.planet.rootConfig,.external_removed_native=external_removed,.water_native=liquid+vapor+soil*state.planet.getMeanPointArea()/1e9,.water_plus_removed=liquid+vapor+soil*state.planet.getMeanPointArea()/1e9+external_removed,.soil_density_sum=soil,.carbon_density_sum=carbon,.nitrogen_density_sum=nitrogen,.living=living_total,.family_known=family.count(),.family_alive=alive.count(),.family_mass=family_mass,.target=target,.target_depth_m=state.planet.waterMass[12352]*state.planet.getKmPerWaterMass()*1000,.target_soil=state.planet.rootSoil[12352],.target_temperature=state.planet.temperature[12352],.target_vapor=state.planet.waterVaporMass[12352],.target_rain=state.planet.rainfall[12352],.precore_heights=heights,.column=audit.target_column,.root=audit.target_root,.audit=audit.current,.stats=state.planet.microbeStats},.{})});
            }
            const endpoint=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const path=try std.fmt.allocPrint(a,"OUTPUT/{s}-action-{d}.json",.{label,action});try std.fs.cwd().writeFile(.{.sub_path=path,.data=endpoint});
            const parsed=try std.json.parseFromSlice(saves.schema.Save,a,endpoint,.{.allocate=.alloc_always});
            for(0..10)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
            const uninterrupted=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});try std.fs.cwd().writeFile(.{.sub_path=try std.fmt.allocPrint(a,"{s}.uninterrupted.json",.{path}),.data=uninterrupted});
            try saves.apply(state,parsed.value);const again=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const exact_roundtrip=std.mem.eql(u8,endpoint,again);
            if(!exact_roundtrip)try std.fs.cwd().writeFile(.{.sub_path=try std.fmt.allocPrint(a,"{s}.recapture-failure.json",.{path}),.data=again});std.debug.assert(exact_roundtrip);
            for(0..10)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
            const restored=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});try std.fs.cwd().writeFile(.{.sub_path=try std.fmt.allocPrint(a,"{s}.restored.json",.{path}),.data=restored});const exact_continuation=std.mem.eql(u8,uninterrupted,restored);
            std.debug.print("ROOT_DRAIN_ENDPOINT label={s} action={d} exact_roundtrip={} exact_continuation={}\n",.{label,action,exact_roundtrip,exact_continuation});std.debug.assert(exact_continuation);
          }
          try saves.apply(state,baseline.value);std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
'''.replace('OUTPUT',str(out.parent))
s=s.replace(needle,block);p.write_text(s)
files=['main.zig','simulation/planet.zig','simulation/microbes.zig','simulation/root_throughflow.zig','simulation/root_scheduler_audit.zig','save_schema.zig','save_game.zig']
proof={'stage':'prepared only, not executed','source':str(source),'files':{f:hashlib.sha256((out/f).read_bytes()).hexdigest()for f in files},'inputs':{str(i):hashlib.sha256(i.read_bytes()).hexdigest()for i in [r.parent/f'site-tmp/root-world-qa/day60-arm-{a}.json' for a in [1,2,3]]}}
(out.parent/'drain-provenance.json').write_text(json.dumps(proof,indent=2)+'\n')
print(out)
