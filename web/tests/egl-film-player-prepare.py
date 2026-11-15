from pathlib import Path
import subprocess,sys,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]);subprocess.run([sys.executable,str(r/'web/tests/egl-ecology-pulse-prepare.py'),str(o)],check=True)
p=o/'main.zig';s=p.read_text();start=s.index('          var found=state.findRecordedFeeding(true);');end=s.index('\n        try originSaveCheck',start)
s=s[:start]+r'''
          _=pm;_=pw;const M=@import("simulation/microbes.zig");const from:usize=12352;const slot:usize=1;
          state.paused=true;state.selectedPoint=from;state.showEscapeMenu=false;state.showPointDetails=false;state.showPlanetControl=false;
          const root_co=state.planet.microbeCells[from].cohorts[slot];std.debug.assert(root_co.lineage==478 and root_co.support_mass>0 and root_co.structure>0 and root_co.relocations==0);
          const frozen=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const baseline=try std.json.parseFromSlice(saves.schema.Save,a,frozen,.{.allocate=.alloc_always});
          var chosen:?usize=null;
          for(state.planet.getNeighbours(from))|n|{if(n==from or M.biomass(state.planet.microbeCells[n])>0)continue;const v=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_transport_prepare(PerformanceDetails.world_serial,@intCast(from),@intCast(slot),@intCast(n),"478")),.{});if(v.value.object.get("ok").?.bool){chosen=n;break;}}
          stella_transport_cancel();const target=chosen orelse return error.NoEligibleEmptyAdjacentPatch;
          std.debug.print("FILM_PREREG target={d} source={d} root={s} first_eligible_empty_actual_neighbor=true arms=5 days=7 no_refills=true\n",.{target,from,try std.json.stringifyAlloc(a,root_co,.{})});
          // Independent expected state changes exactly two cohort slots, only for action oracle.
          var destination_slot:usize=0;while(state.planet.microbeCells[target].cohorts[destination_slot].biomass>0)destination_slot+=1;
          state.planet.microbeCells[target].cohorts[destination_slot]=root_co;state.planet.microbeCells[from].cohorts[slot]=.{};
          const expected_move=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          for(0..5)|arm|{
            try saves.apply(state,baseline.value);state.selectedPoint=from;
            if(arm>=2){const v=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_transport_prepare(PerformanceDetails.world_serial,@intCast(from),@intCast(slot),@intCast(target),"478")),.{});std.debug.assert(v.value.object.get("ok").?.bool);const token:u32=@intCast(v.value.object.get("token").?.integer);const moved=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_transport_execute(token)),.{});std.debug.assert(moved.value.object.get("ok").?.bool);std.debug.assert(std.mem.eql(u8,expected_move,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));const inspect_receipt=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_transport_inspect(PerformanceDetails.world_serial,@intCast(target),"478")),.{});std.debug.assert(inspect_receipt.value.object.get("ok").?.bool);}
            const cell=state.selectedPoint;var supplied:f32=0;
            if(arm==1 or arm==3 or arm==4){const cells_before=try a.dupe(M.Cell,state.planet.microbeCells);supplied=stella_set_water_target(@intCast(cell),if(arm==3)1 else 0.08);std.debug.assert(std.math.isFinite(supplied));std.debug.assert(std.meta.eql(root_co,state.planet.microbeCells[cell].cohorts[if(arm>=2)destination_slot else slot]));std.debug.assert(std.mem.eql(u8,std.mem.sliceAsBytes(cells_before),std.mem.sliceAsBytes(state.planet.microbeCells)));}
            const action=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const action_saved=try std.json.parseFromSlice(saves.schema.Save,a,action,.{.allocate=.alloc_always});try saves.apply(state,action_saved.value);state.selectedPoint=cell;std.debug.assert(std.mem.eql(u8,action,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
            var family=std.AutoHashMap(u64,void).init(a);try family.put(478,{});const first_id=state.planet.microbeStats.next_lineage;const start_time=state.gameTime;var min_depth:f32=std.math.inf(f32);var max_depth:f32=0;var min_temp:f32=std.math.inf(f32);var max_temp:f32=0;var min_n:f32=std.math.inf(f32);var max_n:f32=0;var film_ticks:usize=0;var absent:f64=-1;
            for(0..421)|tick|{
              if(tick>0){state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
              const depth=state.planet.waterMass[cell]*state.planet.getKmPerWaterMass()*1000;const temp=state.planet.temperature[cell];const nutrient=state.planet.microbeCells[cell].nutrient;
              min_depth=@min(min_depth,depth);max_depth=@max(max_depth,depth);min_temp=@min(min_temp,temp);max_temp=@max(max_temp,temp);min_n=@min(min_n,nutrient);max_n=@max(max_n,nutrient);if(tick>0 and depth>0 and depth<0.2)film_ticks+=1;
              var root_alive=false;var root_mass:f32=0;var root_cell:usize=0;
              for(state.planet.microbeCells,0..)|pc,i|for(pc.cohorts)|co|{if(co.biomass>0){if(co.lineage==478){root_alive=true;root_mass=co.biomass;root_cell=i;}if(co.lineage>=first_id and family.contains(co.parent))try family.put(co.lineage,{});}};
              if(!root_alive and absent<0)absent=(state.gameTime-start_time)/86400;
              if(tick%60==0){var alive:usize=0;var mass:f64=0;for(state.planet.microbeCells)|pc|for(pc.cohorts)|co|{if(co.biomass>0 and family.contains(co.lineage)){alive+=1;mass+=co.biomass;}};
                std.debug.print("FILM_DAY {s}\n",.{try std.json.stringifyAlloc(a,.{.arm=arm,.day=tick/60,.selected=cell,.supplied_depth_m=supplied,.depth_m=depth,.min_depth=min_depth,.max_depth=max_depth,.film_observations=film_ticks,.min_temp=min_temp,.max_temp=max_temp,.min_n=min_n,.max_n=max_n,.root_alive=root_alive,.root_mass=root_mass,.root_cell=root_cell,.root_first_absent_day=absent,.family_alive=alive,.family_mass=mass,.new_descendants_seen=family.count()-1,.first_new_id=first_id},.{})});
                if(tick==0 or tick==420){state.watchLife();state.targetCameraPos=state.planet.transformedPoints[cell];_=state.fitLivingClusterResult(390,700);render(window);gl.finish();window.swapBuffers();const shot=try std.fmt.allocPrintZ(a,"/workspace/scratch/f67c3ac60ca3/site-tmp/film-player/arm-{d}-day-{d}.ppm",.{arm,tick/60});qa_capture(shot);}
              }
            }
          }
          try saves.apply(state,baseline.value);std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));std.debug.print("FILM_DONE all_arms_completed_original_restored=true\n",.{});
        }
'''+s[end:];s=s.replace('if (!is_web or !web_initialized or !game.state_init) return null;','if (!game.state_init) return null; // QA native access to actual exports.');p.write_text(s)
files=['src/simulation/microbes.zig','src/simulation/planet.zig','src/manual_transport.zig','src/main.zig','src/states/play.zig']
(o.parent/'source-provenance.json').write_text(json.dumps({f:hashlib.sha256((r/f).read_bytes()).hexdigest() for f in files},indent=2)+'\n')
