#!/usr/bin/env python3
"""Same native binary baseline/candidate switch; copied production only."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1]);subprocess.run([sys.executable,str(root/'web/tests/egl-atmosphere-phase-profile-prepare.py'),str(out)],check=True)
p=out/'simulation/planet.zig';s=p.read_text();needle='        const phase_step=AtmosphereWater.PhaseStep.init(dt);';assert needle in s;s=s.replace(needle,needle+'const use_phase_cache=std.posix.getenv("STELLA_PHASE_CACHE")!=null;',1);needle='phase_step.phase(liquid,vapor,saturation,temperature,self.rainfall[i]) orelse continue';assert needle in s;s=s.replace(needle,'(if(use_phase_cache) phase_step.phase(liquid,vapor,saturation,temperature,self.rainfall[i]) else @import("../experimental/phase_reference.zig").phase(liquid,vapor,saturation,temperature,dt,self.rainfall[i])) orelse continue',1);p.write_text(s)
p=out/'main.zig';s=p.read_text();needle='  phase.enabled=false;';assert needle in s;s=s.replace(needle,'  if(std.posix.getenv("STELLA_PHASE_MEASURED_PATH"))|path|{const measured=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});try std.fs.cwd().writeFile(.{.sub_path=path,.data=measured});}\n'+needle,1);p.write_text(s)
