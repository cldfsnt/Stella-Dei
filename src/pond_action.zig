//! Explicit bounded terraforming and water input; no biological edits or auto-care.
const std = @import("std");
fn includes(ids:[]const usize, id:usize) bool { for(ids)|v|{if(v==id)return true;}return false; }
pub fn makePond(planet:anytype, expected:usize, selected:usize) i32 {
    return shapeBasin(planet,expected,selected,false);
}
pub fn makeNursery(planet:anytype, expected:usize, selected:usize) i32 {
    return shapeBasin(planet,expected,selected,true);
}
fn shapeBasin(planet:anytype, expected:usize, selected:usize, nursery:bool) i32 {
    if (planet.worldMode != .origin or expected != selected or selected >= planet.waterMass.len or planet.elevation.len != planet.waterMass.len) return -1;
    const conversion = planet.getKmPerWaterMass();
    if (!std.math.isFinite(conversion) or conversion <= 0) return -1;
    var ids: [19]usize = undefined;
    ids[0] = selected;var count:usize = 1;
    for (planet.getNeighbours(selected)) |idx| {
        if (idx >= planet.waterMass.len) return -1;
        if (includes(ids[0..count],idx)) continue;
        if(count==7)return -1;
        ids[count]=idx;count+=1;
    }
    const floor_count=count;
    for(ids[0..floor_count])|inner| for(planet.getNeighbours(inner))|idx| {
        if(idx>=planet.waterMass.len)return -1;
        if(includes(ids[0..count],idx))continue;
        if(count==ids.len)return -1;
        ids[count]=idx;count+=1;
    };
    if(count==floor_count)return -1;
    // Raise a dry rim above adjacent outside water surfaces. This is deliberate
    // terrain shaping, not a hidden correction to hydrology or new vegetation.
    var base:f32=planet.elevation[selected]-(if(nursery)@as(f32,0.010) else 0);
    for(ids[0..count],0..)|idx,slot| {
        if(!std.math.isFinite(planet.elevation[idx]) or !std.math.isFinite(planet.waterMass[idx]) or planet.waterMass[idx]<0)return -1;
        if(slot<floor_count)base=@max(base,planet.elevation[idx]-(if(nursery and slot==0)@as(f32,0.010) else 0));
        for(planet.getNeighbours(idx))|outside| {
            if(outside>=planet.waterMass.len)return -1;
            if(includes(ids[0..count],outside))continue;
            const water=planet.waterMass[outside];
            const surface=planet.elevation[outside]+water*conversion;
            if(!std.math.isFinite(surface) or !std.math.isFinite(water) or water<0)return -1;
            base=@max(base,surface);
        }
    }
    const floor_water_mass: f32=0.015/conversion;
    if(!std.math.isFinite(floor_water_mass) or floor_water_mass<=0)return -1;
    const center_elevation=base+(if(nursery)@as(f32,0.010) else 0);
    const center_water_mass: f32=(if(nursery)@as(f32,0.005) else 0.015)/conversion;
    if(!std.math.isFinite(center_elevation) or !std.math.isFinite(center_water_mass) or center_water_mass<=0)return -1;
    const rim=base+0.017;
    if(!std.math.isFinite(rim) or rim<=base)return -1;
    // All validation precedes mutation. Renderer uploads elevations each frame,
    // as with the existing terrain brush; no separate terrain cache is retained.
    for(ids[0..count],0..)|idx,i| {
        planet.elevation[idx]=if(i<floor_count)base else @max(planet.elevation[idx],rim);
        // Basin is an explicit larger intervention; fine-depth editor stays capped at 5m.
        planet.waterMass[idx]=if(i<floor_count)floor_water_mass else 0;
        if(i==0){planet.elevation[idx]=center_elevation;planet.waterMass[idx]=center_water_mass;}
    }
    return @intCast(count);
}
/// Bounded, allocation-free preview. No world or biology writes. Native session
/// owner must supply its actual world serial, not a user-supplied assertion.
pub const Plan = struct {
    owner:usize, world:u32, selected:usize, nursery:bool, conversion_bits:u32,
    count:usize, floor_count:usize,
    ids:[19]usize=[_]usize{0}**19,
    elevations:[19]f32=[_]f32{0}**19,
    waters:[19]f32=[_]f32{0}**19,
    neighbor_counts:[19]usize=[_]usize{0}**19,
    neighbors:[19][6]usize=[_][6]usize{[_]usize{0}**6}**19,
    dependency_count:usize=0,
    dependency_ids:[133]usize=[_]usize{0}**133,
    elevation_bits:[133]u32=[_]u32{0}**133,
    water_bits:[133]u32=[_]u32{0}**133,
    water_added:f64=0, water_removed:f64=0,
    fn remember(self:*Plan,planet:anytype,id:usize) bool {
        if(id>=planet.waterMass.len or id>=planet.elevation.len)return false;
        if(includes(self.dependency_ids[0..self.dependency_count],id))return true;
        if(self.dependency_count==self.dependency_ids.len)return false;
        const n=self.dependency_count; self.dependency_count+=1;
        self.dependency_ids[n]=id;self.elevation_bits[n]=@bitCast(planet.elevation[id]);self.water_bits[n]=@bitCast(planet.waterMass[id]);
        return true;
    }
};
/// Recompute without mutation, then require the full exact plan/dependency
/// snapshot. Never silently apply a changed preview. Writes only water/terrain.
pub fn applyChecked(planet:anytype,plan:*const Plan,selected:usize,world:u32) i32 {
    if(plan.owner!=@intFromPtr(planet) or plan.world!=world or plan.selected!=selected)return -1;
    const fresh=preview(planet,plan.selected,selected,plan.nursery,world) orelse return -1;
    if(!std.meta.eql(plan.*,fresh))return -1;
    for(plan.ids[0..plan.count],0..)|idx,i| {
        planet.elevation[idx]=plan.elevations[i];planet.waterMass[idx]=plan.waters[i];
    }
    return @intCast(plan.count);
}
pub fn preview(planet:anytype, expected:usize, selected:usize, nursery:bool, world:u32) ?Plan {
    if (planet.worldMode != .origin or expected != selected or selected >= planet.waterMass.len or planet.elevation.len != planet.waterMass.len) return null;
    const conversion = planet.getKmPerWaterMass();
    if (!std.math.isFinite(conversion) or conversion <= 0) return null;
    var ids: [19]usize = undefined;
    ids[0] = selected;var count:usize = 1;
    for (planet.getNeighbours(selected)) |idx| {
        if (idx >= planet.waterMass.len) return null;
        if (includes(ids[0..count],idx)) continue;
        if(count==7)return null;
        ids[count]=idx;count+=1;
    }
    const floor_count=count;
    for(ids[0..floor_count])|inner| for(planet.getNeighbours(inner))|idx| {
        if(idx>=planet.waterMass.len)return null;
        if(includes(ids[0..count],idx))continue;
        if(count==ids.len)return null;
        ids[count]=idx;count+=1;
    };
    if(count==floor_count)return null;
    // Raise a dry rim above adjacent outside water surfaces. This is deliberate
    // terrain shaping, not a hidden correction to hydrology or new vegetation.
    var base:f32=planet.elevation[selected]-(if(nursery)@as(f32,0.010) else 0);
    for(ids[0..count],0..)|idx,slot| {
        if(!std.math.isFinite(planet.elevation[idx]) or !std.math.isFinite(planet.waterMass[idx]) or planet.waterMass[idx]<0)return null;
        if(slot<floor_count)base=@max(base,planet.elevation[idx]-(if(nursery and slot==0)@as(f32,0.010) else 0));
        for(planet.getNeighbours(idx))|outside| {
            if(outside>=planet.waterMass.len)return null;
            if(includes(ids[0..count],outside))continue;
            const water=planet.waterMass[outside];
            const surface=planet.elevation[outside]+water*conversion;
            if(!std.math.isFinite(surface) or !std.math.isFinite(water) or water<0)return null;
            base=@max(base,surface);
        }
    }
    const floor_water_mass: f32=0.015/conversion;
    if(!std.math.isFinite(floor_water_mass) or floor_water_mass<=0)return null;
    const center_elevation=base+(if(nursery)@as(f32,0.010) else 0);
    const center_water_mass: f32=(if(nursery)@as(f32,0.005) else 0.015)/conversion;
    if(!std.math.isFinite(center_elevation) or !std.math.isFinite(center_water_mass) or center_water_mass<=0)return null;
    const rim=base+0.017;
    if(!std.math.isFinite(rim) or rim<=base)return null;
    var plan:Plan=.{ .owner=@intFromPtr(planet), .world=world, .selected=selected, .nursery=nursery, .conversion_bits=@bitCast(conversion), .count=count, .floor_count=floor_count };
    // Preserve every read dependency, including outside-neighbor values even if
    // they did not win the max. Bounded real mesh degree is six.
    for(ids[0..count],0..)|idx,i| {
        plan.ids[i]=idx;
        if(!plan.remember(planet,idx))return null;
        const neighbors=planet.getNeighbours(idx);
        if(neighbors.len>6)return null;
        plan.neighbor_counts[i]=neighbors.len;
        for(neighbors,0..)|outside,j| {
            plan.neighbors[i][j]=outside;
            if(!plan.remember(planet,outside))return null;
        }
        plan.elevations[i]=if(i<floor_count)base else @max(planet.elevation[idx],rim);
        plan.waters[i]=if(i<floor_count)floor_water_mass else 0;
        if(i==0){plan.elevations[i]=center_elevation;plan.waters[i]=center_water_mass;}
        const delta=@as(f64,plan.waters[i])-@as(f64,planet.waterMass[idx]);
        if(delta>=0)plan.water_added+=delta else plan.water_removed-=delta;
    }
    return plan;
}

test "basin shapes bounded floor and dry rim, stays repeatable and rejects stale or invalid state atomically" {
    const P=struct {
        worldMode:enum{origin,sandbox}=.origin,
        waterMass:[6]f32=.{0,0.1,0.2,0.3,0,0.02},
        elevation:[6]f32=.{5000,5000.1,5000.2,5000.3,5000.4,5000.5},
        pub fn getKmPerWaterMass(_: *@This()) f32{return 1;}
        pub fn getNeighbours(_: *@This(),i:usize) []const usize{return switch(i){0=>&.{1,2},1=>&.{0,2,3},2=>&.{0,1,4},3=>&.{1,4,5},4=>&.{2,3,5},else=>&.{3,4}};}
    };
    var p=P{};const before=p;
    try std.testing.expectEqual(@as(i32,-1),makePond(&p,1,0));
    try std.testing.expectEqualSlices(f32,&before.waterMass,&p.waterMass);
    try std.testing.expectEqualSlices(f32,&before.elevation,&p.elevation);
    try std.testing.expectEqual(@as(i32,5),makePond(&p,0,0));
    for(0..3)|i|{try std.testing.expectEqual(@as(f32,0.015),p.waterMass[i]);try std.testing.expectEqual(p.elevation[0],p.elevation[i]);}
    for(3..5)|i|{try std.testing.expectEqual(@as(f32,0),p.waterMass[i]);try std.testing.expect(p.elevation[i]>p.elevation[0]+0.015);}
    try std.testing.expect(p.elevation[3]>p.elevation[5]+p.waterMass[5]);
    try std.testing.expectEqual(before.elevation[5],p.elevation[5]);
    try std.testing.expectEqual(before.waterMass[5],p.waterMass[5]);
    const once=p;
    try std.testing.expectEqual(@as(i32,5),makePond(&p,0,0));
    try std.testing.expectEqualSlices(f32,&once.elevation,&p.elevation);
    try std.testing.expectEqualSlices(f32,&once.waterMass,&p.waterMass);
    p.worldMode=.sandbox;try std.testing.expectEqual(@as(i32,-1),makePond(&p,0,0));
    p.worldMode=.origin;p.waterMass[5]=std.math.nan(f32);const snapshot=p.elevation;
    try std.testing.expectEqual(@as(i32,-1),makePond(&p,0,0));
    try std.testing.expectEqualSlices(f32,&snapshot,&p.elevation);
}

test "nursery has shallow center shared waterline, reservoir, dry rim, repeatability and atomic rejection" {
    const P=struct {
        worldMode:enum{origin,sandbox}=.origin,
        waterMass:[6]f32=.{0,0.1,0.2,0.3,0,0.02},
        elevation:[6]f32=.{5000,5000.1,5000.2,5000.3,5000.4,5000.5},
        pub fn getKmPerWaterMass(_: *@This()) f32{return 1;}
        pub fn getNeighbours(_: *@This(),i:usize) []const usize{return switch(i){0=>&.{1,2},1=>&.{0,2,3},2=>&.{0,1,4},3=>&.{1,4,5},4=>&.{2,3,5},else=>&.{3,4}};}
    };
    var p=P{};
    try std.testing.expectEqual(@as(i32,5),makeNursery(&p,0,0));
    try std.testing.expectEqual(@as(f32,0.005),p.waterMass[0]);
    for(1..3)|i|{try std.testing.expectEqual(@as(f32,0.015),p.waterMass[i]);try std.testing.expectApproxEqAbs(p.elevation[0]+p.waterMass[0],p.elevation[i]+p.waterMass[i],0.001);}
    for(3..5)|i|{try std.testing.expectEqual(@as(f32,0),p.waterMass[i]);try std.testing.expect(p.elevation[i]>p.elevation[0]+p.waterMass[0]);}
    const once=p;
    try std.testing.expectEqual(@as(i32,5),makeNursery(&p,0,0));
    try std.testing.expectEqualSlices(f32,&once.elevation,&p.elevation);
    try std.testing.expectEqualSlices(f32,&once.waterMass,&p.waterMass);
    try std.testing.expectEqual(@as(i32,-1),makeNursery(&p,1,0));
    try std.testing.expectEqualSlices(f32,&once.waterMass,&p.waterMass);
    p.waterMass[5]=std.math.nan(f32);const elevations=p.elevation;const waters=p.waterMass;
    try std.testing.expectEqual(@as(i32,-1),makeNursery(&p,0,0));
    try std.testing.expectEqualSlices(f32,&elevations,&p.elevation);
    for(0..5)|i|try std.testing.expectEqual(waters[i],p.waterMass[i]);
}

const PlanFixture = struct {
    worldMode:enum{origin,sandbox}=.origin,
    waterMass:[20]f32=[_]f32{0.02}**20,
    elevation:[20]f32=[_]f32{5000}**20,
    biology:[20]u64=[_]u64{1234567}**20,
    conversion:f32=1,
    pentagon:bool=false,
    pub fn getKmPerWaterMass(self:*@This()) f32{return self.conversion;}
    pub fn getNeighbours(self:*@This(),i:usize) []const usize {
        const table=[20][]const usize{ &.{1,2,3,4,5,6}, &.{0,7,8}, &.{0,9,10}, &.{0,11,12}, &.{0,13,14}, &.{0,15,16}, &.{0,17,18}, &.{1,19}, &.{1,19}, &.{2,19}, &.{2,19}, &.{3,19}, &.{3,19}, &.{4,19}, &.{4,19}, &.{5,19}, &.{5,19}, &.{6,19}, &.{6,19}, &.{7,8} };
        if(i==0 and self.pentagon)return table[0][0..5];
        return table[i];
    }
};
test "preview is pure and checked writes match frozen unchanged action bitwise across mesh/finite cases" {
    for(0..200)|k| for([_]bool{false,true})|nursery| {
        var p=PlanFixture{.pentagon=k%2==0,.conversion=0.0001+@as(f32,@floatFromInt(k+1))*0.002};
        for(0..20)|i| {p.elevation[i]=4999+@as(f32,@floatFromInt((i*17+k*31)%99))*0.031;p.waterMass[i]=@as(f32,@floatFromInt((i*13+k*7)%41))*0.004;}
        const before=p;var old=p;
        const plan=preview(&p,0,0,nursery,17) orelse return error.UnexpectedRefusal;
        try std.testing.expect(std.meta.eql(before,p));
        const n=shapeBasin(&old,0,0,nursery);
        try std.testing.expectEqual(n,applyChecked(&p,&plan,0,17));
        try std.testing.expect(std.meta.eql(old,p));
        try std.testing.expectEqual(@as(usize,if(p.pentagon)16 else 19),plan.count);
        try std.testing.expectEqual(@as(usize,if(p.pentagon)6 else 7),plan.floor_count);
        var delta:f64=0;for(p.waterMass,before.waterMass)|a,b|delta+=@as(f64,a)-@as(f64,b);
        try std.testing.expectApproxEqAbs(delta,plan.water_added-plan.water_removed,1e-12);
    };
}
test "checked plan refuses stale world selection outside input topology owner and tampering atomically" {
    var p=PlanFixture{};const plan=preview(&p,0,0,false,7).?;const original=p;
    try std.testing.expectEqual(@as(i32,-1),applyChecked(&p,&plan,0,8));
    try std.testing.expectEqual(@as(i32,-1),applyChecked(&p,&plan,1,7));
    var other=p;try std.testing.expectEqual(@as(i32,-1),applyChecked(&other,&plan,0,7));
    p.waterMass[19]+=0.001;const changed=p;
    try std.testing.expectEqual(@as(i32,-1),applyChecked(&p,&plan,0,7));try std.testing.expect(std.meta.eql(changed,p));
    p=original;p.pentagon=true;const topology=p;
    try std.testing.expectEqual(@as(i32,-1),applyChecked(&p,&plan,0,7));try std.testing.expect(std.meta.eql(topology,p));
    p=original;var tampered=plan;tampered.waters[0]+=1;
    try std.testing.expectEqual(@as(i32,-1),applyChecked(&p,&tampered,0,7));try std.testing.expect(std.meta.eql(original,p));
    p.conversion*=2;const conversion=p;
    try std.testing.expectEqual(@as(i32,-1),applyChecked(&p,&plan,0,7));try std.testing.expect(std.meta.eql(conversion,p));
}
test "invalid and extreme inputs agree with old action and never mutate through preview" {
    for([_]f32{0,-1,std.math.inf(f32),std.math.nan(f32),1e-38,1e38})|value| {
        var p=PlanFixture{.conversion=value};var old=p;
        const plan=preview(&p,0,0,true,1);const rc=shapeBasin(&old,0,0,true);
        try std.testing.expectEqual(rc>=0,plan!=null);
        if(plan)|q|{try std.testing.expectEqual(rc,applyChecked(&p,&q,0,1));try std.testing.expectEqualSlices(f32,&old.waterMass,&p.waterMass);}
    }
    for([_]f32{std.math.nan(f32),std.math.inf(f32),-1})|value| {
        var p=PlanFixture{};p.waterMass[19]=value;const before=p.elevation;
        try std.testing.expect(preview(&p,0,0,false,1)==null);try std.testing.expectEqualSlices(f32,&before,&p.elevation);
    }
    var p=PlanFixture{};p.elevation=[_]f32{1e30}**20;
    try std.testing.expect(preview(&p,0,0,false,1)==null);
}
