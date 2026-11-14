const std=@import("std");
const M=@import("microbes.zig");
// Exact arithmetic copied from the current Planet f32 hydrology bridge.
fn currentBridge(surface:*f32,vapor:*f32,area:f64,f:M.Flux) void {
 const scale=area/1e9;
 surface.*=@floatCast(@max(0,@as(f64,surface.*)+(@as(f64,f.water_returned)-f.water_taken)*scale));
 vapor.*+=@as(f32,@floatCast(@as(f64,f.water_evaporated)*scale));
}
test "quantify current Planet f32 bridge error at biological scale" {
 const area:f64=7669529600;
 for([_]f32{0.02,15,50})|depth_m|for([_]u32{1,60,1440})|dt|{
  var surface:f32=@floatCast(@as(f64,depth_m)*1000*area/1e9);
  var vapor:f32=@floatCast(100*area/1e9);
  var cell=M.initialized(7);cell.cohorts[0]=.{.biomass=0.1,.support_mass=0.004,.structure=0.15,.organization=0.04,.water_retention=0.4,.lineage=1};
  var stats:M.Stats=.{.next_lineage=2};
  const start=(@as(f64,surface)+vapor)*1e9/area;
  var took:f64=0;var evaporated:f64=0;var returned:f64=0;var peak_error:f64=0;
  const n=3*86400/dt;
  for(0..n)|step|{
   const seconds=step*dt;
   const available=@as(f64,surface)*1e9/area;
   const env:M.Environment=.{.temperature=if(seconds>=2*86400) 270 else 303,.depth_km=@floatCast(available/1000000),.liquid_available=@floatCast(available),.light=if(seconds%86400<43200) 1 else 0,.carbon_available=100,.oxygen_carbon_capacity=100};
   const f=M.step(&cell,env,@floatFromInt(dt));took+=f.water_taken;evaporated+=f.water_evaporated;returned+=f.water_returned;
   currentBridge(&surface,&vapor,area,f);
   if(seconds%86400==0)_=M.reproduce(&cell,0,&cell,&stats,false);
   const total=(@as(f64,surface)+vapor)*1e9/area+M.storedWater(cell);
   peak_error=@max(peak_error,@abs(total-start));
  }
  const end=(@as(f64,surface)+vapor)*1e9/area+M.storedWater(cell);
  const model_error=took-evaporated-returned-M.storedWater(cell);
  std.debug.print("BRIDGE depth_m={d} dt_s={d} days=3 error_kg_m2={d} peak_kg_m2={d} living_reserve_kg_m2={d} relative_to_reserve={d} model_error={d}\n",.{depth_m,dt,end-start,peak_error,M.storedWater(cell),@abs(end-start)/@max(@as(f64,0.000001),M.storedWater(cell)),model_error});
 };
}
