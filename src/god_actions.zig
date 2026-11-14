//! Explicit one-shot interventions. Caller owns tap handling, pause and visuals.
//! Heat is a gameplay impulse, not a physical lightning simulation.
const std=@import("std");
pub const Kind=enum{wave,lightning};
pub const Failure=enum{none,stale,invalid,dry,precision};
pub const Delta=struct{cell:usize=0,water_mass:f32=0,temperature_k:f32=0};
pub const Receipt=struct{
 kind:Kind, failure:Failure=.none, count:usize=0,
 affected:[7]Delta=.{.{}}**7,
 moved_mass:f64=0, heat_joules:f64=0,
 pub fn success(self:Receipt) bool{return self.failure==.none and self.count>0;}
};
fn failed(kind:Kind,reason:Failure) Receipt{return .{.kind=kind,.failure=reason};}
/// Push at most 25% of donor water, capped at one metre equivalent, to adjacent
/// patches. Equal mesh patch masses are used by the existing planet hydrology.
/// No erosion, water creation, direct mortality or automatic repetition.
pub fn wave(planet:anytype,expected:usize,selected:usize) Receipt {
 if(expected!=selected)return failed(.wave,.stale);
 if(selected>=planet.waterMass.len)return failed(.wave,.invalid);
 const conversion=planet.getKmPerWaterMass();const donor=planet.waterMass[selected];
 if(!std.math.isFinite(conversion) or conversion<=0 or !std.math.isFinite(donor) or donor<0)return failed(.wave,.invalid);
 if(donor==0)return failed(.wave,.dry);
 var ids:[6]usize=undefined;var n:usize=0;
 neighbors:for(planet.getNeighbours(selected))|id| {
  if(id>=planet.waterMass.len)return failed(.wave,.invalid);
  if(id==selected)continue;
  for(ids[0..n])|old|{if(id==old)continue :neighbors;}
  if(n==ids.len)return failed(.wave,.invalid);
  if(!std.math.isFinite(planet.waterMass[id]) or planet.waterMass[id]<0)return failed(.wave,.invalid);
  ids[n]=id;n+=1;
 }
 if(n==0)return failed(.wave,.invalid);
 const amount=@min(donor*0.25,0.001/conversion);
 if(!std.math.isFinite(amount) or amount<=0)return failed(.wave,.invalid);
 const share=amount/@as(f32,@floatFromInt(n));
 var updated:[6]f32=undefined;var actual:f64=0;
 for(ids[0..n],0..)|id,i|{
  updated[i]=planet.waterMass[id]+share;
  if(!std.math.isFinite(updated[i]))return failed(.wave,.invalid);
  actual+=@as(f64,updated[i])-planet.waterMass[id];
 }
 // Refuse sub-resolution transfers rather than create or destroy donor water.
 if(actual<=0 or actual>donor)return failed(.wave,.precision);
 const new_donor=donor-@as(f32,@floatCast(actual));
 const removed=@as(f64,donor)-new_donor;
 if(@abs(removed-actual)>@max(1e-12,actual*1e-5))return failed(.wave,.precision);
 var out=Receipt{.kind=.wave,.count=n+1,.moved_mass=removed};
 out.affected[0]=.{.cell=selected,.water_mass=new_donor-donor};
 for(ids[0..n],0..)|id,i|out.affected[i+1]=.{.cell=id,.water_mass=updated[i]-planet.waterMass[id]};
 planet.waterMass[selected]=new_donor;
 for(ids[0..n],0..)|id,i|planet.waterMass[id]=updated[i];
 return out;
}
/// Caller supplies actual current patch heat capacity in J/K from the engine.
/// Adds up to 40 K, bounded below 500 K. Reports actual externally supplied heat.
/// Existing ecology subsequently reacts; the receipt does not invent casualties.
pub fn lightning(planet:anytype,expected:usize,selected:usize,heat_capacity:f64) Receipt {
 if(expected!=selected)return failed(.lightning,.stale);
 if(selected>=planet.temperature.len or !std.math.isFinite(heat_capacity) or heat_capacity<=0)return failed(.lightning,.invalid);
 const before=planet.temperature[selected];
 if(!std.math.isFinite(before) or before<0 or before>=500)return failed(.lightning,.invalid);
 const after=@min(@as(f32,500),before+40);
 const delta=after-before;const energy=heat_capacity*@as(f64,delta);
 if(!std.math.isFinite(energy) or energy<=0)return failed(.lightning,.invalid);
 var out=Receipt{.kind=.lightning,.count=1,.heat_joules=energy};
 out.affected[0]=.{.cell=selected,.temperature_k=delta};
 planet.temperature[selected]=after;
 return out;
}
test "wave conserves bounded real water and fails atomically" {
 const P=struct{waterMass:[8]f32=.{4,0,0,0,0,0,0,9},pub fn getKmPerWaterMass(_: *@This()) f32{return 0.001;}pub fn getNeighbours(_: *@This(),_:usize) []const usize{return &.{1,2,3,4,5,6};}};
 var p=P{};const initial=p.waterMass;
 try std.testing.expectEqual(Failure.stale,wave(&p,1,0).failure);try std.testing.expectEqualSlices(f32,&initial,&p.waterMass);
 const r=wave(&p,0,0);try std.testing.expect(r.success());try std.testing.expectEqual(@as(usize,7),r.count);
 var sum:f64=0;for(p.waterMass)|v|{try std.testing.expect(v>=0);sum+=v;}
 try std.testing.expectApproxEqAbs(@as(f64,13),sum,1e-6);try std.testing.expectEqual(@as(f32,9),p.waterMass[7]);
 try std.testing.expect(r.moved_mass<=1.000001);
 p.waterMass[3]=std.math.nan(f32);const before=p.waterMass[0];try std.testing.expectEqual(Failure.invalid,wave(&p,0,0).failure);try std.testing.expectEqual(before,p.waterMass[0]);
}
test "heat has finite accounted input and existing ecology reacts differently" {
 const Ecology=@import("simulation/ecology.zig");const M=@import("simulation/microbes.zig");
 var p=struct{temperature:[2]f32=.{295,295}}{};
 const r=lightning(&p,0,0,1000);try std.testing.expect(r.success());try std.testing.expectEqual(@as(f64,40000),r.heat_joules);try std.testing.expectEqual(@as(f32,295),p.temperature[1]);
 try std.testing.expect(Ecology.grow(0.5,p.temperature[0],295,0,1,true,86400)<Ecology.grow(0.5,295,295,0,1,true,86400));
 try std.testing.expect(M.thermalFitness(335,330)>M.thermalFitness(335,295));
 const before=p.temperature;try std.testing.expectEqual(Failure.stale,lightning(&p,1,0,1000).failure);try std.testing.expectEqual(Failure.invalid,lightning(&p,0,0,std.math.inf(f64)).failure);try std.testing.expectEqualSlices(f32,&before,&p.temperature);
}
test "deep map precision refusal leaves water unchanged" {
 const P=struct{waterMass:[2]f32=.{1e20,1e20},pub fn getKmPerWaterMass(_: *@This()) f32{return 0.001;}pub fn getNeighbours(_: *@This(),_:usize) []const usize{return &.{1};}};
 var p=P{};const before=p.waterMass;
 try std.testing.expectEqual(Failure.precision,wave(&p,0,0).failure);
 try std.testing.expectEqualSlices(f32,&before,&p.waterMass);
}

test "pentagon wave ignores self fillers and duplicate neighbours without changing budget" {
 const P=struct {
  waterMass:[7]f32=.{4,0,0,0,0,0,9},
  neighbours:[]const usize=&.{1,2,3,4,5,0},
  reconciled:[7]u8=.{0}**7,
  pub fn getKmPerWaterMass(_: *@This()) f32{return 0.001;}
  pub fn getNeighbours(self:*@This(),_:usize) []const usize{return self.neighbours;}
  pub fn reconcileWaterPrecision(self:*@This(),i:usize) void {self.reconciled[i]+=1;}
 };
 var pentagon=P{};var duplicate=P{.neighbours=&.{1,2,3,4,5,1,0,2}};
 const a=wave(&pentagon,0,0);const b=wave(&duplicate,0,0);
 try std.testing.expect(a.success() and b.success());
 try std.testing.expectEqual(@as(usize,6),a.count);
 try std.testing.expectEqualSlices(f32,&pentagon.waterMass,&duplicate.waterMass);
 try std.testing.expectEqual(@as(f32,3),pentagon.waterMass[0]);
 var total:f64=0;for(pentagon.waterMass)|m|total+=m;
 try std.testing.expectApproxEqAbs(@as(f64,13),total,1e-6);
 try std.testing.expectEqual(@as(u8,0),pentagon.reconciled[6]);
 var invalid=P{.neighbours=&.{1,0,1,99}};
 const before=invalid;
 try std.testing.expectEqual(Failure.invalid,wave(&invalid,0,0).failure);
 try std.testing.expectEqualSlices(f32,&before.waterMass,&invalid.waterMass);
 try std.testing.expectEqualSlices(u8,&before.reconciled,&invalid.reconciled);
 var self_only=P{.neighbours=&.{0,0,0}};
 try std.testing.expectEqual(Failure.invalid,wave(&self_only,0,0).failure);
 try std.testing.expectEqual(@as(f32,4),self_only.waterMass[0]);
}
