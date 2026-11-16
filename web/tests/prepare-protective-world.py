from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];t=r.parent/'site-tmp';base=t/'rooted-natural/src';out=t/'protective-world';e=r/'web/tests/continuation-review/protective-world';e.mkdir(parents=True,exist_ok=True)
for name in ['off','on']:
 o=out/name/'src';assert not o.exists();shutil.copytree(base,o)
 for p in o.rglob('*.zig'):
  s=p.read_text().replace(str(t/'rooted-natural'),str(out/name));p.write_text(s)
 shutil.copy2(r/'web/tests/protective-world-state.zig',o/'simulation/inactivity.zig')
 p=o/'simulation/microbes.zig';s=p.read_text()
 def rep(a,b):
  global s
  assert s.count(a)==1,(a,s.count(a));s=s.replace(a,b)
 rep('const std = @import("std");','const std = @import("std");const D=@import("inactivity.zig");')
 rep('return c.support_mass*0.12*','return (if(D.sleeping(c.lineage)) @as(f32,0.1) else 1)*c.support_mass*0.12*')
 rep('pub fn rootDemand(c:Cohort,env:Environment,dt:f32)f64 {','pub fn rootDemand(c:Cohort,env:Environment,dt:f32)f64 {if(D.sleeping(c.lineage))return 0;')
 rep('const wanted_dead=c.biomass*(1-@exp(-(effective_mortality+3*exposed*(1-hydrated))*days));','const ordinary_hazard=effective_mortality+3*exposed*(1-hydrated);const hazard=if(D.sleeping(c.lineage) and env.temperature>=253 and env.temperature<=333) @max(@as(f32,0.08),ordinary_hazard*0.1) else ordinary_hazard;const wanted_dead=c.biomass*(1-@exp(-hazard*days));')
 rep('if(c.biomass<=0 or effective_habitat<=0)continue;','if(D.sleeping(c.lineage) or c.biomass<=0 or effective_habitat<=0)continue;')
 rep('if(pred.biomass<=0 or pred.feeding<=0)continue;','if(D.sleeping(pred.lineage) or pred.biomass<=0 or pred.feeding<=0)continue;')
 rep('if(parent.biomass<min_parent or parent.reproduction_credit<credit)return false;','if(D.sleeping(parent.lineage) or parent.biomass<min_parent or parent.reproduction_credit<credit)return false;')
 rep('if (parent.biomass <= 0) return .{ .reason = .no_living_cohort };','if (parent.biomass <= 0 or D.sleeping(parent.lineage)) return .{ .reason = .no_living_cohort };')
 p.write_text(s)
 p=o/'simulation/shared_soil.zig';s=p.read_text();assert s.count('if(!root_eligible or c.biomass<=0')==1;s=s.replace('if(!root_eligible or c.biomass<=0','if(@import("inactivity.zig").sleeping(c.lineage) or !root_eligible or c.biomass<=0');p.write_text(s)
 p=o/'simulation/planet.zig';s=p.read_text();needle='            const column=@import("capillary_bucket.zig").stepBorrowed';assert s.count(needle)==1;s=s.replace(needle,'''            const D=@import("inactivity.zig");if(D.current.enabled and i==D.current.point){const paid=D.before(&self.microbeCells[i],env,dt);if(paid>0)self.applyMicrobeFlux(.{.recycled=paid});}
'''+needle)
 needle='        @import("../plant_receipt.zig").begin(self,';assert s.count(needle)==1;s=s.replace(needle,'''        const D=@import("inactivity.zig");defer if(D.current.enabled and D.current.point<self.microbeCells.len)D.after(&self.microbeCells[D.current.point]);
'''+needle);p.write_text(s)
 p=o/'main.zig';s=p.read_text();needle='    const start:usize=if(resumed)30 else 0;';assert s.count(needle)==1;s=s.replace(needle,'''    const D=@import("simulation/inactivity.zig");if(resumed){try D.load(a,input,bytes);}else{D.current=.{.enabled='''+('true' if name=='on' else 'false')+''',.subject=Audit.subject,.point=point};}
'''+needle)
 needle='      Audit.emit("PATCH",';s=s.replace(needle,'      Audit.emit("ACTIVITY",D.current);\n'+needle)
 needle='      if(timer.read()>900*std.time.ns_per_s)';s=s.replace(needle,'''      if(tick+1==30 or tick+1==end){const path=try std.fmt.allocPrint(a,"'''+str(out/name)+'''/{s}arm-{}-{}{s}.json",.{if(resumed)"resume-"else "",arm,tick+1,suffix});const wb=try std.fs.cwd().readFileAlloc(a,path,128*1024*1024);try D.save(a,path,wb);}
'''+needle);p.write_text(s)
(e/'source-hashes.json').write_text(json.dumps({name:{str(p.relative_to(out/name/'src')):hashlib.sha256(p.read_bytes()).hexdigest() for p in (out/name/'src').rglob('*.zig')} for name in ['off','on']},indent=2))
