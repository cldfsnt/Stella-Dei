from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];t=r.parent/'site-tmp';b=t/'graded-compact';o=b/'src';assert not o.exists();shutil.copytree(t/'graded-protection/src',o)
s=(o/'simulation/microbes.zig').read_text();same=(t/'graded-world/src/simulation/microbes.zig').read_text();assert s==same
s=s.replace('protective_investment:f32=0, protective_recovery:f32=0, protective_rest:bool=false,','protective_investment:f32=0, protective_clock:f32=-1,')
s=s.replace('child.protective_rest=false;child.protective_recovery=0;','child.protective_clock=-1;')
s=s.replace('c.protective_rest=false;c.protective_recovery=0;','c.protective_clock=-1;')
s=s.replace('c.protective_rest=true;c.protective_recovery=0;','c.protective_clock=0;')
s=s.replace('c.protective_rest','(c.protective_clock>=0)').replace('c.protective_recovery','c.protective_clock')
assert 'protective_rest'not in s and 'protective_recovery'not in s
(o/'simulation/compact_microbes.zig').write_text(s)
shutil.copy2(r/'web/tests/graded-compact-tests.zig',o/'compact_tests.zig')
(b/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},indent=2))
