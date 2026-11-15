//! Explicit session-only 3D render resolution. No simulation/save state.
const std=@import("std");
pub const Choice=enum(u32){sharp=100,reduced=75,fast=50};
var current:Choice=.sharp;
pub fn percent()u32{return @intFromEnum(current);}
pub fn set(value:u32)bool{
 const next:Choice=switch(value){100=>.sharp,75=>.reduced,50=>.fast,else=>return false};
 current=next;return true;
}
pub fn dimension(canvas:i32,choice:Choice)i32{
 const base:@TypeOf(@as(i64,0))=@max(1,canvas);
 return @intCast(@max(1,@divTrunc(base*@as(i64,@intFromEnum(choice)),100)));
}
pub fn dimensions(width:i32,height:i32)[2]i32{return .{dimension(width,current),dimension(height,current)};}
test "sharp default, explicit valid choices, invalid choices unchanged"{
 defer current=.sharp;current=.sharp;try std.testing.expectEqual(@as(u32,100),percent());
 for([_]u32{75,50,100})|v|{try std.testing.expect(set(v));try std.testing.expectEqual(v,percent());}
 for([_]u32{0,1,49,51,74,76,101,std.math.maxInt(u32)})|v|{try std.testing.expect(!set(v));try std.testing.expectEqual(@as(u32,100),percent());}
}
test "dimensions nonzero bounded no overflow and exact full scale"{
 for([_]i32{-1,0,1,239,390,700,768,1366,std.math.maxInt(i32)})|n|for([_]Choice{.sharp,.reduced,.fast})|c|{
 const d=dimension(n,c);try std.testing.expect(d>=1 and d<=@max(1,n));
 if(c==.sharp)try std.testing.expectEqual(@max(1,n),d);
 };
 try std.testing.expectEqual(@as(i32,1024),dimension(1366,.reduced));
 try std.testing.expectEqual(@as(i32,292),dimension(390,.reduced));
}
