const std=@import("std");const M=@import("candidate.zig");const O=@import("original.zig");const H=@import("grazing_accessibility.zig");
fn initial(grazer:bool,swap:bool)M.Cell{
 var c=M.initialized(42);c.nutrient=0.12;
 const weak:usize=if(swap)1 else 0;const strong=1-weak;
 c.cohorts[weak]=.{.biomass=0.2,.support_mass=0.04,.organization=0.2,.structure=0,.lineage=1};
 c.cohorts[strong]=.{.biomass=0.2,.support_mass=0.04,.organization=0.2,.structure=0.7,.lineage=2};
 if(grazer)c.cohorts[2]=.{.biomass=0.1,.feeding=1,.lineage=3};return c;
}
fn totalC(c:M.Cell,air:f64)f64{return @as(f64,M.carbon(c))+air;}
fn audit(c:M.Cell,air:f64,oxygen:f64,carbon:f64,nutrient:f64)!void{try std.testing.expect(M.validCell(c,100));try std.testing.expect(air>=0 and oxygen>=0);try std.testing.expectApproxEqAbs(carbon,totalC(c,air),0.0003);try std.testing.expectApproxEqAbs(nutrient,@as(f64,M.nutrientTotal(c)),0.00003);}
test "support required, bounded intake, original zero coefficient parity, O2 and invalid guards"{
 var c=initial(true,false);const before=c;const carbon=M.carbon(c);const nutrient=M.nutrientTotal(c);
 const f=H.graze(M,&c,0.1,10,4);try std.testing.expect(f.consumed>0 and f.respired==f.consumed*0.25);
 try std.testing.expectApproxEqAbs(carbon,M.carbon(c)+f.respired,1e-6);try std.testing.expectApproxEqAbs(nutrient,M.nutrientTotal(c),1e-6);
 try std.testing.expect(before.cohorts[0].biomass-c.cohorts[0].biomass>before.cohorts[1].biomass-c.cohorts[1].biomass);
 var naked=before.cohorts[1];naked.support_mass=0;try std.testing.expectEqual(naked.biomass,H.accessible(naked,4));
 for([_]f32{0,0.01,2,1000})|days|{var candidate=initial(true,false);var original=O.initialized(42);original.nutrient=candidate.nutrient;for(candidate.cohorts,0..)|co,i|{inline for(std.meta.fields(M.Cohort))|field|@field(original.cohorts[i],field.name)=@field(co,field.name);}
 const a=H.graze(M,&candidate,days,10,0);const b=O.graze(&original,days,10);try std.testing.expectEqual(a.consumed,b.consumed);try std.testing.expectEqual(a.respired,b.respired);
 try std.testing.expectEqual(candidate.nutrient,original.nutrient);try std.testing.expectEqual(candidate.detritus,original.detritus);try std.testing.expectEqual(candidate.rng,original.rng);for(candidate.cohorts,original.cohorts)|ca,cb|{inline for(std.meta.fields(M.Cohort))|field|try std.testing.expectEqual(@field(ca,field.name),@field(cb,field.name));}}
 for([_]f32{0,1e-10,0.0001})|oxygen|{var t=initial(true,false);const flux=H.graze(M,&t,10000,oxygen,4);try std.testing.expect(flux.respired<=oxygen*1.000001);try std.testing.expect(M.validCell(t,100));}
 for([_]f32{-1,std.math.nan(f32),std.math.inf(f32)})|x|{var t=initial(true,false);const old=t;_=H.graze(M,&t,x,1,4);try std.testing.expectEqualDeep(old,t);_=H.graze(M,&t,1,x,4);try std.testing.expectEqualDeep(old,t);_=H.graze(M,&t,1,1,x);try std.testing.expectEqualDeep(old,t);}
 var invalid_strength=initial(true,false);const unchanged=invalid_strength;_=H.graze(M,&invalid_strength,1,1,4.001);try std.testing.expectEqualDeep(unchanged,invalid_strength);
 for([_]f32{std.math.floatTrueMin(f32),0.000001,0.2})|mass|{const all_support=M.Cohort{.biomass=mass,.support_mass=mass,.structure=1,.lineage=1};const amount=H.accessible(all_support,4);try std.testing.expect(amount>0 and amount<=mass);}
 var empty=M.initialized(1);_=H.graze(M,&empty,100,10,4);try std.testing.expectEqual(@as(f32,0),M.biomass(empty));
}
test "60day controlled competition, identical costs, slot reversal and strength sensitivity"{
 for([_]f32{0,1,2,4})|strength|for([_]f32{1,0.2})|light|for([_]f32{0,0.1,0.4,1})|feeding|for(0..2)|resources|{
  var final:[2][3]f32=undefined;
  for(0..2)|slot|{
   var c=initial(true,slot==1);c.cohorts[2].feeding=feeding;if(resources==1)c.nutrient=0.005;var air:f64=if(resources==1)0.02 else 10;var oxygen:f64=10;const carbon=totalC(c,air);const nutrient=@as(f64,M.nutrientTotal(c));var consumed:f64=0;M.accessibility_strength=strength;
   for(0..60*60)|tick|{
    const f=M.step(&c,.{.temperature=303,.depth_km=0.001,.light=light,.carbon_available=@floatCast(air),.oxygen_carbon_capacity=@floatCast(oxygen)},1440);
    air+=@as(f64,f.recycled)-f.fixed;oxygen+=@as(f64,f.fixed)-f.recycled;consumed+=f.grazed;try audit(c,air,oxygen,carbon,nutrient);
    if(tick+1==120 or tick+1==600 or tick+1==3600)std.debug.print("GRAZE_ASSAY coefficient={d} light={d} feeding={d} tight_resources={d} swap={d} day={d} weak={d:.8} strong={d:.8} consumer={d:.8} consumed={d:.8} carbon_error={e} nutrient_error={e}\n",.{strength,light,feeding,resources,slot,(tick+1)/60,c.cohorts[slot].biomass,c.cohorts[1-slot].biomass,c.cohorts[2].biomass,consumed,totalC(c,air)-carbon,@as(f64,M.nutrientTotal(c))-nutrient});
   }
   final[slot]=.{c.cohorts[slot].biomass,c.cohorts[1-slot].biomass,c.cohorts[2].biomass};
  }
  for(final[0],final[1])|a,b|try std.testing.expectApproxEqAbs(a,b,0.00001);
 };
}
