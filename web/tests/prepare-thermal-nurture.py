from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];t=r.parent/'site-tmp';e=r/'web/tests/continuation-review/thermal-nurture';e.mkdir(exist_ok=True)
insert='''
      const before_water=try qaThermalBytes(a,state);const before_parsed=try saves.schema.parse(a,before_water);const old_water=state.planet.waterMass[point];
      if(!state.testAction(@intFromEnum(@as(@TypeOf(state.selectedTool),.EmitWater))))return error.WaterRefused;
      var water_only=try saves.capture(a,state);water_only.water=before_parsed.value.water;std.debug.assert(std.mem.eql(u8,before_water,try std.json.stringifyAlloc(a,water_only,.{})));
      Audit.emit("WATER_INPUT",.{.point=point,.before=old_water,.after=state.planet.waterMass[point],.added_kg=(@as(f64,state.planet.waterMass[point])-old_water)*1e9,.area=state.planet.getMeanPointArea()});
      for(0..6)|step|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;Audit.emit("NURTURE",.{.step=step+1,.soil=state.planet.landSoil[point],.depth_m=state.planet.waterMass[point]*state.planet.getKmPerWaterMass()*1000,.temperature=state.planet.temperature[point]});}
      const before_target=try qaThermalBytes(a,state);const target_parsed=try saves.schema.parse(a,before_target);const old_target=state.planet.waterMass[point];const changed=state.setSelectedWaterTarget(point,0.01);std.debug.assert(std.math.isFinite(changed));
      var target_only=try saves.capture(a,state);target_only.water=target_parsed.value.water;std.debug.assert(std.mem.eql(u8,before_target,try std.json.stringifyAlloc(a,target_only,.{})));
      Audit.emit("WATER_DRAWDOWN",.{.point=point,.before=old_target,.after=state.planet.waterMass[point],.signed_added_kg=(@as(f64,state.planet.waterMass[point])-old_target)*1e9,.actual_change_m=changed});
      try std.fs.cwd().writeFile(.{.sub_path="OUTPUT/preseed.json",.data=try qaThermalBytes(a,state)});
'''
for kind in ['control','candidate']:
 base=t/'thermal-fresh'/kind;b=t/'thermal-nurture'/kind;o=b/'src';assert not o.exists();shutil.copytree(base/'src',o);shutil.copy2(base/'spin.json',b/'spin.json')
 p=o/'main.zig';s=p.read_text().replace(str(base),str(b));needle='    if(!spin and !resumed){\n';assert needle in s;s=s.replace(needle,needle+insert.replace('OUTPUT',str(b)),1);p.write_text(s)
 p=o/'save_game.zig';p.write_text(p.read_text().replace(str(base),str(b)))
 (e/(kind+'-source-hashes.json')).write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},indent=2)+'\n')
