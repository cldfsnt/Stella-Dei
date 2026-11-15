#!/usr/bin/env python3
"""QA-only full coupled grazing ablation; production coefficients/traits unchanged."""
from pathlib import Path
import subprocess,sys,hashlib,json
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-natural60-prepare.py'),str(out)],check=True)
p=out/'simulation/microbes.zig';s=p.read_text();needle='const grazing=graze(cell,days,@max(0,env.oxygen_carbon_capacity-support_respired));'
assert s.count(needle)==1
s=s.replace('const std = @import("std");','const std = @import("std");\npub var qa_disable_grazing:bool=false;').replace(needle,'const grazing=if(qa_disable_grazing) GrazingFlux{} else graze(cell,days,@max(0,env.oxygen_carbon_capacity-support_respired));')
p.write_text(s)
p=out/'main.zig';s=p.read_text();start=s.index('          const start_time=state.gameTime;');end=s.index('\n        try originSaveCheck',start)
s=s[:start]+r'''
          const frozen=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const baseline=try std.json.parseFromSlice(saves.schema.Save,a,frozen,.{.allocate=.alloc_always});
          var baseline_ids=std.AutoHashMap(u64,void).init(a);
          for(state.planet.microbeCells)|pc|for(pc.cohorts)|co|{if(co.biomass>0)try baseline_ids.put(co.lineage,{});};
          const next_baseline=state.planet.microbeStats.next_lineage;
          for(0..2)|arm|{
            try saves.apply(state,baseline.value);micro.qa_disable_grazing=arm==1;
            std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
            const initial_stats=state.planet.microbeStats;
            var initial_c:f64=0;var initial_n:f64=0;var initial_water:f64=0;
            for(0..1801)|tick|{
              if(tick>0){state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
              // Every tick: actual cell and atmospheric validity, not a conservation assertion.
              for(state.planet.microbeCells)|pc|std.debug.assert(micro.validCell(pc,state.planet.microbeStats.next_lineage));
              std.debug.assert(std.math.isFinite(state.planet.averageOxygenMass) and state.planet.averageOxygenMass>=0);
              std.debug.assert(std.math.isFinite(state.planet.averageCarbonDioxideMass) and state.planet.averageCarbonDioxideMass>=0);
              if(arm==1){std.debug.assert(state.planet.microbeStats.grazed_carbon==initial_stats.grazed_carbon);std.debug.assert(state.planet.microbeStats.grazing_respired_carbon==initial_stats.grazing_respired_carbon);}
              if(tick!=0 and tick!=180 and tick!=600 and tick!=1200 and tick!=1800)continue;
              var count:usize=0;var occupied:usize=0;var mass:f64=0;var support_sum:f64=0;var detritus:f64=0;var nutrient:f64=0;var water:f64=0;var baseline_alive:usize=0;var new_alive:usize=0;var generation:u32=0;var forms=[_]usize{0}**6;var feeding_mass:f64=0;
              var ids=std.AutoHashMap(u64,void).init(allocator);defer ids.deinit();
              for(state.planet.microbeCells,0..)|pc,ci|{
                var local:usize=0;detritus+=pc.detritus;nutrient+=pc.nutrient;
                const wm=state.planet.waterMass[ci];const vapor=state.planet.waterVaporMass[ci];std.debug.assert(std.math.isFinite(wm) and wm>=0 and std.math.isFinite(vapor) and vapor>=0);water+=@as(f64,wm)+@as(f64,vapor);
                for(pc.cohorts)|co|if(co.biomass>0){local+=1;count+=1;mass+=co.biomass;support_sum+=co.support_mass;feeding_mass+=co.biomass*co.feeding;generation=@max(generation,co.generation);forms[@intFromEnum(micro.producerForm(co))]+=1;
                  std.debug.assert(co.parent<co.lineage);const entry=try ids.getOrPut(co.lineage);std.debug.assert(!entry.found_existing);
                  if(baseline_ids.contains(co.lineage))baseline_alive+=1;
                  if(co.lineage>=next_baseline)new_alive+=1;
                };if(local>0)occupied+=1;
              }
              const area=state.planet.getMeanPointArea();const points:@TypeOf(area)=@floatFromInt(state.planet.vertices.len);
              const carbon=(mass+detritus)*area+state.planet.averageCarbonDioxideMass*points*1e9*(12.0/44.0);
              // Nutrient already released when tissue dies; detritus has no second bound-N pool.
              const n=(nutrient+mass*@as(f64,micro.nutrient_per_carbon))*area;
              if(tick==0){initial_c=carbon;initial_n=n;initial_water=water;}
              const st=state.planet.microbeStats;
              std.debug.print("GRAZING_COUPLED {s}\n",.{try std.json.stringifyAlloc(a,.{
                .arm=arm,.day=60+tick/60,.tick=tick,.colonies=count,.patches=occupied,.biomass_sum=mass,.support_sum=support_sum,.detritus_sum=detritus,.free_nutrient_sum=nutrient,.baseline_alive=baseline_alive,.new_alive=new_alive,.births=st.births-initial_stats.births,.max_generation=generation,.forms=forms,.biomass_weighted_feeding=if(mass>0)feeding_mass/mass else 0,
                .fixed_kgC=st.fixed_carbon-initial_stats.fixed_carbon,.recycled_kgC=st.recycled_carbon-initial_stats.recycled_carbon,.grazed_kgC=st.grazed_carbon-initial_stats.grazed_carbon,.grazing_respired_kgC=st.grazing_respired_carbon-initial_stats.grazing_respired_carbon,.movement_respired_kgC=st.movement_respired_carbon-initial_stats.movement_respired_carbon,.relocations=st.relocations-initial_stats.relocations,
                .o2_kg=state.planet.averageOxygenMass*points*1e9,.co2_kg=state.planet.averageCarbonDioxideMass*points*1e9,.total_carbon_kg=carbon,.carbon_residual_kg=carbon-initial_c,.total_nutrient_kg=n,.nutrient_residual_kg=n-initial_n,.water_1e9kg=water,.water_residual_1e9kg=water-initial_water,.area_m2=area,
              },.{})});
              if(tick==1800){const snapshot=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const path=try std.fmt.allocPrint(a,"/workspace/scratch/f67c3ac60ca3/site-tmp/grazing-coupled/arm-{d}-day90.json",.{arm});try std.fs.cwd().writeFile(.{.sub_path=path,.data=snapshot});}
            }
          }
          micro.qa_disable_grazing=false;try saves.apply(state,baseline.value);
          std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.print("GRAZING_COUPLED_PASS identical_starts=true finite_cells_every_tick=true unique_living_ids=true ablation_zero_flux=true original_world_restored=true\n",.{});
        }
'''+s[end:];p.write_text(s)
files=['simulation/microbes.zig','simulation/planet.zig','main.zig','states/play.zig']
prov={'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'production':{},'copied':{}}
for f in files:
 prov['production'][f]=hashlib.sha256((root/'src'/f).read_bytes()).hexdigest();prov['copied'][f]=hashlib.sha256((out/f).read_bytes()).hexdigest()
(out.parent/'provenance.json').write_text(json.dumps(prov,indent=2)+'\n')
