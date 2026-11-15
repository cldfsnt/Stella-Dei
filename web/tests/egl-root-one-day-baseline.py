#!/usr/bin/env python3
"""Matched diagnostic production day, not a rerun/tuning of candidate outcomes."""
from pathlib import Path
import subprocess,sys
r=Path(__file__).resolve().parents[2];out=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(r/'web/tests/egl-hydration-coupled-prepare.py'),str(out),'baseline'],check=True)
p=out/'main.zig';s=p.read_text();needle='const ticks:usize=if(arm==0)10 else 420;';assert s.count(needle)==1
p.write_text(s.replace(needle,'const ticks:usize=if(arm==0)60 else 420;',1))
