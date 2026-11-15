const std=@import("std");const H=@import("feeding_marker.zig");const T=@import("colony_targets.zig");
test "selected center and body edges remain assigned after rejecting overlapping glyph"{
 var targets=T.List{};targets.add(.{.cell=77,.x=100,.y=100,.scale=0.75});
 for([_][3]f32{.{120,100,0.325},.{100,118,0.325},.{140,100,0.325},.{100,145,0.325}})|p|{
  if(!H.overlaps(100,100,0.75,p[0],p[1],p[2]))targets.add(.{.cell=88,.x=p[0],.y=p[1],.scale=p[2]});
 }
 try std.testing.expectEqual(@as(usize,3),targets.count);
 for([_][2]f32{.{100,100},.{100-21.5*0.75,100-10*0.75},.{100+21.5*0.75,100-10*0.75},.{100,100-40.5*0.75},.{100,100+7.5*0.75}})|p|try std.testing.expectEqual(@as(?usize,77),targets.pick(p[0],p[1]));
}
