//! Origin-only dimensional corrections. Legacy Sandbox equations stay intact.
const std = @import("std");
/// Ground active layer plus an explicit50m water mixed-layer approximation.
/// area:m², water_mass:10^9kg, returned capacity:J/K.
pub fn originHeatCapacity(area:f32,water_mass:f32,temperature:f32) f32 {
    const depth_m=@max(0,water_mass)*1e9/area/1000;
    const mixed_depth=@min(depth_m,50);
    const water_cp:f32=if(temperature>273.15)4184 else 2093;
    return area*(0.1*5513*700+mixed_depth*1000*water_cp);
}
/// Height difference/km-per-mass is mass, then multiplied by a dimensionless
/// time-dependent fraction. Multiplying by shared MASS again would square units.
pub fn heightLimitedMass(comptime T:type,height:T,km_per_mass:T,fraction:T) T {
    return height/km_per_mass*fraction;
}
fn transfer(mass:f32,height_difference:f32,km_per_mass:f32,fraction:f32) f32 {
    return @min(mass*fraction,@max(0,heightLimitedMass(f32,height_difference,km_per_mass,fraction)));
}
test "water thermal capacity uses depth, not grid size, and dry ground unchanged" {
    const area:f32=1e9;const mass:f32=3*area*1000/1e9;
    try std.testing.expectApproxEqRel(area*0.1*5513*700,originHeatCapacity(area,0,293),0.000001);
    try std.testing.expectApproxEqRel(originHeatCapacity(area,mass,293)/area,originHeatCapacity(area*4,mass*4,293)/(area*4),0.000001);
    try std.testing.expectApproxEqRel(@as(f32,12937910),originHeatCapacity(area,mass,293)/area,0.000001);
}
test "closed water exchange conserves water plus vapor and cannot overshoot or go negative" {
    var a:f32=1000;var b:f32=10;const vapor:f32=33;const before=a+b+vapor;
    const conversion:f32=0.00001;
    for(0..20000)|_|{
        const flux=transfer(a,(a-b)*conversion,conversion,0.0002);
        a-=flux;b+=flux;
        try std.testing.expect(a>=0 and b>=0 and a>=b-0.001);
    }
    try std.testing.expectApproxEqAbs(before,a+b+vapor,0.01);
    try std.testing.expectApproxEqAbs(a,b,1);
    try std.testing.expectEqual(@as(f32,0),transfer(100,0,conversion,0.1));
    // Equal physical water levels at different grid areas transfer equal depth.
    const small=transfer(100,0.001,0.00001,0.01)*0.00001;
    const large=transfer(400,0.001,0.0000025,0.01)*0.0000025;
    try std.testing.expectApproxEqAbs(small,large,0.00000001);
}
