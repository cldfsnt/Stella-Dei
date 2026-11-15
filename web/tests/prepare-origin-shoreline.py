from pathlib import Path
import shutil,hashlib,json
r=Path(__file__).resolve().parents[2];s=r.parent/'site-tmp/origin-root-drain/src';b=r.parent/'site-tmp/origin-shoreline';o=b/'src';assert not o.exists();shutil.copytree(s,o)
p=o/'main.zig';t=p.read_text().replace(str(s.parent),str(b));t=t.replace('    const ablated=', '    const depth_index=try std.fmt.parseInt(usize,std.posix.getenv("QA_DEPTH") orelse "0",10);if(depth_index>=4)return error.InvalidDepth;const target=([_]f32{0,0.001,0.01,0.1})[depth_index];\n    const ablated=')
# Every output filename gains depth prefix, original immutable day30 input remains unchanged.
t=t.replace('arm-{}-', 'depth-{}-arm-{}-').replace('.{@intFromBool(ablated)}', '.{depth_index,@intFromBool(ablated)}').replace('.{if(resumed)"resume-"else "",@intFromBool(ablated),tick+1}', '.{if(resumed)"resume-"else "",depth_index,@intFromBool(ablated),tick+1}')
t=t.replace('setSelectedWaterTarget(18327,0)', 'setSelectedWaterTarget(18327,target)').replace('and state.planet.waterMass[18327]==0 and', 'and state.planet.waterMass[18327]>=0 and')
t=t.replace('      state.planet.waterMass[18327]=old;', '      const new_water=state.planet.waterMass[18327];state.planet.waterMass[18327]=old;').replace('state.planet.waterMass[18327]=0;', 'state.planet.waterMass[18327]=new_water;')
t=t.replace('.removed_kg=@as(f64,old)*1e9', '.removed_kg=(@as(f64,old)-@as(f64,new_water))*1e9,.requested_target_m=target,.actual_target_m=new_water*state.planet.getKmPerWaterMass()*1000')
t=t.replace('      for(state.planet.microbeCells,0..)', '      Audit.emit("PATCH",.{.tick=tick+1,.cell=18327,.cohorts=state.planet.microbeCells[18327].cohorts,.soil=state.planet.landSoil[18327],.depth_m=state.planet.waterMass[18327]*state.planet.getKmPerWaterMass()*1000,.temperature=state.planet.temperature[18327]});\n      for(state.planet.microbeCells,0..)')
t=t.replace('/{s}-{}.log', '/{s}-{}-{}.log').replace('.{mode,@intFromBool(ablated)}', '.{mode,depth_index,@intFromBool(ablated)}')
p.write_text(t);(b/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},indent=2));assert [str(p.relative_to(o))for p in o.rglob('*.zig')if p.read_bytes()!=(s/p.relative_to(o)).read_bytes()]==['main.zig']
