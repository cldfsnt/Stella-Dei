from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent;out=Path(sys.argv[1]);subprocess.run([sys.executable,str(here/'egl-nursery-prepare.py'),str(out)],check=True)
p=out/'states/play.zig';s=p.read_text().replace('initNewWorld(game, subdivisions, game.newWorldChoice.preset)','initNewWorld(game, subdivisions, .continents)');p.write_text(s)
p=out/'main.zig';s=p.read_text();s=s.replace('    std.debug.assert(state.planet.seedEligibility(state.selectedPoint)==.eligible);','    state.selectedPoint=30114;',1)
needle='    if (std.posix.getenv("STELLA_ORIGIN_COUPLED") != null) {'
s=s.replace(needle,'''    @import("simulation/microbes.zig").film_enabled=std.posix.getenv("QA_FILM_OFF")==null;
    {const Save=@import("save_game.zig");var arena=std.heap.ArenaAllocator.init(allocator);defer arena.deinit();
      const bytes=try std.json.stringifyAlloc(arena.allocator(),try Save.capture(arena.allocator(),state),.{});
      const path=std.posix.getenv("QA_INITIAL") orelse unreachable;
      if(std.posix.getenv("QA_FILM_OFF")==null){const f=try std.fs.createFileAbsolute(path,.{});defer f.close();try f.writeAll(bytes);}
      const f=try std.fs.openFileAbsolute(path,.{});defer f.close();const prior=try f.readToEndAlloc(arena.allocator(),64*1024*1024);
      std.debug.assert(std.mem.eql(u8,bytes,prior));std.debug.print("MATCHED_INITIAL schema6=true identical=true one_seed=true\\n",.{});
    }
'''+needle)
s=s.replace('            var tick_timer=try std.time.Timer.start();','''            if(i%240==239){
                const P=@import("simulation/planet.zig");var living:usize=0;var mass:f64=0;
                for(state.planet.microbeCells,0..)|cell,j|if(state.planet.waterMass[j]*state.planet.getKmPerWaterMass()<0.0002){for(cell.cohorts)|c|if(c.biomass>0){living+=1;mass+=c.biomass;};};
                std.debug.print("FILM_DAY day={d} living={d} biomass={d} fixed={d} dry_fixed={d} frozen_fixed={d}\\n",.{(i+1)/240,living,mass,P.qa_film_fixed,P.qa_dry_fixed,P.qa_frozen_fixed});
            }
            var tick_timer=try std.time.Timer.start();''')
p.write_text(s)
p=out/'simulation/microbes.zig';s=p.read_text();s=s.replace('const std =', 'pub var film_enabled:bool=true;\nconst std =',1);s=s.replace('    return filmProtection(c)*@sqrt','    if(!film_enabled)return 0;\n    return filmProtection(c)*@sqrt');s=s.replace('const film=env.depth_km>0','const film=film_enabled and env.depth_km>0');p.write_text(s)
p=out/'simulation/planet.zig';s=p.read_text();s='pub var qa_film_fixed:f64=0;pub var qa_dry_fixed:f64=0;pub var qa_frozen_fixed:f64=0;\n'+s
needle='            self.applyMicrobeFlux(flux);';assert needle in s
s=s.replace(needle,'''            const env=self.microbeEnvironment(i,light);
            if(env.depth_km<0.0002)qa_film_fixed+=flux.fixed;
            if(env.depth_km<=0)qa_dry_fixed+=flux.fixed;
            if(env.temperature<=273.15)qa_frozen_fixed+=flux.fixed;
'''+needle)
s=s.replace('self.propaguleArrivals+|=1;self.propaguleFeedback.arrived(i,n,lineage,options.gameTime);','''self.propaguleArrivals+|=1;self.propaguleFeedback.arrived(i,n,lineage,options.gameTime);
                            const source_depth=self.waterMass[i]*self.getKmPerWaterMass();
                            if(source_depth<0.0002)std.debug.print("FILM_PAID_BIRTH day={d} source={d} parent={d} child={d} depth_m={d}\\n",.{options.gameTime/86400,i,cell.cohorts[cohort].lineage,lineage,source_depth*1000});''')
p.write_text(s)
