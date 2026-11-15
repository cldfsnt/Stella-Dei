//! Isolated scalar-only physical transfer; no cohort allocation/fairness change.
const std=@import("std");
pub const Result=struct{source:f64,target:f64,paid:f64=0,quantum:f64=0,accepted:bool=false};
fn exactDifference(a:f128,b:f128)?f128{@setFloatMode(.strict);const s=a-b;const bb=s-a;const error_term=(a-(s-bb))+(-b-bb);if(!std.math.isFinite(s) or error_term!=0)return null;return s;}
pub fn transfer(source:f64,target:f64,requested:f64)Result{
 @setFloatMode(.strict);var out=Result{.source=source,.target=target};
 if(!std.math.isFinite(source) or !std.math.isFinite(target) or !std.math.isFinite(requested) or source<0 or target<0 or requested<0)return out;
 if(source==0 or requested==0){out.accepted=true;return out;}
 const want=@min(source,requested);const bound128=@as(f128,target)+want;if(!std.math.isFinite(bound128) or bound128>std.math.floatMax(f64))return out;
 var bound:f64=@floatCast(bound128);if(@as(f128,bound)<bound128)bound=std.math.nextAfter(f64,bound,std.math.inf(f64));
 const q=@max(source-std.math.nextAfter(f64,source,0),std.math.nextAfter(f64,bound,std.math.inf(f64))-bound);if(!std.math.isFinite(q) or q<=0)return out;out.quantum=q;
 const n=@floor(@as(f128,want)/q);const amount128=n*q;if(amount128<=0 or amount128>want)return out;
 const amount:f64=@floatCast(amount128);if(@as(f128,amount)!=amount128)return out;
 const after_source=source-amount;const after_target=target+amount;if(!std.math.isFinite(after_target) or after_source<0)return out;
 const debit=exactDifference(source,after_source) orelse return out;const credit=exactDifference(after_target,target) orelse return out;
 if(debit!=credit or debit!=amount128 or debit>requested)return out;
 out.source=after_source;out.target=after_target;out.paid=amount;out.accepted=true;return out;
}
