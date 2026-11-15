#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(r/'web/tests/egl-playable-ecology-prepare.py'),str(o)],check=True)
p=o/'main.zig';s=p.read_text().replace('state.gameTime-start<7*86400','state.gameTime-start<14*86400').replace('day==7','day==14').replace('if(day==3 or day==14)','if(day==7 or day==14)')
s=s.replace('const nursery=state.makeSelectedNursery(point);','const nursery=state.makeSelectedSunlitNursery(point);')
s=s.replace('    const start=state.gameTime;','    var qa_timer=try std.time.Timer.start();\n    const start=state.gameTime;')
needle='        std.debug.print("PLAYABLE_STATS day='
i=s.index(needle)
s=s[:i]+r'''
        var forms=[_]usize{0}**6;var feeding:usize=0;var supported:usize=0;
        for(state.planet.microbeCells)|patch|for(patch.cohorts)|co|{if(co.biomass>0){forms[@intFromEnum(M.producerForm(co))]+=1;if(co.lifetime_grazed>0)feeding+=1;if(co.support_mass>0)supported+=1;}};
        std.debug.print("SUNLIT14_DAY {s}\n",.{try std.json.stringifyAlloc(allocator,.{.day=day,.forms=forms,.feeding_history=feeding,.supported=supported,.stats=state.planet.microbeStats,.oxygen=state.planet.oxygen},.{})});
''' +s[i:]
# oxygen field may not be direct; omit to keep exact core receipt only.
s=s.replace(',.oxygen=state.planet.oxygen','')
needle='    std.debug.print("EARLY_EXPLICIT_FIT result={d} rendered_before={d} rendered_after={d} time_births_arrivals_unchanged=true no_auto_framing=true\\n",.{fitted,before,state.visibleSprouts});';assert needle in s
s=s.replace(needle,needle+r'''
    const end_bytes=try std.json.stringifyAlloc(aa,try saves.capture(aa,state),.{});
    const end_parsed=try std.json.parseFromSlice(saves.schema.Save,aa,end_bytes,.{.allocate=.alloc_always});
    try saves.apply(state,end_parsed.value);
    std.debug.assert(std.mem.eql(u8,end_bytes,try std.json.stringifyAlloc(aa,try saves.capture(aa,state),.{})));
    std.debug.print("SUNLIT14_PASS elapsed_wall_ms={} full_endpoint_reload_exact=true explicit_qa_exit_skips_teardown=true\n",.{qa_timer.read()/1000000});
    std.process.exit(0);
''')
s='extern fn qa_capture(path:[*:0]const u8) void;\n'+s
s=s.replace('    const end_bytes=try std.json.stringifyAlloc','    qa_capture("'+str(o.parent/'day14-fit.ppm')+'");\n    const end_bytes=try std.json.stringifyAlloc')
p.write_text(s)
subprocess.run([sys.executable,str(r/'web/tests/audit-zig-exports.py'),str(r/'src/main.zig'),str(p)],check=True,stdout=(o.parent/'export-audit.json').open('w'))
(o.parent/'provenance.json').write_text(json.dumps({'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip(),'days':14,'seed':42,'source':{f:{'production':hashlib.sha256((r/'src'/f).read_bytes()).hexdigest(),'copy':hashlib.sha256((o/f).read_bytes()).hexdigest()}for f in ['simulation/planet.zig','simulation/microbes.zig','pond_action.zig','states/play.zig','main.zig']}},indent=2)+'\n')
