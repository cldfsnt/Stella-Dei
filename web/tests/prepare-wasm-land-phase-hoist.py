from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];o=r.parent/'site-tmp/wasm-land-phase-hoist';o.mkdir(exist_ok=True);frozen=r.parent/'site-tmp/wasm-land-screen/candidate/src'
def patch(d):
 p=d/'simulation/capillary_bucket.zig';s=p.read_text();needle='pub fn step(initial: State, p: Params) ?Result {';assert s.count(needle)==1
 s=s.replace(needle,'''pub fn step(initial: State, p: Params) ?Result { return stepPrepared(initial,p,A.PhaseStep.init(p.dt)); }
// Caller caches the identical timestep coefficients; standalone API preserved.
pub fn stepPrepared(initial: State, p: Params, c:A.PhaseStep) ?Result {''')
 needle='    const c = A.PhaseStep.init(p.dt);';assert s.count(needle)==1;s=s.replace(needle,'''    if(c.dt!=p.dt or !valid(c.evaporation) or c.evaporation>1 or !valid(c.condensation) or c.condensation>1 or !valid(c.rain_memory) or c.rain_memory>1)return null;''');p.write_text(s)
 p=d/'simulation/planet.zig';s=p.read_text();needle='        @memset(self.landRootH,.{0,0,0,0});\n        for(self.waterMass,self.landVapor,0..)|liquid,vapor,i|{';assert s.count(needle)==1;s=s.replace(needle,'        const land_phase=AtmosphereWater.PhaseStep.init(dt);\n'+needle)
 needle='@import("capillary_bucket.zig").step(';assert s.count(needle)==1;s=s.replace(needle,'@import("capillary_bucket.zig").stepPrepared(');needle='.conductance=10}) orelse continue;';assert s.count(needle)==1;s=s.replace(needle,'.conductance=10},land_phase) orelse continue;');p.write_text(s)
for arm in ['baseline','candidate']:
 d=o/arm/'src';shutil.copytree(frozen,d,dirs_exist_ok=True)
 if arm=='candidate':patch(d)
 (o/arm/'source-hashes.json').write_text(json.dumps({str(p.relative_to(d)):hashlib.sha256(p.read_bytes()).hexdigest()for p in d.rglob('*.zig')},indent=2))
d=o/'native/src';shutil.copytree(r.parent/'site-tmp/origin-root-drain/src',d,dirs_exist_ok=True);patch(d)
p=d/'main.zig';p.write_text(p.read_text().replace(str(r.parent/'site-tmp/origin-root-drain'),str(o/'native')))
shutil.copyfile(r.parent/'site-tmp/wasm-land-screen/graph.json',o/'graph.json')
