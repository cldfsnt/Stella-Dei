from pathlib import Path
import shutil,sys,hashlib,json
src=Path(sys.argv[1]);dst=Path(sys.argv[2]);assert not dst.exists();shutil.copytree(src,dst)
def edit(name,fn):
 p=dst/name;s=p.read_text();p.write_text(fn(s))
shutil.copyfile(src/'simulation/microbes.zig',dst/'simulation/microbes_law3_reference.zig')
edit('simulation/land_beta.zig',lambda s:s.replace('c.physiology_law==3)', 'c.physiology_law==3 or c.physiology_law==4)'))
edit('simulation/microbes.zig',lambda s:s.replace('final_demand_physiology:bool=false,','final_demand_physiology:bool=false,composed_growth_physiology:bool=false,').replace('        const effective_habitat=@max(immersed,effectiveHydration(if(env.final_demand_physiology)fundedHydration(c,env,elapsed,i,interval_demand[i])else env.root_hydration[i],env.depth_km,env.temperature));','''        const funded=effectiveHydration(if(env.final_demand_physiology)fundedHydration(c,env,elapsed,i,interval_demand[i])else env.root_hydration[i],env.depth_km,env.temperature);
        const effective_habitat=if(env.composed_growth_physiology) composedGrowthHabitat(habitat,if(env.immersion_physiology)geometricImmersion(c,env.depth_km,env.temperature)else 0,funded) else @max(immersed,funded);''')+'\n/// Law4: funded is the fraction of exposed demand, not whole-body hydration.\npub fn composedGrowthHabitat(film:f32,immersion:f32,funded:f32)f32{return @max(film,immersion+(1-immersion)*funded);}\n')
edit('simulation/planet.zig',lambda s:s.replace('self.landBeta.physiology_law==3','self.landBeta.physiology_law>=3').replace('env.final_demand_physiology=true;','env.final_demand_physiology=true;env.composed_growth_physiology=self.landBeta.physiology_law==4;'))
edit('save_schema.zig',lambda s:s.replace('origin_land_beta_v3}', 'origin_land_beta_v3,origin_land_beta_v4}').replace('self.version > VERSION)', '(self.version > VERSION and self.version!=12))').replace('}else return error.InvalidValue;\n            if(self.mode', '}else if(beta.config.physiology_law==4){if(self.version!=12 or beta.format!=.origin_land_beta_v4)return error.IncompatibleSave;}else return error.InvalidValue;\n            if(self.mode',1).replace('        switch (self.mode) {','        if(self.version==12 and self.beta_origin==null)return error.IncompatibleSave;\n        switch (self.mode) {',1))
edit('save_game.zig',lambda s:s.replace('if(p.landBeta.physiology_law==3).origin_land_beta_v3','if(p.landBeta.physiology_law==4).origin_land_beta_v4 else if(p.landBeta.physiology_law==3).origin_land_beta_v3').replace('if(p.landBeta.physiology_law==3) @as(u32,10)','if(p.landBeta.physiology_law==4) @as(u32,12) else if(p.landBeta.physiology_law==3) @as(u32,10)'))
shutil.copyfile(Path(__file__).with_name('origin-growth-normalization-tests.zig'),dst/'simulation/qa_growth_normalization.zig')
print(dst)

p=dst/"save_schema.zig";p.write_text(p.read_text()+"\n"+Path(__file__).with_name("origin-growth-normalization-save-tests.zig").read_text())
