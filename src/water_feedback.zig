//! Last successful selected-patch water step, not a held-gesture total.
const std=@import("std");
fn metres(buf:[]u8,value:f64) []const u8 {
    if(!std.math.isFinite(value) or value<0)return "?";
    if(value==0)return "0";
    if(value<0.01)return "<0.01";
    if(value>=10000)return std.fmt.bufPrint(buf,"{e:.2}",.{value}) catch "large";
    return std.fmt.bufPrint(buf,"{d:.2}",.{value}) catch "?";
}
pub fn lastStep(buf:[]u8,removed_m:f64,depth_m:f64) []const u8 {
    var r:[32]u8=undefined;var d:[32]u8=undefined;
    return std.fmt.bufPrint(buf,"Patch last step: -{s}m; depth {s}m",.{metres(&r,removed_m),metres(&d,depth_m)}) catch "Water removed from selected patch";
}
test "tap and shallow depletion report actual represented depths" {
    var b:[128]u8=undefined;
    try std.testing.expectEqualStrings("Patch last step: -1.00m; depth 16.47m",lastStep(&b,1,16.46607));
    try std.testing.expectEqualStrings("Patch last step: -<0.01m; depth 0m",lastStep(&b,0.0001,0));
}
test "held step isn't cumulative and values stay bounded" {
    var b:[128]u8=undefined;
    try std.testing.expectEqualStrings("Patch last step: -0.08m; depth 3.20m",lastStep(&b,5.0/60.0,3.2));
    const huge=lastStep(&b,1e100,1e200);try std.testing.expect(huge.len<80);
    try std.testing.expect(std.mem.indexOf(u8,lastStep(&b,0.01,0.009),"depth <0.01m")!=null);
    try std.testing.expect(std.mem.indexOf(u8,lastStep(&b,std.math.nan(f64),std.math.inf(f64)),"?")!=null);
    var tiny:[1]u8=undefined;try std.testing.expectEqualStrings("Water removed from selected patch",lastStep(&tiny,1,2));
}
test "real water brush changed steps and refused states" {
    const W=@import("water_brush.zig");var water=[_]f32{3,7};var b:[128]u8=undefined;
    const tap=W.remove(&water,0,0.001,true,0);try std.testing.expectEqual(W.Status.changed,tap.status);
    try std.testing.expectEqualStrings("Patch last step: -1.00m; depth 2.00m",lastStep(&b,tap.removed_m,@as(f64,water[0])*0.001*1000));
    const held=W.remove(&water,0,0.001,false,1.0/60.0);try std.testing.expect(held.removed_m>0 and held.removed_m<0.1);
    water[0]=0.0001;const shallow=W.remove(&water,0,0.001,true,0);try std.testing.expectEqualStrings("Patch last step: -<0.01m; depth 0m",lastStep(&b,shallow.removed_m,water[0]));
    const old=water;try std.testing.expectEqual(W.Status.dry,W.remove(&water,0,0.001,true,0).status);try std.testing.expectEqualSlices(f32,&old,&water);
}
