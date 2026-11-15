#!/usr/bin/env python3
"""Apply only the tested readonly Cell borrowing to an isolated beta tree."""
from pathlib import Path
import sys
def patch(d):
 p=d/'simulation/shared_soil.zig';s=p.read_text();needle='pub fn step(cell:M.Cell,soil:f64,vapor:f64,area:f64,env:M.Environment,dt:f32,conductance:u8,bare:f64)?Result{';assert s.count(needle)==1
 s=s.replace(needle,needle+'return stepBorrowed(&cell,soil,vapor,area,env,dt,conductance,bare);}\npub fn stepBorrowed(cell:*const M.Cell,soil:f64,vapor:f64,area:f64,env:M.Environment,dt:f32,conductance:u8,bare:f64)?Result{');p.write_text(s)
 p=d/'simulation/capillary_bucket.zig';s=p.read_text();needle='pub fn step(initial: State, p: Params) ?Result {';assert s.count(needle)==1;s=s.replace(needle,needle+'return stepBorrowed(initial,p,null);}\n// Optional borrow is valid only for this synchronous readonly call. Value API retained.\npub fn stepBorrowed(initial: State, p: Params, borrowed:?*const @import("microbes.zig").Cell) ?Result {')
 needle='const shared=@import("shared_soil.zig").step(p.cell orelse return null,';assert s.count(needle)==1;s=s.replace(needle,'const cell=borrowed orelse if(p.cell)|*value| value else return null;\n        const shared=@import("shared_soil.zig").stepBorrowed(cell,');p.write_text(s)
 p=d/'simulation/planet.zig';s=p.read_text();needle='@import("capillary_bucket.zig").step(';assert s.count(needle)==1;s=s.replace(needle,'@import("capillary_bucket.zig").stepBorrowed(');needle='.cell=self.microbeCells[i],.environment=env,.conductance=10}) orelse continue;';assert s.count(needle)==1;s=s.replace(needle,'.environment=env,.conductance=10},&self.microbeCells[i]) orelse continue;');p.write_text(s)

if __name__=="__main__":
 d=Path(sys.argv[1]).resolve();r=Path(__file__).resolve().parents[2]
 assert d!=(r/"src").resolve(),"never patch production"
 assert "landBeta" in (d/"simulation/planet.zig").read_text(),"beta copy required"
 patch(d)
