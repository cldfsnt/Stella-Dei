const std=@import("std");const visuals=@import("biology_visuals.zig");
fn dot(a:[3]f32,b:[3]f32)f32{return a[0]*b[0]+a[1]*b[1]+a[2]*b[2];}
fn unit(a:[3]f32)[3]f32{const n=@sqrt(dot(a,a));return .{a[0]/n,a[1]/n,a[2]/n};}
fn mul(m:[4][4]f32,n:[3]f32)[3]f32{return .{m[0][0]*n[0]+m[1][0]*n[1]+m[2][0]*n[2],m[0][1]*n[0]+m[1][1]*n[1]+m[2][1]*n[2],m[0][2]*n[0]+m[1][2]*n[1]+m[2][2]*n[2]};}
test "rabbit local upward normal follows world radial under actual grounded model"{
 const sites=[_][3]f32{.{5000,0,0},.{0,5000,0},.{0,-5000,0},.{0,0,5000},.{0,0,-5000},.{3000,4000,0}};
 for(sites)|p|for([_]f32{0.12,1,2})|scale|{
  const model=visuals.groundedRabbit(p,scale);const transformed=unit(mul(model,.{0,1,0}));
  try std.testing.expectApproxEqAbs(@as(f32,1),dot(transformed,unit(p)),1e-6);
  try std.testing.expectApproxEqAbs(@as(f32,0),dot(transformed,mul(model,.{1,0,0})),1e-6);
 };
 // Visible bug: local+Y top face at world+X was assigned zero diffuse light
 // under radial daylight, despite its actual transformed normal facing the sun.
 try std.testing.expectEqual(@as(f32,0),dot(.{0,1,0},.{1,0,0}));
 try std.testing.expectEqual(@as(f32,1),dot(unit(mul(visuals.groundedRabbit(.{5000,0,0},0.12),.{0,1,0})),.{1,0,0}));
}
test "uniform scale cancels after normalization and fragment normal remains unit"{
 const n=unit(.{1,2,3});const p=[3]f32{3000,4000,0};
 const a=unit(mul(visuals.groundedRabbit(p,0.12),n));const b=unit(mul(visuals.groundedRabbit(p,1),n));
 for(a,b)|x,y|try std.testing.expectApproxEqAbs(x,y,1e-6);
 const interpolated=[3]f32{0.5,0.5,0};try std.testing.expect(dot(interpolated,interpolated)<1);
 try std.testing.expectApproxEqAbs(@as(f32,1),dot(unit(interpolated),unit(interpolated)),1e-6);
}
