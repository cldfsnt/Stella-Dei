//! Experimental handling/accessibility hypothesis, not calibrated plant armor.
//! Tough paid support is less accessible than fronds. Same growth/costs elsewhere.
const std=@import("std");
pub fn accessible(c:anytype,strength:f32)f32{
 if(c.biomass<=0)return 0;
 if(strength==0 or c.structure<=0 or c.support_mass<=0)return c.biomass;
 // Subnormal rounding must not turn living accessible tissue into immunity.
 return @max(std.math.floatTrueMin(f32),(c.biomass-c.support_mass)+c.support_mass/(1+strength*c.structure));
}
pub fn graze(comptime M:type,cell:*M.Cell,days:f32,oxygen:f32,strength:f32)M.GrazingFlux{
 if(!std.math.isFinite(days) or days<=0 or !std.math.isFinite(oxygen) or oxygen<=0 or !std.math.isFinite(strength) or strength<0 or strength>4 or !M.validCell(cell.*,std.math.maxInt(u64)))return .{};
 const snapshot=cell.cohorts;var demand:[4][4]f32=.{.{0,0,0,0},.{0,0,0,0},.{0,0,0,0},.{0,0,0,0}};
 for(snapshot,0..)|pred,i|{
  if(pred.biomass<=0 or pred.feeding<=0)continue;
  var food:f32=0;var available:f32=0;
  for(snapshot,0..)|prey,j|if(i!=j){food+=prey.biomass;available+=accessible(prey,strength);};
  if(food<=0 or available<=0)continue;
  // Reduced handling efficiency, not just a smaller cap that disappears at low demand.
  const desired=@min(available,pred.biomass*3*pred.feeding*days*(available/food));
  for(snapshot,0..)|prey,j|if(i!=j){demand[i][j]=desired*accessible(prey,strength)/available;};
 }
 var requested:f32=0;for(demand)|row|for(row)|v|{requested+=v;};
 const oxygen_scale=if(requested>0)@min(@as(f32,1),@max(0,oxygen)/(requested*0.25)) else 0;
 var gains=[_]f32{0,0,0,0};var losses=[_]f32{0,0,0,0};var total:f32=0;
 for(snapshot,0..)|prey,j|{
  var wanted:f32=0;for(demand)|row|wanted+=row[j];
  const scale=if(wanted>0)@min(@as(f32,1),prey.biomass/wanted) else 0;
  for(0..4)|i|{const consumed=demand[i][j]*scale*oxygen_scale;gains[i]+=consumed*0.5;losses[j]+=consumed;total+=consumed;}
 }
 for(&cell.cohorts,0..)|*c,i|{if(c.biomass>0)c.support_mass*=@max(0,1-losses[i]/c.biomass);c.support_mass+=gains[i]*c.organization;c.biomass=@max(0,c.biomass-losses[i]+gains[i]);c.support_mass=std.math.clamp(c.support_mass,0,c.biomass);c.reproduction_credit+=gains[i];c.lifetime_grazed+=gains[i]*2;}
 cell.detritus+=total*0.25;cell.nutrient+=total*0.5*M.nutrient_per_carbon;
 return .{.consumed=total,.respired=total*0.25};
}
