from pathlib import Path
import sys,subprocess
here=Path(__file__).resolve().parent;out=Path(sys.argv[1]);subprocess.run([sys.executable,str(here/'egl-world-menu-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text();needle=' game.loop.pump(1024);\n try saves.replaceWorld(state,created_parsed.value);';assert needle in s
s=s.replace(needle,''' try waterlineDump(state,a,"wet");
 state.selectedPoint=13888;const changed=state.setSelectedWaterTarget(13888,0.1);std.debug.assert(std.math.isFinite(changed));
 try waterlineDump(state,a,"exposed");
'''+needle)
s+=r'''
fn waterlineDump(state:*PlayState,a:std.mem.Allocator,label:[]const u8)!void{
 const save=@import("save_game.zig");const M=@import("simulation/microbes.zig");const index:usize=13888;
 const before=try std.json.stringifyAlloc(a,try save.capture(a,state),.{});
 const cell=state.planet.microbeCells[index];const depth=state.planet.waterMass[index]*state.planet.getKmPerWaterMass();
 const observation=@import("waterline_observation.zig").inspect(cell,depth,state.planet.temperature[index],index,&state.planet.propaguleFeedback.events);
 const after=try std.json.stringifyAlloc(a,try save.capture(a,state),.{});std.debug.assert(std.mem.eql(u8,before,after));
 const snapshot=try std.json.stringifyAlloc(a,.{.status="origin",.cell=index,.day=state.gameTime/86400,.water_m=depth*1000,.temperature_c=state.planet.temperature[index]-273.15,.nutrients=cell.nutrient,.detritus=cell.detritus,.simulation_light=M.availableLight(@max(0,state.planet.transformedPoints[index].norm().dot(state.simulationSolarVector()))*std.math.clamp(state.solarConstant/1361,0,2),depth),.seed_reason=@tagName(state.planet.seedEligibility(index)),.cohorts=cell.cohorts,.waterline=observation},.{});
 const root=std.posix.getenv("QA_WATERLINE_OUTPUT") orelse unreachable;const path=try std.fmt.allocPrint(a,"{s}/{s}.json",.{root,label});const file=try std.fs.createFileAbsolute(path,.{});defer file.close();try file.writeAll(snapshot);
 std.debug.print("WATERLINE_UI case={s} zone={s} actual_depth_m={d} living_descendants={d} supported={d} observation_full_save_unchanged=true schema={d}\n",.{label,observation.zone,depth*1000,observation.living_descendants,observation.supported_descendants,save.schema.VERSION});

}
''';p.write_text(s)
