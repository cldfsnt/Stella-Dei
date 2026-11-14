//! Bounded display only. Exact session counters remain unchanged in Planet.
const std=@import("std");
pub fn count(buffer:[]u8,n:u64) []const u8 {
 if(n>999)return "999+";
 return std.fmt.bufPrint(buffer,"{d}",.{n}) catch "?";
}
pub fn line(buffer:[]u8,arrivals:u64,losses:u64) []const u8 {
 var a:[4]u8=undefined;var l:[4]u8=undefined;
 return std.fmt.bufPrint(buffer,"Since load: {s} arrivals · {s} tracked losses",.{count(&a,arrivals),count(&l,losses)}) catch "Session dispersal";
}
pub const legend="◇ paid arrival · × tracked loss (not all deaths)";
test "counter formatting is bounded and does not misrepresent capped counts"{
 var b:[96]u8=undefined;
 try std.testing.expectEqualStrings("Since load: 0 arrivals · 0 tracked losses",line(&b,0,0));
 try std.testing.expectEqualStrings("Since load: 999 arrivals · 999+ tracked losses",line(&b,999,1000));
 try std.testing.expectEqualStrings("Since load: 999+ arrivals · 999+ tracked losses",line(&b,std.math.maxInt(u64),std.math.maxInt(u64)));
 try std.testing.expect(line(&b,std.math.maxInt(u64),std.math.maxInt(u64)).len<60);
}
