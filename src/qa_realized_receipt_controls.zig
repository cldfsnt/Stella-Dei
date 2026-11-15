const std=@import("std");const E=@import("experimental/realized_receipt_pace.zig");const M=E.M;
test "prior four neutral 48day failures with unchanged C N oxygen ledgers"{
 for([_]bool{false,true})|crowded|for(0..2)|swap|{var s=E.State{.cell=M.initialized(42)};for(0..2)|i|s.cell.cohorts[i^swap]=.{.lineage=i+1,.biomass=if(crowded)0.4 else 0.02};s.air=10.8-M.carbon(s.cell);s.cell.nutrient=@floatCast(0.18-@as(f64,M.biomass(s.cell))*M.nutrient_per_carbon);const c0=E.carbon(s);const n0=E.nutrient(s);const gases=s.air+s.oxygen;var mc:f64=0;var mn:f64=0;for(0..2880)|_|{_=E.step(&s,.{1,1,1,1},0.2,1,1440).?;mc=@max(mc,@abs(E.carbon(s)-c0));mn=@max(mn,@abs(E.nutrient(s)-n0));try std.testing.expect(mc<1e-4 and mn<1e-5);try std.testing.expectApproxEqAbs(gases,s.air+s.oxygen,1e-10);}std.debug.print("RECEIPT_CONTROL crowded={} swap={d} maxC={e} maxN={e} gas_balance={e}\n",.{crowded,swap,mc,mn,s.air+s.oxygen-gases});};
}
test "actual earned credit cannot exceed actual fixation receipt"{
 for(0..10000)|i|{var c=M.initialized(42);c.cohorts[0]=.{.lineage=1,.biomass=0.02,.reproduction_credit=0.00001+@as(f32,@floatFromInt(i))*0.00001};const old=c.cohorts[0].reproduction_credit;const f=M.step(&c,.{.temperature=303,.depth_km=0.001,.light=1,.carbon_available=1,.oxygen_carbon_capacity=1},1440);const credited=@as(f64,c.cohorts[0].reproduction_credit)-old;if(credited>@as(f64,f.fixed)){std.debug.print("CREDIT_BUDGET_FAILURE i={d} old={e} actual_credit={e} fixation={e} excess={e}\n",.{i,old,credited,f.fixed,credited-f.fixed});try std.testing.expect(false);}}
}
test "tiny represented nutrient store cannot silently fund uncharged net tissue"{
 for([_]f32{0.0001,0.001,0.01,0.1,1})|seconds|for([_]f32{0.1,0.5,1})|light|{var c=M.initialized(42);c.cohorts[0]=.{.lineage=1,.biomass=0.02};const before=c;const f=M.step(&c,.{.temperature=303,.depth_km=0.001,.light=light,.carbon_available=1,.oxygen_carbon_capacity=1},seconds);const gain=@as(f64,c.cohorts[0].biomass)-before.cohorts[0].biomass;
 if(gain>0 and c.nutrient==before.nutrient){std.debug.print("TINY_N_FAILURE seconds={d} light={d} represented_net_gain={e} nutrient_before={e} nutrient_after={e} fixed={e}\n",.{seconds,light,gain,before.nutrient,c.nutrient,f.fixed});try std.testing.expect(false);}};
}
test "support receiver growth stays within represented paid organization budget"{
 for([_]f32{0,0.000001,0.03,0.1})|support|for([_]f32{0,0.01,0.5,1})|organization|{
 var c=M.initialized(42);c.cohorts[0]=.{.lineage=1,.biomass=0.2,.support_mass=support,.organization=organization};var dark=c;const env=M.Environment{.temperature=303,.depth_km=0.001,.light=1,.carbon_available=1,.oxygen_carbon_capacity=1};var denv=env;denv.light=0;denv.carbon_available=0;_=M.step(&dark,denv,1440);const f=M.step(&c,env,1440);const gained=@as(f64,c.cohorts[0].support_mass)-dark.cohorts[0].support_mass;try std.testing.expect(gained<=@as(f64,f.fixed)*organization);try std.testing.expect(c.cohorts[0].support_mass<=c.cohorts[0].biomass);
 };
}
test "aggregate oxygen and fixation capacity boundaries"{
 var failures:usize=0;
 for([_]f32{0,0.000000000001,0.00000001,0.00001,0.01,1})|oxygen|for([_]f32{0.0001,0.01,1,1440,86400,864000})|elapsed|{
 var c=M.initialized(42);for(&c.cohorts,0..)|*co,i|co.*=.{.lineage=i+1,.biomass=0.2,.support_mass=0.1,.organization=0.5};const f=M.step(&c,.{.temperature=303,.depth_km=0.001,.light=1,.carbon_available=oxygen,.oxygen_carbon_capacity=oxygen},elapsed);
 if(f.recycled>oxygen or f.fixed>oxygen){failures+=1;std.debug.print("AGGREGATE_BOUND_FAILURE oxygen={e} dt={e} recycled={e} fixed={e}\n",.{oxygen,elapsed,f.recycled,f.fixed});}
 };
 std.debug.print("AGGREGATE_BOUND failures={d}\n",.{failures});try std.testing.expectEqual(@as(usize,0),failures);
}
