from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];base=r.parent/'site-tmp/origin-root-drain';src=r.parent/'site-tmp/origin-land-day30/src';o=base/'src';assert not o.exists();shutil.copytree(src,o)
p=o/'main.zig';s=p.read_text();a=s.index('    const resumed=');b=s.index('\n}\n\nconst expect',a)
code=r'''    const ablated=std.mem.eql(u8,std.posix.getenv("QA_ARM") orelse "0","1");const resumed=std.mem.eql(u8,mode,"resume");
    const input=if(resumed)try std.fmt.allocPrint(a,"BASE/arm-{}-30.json",.{@intFromBool(ablated)})else "INPUT";
    const bytes=try std.fs.cwd().readFileAlloc(a,input,128*1024*1024);const parsed=try std.json.parseFromSlice(saves.schema.Save,a,bytes,.{.allocate=.alloc_always});try saves.apply(state,parsed.value);std.debug.assert(std.mem.eql(u8,bytes,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
    if(!resumed){
      var wait:usize=0;
      while(true){
        const co=state.planet.microbeCells[18327].cohorts[2];if(co.lineage!=524 or co.biomass<=0 or co.support_mass<=0 or co.root_fraction<=0)return error.SubjectLost;
        const soil=state.planet.landSoil[18327];if(!std.math.isFinite(soil) or soil<=0 or soil>1)return error.InvalidSoil;
        const light=@max(0,state.planet.transformedPoints[18327].norm().dot(state.simulationSolarVector()))*std.math.clamp(state.solarConstant/1361,0,2);
        if(light>0){Audit.emit("SETUP",.{.wait=wait,.light=light,.cohort=co,.soil=soil,.temperature=state.planet.temperature[18327],.depth_m=state.planet.waterMass[18327]*state.planet.getKmPerWaterMass()*1000});break;}
        if(wait==60)return error.NoDaylight;
        state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;wait+=1;
      }
      state.paused=true;state.selectedPoint=18327;const before=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const old=state.planet.waterMass[18327];const soil=state.planet.landSoil[18327];const changed=state.setSelectedWaterTarget(18327,0);std.debug.assert(std.math.isFinite(changed) and state.planet.waterMass[18327]==0 and state.planet.landSoil[18327]==soil);
      state.planet.waterMass[18327]=old;std.debug.assert(std.mem.eql(u8,before,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));state.planet.waterMass[18327]=0;
      Audit.emit("DRAIN",.{.water_before=old,.water_after=state.planet.waterMass[18327],.removed_kg=@as(f64,old)*1e9,.returned_depth=changed,.soil=soil,.area=state.planet.getMeanPointArea()});
      if(ablated)state.planet.microbeCells[18327].cohorts[2].root_fraction=0;
      const initial=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});try std.fs.cwd().writeFile(.{.sub_path=try std.fmt.allocPrint(a,"BASE/arm-{}-0.json",.{@intFromBool(ablated)}),.data=initial});
    }
    Audit.enabled=true;const start:usize=if(resumed)30 else 0;
    for(start..60)|tick|{
      Audit.tick=tick+1;state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;
      for(state.planet.microbeCells,0..)|cell,i|{std.debug.assert(M.validCell(cell,state.planet.microbeStats.next_lineage));for(cell.cohorts)|co|{if(co.lineage==524 or (co.biomass>0 and co.root_fraction>0))Audit.emit("FATE",.{.tick=tick+1,.cell=i,.cohort=co,.soil=state.planet.landSoil[i],.depth_m=state.planet.waterMass[i]*state.planet.getKmPerWaterMass()*1000,.temperature=state.planet.temperature[i],.height=M.producerHeightMeters(co)});}}
      for(state.planet.landSoil)|v|std.debug.assert(std.math.isFinite(v) and v>=0 and v<=1);for(state.planet.landVapor)|v|std.debug.assert(std.math.isFinite(v) and v>=0);
      if(tick+1==30 or tick+1==60){var sa=std.heap.ArenaAllocator.init(allocator);defer sa.deinit();const aa=sa.allocator();const saved=try std.json.stringifyAlloc(aa,try saves.capture(aa,state),.{});try std.fs.cwd().writeFile(.{.sub_path=try std.fmt.allocPrint(aa,"BASE/{s}arm-{}-{}.json",.{if(resumed)"resume-"else "",@intFromBool(ablated),tick+1}),.data=saved});}
      if(timer.read()>900*std.time.ns_per_s)return error.FixedRuntimeBudget;
      const stat=try std.fs.cwd().statFile(try std.fmt.allocPrint(a,"BASE/{s}-{}.log",.{mode,@intFromBool(ablated)}));if(stat.size>512*1024*1024)return error.FixedLogBudget;
    }
    std.debug.print("COMPLETE arm={} resumed={} ticks={} elapsed_ms={}\n",.{@intFromBool(ablated),resumed,60-start,timer.read()/1000000});std.process.exit(0);'''
# Audit emit defaults enabled? explicitly enable setup logging too.
code=code.replace('    const ablated=', '    Audit.enabled=true;\n    const ablated=')
s=s[:a]+code.replace('BASE',str(base)).replace('INPUT',str(src.parent/'day-30.json'))+s[b:];p.write_text(s)
changes=[str(p.relative_to(o))for p in o.rglob('*.zig')if p.read_bytes()!=(src/p.relative_to(o)).read_bytes()];assert changes==['main.zig'];(base/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},indent=2));print(base)
