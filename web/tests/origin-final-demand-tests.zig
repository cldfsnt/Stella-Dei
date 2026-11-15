const std=@import("std");const M=@import("microbes.zig");const R=@import("microbes_law2_reference.zig");const F=@import("final_demand.zig");
fn c0() M.Cohort{return .{.biomass=0.1,.support_mass=0.004,.organization=0.04,.structure=0.1,.root_fraction=0.25,.lineage=42};}
fn environment(depth:f32)M.Environment{return .{.temperature=303,.depth_km=depth,.light=1,.carbon_available=1,.oxygen_carbon_capacity=1,.immersion_physiology=true,.final_demand_physiology=true};}
test "drying final demand lowers funded fraction and wetting cannot create credit" {
 const c=c0();var pre=environment(0.00000099);var post=environment(0.000000175);const dp=M.rootDemand(c,pre,1440);const df=M.rootDemand(c,post,1440);try std.testing.expect(df>dp and dp>0);
 const credit=dp*0.25;post.root_credit[0]=credit;post.root_owner[0]=42;
 const h=M.fundedHydration(c,post,1440,0,df);try std.testing.expect(h<0.25);try std.testing.expect(@as(f128,h)*@as(f128,df)<=@as(f128,credit));
 pre.root_credit=post.root_credit;pre.root_owner=post.root_owner;const same=M.fundedHydration(c,pre,1440,0,dp);try std.testing.expectEqual(F.signal(credit,42,42,dp),same);
 var wet=post;wet.depth_km=0.0001;try std.testing.expectEqual(@as(f32,0),M.fundedHydration(c,wet,1440,0,df));
 var replacement=c;replacement.lineage=43;try std.testing.expectEqual(@as(f32,0),M.fundedHydration(replacement,post,1440,0,df));replacement.lineage=0;try std.testing.expectEqual(@as(f32,0),M.fundedHydration(replacement,post,1440,0,df));
 post.root_credit[0]=0;try std.testing.expectEqual(@as(f32,0),M.fundedHydration(c,post,1440,0,df));
}
test "conservative ratios invalid states and one interval demand ceiling" {
 for([_]f64{1e-300,1e-20,0.001,1,1e100})|d|for([_]f64{0,0.0001,0.25,1,2})|ratio|{const credit=d*ratio;const h=F.signal(credit,42,42,d);try std.testing.expect(@as(f128,h)*@as(f128,d)<=@as(f128,credit));};
 for([_]f64{0,-1,std.math.nan(f64),std.math.inf(f64)})|bad|{try std.testing.expectEqual(@as(f32,0),F.signal(1,42,42,bad));try std.testing.expectEqual(@as(f32,0),F.signal(bad,42,42,1));}
 const c=c0();var e=environment(0);const demand=M.rootDemand(c,e,1440);e.root_credit[0]=demand*0.25;e.root_owner[0]=42;
 const h=M.fundedHydration(c,e,1440,0,demand*2);try std.testing.expect(h<=0.125);try std.testing.expect(@as(f128,h)*@as(f128,demand*2)<=@as(f128,e.root_credit[0]));
 for([_]f32{273.15,355,std.math.nan(f32)})|t|{e.temperature=t;try std.testing.expectEqual(@as(f64,0),M.rootDemand(c,e,1440));}
 e=environment(0);for([_]f32{-1,0.0002,0.051,std.math.nan(f32)})|d|{e.depth_km=d;try std.testing.expectEqual(@as(f64,0),M.rootDemand(c,e,1440));}
}
test "law1 and law2 complete cells and RNG exactly equal original core" {
 for([_]bool{false,true})|immersion|for([_]f32{0,0.000001,0.0001,0.0002,0.01,0.051})|depth|for([_]f32{260,273.15,303,355})|temp|{
 var e=environment(depth);e.immersion_physiology=immersion;e.final_demand_physiology=false;e.temperature=temp;e.root_hydration=.{0.25,0,0,0};var a=M.initialized(42);a.cohorts[0]=c0();var b=R.initialized(42);inline for(std.meta.fields(M.Cohort))|f|{@field(b.cohorts[0],f.name)=@field(a.cohorts[0],f.name);}var re:R.Environment=undefined;inline for(std.meta.fields(R.Environment))|f|{@field(re,f.name)=@field(e,f.name);}
 _=M.step(&a,e,1440);_=R.step(&b,re,1440);const ab=try std.json.stringifyAlloc(std.testing.allocator,a,.{});defer std.testing.allocator.free(ab);const bb=try std.json.stringifyAlloc(std.testing.allocator,b,.{});defer std.testing.allocator.free(bb);try std.testing.expectEqualStrings(ab,bb);
 };
}
