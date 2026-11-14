//! Nonnegative sub-quantum precision carry for the existing f32 hydrology arrays.
//! Bulk fields retain engine units (10^9 kg); carry and transfers use kg H2O/m².
//! This is numeric precision, not a biological or soil-water reservoir.
const std=@import("std");
pub const Amount=struct{bulk:f32,carry:f64};
fn up(x:f32) f32{return if(x==0) @bitCast(@as(u32,1)) else @bitCast(@as(u32,@bitCast(x))+1);}
fn down(x:f32) f32{return if(x==0) 0 else @bitCast(@as(u32,@bitCast(x))-1);}
pub fn quantumKg(bulk:f32,area:f64) f64 {
 if(!std.math.isFinite(bulk) or bulk<0 or !std.math.isFinite(area) or area<=0)return std.math.nan(f64);
 const gap=if(bulk==std.math.floatMax(f32)) @as(f64,bulk)-down(bulk) else @as(f64,up(bulk))-bulk;
 return gap*(1e9/area);
}
pub fn validCarry(bulk:f32,carry:f64,area:f64) bool {
 const quantum=quantumKg(bulk,area);
 return std.math.isFinite(carry) and carry>=0 and std.math.isFinite(quantum) and quantum>0 and carry<quantum;
}
pub fn requantize(bulk:f32,carry:f64,delta:f64,area:f64) ?Amount {
 if(!std.math.isFinite(bulk) or bulk<0 or !std.math.isFinite(carry) or carry<0 or !std.math.isFinite(delta) or !std.math.isFinite(area) or area<=0)return null;
 const kg_per_unit=1e9/area;
 if(!std.math.isFinite(kg_per_unit) or kg_per_unit<=0)return null;
 // Exact representable full-debit case: avoid subtracting bulk twice through
 // independently rounded unit conversions. This is equality, not a tolerance
 // that would permit overdrafts. The public supply uses this same balance.
 const available=@as(f64,bulk)*1e9/area+carry;
 if(delta<0 and -delta==available)return .{.bulk=0,.carry=0};
 const change=carry+delta;
 const estimate=@as(f64,bulk)+change/kg_per_unit;
 if(!std.math.isFinite(estimate) or estimate<0)return null;
 var rounded:f32=@floatCast(@min(estimate,@as(f64,std.math.floatMax(f32))));
 // Form the residual from the small change, avoiding large+small cancellation.
 var remainder=change+(@as(f64,bulk)-rounded)*kg_per_unit;
 var corrections:u8=0;
 while(remainder<0):(corrections+=1){
  if(rounded==0 or corrections>=8)return null;
  const lower=down(rounded);remainder+=(@as(f64,rounded)-lower)*kg_per_unit;rounded=lower;
 }
 while(remainder>=quantumKg(rounded,area)):(corrections+=1){
  if(rounded==std.math.floatMax(f32) or corrections>=8)return null;
  const higher=up(rounded);remainder-=(@as(f64,higher)-rounded)*kg_per_unit;rounded=higher;
 }
 if(!validCarry(rounded,remainder,area))return null;
 return .{.bulk=rounded,.carry=remainder};
}
/// Atomic: neither compartment changes if any transfer/state is invalid.
pub fn apply(surface:*f32,vapor:*f32,surface_carry:*f64,vapor_carry:*f64,area:f64,taken:f64,returned:f64,evaporated:f64) bool {
 if(!std.math.isFinite(taken) or taken<0 or !std.math.isFinite(returned) or returned<0 or !std.math.isFinite(evaporated) or evaporated<0)return false;
 const liquid=requantize(surface.*,surface_carry.*,returned-taken,area) orelse return false;
 const gas=requantize(vapor.*,vapor_carry.*,evaporated,area) orelse return false;
 surface.*=liquid.bulk;surface_carry.*=liquid.carry;vapor.*=gas.bulk;vapor_carry.*=gas.carry;
 return true;
}
test "precision carries retain tiny uptake and evaporation without hidden gain" {
 const area:f64=7669529600;var liquid:f32=115042.9453;var vapor:f32=766.953;var lc:f64=0;var vc:f64=0;
 const before=(@as(f64,liquid)+vapor)*1e9/area;var reserve:f64=0;
 for(0..100000)|_|{try std.testing.expect(apply(&liquid,&vapor,&lc,&vc,area,0.0001,0,0.00003));reserve+=0.00007;}
 try std.testing.expect(validCarry(liquid,lc,area) and validCarry(vapor,vc,area));
 const after=(@as(f64,liquid)+vapor)*1e9/area+lc+vc+reserve;
 try std.testing.expectApproxEqAbs(before,after,0.00000001);
}
test "carry-only water requantizes after weather drains bulk including zero and subnormal" {
 const area:f64=7669529600;
 const initial=requantize(115042.9453,0,-0.0001,area).?;
 // Weather consumes only represented bulk; the remainder is still real water.
 const drained=requantize(0,initial.carry,0,area).?;
 try std.testing.expect(drained.bulk>0);try std.testing.expect(validCarry(drained.bulk,drained.carry,area));
 try std.testing.expectApproxEqAbs(initial.carry,@as(f64,drained.bulk)*1e9/area+drained.carry,1e-15);
 const quantum=quantumKg(0,area);const tiny=requantize(0,quantum/2,0,area).?;
 try std.testing.expectEqual(@as(f32,0),tiny.bulk);try std.testing.expectEqual(quantum/2,tiny.carry);
 try std.testing.expect(validCarry(0,0,area));try std.testing.expect(!validCarry(0,quantum,area));
}
test "precision transfer rejects invalid or impossible state atomically" {
 var s:f32=0;var v:f32=0;var sc:f64=0;var vc:f64=0;
 try std.testing.expect(!apply(&s,&v,&sc,&vc,1,1,0,0));
 try std.testing.expectEqual(@as(f32,0),s);try std.testing.expectEqual(@as(f32,0),v);
 try std.testing.expect(!apply(&s,&v,&sc,&vc,1,0,0,std.math.inf(f64)));
 try std.testing.expect(requantize(std.math.floatMax(f32),0,1e100,1)==null);
 try std.testing.expect(requantize(1,-1,0,1)==null);
}

test "signed zero bulk remains compatible with legacy water" {
 try std.testing.expect(validCarry(-0.0,0,7669529600));
 const normalized=requantize(-0.0,0,0,7669529600).?;
 try std.testing.expect(normalized.bulk==0 and normalized.carry==0);
}


test "exact full represented balance can drain without cancellation rejection" {
 const area:f64=7669529600;
 var prng=std.Random.DefaultPrng.init(42);const rng=prng.random();
 for(0..100000)|_|{
  const bulk:f32=rng.float(f32)*100000;
  const carry=quantumKg(bulk,area)*rng.float(f64);
  const amount=@as(f64,bulk)*1e9/area+carry;
  const drained=requantize(bulk,carry,-amount,area).?;
  try std.testing.expect(drained.bulk==0 and drained.carry==0);
 }
}
