#!/usr/bin/env python3
"""Instrument copied native cooperative web-frame proxy; never production edits."""
from pathlib import Path
import subprocess,sys,json,hashlib
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-full-frame-profile-prepare.py'),str(out)],check=True)
p=out/'loop.zig';s=p.read_text();s=s.replace('const TaskStack =', 'pub var qa_enabled:bool=false;\npub var qa_jobs:u64=0;\npub var qa_ns:u64=0;\npub var qa_max:u64=0;\npub fn qa_reset()void{qa_jobs=0;qa_ns=0;qa_max=0;}\nconst TaskStack =',1)
s=s.replace('            data.fnPtr(data.userdata);','            var qa_timer=std.time.Timer.start() catch unreachable;\n            data.fnPtr(data.userdata);\n            if(qa_enabled){const ns=qa_timer.read();qa_jobs+=1;qa_ns+=ns;qa_max=@max(qa_max,ns);}',1);p.write_text(s)
p=out/'main.zig';s=p.read_text();i=s.index('\nfn profileFrames(');s=s[:i]+(root/'web/tests/pump-profile.zig.part').read_text();p.write_text(s)
manifest={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [root/'src/main.zig',root/'src/loop.zig',root/'src/states/play.zig',root/'src/simulation/planet.zig',root/'web/shell.html']}
(out/'pump-input-hashes.json').write_text(json.dumps(manifest,indent=2))
