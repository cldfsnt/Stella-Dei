//! Isolated hypothesis; no production state/schema. Water kg/m², pools10^9kg/patch.
const std=@import("std");
pub const M=@import("paid_hydration_core.zig");
pub const area:f64=7669529600;
const conversion:f64=1e9/area;
pub fn capacity(c:M.Cohort)f64{return @as(f64,c.support_mass)*c.qa_retention*10;}
pub fn take(pool:*f32,wanted:f64)f64{
 if(!std.math.isFinite(pool.*) or pool.*<0 or !std.math.isFinite(wanted) or wanted<=0)return 0;
 const old=pool.*;var after:f32=@floatCast(@max(0,@as(f64,old)-wanted/conversion));
 if((@as(f64,old)-after)*conversion>wanted)after=std.math.nextAfter(f32,after,std.math.inf(f32));
 if(after>old or after<0)return 0;
 const received=(@as(f64,old)-after)*conversion;
 std.debug.assert(received>=0 and received<=wanted);pool.*=after;return received;
}
pub fn deposit(pool:*f32,escrow:*f64)void{
 if(!std.math.isFinite(pool.*) or pool.*<0 or !std.math.isFinite(escrow.*) or escrow.*<=0)return;
 const old=pool.*;var after:f32=@floatCast(@as(f64,old)+escrow.*/conversion);
 if(!std.math.isFinite(after))return;
 if((@as(f64,after)-old)*conversion>escrow.*)after=std.math.nextAfter(f32,after,-std.math.inf(f32));
 if(after<old)return;
 const paid=(@as(f64,after)-old)*conversion;std.debug.assert(paid>=0 and paid<=escrow.*);
 pool.*=after;escrow.*-=paid;
}
pub const State=struct{
 cell:M.Cell=M.initialized(7),retained:[4]f64=.{0,0,0,0},liquid:f32=0,vapor:f32=0,liquid_escrow:f64=0,vapor_escrow:f64=0,held:f64=0,
 co2:f64=10,oxygen:f64=10,evaporated:f64=0,uptake:f64=0,returned:f64=0,
 pub fn totalWater(s:*const State)f64{var v=(@as(f64,s.liquid)+s.vapor)*conversion+s.liquid_escrow+s.vapor_escrow+s.held;for(s.retained)|w|v+=w;return v;}
 pub fn totalCarbon(s:*const State)f64{var v=s.co2+@as(f64,s.cell.detritus);for(s.cell.cohorts)|c|v+=c.biomass;return v;}
 pub fn totalN(s:*const State)f64{var v=@as(f64,s.cell.nutrient);for(s.cell.cohorts)|c|v+=@as(f64,c.biomass)*M.nutrient_per_carbon;return v;}
 pub fn exposure(s:*State,wet:bool)void{
  if(!wet){s.held+=@as(f64,s.liquid)*conversion;s.liquid=0;}else deposit(&s.liquid,&s.held);
 }
 pub fn settle(s:*State)void{
  for(s.cell.cohorts,0..)|c,i|{const cap=capacity(c);if(s.retained[i]>cap){const extra=s.retained[i]-cap;s.retained[i]=cap;s.liquid_escrow+=extra;s.returned+=extra;}}
  deposit(&s.liquid,&s.liquid_escrow);deposit(&s.vapor,&s.vapor_escrow);
 }
 pub fn step(s:*State,dt:f32,light:f32,wet:bool)?M.Flux{
  if(!std.math.isFinite(dt) or dt<=0 or !std.math.isFinite(light) or light<0 or !std.math.isFinite(s.liquid) or s.liquid<0 or !std.math.isFinite(s.vapor) or s.vapor<0 or !std.math.isFinite(s.held) or s.held<0 or !std.math.isFinite(s.liquid_escrow) or s.liquid_escrow<0 or !std.math.isFinite(s.vapor_escrow) or s.vapor_escrow<0 or !std.math.isFinite(s.co2) or s.co2<0 or !std.math.isFinite(s.oxygen) or s.oxygen<0)return null;
  for(s.cell.cohorts,0..)|c,i|{if(!std.math.isFinite(c.qa_retention) or c.qa_retention<0 or c.qa_retention>1 or !std.math.isFinite(s.retained[i]) or s.retained[i]<0)return null;}

  s.settle();s.exposure(wet);var hydrated=[_]f32{0,0,0,0};
  for(s.cell.cohorts,0..)|c,i|{
   const cap=capacity(c);const credit=take(&s.liquid,@max(0,cap-s.retained[i]));
   const before=s.retained[i];var after=before+credit;
   if(after-before>credit)after=std.math.nextAfter(f64,after,-std.math.inf(f64));
   s.retained[i]=after;s.liquid_escrow+=credit-(after-before);s.uptake+=credit;
   const demand=0.1*@as(f64,M.frondMass(c))*(@as(f64,dt)/86400)*(0.5+0.5*std.math.clamp(@as(f64,light),0,1));
   const wanted=@min(s.retained[i],demand);const old=s.retained[i];s.retained[i]=@max(0,old-wanted);const spent=old-s.retained[i];
   s.vapor_escrow+=spent;s.evaporated+=spent;
   if(cap>0)hydrated[i]=@floatCast(std.math.clamp(s.retained[i]/cap,0,1));
  }
  const depth:f32=if(wet)@floatCast(@as(f64,s.liquid)*conversion/1e6) else 0;
  const flux=M.step(&s.cell,.{.temperature=300,.depth_km=depth,.light=light,.carbon_available=@floatCast(s.co2),.oxygen_carbon_capacity=@floatCast(s.oxygen),.qa_hydration=hydrated},dt);
  s.co2-=flux.fixed;s.co2+=flux.recycled;s.oxygen+=flux.fixed;s.oxygen-=flux.recycled;
  std.debug.assert(s.co2>=0 and s.oxygen>=0);s.settle();return flux;
 }
};
test "no representable liquid withdrawal means no hydration credit"{var p:f32=1e9;const before=p;try std.testing.expectEqual(@as(f64,0),take(&p,1e-9));try std.testing.expectEqual(before,p);}
test "unrepresentable vapor return stays nonhydrating escrow"{var p:f32=1e9;var e:f64=1e-9;deposit(&p,&e);try std.testing.expectEqual(@as(f32,1e9),p);try std.testing.expectEqual(@as(f64,1e-9),e);}
test "bounded realized receipts across tiny and huge sources"{for([_]f32{0,1e-10,0.001,1,10000,1e9})|initial|{for([_]f64{0,1e-12,1e-6,0.01,1,1e10})|want|{var p=initial;const got=take(&p,want);try std.testing.expect(got<=want);try std.testing.expectEqual((@as(f64,initial)-p)*conversion,got);var e=got;deposit(&p,&e);try std.testing.expect(@abs((@as(f64,p)-initial)*conversion+e)<=@max(1e-9,64*std.math.floatEps(f64)*@as(f64,initial)*conversion));}}}
