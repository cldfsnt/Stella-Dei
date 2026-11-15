const std=@import("std");const Q=@import("experimental/quiescence.zig");const M=@import("simulation/microbes.zig");
fn initial()Q.State{var s=Q.State{.active=M.initialized(42),.rest=M.initialized(43)};s.active.cohorts[0]=.{.biomass=0.2,.lineage=1};s.active.nutrient=0.1;s.rest.nutrient=0;return s;}
fn env(temp:f32,depth:f32)M.Environment{return .{.temperature=temp,.depth_km=depth,.light=1,.carbon_available=0,.oxygen_carbon_capacity=0};}
fn check(s:Q.State,c:f64,n:f64)!void{try std.testing.expect(Q.valid(s));try std.testing.expectApproxEqAbs(c,Q.carbon(s),0.0001);try std.testing.expectApproxEqAbs(n,Q.nutrient(s),0.00001);}
test "paid pool transfers no oxygen refusal invalid zero lineage and no resurrection"{
 var s=initial();const c=Q.carbon(s);const n=Q.nutrient(s);
 try std.testing.expect(Q.transfer(&s,true,0.1));try check(s,c,n);try std.testing.expect(s.rest.cohorts[0].biomass<0.1);
 try std.testing.expect(Q.transfer(&s,false,s.rest.cohorts[0].biomass));try check(s,c,n);
 s.oxygen=0;const before=s;try std.testing.expect(!Q.transfer(&s,true,0.01));try std.testing.expectEqualDeep(before,s);
 s=initial();s.active.cohorts[0].lineage=0;const bad=s;try std.testing.expect(!Q.transfer(&s,true,0.1));try std.testing.expect(!Q.step(&s,env(303,0.001),1440));try std.testing.expectEqualDeep(bad,s);
 s=initial();s.active.cohorts[0]=.{};try std.testing.expect(!Q.transfer(&s,false,0.01));for(0..200)|_|try std.testing.expect(Q.step(&s,env(303,0.001),1440));try std.testing.expectEqual(@as(f32,0),M.biomass(s.active)+M.biomass(s.rest));
}
test "null resting ecology stable intermittent dry heat oxygen and nutrient controls"{
 for(0..6)|habitat|for(0..2)|resting|{
  var s=initial();if(habitat==4)s.oxygen=0;if(habitat==5)s.active.nutrient=0;const c=Q.carbon(s);const n=Q.nutrient(s);var entered=false;var woke=false;
  // Resting strategy is fixed experimental assignment, NOT inherited evolution.
  if(resting==1)entered=Q.transfer(&s,true,0.1);
  for(0..30*60)|tick|{
   const day=tick/60;const dry=habitat==2 or (habitat==1 and day>=2 and day<5);
   const t:f32=if(habitat==3)400 else 303;
   if(day==5 and resting==1 and habitat==1 and !woke){woke=Q.transfer(&s,false,s.rest.cohorts[0].biomass);}
   try std.testing.expect(Q.step(&s,env(t,if(dry)0 else 0.001),1440));try check(s,c,n);
   try std.testing.expect(M.biomass(s.active)+M.biomass(s.rest)<=1.00001);
   if(tick+1==120 or tick+1==300 or tick+1==1800)std.debug.print("QUIESCENCE habitat={d} resting={d} day={d} active={d:.9} rest={d:.9} detritus={d:.9} air={d:.9} oxygen={d:.9} transition_cost={d:.9} entered={} woke={} cutoff_losses={d} carbon_error={e} nutrient_error={e}\n",.{habitat,resting,(tick+1)/60,M.biomass(s.active),M.biomass(s.rest),s.active.detritus+s.rest.detritus,s.air,s.oxygen,s.transition_respired,entered,woke,s.cutoff_losses,Q.carbon(s)-c,Q.nutrient(s)-n});
  }
 };
}
test "small active pool cutoff is exposed not magically restored"{
 var s=initial();const c=Q.carbon(s);const n=Q.nutrient(s);try std.testing.expect(Q.transfer(&s,true,0.198));
 try std.testing.expect(Q.step(&s,env(303,0.001),1440));try check(s,c,n);
 try std.testing.expectEqual(@as(f32,0),M.biomass(s.active));try std.testing.expect(M.biomass(s.rest)>0 and s.cutoff_losses==1);
 // Waking funded by genuinely living resting tissue, never by cleared active ID.
 const before=Q.carbon(s);try std.testing.expect(Q.transfer(&s,false,0.02));try std.testing.expectApproxEqAbs(before,Q.carbon(s),1e-6);
}
test "zero oxygen in darkness remains finite and cannot pay waking"{
 var s=initial();try std.testing.expect(Q.transfer(&s,true,0.1));s.oxygen=0;const c=Q.carbon(s);const n=Q.nutrient(s);var e=env(303,0.001);e.light=0;
 for(0..600)|_|{try std.testing.expect(Q.step(&s,e,1440));try check(s,c,n);try std.testing.expectEqual(@as(f64,0),s.oxygen);}
 const before=s;try std.testing.expect(!Q.transfer(&s,false,0.01));try std.testing.expectEqualDeep(before,s);
}

test "combined capacity and mismatched same-lineage phenotypes refuse atomically"{
 var s=initial();s.active.cohorts[0].biomass=0.7;s.rest.cohorts[0]=s.active.cohorts[0];const full=s;
 try std.testing.expect(!Q.step(&s,env(303,0.001),1440));try std.testing.expectEqualDeep(full,s);
 s=initial();try std.testing.expect(Q.transfer(&s,true,0.1));s.rest.cohorts[0].efficiency=1.1;const mismatch=s;
 try std.testing.expect(!Q.transfer(&s,false,0.01));try std.testing.expect(!Q.step(&s,env(303,0.001),1440));try std.testing.expectEqualDeep(mismatch,s);
}
