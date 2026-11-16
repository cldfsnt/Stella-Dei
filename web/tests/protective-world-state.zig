//! QA-only single assigned lineage, separate hash-bound checkpoint. NOT production save state.
const std=@import("std");
pub const State=struct{enabled:bool=false,subject:u64=0,point:usize=0,inactive:bool=false,recovery:f32=0,wake:bool=false,paid:f64=0,entries:u32=0,wakes:u32=0};pub var current:State=.{};
pub fn sleeping(id:u64)bool{return current.enabled and current.inactive and id!=0 and id==current.subject;}
pub fn before(cell:anytype,env:anytype,dt:f32)f32{
 if(!current.enabled)return 0;
 for(&cell.cohorts)|*c|{if(c.lineage!=current.subject or c.biomass<=0)continue;
  current.wake=false;
  if(current.inactive){if(env.temperature>=283 and env.temperature<=318 and env.depth_km>0)current.recovery+=dt else current.recovery=0;current.wake=current.recovery>=7200;return 0;}
  if(env.temperature>=278 and env.temperature<=323 and env.depth_km>0)return 0;
  const remaining=c.biomass*0.98;const debit=c.biomass-remaining;
  if(debit<=0 or debit>env.oxygen_carbon_capacity or remaining<0.0025)return 0;
  c.support_mass*=remaining/c.biomass;c.biomass=remaining;cell.nutrient+=debit*@as(f32,0.1);current.inactive=true;current.recovery=0;current.paid+=debit;current.entries+=1;return debit;
 }
 current.inactive=false;current.recovery=0;current.wake=false;return 0;
}
pub fn after(cell:anytype)void{if(!current.enabled)return;for(cell.cohorts)|c|{if(c.lineage==current.subject and c.biomass>0){if(current.wake){current.inactive=false;current.recovery=0;current.wake=false;current.wakes+=1;}return;}}current.inactive=false;current.recovery=0;current.wake=false;}
const Checkpoint=struct{world_sha:[32]u8,state:State};
pub fn save(a:std.mem.Allocator,path:[]const u8,world:[]const u8)!void{var hash:[32]u8=undefined;std.crypto.hash.sha2.Sha256.hash(world,&hash,.{});const bytes=try std.json.stringifyAlloc(a,Checkpoint{.world_sha=hash,.state=current},.{});try std.fs.cwd().writeFile(.{.sub_path=try std.fmt.allocPrint(a,"{s}.activity.json",.{path}),.data=bytes});}
pub fn load(a:std.mem.Allocator,path:[]const u8,world:[]const u8)!void{var hash:[32]u8=undefined;std.crypto.hash.sha2.Sha256.hash(world,&hash,.{});const bytes=try std.fs.cwd().readFileAlloc(a,try std.fmt.allocPrint(a,"{s}.activity.json",.{path}),10000);const value=try std.json.parseFromSlice(Checkpoint,a,bytes,.{});if(!std.mem.eql(u8,&hash,&value.value.world_sha))return error.WorldMismatch;const st=value.value.state;if(!std.math.isFinite(st.recovery) or st.recovery<0 or st.recovery>7200 or !std.math.isFinite(st.paid) or st.paid<0)return error.InvalidState;current=st;}
test "lineage isolation death and replacement clear state" {const C=struct{lineage:u64=0,biomass:f32=0,support_mass:f32=0};const Cell=struct{cohorts:[1]C,nutrient:f32=0};var cell=Cell{.cohorts=.{.{.lineage=1,.biomass=0.02,.support_mass=0.005}}};current=.{.enabled=true,.subject=1};const e=.{.temperature=@as(f32,263),.depth_km=@as(f32,0.001),.oxygen_carbon_capacity=@as(f32,1)};try std.testing.expect(before(&cell,e,1440)>0);try std.testing.expect(sleeping(1) and !sleeping(2));cell.cohorts[0].lineage=2;after(&cell);try std.testing.expect(!sleeping(1) and !sleeping(2));current.inactive=true;cell.cohorts[0]=.{};after(&cell);try std.testing.expect(!current.inactive);current=.{};}
