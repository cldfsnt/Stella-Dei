#!/usr/bin/env python3
"""Controlled actual-engine motility QA; never alters production source."""
from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent;out=Path(sys.argv[1])
subprocess.run([sys.executable,str(here/'egl-origin-prepare.py'),str(out)],check=True)
subprocess.run(['patch','-p1','-d',str(out),'-i',str(here/'egl-motility-trace.patch')],check=True)
p=out/'main.zig';s=p.read_text();a=s.index('    if (std.posix.getenv("STELLA_ORIGIN_COUPLED")');b=s.index('\nfn originReport',a);s=s[:a]+(here/'egl-motility-render.zig.part').read_text()+s[b:];a=s.index('fn originSaveCheck(');p.write_text(s[:a]+(here/'egl-motility-save.zig.part').read_text())
