//! Isolated controlled ecology probe, not production gameplay or natural-world proof.
const std=@import("std");const M=@import("simulation/microbes.zig");
const N=16;
const World=struct{
 cells:[N]M.Cell, air:[N]f64=.{10}**N, oxygen:[N]f64=.{10}**N,stats:M.Stats=.{},attempts:u64=0,blocked_full:u64=0,maxgen:u32=0,
 fn init(seed:u64)World{var w:World=undefined;w.air=.{10}**N;w.oxygen=.{10}**N;w.stats=.{};w.attempts=0;w.blocked_full=0;w.maxgen=0;
 for(&w.cells,0..)|*c,i|{c.*=M.initialized(seed+@as(u64,@intCast(i))*1009);c.nutrient=0.12;}
 w.air[0]-=M.seed(&w.cells[0],&w.stats,@floatCast(w.air[0]));return w;}
 fn carbon(w:*const World)f64{var n:f64=0;for(w.cells,w.air)|c,a|n+=@as(f64,M.carbon(c))+a;return n;}
 fn nutrient(w:*const World)f64{var n:f64=0;for(w.cells)|c|n+=M.nutrientTotal(c);return n;}
 fn sample(w:*const World,seed:u64,kind:u8,day:usize)void{var total:f64=0;var org:f64=0;var tough:f64=0;var feeding:f64=0;var cohorts:usize=0;var occupied:usize=0;var slots:usize=0;
 for(w.cells)|c|{if(M.biomass(c)>0)occupied+=1;var count:usize=0;for(c.cohorts)|v|{if(v.biomass>0){cohorts+=1;count+=1;total+=v.biomass;org+=@as(f64,v.biomass)*v.organization;tough+=@as(f64,v.biomass)*v.structure;feeding+=@as(f64,v.biomass)*v.feeding;}}if(count==4)slots+=1;}
 std.debug.print("seed={d} treatment={d} day={d} biomass={d:.6} occupied={d} cohorts={d} full_cells={d} organization={d:.5} structure={d:.5} feeding={d:.5} births={d} maxgen={d} attempts={d} blocked_full={d} carbon={d:.7} nutrient={d:.7}\n",.{seed,kind,day,total,occupied,cohorts,slots,org/@max(total,1e-20),tough/@max(total,1e-20),feeding/@max(total,1e-20),w.stats.births,w.maxgen,w.attempts,w.blocked_full,w.carbon(),w.nutrient()});}
};
fn run(seed:u64,kind:u8,reverse:bool)!void{
 var w=World.init(seed);const carbon=w.carbon();const nutrient=w.nutrient();
 for(0..180*60)|tick|{
  const day=tick/60;
  // Day60 partial patch-clearing event: paid carbon becomes detritus, nutrients released.
  if(tick==60*60 and kind==1){for(&w.cells,0..)|*cell,i|{if(i%3!=0)continue;for(&cell.cohorts)|*co|{cell.detritus+=co.biomass;cell.nutrient+=co.biomass*M.nutrient_per_carbon;co.*=.{};}}}
  for(0..N)|k|{const i=if(reverse) N-1-k else k;const flux=M.step(&w.cells[i],.{.temperature=303,.depth_km=if((kind==2 or kind==4) and day>=60 and day<63)0.00008 else 0.001,.light=if(tick%60<30)1 else 0,.carbon_available=@floatCast(w.air[i]),.oxygen_carbon_capacity=@floatCast(w.oxygen[i])},1440);
   w.air[i]+=@as(f64,flux.recycled)-flux.fixed;w.oxygen[i]+=@as(f64,flux.fixed)-flux.recycled;
   try std.testing.expect(M.validCell(w.cells[i],w.stats.next_lineage));try std.testing.expect(w.air[i]>=-1e-6 and w.oxygen[i]>=-1e-6);
  }
  // Every six hours, offer each pre-existing cohort one neighbor; no same-pass chain.
  if(tick%15==14 and !(kind==4 and day>=60 and day<63)){const before=w.stats.next_lineage;for(0..N)|k|{const i=if(reverse)N-1-k else k;for(0..4)|j|{if(w.cells[i].cohorts[j].biomass==0 or w.cells[i].cohorts[j].lineage>=before)continue;const dest=if((tick/15)%2==0)(i+1)%N else (i+N-1)%N;w.attempts+=1;
    var full=true;for(w.cells[dest].cohorts)|c|{if(c.biomass==0)full=false;}if(full)w.blocked_full+=1;
    _=M.reproduce(&w.cells[i],j,&w.cells[dest],&w.stats,kind!=3);
   }}}
  for(w.cells)|cell|for(cell.cohorts)|co|{w.maxgen=@max(w.maxgen,co.generation);};
  try std.testing.expectApproxEqAbs(carbon,w.carbon(),0.001);try std.testing.expectApproxEqAbs(nutrient,w.nutrient(),0.001);
  if((tick+1)%60==0){const d=(tick+1)/60;if(d==30 or d==60 or d==63 or d==100 or d==180)w.sample(seed,kind,d);}
 }
}
test "paid multigeneration succession probe with resource ledger and reset contrasts"{
 for([_]u64{42,1337,2027})|seed|for(0..5)|kind|try run(seed,@intCast(kind),false);
 std.debug.print("REVERSE_ORDER_CONTROL\n",.{});try run(42,0,true);
}
