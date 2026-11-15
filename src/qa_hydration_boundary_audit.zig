const std=@import("std");const H=@import("experimental/paid_hydration_fair.zig");
test "funded identical reservoir boundary diagnostic no candidate coefficient changes"{
 var charged:H.State=.{};charged.cell.cohorts[0]=.{.biomass=0.12940502166748047,.organization=0.13426367938518524,.support_mass=0.017374489456415176,.optimum=296.1463928222656,.efficiency=1.0451198816299438,.structure=0.13595879077911377,.feeding=0.20643378794193268,.qa_retention=0.25,.lineage=478,.parent=232,.generation=6};
 charged.liquid=1;charged.simultaneousUptake();const cap=H.capacity(charged.cell.cohorts[0]);try std.testing.expect(charged.retained[0]>0);
 // Same represented paid store and same one-hour evaporative expenditure in every snapshot.
 const demand=0.1*@as(f64,H.M.frondMass(charged.cell.cohorts[0]))/24;
 const spent=@min(charged.retained[0],demand);charged.retained[0]-=spent;charged.vapor_escrow+=spent;
 const hydration:f32=@floatCast(charged.retained[0]/cap);
 for([_]f32{0,0.000000001,0.0000001,0.000001,0.00001,0.00008,0.00015,0.0002})|depth|{
  for([_]f32{0,hydration})|h|{var cell=charged.cell;const f=H.M.step(&cell,.{.temperature=300,.depth_km=depth,.light=1,.carbon_available=10,.oxygen_carbon_capacity=10,.qa_hydration=.{h,0,0,0}},3600);
   std.debug.print("HYDRATION_BOUNDARY depth_m={d} h={d} paid_store={d} start_mass={d} mass={d} fixed={d} recycled={d}\n",.{depth*1000,h,charged.retained[0],charged.cell.cohorts[0].biomass,cell.cohorts[0].biomass,f.fixed,f.recycled});
  }
 }
}
