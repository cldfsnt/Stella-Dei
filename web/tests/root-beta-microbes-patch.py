#!/usr/bin/env python3
"""Patch only a copied current production Microbes module; never Planet or production."""
from pathlib import Path
import sys,hashlib,json
r=Path(__file__).resolve().parents[2]
def change(s,a,b):
 assert s.count(a)==1,(a,s.count(a));return s.replace(a,b,1)
def patch(source):
 s=source
 s=change(s,'pub const Cohort=struct {','pub const Cohort=struct {\n    root_fraction:f32=0,')
 s=change(s,'oxygen_carbon_capacity:f32};','oxygen_carbon_capacity:f32,root_hydration:[4]f32=.{0,0,0,0}};')
 s=change(s,'pub fn frondMass','pub fn abovegroundSupport(c:Cohort)f32{return c.support_mass*(1-c.root_fraction);}\npub fn frondMass')
 s=s.replace('c.biomass<=0 or c.support_mass<=0 or frondMass(c)<=0','c.biomass<=0 or abovegroundSupport(c)<=0 or frondMass(c)<=0').replace('c.support_mass/@max(c.biomass,0.000001)','abovegroundSupport(c)/@max(c.biomass,0.000001)').replace('0.2*c.support_mass/(frondMass(c)+0.01)','0.2*abovegroundSupport(c)/(frondMass(c)+0.01)').replace('std.math.clamp(c.support_mass/c.biomass,0,1)','std.math.clamp(abovegroundSupport(c)/c.biomass,0,1)').replace('if(c.support_mass>0)organized=true','if(abovegroundSupport(c)>0)organized=true')
 s=change(s,'fn aquaticSubmergence','pub fn effectiveHydration(h:f32,depth:f32,temp:f32)f32 {\n if(!std.math.isFinite(h) or !std.math.isFinite(depth) or !std.math.isFinite(temp) or depth<0 or temp<=273.15 or temp>=355)return 0;\n return std.math.clamp(h,0,1)*(1-aquaticSubmergence(depth));\n}\nfn aquaticSubmergence')
 s=change(s,'    for(&cell.cohorts) |*c| {','    for(&cell.cohorts,0..) |*c,i| {')
 s=change(s,'        const wanted_dead=c.biomass*(1-@exp(-(mortality+3*exposed)*days));','''        const hydrated=effectiveHydration(env.root_hydration[i],env.depth_km,env.temperature);
         const wet_mortality=0.04+(1-fitness)*0.7+0.10*c.structure+0.10*c.feeding+0.05*c.mobility;
         const effective_mortality=if(hydrated>0) mortality*(1-hydrated)+wet_mortality*hydrated else mortality;
         const wanted_dead=c.biomass*(1-@exp(-(effective_mortality+3*exposed*(1-hydrated))*days));''')
 s=change(s,'        if(c.biomass<=0 or photosyntheticHabitat(c,env.depth_km,env.temperature)<=0)continue;','''        const effective_habitat=@max(photosyntheticHabitat(c,env.depth_km,env.temperature),effectiveHydration(env.root_hydration[i],env.depth_km,env.temperature));
         if(c.biomass<=0 or effective_habitat<=0)continue;''')
 s=s.replace('3*photosyntheticHabitat(c,env.depth_km,env.temperature)*fitness','3*effective_habitat*fitness')
 s=change(s,'    for(cell.cohorts) |c| {\n        if(!std.math.isFinite(c.biomass)','    for(cell.cohorts) |c| {\n        if(!std.math.isFinite(c.root_fraction) or c.root_fraction<0 or c.root_fraction>1)return false;\n        if(!std.math.isFinite(c.biomass)')
 s=s.replace('pub const nutrient_per_carbon','pub const RootMutation=@import("root_mutation.zig");\npub const nutrient_per_carbon',1)
 s=s.replace('mutate,0.01,0.03,0.04);','mutate,0.01,0.03,0.04,.{});',1).replace('true,0.004,0.02,0.01);','true,0.004,0.02,0.01,.{});',1)
 s=s.replace('fn reproduceSized(','''pub fn reproduceWithRoot(d:*Cell,w:usize,t:*Cell,stats:*Stats,mutate:bool,config:RootMutation.Config)bool{return reproduceSized(d,w,t,stats,mutate,0.01,0.03,0.04,config);}
 pub fn propagateWithRoot(d:*Cell,w:usize,t:*Cell,stats:*Stats,config:RootMutation.Config)bool{return reproduceSized(d,w,t,stats,true,0.004,0.02,0.01,config);}
 fn reproduceSized(''',1)
 s=s.replace('credit:f32) bool {','credit:f32,config:RootMutation.Config) bool {\n    if(!config.valid())return false;',1)
 s=s.replace('    if(parent.biomass<min_parent','    if(!std.math.isFinite(parent.root_fraction) or parent.root_fraction<0 or parent.root_fraction>1)return false;\n    if(parent.biomass<min_parent',1)
 s=s.replace('        applyRareMutation(&child,parent.*,organization_draw);','        applyRareMutation(&child,parent.*,organization_draw);\n        if(config.enabled)child.root_fraction=RootMutation.allocation(parent.root_fraction,config.stream_seed,child.parent,child.lineage,child.generation);',1)
 return s
if __name__=='__main__':
 p=Path(sys.argv[1]).resolve();source=p.read_text();assert 'root_fraction' not in source,'requires unpatched current production copy'
 p.write_text(patch(source));(p.parent/'root_mutation.zig').write_text((r/'web/tests/root_mutation.zig').read_text())
 print(json.dumps({'input_sha256':hashlib.sha256(source.encode()).hexdigest(),'output_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}))
