#!/usr/bin/env python3
"""Inject fixed actual-world trials into an already prepared root-only QA copy."""
from pathlib import Path
import sys, hashlib, json
out=Path(sys.argv[1]).resolve(); p=out/'main.zig'; s=p.read_text()
needle='          std.debug.print("ROOT_ONLY_COPY_READY no_model_activation=true\\n",.{});'
assert s.count(needle)==1
block=r'''
          const micro=@import("simulation/microbes.zig");
          const audit=@import("simulation/root_scheduler_audit.zig");
          const label=try std.process.getEnvVarOwned(a,"QA_ROOT_LABEL");
          std.debug.assert(std.mem.eql(u8,label,"day30") or std.mem.eql(u8,label,"day60") or std.mem.eql(u8,label,"day90"));
          const frozen=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const baseline=try std.json.parseFromSlice(saves.schema.Save,a,frozen,.{.allocate=.alloc_always});
          const original_next=state.planet.microbeStats.next_lineage;
          const stage=try std.process.getEnvVarOwned(a,"QA_ROOT_STAGE");
          std.debug.assert(std.mem.eql(u8,stage,"off") or std.mem.eql(u8,stage,"enabled"));
          const arm_count:usize=if(std.mem.eql(u8,label,"day60"))4 else 2;
          for(0..arm_count)|arm|{
            if(std.mem.eql(u8,stage,"off") and arm!=0)continue;
            if(std.mem.eql(u8,stage,"enabled") and arm==0)continue;
            try saves.apply(state,baseline.value);
            std.debug.assert(!state.planet.rootConfig.enabled);
            if(arm>0){
              try state.planet.ensureRootSoil(); @memset(state.planet.rootSoil,0);
              state.planet.rootConfig=.{.enabled=true,.law=1,.conductance=if(arm==3)10 else 1};
            }
            if(arm>=2){
              var found:usize=0;
              for(state.planet.microbeCells)|*cell|for(&cell.cohorts)|*co|{
                if(co.biomass>0 and co.lineage==478){co.root_fraction=0.25;found+=1;}
              };
              std.debug.assert(found==1);
            }
            audit.current=.{};
            var family=std.AutoHashMap(u64,void).init(a);try family.put(478,{});
            const ticks:usize=if(arm==0)10 else 60;
            for(0..ticks+1)|tick|{
              if(tick>0){state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
              var added=true;while(added){added=false;for(state.planet.microbeCells)|cell|for(cell.cohorts)|co|{
                if(co.biomass>0 and co.lineage>=original_next and family.contains(co.parent) and !family.contains(co.lineage)){
                  std.debug.assert(co.root_fraction==(if(arm>=2)@as(f32,0.25)else 0));
                  try family.put(co.lineage,{});added=true;
                }
              };}
              var colonies:usize=0;var bio_mass:f64=0;var support_total:f64=0;var detritus:f64=0;var nutrient:f64=0;var liquid:f64=0;var vapor:f64=0;var soil:f64=0;var rooted:usize=0;var family_alive:usize=0;var family_mass:f64=0;
              for(state.planet.microbeCells,0..)|cell,i|{
                std.debug.assert(micro.validCell(cell,state.planet.microbeStats.next_lineage));
                nutrient+=cell.nutrient;detritus+=cell.detritus;liquid+=state.planet.waterMass[i];vapor+=state.planet.waterVaporMass[i];
                for(cell.cohorts)|co|if(co.biomass>0){colonies+=1;bio_mass+=co.biomass;support_total+=co.support_mass;if(co.root_fraction>0)rooted+=1;if(family.contains(co.lineage)){family_alive+=1;family_mass+=co.biomass;}};
              }
              for(state.planet.rootSoil)|w|{std.debug.assert(std.math.isFinite(w) and w>=0 and w<=1);soil+=w;}
              std.debug.assert(std.math.isFinite(liquid) and liquid>=0 and std.math.isFinite(vapor) and vapor>=0);
              std.debug.print("ROOT_WORLD {s}\n",.{try std.json.stringifyAlloc(a,.{.label=label,.arm=arm,.tick=tick,.game_time=state.gameTime,.config=state.planet.rootConfig,.colonies=colonies,.biomass_density_sum=bio_mass,.support_density_sum=support_total,.carbon_density_sum=bio_mass+detritus,.nitrogen_density_sum=nutrient+bio_mass*micro.nutrient_per_carbon,.liquid_native_sum=liquid,.vapor_native_sum=vapor,.soil_density_sum=soil,.water_native_sum=liquid+vapor+soil*state.planet.getMeanPointArea()/1e9,.mean_area=state.planet.getMeanPointArea(),.rooted_alive=rooted,.observed_family_alive=family_alive,.observed_family_mass=family_mass,.observed_family_ids=family.count(),.stats=state.planet.microbeStats,.audit=audit.current},.{})});
            }
            const endpoint=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
            const path=try std.fmt.allocPrint(a,"OUTPUT/{s}-arm-{d}.json",.{label,arm});
            try std.fs.cwd().writeFile(.{.sub_path=path,.data=endpoint});
            const decoded=try std.json.parseFromSlice(saves.schema.Save,a,endpoint,.{.allocate=.alloc_always});
            for(0..10)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
            const uninterrupted=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
            try std.fs.cwd().writeFile(.{.sub_path=try std.fmt.allocPrint(a,"{s}.uninterrupted.json",.{path}),.data=uninterrupted});
            try saves.apply(state,decoded.value);
            const recaptured=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
            const exact_roundtrip=std.mem.eql(u8,endpoint,recaptured);
            if(!exact_roundtrip)try std.fs.cwd().writeFile(.{.sub_path=try std.fmt.allocPrint(a,"{s}.recapture-failure.json",.{path}),.data=recaptured});
            std.debug.print("ROOT_ROUNDTRIP label={s} arm={d} exact={}\n",.{label,arm,exact_roundtrip});std.debug.assert(exact_roundtrip);
            for(0..10)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
            const restored=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
            try std.fs.cwd().writeFile(.{.sub_path=try std.fmt.allocPrint(a,"{s}.restored.json",.{path}),.data=restored});
            const exact_continuation=std.mem.eql(u8,uninterrupted,restored);
            std.debug.print("ROOT_CONTINUATION label={s} arm={d} exact={}\n",.{label,arm,exact_continuation});std.debug.assert(exact_continuation);
          }
          try saves.apply(state,baseline.value);
          std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
'''.replace('OUTPUT',str(out.parent))
s=s.replace(needle,block);p.write_text(s)
(out.parent/'world-qa-provenance.json').write_text(json.dumps({'main_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'fixed eight arms; no interventions; actual candidate save helpers'},indent=2)+'\n')
