//! Explicit read-only current morphology search. No cached census or taxonomy.
const std=@import("std");const M=@import("simulation/microbes.zig");
pub const Found=struct{cell:usize,lineage:u64};
pub fn matches(c:M.Cohort,form:M.ProducerForm)bool{return c.lineage!=0 and std.math.isFinite(c.biomass) and c.biomass>0 and std.math.isFinite(c.support_mass) and c.support_mass>=0 and c.support_mass<=c.biomass and std.math.isFinite(c.organization) and std.math.isFinite(c.structure) and std.math.isFinite(c.efficiency) and M.producerForm(c)==form;}
pub fn find(cells:[]const M.Cell,points:anytype,direction:[3]f32,form:M.ProducerForm)error{UnsafeView}!?Found{
 if(cells.len!=points.len)return error.UnsafeView;
 var best:?Found=null;var score:f32=-std.math.inf(f32);var unsafe=false;
 for(direction)|v|if(!std.math.isFinite(v))return error.UnsafeView;
 const dn=direction[0]*direction[0]+direction[1]*direction[1]+direction[2]*direction[2];if(!std.math.isFinite(dn) or dn<=0)return error.UnsafeView;
 for(cells,0..)|cell,i|for(cell.cohorts)|c|{
  if(!matches(c,form))continue;
  const v=points[i].data;const len=@sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2]);
  if(!std.math.isFinite(len) or len<=0 or @abs(v[2]/len)>0.95){unsafe=true;continue;}
  const dot=(v[0]*direction[0]+v[1]*direction[1]+v[2]*direction[2])/len;
  if(!std.math.isFinite(dot)){unsafe=true;continue;}
  if(best==null or dot>score){best=.{.cell=i,.lineage=c.lineage};score=dot;}
 };
 if(best==null and unsafe)return error.UnsafeView;return best;
}
test "matching minority identity current form tie and unsafe scope"{
 const P=struct{data:[3]f32};var cells=[_]M.Cell{.{},.{}};const points=[_]P{.{.data=.{5000,0,0}},.{.data=.{0,5000,0}}};
 cells[0].cohorts[0]=.{.lineage=1,.biomass=0.5};cells[0].cohorts[1]=.{.lineage=9007199254740993,.biomass=0.01,.support_mass=0.001,.organization=0.1,.structure=0.2};
 const before=cells;const f=(try find(&cells,&points,.{1,0,0},.branching)).?;try std.testing.expectEqual(@as(u64,9007199254740993),f.lineage);try std.testing.expectEqualDeep(before,cells);
 cells[0].cohorts[1].structure=0;try std.testing.expect((try find(&cells,&points,.{1,0,0},.branching))==null);
 cells[0].cohorts[1].structure=0.2;cells[0].cohorts[1].biomass=std.math.nan(f32);try std.testing.expect((try find(&cells,&points,.{1,0,0},.branching))==null);
 cells[0].cohorts[1]=before[0].cohorts[1];const polar=[_]P{.{.data=.{0,0,5000}},points[1]};try std.testing.expectError(error.UnsafeView,find(&cells,&polar,.{1,0,0},.branching));
}
