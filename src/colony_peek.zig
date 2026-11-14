//! One pinned patch, four current cohorts; purely observational, never persisted.
const std=@import("std");const M=@import("simulation/microbes.zig");
pub const Trend=enum{waiting,rising,falling,stable,turnover,empty};
pub const Item=struct{lineage:u64=0,biomass:f32=0,share:f32=0,optimum:f32=303,form:M.ProducerForm=.mat};
pub const View=struct{items:[4]Item=.{.{}}**4,count:usize=0,dominant:usize=0,trend:Trend=.empty,days:f64=0};
pub fn read(cell:M.Cell)View{
 var v=View{};var total:f64=0;
 for(cell.cohorts)|c|{
  if(c.lineage==0 or !std.math.isFinite(c.biomass) or c.biomass<=0)continue;
  v.items[v.count]=.{.lineage=c.lineage,.biomass=c.biomass,.optimum=c.optimum,.form=M.producerForm(c)};
  total+=c.biomass;if(c.biomass>v.items[v.dominant].biomass)v.dominant=v.count;
  v.count+=1;
 }
 if(total>0)for(v.items[0..v.count])|*i|{i.share=@floatCast(@as(f64,i.biomass)/total);};
 return v;
}
pub const Pin=struct{
 cell:?usize=null,since:f64=0,baseline:View=.{},
 pub fn clear(self:*Pin)void{self.*=.{};}
 pub fn set(self:*Pin,cell:usize,data:M.Cell,time:f64)void{
  if(!std.math.isFinite(time)){self.clear();return;}
  self.*=.{.cell=cell,.since=time,.baseline=read(data)};
 }
 pub fn observe(self:*Pin,data:M.Cell,time:f64)View{
  if(self.cell==null or !std.math.isFinite(time) or time<self.since){self.clear();return .{};}
  var v=read(data);v.days=(time-self.since)/86400;
  if(v.count==0)return v;
  v.trend=.waiting;
  if(self.baseline.count==0 or v.items[v.dominant].lineage!=self.baseline.items[self.baseline.dominant].lineage){v.trend=.turnover;return v;}
  if(v.days<2)return v;
  const before=self.baseline.items[self.baseline.dominant].biomass;const delta=v.items[v.dominant].biomass-before;
  v.trend=if(@abs(delta)<=before*0.01) .stable else if(delta>0) .rising else .falling;return v;
 }
};
pub fn label(t:Trend)[]const u8{return switch(t){.waiting=>"observing",.rising=>"biomass up",.falling=>"biomass down",.stable=>"biomass steady",.turnover=>"dominant changed",.empty=>"no living colonies"};}
test "actual shares and same-lineage changes are distinct from turnover"{
 var c=M.Cell{};c.cohorts[0]=.{.lineage=7,.biomass=0.03};c.cohorts[1]=.{.lineage=8,.biomass=0.01};
 const original=c;var p=Pin{};p.set(12,c,0);var v=p.observe(c,86400);
 try std.testing.expectApproxEqAbs(@as(f32,0.75),v.items[0].share,0.00001);try std.testing.expectEqual(Trend.waiting,v.trend);
 c.cohorts[0].biomass=0.04;v=p.observe(c,2*86400);try std.testing.expectEqual(Trend.rising,v.trend);
 c.cohorts[0].biomass=0.02;v=p.observe(c,3*86400);try std.testing.expectEqual(Trend.falling,v.trend);
 c.cohorts[1].biomass=0.04;v=p.observe(c,3*86400);try std.testing.expectEqual(Trend.turnover,v.trend);
 const before=c;_=p.observe(c,4*86400);try std.testing.expectEqualDeep(before,c);
 p.set(2,original,5*86400);_=p.observe(original,0);try std.testing.expect(p.cell==null);
}
test "empty invalid and replacement observations never invent growth"{
 var p=Pin{};var c=M.Cell{};p.set(0,c,0);try std.testing.expectEqual(Trend.empty,p.observe(c,86400).trend);
 c.cohorts[2]=.{.lineage=99,.biomass=1};try std.testing.expectEqual(Trend.turnover,p.observe(c,3*86400).trend);
 p.set(1,c,0);c.cohorts[2].lineage=100;try std.testing.expectEqual(Trend.turnover,p.observe(c,3*86400).trend);
 c.cohorts[2].biomass=std.math.nan(f32);try std.testing.expectEqual(@as(usize,0),p.observe(c,4*86400).count);
 p.clear();try std.testing.expect(p.cell==null);
}
