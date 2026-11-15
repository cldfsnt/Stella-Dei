//! Stage a real paid packet and its deposition before committing any state.
const std=@import("std");const M=@import("microbes.zig");const G=@import("wind_genetics.zig");
pub const Receipt=struct{arrived:bool,outcome:enum{arrival,viability_failure,capacity_failure},carbon_paid:f64,nitrogen_paid:f64,support_paid:f64,carbon_received:f64,nitrogen_received:f64,carbon_returned:f64,nitrogen_returned:f64,carbon_residual:f64,nitrogen_residual:f64,carbon_bound:f64,nitrogen_bound:f64,lineage:u64=0};
fn density(budget:f64,area:f64)?f32{const x=budget/area;if(!std.math.isFinite(x) or x<0 or x>std.math.floatMax(f32))return null;var y:f32=@floatCast(x);if(@as(f64,y)*area>budget)y=std.math.nextAfter(f32,y,0);return y;}
fn add(pool:f32,budget:f64,area:f64)?f32{if(!std.math.isFinite(pool) or pool<0)return null;const inc=density(budget,area) orelse return null;const exact=@as(f64,pool)+inc;if(exact>std.math.floatMax(f32))return null;var out:f32=@floatCast(exact);if((@as(f64,out)-pool)*area>budget)out=std.math.nextAfter(f32,out,pool);return out;}
pub fn launch(donor:*M.Cell,slot:usize,target:*M.Cell,stats:*M.Stats,area_source:f64,area_target:f64,viable:bool,config:G.Config)?Receipt{
 if(donor==target or slot>=4 or !config.enabled or !config.valid() or !std.math.isFinite(area_source) or area_source<=0 or !std.math.isFinite(area_target) or area_target<=0)return null;
 if(!M.validCell(donor.*,stats.next_lineage) or !M.validCell(target.*,stats.next_lineage) or stats.next_lineage==std.math.maxInt(u64) or stats.births==std.math.maxInt(u64))return null;
 const original=donor.*;var paid=original;var packet=M.Cell{};var trial_stats=stats.*;
 if(!M.prepareWindPacket(&paid,slot,&packet,&trial_stats,false,config))return null;
 const c=(@as(f64,original.cohorts[slot].biomass)-paid.cohorts[slot].biomass)*area_source;
 const support=(@as(f64,original.cohorts[slot].support_mass)-paid.cohorts[slot].support_mass)*area_source;
 const n=c*@as(f64,M.nutrient_per_carbon);if(!std.math.isFinite(c) or c<=0 or !std.math.isFinite(n) or support<0 or support>c)return null;
 const amount=density(c,area_target) orelse return null;const tissue=density(support,area_target) orelse return null;if(amount<=0)return null;
 var empty:?usize=null;for(target.cohorts,0..)|co,i|if(co.biomass==0){empty=i;break;};
 const arrived=viable and empty!=null and @as(f64,M.biomass(target.*))+amount<=1 and M.biomass(target.*)<=0.99;
 var next=target.*;var received:f64=0;var received_n:f64=0;var lineage:u64=0;
 if(arrived){
  paid=original;packet=.{};trial_stats=stats.*;if(!M.prepareWindPacket(&paid,slot,&packet,&trial_stats,true,config))return null;
  var child=packet.cohorts[0];child.biomass=amount;child.support_mass=@min(tissue,amount);next.cohorts[empty.?]=child;lineage=child.lineage;
  received=@as(f64,amount)*area_target;received_n=received*@as(f64,M.nutrient_per_carbon);
 }else{
  next.detritus=add(next.detritus,c,area_target) orelse return null;next.nutrient=add(next.nutrient,n,area_target) orelse return null;
  received=(@as(f64,next.detritus)-target.detritus)*area_target;received_n=(@as(f64,next.nutrient)-target.nutrient)*area_target;
  if(received<=0 or received_n<=0)return null;
 }
 if(received>c or received_n>n)return null;
 paid.detritus=add(paid.detritus,c-received,area_source) orelse return null;paid.nutrient=add(paid.nutrient,n-received_n,area_source) orelse return null;
 const returned=(@as(f64,paid.detritus)-original.detritus)*area_source;const returned_n=(@as(f64,paid.nutrient)-original.nutrient)*area_source;
 const residual=c-received-returned;const residual_n=n-received_n-returned_n;
 const bound=16*0x1p-24*((@as(f64,M.carbon(original))+M.carbon(paid))*area_source+(@as(f64,M.carbon(target.*))+M.carbon(next))*area_target);
 const nbound=16*0x1p-24*((@as(f64,M.nutrientTotal(original))+M.nutrientTotal(paid))*area_source+(@as(f64,M.nutrientTotal(target.*))+M.nutrientTotal(next))*area_target);
 if(residual<0 or residual_n<0 or !std.math.isFinite(bound) or !std.math.isFinite(nbound) or residual>bound or residual_n>nbound)return null;
 if(!M.validCell(paid,trial_stats.next_lineage) or !M.validCell(next,trial_stats.next_lineage))return null;
 donor.*=paid;target.*=next;if(arrived)stats.*=trial_stats;
 return .{.arrived=arrived,.outcome=if(arrived).arrival else if(!viable).viability_failure else .capacity_failure,.carbon_paid=c,.nitrogen_paid=n,.support_paid=support,.carbon_received=received,.nitrogen_received=received_n,.carbon_returned=returned,.nitrogen_returned=returned_n,.carbon_residual=residual,.nitrogen_residual=residual_n,.carbon_bound=bound,.nitrogen_bound=nbound,.lineage=lineage};
}
test "paid success and failed launch conserve absolute budgets across unequal areas"{
 const areas=[_][2]f64{.{1,1},.{1,2},.{2,1},.{1,10},.{10,1}};
 for(areas)|a|for([_]bool{false,true})|success|{
  var donor=M.Cell{};donor.cohorts[0]=.{.lineage=1,.biomass=0.1,.support_mass=0.02,.reproduction_credit=0.1,.aerial_allocation=0.5};var dst=M.Cell{};var stats=M.Stats{.next_lineage=2};const before=donor;const old=stats;
  const r=launch(&donor,0,&dst,&stats,a[0],a[1],success,.{.enabled=true,.law=1}) orelse return error.Refused;
  try std.testing.expect(r.carbon_paid>0 and r.carbon_received<=r.carbon_paid and r.nitrogen_received<=r.nitrogen_paid and r.carbon_residual<=r.carbon_bound);
  try std.testing.expect(donor.cohorts[0].biomass<before.cohorts[0].biomass and donor.cohorts[0].reproduction_credit<before.cohorts[0].reproduction_credit);
  if(success){try std.testing.expectEqual(@as(u64,1),stats.births);try std.testing.expectEqual(@as(f32,0),dst.cohorts[0].reproduction_credit);}else{try std.testing.expectEqualDeep(old,stats);try std.testing.expect(dst.detritus>0 and dst.nutrient>0 and M.biomass(dst)==0);}
 };
}
test "full destination is paid failure but invalid budget refuses atomically"{
 var donor=M.Cell{};donor.cohorts[0]=.{.lineage=1,.biomass=0.1,.support_mass=0.02,.reproduction_credit=0.1};var dst=M.Cell{};for(&dst.cohorts,0..)|*c,i|c.*=.{.lineage=i+2,.biomass=0.1};var stats=M.Stats{.next_lineage=6};const cfg=G.Config{.enabled=true,.law=1};
 try std.testing.expect(!launch(&donor,0,&dst,&stats,1,1,true,cfg).?.arrived);const a=donor;const b=dst;const ss=stats;try std.testing.expect(launch(&donor,0,&dst,&stats,0,1,true,cfg)==null);try std.testing.expectEqualDeep(a,donor);try std.testing.expectEqualDeep(b,dst);try std.testing.expectEqualDeep(ss,stats);
}

test "actual represented C N ledger and invalid extremes"{
 var donor=M.Cell{};donor.cohorts[0]=.{.lineage=1,.biomass=0.1,.support_mass=0.02,.reproduction_credit=0.1};var dst=M.Cell{};var stats=M.Stats{.next_lineage=2};const cfg=G.Config{.enabled=true,.law=1};
 const before=donor;const empty=dst;const old=stats;
 for([_]f64{std.math.nan(f64),std.math.inf(f64),-1,0})|area|{try std.testing.expect(launch(&donor,0,&dst,&stats,area,1,true,cfg)==null);try std.testing.expectEqualDeep(before,donor);try std.testing.expectEqualDeep(empty,dst);try std.testing.expectEqualDeep(old,stats);}
 const r=launch(&donor,0,&dst,&stats,10,1,false,cfg).?;
 const cbefore=(@as(f64,before.cohorts[0].biomass)+before.detritus)*10;
 const cafter=(@as(f64,donor.cohorts[0].biomass)+donor.detritus)*10+dst.detritus;
 const nbefore=(@as(f64,before.cohorts[0].biomass)*M.nutrient_per_carbon+before.nutrient)*10+empty.nutrient;
 const nafter=(@as(f64,donor.cohorts[0].biomass)*M.nutrient_per_carbon+donor.nutrient)*10+dst.nutrient;
 try std.testing.expect(@abs((cbefore-cafter)-r.carbon_residual)<=1e-14);try std.testing.expect(@abs((nbefore-nafter)-r.nitrogen_residual)<=1e-14);
 std.debug.print("WIND_LAYOUT cohort_bytes{} cell_bytes{} receipt_bytes{}\n",.{@sizeOf(M.Cohort),@sizeOf(M.Cell),@sizeOf(Receipt)});
}
test "all three successful birth routes mutate aerial exactly once and off retains old RNG"{
 var initial=M.Cell{};initial.cohorts[0]=.{.lineage=1,.biomass=0.1,.support_mass=0.02,.reproduction_credit=0.1,.aerial_allocation=0.5};const cfg=G.Config{.enabled=true,.law=1,.stream_seed=42};
 for(0..3)|route|{
  var d=initial;var t=M.Cell{};var stats=M.Stats{.next_lineage=2};
  if(route==0){try std.testing.expect(M.prepareWindPacket(&d,0,&t,&stats,true,cfg));}else if(route==1){try std.testing.expect(M.reproduceWithWind(&d,0,&t,&stats,cfg));}else{try std.testing.expect(launch(&d,0,&t,&stats,1,1,true,cfg).?.arrived);}
  try std.testing.expectEqual(G.mutation(0.5,42,1,2,1),t.cohorts[0].aerial_allocation);try std.testing.expectEqual(@as(u64,1),stats.births);try std.testing.expectEqual(@as(f32,0),t.cohorts[0].reproduction_credit);
 }
 initial.cohorts[0].aerial_allocation=0;var a=initial;var b=initial;var ta=M.Cell{};var tb=M.Cell{};var sa=M.Stats{.next_lineage=2};var sb=sa;
 try std.testing.expect(M.propagate(&a,0,&ta,&sa));try std.testing.expect(M.prepareWindPacket(&b,0,&tb,&sb,true,.{}));try std.testing.expectEqualDeep(a,b);try std.testing.expectEqualDeep(ta,tb);try std.testing.expectEqualDeep(sa,sb);
 a=initial;b=initial;ta=.{};tb=.{};sa=.{.next_lineage=2};sb=sa;
 try std.testing.expect(M.reproduce(&a,0,&ta,&sa,true));try std.testing.expect(M.reproduceWithWind(&b,0,&tb,&sb,.{}));try std.testing.expectEqualDeep(a,b);try std.testing.expectEqualDeep(ta,tb);try std.testing.expectEqualDeep(sa,sb);
}
