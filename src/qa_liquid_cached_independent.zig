const std=@import("std");const G=@import("experimental/liquid_gather.zig");const C=@import("experimental/liquid_gather_cached.zig");
fn compare(comptime n:usize,graph:*const [n][6]usize,mass:*const [n]f32,e:*const [n]f32,dt:f32)!void{
 var slots:[n][6]u8=undefined;try C.prepare(graph,&slots);
 var a:[n]f32=undefined;var b:[n]f32=undefined;var ea:[n][6]f64=undefined;var eb:[n][6]f64=undefined;
 for([_]bool{false,true})|reverse|{
 const la=try G.step(mass,e,graph,&ea,&a,1,dt,reverse);const lb=try C.step(mass,e,graph,&slots,&eb,&b,1,dt,reverse);
 try std.testing.expectEqualSlices(u8,std.mem.asBytes(&a),std.mem.asBytes(&b));try std.testing.expectEqualSlices(u8,std.mem.asBytes(&ea),std.mem.asBytes(&eb));try std.testing.expectEqual(la.rounding_signed,lb.rounding_signed);try std.testing.expectEqual(la.rounding_absolute,lb.rounding_absolute);
 }
}
test "cached exact naive duplicates self tail mixed and rebuilt same count"{
 var g=[_][6]usize{.{1,0,0,0,0,0},.{0,2,1,1,1,1},.{1,3,2,2,2,2},.{2,4,4,3,3,3},.{3,3,4,4,4,4}};
 const e=[_]f32{0,1,-1,2,0};
 for([_][5]f32{.{0,0,0,0,100},.{1e30,1e-20,0,2,3},.{1e-30,0,0,0,0},.{0,0,0,0,0},.{1,1,1,1,1}})|m|for([_]f32{0,1440,15000})|dt|{try compare(5,&g,&m,&e,dt);};
 // Same allocation and count, different reciprocal graph. Explicit prepare is required.
 g=.{.{4,0,0,0,0,0},.{2,1,1,1,1,1},.{1,3,2,2,2,2},.{2,3,3,3,3,3},.{0,4,4,4,4,4}};
 try compare(5,&g,&.{2,3,4,5,100},&e,1440);
}
test "cached topology refusal and offset aliases"{
 const bad=[_][6]usize{.{1,0,0,0,0,0},.{1,1,1,1,1,1}};var slots:[2][6]u8=undefined;try std.testing.expectError(error.InvalidTopology,C.prepare(&bad,&slots));
 const g=[_][6]usize{.{1,0,0,0,0,0},.{0,1,1,1,1,1}};try C.prepare(&g,&slots);var backing=[_]f32{1,0,0};var e=[_]f32{0,0};var edges:[2][6]f64=undefined;
 try std.testing.expectError(error.InvalidShape,C.step(backing[0..2],&e,&g,&slots,&edges,backing[1..3],1,1440,false));try std.testing.expectEqualSlices(f32,&.{1,0,0},&backing);
 try std.testing.expectError(error.InvalidShape,C.step(backing[0..2],&e,&g,&slots,&edges,&e,1,1440,false));
}
