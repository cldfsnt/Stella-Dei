const std=@import("std");const P=@import("physical_water_f64.zig");
pub var strict_closure:bool=false;
pub var dumps:bool=false;pub var serial:usize=0;
pub fn dump(label:[]const u8,bytes:[]const u8)void{
 if(!dumps)return;var buf:[1024]u8=undefined;const path=std.fmt.bufPrint(&buf,"/workspace/scratch/f67c3ac60ca3/site-tmp/vapor-cycle-engine/{s}-{d}-{s}.bin",.{if(strict_closure)"strict"else"diagnostic",serial,label}) catch unreachable;
 std.fs.cwd().writeFile(.{.sub_path=path,.data=bytes}) catch unreachable;
}
pub const Result=struct{soil:f64,vapor:f64,paid:f64=0,funded:f64=0,native_received:f64=0,residual_density:f64=0};
pub fn step(soil:f64,vapor:f64,area:f64,wanted:f64)?Result{
 @setFloatMode(.strict);if(!std.math.isFinite(area) or area<=0 or !std.math.isFinite(vapor) or vapor<0)return null;
 const keep=Result{.soil=soil,.vapor=vapor};const removed=P.remove(soil,wanted) orelse return null;if(removed.paid==0)return keep;
 const budget=P.downRatio(P.downProduct(removed.paid,area),1e9);if(!std.math.isFinite(budget))return null;
 var after=vapor+budget;if(!std.math.isFinite(after))return null;const delta=P.difference(after,vapor);if(delta.hi>budget or (delta.hi==budget and delta.lo>0))after=std.math.nextAfter(f64,after,vapor);
 const received=P.downDifference(after,vapor);if(received<=0)return keep;
 const sd=P.difference(soil,removed.after);const vd=P.difference(after,vapor);
 if(strict_closure and (sd.lo!=0 or vd.lo!=0 or @as(f128,sd.hi)*@as(f128,area)!=@as(f128,vd.hi)*1e9))return keep;
 const source_sum=@as(f128,sd.hi)+@as(f128,sd.lo);const receiver_sum=@as(f128,vd.hi)+@as(f128,vd.lo);
 const source_lo=down(down(source_sum)*@as(f128,area));const source_hi=up(up(source_sum)*@as(f128,area));
 const receiver_lo=down(down(receiver_sum)*1e9);const receiver_hi=up(up(receiver_sum)*1e9);
 const error_hi=@max(up(@abs(receiver_lo-source_hi)),up(@abs(receiver_hi-source_lo)));
 const vu=@max(std.math.nextAfter(f64,after,std.math.inf(f64))-after,after-std.math.nextAfter(f64,after,-std.math.inf(f64)));
 const su=@max(std.math.nextAfter(f64,soil,std.math.inf(f64))-soil,soil-std.math.nextAfter(f64,soil,-std.math.inf(f64)));
 const vapor_ulp=up(@as(f128,vu)*1e9);const soil_ulp=up(@as(f128,su)*@as(f128,area));
 const envelope=up(up(up(2*vapor_ulp)+up(2*soil_ulp))+up(16*std.math.floatEps(f64)*source_hi));
 if(!std.math.isFinite(envelope) or !std.math.isFinite(error_hi) or source_lo<=0 or error_hi>source_lo*0x1p-20 or error_hi>envelope)return keep;
 const funded=@min(removed.paid,P.downRatio(P.downProduct(received,1e9),area));
 return .{.soil=removed.after,.vapor=after,.paid=removed.paid,.funded=funded,.native_received=received,.residual_density=(after-vapor)*1e9/area-(soil-removed.after)};
}

fn up(x:f128)f128{return std.math.nextAfter(f128,x,std.math.inf(f128));}
fn down(x:f128)f128{return std.math.nextAfter(f128,x,-std.math.inf(f128));}
