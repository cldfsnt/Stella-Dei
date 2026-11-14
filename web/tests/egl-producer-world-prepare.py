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
