//! Isolated explicit Sandbox god actions. No Origin seeding or resource-conservation claim.
const std=@import("std");const E=@import("simulation/ecology.zig");
pub const Status=enum{enabled,already_enabled,eligible,planted,disabled,wrong_mode,invalid,occupied,water};
pub const Receipt=struct{status:Status,cover_added:f32=0,toughness:f32=0,depth_m:f64=0};
pub fn validConfig(c:E.DefenseConfig)bool{return if(c.enabled) c.law==1 and c.mutation_law==2 else c.law==0 and c.mutation_law==0 and c.stream_seed==0;}
pub fn enableDefenses(p:anytype)Receipt{
 if(p.worldMode!=.sandbox)return .{.status=.wrong_mode};
 if(!validConfig(p.sandboxDefense))return .{.status=.invalid};
 if(p.sandboxDefense.enabled)return .{.status=.already_enabled};
 for(p.plantTraits)|t|if(t.toughness!=0)return .{.status=.invalid};
 p.sandboxDefense=.{.enabled=true,.law=1,.mutation_law=2,.stream_seed=p.seed};
 return .{.status=.enabled};
}
pub fn previewPlantDefended(p:anytype,index:usize,d:f32)Receipt{
 if(p.worldMode!=.sandbox)return .{.status=.wrong_mode};
 if(!validConfig(p.sandboxDefense))return .{.status=.invalid};
 if(!p.sandboxDefense.enabled)return .{.status=.disabled};
 if(index>=p.vegetation.len or p.plantTraits.len!=p.vegetation.len or p.waterMass.len!=p.vegetation.len or p.temperature.len!=p.vegetation.len or (d!=0 and d!=0.5))return .{.status=.invalid};
 const old=p.vegetation[index];const water=p.waterMass[index];
 if(!std.math.isFinite(old) or old<0 or old>1 or !std.math.isFinite(water) or water<0 or !std.math.isFinite(p.temperature[index]))return .{.status=.invalid};
 if(old>0)return .{.status=.occupied};
 const conversion=p.getKmPerWaterMass();
 const depth=water*conversion;
 if(!std.math.isFinite(conversion) or conversion<=0 or !std.math.isFinite(depth))return .{.status=.invalid};
 if(depth>0.0005)return .{.status=.water,.depth_m=@as(f64,depth)*1000};
 return .{.status=.eligible,.toughness=d,.depth_m=@as(f64,depth)*1000};
}
pub fn plantDefended(p:anytype,index:usize,d:f32)Receipt{
 const preview=previewPlantDefended(p,index,d);if(preview.status!=.eligible)return preview;
 const old=p.vegetation[index];
 // Explicit external founder input, not conversion of an existing living plant.
 p.vegetation[index]=0.35;p.plantTraits[index]=.{.toughness=d};
 return .{.status=.planted,.cover_added=p.vegetation[index]-old,.toughness=d,.depth_m=preview.depth_m};
}
