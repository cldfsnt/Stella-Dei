#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent;out=Path(sys.argv[1])
subprocess.run([sys.executable,str(here/'egl-origin-coupled-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text().replace('if(fast)300 else 7200','if(fast)1200 else 7200')
s=s.replace('    var state = &game.state.Playing;','    var max_structure:f32=0;var max_generation:u32=0;\n    var state = &game.state.Playing;')
s=s.replace('state.update(&game,1.0/60.0);','state.update(&game,1.0/60.0);\n            for(state.planet.microbeCells)|cell|for(cell.cohorts)|co|{if(co.biomass>0){max_structure=@max(max_structure,co.structure);max_generation=@max(max_generation,co.generation);}};')
s=s.replace('try originSaveCheck(state,allocator);\n        return;','std.debug.print("STRUCTURE_WORLD max_structure={d} max_generation={d} failed_patches={d}\\n",.{max_structure,max_generation,state.planet.microbeStats.failed_patches});\n        try originSaveCheck(state,allocator);\n        return;')
p.write_text(s)
