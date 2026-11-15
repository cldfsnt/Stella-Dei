//! Isolated finite search/handling hypothesis. Dimensionless cover, seconds, satiety.
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
 }
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
