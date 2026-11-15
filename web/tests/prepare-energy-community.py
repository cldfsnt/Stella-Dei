#!/usr/bin/env python3
"""Generate isolated actual-core copy with per-cohort acquisition capacity only."""
from pathlib import Path
import hashlib
root=Path(__file__).resolve().parents[2]
source=(root/'src/simulation/microbes.zig').read_text()
old='pub fn step(cell:*Cell,env:Environment,elapsed:f32) Flux {'
new='pub fn step(cell:*Cell,env:Environment,elapsed:f32) Flux {return stepWithActivity(cell,env,elapsed,.{1,1,1,1});}\npub fn stepWithActivity(cell:*Cell,env:Environment,elapsed:f32,activity:[4]f32) Flux {'
assert source.count(old)==1
source=source.replace(old,new)
old='potentials[i]=frondMass(c)*(@exp(@min(20,rate*days))-1)*space;'
assert source.count(old)==1
source=source.replace(old,old+'\n        potentials[i]*=activity[i]; // Experimental paid metabolic pace, not free efficiency.')
header='//! GENERATED EXPERIMENT ONLY; no production imports this file.\n//! source microbes SHA256 '+hashlib.sha256((root/'src/simulation/microbes.zig').read_bytes()).hexdigest()+'\n'
(root/'src/experimental/energy_community_core.zig').write_text(header+source)
