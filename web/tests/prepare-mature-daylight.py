#!/usr/bin/env python3
"""Fixed first-positive-light intervention; archived experimental law, no tuning."""
from pathlib import Path
import shutil,hashlib,json
r=Path(__file__).resolve().parents[2]; src=r.parent/'site-tmp/mature-budget/src'; o=r.parent/'site-tmp/mature-daylight/src'
shutil.copytree(src,o,dirs_exist_ok=True)
p=o/'simulation/planet.zig';s=p.read_text();assert s.count('    fn microbeEnvironment(')==1;s=s.replace('    fn microbeEnvironment(','    pub fn microbeEnvironment(');p.write_text(s)
p=o/'main.zig';s=p.read_text();s=s.replace('for(0..4)|arm|{','for(0..2)|arm|{').replace('qa_budget_enabled=arm>=2','qa_budget_enabled=true')
needle='          std.debug.print("TERRESTRIAL_STAGE drain\\n",.{});';assert s.count(needle)==1
s=s.replace(needle,r'''          var waited:usize=0;
          while(true){
            const env=state.planet.microbeEnvironment(target,@max(0,state.planet.transformedPoints[target].norm().dot(state.simulationSolarVector()))*std.math.clamp(state.solarConstant/1361,0,2));
            const light=M.availableLight(env.light,env.depth_km);
            std.debug.print("DAYLIGHT_WAIT {s}\n",.{try std.json.stringifyAlloc(a,.{.waited=waited,.time=state.gameTime,.env=env,.biological_light=light,.soil=state.planet.rootSoil[target],.donor=state.planet.microbeCells[from].cohorts[slot]},.{})});
            if(light>0)break;
            if(waited==60){std.debug.print("DAYLIGHT_SETUP_FAILURE no_light\n",.{});std.process.exit(2);}
            state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;waited+=1;
          }
          if(state.planet.microbeCells[from].cohorts[slot].lineage!=931 or state.planet.microbeCells[from].cohorts[slot].biomass<=0 or M.biomass(state.planet.microbeCells[target])!=0){std.debug.print("DAYLIGHT_SETUP_FAILURE donor_or_target_changed\n",.{});std.process.exit(2);}
'''+needle)
needle='          const initial=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});';assert s.count(needle)==1
s=s.replace(needle,r'''          const setup_env=state.planet.microbeEnvironment(target,@max(0,state.planet.transformedPoints[target].norm().dot(state.simulationSolarVector()))*std.math.clamp(state.solarConstant/1361,0,2));
          std.debug.assert(M.availableLight(setup_env.light,setup_env.depth_km)>0);
          std.debug.print("DAYLIGHT_SETUP_ENV {s}\n",.{try std.json.stringifyAlloc(a,setup_env,.{})});
'''+needle)
needle='const frozen=try std.json.parseFromSlice(saves.schema.Save,a,initial,.{.allocate=.alloc_always});';assert s.count(needle)==1
s=s.replace(needle,needle+'try std.fs.cwd().writeFile(.{.sub_path="../site-tmp/mature-daylight/common-input.json",.data=initial});')
needle='const parsed=try std.json.parseFromSlice(saves.schema.Save,a,ending,';assert s.count(needle)==1
s=s.replace(needle,'try std.fs.cwd().writeFile(.{.sub_path=try std.fmt.allocPrint(a,"../site-tmp/mature-daylight/arm{d}.json",.{arm}),.data=ending});'+needle)
p.write_text(s)
(o.parent/'provenance.json').write_text(json.dumps({'reference':'mature-budget frozen trace source','files':{str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')}},indent=2)+'\n')
