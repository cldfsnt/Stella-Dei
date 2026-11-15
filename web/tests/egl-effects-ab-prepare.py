#!/usr/bin/env python3
"""Actual earned receipt rendering ON/OFF only. Never modifies production biology."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1]);subprocess.run([sys.executable,str(root/'web/tests/egl-laptop-render-prepare.py'),str(out),sys.argv[2]],check=True)
(out/'qa_effects.zig').write_text('pub var off:bool=false;pub var potential:u64=0;pub var drawn:u64=0;pub var arrivals:u64=0;pub var deaths:u64=0;\n')
p=out/'states/play.zig';s=p.read_text();a=s.index('    fn renderPropaguleFeedback(');b=s.index('\n    /// Read-only Seed map',a);part=s[a:b];needle='            const x=pos.x();const y=pos.y();';assert needle in part;part=part.replace(needle,'            const qa=@import("../qa_effects.zig");qa.potential+=1;if(qa.off)continue;qa.drawn+=1;if(pulse.event.kind==.arrival)qa.arrivals+=1 else qa.deaths+=1;\n'+needle);s=s[:a]+part+s[b:];p.write_text(s)
p=out/'main.zig';s=p.read_text();needle='try profileFrames("cached30d",state,window,allocator);';assert needle in s;s=s.replace(needle,'''const base_time=state.gameTime;var extra:usize=0;
while(state.planet.propaguleFeedback.next_serial<13 and extra<420):(extra+=1){state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
std.debug.print("REAL_RECEIPTS extra_hours={d} events={d} attempts={d} arrivals={d} losses={d} fabricated=false\\n",.{(state.gameTime-base_time)/3600,state.planet.propaguleFeedback.next_serial-1,state.planet.propaguleAttempts,state.planet.propaguleArrivals,state.planet.propaguleTrackedLosses});
try profileFrames("natural_receipts",state,window,allocator);''')
s=s.replace(' const bytes=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});',' const receipts=state.planet.propaguleFeedback;const pulses=state.propaguleVisuals;const qa=@import("qa_effects.zig");qa.off=std.posix.getenv("STELLA_EFFECTS_OFF")!=null;\n const bytes=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});')
s=s.replace('try saves.apply(state,frozen.value);state.paused=', 'try saves.apply(state,frozen.value);state.planet.propaguleFeedback=receipts;state.propaguleVisuals=pulses;state.paused=')
s=s.replace('  qa_reset_draws();perf.metrics.setEnabled(true);','  qa.potential=0;qa.drawn=0;qa.arrivals=0;qa.deaths=0;qa_reset_draws();perf.metrics.setEnabled(true);')
s=s.replace('  qa_report_draws();const physics=', '  std.debug.print("EFFECTS_SCOPE off={} potential_draws={d} actual_draws={d} arrival_draws={d} death_draws={d}\\n",.{qa.off,qa.potential,qa.drawn,qa.arrivals,qa.deaths});const result_json=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});var digest:[32]u8=undefined;std.crypto.hash.sha2.Sha256.hash(result_json,&digest,.{});std.debug.print("EFFECTS_WORLD stage={s} speed={d} sha256={s}\\n",.{label,speed,std.fmt.fmtSliceHexLower(&digest)});\n  qa_report_draws();const physics=')
p.write_text(s)
