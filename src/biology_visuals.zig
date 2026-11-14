//! Visual-only helpers. These never modify simulation state or organism counts.
const std = @import("std");
fn dot(a:[3]f32,b:[3]f32) f32 {return a[0]*b[0]+a[1]*b[1]+a[2]*b[2];}
fn cross(a:[3]f32,b:[3]f32) [3]f32 {return .{a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]};}
fn norm(a:[3]f32) [3]f32 {const n=@sqrt(dot(a,a));return .{a[0]/n,a[1]/n,a[2]/n};}
/// Column-major Y-up rabbit model; local feet are at -35.810169 in original OBJ.
pub fn groundedRabbit(point:[3]f32,scale:f32) [4][4]f32 {
    const up=norm(point);
    const reference:[3]f32=if(@abs(up[2])<0.95) .{0,0,1} else .{1,0,0};
    const right=norm(cross(up,reference));
    const forward=cross(right,up);
    const footLift=35.810169*scale;
    return .{
        .{right[0]*scale,right[1]*scale,right[2]*scale,0},
        .{up[0]*scale,up[1]*scale,up[2]*scale,0},
        .{forward[0]*scale,forward[1]*scale,forward[2]*scale,0},
        .{point[0]+up[0]*footLift,point[1]+up[1]*footLift,point[2]+up[2]*footLift,1},
    };
}
pub fn sproutSize(cover:f32) f32 {return 3+7*std.math.clamp(cover,0,1);}
pub fn showSprouts(distance:f32,radius:f32,normal_view:bool) bool {return normal_view and distance < radius*1.3;}
test "rabbit feet rest on surface and Y up follows radial at all axes" {
    const sites=[_][3]f32{.{5000,0,0},.{0,5000,0},.{0,-5000,0},.{0,0,5000},.{0,0,-5000},.{3000,4000,0}};
    for(sites)|p|{const m=groundedRabbit(p,0.12);const up=norm(p);
        const feet:[3]f32=.{m[3][0]-35.810169*m[1][0],m[3][1]-35.810169*m[1][1],m[3][2]-35.810169*m[1][2]};
        for(feet,p)|actual,expected|try std.testing.expectApproxEqAbs(expected,actual,0.001);
        try std.testing.expectApproxEqAbs(@as(f32,0.12),dot(.{m[1][0],m[1][1],m[1][2]},up),0.00001);
        try std.testing.expectApproxEqAbs(@as(f32,0),dot(.{m[0][0],m[0][1],m[0][2]},up),0.00001);
    }
}
test "sprouts scale with real biomass and stay off globe and overlays" {
    try std.testing.expect(sproutSize(0.2)<sproutSize(0.8));
    try std.testing.expectEqual(@as(f32,10),sproutSize(2));
    try std.testing.expect(showSprouts(5500,5000,true));
    try std.testing.expect(!showSprouts(10000,5000,true));
    try std.testing.expect(!showSprouts(5500,5000,false));
}

/// Historical feeding evidence in a currently living, grazing-capable cohort.
/// Not a claim of feeding this frame or animal identity.
pub fn hasFed(cohorts: anytype) bool {
    for (cohorts) |c| {
        if (c.biomass > 0 and c.feeding > 0 and c.lifetime_grazed > 0) return true;
    }
    return false;
}
test "feeding marker requires living capability and recorded intake" {
    const C = struct { biomass:f32, feeding:f32, lifetime_grazed:f32 };
    try std.testing.expect(!hasFed([_]C{.{.biomass=1,.feeding=0.2,.lifetime_grazed=0}}));
    try std.testing.expect(!hasFed([_]C{.{.biomass=0,.feeding=0.2,.lifetime_grazed=1}}));
    try std.testing.expect(!hasFed([_]C{.{.biomass=1,.feeding=0,.lifetime_grazed=1}}));
    try std.testing.expect(hasFed([_]C{.{.biomass=1,.feeding=0.2,.lifetime_grazed=0.01}}));
}

/// Map-scale schematic only: no tissue means no raised collecting glyph.
pub fn producerShape(support:f32,frond:f32,height_m:f32) ?struct{stem:f32,canopy:f32} {
    if (!std.math.isFinite(support) or !std.math.isFinite(frond) or !std.math.isFinite(height_m) or support<=0 or frond<=0 or height_m<=0) return null;
    return .{.stem=4+18*std.math.clamp(height_m/0.5,0,1),.canopy=3+9*@sqrt(std.math.clamp(frond,0,1))};
}
test "producer schematic requires actual tissue and bounded height" {
    try std.testing.expect(producerShape(0,1,0.5)==null);
    try std.testing.expect(producerShape(1,0,0.5)==null);
    const small=producerShape(0.01,0.02,0.01).?;
    const large=producerShape(1,1,0.5).?;
    try std.testing.expect(small.stem<large.stem and small.canopy<large.canopy);
    try std.testing.expectEqual(@as(f32,22),producerShape(1,1,999).?.stem);
}
