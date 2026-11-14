#!/usr/bin/env python3
"""Fresh production Habitat→Seed coupled gate. No environment or selection overrides."""
from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent
out=Path(sys.argv[1])
subprocess.run([sys.executable,str(here/'egl-origin-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text();a=s.index('    if (std.posix.getenv("STELLA_ORIGIN_COUPLED")');b=s.index('        return;',a)+len('        return;')
p.write_text(s[:a]+(here/'egl-origin-coupled.zig.part').read_text()+s[b:])
