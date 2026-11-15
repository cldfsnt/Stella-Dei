//! Research only: nonmutating paid daughter; no UI, Planet wiring or save fields.
const std=@import("std");
const M=@import("../simulation/microbes.zig");
pub const Receipt=struct{ok:bool=false,mass:f64=0,support:f64=0,credit:f64=0};
const Part=struct{left:f32,taken:f32};
fn withdraw(old:f32,want:f32,at_least:bool)?Part{
 if(!std.math.isFinite(old) or !std.math.isFinite(want) or old<0 or want<0 or want>old)return null;
 if(want==0)return .{.left=old,.taken=0};
 var left=old-want;
 var delta=@as(f64,old)-@as(f64,left);
 if(at_least and delta<@as(f64,want))left=std.math.nextAfter(f32,left,0);
 if(!at_least and delta>@as(f64,want))left=std.math.nextAfter(f32,left,std.math.inf(f32));
 delta=@as(f64,old)-@as(f64,left);
 const taken:f32=@floatCast(delta);
 // Refuse events too small to represent with a narrow bound, not silent losses.
 if(left<0 or delta<=0 or @as(f64,taken)!=delta or @abs(delta-@as(f64,want))>@as(f64,want)*0.00001)return null;
 if(at_least and delta<@as(f64,want))return null;
 if(!at_least and delta>@as(f64,want))return null;
 return .{.left=left,.taken=taken};
}
pub fn apply(cells:[]M.Cell,stats:*M.Stats,from:usize,slot:usize,to:usize,id:u64,world:u32,expected_world:u32,neighbors:[]const usize)Receipt{
 if(world!=expected_world or from>=cells.len or to>=cells.len or from==to or slot>=4 or stats.next_lineage==std.math.maxInt(u64) or stats.births==std.math.maxInt(u64))return .{};
 var adjacent=false;for(neighbors)|n|if(n==to){adjacent=true;break;};if(!adjacent)return .{};
 if(!M.validCell(cells[from],stats.next_lineage) or !M.validCell(cells[to],stats.next_lineage))return .{};
 const parent=cells[from].cohorts[slot];if(parent.lineage!=id or parent.biomass<=0)return .{};
 var source=cells[from];var target=cells[to];var next=stats.*;
 // Retain production eligibility/ancestry and no-mutation behavior on temporary copies.
 if(!M.reproduce(&source,slot,&target,&next,false))return .{};
 var child_slot:usize=0;while(child_slot<4 and target.cohorts[child_slot].lineage!=stats.next_lineage):(child_slot+=1){}if(child_slot==4)return .{};
 const mass=withdraw(parent.biomass,0.01,false) orelse return .{};
 const desired_support:f32=@floatCast(@as(f64,parent.support_mass)*@as(f64,mass.taken)/@as(f64,parent.biomass));
 const support=withdraw(parent.support_mass,desired_support,false) orelse return .{};
 const credit=withdraw(parent.reproduction_credit,0.04,true) orelse return .{};
 if(support.left>mass.left or support.taken>mass.taken)return .{};
 source.cohorts[slot].biomass=mass.left;source.cohorts[slot].support_mass=support.left;source.cohorts[slot].reproduction_credit=credit.left;
 target.cohorts[child_slot].biomass=mass.taken;target.cohorts[child_slot].support_mass=support.taken;
 if(!M.validCell(source,next.next_lineage) or !M.validCell(target,next.next_lineage))return .{};
 cells[from]=source;cells[to]=target;stats.*=next;
 return .{.ok=true,.mass=mass.taken,.support=support.taken,.credit=credit.taken};
}
