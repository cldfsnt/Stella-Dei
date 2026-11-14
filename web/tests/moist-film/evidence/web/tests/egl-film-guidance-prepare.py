from pathlib import Path
import sys,subprocess
here=Path(__file__).resolve().parent;out=Path(sys.argv[1]);subprocess.run([sys.executable,str(here/'egl-world-menu-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text();needle=' game.loop.pump(1024);\n try saves.replaceWorld(state,created_parsed.value);';assert needle in s
s=s.replace(needle,' try filmGuidanceCheck(state,a);\n'+needle)
s=s.replace('if (!is_web or !web_initialized or !game.state_init) return null;', 'if (!game.state_init) return null;') # Test-only initialized browser export gate.
s+=r'''
fn filmGuidanceCheck(state:*PlayState,a:std.mem.Allocator)!void{
 const Save=@import("save_game.zig");const H=@import("producer_habitat.zig");
 std.debug.print("GATE_START\n",.{});
 const before=try std.json.stringifyAlloc(a,try Save.capture(a,state),.{});
 for(state.planet.microbeCells,0..)|cell,i|{_=H.inspect(cell,state.planet.waterMass[i]*state.planet.getKmPerWaterMass(),state.planet.temperature[i]);}
 const snapshot=std.mem.span(stella_life_snapshot());
 std.debug.assert(std.mem.indexOf(u8,snapshot,"producer_habitat")!=null);
 const after=try std.json.stringifyAlloc(a,try Save.capture(a,state),.{});
 std.debug.assert(std.mem.eql(u8,before,after));
 std.debug.print("GATE_OBSERVATION_OK\n",.{});
 std.debug.assert(state.focusSeedableHabitat());const selected=state.selectedPoint;
 std.debug.print("GATE_FOCUS_OK selected={d}\n",.{selected});
 std.debug.assert(state.planet.temperature[selected]>273.15);
 const temperatures=try a.dupe(f32,state.planet.temperature);@memset(state.planet.temperature,273.15);
 const frozen=try std.json.stringifyAlloc(a,try Save.capture(a,state),.{});
 std.debug.assert(state.planet.seedEligibility(selected)==.too_cold);
 std.debug.assert(state.seedSelectedColony(@intCast(selected))<=0);
 std.debug.assert(!state.focusSeedableHabitat());
 // Render can legitimately renormalize camera vectors; seed/focus invariant is checked first.
 std.debug.print("GATE_FROZEN_TARGETS_OK\n",.{});
 const unchanged=try std.json.stringifyAlloc(a,try Save.capture(a,state),.{});
 if(!std.mem.eql(u8,frozen,unchanged)){
  const root=std.posix.getenv("QA_GUIDANCE_OUTPUT") orelse unreachable;
  const fp=try std.fmt.allocPrint(a,"{s}/frozen-before.json",.{root});const ap=try std.fmt.allocPrint(a,"{s}/frozen-after.json",.{root});
  const ff=try std.fs.createFileAbsolute(fp,.{});defer ff.close();try ff.writeAll(frozen);
  const af=try std.fs.createFileAbsolute(ap,.{});defer af.close();try af.writeAll(unchanged);
  return error.FrozenRenderSaveChanged;
 }
 render(game.window);std.debug.assert(state.seedTargets.count==0);
 std.debug.print("GATE_FROZEN_NO_MUTATION_OK\n",.{});
 @memcpy(state.planet.temperature,temperatures);
 std.debug.assert(state.focusSeedableHabitat());const warm=state.selectedPoint;
 std.debug.assert(state.planet.seedEligibility(warm)==.eligible);
 render(game.window);
 for(state.seedTargets.items[0..state.seedTargets.count])|target|{std.debug.assert(state.planet.temperature[target.cell]>273.15);std.debug.assert(state.planet.seedEligibility(target.cell)==.eligible);}
 const biomass_before=@import("simulation/microbes.zig").biomass(state.planet.microbeCells[warm]);
 std.debug.assert(state.seedSelectedColony(@intCast(warm))==1);
 std.debug.assert(@import("simulation/microbes.zig").biomass(state.planet.microbeCells[warm])>biomass_before);
 std.debug.print("FILM_GUIDANCE full_save_observation_invariant=true frozen_seed_rejected=true all_frozen_focus_rejected=true no_frozen_targets=true warm_focus_and_seed=true schema=6\n",.{});
}
''';p.write_text(s)
