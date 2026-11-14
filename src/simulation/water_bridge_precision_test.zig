const std=@import("std");
const M=@import("microbes.zig");
const P=@import("water_precision.zig");
// Exact arithmetic copied from the current Planet f32 hydrology bridge.
fn currentBridge(surface:*f32,vapor:*f32,area:f64,f:M.Flux) void {
 const scale=area/1e9;
 surface.*=@floatCast(@max(0,@as(f64,surface.*)+(@as(f64,f.water_returned)-f.water_taken)*scale));
 vapor.*+=@as(f32,@floatCast(@as(f64,f.water_evaporated)*scale));
}
test "quantify current Planet f32 bridge error at biological scale" {
 const area:f64=7669529600;
 for([_]bool{false,true})|corrected|for([_]f32{0.02,15,50})|depth_m|for([_]u32{1,60,1440})|dt|{
  var surface:f32=@floatCast(@as(f64,depth_m)*1000*area/1e9);
  var vapor:f32=@floatCast(100*area/1e9);
  var cell=M.initialized(7);cell.cohorts[0]=.{.biomass=0.1,.support_mass=0.004,.structure=0.15,.organization=0.04,.water_retention=0.4,.lineage=1};
  var stats:M.Stats=.{.next_lineage=2};
  const start=(@as(f64,surface)+vapor)*1e9/area;
  var took:f64=0;var evaporated:f64=0;var returned:f64=0;var peak_error:f64=0;
  const n=3*86400/dt;
  for(0..n)|step|{
   const seconds=step*dt;
   const available=@as(f64,surface)*1e9/area+cell.surface_water_carry;
   const env:M.Environment=.{.temperature=if(seconds>=2*86400) 270 else 303,.depth_km=@floatCast(available/1000000),.liquid_available=available,.light=if(seconds%86400<43200) 1 else 0,.carbon_available=100,.oxygen_carbon_capacity=100};
   const f=M.step(&cell,env,@floatFromInt(dt));took+=f.water_taken;evaporated+=f.water_evaporated;returned+=f.water_returned;
   if(corrected){try std.testing.expect(P.apply(&surface,&vapor,&cell.surface_water_carry,&cell.vapor_water_carry,area,f.water_taken,f.water_returned,f.water_evaporated));}else currentBridge(&surface,&vapor,area,f);
   if(seconds%86400==0)_=M.reproduce(&cell,0,&cell,&stats,false);
   const total=(@as(f64,surface)+vapor)*1e9/area+M.storedWater(cell)+cell.surface_water_carry+cell.vapor_water_carry;
   peak_error=@max(peak_error,@abs(total-start));
  }
  const end=(@as(f64,surface)+vapor)*1e9/area+M.storedWater(cell)+cell.surface_water_carry+cell.vapor_water_carry;
  const model_error=took-evaporated-returned-M.storedWater(cell);
  if(corrected)try std.testing.expect(peak_error<0.0000001);
  std.debug.print("BRIDGE corrected={} depth_m={d} dt_s={d} days=3 error_kg_m2={d} peak_kg_m2={d} living_reserve_kg_m2={d} relative_to_reserve={d} model_error={d}\n",.{corrected,depth_m,dt,end-start,peak_error,M.storedWater(cell),@abs(end-start)/@max(@as(f64,0.000001),M.storedWater(cell)),model_error});
 };
}

test "water carry stays accounted when weather drains raw compartments" {
 const area:f64=7669529600;var surface:f32=115042.9453;var vapor:f32=766.953;
 var cell=M.initialized(2);cell.cohorts[0]=.{.biomass=0.1,.support_mass=0.004,.organization=0.04,.structure=0.15,.lineage=1};
 const initial=(@as(f64,surface)+vapor)*1e9/area;var runoff:f64=0;
 for(0..24*1000)|hour|{
  if(hour==24){runoff+=(@as(f64,surface)+vapor)*1e9/area;surface=0;vapor=0;}
  const available=@as(f64,surface)*1e9/area+cell.surface_water_carry;
  const env:M.Environment=.{.temperature=303,.depth_km=@floatCast(@as(f64,surface)*1e9/area/1000000),.liquid_available=available,.light=1,.carbon_available=100,.oxygen_carbon_capacity=100};
  const f=M.step(&cell,env,3600);
  try std.testing.expect(P.apply(&surface,&vapor,&cell.surface_water_carry,&cell.vapor_water_carry,area,f.water_taken,f.water_returned,f.water_evaporated));
  try std.testing.expect(P.validCarry(surface,cell.surface_water_carry,area));try std.testing.expect(P.validCarry(vapor,cell.vapor_water_carry,area));
  const total=(@as(f64,surface)+vapor)*1e9/area+cell.surface_water_carry+cell.vapor_water_carry+M.storedWater(cell)+runoff;
  try std.testing.expectApproxEqAbs(initial,total,0.0000001);
 }
 try std.testing.expectEqual(@as(f32,0),M.biomass(cell));
}
