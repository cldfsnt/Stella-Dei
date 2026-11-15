const std=@import("std");const M=@import("microbes.zig");const R=@import("microbes_law3_reference.zig");
fn cohort()M.Cohort{return .{.lineage=42,.biomass=0.1,.support_mass=0.004,.organization=0.1,.root_fraction=0.25,.structure=0.1};}
fn environment(depth:f32)M.Environment{return .{.temperature=303,.depth_km=depth,.light=1,.carbon_available=1,.oxygen_carbon_capacity=1,.immersion_physiology=true,.final_demand_physiology=true};}
test "exposed funding composition endpoints and partial immersion"{
 for([_]f32{0,0.25,0.5,1})|i|{try std.testing.expectEqual(i,M.composedGrowthHabitat(0,i,0));try std.testing.expectEqual(@as(f32,1),M.composedGrowthHabitat(0,i,1));}
 try std.testing.expectEqual(@as(f32,0.6),M.composedGrowthHabitat(0,0.5,0.2));try std.testing.expectEqual(@as(f32,0.8),M.composedGrowthHabitat(0.8,0.5,0.2));
}
test "historical law3 and earlier cells flux RNG exactly unchanged"{
 for([_]bool{false,true})|immersion|for([_]bool{false,true})|final|for([_]f32{0,0.000001,0.0001,0.0002,0.01,0.051})|depth|for([_]f32{260,273.15,303,355})|temp|{
 var e=environment(depth);e.temperature=temp;e.immersion_physiology=immersion;e.final_demand_physiology=final;e.root_credit[0]=0.0001;e.root_owner[0]=42;e.root_hydration[0]=0.25;var a=M.initialized(42);a.cohorts[0]=cohort();var b=R.initialized(42);inline for(std.meta.fields(M.Cohort))|f|{@field(b.cohorts[0],f.name)=@field(a.cohorts[0],f.name);}var re:R.Environment=undefined;inline for(std.meta.fields(R.Environment))|f|{@field(re,f.name)=@field(e,f.name);}const af=M.step(&a,e,1440);const bf=R.step(&b,re,1440);
 const ab=try std.json.stringifyAlloc(std.testing.allocator,.{a,af},.{});defer std.testing.allocator.free(ab);const bb=try std.json.stringifyAlloc(std.testing.allocator,.{b,bf},.{});defer std.testing.allocator.free(bb);try std.testing.expectEqualStrings(ab,bb);
 };
}
test "law4 obeys ownership invalid habitat and resource limits"{
 const c=cohort();var e=environment(0.000001);e.composed_growth_physiology=true;e.root_credit[0]=M.rootDemand(c,e,1440);e.root_owner[0]=41;try std.testing.expectEqual(@as(f32,0),M.fundedHydration(c,e,1440,0,0));e.root_owner[0]=42;
 for([_]f32{273.15,355,std.math.nan(f32)})|t|{e.temperature=t;try std.testing.expectEqual(@as(f32,0),M.geometricImmersion(c,e.depth_km,t));try std.testing.expectEqual(@as(f64,0),M.rootDemand(c,e,1440));}
 for(0..3)|which|{e=environment(0.000001);e.composed_growth_physiology=true;e.root_credit[0]=0.0001;e.root_owner[0]=42;var a=M.initialized(42);a.cohorts[0]=c;a.nutrient=1;if(which==0)e.light=0;if(which==1)e.carbon_available=0;if(which==2){a.nutrient=0;e.oxygen_carbon_capacity=0;}const before=M.carbon(a);const flux=M.step(&a,e,1440);if(which<2)try std.testing.expectEqual(@as(f32,0),flux.fixed);try std.testing.expect(M.carbon(a)<=before+flux.fixed+0.000001);}
}
test "real step uses partial paid exposure without changing mortality or water receipt"{
 var e=environment(0);const c=cohort();e.depth_km=@floatCast(@as(f64,M.producerHeightMeters(c))*0.5/1000);const demand=M.rootDemand(c,e,1440);try std.testing.expect(demand>0);e.root_credit[0]=demand*0.2;e.root_owner[0]=42;
 var old=M.initialized(42);old.cohorts[0]=c;old.nutrient=1;var newer=old;const prior=M.step(&old,e,1440);e.composed_growth_physiology=true;const next=M.step(&newer,e,1440);try std.testing.expect(next.fixed>prior.fixed);try std.testing.expectEqual(prior.recycled,next.recycled);try std.testing.expectEqual(old.detritus,newer.detritus);try std.testing.expectEqual(old.rng,newer.rng);try std.testing.expectEqual(demand*0.2,e.root_credit[0]);
 for([_]f32{0,e.depth_km,0.0001,0.0002,0.01,0.051})|depth|{e.depth_km=depth;e.root_credit[0]=0;e.composed_growth_physiology=false;var a=M.initialized(42);a.cohorts[0]=c;a.nutrient=1;var b=a;const af=M.step(&a,e,1440);e.composed_growth_physiology=true;const bf=M.step(&b,e,1440);try std.testing.expectEqualDeep(a,b);try std.testing.expectEqualDeep(af,bf);}
}
