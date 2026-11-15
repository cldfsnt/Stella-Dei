#!/usr/bin/env python3
"""Real nearshore basin actions, no imported organisms or persistent water fixing."""
from pathlib import Path
import subprocess,sys,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]);subprocess.run([sys.executable,str(r/'web/tests/egl-ecology-pulse-prepare.py'),str(o)],check=True)
p=o/'main.zig';s=p.read_text()
# Legacy nursery setup rewrites this export globally; restore exact production body.
production=(r/'src/main.zig').read_text();api='export fn stella_make_pond(';next_api='export fn stella_test_action('
s=s[:s.index(api)]+production[production.index(api):production.index(next_api)]+s[s.index(next_api):]
start=s.index('          var found=state.findRecordedFeeding(true);');end=s.index('\n        try originSaveCheck',start)
s=s[:start]+r'''
          _=pm;_=pw;const M=@import("simulation/microbes.zig");state.paused=true;state.showEscapeMenu=false;state.showPointDetails=false;state.showPlanetControl=false;
          const conv=state.planet.getKmPerWaterMass();const size=state.planet.microbeCells.len;
          // Exact production habitat predicate, read-only graph scan.
          const seen_h=try a.alloc(bool,size);@memset(seen_h,false);const queue=try a.alloc(usize,size);
          var habitable_total:usize=0;var components:usize=0;var occupied_components:usize=0;var reachable_empty:usize=0;var largest:usize=0;var top_sizes=[_]usize{0}**10;
          for(0..size)|i|{
            if(seen_h[i] or !M.habitable(state.planet.waterMass[i]*conv,state.planet.temperature[i]))continue;
            var head:usize=0;var count:usize=1;var occupied:usize=0;queue[0]=i;seen_h[i]=true;
            while(head<count):(head+=1){const current=queue[head];if(M.biomass(state.planet.microbeCells[current])>0)occupied+=1;
              for(state.planet.getNeighbours(current))|n|{if(!seen_h[n] and M.habitable(state.planet.waterMass[n]*conv,state.planet.temperature[n])){seen_h[n]=true;queue[count]=n;count+=1;}}
            }
            components+=1;habitable_total+=count;largest=@max(largest,count);if(occupied>0){occupied_components+=1;reachable_empty+=count-occupied;}
            top_sizes[0]=@max(top_sizes[0],count);std.mem.sort(usize,&top_sizes,{},std.sort.asc(usize));
          }
          std.debug.print("HABITAT_GRAPH {s}\n",.{try std.json.stringifyAlloc(a,.{.habitable=habitable_total,.components=components,.largest=largest,.top10=top_sizes,.occupied_components=occupied_components,.reachable_empty=reachable_empty,.point_area_m2=state.planet.getMeanPointArea(),.mean_width_km=@sqrt(state.planet.getMeanPointArea())/1000},.{})});
          var selected:?usize=null;var source:usize=0;
          for(0..size)|i|{const d=state.planet.waterMass[i]*conv;const t=state.planet.temperature[i];if(M.biomass(state.planet.microbeCells[i])>0 or d<0.0002 or d>0.02 or t<=273.15 or t>=320)continue;
            var best:?usize=null;for(state.planet.getNeighbours(i))|n|{const nd=state.planet.waterMass[n]*conv;const nt=state.planet.temperature[n];if(M.biomass(state.planet.microbeCells[n])>=0.03 and nd>=0.0002 and nd<=0.02 and nt>273.15 and nt<320 and @abs(state.planet.elevation[n]-state.planet.elevation[i])<=0.020){if(best==null or n<best.?)best=n;}}
            if(best)|n|{selected=i;source=n;break;}
          }
          if(selected==null){std.debug.print("HABITAT_UNAVAILABLE no_predeclared_empty_nearshore_neighbor=true\n",.{});return;}
          const target=selected.?;state.selectedPoint=target;
          var root_slot:usize=0;for(state.planet.microbeCells[source].cohorts,0..)|co,i|{if(co.biomass>state.planet.microbeCells[source].cohorts[root_slot].biomass)root_slot=i;}
          const root=state.planet.microbeCells[source].cohorts[root_slot];const first_id=state.planet.microbeStats.next_lineage;
          var ids:[19]usize=undefined;ids[0]=target;var footprint:usize=1;for(state.planet.getNeighbours(target))|n|{ids[footprint]=n;footprint+=1;}const floor_count=footprint;
          for(ids[0..floor_count])|inner|for(state.planet.getNeighbours(inner))|n|{var found=false;for(ids[0..footprint])|existing|{if(n==existing)found=true;}if(!found){std.debug.assert(footprint<19);ids[footprint]=n;footprint+=1;}};
          const frozen=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const baseline=try std.json.parseFromSlice(saves.schema.Save,a,frozen,.{.allocate=.alloc_always});
          std.debug.print("HABITAT_CHOSEN {s}\n",.{try std.json.stringifyAlloc(a,.{.target=target,.source=source,.root_slot=root_slot,.root=root,.target_depth_m=state.planet.waterMass[target]*conv*1000,.source_depth_m=state.planet.waterMass[source]*conv*1000,.footprint=ids[0..footprint],.floor_count=floor_count},.{})});
          for(0..3)|arm|{
            try saves.apply(state,baseline.value);state.selectedPoint=target;const initial_stats=state.planet.microbeStats;
            const changed=if(arm==1)stella_make_pond(@intCast(target)) else if(arm==2)stella_make_nursery(@intCast(target)) else 0;std.debug.assert(changed==if(arm>0)@as(i32,@intCast(footprint)) else 0);
            if(arm>0)std.debug.assert(@abs(state.planet.waterMass[target]*conv*1000-@as(f32,if(arm==1)15 else 5))<0.01);
            const post=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const oracle=try std.json.parseFromSlice(saves.schema.Save,a,post,.{.allocate=.alloc_always});
            var external_water:f64=0;var terrain_abs_m3:f64=0;
            for(ids[0..footprint],0..)|cell,j|{
              external_water+=@as(f64,state.planet.waterMass[cell])-baseline.value.water[cell];terrain_abs_m3+=@abs(@as(f64,state.planet.elevation[cell])-baseline.value.elevation[cell])*1000*state.planet.getMeanPointArea();
              std.debug.print("HABITAT_EDIT {s}\n",.{try std.json.stringifyAlloc(a,.{.arm=arm,.cell=cell,.floor=j<floor_count,.elevation_before_km=baseline.value.elevation[cell],.elevation_after_km=state.planet.elevation[cell],.depth_before_m=baseline.value.water[cell]*conv*1000,.depth_after_m=state.planet.waterMass[cell]*conv*1000,.initial_biomass=M.biomass(state.planet.microbeCells[cell])},.{})});
              @constCast(oracle.value.water)[cell]=baseline.value.water[cell];@constCast(oracle.value.elevation)[cell]=baseline.value.elevation[cell];
            }
            std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,oracle.value,.{})));
            const post_parsed=try std.json.parseFromSlice(saves.schema.Save,a,post,.{.allocate=.alloc_always});try saves.apply(state,post_parsed.value);state.selectedPoint=target;std.debug.assert(std.mem.eql(u8,post,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
            var family=std.AutoHashMap(u64,void).init(a);try family.put(root.lineage,{});var first_occupied:i32=-1;var occupied_ticks:usize=0;var current_streak:usize=0;var max_streak:usize=0;var target_habitable_ticks:usize=0;var min_depth:f32=std.math.inf(f32);var max_depth:f32=0;var initial_c:f64=0;var initial_n:f64=0;var initial_water:f64=0;
            for(0..841)|tick|{
              if(tick>0){state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
              for(state.planet.microbeCells)|pc|{std.debug.assert(M.validCell(pc,state.planet.microbeStats.next_lineage));for(pc.cohorts)|co|{if(co.biomass>0 and co.lineage>=first_id and family.contains(co.parent))try family.put(co.lineage,{});}}
              std.debug.assert(std.math.isFinite(state.planet.averageOxygenMass) and state.planet.averageOxygenMass>=0 and std.math.isFinite(state.planet.averageCarbonDioxideMass) and state.planet.averageCarbonDioxideMass>=0);
              const depth=state.planet.waterMass[target]*conv*1000;min_depth=@min(min_depth,depth);max_depth=@max(max_depth,depth);
              if(tick>0){if(M.biomass(state.planet.microbeCells[target])>0){occupied_ticks+=1;current_streak+=1;max_streak=@max(max_streak,current_streak);if(first_occupied<0)first_occupied=@intCast(tick);}else current_streak=0;if(M.habitable(depth/1000,state.planet.temperature[target]))target_habitable_ticks+=1;}
              if(tick!=0 and tick!=60 and tick!=180 and tick!=420 and tick!=840)continue;
              var colonies:usize=0;var patches:usize=0;var living:f64=0;var detritus:f64=0;var nutrient:f64=0;var water:f64=0;var family_alive:usize=0;var family_mass:f64=0;var root_mass:f32=0;var floor_alive:usize=0;var rim_alive:usize=0;
              for(state.planet.microbeCells,0..)|pc,i|{var local:usize=0;detritus+=pc.detritus;nutrient+=pc.nutrient;water+=@as(f64,state.planet.waterMass[i])+@as(f64,state.planet.waterVaporMass[i]);for(pc.cohorts)|co|{if(co.biomass>0){local+=1;colonies+=1;living+=co.biomass;if(co.lineage==root.lineage)root_mass=co.biomass;if(family.contains(co.lineage)){family_alive+=1;family_mass+=co.biomass;}}}if(local>0)patches+=1;}
              for(ids[0..footprint],0..)|cell,j|{if(M.biomass(state.planet.microbeCells[cell])>0){if(j<floor_count)floor_alive+=1 else rim_alive+=1;}}
              const area=state.planet.getMeanPointArea();const points:f64=@floatFromInt(size);const carbon=(living+detritus)*area+state.planet.averageCarbonDioxideMass*points*1e9*(12.0/44.0);const n=(nutrient+living*@as(f64,M.nutrient_per_carbon))*area;if(tick==0){initial_c=carbon;initial_n=n;initial_water=water;}
              const st=state.planet.microbeStats;
              std.debug.print("HABITAT_DAY {s}\n",.{try std.json.stringifyAlloc(a,.{.arm=arm,.day=tick/60,.target_depth_m=depth,.target_temperature_K=state.planet.temperature[target],.target=state.planet.microbeCells[target],.source_depth_m=state.planet.waterMass[source]*conv*1000,.target_min_depth_m=min_depth,.target_max_depth_m=max_depth,.habitable_postticks=target_habitable_ticks,.occupied_postticks=occupied_ticks,.first_occupied_tick=first_occupied,.longest_occupied_streak_ticks=max_streak,.floor_occupied=floor_alive,.rim_occupied=rim_alive,.root_mass=root_mass,.family_alive=family_alive,.family_mass=family_mass,.new_descendants_seen=family.count()-1,.colonies=colonies,.patches=patches,.living_sum=living,.detritus_sum=detritus,.free_nutrient_sum=nutrient,.births=st.births-initial_stats.births,.fixed_kgC=st.fixed_carbon-initial_stats.fixed_carbon,.recycled_kgC=st.recycled_carbon-initial_stats.recycled_carbon,.grazed_kgC=st.grazed_carbon-initial_stats.grazed_carbon,.external_water_1e9kg=external_water,.absolute_terrain_displacement_m3=terrain_abs_m3,.carbon_residual_kg=carbon-initial_c,.nutrient_residual_kg=n-initial_n,.water_residual_1e9kg=water-initial_water},.{})});
              if(tick==0 or tick==840){state.watchLife();state.targetCameraPos=state.planet.transformedPoints[target];_=state.fitLivingClusterResult(390,700);render(window);gl.finish();window.swapBuffers();const shot=try std.fmt.allocPrintZ(a,"/workspace/scratch/f67c3ac60ca3/site-tmp/habitat-engineering/arm-{d}-day-{d}.ppm",.{arm,tick/60});qa_capture(shot);}
            }
            const final=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const file=try std.fmt.allocPrint(a,"/workspace/scratch/f67c3ac60ca3/site-tmp/habitat-engineering/arm-{d}-day14.json",.{arm});try std.fs.cwd().writeFile(.{.sub_path=file,.data=final});
          }
          try saves.apply(state,baseline.value);std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));std.debug.print("HABITAT_PASS original_restored=true all_arms14days=true actual_exports=true immediate_biology_unchanged=true\n",.{});
        }
'''+s[end:];s=s.replace('if (!is_web or !web_initialized or !game.state_init) return null;','if (!game.state_init) return null; // QA native availability bridge, actual exports unchanged.');p.write_text(s)
files=['main.zig','simulation/planet.zig','simulation/microbes.zig','states/play.zig','pond_action.zig'];(o.parent/'provenance.json').write_text(json.dumps({'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip(),'production':{f:hashlib.sha256((r/'src'/f).read_bytes()).hexdigest() for f in files},'copied':{f:hashlib.sha256((o/f).read_bytes()).hexdigest() for f in files}},indent=2)+'\n')

# Boundary audit: only native world-availability is bridged; player actions are exact.
def function(text, marker):
 start=text.index(marker);return text[start:text.index('\n}',start)+2]
for name in ['stella_make_pond','stella_make_nursery']:
 assert function((r/'src/main.zig').read_text(),'export fn '+name+'(')==function((o/'main.zig').read_text(),'export fn '+name+'('),name
assert (r/'src/pond_action.zig').read_bytes()==(o/'pond_action.zig').read_bytes()
print('PUBLIC_ACTION_AUDIT exact_production_pond_export=true exact_production_nursery_export=true pond_action_module_exact=true')

for name in ['makeSelectedPond','makeSelectedNursery']:
 marker='    pub fn '+name+'('
 left=(r/'src/states/play.zig').read_text();right=(o/'states/play.zig').read_text()
 li=left.index(marker);ri=right.index(marker)
 assert left[li:left.index('\n    }',li)+6]==right[ri:right.index('\n    }',ri)+6],name
print('PLAYER_METHOD_AUDIT exact_pond_and_nursery_methods=true')
