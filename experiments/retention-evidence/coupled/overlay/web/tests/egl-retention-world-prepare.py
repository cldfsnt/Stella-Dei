from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent;out=Path(sys.argv[1]);subprocess.run([sys.executable,str(here/'egl-nursery-prepare.py'),str(out)],check=True)
p=out/'states/play.zig';s=p.read_text().replace('seed, .{}) catch unreachable','seed, .{.water_preset=.continents}) catch unreachable');p.write_text(s)
p=out/'main.zig';s=p.read_text();needle='    std.debug.assert(state.planet.seedEligibility(state.selectedPoint)==.eligible);';assert needle in s
s=s.replace(needle,'''    const shore:usize=30111;
    const adjacent=state.planet.getNeighbours(shore);var chosen:?usize=null;
    outer:for(adjacent)|a|for(state.planet.getNeighbours(a))|b|{
        if(b==shore)continue;var near=false;for(adjacent)|c|{if(c==b)near=true;}
        if(!near){chosen=b;break :outer;}
    };
    state.selectedPoint=chosen orelse unreachable;
    std.debug.print("ACTUAL_NURSERY_RIM center={d} target={d} graph_distance=2 existing_player_tool=true\\n",.{state.selectedPoint,shore});''',1)
needle='    if (std.posix.getenv("STELLA_ORIGIN_COUPLED") != null) {'
s=s.replace(needle,r'''    {
        const saves=@import("save_game.zig");var arena=std.heap.ArenaAllocator.init(allocator);defer arena.deinit();const a=arena.allocator();
        loop.pump(1024);const bytes=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
        const path=std.posix.getenv("QA_MATCHED_INITIAL") orelse unreachable;
        if(std.posix.getenv("STELLA_DISABLE_RESERVE")==null){const file=try std.fs.createFileAbsolute(path,.{});defer file.close();try file.writeAll(bytes);}
        const file=try std.fs.openFileAbsolute(path,.{});defer file.close();const loaded=try file.readToEndAlloc(a,64*1024*1024);
        std.debug.assert(std.mem.eql(u8,bytes,loaded));var parsed=try saves.schema.parse(a,loaded);defer parsed.deinit();
        const selected=state.selectedPoint;try saves.replaceWorld(state,parsed.value);state.selectedPoint=selected;
        for(state.planet.microbeCells)|cell|std.debug.assert(@import("simulation/microbes.zig").storedWater(cell)==0);
        std.debug.print("MATCHED_INITIAL exact_serialized=true zero_reserves=true one_seed=true schema={d}\n",.{parsed.value.version});
    }
'''+needle,1)
needle='            var tick_timer=try std.time.Timer.start();'
s=s.replace(needle,r'''            if(i%240==239){
                const M=@import("simulation/microbes.zig");const c=state.planet.microbeCells[30111];
                std.debug.print("RIM_DAY day={d} depth_m={d} temperature={d} biomass={d} reserve={d} dry_fixed={d}\n",.{(i+1)/240,state.planet.waterMass[30111]*state.planet.getKmPerWaterMass()*1000,state.planet.temperature[30111],M.biomass(c),M.storedWater(c),@import("simulation/planet.zig").qa_dry_fixed});
                for(c.cohorts)|co|if(co.biomass>0){std.debug.print("RIM_LINEAGE day={d} id={d} parent={d} generation={d} biomass={d} structure={d} support={d} retention={d} optimum={d}\n",.{(i+1)/240,co.lineage,co.parent,co.generation,co.biomass,co.structure,co.support_mass,co.water_retention,co.optimum});};
                var total:f64=0;var tissue:f64=0;for(state.planet.waterMass,state.planet.waterVaporMass,state.planet.microbeCells)|w,v,cc|{total+=@as(f64,w)+v;tissue+=M.storedWater(cc)+cc.surface_water_carry+cc.vapor_water_carry;}
                total+=tissue*state.planet.getMeanPointArea()/1e9;
                std.debug.print("WATER_DAY day={d} total_engine_mass={d} tissue_and_carry_kg_m2_sum={d}\n",.{(i+1)/240,total,tissue});
            }
'''+needle,1);p.write_text(s)
p=out/'simulation/planet.zig';s=p.read_text().replace('            .liquid_available =','            .reserve_enabled=std.posix.getenv("STELLA_DISABLE_RESERVE")==null,\n            .liquid_available =');s='pub var qa_dry_fixed:f64=0;\n'+s
s=s.replace('            self.applyMicrobeWater(i,flux);','            if(i==30111 and self.waterMass[i]==0)qa_dry_fixed+=flux.fixed;\n            self.applyMicrobeWater(i,flux);')
s=s.replace('self.propaguleArrivals+|=1;self.propaguleFeedback.arrived(i,n,lineage,options.gameTime);','self.propaguleArrivals+|=1;self.propaguleFeedback.arrived(i,n,lineage,options.gameTime);if(n==30111)std.debug.print("RIM_ARRIVAL day={d} from={d} id={d} parent={d}\\n",.{options.gameTime/86400,i,lineage,cell.cohorts[cohort].lineage});')
p.write_text(s)
p=out/'simulation/planet.zig';s=p.read_text();s='pub var qa_shore_fixed:f64=0;pub var qa_all_dry_fixed:f64=0;\n'+s
s=s.replace('            self.applyMicrobeWater(i,flux);','            if(self.waterMass[i]*self.getKmPerWaterMass()<0.0002){qa_shore_fixed+=flux.fixed;if(self.waterMass[i]==0)qa_all_dry_fixed+=flux.fixed;}\n            self.applyMicrobeWater(i,flux);')
s=s.replace('self.propaguleArrivals+|=1;self.propaguleFeedback.arrived(i,n,lineage,options.gameTime);','''self.propaguleArrivals+|=1;self.propaguleFeedback.arrived(i,n,lineage,options.gameTime);
                            if(self.waterMass[n]*self.getKmPerWaterMass()<0.0002 or self.waterMass[i]*self.getKmPerWaterMass()<0.0002)std.debug.print("SHORE_PROPAGULE day={d} from={d} to={d} id={d} parent={d} source_depth_m={d} dest_depth_m={d}\\n",.{options.gameTime/86400,i,n,lineage,cell.cohorts[cohort].lineage,self.waterMass[i]*self.getKmPerWaterMass()*1000,self.waterMass[n]*self.getKmPerWaterMass()*1000});''')
s=s.replace('if (Microbes.reproduce(cell, cohort, cell, &self.microbeStats, true)) continue;','''if (Microbes.reproduce(cell, cohort, cell, &self.microbeStats, true)) {if(self.waterMass[i]*self.getKmPerWaterMass()<0.0002)std.debug.print("SHORE_LOCAL_BIRTH day={d} cell={d} depth_m={d}\\n",.{options.gameTime/86400,i,self.waterMass[i]*self.getKmPerWaterMass()*1000});continue;}''');p.write_text(s)
p=out/'main.zig';s=p.read_text().replace('                const M=@import("simulation/microbes.zig");const c=', '                std.debug.print("SHORE_FLUX day={d} fixed={d} dry_fixed={d}\\n",.{(i+1)/240,@import("simulation/planet.zig").qa_shore_fixed,@import("simulation/planet.zig").qa_all_dry_fixed});\n                const M=@import("simulation/microbes.zig");const c=');p.write_text(s)
