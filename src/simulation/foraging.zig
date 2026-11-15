//! Finite search/handling model for Sandbox rabbits. Cover is dimensionless; time is seconds.
//! No protected floor: a budget-funded final resolution fragment can be consumed.
const std=@import("std");
pub const maximum_per_day:f64=0.288;
pub const half_saturation:f64=0.1;
pub const fragment_resolution:f64=0.0001;
pub const Bite=struct{after:f32,eaten:f64=0,budget:f64=0,fragment:bool=false};
pub fn take(cover:f32,satiety:f32,seconds:f32) Bite {
    @setFloatMode(.strict);
    const no=Bite{.after=cover};
    if(!std.math.isFinite(cover) or cover<=0 or cover>1 or !std.math.isFinite(satiety) or satiety<0 or satiety>=100 or !std.math.isFinite(seconds) or seconds<=0)return no;
    const c:@TypeOf(@as(f64,0))=cover;
    const maximum=maximum_per_day*(@as(f64,seconds)/86400);
    const budget=@min(c,@min((100-@as(f64,satiety))/150,maximum));
    const desired=@min(budget,maximum*(c/(c+half_saturation)));
    const fragment=c-desired<fragment_resolution and c<=budget;
    var after:f32=if(fragment)0 else @floatCast(@max(0,c-desired));
    // A rounded receiver must never increase the actual debit beyond the hard budget.
    if(c-@as(f64,after)>budget)after=std.math.nextAfter(f32,after,std.math.inf(f32));
    const paid=c-@as(f64,after);
    if(paid<=0 or paid>budget or after<0 or after>cover)return no;
    return .{.after=after,.eaten=paid,.budget=budget,.fragment=fragment};
}
test "actual cover debit funds food under finite time and hunger caps" {
 for([_]f32{0,1e-7,0.00005,0.001,0.01,0.1,0.35,1})|c|for([_]f32{0,50,84.99,99.99,100})|s|for([_]f32{0,0.0001,1,360,720,1440,86400,1e7})|dt|{
  const b=take(c,s,dt);try std.testing.expect(b.after>=0 and b.after<=c);try std.testing.expectEqual(@as(f64,c)-b.after,b.eaten);
  try std.testing.expect(b.eaten<=b.budget);try std.testing.expect(b.eaten*150<=@as(f64,100)-s+1e-14);
 };
}
test "sparse meals no longer consume an entire 0.02 patch in one normal tick" {
 const b=take(0.02,84,1440);try std.testing.expect(b.after>0.019 and b.eaten>0);
 const extinction=take(0.00005,50,1440);try std.testing.expectEqual(@as(f32,0),extinction.after);try std.testing.expect(extinction.fragment);
 const tiny=take(0.00005,50,0.001);try std.testing.expect(tiny.after>0);try std.testing.expect(!tiny.fragment);
}
test "invalid inputs refuse unchanged" {
 for([_]f32{-1,std.math.nan(f32),std.math.inf(f32)})|bad|{
  try std.testing.expectEqual(@as(f32,0.2),take(0.2,50,bad).after);
  try std.testing.expectEqual(@as(f32,0.2),take(0.2,bad,1440).after);
 }
}

pub fn fedSatiety(before:f32,eaten:f64) f32 {
    @setFloatMode(.strict);
    if(!std.math.isFinite(before) or before<0 or before>100 or !std.math.isFinite(eaten) or eaten<=0)return before;
    const funded=eaten*150;
    var after:f32=@floatCast(@min(100,@as(f64,before)+funded));
    if(@as(f64,after)-before>funded)after=std.math.nextAfter(f32,after,before);
    return @max(before,after);
}
test "last fragment respects hunger and actual satiety funding" {
 const b=take(0.00005,99.999,1440);try std.testing.expect(b.after>0 and !b.fragment);
 for([_]f32{0.00005,0.02,0.35,1})|cover|for([_]f32{0,50,84.99,99.999})|sat|{
  const bite=take(cover,sat,1440);const after=fedSatiety(sat,bite.eaten);
  try std.testing.expect(after>=sat and after<=100);try std.testing.expect(@as(f64,after)-sat<=bite.eaten*150);
 };
}
test "fixed one-day sparse foraging refinement reports no-growth depletion" {
 for([_]f32{1440,720,360})|dt|{
  var cover:f32=0.02;var removed:f64=0;var i:usize=0;
  while(i<@as(usize,@intFromFloat(86400/dt))):(i+=1){const b=take(cover,50,dt);cover=b.after;removed+=b.eaten;}
  try std.testing.expect(cover>=0 and cover<0.02);
  std.debug.print("FORAGING_REFINEMENT dt={d} final_cover={d} removed={d} no_growth=true\n",.{dt,cover,removed});
 }
}
