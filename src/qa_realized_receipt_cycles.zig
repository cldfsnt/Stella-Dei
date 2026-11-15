const std=@import("std");const E=@import("experimental/realized_receipt_pace.zig");const M=E.M;
test "preregistered exposure duration and reciprocal rarity finite shared resources"{
 for(0..2)|limited|for([_]f32{0.05,0.5,0.95})|fraction|for([_]f32{1,0.5})|pace|for([_]usize{0,2,8,24})|period|{
 var a=E.State{.cell=M.initialized(42),.air=if(limited==1)0.05 else 10,.oxygen=if(limited==1)0.01 else 10};a.cell.nutrient=if(limited==1)0.005 else 0.1;a.cell.cohorts[0]=.{.lineage=1,.biomass=0.2*fraction};a.cell.cohorts[1]=.{.lineage=2,.biomass=0.2-a.cell.cohorts[0].biomass};
 try std.testing.expect(a.cell.cohorts[0].biomass>=0.0025 and a.cell.cohorts[1].biomass>=0.0025 and M.validCell(a.cell,3));var b=a;std.mem.swap(M.Cohort,&b.cell.cohorts[0],&b.cell.cohorts[1]);const c0=E.carbon(a);const n0=E.nutrient(a);var maxc:f64=0;var maxn:f64=0;var swap:f64=0;var paid=[_]f64{0,0};var extinct=[_]i32{-1,-1};var rounding:f64=0;var light_ticks:usize=0;
 for(0..56*60)|tick|{const day=tick/60;const dark=period>0 and day<48 and day%period>=period/2;if(!dark)light_ticks+=1;
 const r=E.step(&a,.{pace,1,1,1},0.2,if(dark)0 else 1,1440).?;_=E.step(&b,.{1,pace,1,1},0.2,if(dark)0 else 1,1440).?;rounding+=r.rounding;
 maxc=@max(maxc,@abs(E.carbon(a)-c0));maxn=@max(maxn,@abs(E.nutrient(a)-n0));for(0..2)|i|{paid[i]+=r.paid[i];swap=@max(swap,@abs(@as(f64,a.cell.cohorts[i].biomass)-b.cell.cohorts[1-i].biomass));if(a.cell.cohorts[i].biomass==0 and extinct[i]<0)extinct[i]=@intCast(tick+1);if(extinct[i]>=0)try std.testing.expect(a.cell.cohorts[i].biomass==0);}
 if(!(maxc<0.0001 and maxn<0.00001 and swap<0.00001))std.debug.print("CYCLES_FAILURE tick={d} initial_c={e} current_c={e} initial_n={e} current_n={e} max_c={e} max_n={e} swap={e}\n",.{tick+1,c0,E.carbon(a),n0,E.nutrient(a),maxc,maxn,swap});
 try std.testing.expect(maxc<0.0001 and maxn<0.00001 and swap<0.00001);
 const end=tick+1;const complete=period>0 and end<=48*60 and end%(period*60)==0;
 if(complete or end==48*60 or end==56*60){const mass=M.biomass(a.cell);std.debug.print("CYCLES limited={d} initial_slow_fraction={d} slow_pace={d} period={d} day={d} light_days={d} slow_mass={d} fast_mass={d} slow_fraction={d} slow_paid={d} fast_paid={d} extinct_slow_tick={d} extinct_fast_tick={d} max_c={e} max_n={e} max_swap={e} rounding={e}\n",.{limited,fraction,pace,period,end/60,@as(f64,@floatFromInt(light_ticks))/60,a.cell.cohorts[0].biomass,a.cell.cohorts[1].biomass,if(mass>0)a.cell.cohorts[0].biomass/mass else 0,paid[0],paid[1],extinct[0],extinct[1],maxc,maxn,swap,rounding});}
 }
 };
}
