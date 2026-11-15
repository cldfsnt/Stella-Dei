#!/usr/bin/env python3
"""Separate experimental physiology law; never edit source tree or production."""
from pathlib import Path
import shutil,sys
src=Path(sys.argv[1]);dst=Path(sys.argv[2]);assert not dst.exists()
shutil.copytree(src,dst)
p=dst/'simulation/land_beta.zig';s=p.read_text().replace('law:u8=0,','law:u8=0,physiology_law:u8=1,',1).replace('return if(!c.enabled)', 'return (c.physiology_law==1 or (c.enabled and c.physiology_law==2)) and (if(!c.enabled)').replace('c.root_mutation.enabled;','c.root_mutation.enabled);')
s=s.replace('pub fn valid', '''pub fn jsonStringify(c:@This(),w:anytype)!void{try w.beginObject();try w.objectField("enabled");try w.write(c.enabled);try w.objectField("law");try w.write(c.law);if(c.physiology_law!=1){try w.objectField("physiology_law");try w.write(c.physiology_law);}try w.objectField("root_mutation");try w.write(c.root_mutation);try w.endObject();}pub fn valid''');p.write_text(s)
p=dst/'simulation/microbes.zig';s=p.read_text().replace('root_hydration:[4]f32=', 'immersion_physiology:bool=false,root_hydration:[4]f32=',1)
s=s.replace('pub fn seed(cell:', '''/// Beta law2 only. Zero-height geometry is unresolved: retain law1, no epsilon.
pub fn geometricImmersion(c:Cohort,depth:f32,temp:f32) f32 {
    if(!std.math.isFinite(depth) or depth<=0 or depth>0.05 or !std.math.isFinite(temp) or temp<=273.15 or temp>=355)return 0;
    const height=producerHeightMeters(c);
    if(!std.math.isFinite(height) or height<=0)return 0;
    return std.math.clamp(depth*1000/height,0,1);
}
pub fn seed(cell:''',1)
s=s.replace('const effective_mortality=if(hydrated>0) mortality*(1-hydrated)+wet_mortality*hydrated else mortality;', '''const immersion=if(env.immersion_physiology)geometricImmersion(c.*,env.depth_km,env.temperature)else 0;
         const base_mortality=if(immersion>0) mortality*(1-immersion)+wet_mortality*immersion else mortality;
         const effective_mortality=if(hydrated>0) base_mortality*(1-hydrated)+wet_mortality*hydrated else base_mortality;''')
s=s.replace('const effective_habitat=@max(photosyntheticHabitat(c,env.depth_km,env.temperature),effectiveHydration(env.root_hydration[i],env.depth_km,env.temperature));','''const habitat=photosyntheticHabitat(c,env.depth_km,env.temperature);
        const immersed=if(env.immersion_physiology)@max(habitat,geometricImmersion(c,env.depth_km,env.temperature))else habitat;
        const effective_habitat=@max(immersed,effectiveHydration(env.root_hydration[i],env.depth_km,env.temperature));''')
p.write_text(s)
p=dst/'simulation/planet.zig';s=p.read_text().replace('if(self.landBeta.enabled)env.root_hydration=self.landRootH[i];','if(self.landBeta.enabled){env.root_hydration=self.landRootH[i];env.immersion_physiology=self.landBeta.physiology_law==2;}');p.write_text(s)
p=dst/'save_schema.zig';s=p.read_text().replace('VERSION: u32 = 8','VERSION: u32 = 9').replace('enum{origin_land_beta_v1}','enum{origin_land_beta_v1,origin_land_beta_v2}')
s=s.replace('if(self.version!=8)return error.IncompatibleSave;', '''if(beta.config.physiology_law==1){if(self.version!=8 or beta.format!=.origin_land_beta_v1)return error.IncompatibleSave;}else if(beta.config.physiology_law==2){if(self.version!=9 or beta.format!=.origin_land_beta_v2)return error.IncompatibleSave;}else return error.InvalidValue;''')
s+='\n'+Path(__file__).with_name('origin-immersion-save-tests.zig').read_text();p.write_text(s)
p=dst/'save_game.zig';s=p.read_text().replace('.format=.origin_land_beta_v1,.config=p.landBeta', '.format=if(p.landBeta.physiology_law==2).origin_land_beta_v2 else .origin_land_beta_v1,.config=p.landBeta').replace('if(beta!=null) schema.VERSION else 7','if(beta!=null) (if(p.landBeta.physiology_law==2) @as(u32,9) else @as(u32,8)) else 7');p.write_text(s)
shutil.copyfile(src/'simulation/microbes.zig',dst/'simulation/microbes_law1_reference.zig')
shutil.copyfile(Path(__file__).with_name('origin-immersion-tests.zig'),dst/'simulation/qa_immersion.zig')
print(dst)
