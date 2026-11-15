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
