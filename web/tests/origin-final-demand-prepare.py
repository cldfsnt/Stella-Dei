from pathlib import Path
import shutil,sys
here=Path(__file__).parent;src=Path(sys.argv[1]);dst=Path(sys.argv[2]);assert not dst.exists();shutil.copytree(src,dst)
shutil.copyfile(here/'origin-final-demand-helper.zig',dst/'simulation/final_demand.zig')
p=dst/'simulation/land_beta.zig';s=p.read_text().replace('c.enabled and c.physiology_law==2','c.enabled and (c.physiology_law==2 or c.physiology_law==3)');p.write_text(s)
p=dst/'simulation/microbes.zig';s=p.read_text().replace('immersion_physiology:bool=false,','immersion_physiology:bool=false,final_demand_physiology:bool=false,root_credit:[4]f64=.{0,0,0,0},root_owner:[4]u64=.{0,0,0,0},')
pos=s.index('pub fn seed(cell:');s=s[:pos]+'''/// Full-interval demand for current tissue and final environmental snapshot.
pub fn rootDemand(c:Cohort,env:Environment,dt:f32)f64 {
    if(!std.math.isFinite(dt) or dt<=0 or !std.math.isFinite(env.temperature) or env.temperature<=273.15 or env.temperature>=355 or !std.math.isFinite(env.depth_km) or env.depth_km<0 or env.depth_km>=0.0002 or !std.math.isFinite(env.light) or env.light<0 or env.light>2)return 0;
    if(!std.math.isFinite(c.biomass) or c.biomass<=0 or !std.math.isFinite(c.support_mass) or c.support_mass<=0 or c.support_mass>c.biomass or !std.math.isFinite(c.root_fraction) or c.root_fraction<=0 or c.root_fraction>1)return 0;
    const immersion=@import("basal_geometry.zig").immersion(c.biomass,producerHeightMeters(c),@as(f64,env.depth_km)*1000,100) orelse return 0;
    const d=0.1*@as(f64,frondMass(c))*@as(f64,dt)/86400*(0.5+0.5*@as(f64,env.light))*(1-immersion);
    return if(std.math.isFinite(d) and d>0)d else 0;
}
pub fn fundedHydration(c:Cohort,env:Environment,dt:f32,slot:usize,entry_demand:f64)f32{
    const current=rootDemand(c,env,dt);
    if(current<=0)return 0;
    return @import("final_demand.zig").signal(env.root_credit[slot],env.root_owner[slot],c.lineage,@max(entry_demand,current));
}
'''+s[pos:]
s=s.replace('    const days=elapsed/86400;','    var interval_demand=[_]f64{0,0,0,0};if(env.final_demand_physiology)for(cell.cohorts,0..)|c,i|{interval_demand[i]=rootDemand(c,env,elapsed);};\n    const days=elapsed/86400;',1)
s=s.replace('effectiveHydration(env.root_hydration[i],env.depth_km,env.temperature)','effectiveHydration(if(env.final_demand_physiology)fundedHydration(c.*,env,elapsed,i,interval_demand[i])else env.root_hydration[i],env.depth_km,env.temperature)',1)
# Growth c is by value, not pointer.
s=s.replace('effectiveHydration(env.root_hydration[i],env.depth_km,env.temperature)','effectiveHydration(if(env.final_demand_physiology)fundedHydration(c,env,elapsed,i,interval_demand[i])else env.root_hydration[i],env.depth_km,env.temperature)',1);p.write_text(s)
p=dst/'simulation/planet.zig';s=p.read_text().replace('landRootH:[][4]f32=&.{},','landRootH:[][4]f64=&.{},\n    landRootOwner:[][4]u64=&.{},')
s=s.replace('self.landRootH.len==n)return','self.landRootH.len==n and self.landRootOwner.len==n)return').replace('const h=try a.alloc([4]f32,n);','const h=try a.alloc([4]f64,n);const owners=try a.alloc([4]u64,n);').replace('@memset(h,.{0,0,0,0});','@memset(h,.{0,0,0,0});@memset(owners,.{0,0,0,0});').replace('self.landRootH=h;','self.landRootH=h;self.landRootOwner=owners;')
s=s.replace('@memset(self.landRootH,.{0,0,0,0});','{@memset(self.landRootH,.{0,0,0,0});@memset(self.landRootOwner,.{0,0,0,0});}')
s=s.replace('self.landRootH[i]=column.root_h;','for(0..4)|slot|{self.landRootH[i][slot]=if(self.landBeta.physiology_law==3)column.root_credits[slot]else column.root_h[slot];self.landRootOwner[i][slot]=if(self.landBeta.physiology_law==3)self.microbeCells[i].cohorts[slot].lineage else 0;}')
s=s.replace('self.landBeta.physiology_law==2','self.landBeta.physiology_law>=2')
s=s.replace('env.root_hydration=self.landRootH[i];','if(self.landBeta.physiology_law==3){env.final_demand_physiology=true;env.root_credit=self.landRootH[i];env.root_owner=self.landRootOwner[i];}else for(0..4)|slot|{env.root_hydration[slot]=@floatCast(self.landRootH[i][slot]);}')
s=s.replace('            const flux = Microbes.step(cell, env, dt);','            const flux = Microbes.step(cell, env, dt);\n            if(self.landBeta.enabled and self.landBeta.physiology_law==3){self.landRootH[i]=.{0,0,0,0};self.landRootOwner[i]=.{0,0,0,0};}')
p.write_text(s)
p=dst/'save_schema.zig';s=p.read_text().replace('VERSION: u32 = 9','VERSION: u32 = 10').replace('origin_land_beta_v1,origin_land_beta_v2}','origin_land_beta_v1,origin_land_beta_v2,origin_land_beta_v3}')
s=s.replace('}else return error.InvalidValue;\n            if(self.mode', '}else if(beta.config.physiology_law==3){if(self.version!=10 or beta.format!=.origin_land_beta_v3)return error.IncompatibleSave;}else return error.InvalidValue;\n            if(self.mode',1)
# Prior unknown law test uses3, now valid identity: make unknown99.
s=s.replace('bad.beta_origin.?.config.physiology_law=3;','bad.beta_origin.?.config.physiology_law=99;')
s+='\n'+(here/'origin-final-demand-save-tests.zig').read_text();p.write_text(s)
p=dst/'save_game.zig';s=p.read_text().replace('if(p.landBeta.physiology_law==2).origin_land_beta_v2 else .origin_land_beta_v1','if(p.landBeta.physiology_law==3).origin_land_beta_v3 else if(p.landBeta.physiology_law==2).origin_land_beta_v2 else .origin_land_beta_v1').replace('if(p.landBeta.physiology_law==2) @as(u32,9) else @as(u32,8)','if(p.landBeta.physiology_law==3) @as(u32,10) else if(p.landBeta.physiology_law==2) @as(u32,9) else @as(u32,8)').replace('@memset(p.landRootH,.{0,0,0,0});','@memset(p.landRootH,.{0,0,0,0});@memset(p.landRootOwner,.{0,0,0,0});');p.write_text(s)
shutil.copyfile(here/'origin-final-demand-tests.zig',dst/'simulation/qa_final_demand.zig')
shutil.copyfile(src/'simulation/microbes.zig',dst/'simulation/microbes_law2_reference.zig')
print(dst)
