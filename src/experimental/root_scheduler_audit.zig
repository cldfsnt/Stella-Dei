//! Read-only diagnostic sums; not spendable material or a new acceptance tolerance.
const std=@import("std");
pub const Audit=struct{
 columns:u64=0,soil_positive:u64=0,cold:u64=0,exposed:u64=0,
 infiltrated:f64=0,infiltration_requested:f64=0,soil_evaporated:f64=0,standing_evaporated:f64=0,
 phase_signed:[5]f64=.{0,0,0,0,0},phase_absolute:[5]f64=.{0,0,0,0,0},phase_max:[5]f64=.{0,0,0,0,0},
 root_calls:u64=0,root_demand:f64=0,root_paid:f64=0,root_credited:f64=0,root_zero_receipt:u64=0,vapor_zero_receipt:u64=0,
 root_receiver_signed:f64=0,root_receiver_absolute:f64=0,root_receiver_max:f64=0,
};
pub var current:Audit=.{};
pub fn column(before:anytype,result:anytype,area:f64,temp:f64)void{
 @setFloatMode(.strict);
 current.columns+=1;if(result.state.soil>0)current.soil_positive+=1;if(temp<=273.15)current.cold+=1;if(result.exposed_seconds>0)current.exposed+=1;
 current.infiltrated+=result.infiltrated_density;current.infiltration_requested+=result.infiltration_requested_density;current.soil_evaporated+=result.soil_evap_density;current.standing_evaporated+=result.standing_evap_native*1e9/area;
 var old=before;
 for(result.stages,0..)|after,i|{
  // Signed physical endpoint residual; do not infer exactness from cancellation.
  const residual=(@as(f64,after.liquid)-old.liquid+@as(f64,after.vapor)-old.vapor)*1e9/area+(after.soil-old.soil);
  current.phase_signed[i]+=residual;current.phase_absolute[i]+=@abs(residual);current.phase_max[i]=@max(current.phase_max[i],@abs(residual));old=after;
 }
}
pub fn root(old_vapor:f32,result:anytype)void{
 current.root_calls+=1;var requested:f64=0;for(result.demand)|d|requested+=d;current.root_demand+=requested;current.root_paid+=result.paid;for(result.credits)|c|current.root_credited+=c;
 if(requested>0 and result.paid==0)current.root_zero_receipt+=1;if(result.paid>0 and result.vapor==old_vapor)current.vapor_zero_receipt+=1;
 current.root_receiver_signed+=result.vapor_rounding_density;current.root_receiver_absolute+=@abs(result.vapor_rounding_density);current.root_receiver_max=@max(current.root_receiver_max,@abs(result.vapor_rounding_density));
}
