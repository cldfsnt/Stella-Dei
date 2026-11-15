from pathlib import Path
import subprocess,sys,json,hashlib
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1]);candidate=len(sys.argv)>2 and sys.argv[2]=='candidate'
subprocess.run([sys.executable,str(root/'web/tests/egl-natural60-prepare.py'),str(out)],check=True)
# Restore production Planet before narrow integration, removing inherited QA counters.
p=out/'simulation/planet.zig';p.write_text((root/'src/simulation/planet.zig').read_text())
if candidate:
 (out/'simulation/microbes.zig').write_text((root/'src/experimental/hydration_continuous_core.zig').read_text())
 (out/'simulation/hydration_exchange.zig').write_text((root/'src/experimental/hydration_exchange.zig').read_text().replace('@import("hydration_continuous_core.zig")','@import("microbes.zig")'))
 hx=out/'simulation/hydration_exchange.zig';hs=hx.read_text();hs='pub var qa_max_residual:f64=0;pub var qa_sum_residual:f64=0;\n'+hs;hs=hs.replace(' const conv=1e9/area;', ' const qa_before=total(cell.*,liquid.*,vapor.*,area);\n const conv=1e9/area;',1);hs=hs.replace('deposit(vapor,&cell.vapor_return,conv);return flux;', 'deposit(vapor,&cell.vapor_return,conv);const residual=total(cell.*,liquid.*,vapor.*,area)-qa_before;qa_max_residual=@max(qa_max_residual,@abs(residual));qa_sum_residual+=residual;std.debug.assert(@abs(residual)<=@max(1e-9,64*std.math.floatEps(f64)*qa_before));return flux;');hx.write_text(hs.replace('//!','//'))
 schema=(root/'src/experimental/hydration_save_schema.zig').read_text().replace('@import("hydration_schema_types.zig")','@import("simulation/microbes.zig")').replace('@import("../simulation/ecology.zig")','@import("simulation/ecology.zig")');(out/'save_schema.zig').write_text(schema)
 s=p.read_text();needle='            if (Microbes.biomass(cell.*) <= 0 and cell.detritus <= 0) continue;';assert s.count(needle)==1
 s=s.replace(needle,'''            if (Microbes.biomass(cell.*) <= 0 and cell.detritus <= 0) {
                const HX=@import("hydration_exchange.zig");const conversion=1e9/@as(f64,self.getMeanPointArea());
                if(cell.liquid_return>0)HX.deposit(&self.waterMass[i],&cell.liquid_return,conversion);
                if(cell.vapor_return>0)HX.deposit(&self.waterVaporMass[i],&cell.vapor_return,conversion);
                continue;
            }''')
 needle='            const flux = Microbes.step(cell, self.microbeEnvironment(i, light), dt);';assert s.count(needle)==1
 s=s.replace(needle,'''            var water_owned=cell.liquid_return>0 or cell.vapor_return>0;
            for(cell.cohorts)|co|{if(co.retention_allocation>0 or co.stored_water>0){water_owned=true;break;}}
            const flux=if(water_owned) @import("hydration_exchange.zig").step(cell,&self.waterMass[i],&self.waterVaporMass[i],self.getMeanPointArea(),self.microbeEnvironment(i,light),dt) orelse unreachable else Microbes.step(cell,self.microbeEnvironment(i,light),dt);''')
 s='pub var qa_bio_max:f64=0;pub var qa_bio_sum:f64=0;\n'+s
 s=s.replace('        // Rebuild every tick;', '        var qa_water_before:f64=0;for(self.microbeCells,0..)|pc,ci|qa_water_before+=@import("hydration_exchange.zig").total(pc,self.waterMass[ci],self.waterVaporMass[ci],self.getMeanPointArea());\n        // Rebuild every tick;',1)
 s=s.replace('        if(observing)watch.finishPopulationTick', '        var qa_water_after:f64=0;for(self.microbeCells,0..)|pc,ci|qa_water_after+=@import("hydration_exchange.zig").total(pc,self.waterMass[ci],self.waterVaporMass[ci],self.getMeanPointArea());qa_bio_max=@max(qa_bio_max,@abs(qa_water_after-qa_water_before));qa_bio_sum+=qa_water_after-qa_water_before;\n        if(observing)watch.finishPopulationTick',1)
 p.write_text(s)
p=out/'main.zig';s=p.read_text();start=s.index('          const start_time=state.gameTime;');end=s.index('\n        try originSaveCheck',start)
block=r'''
          const frozen=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const baseline=try std.json.parseFromSlice(saves.schema.Save,a,frozen,.{.allocate=.alloc_always});
          const baseline_next=state.planet.microbeStats.next_lineage;
          for(0..ARMCOUNT)|arm|{
            if(arm>0 and std.posix.getenv("QA_HYDRATION_PARITY")!=null)break;
            try saves.apply(state,baseline.value);
            RESET
            ASSIGN
            var family=std.AutoHashMap(u64,void).init(a);try family.put(478,{});
            var external_water:f64=0;
            const ticks:usize=if(arm==0)10 else 420;
            for(0..ticks+1)|tick|{
              if(tick>0){state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
              if(arm>0 and arm<=2 and tick==60){state.selectedPoint=12352;state.pointerOnPlanet=true;const old=state.planet.waterMass[12352];const changed=state.testAction(2);external_water=@as(f64,old)-state.planet.waterMass[12352];std.debug.print("HYDRATION_WATER_ACTION arm={d} changed={} removed1e9kg={d}\n",.{arm,changed,external_water});}
              var changed_family=true;while(changed_family){changed_family=false;for(state.planet.microbeCells)|pc|for(pc.cohorts)|co|{if(co.biomass>0 and co.lineage>=baseline_next and family.contains(co.parent) and !family.contains(co.lineage)){INHERIT_CHECK try family.put(co.lineage,{});changed_family=true;}};}
              if(tick%60==0 or tick==ticks){
                var count:usize=0;var mass:f64=0;var water:f64=0;var family_count:usize=0;var family_mass:f64=0;var nutrient:f64=0;var detritus:f64=0;var root:micro.Cohort=.{};
                for(state.planet.microbeCells,0..)|cell,i|{std.debug.assert(micro.validCell(cell,state.planet.microbeStats.next_lineage));nutrient+=cell.nutrient;detritus+=cell.detritus;water+=@as(f64,state.planet.waterMass[i])+state.planet.waterVaporMass[i];WATERCOUNT
                for(cell.cohorts)|co|{if(co.biomass>0){count+=1;mass+=co.biomass;if(family.contains(co.lineage)){family_count+=1;family_mass+=co.biomass;}if(co.lineage==478)root=co;}}}
                std.debug.print("HYDRATION_COUPLED {s}\n",.{try std.json.stringifyAlloc(a,.{.arm=arm,.tick=tick,.count=count,.mass=mass,.root=root,.observed_family_mass=family_mass,.observed_family_count=family_count,.observed_family_ids=family.count(),.nutrient_sum=nutrient+mass*micro.nutrient_per_carbon,.carbon_sum=mass+detritus,.oxygen_mass=state.planet.averageOxygenMass,.co2_mass=state.planet.averageCarbonDioxideMass,.water1e9kg=water,.external_removed1e9kg=external_water,.depth_m=state.planet.waterMass[12352]*state.planet.getKmPerWaterMass()*1000,.temperature=state.planet.temperature[12352],.stats=state.planet.microbeStats},.{})});
              }
            }
            REPORT
            const path=try std.fmt.allocPrint(a,"OUTPUT/arm-{d}.json",.{arm});const endpoint=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});try std.fs.cwd().writeFile(.{.sub_path=path,.data=endpoint});const decoded=try std.json.parseFromSlice(saves.schema.Save,a,endpoint,.{.allocate=.alloc_always});for(0..10)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}const uninterrupted=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});try std.fs.cwd().writeFile(.{.sub_path=try std.fmt.allocPrint(a,"{s}.uninterrupted.json",.{path}),.data=uninterrupted});try saves.apply(state,decoded.value);std.debug.assert(std.mem.eql(u8,endpoint,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));std.debug.print("HYDRATION_ENDPOINT arm={d} exact_owned_save_roundtrip=true\n",.{arm});var continuation:?[]const u8=null;for(0..2)|repeat|{try saves.apply(state,decoded.value);for(0..10)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}const after=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});if(repeat==0){continuation=after;try std.fs.cwd().writeFile(.{.sub_path=try std.fmt.allocPrint(a,"{s}.restored.json",.{path}),.data=after});std.debug.print("HYDRATION_UNINTERRUPTED arm={d} exact={}\n",.{arm,std.mem.eql(u8,uninterrupted,after)});}else std.debug.assert(std.mem.eql(u8,continuation.?,after));}std.debug.print("HYDRATION_CONTINUATION arm={d} restored10tick_exact=true\n",.{arm});
          }
          try saves.apply(state,baseline.value);
        }
'''
block=block.replace('INHERIT_CHECK','std.debug.assert(co.retention_allocation==(if(arm>0 and arm%2==0) @as(f32,0.25) else 0));' if candidate else '').replace('RESET','@import("simulation/hydration_exchange.zig").qa_max_residual=0;@import("simulation/hydration_exchange.zig").qa_sum_residual=0;pm.qa_bio_max=0;pm.qa_bio_sum=0;' if candidate else '').replace('REPORT','std.debug.print("HYDRATION_LEDGER arm={d} local_max={d} local_sum={d} whole_bio_max={d} whole_bio_sum={d}\\n",.{arm,@import("simulation/hydration_exchange.zig").qa_max_residual,@import("simulation/hydration_exchange.zig").qa_sum_residual,pm.qa_bio_max,pm.qa_bio_sum});' if candidate else '').replace('ARMCOUNT','5' if candidate else '1').replace('ASSIGN','if(arm>0){var found=false;for(&state.planet.microbeCells[12352].cohorts)|*co|{if(co.lineage==478){co.retention_allocation=if(arm%2==0)0.25 else 0;found=true;}}std.debug.assert(found);}' if candidate else '').replace('WATERCOUNT','water+=micro.waterTotal(cell)*state.planet.getMeanPointArea()/1e9;' if candidate else '').replace('OUTPUT',str(out.parent))
s=s[:start]+block+s[end:]
# Remove known inherited, unused public Pond->Nursery QA substitution only.
s=s.replace('state.createNurseryAtSelection()', 'state.createNurseryAtSelection()')
# Exact production public Pond export body restored by balanced brace extraction.
def body(t,name):
 a=t.index('export fn '+name+'(');b=t.index('{',a);depth=1;i=b+1
 while depth:
  depth+=(t[i]=='{')-(t[i]=='}');i+=1
 return a,i,t[a:i]
original=(root/'src/main.zig').read_text();a,b,_=body(s,'stella_make_pond');s=s[:a]+body(original,'stella_make_pond')[2]+s[b:]
if candidate:s=s.replace('_=pw;_=pm;','_=pw;')
p.write_text(s)
(out.parent/'coupled-provenance.json').write_text(json.dumps({'candidate':candidate,'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'files':{str(p.relative_to(out)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [out/'simulation/microbes.zig',out/'simulation/planet.zig',out/'main.zig',out/'save_schema.zig']}},indent=2)+'\n')
