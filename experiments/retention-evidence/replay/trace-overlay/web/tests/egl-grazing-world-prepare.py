#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent;out=Path(sys.argv[1])
subprocess.run([sys.executable,str(here/'egl-structure-world-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text();marker='        try originSaveCheck(state,allocator);\n        return;'
extra='''        var capable:usize=0;var observed:usize=0;var top_feeding:f32=0;
        for(state.planet.microbeCells)|cell|for(cell.cohorts)|co|{if(co.biomass>0){if(co.feeding>0)capable+=1;if(co.lifetime_grazed>0)observed+=1;top_feeding=@max(top_feeding,co.feeding);}};
        std.debug.print("GRAZING_WORLD capable={d} observed={d} max_feeding={d} consumed_kgC={d} respired_kgC={d}\\n",.{capable,observed,top_feeding,state.planet.microbeStats.grazed_carbon,state.planet.microbeStats.grazing_respired_carbon});
'''
assert marker in s;s=s.replace(marker,extra+marker);s=s.replace('if(i<6 or (if(fast) i%60==59 else i%1440==1439))','if(i==0 or (if(fast) i%300==299 else i%1440==1439))')
p.write_text(s)
