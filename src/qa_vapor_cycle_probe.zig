const std=@import("std");const C=@import("experimental/vapor_cycle_probe.zig");const T=@import("experimental/root_vapor_receipt.zig");const P=@import("experimental/physical_water_f64.zig");const A=@import("simulation/atmosphere_water.zig");
fn equalDelta(a:f64,b:f64,c:f64,d:f64)!void{const x=P.difference(a,b);const y=P.difference(c,d);try std.testing.expectEqual(@as(f64,0),x.lo);try std.testing.expectEqual(@as(f64,0),y.lo);try std.testing.expectEqual(x.hi,y.hi);}
test "fixed actual pulse conditioned columns and unfavorable phases" {
 const cases=[_][6]f64{
 .{58.00004577636719,1680.0450439453125,1707.4408831105316,294.3619384765625,0.9999999167069676,5.445914790658257e-5},
 .{115.51077270507812,1635.706298828125,1576.8606428660353,293.0024108886719,0.9999991749741014,1.3555834952327928e-6},
 .{1e12,1680,1000,293,1,1e-6},.{0,1680,1000,270,1,1e-6},.{1,0,1000,293,1,1e-6},.{1,1e30,1e30,293,1,1e-20}};
 for(cases,0..)|x,i|for([_]f64{360,720,1440})|dt|for([_]bool{false,true})|pulse|{
  // Density-to-native conversion is an explicit initial representation, not an engine bridge proof.
  const soil=x[4]*7669529600.0/1e9;const request=if(pulse)x[5]*7669529600.0/1e9 else 0;
  const t=T.transfer(soil,x[1],request).?;try equalDelta(soil,t.source,t.vapor,x[1]);
  const s=C.State{.liquid=@floatCast(x[0]),.vapor=t.vapor};const r=C.phase(s,x[2],x[3],dt).?;
  try equalDelta(@as(f64,s.liquid),@as(f64,r.state.liquid),r.state.vapor,s.vapor);
  try std.testing.expect(r.evap_paid<=r.evap_requested and r.rain_paid<=r.rain_requested);
  // Synthetic fixed directed edge; not an actual world's wind/geometry.
  const rate=A.edgeRate(.{0,0,0},.{100,0,0},.{0.01,0,0});
  const asked=A.coefficient(r.state.vapor,rate,dt)*rate;
  const edge=T.transfer(r.state.vapor,200,asked).?;try equalDelta(r.state.vapor,edge.source,edge.vapor,200);
  const legacy=A.phase(s.liquid,@as(f32,@floatCast(s.vapor)),x[2],x[3],dt,0).?;
  const ll:f32=@floatCast(legacy.liquid);const lv:f32=@floatCast(legacy.vapor);
  std.debug.print("CYCLE {{\"case\":{},\"dt\":{d},\"pulse\":{},\"soil0\":{d},\"soil1\":{d},\"v0\":{d},\"v1\":{d},\"l0\":{d},\"l1\":{d},\"v2\":{d},\"edge_source\":{d},\"edge_target\":{d},\"pulse_paid\":{d},\"evap_request\":{d},\"evap_paid\":{d},\"rain_request\":{d},\"rain_paid\":{d},\"edge_request\":{d},\"edge_paid\":{d},\"legacy_l\":{d},\"legacy_v\":{d}}}\n",.{i,dt,pulse,soil,t.source,x[1],s.vapor,s.liquid,r.state.liquid,r.state.vapor,edge.source,edge.vapor,t.paid,r.evap_requested,r.evap_paid,r.rain_requested,r.rain_paid,asked,edge.paid,ll,lv});
 };
}
test "invalids refuse and cold forbids evaporation" {try std.testing.expect(C.phase(.{.liquid=1,.vapor=1},1,std.math.nan(f64),1)==null);try std.testing.expect(C.phase(.{.liquid=-1,.vapor=1},1,300,1)==null);try std.testing.expectEqual(@as(f64,0),C.phase(.{.liquid=1,.vapor=0},1000,273.15,1440).?.evap_paid);}
