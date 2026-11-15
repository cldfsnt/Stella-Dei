//! Isolated Origin liquid law: immutable source, fixed downhill budgets, destination gather.
const std=@import("std");
pub const Ledger=struct{rounding_signed:f64=0,rounding_absolute:f64=0};
fn overlaps(a:anytype,b:anytype)bool{
 const aa=std.mem.sliceAsBytes(a);const bb=std.mem.sliceAsBytes(b);if(aa.len==0 or bb.len==0)return false;
 const lo_a=@intFromPtr(aa.ptr);const lo_b=@intFromPtr(bb.ptr);const end_a=@addWithOverflow(lo_a,aa.len);const end_b=@addWithOverflow(lo_b,bb.len);
 return end_a[1]!=0 or end_b[1]!=0 or (lo_a<end_b[0] and lo_b<end_a[0]);
}
pub fn step(mass:[]const f32,elevation:[]const f32,neighbors:[]const [6]usize,edges:[][6]f64,out:[]f32,km:f32,dt:f32,reverse:bool)!Ledger{
 @setFloatMode(.strict);const n=mass.len;if(n!=elevation.len or n!=neighbors.len or n!=edges.len or n!=out.len or overlaps(mass,out) or overlaps(elevation,out) or overlaps(neighbors,out) or overlaps(edges,out) or overlaps(mass,edges) or overlaps(elevation,edges) or overlaps(neighbors,edges))return error.InvalidShape;
 if(!std.math.isFinite(km) or km<=0 or !std.math.isFinite(dt) or dt<0)return error.InvalidValue;
 const factor:f32=@min(@as(f32,0.00002)*dt/6,1.0/7.0);
 for(mass,elevation,0..)|m,e,i|{if(!std.math.isFinite(m) or m<0 or !std.math.isFinite(e) or !std.math.isFinite(e+m*km))return error.InvalidValue;for(neighbors[i])|j|{if(j>=n)return error.InvalidTopology;var reciprocal=false;for(neighbors[j])|back|{if(back==i)reciprocal=true;}if(!reciprocal)return error.InvalidTopology;}}
 for(0..n)|cursor|{const i=if(reverse)n-1-cursor else cursor;const height=elevation[i]+mass[i]*km;var total:f64=0;
  for(neighbors[i],0..)|j,k|{var duplicate=j==i;for(neighbors[i][0..k])|prior|{if(prior==j)duplicate=true;}const target=elevation[j]+mass[j]*km;const flow:f32=if(!duplicate and height>target)@min(mass[i]*factor,(height-target)/km*factor)else 0;if(!std.math.isFinite(flow) or flow<0)return error.InvalidValue;edges[i][k]=flow;total+=flow;}
  if(total>mass[i])return error.OverBudget;
 }
 var ledger=Ledger{};
 for(0..n)|i|{var next:f64=mass[i];for(edges[i])|flow|next-=flow;
  for(neighbors[i],0..)|j,k|{var duplicate=j==i;for(neighbors[i][0..k])|prior|{if(prior==j)duplicate=true;}if(duplicate)continue;for(neighbors[j],0..)|target,slot|if(target==i){next+=edges[j][slot];};}
  if(!std.math.isFinite(next) or next<0 or next>std.math.floatMax(f32))return error.InvalidValue;
  out[i]=@floatCast(next);const residual=@as(f64,out[i])-next;ledger.rounding_signed+=residual;ledger.rounding_absolute+=@abs(residual);
 }return ledger;
}
