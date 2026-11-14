const std=@import("std");
const S=@import("save_schema.zig");
test "actual v20 v6 fixture gains no reserve or precision water" {
 var arena=std.heap.ArenaAllocator.init(std.testing.allocator);defer arena.deinit();const a=arena.allocator();
 const path=std.posix.getenv("STELLA_V6_FIXTURE") orelse return error.SkipZigTest;
 const bytes=try std.fs.cwd().readFileAlloc(a,path,100*1024*1024);
 std.debug.print("REAL_V6 read={d}\n",.{bytes.len});
 var parsed=try S.parse(a,bytes);defer parsed.deinit();
 std.debug.print("REAL_V6 parsed version={d}\n",.{parsed.value.version});
 try std.testing.expectEqual(@as(u32,6),parsed.value.version);
 for(parsed.value.origin.?.cells)|saved|{
  const c=saved.runtime();try std.testing.expect(c.surface_water_carry==0 and c.vapor_water_carry==0);
  for(c.cohorts)|co|try std.testing.expect(co.water_reserve==0 and co.water_retention==0);
 }
}
