from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];o=r.parent/'site-tmp/wasm-land-borrowed';o.mkdir(exist_ok=True);frozen=r.parent/'site-tmp/wasm-land-screen/candidate/src'
def patch(d):
 p=d/'simulation/shared_soil.zig';s=p.read_text();needle='pub fn step(cell:M.Cell,soil:f64,vapor:f64,area:f64,env:M.Environment,dt:f32,conductance:u8,bare:f64)?Result{';assert s.count(needle)==1
 s=s.replace(needle,needle+'return stepBorrowed(&cell,soil,vapor,area,env,dt,conductance,bare);}\npub fn stepBorrowed(cell:*const M.Cell,soil:f64,vapor:f64,area:f64,env:M.Environment,dt:f32,conductance:u8,bare:f64)?Result{');p.write_text(s)
 p=d/'simulation/capillary_bucket.zig';s=p.read_text();needle='pub fn step(initial: State, p: Params) ?Result {';assert s.count(needle)==1;s=s.replace(needle,needle+'return stepBorrowed(initial,p,null);}\n// Optional borrow is valid only for this synchronous readonly call. Value API retained.\npub fn stepBorrowed(initial: State, p: Params, borrowed:?*const @import("microbes.zig").Cell) ?Result {')
 needle='const shared=@import("shared_soil.zig").step(p.cell orelse return null,';assert s.count(needle)==1;s=s.replace(needle,'const cell=borrowed orelse if(p.cell)|*value| value else return null;\n        const shared=@import("shared_soil.zig").stepBorrowed(cell,');p.write_text(s)
 p=d/'simulation/planet.zig';s=p.read_text();needle='@import("capillary_bucket.zig").step(';assert s.count(needle)==1;s=s.replace(needle,'@import("capillary_bucket.zig").stepBorrowed(');needle='.cell=self.microbeCells[i],.environment=env,.conductance=10}) orelse continue;';assert s.count(needle)==1;s=s.replace(needle,'.environment=env,.conductance=10},&self.microbeCells[i]) orelse continue;');p.write_text(s)
for arm in ['baseline','candidate']:
 d=o/arm/'src';shutil.copytree(frozen,d,dirs_exist_ok=True)
 if arm=='candidate':patch(d)
 (o/arm/'source-hashes.json').write_text(json.dumps({str(p.relative_to(d)):hashlib.sha256(p.read_bytes()).hexdigest()for p in d.rglob('*.zig')},indent=2))
d=o/'native/src';shutil.copytree(r.parent/'site-tmp/origin-root-drain/src',d,dirs_exist_ok=True);patch(d)
p=d/'main.zig';p.write_text(p.read_text().replace(str(r.parent/'site-tmp/origin-root-drain'),str(o/'native')))
shutil.copyfile(r.parent/'site-tmp/wasm-land-screen/graph.json',o/'graph.json')
# The same fixed corpus now compares value and borrowed paths, all Result fields.
s=(r.parent/'site-tmp/wasm-land-phase-hoist/qa.zig').read_text();s=s.replace('const h=C.stepPrepared(cs.value,cp.value,A.PhaseStep.init(p.dt));','var params=cp.value;const cell=params.cell;params.cell=null;const h=C.stepBorrowed(cs.value,params,if(cell)|*value|value else null);')
s=s[:s.index('test "invalid area')]+'''test "invalid area unchanged" {try check(.{.liquid=1,.soil=0.25,.vapor=1},.{.dt=1440,.area=0,.temperature=300,.saturation=2});}\n''';s=s.replace('prepared','borrowed').replace('HOIST_CORPUS','BORROWED_CORPUS');(o/'qa.zig').write_text(s)
