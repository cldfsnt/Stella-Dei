from pathlib import Path
import sys,shutil
src=Path(sys.argv[1]);out=Path(sys.argv[2]);shutil.copytree(src,out,dirs_exist_ok=True)
p=out/'main.zig';s=p.read_text()
production=(Path(__file__).resolve().parents[2]/'src/main.zig').read_text()
def export_body(text,name):
 start=text.index('export fn '+name+'(');brace=text.index('{',start);level=1;i=brace+1
 while level:
  if text[i]=='{':level+=1
  elif text[i]=='}':level-=1
  i+=1
 return text[start:i]
s=s.replace(export_body(s,'stella_make_pond'),export_body(production,'stella_make_pond'))
needle='          std.debug.print("ROOT_ONLY_COPY_READY no_model_activation=true\\n",.{});';assert s.count(needle)==1
s=s.replace(needle,r'''
          const legacy=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const original=try std.json.parseFromSlice(saves.schema.Save,a,legacy,.{.allocate=.alloc_always});
          try state.planet.ensureRootSoil();state.planet.rootConfig=.{.enabled=true,.law=1,.conductance=10};
          var donor_found=false;
          for(state.planet.microbeCells,0..)|*cell,i|{for(&cell.cohorts)|*co|{if(co.lineage==478 and co.biomass>0){co.root_fraction=0.25;state.planet.rootSoil[i]=0.125;donor_found=true;}}}
          std.debug.assert(donor_found);
          const enabled=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const decoded=try std.json.parseFromSlice(saves.schema.Save,a,enabled,.{.allocate=.alloc_always});
          for(0..10)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
          const uninterrupted=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          try saves.apply(state,decoded.value);std.debug.assert(std.mem.eql(u8,enabled,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          for(0..10)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
          const resumed=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          try std.fs.cwd().writeFile(.{.sub_path="uninterrupted.json",.data=uninterrupted});try std.fs.cwd().writeFile(.{.sub_path="resumed.json",.data=resumed});
          std.debug.assert(std.mem.eql(u8,uninterrupted,resumed));std.debug.print("ROOT_SAVE continuation_exact=true enabled_roundtrip=true\n",.{});
          // Actual native apply refusal must retain complete current model, not only fields under test.
          for(0..7)|case|{
            var invalid=decoded.value;var origin=invalid.origin.?;
            switch(case){0=>invalid.version=9,1=>origin.root_config.?.law=2,2=>origin.root_config.?.conductance=2,3=>origin.root_soil=origin.root_soil[0..1],4=>{const bad=try a.dupe(f64,origin.root_soil);bad[0]=std.math.nan(f64);origin.root_soil=bad;},5=>{origin.root_config=.{.enabled=false};},6=>{invalid.version=6;origin.model_revision=5;},else=>unreachable}
            invalid.origin=origin;
            if(saves.apply(state,invalid)) |_| {return error.ExpectedRefusal;} else |_| {}
            std.debug.assert(std.mem.eql(u8,resumed,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          }
          const rejected_dir=try std.process.getEnvVarOwned(a,"QA_REJECTED_DIR");
          for(0..6)|arm|{
            const path=try std.fmt.allocPrint(a,"{s}/arm-{d}.json",.{rejected_dir,arm});const bytes=try std.fs.cwd().readFileAlloc(a,path,128*1024*1024);
            if(saves.schema.parse(a,bytes)) |parsed| {defer parsed.deinit();if(saves.apply(state,parsed.value)) |_| {return error.ExpectedRefusal;} else |_| {}} else |_| {}
            std.debug.assert(std.mem.eql(u8,resumed,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          }
          var sandbox=original.value;sandbox.mode=.sandbox;sandbox.origin=null;try saves.apply(state,sandbox);std.debug.assert(!state.planet.rootConfig.enabled);for(state.planet.rootSoil)|v|std.debug.assert(v==0);
          const raw_path=try std.process.getEnvVarOwned(a,"QA_PULSE_SAVE");const raw=try std.fs.cwd().readFileAlloc(a,raw_path,128*1024*1024);const raw_parsed=try saves.schema.parse(a,raw);std.debug.assert(raw_parsed.value.version==6);try saves.apply(state,raw_parsed.value);std.debug.assert(!state.planet.rootConfig.enabled);
          try saves.apply(state,original.value);std.debug.assert(!state.planet.rootConfig.enabled);for(state.planet.rootSoil)|v|std.debug.assert(v==0);
          std.debug.assert(std.mem.eql(u8,legacy,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.print("ROOT_SAVE_PASS invalid7_atomic=true experimental6_rejected=true disabled_restore=true prescribed_soil=true\n",.{});
''');p.write_text(s)
