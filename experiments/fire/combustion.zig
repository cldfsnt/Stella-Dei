//! Isolated transaction planner. Not hooked into the game or a weather model.
//! Masses are kg/m². Caller must supply measured liquid/ice AND tissue/detrital
//! water. Unknown moisture must never be converted to zero by an adapter.
const std=@import("std");
pub const Tissue=struct{carbon:f64=0,support:f64=0,water:f64=0};
pub const State=struct{
 live:[4]Tissue=.{.{}}**4,detritus:f64=0,detrital_water:f64=0,
 external_water:f64=0,nutrient:f64=0,oxygen:f64=0,carbon_dioxide:f64=0,
 moisture_known:bool=false,
};
pub const Failure=enum{none,invalid,submerged,moisture_unknown,wet_fuel,no_fuel,no_oxygen,precision};
pub const Result=struct{
 failure:Failure,after:State,burned_carbon:f64=0,oxygen_used:f64=0,co2_produced:f64=0,nutrient_released:f64=0,
 live_removed:[4]f64=.{0}**4,detritus_removed:f64=0,
 pub fn success(self:@This())bool{return self.failure==.none;}
};
fn valid(x:f64)bool{return std.math.isFinite(x) and x>=0;}
fn reject(before:State,reason:Failure)Result{return .{.failure=reason,.after=before};}
/// Intentionally conservative ignition: no exterior water/ice and zero measured
/// stored water in ALL available fuel. No moisture threshold invented for aquatic
/// organisms, no fire-resistance bonus inferred from morphology. Heat omitted.
pub fn plan(before:State,request_carbon:f64)Result{
 if(!valid(request_carbon) or request_carbon==0 or !valid(before.detritus) or !valid(before.detrital_water) or !valid(before.external_water) or !valid(before.nutrient) or !valid(before.oxygen) or !valid(before.carbon_dioxide))return reject(before,.invalid);
 var fuel=before.detritus;
 for(before.live)|c|{if(!valid(c.carbon) or !valid(c.support) or !valid(c.water) or c.support>c.carbon)return reject(before,.invalid);fuel+=c.carbon;}
 if(!valid(fuel))return reject(before,.invalid);
 if(before.external_water>0)return reject(before,.submerged);
 if(!before.moisture_known)return reject(before,.moisture_unknown);
 if(before.detrital_water>0)return reject(before,.wet_fuel);
 for(before.live)|c|{if(c.water>0)return reject(before,.wet_fuel);}
 if(fuel==0)return reject(before,.no_fuel);
 if(before.oxygen==0)return reject(before,.no_oxygen);
 const budget=@min(request_carbon,@min(fuel,before.oxygen*(12.0/32.0)));
 const fraction=budget/fuel;
 var out=Result{.failure=.none,.after=before};
 var live_removed:f64=0;
 for(before.live,0..)|c,i|{
  const after=c.carbon*(1-fraction);
  const removed=c.carbon-after;
  out.after.live[i].carbon=after;
  out.after.live[i].support=if(c.carbon>0)c.support*(after/c.carbon) else 0;
  // No water is deleted: nonzero physiological reserve rejected above.
  out.live_removed[i]=removed;live_removed+=removed;
 }
 out.after.detritus=before.detritus*(1-fraction);
 out.detritus_removed=before.detritus-out.after.detritus;
 out.burned_carbon=live_removed+out.detritus_removed;
 out.oxygen_used=out.burned_carbon*(32.0/12.0);
 out.co2_produced=out.burned_carbon*(44.0/12.0);
 out.nutrient_released=live_removed*0.1;
 if(out.burned_carbon<=0 or out.burned_carbon>budget or out.oxygen_used>before.oxygen)return reject(before,.precision);
 out.after.oxygen=before.oxygen-out.oxygen_used;
 out.after.carbon_dioxide=before.carbon_dioxide+out.co2_produced;
 out.after.nutrient=before.nutrient+out.nutrient_released;
 if(!valid(out.after.carbon_dioxide) or !valid(out.after.nutrient))return reject(before,.precision);
 // Refuse lost atmospheric/nutrient updates; a production f32 adapter must also
 // read back its own committed values and reject before mutating on mismatch.
 if(out.after.oxygen==before.oxygen or out.after.carbon_dioxide==before.carbon_dioxide or (out.nutrient_released>0 and out.after.nutrient==before.nutrient))return reject(before,.precision);
 if(@abs((before.oxygen-out.after.oxygen)-out.oxygen_used)>out.oxygen_used*1e-12 or @abs((out.after.carbon_dioxide-before.carbon_dioxide)-out.co2_produced)>out.co2_produced*1e-12)return reject(before,.precision);
 return out;
}
fn carbon(s:State)f64{var c=s.detritus+s.carbon_dioxide*(12.0/44.0);for(s.live)|t|c+=t.carbon;return c;}
fn nutrient(s:State)f64{var n=s.nutrient;for(s.live)|t|n+=t.carbon*0.1;return n;}
test "actual carbon oxidation preserves carbon nutrient support and total reacting mass"{
 const before=State{.live=.{.{.carbon=1,.support=0.2},.{.carbon=0.5,.support=0.1},.{},.{}},.detritus=0.5,.nutrient=0.2,.oxygen=8,.carbon_dioxide=1,.moisture_known=true};
 const r=plan(before,1);try std.testing.expect(r.success());
 try std.testing.expectApproxEqAbs(carbon(before),carbon(r.after),1e-12);
 try std.testing.expectApproxEqAbs(nutrient(before),nutrient(r.after),1e-12);
 try std.testing.expectApproxEqAbs(r.burned_carbon+r.oxygen_used,r.co2_produced,1e-12);
 for(r.after.live)|t|try std.testing.expect(t.support<=t.carbon and t.carbon>=0);
 try std.testing.expectApproxEqAbs(@as(f64,0.1),r.after.live[0].support,1e-12);
}
test "water unknown moisture invalid and oxygen rejections are atomic"{
 const base=State{.live=.{.{.carbon=1},.{},.{},.{}},.oxygen=8,.moisture_known=true};
 var s=base;s.external_water=1;var r=plan(s,1);try std.testing.expectEqual(Failure.submerged,r.failure);try std.testing.expectEqualDeep(s,r.after);
 s=base;s.live[0].water=0.000001;r=plan(s,1);try std.testing.expectEqual(Failure.wet_fuel,r.failure);try std.testing.expectEqualDeep(s,r.after);
 s=base;s.moisture_known=false;r=plan(s,1);try std.testing.expectEqual(Failure.moisture_unknown,r.failure);try std.testing.expectEqualDeep(s,r.after);
 s=base;s.oxygen=0;r=plan(s,1);try std.testing.expectEqual(Failure.no_oxygen,r.failure);try std.testing.expectEqualDeep(s,r.after);
 s=base;s.live[0].support=2;r=plan(s,1);try std.testing.expectEqual(Failure.invalid,r.failure);try std.testing.expectEqualDeep(s,r.after);
}
test "oxygen limits burning no recovery or protected morphology is invented"{
 var s=State{.live=.{.{.carbon=1,.support=0.5},.{.carbon=1},.{},.{}},.oxygen=1,.moisture_known=true};
 const r=plan(s,2);try std.testing.expect(r.success());try std.testing.expect(r.oxygen_used<=s.oxygen);
 try std.testing.expectEqual(r.live_removed[0],r.live_removed[1]);
 s=r.after;const again=plan(s,2);try std.testing.expect(!again.success());try std.testing.expectEqualDeep(s,again.after);
}
test "unrepresentable large background refuses instead of silently losing carbon"{
 const s=State{.live=.{.{.carbon=1},.{},.{},.{}},.oxygen=8,.carbon_dioxide=1e30,.moisture_known=true};
 const r=plan(s,0.1);try std.testing.expectEqual(Failure.precision,r.failure);try std.testing.expectEqualDeep(s,r.after);
}

test "oxygen subtraction must actually be represented"{
 const s=State{.live=.{.{.carbon=1},.{},.{},.{}},.oxygen=1e30,.moisture_known=true};
 const r=plan(s,0.1);try std.testing.expectEqual(Failure.precision,r.failure);try std.testing.expectEqualDeep(s,r.after);
}
test "no fuel and wet detritus cannot produce effects"{
 const empty=State{.oxygen=8,.moisture_known=true};try std.testing.expectEqual(Failure.no_fuel,plan(empty,1).failure);
 var wet=empty;wet.detritus=1;wet.detrital_water=0.1;const r=plan(wet,1);try std.testing.expectEqual(Failure.wet_fuel,r.failure);try std.testing.expectEqualDeep(wet,r.after);
}

test "repeated accepted transactions cannot regenerate fuel or overspend request"{
 var s=State{.live=.{.{.carbon=1,.support=0.2},.{.carbon=0.7,.support=0.1},.{},.{}},.detritus=0.3,.nutrient=0.2,.oxygen=10,.carbon_dioxide=1,.moisture_known=true};
 const initial=s;var accepted:usize=0;
 for(0..100)|_|{const r=plan(s,0.01);if(!r.success())break;try std.testing.expect(r.burned_carbon<=0.01);try std.testing.expect(r.after.oxygen>=0);try std.testing.expect(r.after.live[0].carbon<=s.live[0].carbon);s=r.after;accepted+=1;}
 try std.testing.expect(accepted>0);try std.testing.expectApproxEqAbs(carbon(initial),carbon(s),1e-10);try std.testing.expectApproxEqAbs(nutrient(initial),nutrient(s),1e-10);
}
