import os,sys,subprocess
from pathlib import Path
root=Path(os.environ['STELLA_SOURCE_ROOT']).resolve();out=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(root/'web/tests/fit-life/qa/prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text();a=s.index('    if(std.posix.getenv("QA_REPLAY_SAVE"))');b=s.index('    { std.debug.assert(state.focusSeedableHabitat());',a)
s=s[:a]+Path(__file__).with_name('replay.part').read_text()+s[b:];p.write_text(s)
# Native generated source already substitutes browser mobile predicates. Keep them.
