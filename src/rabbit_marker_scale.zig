//! Candidate display-only zoom scaling. No filtering or organism state.
const std=@import("std");
pub fn scale(distance:f32,radius:f32) f32 {
    if(!std.math.isFinite(distance) or !std.math.isFinite(radius) or radius<=0)return 1;
    const zoom=distance/radius;
    if(zoom<=1.12)return 1;
    if(zoom>=1.6)return 5.0/12.0;
    return 1-(zoom-1.12)/(1.6-1.12)*(1-5.0/12.0);
}
test "near badge unchanged, distant remains positive, continuous monotone" {
    try std.testing.expectEqual(@as(f32,1),scale(5200,5000));
    try std.testing.expectEqual(@as(f32,1),scale(5600,5000));
    try std.testing.expectEqual(@as(f32,5.0/12.0),scale(8000,5000));
    var prior:f32=1;
    for(0..1001)|i|{const s=scale(5000+@as(f32,@floatFromInt(i))*10,5000);try std.testing.expect(s<=prior and s>=5.0/12.0 and s<=1);prior=s;}
    for([_]f32{std.math.nan(f32),std.math.inf(f32)})|bad|try std.testing.expectEqual(@as(f32,1),scale(bad,5000));
    for([_]f32{0,-1,std.math.nan(f32),std.math.inf(f32)})|bad|try std.testing.expectEqual(@as(f32,1),scale(5000,bad));
    try std.testing.expectEqual(@as(f32,5.0/12.0),scale(std.math.floatMax(f32),5000));
}
