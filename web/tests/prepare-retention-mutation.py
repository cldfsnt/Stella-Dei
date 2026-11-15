from pathlib import Path
s=Path('src/experimental/hydration_continuous_core.zig').read_text()
s=s.replace('mutate,0.01,0.03,0.04);','mutate,0.01,0.03,0.04,null);')
s=s.replace('true,0.004,0.02,0.01);','true,0.004,0.02,0.01,null);')
# Match original reproductive constants exactly below rather than guessing.
s=s.replace('credit:f32) bool {','credit:f32,retention_seed:?u64) bool {',1)
needle='        applyRareMutation(&child,parent.*,organization_draw);';assert s.count(needle)==1
s=s.replace(needle,needle+'\n        if(retention_seed)|world_seed|child.retention_allocation=@import("retention_mutation.zig").allocation(parent.retention_allocation,world_seed,parent.lineage,child.lineage,child.generation);')
pos=s.index('fn reproduceSized(')
s=s[:pos]+'''pub fn reproduceWithRetention(donor:*Cell,which:usize,destination:*Cell,stats:*Stats,mutate:bool,world_seed:u64)bool{return reproduceSized(donor,which,destination,stats,mutate,0.01,0.03,0.04,world_seed);}
pub fn propagateWithRetention(donor:*Cell,which:usize,destination:*Cell,stats:*Stats,world_seed:u64)bool{return reproduceSized(donor,which,destination,stats,true,0.004,0.02,0.01,world_seed);}
'''+s[pos:]
Path('src/experimental/hydration_mutation_core.zig').write_text(s)
