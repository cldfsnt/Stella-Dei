//! Controlled transfer precision; no natural evolution or establishment claim.
const std=@import("std");const M=@import("simulation/microbes.zig");const D=@import("experimental/directed_sample.zig");
fn fixture(mass:f32,support:f32,credit:f32)[2]M.Cell{
 var c=[_]M.Cell{.{},.{}};c[0].cohorts[0]=.{.biomass=mass,.support_mass=support,.reproduction_credit=credit,.lineage=1,.parent=0,.generation=7,.structure=0.4,.organization=0.3,.efficiency=0.9,.feeding=0.1,.mobility=0.2,.lifetime_grazed=0.2,.relocations=2,.last_from=3,.last_to=0,.last_move_time=100};return c;
}
fn totalMass(cells:[2]M.Cell)f64{var n:f64=0;for(cells)|c|{n+=c.detritus;for(c.cohorts)|co|n+=co.biomass;}return n;}
fn totalSupport(cells:[2]M.Cell)f64{var n:f64=0;for(cells)|c|for(c.cohorts)|co|{n+=co.support_mass;};return n;}
test "measure actual production rounding and conservative no-mutation transfer"{
 var minted:f64=0;var lost:f64=0;var ok:usize=0;var refused:usize=0;
 for(0..10000)|i|{
  const x:f32=0.03+@as(f32,@floatFromInt(i))*0.000096;
  const initial=fixture(x,x*0.35,0.2);var old=initial;var os=M.Stats{.next_lineage=2};
  try std.testing.expect(M.reproduce(&old[0],0,&old[1],&os,false));
  const err=totalMass(old)-totalMass(initial);if(err>0)minted=@max(minted,err)else lost=@max(lost,-err);
  var c=initial;var stats=M.Stats{.next_lineage=2};const receipt=D.apply(&c,&stats,0,0,1,1,9,9,&.{1});
  if(!receipt.ok){refused+=1;try std.testing.expectEqualDeep(initial,c);continue;}ok+=1;
  try std.testing.expectEqual(totalMass(initial),totalMass(c));try std.testing.expectEqual(totalSupport(initial),totalSupport(c));
  try std.testing.expectEqual(initial[0].nutrient,c[0].nutrient);try std.testing.expectEqual(initial[1].nutrient,c[1].nutrient);
  try std.testing.expectEqual(initial[0].rng,c[0].rng);try std.testing.expectEqual(initial[1].rng,c[1].rng);
  try std.testing.expectEqual(@as(f64,initial[0].cohorts[0].biomass)-c[0].cohorts[0].biomass,receipt.mass);
  try std.testing.expect(receipt.mass<=@as(f64,@as(f32,0.01)) and receipt.credit>=@as(f64,@as(f32,0.04)));
  const child=c[1].cohorts[0];try std.testing.expect(child.lineage==2 and child.parent==1 and child.generation==8 and child.reproduction_credit==0 and child.lifetime_grazed==0 and child.relocations==0);
  try std.testing.expectEqual(initial[0].cohorts[0].structure,child.structure);try std.testing.expectEqual(initial[0].cohorts[0].organization,child.organization);try std.testing.expectEqual(initial[0].cohorts[0].efficiency,child.efficiency);
 }
 try std.testing.expect(ok>0 and minted>0 and lost>0);
 std.debug.print("DIRECTED_PRECISION cases=10000 accepted={d} refused={d} production_max_created_C={e} production_max_lost_C={e} candidate_exact_represented_C_support=true free_nutrient_unchanged=true no_rng_draw=true\n",.{ok,refused,minted,lost});
}
test "refusals leave all cells RNG stats unchanged"{
 const original=fixture(0.1,0.02,0.2);
 for(0..10)|kind|{
  var c=original;var stats=M.Stats{.next_lineage=2};var from:usize=0;var to:usize=1;var slot:usize=0;var id:u64=1;var world:u32=9;var adjacent=true;
  switch(kind){0=>id=8,1=>world=8,2=>from=3,3=>to=3,4=>to=0,5=>slot=4,6=>adjacent=false,7=>c[0].cohorts[0].reproduction_credit=0,8=>{for(&c[1].cohorts,0..)|*co,i|co.*=.{.biomass=0.1,.lineage=@intCast(i+2)};stats.next_lineage=6;},9=>stats.next_lineage=std.math.maxInt(u64),else=>unreachable}
  const before=c;const bs=stats;const r=D.apply(&c,&stats,from,slot,to,id,world,9,if(adjacent)&.{1}else &.{});
  try std.testing.expect(!r.ok);try std.testing.expectEqualDeep(before,c);try std.testing.expectEqualDeep(bs,stats);
 }
}
test "zero full and near-full support plus precision refusals"{
 for([_]f32{0,0.0000001,0.35,0.9999999,1})|fraction|{
  var c=fixture(0.1,0.1*fraction,0.2);const before=c;var s=M.Stats{.next_lineage=2};
  const r=D.apply(&c,&s,0,0,1,1,1,1,&.{1});try std.testing.expect(r.ok);
  try std.testing.expectEqual(totalMass(before),totalMass(c));try std.testing.expectEqual(totalSupport(before),totalSupport(c));
  var expected=before[0].cohorts[0];expected.biomass=c[1].cohorts[0].biomass;expected.support_mass=c[1].cohorts[0].support_mass;expected.lineage=2;expected.parent=1;expected.generation=8;expected.reproduction_credit=0;expected.lifetime_grazed=0;expected.relocations=0;expected.last_from=0;expected.last_to=0;expected.last_move_time=0;
  try std.testing.expectEqualDeep(expected,c[1].cohorts[0]);
 }
 for(0..5)|kind|{
  var c=fixture(0.1,0.03,0.2);var s=M.Stats{.next_lineage=2};
  switch(kind){0=>c[0].cohorts[0].biomass=std.math.nan(f32),1=>c[0].cohorts[0].biomass=0.02,2=>c[0].cohorts[0].reproduction_credit=1e8,3=>s.births=std.math.maxInt(u64),4=>c[1].cohorts[0]=.{.biomass=0.995,.lineage=2},else=>unreachable}
  if(kind==4)s.next_lineage=3;
  const before=c;const bs=s;const r=D.apply(&c,&s,0,0,1,1,1,1,&.{1});try std.testing.expect(!r.ok);
  try std.testing.expectEqualSlices(u8,std.mem.asBytes(&before),std.mem.asBytes(&c));try std.testing.expectEqualDeep(bs,s);
 }
}
test "repeated transfer retains every child without resetting resources"{
 var cells=[_]M.Cell{.{}}**100;cells[0]=fixture(0.99,0.35,4)[0];var stats=M.Stats{.next_lineage=2};const initialC=@as(f64,cells[0].cohorts[0].biomass);const initialS=@as(f64,cells[0].cohorts[0].support_mass);var count:usize=0;
 for(1..100)|to|{
  const r=D.apply(&cells,&stats,0,0,to,1,1,1,&.{to});if(!r.ok)break;count+=1;
  var c:f64=0;var s:f64=0;for(cells)|cell|for(cell.cohorts)|co|{c+=co.biomass;s+=co.support_mass;};
  try std.testing.expectEqual(initialC,c);try std.testing.expectEqual(initialS,s);
 }
 try std.testing.expect(count>80);std.debug.print("DIRECTED_CUMULATIVE children={d} exact_represented_C_support_each_transfer=true credits_never_refilled=true\n",.{count});
}
