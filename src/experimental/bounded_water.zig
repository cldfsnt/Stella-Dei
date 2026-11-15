//! Phase-local conservative binary-grid water transfers. No physical defaults.
const std=@import("std");
pub const Scatter=struct{source:f64,target:f64,paid:[4]f64=.{0,0,0,0},quantum:f64=0};
pub const Gather=struct{sources:[4]f64,target:f64,paid:[4]f64=.{0,0,0,0},quantum:f64=0};
fn boundary(x:f64)f64{const e=(@as(u64,@bitCast(x))>>52)&0x7ff;if(e>=2046)return std.math.floatMax(f64);return @bitCast((e+1)<<52);}
fn sourceGrid(x:f64)f64{return if(x>0)x-std.math.nextAfter(f64,x,0) else 0;}
fn targetGrid(x:f64)f64{return std.math.nextAfter(f64,x,std.math.inf(f64))-x;}
fn units(x:f64,q:f64)?u64{if(x<=0)return 0;const n=@floor(@as(f128,x)/q);if(!std.math.isFinite(n) or n>0x1fffffffffffffff)return null;return @intFromFloat(n);}
fn amount(n:u64,q:f64)f64{return @as(f64,@floatFromInt(n))*q;}
fn exact(source:f64,target:f64,n:u64,q:f64)bool{@setFloatMode(.strict);const paid=amount(n,q);if(!std.math.isFinite(paid) or paid>source)return false;const a=source-paid;const b=target+paid;return std.math.isFinite(b) and (@as(f128,source)-a)==@as(f128,paid) and (@as(f128,b)-target)==@as(f128,paid);}
fn shares(wanted:[4]u64,budget:u64)[4]u64{var total:u128=0;for(wanted)|x|total+=x;var out=[_]u64{0,0,0,0};if(total==0)return out;for(wanted,0..)|x,i|out[i]=@intCast(@min(@as(u128,x),(@as(u128,budget)*x)/total));return out;}
pub fn scatter(source:f64,target:f64,wanted:[4]f64)Scatter{
 @setFloatMode(.strict);var out=Scatter{.source=source,.target=target};
 if(!std.math.isFinite(source) or source<=0 or !std.math.isFinite(target) or target<0)return out;
 const q=@max(sourceGrid(source),targetGrid(target));if(!std.math.isFinite(q) or q<=0)return out;out.quantum=q;
 const room=if(target==0)source else boundary(target)-target;const budget=units(@min(source,room),q) orelse return out;
 var requests:[4]u64=undefined;for(wanted,0..)|w,i|{if(!std.math.isFinite(w) or w<0)return out;requests[i]=units(w,q) orelse return out;}
 const grants=shares(requests,budget);var n:u64=0;for(grants)|x|n+=x;if(!exact(source,target,n,q))return out;
 const paid=amount(n,q);out.source=source-paid;out.target=target+paid;for(grants,0..)|x,i|out.paid[i]=amount(x,q);return out;
}
pub fn gather(sources:[4]f64,target:f64,wanted:[4]f64)Gather{
 @setFloatMode(.strict);var out=Gather{.sources=sources,.target=target};if(!std.math.isFinite(target) or target<0)return out;var q=targetGrid(target);
 for(sources,wanted)|x,w|{if(!std.math.isFinite(x) or x<0 or !std.math.isFinite(w) or w<0)return out;if(x>0 and w>0)q=@max(q,sourceGrid(x));}if(!std.math.isFinite(q) or q<=0)return out;out.quantum=q;
 const budget=if(target==0)@as(u64,1)<<53 else units(boundary(target)-target,q) orelse return out;var requests:[4]u64=undefined;
 for(sources,wanted,0..)|s,w,i|{if(!std.math.isFinite(w) or w<0)return out;requests[i]=units(@min(s,w),q) orelse return out;}
 const grants=shares(requests,budget);var n:u64=0;for(grants)|x|n+=x;const paid=amount(n,q);const after=target+paid;
 if(!std.math.isFinite(after) or @as(f128,after)-target!=@as(f128,paid))return out;
 for(sources,grants)|s,g|{const a=amount(g,q);if(a>s or @as(f128,s)-(s-a)!=@as(f128,a))return out;}
 out.target=after;for(grants,0..)|g,i|{out.paid[i]=amount(g,q);out.sources[i]-=out.paid[i];}return out;
}
pub fn lowerSum(a:f64,b:f64)f64{@setFloatMode(.strict);const s=a+b;const v=s-a;const error_term=(a-(s-v))+(b-v);return if(error_term<0)std.math.nextAfter(f64,s,0) else s;}
