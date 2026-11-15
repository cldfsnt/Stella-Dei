const std=@import("std");const E=@import("experimental/maintenance_quiescence.zig");const Q=E.Q;const M=@import("simulation/microbes.zig");
fn initial()Q.State{var s=Q.State{.active=M.initialized(42),.rest=M.initialized(43)};s.active.cohorts[0]=.{.biomass=0.2,.lineage=1};s.active.nutrient=0.1;s.rest.nutrient=0;return s;}
fn env(light:f32)M.Environment{return .{.temperature=303,.depth_km=0.001,.light=light,.carbon_available=0,.oxygen_carbon_capacity=0};}
const params=E.Parameters{.active_per_day=0.2,.rest_per_day=0.05,.unmet_stress_per_day=0.5};
fn check(s:Q.State,c:f64,n:f64)!void{try std.testing.expect(Q.valid(s));try std.testing.expectApproxEqAbs(c,Q.carbon(s),0.0001);try std.testing.expectApproxEqAbs(n,Q.nutrient(s),0.00001);}
test "maintenance actual ledgers no oxygen identical maximal hazard and invalid atomicity"{
 var s=initial();try std.testing.expect(Q.transfer(&s,true,0.1));const c=Q.carbon(s);const n=Q.nutrient(s);const before=s;
 const r=E.maintain(&s,params,1440).?;try check(s,c,n);
 try std.testing.expectApproxEqAbs(r.paid_active+r.paid_rest,s.air-before.air,1e-12);try std.testing.expectApproxEqAbs(r.paid_active+r.paid_rest,before.oxygen-s.oxygen,1e-12);
 try std.testing.expectApproxEqAbs(r.dead_active+r.dead_rest,@as(f64,s.active.detritus)-before.active.detritus,1e-8);
 s=before;s.oxygen=0;const zero=s;const z=E.maintain(&s,params,86400).?;
 try std.testing.expectEqual(@as(f64,0),z.paid_active+z.paid_rest);try std.testing.expectEqual(@as(f64,1),z.unmet_fraction);
 try std.testing.expectApproxEqAbs(z.dead_active/zero.active.cohorts[0].biomass,z.dead_rest/zero.rest.cohorts[0].biomass,1e-6);
 try std.testing.expectApproxEqAbs(1-@exp(@as(f64,-0.5)),z.stress_fraction,1e-12);try check(s,Q.carbon(zero),Q.nutrient(zero));
 const unchanged=s;var bad=params;bad.rest_per_day=0;try std.testing.expect(E.maintain(&s,bad,1440)==null);try std.testing.expectEqualDeep(unchanged,s);
 try std.testing.expect(E.maintain(&s,params,std.math.nan(f32))==null);try std.testing.expectEqualDeep(unchanged,s);
}
test "zero oxygen darkness death cannot wake or resurrect and rest has no uptake"{
 var s=initial();try std.testing.expect(Q.transfer(&s,true,0.2));const c=Q.carbon(s);const n=Q.nutrient(s);const starting=s.rest.cohorts[0].biomass;
 _=E.step(&s,params,env(1),1440).?;try check(s,c,n);try std.testing.expect(s.rest.cohorts[0].biomass<starting and M.biomass(s.active)==0);
 s.oxygen=0;const c0=Q.carbon(s);const n0=Q.nutrient(s);
 for(0..20*60)|_|{_=E.step(&s,params,env(0),1440).?;try check(s,c0,n0);try std.testing.expectEqual(@as(f64,0),s.oxygen);}
 try std.testing.expectEqual(@as(f32,0),M.biomass(s.active)+M.biomass(s.rest));try std.testing.expect(!Q.transfer(&s,false,0.01));
 for(0..120)|_|_=E.step(&s,params,env(1),1440).?;try std.testing.expectEqual(@as(f32,0),M.biomass(s.active)+M.biomass(s.rest));
}
test "sensitivity stable alternating dark and finite limited resources no forced winners"{
 for([_]f64{0.05,0.2,0.6})|rate|for([_]f64{1,0.5,0.25})|ratio|for(0..3)|habitat|for(0..2)|strategy|{
  var s=initial();if(habitat==2){s.air=0.05;s.oxygen=0.01;s.active.nutrient=0.005;}
  const c0=Q.carbon(s);const n0=Q.nutrient(s);const p=E.Parameters{.active_per_day=rate,.rest_per_day=rate*ratio,.unmet_stress_per_day=0.5};
  var paid:f64=0;var stress:f64=0;var rounding:f64=0;var fixed_proxy:f64=0;var entries:u32=0;var wakes:u32=0;var extinct=false;
  for(0..20*60)|tick|{
   const day=tick/60;const window=day>=2 and day%4>=2;
   // SAME prescribed transfer windows in stable and dark controls, not prophecy.
   if(strategy==1 and tick%60==0 and day>=2 and day%4==2){if(Q.transfer(&s,true,s.active.cohorts[0].biomass*0.5))entries+=1;}
   if(strategy==1 and tick%60==0 and day>=4 and day%4==0){if(Q.transfer(&s,false,s.rest.cohorts[0].biomass))wakes+=1;}
   const oldair=s.air;const r=E.step(&s,p,env(if(habitat>0 and window)0 else 1),1440).?;
   paid+=r.paid_active+r.paid_rest;stress+=r.dead_active+r.dead_rest;rounding+=r.retained_rounding;fixed_proxy+=oldair-s.air;
   try check(s,c0,n0);const living=M.biomass(s.active)+M.biomass(s.rest);try std.testing.expect(living<=1.0001);
   if(extinct)try std.testing.expectEqual(@as(f32,0),living);if(living==0)extinct=true;
   if(tick+1==240 or tick+1==600 or tick+1==1200)std.debug.print("ENERGY rate={d} ratio={d} habitat={d} strategy={d} day={d} active={d:.9} rest={d:.9} living={d:.9} detritus={d:.9} air={d:.9} oxygen={d:.9} maintenance={d:.9} stress_dead={d:.9} conversion={d:.9} entries={d} wakes={d} cutoff={d} net_atmospheric_draw={d:.9} carbon_error={e} nutrient_error={e}\n",.{rate,ratio,habitat,strategy,(tick+1)/60,M.biomass(s.active),M.biomass(s.rest),living,s.active.detritus+s.rest.detritus,s.air,s.oxygen,paid,stress,s.transition_respired,entries,wakes,s.cutoff_losses,fixed_proxy,Q.carbon(s)-c0,Q.nutrient(s)-n0});
  }
  std.debug.print("ENERGY_ROUNDING rate={d} ratio={d} habitat={d} strategy={d} retained_tissue_shortfall={e}\n",.{rate,ratio,habitat,strategy,rounding});
 };
}

test "common demand equal-pool allocation and numerical roundoff exposed"{
 var a=initial();try std.testing.expect(Q.transfer(&a,true,0.08));a.oxygen=0.0001;var b=a;
 std.mem.swap(M.Cohort,&b.active.cohorts[0],&b.rest.cohorts[0]);
 const equal=E.Parameters{.active_per_day=0.2,.rest_per_day=0.2,.unmet_stress_per_day=0.5};
 const ra=E.maintain(&a,equal,1440).?;const rb=E.maintain(&b,equal,1440).?;
 try std.testing.expectEqual(ra.paid_active,rb.paid_rest);try std.testing.expectEqual(ra.paid_rest,rb.paid_active);
 try std.testing.expectEqual(ra.dead_active,rb.dead_rest);try std.testing.expectEqual(ra.dead_rest,rb.dead_active);
 try std.testing.expectEqual(a.oxygen,b.oxygen);try std.testing.expect(ra.retained_rounding>=0);
 var rich=initial();const rr=E.maintain(&rich,params,1440).?;try std.testing.expectEqual(@as(f64,0),rr.unmet_fraction);try std.testing.expectEqual(@as(f64,0),rr.dead_active+rr.dead_rest);
}
test "slow active phenotype pays lower demand by lower real uptake capacity"{
 for([_]f64{0.25,0.5,1})|activity|for(0..3)|habitat|{
  var s=initial();if(habitat==2){s.air=0.05;s.oxygen=0.01;s.active.nutrient=0.005;}
  const c=Q.carbon(s);const n=Q.nutrient(s);const p=E.Parameters{.active_per_day=0.2*activity,.rest_per_day=0.2*activity,.unmet_stress_per_day=0.5,.uptake_fraction=activity};
  var paid:f64=0;var dead:f64=0;
  for(0..20*60)|tick|{
   const day=tick/60;const dark=habitat>0 and day>=2 and day%4>=2;
   const r=E.step(&s,p,env(if(dark)0 else 1),1440).?;paid+=r.paid_active+r.paid_rest;dead+=r.dead_active+r.dead_rest;try check(s,c,n);
   if(tick+1==120 or tick+1==240 or tick+1==600 or tick+1==1200)std.debug.print("SLOW_ACTIVE activity={d} habitat={d} day={d} living={d:.9} detritus={d:.9} maintenance={d:.9} stress_dead={d:.9} air={d:.9} oxygen={d:.9} carbon_error={e} nutrient_error={e}\n",.{activity,habitat,(tick+1)/60,M.biomass(s.active),s.active.detritus,paid,dead,s.air,s.oxygen,Q.carbon(s)-c,Q.nutrient(s)-n});
  }
 };
}
