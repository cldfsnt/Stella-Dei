#!/usr/bin/env python3
from pathlib import Path
import os,sys,subprocess
here=Path(__file__).resolve().parent;root=Path(os.environ['STELLA_SOURCE_ROOT']);out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-nursery-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text()
if '--sandbox' in sys.argv:
 s=s.replace('game.startOriginNext = true;','game.startOriginNext = false;');a=s.index('    var max_structure:f32=0;');b=s.index('fn originReport(',a);s=s[:a]+(here/'clock-sandbox.zig.part').read_text()+s[b:]
else:
 s=s.replace('if (!is_web or !web_initialized or !game.state_init) return null;','if (!game.state_init) return null; // native harness only; actual callback body unchanged')
 needle='    if (std.posix.getenv("STELLA_ORIGIN_COUPLED") != null) {';s=s.replace(needle,(here/'clock-callbacks.zig.part').read_text()+needle)
p.write_text(s)
