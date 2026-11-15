#!/usr/bin/env python3
from pathlib import Path
import shutil,sys,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve();src=r.parent/'site-tmp/vapor-cycle-engine/src';shutil.copytree(src,o,dirs_exist_ok=True)
p=o/'save_schema.zig';s=p.read_text().replace('VERSION: u32 = 10','VERSION: u32 = 11').replace('self.version<=9','self.version<=10');p.write_text(s)
p=o/'save_game.zig';s=p.read_text().replace('d.*=@as(f32,@floatCast(v));','d.*=if(saved.version==11)v else @as(f32,@floatCast(v));');p.write_text(s)
p=o/'simulation/vapor_bridge.zig';s=p.read_text();s+='\nfn up(x:f128)f128{return std.math.nextAfter(f128,x,std.math.inf(f128));}\nfn down(x:f128)f128{return std.math.nextAfter(f128,x,-std.math.inf(f128));}\n';needle=' const funded=@min(removed.paid,P.downRatio(P.downProduct(received,1e9),area));';assert s.count(needle)==1;s=s.replace(needle,''' const source_sum=@as(f128,sd.hi)+@as(f128,sd.lo);const receiver_sum=@as(f128,vd.hi)+@as(f128,vd.lo);
 const source_lo=down(down(source_sum)*@as(f128,area));const source_hi=up(up(source_sum)*@as(f128,area));
 const receiver_lo=down(down(receiver_sum)*1e9);const receiver_hi=up(up(receiver_sum)*1e9);
 const error_hi=@max(up(@abs(receiver_lo-source_hi)),up(@abs(receiver_hi-source_lo)));
 const vu=@max(std.math.nextAfter(f64,after,std.math.inf(f64))-after,after-std.math.nextAfter(f64,after,-std.math.inf(f64)));
 const su=@max(std.math.nextAfter(f64,soil,std.math.inf(f64))-soil,soil-std.math.nextAfter(f64,soil,-std.math.inf(f64)));
 const vapor_ulp=up(@as(f128,vu)*1e9);const soil_ulp=up(@as(f128,su)*@as(f128,area));
 const envelope=up(up(up(2*vapor_ulp)+up(2*soil_ulp))+up(16*std.math.floatEps(f64)*source_hi));
 if(!std.math.isFinite(envelope) or !std.math.isFinite(error_hi) or source_lo<=0 or error_hi>source_lo*0x1p-20 or error_hi>envelope)return keep;
'''+needle);p.write_text(s)
p=o/'main.zig';s=p.read_text();a=s.index('          @import("simulation/vapor_bridge.zig").strict_closure=');b=s.index('          std.process.exit(0);',a)+len('          std.process.exit(0);')
s=s[:a]+r'''
          const M=@import("simulation/microbes.zig");const bridge=@import("simulation/vapor_bridge.zig");bridge.dumps=false;bridge.strict_closure=false;
          state.paused=true;state.showEscapeMenu=false;
          std.debug.assert(!state.planet.rootConfig.enabled);for(state.planet.rootSoil)|water|std.debug.assert(water==0);for(state.planet.microbeCells)|cell|for(cell.cohorts)|co|std.debug.assert(co.root_fraction==0);
          const oldcapture=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const oldparsed=try std.json.parseFromSlice(saves.schema.Save,a,oldcapture,.{.allocate=.alloc_always});try saves.apply(state,oldparsed.value);std.debug.assert(std.mem.eql(u8,oldcapture,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          const from:usize=29440;const target:usize=29441;const slot:usize=0;
          std.debug.assert(state.planet.microbeCells[from].cohorts[slot].lineage==44 and state.planet.microbeCells[from].cohorts[slot].support_mass>0 and M.biomass(state.planet.microbeCells[target])==0 and state.planet.waterMass[target]==0 and state.planet.temperature[target]>273.15 and state.planet.temperature[target]<355);
          try state.planet.ensureRootSoil();state.planet.rootConfig=.{.enabled=true,.law=1,.conductance=10};
          state.selectedPoint=target;state.pointerOnPlanet=true;const water_before=state.planet.waterMass[target];const plus=stella_adjust_water(@intCast(target),1);std.debug.assert(plus>0);const water_added=@as(f64,state.planet.waterMass[target])-water_before;
          state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;
          const soil_before_drain=state.planet.rootSoil[target];const pre_drain=state.planet.waterMass[target];std.debug.assert(state.testAction(2));const water_removed=@as(f64,pre_drain)-state.planet.waterMass[target];std.debug.assert(state.planet.rootSoil[target]==soil_before_drain);
          state.selectedPoint=from;const prep=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_transport_prepare(PerformanceDetails.world_serial,@intCast(from),@intCast(slot),@intCast(target),"44")),.{.allocate=.alloc_always});
          std.debug.assert(prep.value.object.get("ok").?.bool);const token:u32=@intCast(prep.value.object.get("token").?.integer);const moved=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_transport_execute(token)),.{.allocate=.alloc_always});std.debug.assert(moved.value.object.get("ok").?.bool);
          std.debug.print("TERRESTRIAL_SETUP {s}\n",.{try std.json.stringifyAlloc(a,.{.source=from,.target=target,.id=@as(u64,44),.water_added_native=water_added,.water_removed_native=water_removed,.soil=soil_before_drain,.depth_m=state.planet.waterMass[target]*state.planet.getKmPerWaterMass()*1000,.cohort=state.planet.microbeCells[target].cohorts[0],.temperature=state.planet.temperature[target],.area=state.planet.getMeanPointArea()},.{})});
          const initial=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const frozen=try std.json.parseFromSlice(saves.schema.Save,a,initial,.{.allocate=.alloc_always});
          for(0..2)|arm|{
            try saves.apply(state,frozen.value);std.debug.assert(std.mem.eql(u8,initial,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));state.planet.microbeCells[target].cohorts[0].root_fraction=if(arm==0)0 else 0.25;
            for(0..2)|tick|{
              const before=state.planet.microbeCells[target].cohorts[0];std.debug.print("TERRESTRIAL_BEFORE {s}\n",.{try std.json.stringifyAlloc(a,.{.arm=arm,.tick=tick,.depth_m=state.planet.waterMass[target]*state.planet.getKmPerWaterMass()*1000,.height_m=M.producerHeightMeters(before),.soil=state.planet.rootSoil[target],.vapor=state.planet.waterVaporMass[target],.cohort=before},.{})});
              state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;
              std.debug.print("TERRESTRIAL_AFTER {s}\n",.{try std.json.stringifyAlloc(a,.{.arm=arm,.tick=tick,.soil=state.planet.rootSoil[target],.vapor=state.planet.waterVaporMass[target],.cohort=state.planet.microbeCells[target].cohorts[0],.depth_m=state.planet.waterMass[target]*state.planet.getKmPerWaterMass()*1000},.{})});
            }
            const ending=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const parsed=try std.json.parseFromSlice(saves.schema.Save,a,ending,.{.allocate=.alloc_always});try saves.apply(state,parsed.value);std.debug.assert(std.mem.eql(u8,ending,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
            std.debug.print("TERRESTRIAL_ARM_PASS arm={} experimental_f64_reload_exact=true\n",.{arm});
          }
          std.debug.print("TERRESTRIAL_GATE_COMPLETE no_long_run=true legacy_import_zero=true\n",.{});std.process.exit(0);
''' +s[b:];p.write_text(s)
(o.parent/'provenance.json').write_text(json.dumps({'source_tree':str(src),'input_sha256':hashlib.sha256((r.parent/'site-tmp/sunlit14/day-14.json').read_bytes()).hexdigest(),'files':{str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')}},indent=2)+'\n')
