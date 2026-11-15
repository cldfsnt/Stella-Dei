from pathlib import Path
r=Path(__file__).resolve().parents[2]
s=(r/'src/simulation/microbes.zig').read_text()
s='//! Generated experimental copy; production unchanged. See prepare-shared-pace.py.\n'+s
needle='pub fn step(cell:*Cell,env:Environment,elapsed:f32) Flux {'
assert s.count(needle)==1
s=s.replace(needle,'pub fn step(cell:*Cell,env:Environment,elapsed:f32) Flux {return stepPaced(cell,env,elapsed,.{1,1,1,1});}\npub fn stepPaced(cell:*Cell,env:Environment,elapsed:f32,pace:[4]f32) Flux {')
needle='potentials[i]=frondMass(c)*(@exp(@min(20,rate*days))-1)*space;'
assert s.count(needle)==1
s=s.replace(needle,needle[:-1]+'*pace[i];')
(r/'src/experimental/shared_pace_core.zig').write_text(s)
