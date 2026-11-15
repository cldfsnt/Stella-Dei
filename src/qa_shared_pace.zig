const std=@import("std");const E=@import("experimental/shared_pace.zig");const M=E.M;
fn initial(crowded:bool,limited:bool)E.State{var s=E.State{.cell=M.initialized(42)};s.cell.cohorts[0]=.{.lineage=1,.biomass=if(crowded)0.4 else 0.1};s.cell.cohorts[1]=.{.lineage=2,.biomass=if(crowded)0.4 else 0.1};s.cell.nutrient=if(limited)0.005 else 0.1;if(limited){s.air=0.05;s.oxygen=0.01;}return s;}
test "shared pace matrix paired slots complete cycles and recovery"{
 for([_]f64{0,0.05,0.2,0.6})|rate|for([_]f32{1,0.5,0.25})|slow|for(0..3)|habitat|for(0..2)|crowded|{
 var a=initial(crowded==1,habitat==2);var b=a;std.mem.swap(M.Cohort,&b.cell.cohorts[0],&b.cell.cohorts[1]);const c0=E.carbon(a);const n0=E.nutrient(a);var maxc:f64=0;var maxn:f64=0;var maxswap:f64=0;var rounding:f64=0;var paid=[_]f64{0,0};var dead=[_]f64{0,0};
 for(0..24*60)|tick|{const day=tick/60;const dark=habitat>0 and day<20 and day%4>=2;const ra=E.step(&a,.{slow,1,1,1},rate,if(dark)0 else 1,1440).?;_=E.step(&b,.{1,slow,1,1},rate,if(dark)0 else 1,1440).?;
 maxc=@max(maxc,@abs(E.carbon(a)-c0));maxn=@max(maxn,@abs(E.nutrient(a)-n0));rounding+=ra.rounding;
 for(0..2)|i|{paid[i]+=ra.paid[i];dead[i]+=ra.dead[i];maxswap=@max(maxswap,@abs(@as(f64,a.cell.cohorts[i].biomass)-b.cell.cohorts[1-i].biomass));}
 try std.testing.expect(maxc<0.0001 and maxn<0.00001);try std.testing.expect(maxswap<0.00001);try std.testing.expect(M.biomass(a.cell)<=1.0001);
 if(tick+1==120 or tick+1==240 or tick+1==1200 or tick+1==1440)std.debug.print("PACE rate={d} slow={d} habitat={d} crowded={d} day={d} slow_mass={d} fast_mass={d} slow_paid={d} fast_paid={d} slow_stress={d} fast_stress={d} air={d} oxygen={d} nutrient={d} max_carbon_error={e} max_nutrient_error={e} max_swap={e} rounding={e}\n",.{rate,slow,habitat,crowded,(tick+1)/60,a.cell.cohorts[0].biomass,a.cell.cohorts[1].biomass,paid[0],paid[1],dead[0],dead[1],a.air,a.oxygen,a.cell.nutrient,maxc,maxn,maxswap,rounding});
 }
 };
}
test "invalid inputs atomic and zero O2 no maintenance creation"{var s=initial(false,false);const original=s;try std.testing.expect(E.step(&s,.{0,1,1,1},0.2,1,1440)==null);try std.testing.expectEqualDeep(original,s);s.oxygen=0;const r=E.step(&s,.{0.5,1,1,1},0.2,0,1440).?;try std.testing.expectEqual(@as(f64,0),r.paid[0]+r.paid[1]);try std.testing.expectEqual(@as(f64,1),r.unmet);try std.testing.expectEqual(@as(f64,0),s.oxygen);}
test "generated unpaced core identical to production control"{const P=@import("simulation/microbes.zig");var a=initial(false,false).cell;var b:P.Cell=undefined;inline for(std.meta.fields(P.Cell))|f|{@field(b,f.name)=if(comptime std.mem.eql(u8,f.name,"cohorts")) blk:{var co:[4]P.Cohort=undefined;for(a.cohorts,0..)|v,i|{inline for(std.meta.fields(P.Cohort))|cf|@field(co[i],cf.name)=@field(v,cf.name);}break :blk co;} else @field(a,f.name);}
 const e=M.Environment{.temperature=303,.depth_km=0.001,.light=1,.carbon_available=10,.oxygen_carbon_capacity=10};const pe=P.Environment{.temperature=303,.depth_km=0.001,.light=1,.carbon_available=10,.oxygen_carbon_capacity=10};
 _=M.step(&a,e,1440);_=P.step(&b,pe,1440);try std.testing.expectEqual(a.nutrient,b.nutrient);for(a.cohorts,b.cohorts)|x,y|try std.testing.expectEqual(x.biomass,y.biomass);
}
