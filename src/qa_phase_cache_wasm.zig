//! Pure wasm32-freestanding parity smoke; not Emscripten or browser gameplay.
const std=@import("std");const W=@import("experimental/phase_reference.zig");const C=@import("experimental/phase_cache.zig").Cache;
const Production=@import("simulation/atmosphere_water.zig");
var checked:u32=0;
fn same(a:?W.Phase,b:?W.Phase)bool{
 if((a==null)!=(b==null))return false;if(a)|p|{inline for(.{"liquid","vapor","evaporated","condensed","rain_rate"})|f|if(@as(u64,@bitCast(@field(p,f)))!=@as(u64,@bitCast(@field(b.?,f))))return false;}return true;
}
export fn parity_count()u32{return checked;}
export fn parity_run()u32{
 checked=0;var failures:u32=0;
 const edges=[_]f64{0,-0.0,1e-320,1e-12,1,60,360,1440,86400,1e300,std.math.floatMax(f64),-1,std.math.inf(f64),std.math.nan(f64)};
 for(edges)|dt|{const c=C.init(dt);for(0..1024)|i|{
  const x:f64=@floatFromInt(i);const liquid=x*97.125;const vapor=@mod(x*43.25,500);const saturation=@mod(x*71.5,700);const temp=250+@mod(x,80);const rain=x*0.125;
  const reference=W.phase(liquid,vapor,saturation,temp,dt,rain);
  if(!same(reference,c.phase(liquid,vapor,saturation,temp,rain)))failures+=1;
  if(!same(reference,Production.PhaseStep.init(dt).phase(liquid,vapor,saturation,temp,rain)))failures+=1;
  if(!same(reference,Production.phase(liquid,vapor,saturation,temp,dt,rain)))failures+=1;checked+=1;
 }}
 for(edges)|x|for(edges)|dt|{const c=C.init(dt);inline for(0..5)|field|{
  var v=[5]f64{1000,120,200,293,3};v[field]=x;
  const reference=W.phase(v[0],v[1],v[2],v[3],dt,v[4]);
  if(!same(reference,c.phase(v[0],v[1],v[2],v[3],v[4])))failures+=1;
  if(!same(reference,Production.PhaseStep.init(dt).phase(v[0],v[1],v[2],v[3],v[4])))failures+=1;
  if(!same(reference,Production.phase(v[0],v[1],v[2],v[3],dt,v[4])))failures+=1;checked+=1;
 }};
 return failures;
}
