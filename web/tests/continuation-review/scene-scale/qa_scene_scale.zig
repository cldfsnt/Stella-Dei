const std=@import("std");pub fn dimension(size:f32,scale:f32)c_int{return @intFromFloat(@max(1,@floor(size*scale)));}
pub fn requested()f32{const raw=std.posix.getenv("STELLA_SCENE_SCALE") orelse return 1;const value=std.fmt.parseFloat(f32,raw) catch return 1;return if(value==0.75 or value==0.5)value else 1;}
test "dimensions stay nonzero, bounded and within one pixel"{for([_]f32{1,239,390,700,768,1366})|n|for([_]f32{1,0.75,0.5})|s|{const d=dimension(n,s);try std.testing.expect(d>=1 and @as(f32,@floatFromInt(d))<=n);try std.testing.expect(@abs(@as(f32,@floatFromInt(d))-n*s)<1);};}
