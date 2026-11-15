from pathlib import Path
import sys,hashlib,json,gzip
r=Path(__file__).resolve().parents[2];out=Path(sys.argv[1]).resolve();out.mkdir(parents=True,exist_ok=True)
baseline=gzip.decompress((r/'web/tests/continuation-review/root-mutation/baseline.zig.gz').read_bytes()).decode()
(out/'baseline.zig').write_text(baseline)
s=baseline.replace('pub const nutrient_per_carbon','pub const RootMutation=@import("root_mutation.zig");\npub const nutrient_per_carbon',1)
s=s.replace('mutate,0.01,0.03,0.04);','mutate,0.01,0.03,0.04,.{});',1).replace('true,0.004,0.02,0.01);','true,0.004,0.02,0.01,.{});',1)
s=s.replace('fn reproduceSized(','''pub fn reproduceWithRoot(d:*Cell,w:usize,t:*Cell,stats:*Stats,mutate:bool,config:RootMutation.Config)bool{return reproduceSized(d,w,t,stats,mutate,0.01,0.03,0.04,config);}
pub fn propagateWithRoot(d:*Cell,w:usize,t:*Cell,stats:*Stats,config:RootMutation.Config)bool{return reproduceSized(d,w,t,stats,true,0.004,0.02,0.01,config);}
fn reproduceSized(''',1)
s=s.replace('credit:f32) bool {','credit:f32,config:RootMutation.Config) bool {\n    if(!config.valid())return false;',1)
s=s.replace('    if(parent.biomass<min_parent','    if(!std.math.isFinite(parent.root_fraction) or parent.root_fraction<0 or parent.root_fraction>1)return false;\n    if(parent.biomass<min_parent',1)
s=s.replace('        applyRareMutation(&child,parent.*,organization_draw);','        applyRareMutation(&child,parent.*,organization_draw);\n        if(config.enabled)child.root_fraction=RootMutation.allocation(parent.root_fraction,config.stream_seed,child.parent,child.lineage,child.generation);',1)
(out/'microbes.zig').write_text(s)
for n in ['root_mutation.zig','qa_root_mutation.zig']:(out/n).write_text((r/'web/tests'/n).read_text())
(out/'source-hashes.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in out.glob('*.zig')},indent=2))
