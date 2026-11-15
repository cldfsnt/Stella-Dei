#!/usr/bin/env python3
"""Actual all-point staging/cancel/commit equivalence and atomic stale guards."""
from pathlib import Path
import subprocess,sys,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve();subprocess.run([sys.executable,str(r/'web/tests/egl-arrival-toggle-prepare.py'),str(o)],check=True)
p=o/'main.zig';s=p.read_text();a=s.index('          _=pm;_=pw;');b=s.index('\n        std.debug.print("ARRIVAL_TOGGLE_COMPLETE',a)
s=s[:a]+r'''
          _=pm;_=pw;state.paused=true;state.showEscapeMenu=false;
          const AS=@import("auto_seed.zig");const world=@import("performance_details.zig").world_serial;
          const original=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const initial=try std.json.parseFromSlice(saves.schema.Save,a,original,.{.allocate=.alloc_always});
          try std.fs.cwd().writeFile(.{.sub_path="OUTPUT/before.json",.data=original});
          const ids=try a.alloc(bool,state.planet.microbeCells.len);var expected_eligible:usize=0;var partial:usize=0;
          for(ids,0..)|*yes,i|{yes.*=state.planet.seedEligibility(i)==.eligible;if(yes.*){expected_eligible+=1;if(@import("simulation/microbes.zig").biomass(state.planet.microbeCells[i])>0)partial+=1;}}
          var direct_planted:usize=0;for(ids,0..)|yes,i|{if(yes and state.planet.seedMicrobes(i))direct_planted+=1;}
          const expected=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});try std.fs.cwd().writeFile(.{.sub_path="OUTPUT/after.json",.data=expected});try saves.apply(state,initial.value);
          for(0..11)|which|{
            try saves.apply(state,initial.value);const begin_ns=std.time.nanoTimestamp();
            var response=try std.json.parseFromSlice(std.json.Value,a,AS.start(state,world,world),.{.allocate=.alloc_always});const prep_ns=std.time.nanoTimestamp()-begin_ns;
            std.debug.assert(response.value.object.get("ok").?.bool);const ticket:u32=@intCast(response.value.object.get("token").?.integer);
            var chunks:usize=0;var max_step_ns:i128=0;
            while(std.mem.eql(u8,response.value.object.get("phase").?.string,"planning")){
              const step_ns=std.time.nanoTimestamp();response=try std.json.parseFromSlice(std.json.Value,a,AS.step(state,world,ticket),.{.allocate=.alloc_always});max_step_ns=@max(max_step_ns,std.time.nanoTimestamp()-step_ns);chunks+=1;std.debug.assert(response.value.object.get("ok").?.bool);
            }
            std.debug.assert(std.mem.eql(u8,response.value.object.get("phase").?.string,"ready"));
            std.debug.assert(response.value.object.get("eligible").?.integer==expected_eligible and response.value.object.get("planted").?.integer==direct_planted);
            std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
            if(which==0){_=AS.cancel(ticket);std.debug.assert(std.mem.indexOf(u8,AS.apply(state,world,ticket),"\"ok\":false")!=null);}
            else if(which==1){const apply_ns=std.time.nanoTimestamp();const receipt=try a.dupe(u8,AS.apply(state,world,ticket));const elapsed=std.time.nanoTimestamp()-apply_ns;std.debug.assert(std.mem.indexOf(u8,receipt,"\"ok\":true")!=null);std.debug.assert(std.mem.eql(u8,expected,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));std.debug.assert(std.mem.indexOf(u8,AS.apply(state,world,ticket),"\"ok\":false")!=null);std.debug.assert(std.mem.eql(u8,expected,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
              const saved=try std.json.parseFromSlice(saves.schema.Save,a,expected,.{.allocate=.alloc_always});try saves.apply(state,saved.value);std.debug.assert(std.mem.eql(u8,expected,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));

              const before_births=state.planet.microbeStats.births;var live_before:usize=0;for(state.planet.microbeCells)|cell|for(cell.cohorts)|co|{if(co.biomass>0)live_before+=1;};
              for(0..10)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
              const future=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});var live_after:usize=0;for(state.planet.microbeCells)|cell|for(cell.cohorts)|co|{if(co.biomass>0)live_after+=1;};
              const recent=try std.json.parseFromSlice(std.json.Value,a,@import("world_ecology.zig").snapshot(&state.planet,world,state.gameTime,false),.{.allocate=.alloc_always});const rc=recent.value.object.get("recent").?.object.get("counts").?.object;
              std.debug.assert(rc.get("births").?.integer==state.planet.microbeStats.births-before_births);std.debug.assert(rc.get("deaths").?.integer==live_before+state.planet.microbeStats.births-before_births-live_after);
              std.debug.print("AUTO_SEED_EVOLUTION births={} physiology_deaths={} living_before={} living_after={} exact_global_balance=true\n",.{rc.get("births").?.integer,rc.get("deaths").?.integer,live_before,live_after});
              try saves.apply(state,saved.value);for(0..10)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}std.debug.assert(std.mem.eql(u8,future,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));render(window);gl.finish();window.swapBuffers();qa_capture("OUTPUT/recent-footer.ppm");
              std.debug.print("AUTO_SEED_APPLY_PASS eligible={} planted={} partial_occupied_eligible={} chunks={} snapshot_ms={d} max_step_ms={d} apply_ms={d} snapshot_bytes={} actual_direct_seed_fullsave_exact=true duplicate_inert=true saved_reload_exact=true receipt={s}\n",.{expected_eligible,direct_planted,partial,chunks,@as(f64,@floatFromInt(prep_ns))/1e6,@as(f64,@floatFromInt(max_step_ns))/1e6,@as(f64,@floatFromInt(elapsed))/1e6,state.planet.microbeCells.len*(2*@sizeOf(@import("simulation/microbes.zig").Cell)+3*@sizeOf(f32)),receipt});
            }else{
              switch(which){2=>state.planet.waterMass[0]+=1,3=>state.planet.averageCarbonDioxideMass+=1,4=>{state.paused=false;AS.guard(state,world);state.paused=true;},5=>state.gameTime+=1,6=>{try saves.apply(state,initial.value);},7=>{},8=>state.planet.microbeStats.next_lineage+=1,9=>state.planet.elevation[0]+=1,10=>{},else=>unreachable}
              const stale=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const reply=AS.apply(state,if(which==10) world+1 else world,if(which==7)ticket+1 else ticket);std.debug.assert(std.mem.indexOf(u8,reply,"\"ok\":false")!=null);std.debug.assert(std.mem.eql(u8,stale,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
            }
          }
          try saves.apply(state,initial.value);std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));

          var tiny_buffer:[1]u8=undefined;var tiny=std.heap.FixedBufferAllocator.init(&tiny_buffer);
          std.debug.assert(std.mem.indexOf(u8,AS.startWithAllocator(state,world,world,tiny.allocator()),"Not enough memory")!=null);
          std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          var bad:usize=0;for(ids,0..)|yes,i|{if(yes and i%512<511 and i+1<ids.len){bad=i+1;break;}}std.debug.assert(bad>0);
          state.planet.microbeCells[bad].cohorts[0].biomass = -1;
          const invalid_before=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          var invalid_reply=try std.json.parseFromSlice(std.json.Value,a,AS.start(state,world,world),.{.allocate=.alloc_always});const bad_ticket:u32=@intCast(invalid_reply.value.object.get("token").?.integer);
          while(std.mem.eql(u8,invalid_reply.value.object.get("phase").?.string,"planning")){invalid_reply=try std.json.parseFromSlice(std.json.Value,a,AS.step(state,world,bad_ticket),.{.allocate=.alloc_always});}
          std.debug.assert(!invalid_reply.value.object.get("ok").?.bool);std.debug.assert(invalid_reply.value.object.get("scanned").?.integer>=invalid_reply.value.object.get("eligible").?.integer);
          std.debug.assert(std.mem.eql(u8,invalid_before,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          try saves.apply(state,initial.value);std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.print("AUTO_SEED_FAILURE_PASS oom_atomic=true invalid_after_eligible_atomic=true bad_cell={}\n",.{bad});
          std.debug.print("AUTO_SEED_COMPLETE cancel_stale_water_gas_unpause_time_load_atomic=true original_restored=true\n",.{});
        }
'''.replace('OUTPUT',str(o.parent))+s[b:];p.write_text(s.replace('ARRIVAL_TOGGLE_COMPLETE','AUTO_SEED_GATE'))
subprocess.run([sys.executable,str(r/'web/tests/audit-zig-exports.py'),str(r/'src/main.zig'),str(p)],check=True,stdout=(o.parent/'export-audit.json').open('w'))
(o.parent/'source-hashes.json').write_text(json.dumps({f:hashlib.sha256((o/f).read_bytes()).hexdigest()for f in ['main.zig','auto_seed.zig','states/play.zig','simulation/planet.zig','simulation/microbes.zig']},indent=2)+'\n')
