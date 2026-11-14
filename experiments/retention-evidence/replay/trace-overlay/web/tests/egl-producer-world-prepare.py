#!/usr/bin/env python3
"""Isolated actual-engine producer acceptance, ordinary scenario never injects traits."""
from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent;out=Path(sys.argv[1])
subprocess.run([sys.executable,str(here/'egl-motility-world-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text();needle='    if (std.posix.getenv("STELLA_ORIGIN_COUPLED") != null) {'
assert needle in s;s=s.replace(needle,(here/'egl-producer-migration.zig.part').read_text()+needle,1)
needle='        try originSaveCheck(state,allocator);\n        return;'
report='''        var organized:usize=0;var supported:usize=0;var support:f64=0;var biomass:f64=0;
        for(state.planet.microbeCells)|cell|for(cell.cohorts)|co|{if(co.biomass>0){biomass+=co.biomass;support+=co.support_mass;if(co.organization>0)organized+=1;if(co.support_mass>0)supported+=1;std.debug.assert(co.support_mass>=0 and co.support_mass<=co.biomass);}};
        std.debug.print("PRODUCER_WORLD inherited_capable={d} actual_supported={d} support_density_sum={d} biomass_density_sum={d}\\n",.{organized,supported,support,biomass});
'''
assert needle in s;s=s.replace(needle,report+needle);p.write_text(s)

s=p.read_text();a=s.index('    const seed=state.selectedPoint;');b=s.index('fn originReport(',a);s=s[:a]+(here/'egl-producer-controlled.zig.part').read_text()+'\n'+s[b:];p.write_text(s)

s=p.read_text();s=s.replace(' state.planet.worldMode=.sandbox;', ' var support_mutated:usize=0;for(state.planet.microbeCells)|*cell|for(&cell.cohorts)|*co|{if(co.support_mass>0){co.support_mass=0;support_mutated+=1;}};\n std.debug.print("SUPPORT_RESTORE mutated_cohorts={d}\\n",.{support_mutated});\n state.planet.worldMode=.sandbox;');p.write_text(s)

s=p.read_text().replace("if(fast)1200 else 7200", "if(fast) (if(std.posix.getenv(\"STELLA_PRODUCER_LONG\") != null) @as(usize,6000) else 1200) else 7200");p.write_text(s)

p=out/'states/play.zig';s=p.read_text().replace('std.rand.DefaultPrng.init(1337)', 'std.rand.DefaultPrng.init(if(std.posix.getenv("STELLA_PRODUCER_SEED")) |seed_text| std.fmt.parseInt(u64,seed_text,10) catch 1337 else 1337)');p.write_text(s)
p=out/'main.zig';s=p.read_text().replace('        var update_total_ns:u64=0;', '        var ever_support:f32=0;var ever_organization:f32=0;\n        var update_total_ns:u64=0;').replace('            const tick_ns=tick_timer.read();','            for(state.planet.microbeCells)|cc|for(cc.cohorts)|co|{ever_support=@max(ever_support,co.support_mass);ever_organization=@max(ever_organization,co.organization);};\n            const tick_ns=tick_timer.read();').replace('        var organized:usize=0;', '        std.debug.print("PRODUCER_EVER max_support={d} max_organization={d}\\n",.{ever_support,ever_organization});\n        var organized:usize=0;');p.write_text(s)

s=p.read_text().replace("try originSaveCheck(state,allocator);", "try originSaveCheck(state,allocator);loop.pump(1024);");p.write_text(s)

s=p.read_text().replace('    if (std.posix.getenv("STELLA_ORIGIN_COUPLED") != null) {', '    if(std.posix.getenv("STELLA_PRODUCER_EXPAND") != null){\n        const center=state.selectedPoint;var edited:usize=0;var actions:usize=0;\n        for(state.planet.getNeighbours(center))|neighbor|{\n            state.selectedPoint=neighbor;var depth=state.planet.waterMass[neighbor]*state.planet.getKmPerWaterMass()*1000;\n            if(depth>5)continue;\n            while(depth<1.5 and actions<1000){_=state.adjustSelectedWater(@intCast(neighbor),0.1);actions+=1;depth=state.planet.waterMass[neighbor]*state.planet.getKmPerWaterMass()*1000;}\n            edited+=1;\n        }\n        state.selectedPoint=center;\n        std.debug.print("PLAYER_HABITAT neighboring_patches={d} actual_plus01m_actions={d} biology_assigned=false\\n",.{edited,actions});\n    }\n'+'    if (std.posix.getenv("STELLA_ORIGIN_COUPLED") != null) {',1);p.write_text(s)
