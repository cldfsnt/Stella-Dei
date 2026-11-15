//! Display-only percentage-point formatting; never used in simulation.
const std=@import("std");
pub fn points(buffer:[]u8, value:f64)[]const u8{
 if(!std.math.isFinite(value))return "unavailable";
 if(value==0)return "0.0000";
 const sign:[]const u8=if(value<0) "-" else "+";
 if(@abs(value)<0.0001)return std.fmt.bufPrint(buffer,"{s}<0.0001",.{sign}) catch "unavailable";
 return std.fmt.bufPrint(buffer,"{s}{d:.4}",.{sign,@abs(value)}) catch "unavailable";
}
test "fixed percentage points never disguise nonzero tiny changes"{
 var b:[64]u8=undefined;
 try std.testing.expectEqualStrings("0.0000",points(&b,0));
 try std.testing.expectEqualStrings("0.0000",points(&b,-0.0));
 try std.testing.expectEqualStrings("+0.0783",points(&b,0.0783));
 try std.testing.expectEqualStrings("-0.0783",points(&b,-0.0783));
 try std.testing.expectEqualStrings("+<0.0001",points(&b,1e-30));
 try std.testing.expectEqualStrings("-<0.0001",points(&b,-1e-30));
 try std.testing.expectEqualStrings("+0.0001",points(&b,0.0001));
 try std.testing.expectEqualStrings("unavailable",points(&b,std.math.nan(f64)));
 try std.testing.expectEqualStrings("unavailable",points(&b,std.math.inf(f64)));
}
