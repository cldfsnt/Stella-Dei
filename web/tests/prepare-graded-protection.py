from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/graded-protection';o=b/'src';assert not o.exists();shutil.copytree(r.parent/'site-tmp/root-water-ui/src',o)
p=o/'simulation/microbes.zig';s=p.read_text();s=s.replace('pub const Cohort=struct {','pub var qa_protection_enabled:bool=false;\npub const Cohort=struct {\n    protective_investment:f32=0, protective_recovery:f32=0, protective_rest:bool=false,')
s+='''
// Experimental graded cold protection, not a production saved law.
pub fn protectiveFraction(c:Cohort)f32{return if(qa_protection_enabled and c.protective_rest)c.protective_investment else 0;}
pub fn activity(c:Cohort)f32{return 1-protectiveFraction(c);}
pub fn protectBefore(cell:*Cell,env:Environment,dt:f32)f32{
 if(!qa_protection_enabled)return 0;var paid:f32=0;
 for(&cell.cohorts)|*c|{
  if(c.biomass<=0 or c.protective_investment<=0)continue;
  if(c.protective_rest){
   if(env.temperature>=283 and env.temperature<=318){if(c.protective_recovery>=7200){c.protective_rest=false;c.protective_recovery=0;}else c.protective_recovery+=dt;}else c.protective_recovery=0;
   continue;
  }
  // Temperature-only prototype: dry but root-funded tissue is NOT a stress trigger.
  if(env.temperature>=278 and env.temperature<=323)continue;
  const after=c.biomass*(1-0.02*c.protective_investment);const debit=c.biomass-after;
  if(debit<=0 or debit>env.oxygen_carbon_capacity-paid or after<0.0025)continue;
  c.support_mass*=after/c.biomass;c.biomass=after;cell.nutrient+=debit*nutrient_per_carbon;paid+=debit;c.protective_rest=true;c.protective_recovery=0;
 }
 return paid;
}
'''
s=s.replace('return c.support_mass*0.12*','return (1-0.9*protectiveFraction(c))*c.support_mass*0.12*')
s=s.replace('return if(std.math.isFinite(d) and d>0)d else 0;', 'return if(std.math.isFinite(d) and d>0)d*@as(f64,activity(c)) else 0;')
s=s.replace('const wanted_dead=c.biomass*(1-@exp(-(effective_mortality+3*exposed*(1-hydrated))*days));','const ordinary_hazard=effective_mortality+3*exposed*(1-hydrated);const fraction=protectiveFraction(c.*);const hazard=if(fraction>0 and env.temperature>=253 and env.temperature<=333) @max(@as(f32,0.08),ordinary_hazard*(1-0.9*fraction)) else ordinary_hazard;const wanted_dead=c.biomass*(1-@exp(-hazard*days));')
s=s.replace('potentials[i]=frondMass(c)*(@exp(@min(20,rate*days))-1)*space;', 'potentials[i]=frondMass(c)*(@exp(@min(20,rate*days))-1)*space;\n        if(qa_protection_enabled and c.protective_investment>0)potentials[i]*=(1-0.1*c.protective_investment)*activity(c);')
s=s.replace('pred.biomass*3*pred.feeding*days','pred.biomass*3*pred.feeding*days*activity(pred)')
s=s.replace('if(parent.biomass<min_parent or', 'if(activity(parent.*)<=0 or parent.biomass<min_parent or')
s=s.replace('var child=parent.*;', 'var child=parent.*;child.protective_rest=false;child.protective_recovery=0;')
s=s.replace('if (parent.biomass <= 0) return', 'if (parent.biomass <= 0 or activity(parent)<=0) return')
p.write_text(s)
p=o/'simulation/shared_soil.zig';s=p.read_text().replace('out.demand[i]=0.1*','out.demand[i]=@as(f64,M.activity(c))*0.1*');p.write_text(s)
p=o/'simulation/planet.zig';s=p.read_text();needle='            const column=@import("capillary_bucket.zig").stepBorrowed';assert s.count(needle)==1;s=s.replace(needle,'            const protective_paid=Microbes.protectBefore(&self.microbeCells[i],env,dt);if(protective_paid>0)self.applyMicrobeFlux(.{.recycled=protective_paid});\n'+needle);s=s.replace('if(!std.math.isFinite(c.aerial_allocation) or', 'if(Microbes.activity(c)<=0 or !std.math.isFinite(c.aerial_allocation) or');p.write_text(s)
shutil.copy2(r.parent/'site-tmp/root-water-ui/src/simulation/microbes.zig',o/'simulation/legacy_microbes.zig')
shutil.copy2(r/'web/tests/graded-protection-tests.zig',o/'graded_tests.zig')
e=r/'web/tests/continuation-review/graded-protection';e.mkdir(parents=True,exist_ok=True);(e/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},indent=2)+'\n')
