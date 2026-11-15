const std=@import("std");
const M=@import("experimental/soil_physiology_core.zig");
fn fixture(root:f32,storage:f32)M.Cell{var c=M.initialized(123);c.cohorts[0]=.{.biomass=0.125,.support_mass=0.03125,.organization=0.25,.root_fraction=root,.retention_allocation=storage,.stored_water=@as(f64,storage)*0.15625,.lineage=1,.reproduction_credit=0.125,.generation=3};return c;}
fn equal(a:anytype,b:@TypeOf(a))!void{try std.testing.expectEqualDeep(a,b);}
test "funded no mutation birth same and adjacent cells with inherited allocation"{
 for([_][2]f32{.{0,0},.{0.25,0.25},.{0.75,0.25},.{1,0},.{0,1}})|allocation|for([_]bool{false,true})|same|{
 var donor=fixture(allocation[0],allocation[1]);var target=M.initialized(456);var stats=M.Stats{.next_lineage=2};const before=donor;const old=before.cohorts[0];const dst=if(same)&donor else &target;
 try std.testing.expect(M.reproduce(&donor,0,dst,&stats,false));const child=dst.cohorts[if(same)@as(usize,1) else 0];const parent=donor.cohorts[0];
 try equal(child.root_fraction,old.root_fraction);try equal(child.retention_allocation,old.retention_allocation);try equal(donor.rng,before.rng);try equal(target.rng,@as(u64,456));try equal(child.parent,old.lineage);try equal(child.lineage,@as(u64,2));try equal(child.generation,@as(u32,4));try equal(child.reproduction_credit,@as(f32,0));
 const amount:@TypeOf(old.biomass)=0.01;const support=@min(amount,old.support_mass*(amount/old.biomass));
 try equal(child.biomass,amount);try equal(parent.biomass,old.biomass-amount);try equal(child.support_mass,support);try equal(parent.support_mass,old.support_mass-support);try equal(parent.reproduction_credit,old.reproduction_credit-@as(f32,0.04));
 const expected_parent_water=old.stored_water*(1-@as(f64,support)/old.support_mass);try equal(parent.stored_water,expected_parent_water);try equal(child.stored_water,old.stored_water-expected_parent_water);
 try std.testing.expectApproxEqAbs(M.waterTotal(before),M.waterTotal(donor)+(if(same)@as(f64,0) else M.waterTotal(target)),1e-16);
 try std.testing.expect(M.validCell(donor,3) and M.validCell(target,3));try equal(stats.births,@as(u64,1));
 // f32 tissue subtraction need not have exact real-number closure; no tolerance-free closure claim.
 std.debug.print("INHERIT same={} root={d} storage={d} carbon_residual={e} support_residual={e}\n",.{same,allocation[0],allocation[1],@as(f64,parent.biomass)+child.biomass-old.biomass,@as(f64,parent.support_mass)+child.support_mass-old.support_mass});
 };}
test "failed birth leaves both cells and stats unchanged"{for(0..5)|case|{
 var donor=fixture(0.25,0.25);var target=M.initialized(456);var stats=M.Stats{.next_lineage=2};var which:usize=0;
 switch(case){0=>which=4,1=>donor.cohorts[0].biomass=0.02,2=>donor.cohorts[0].reproduction_credit=0.039,3=>{for(&target.cohorts)|*c|c.*=.{.biomass=0.1};},4=>target.cohorts[1]=.{.biomass=1},else=>unreachable}
 const d=donor;const t=target;const s=stats;try std.testing.expect(!M.reproduce(&donor,which,&target,&stats,false));try equal(d,donor);try equal(t,target);try equal(s,stats);
 }}
test "allocation bounds and explicit capacity shrink returns to legacy escrow only"{
 var cell=fixture(0.25,0.25);try std.testing.expect(M.validCell(cell,2));cell.cohorts[0].root_fraction=0.8;try std.testing.expect(!M.validCell(cell,2));cell.cohorts[0].root_fraction=0.25;
 const total=M.waterTotal(cell);cell.cohorts[0].retention_allocation=0;M.settleWater(&cell);try equal(cell.cohorts[0].stored_water,@as(f64,0));try equal(cell.liquid_return,total);try equal(M.waterTotal(cell),total);try std.testing.expect(M.validCell(cell,2));
 // This is prescribed capacity shrink, not mutation or approved physical destination integration.
}
