const std=@import("std");const X=@import("experimental/hydration_exchange.zig");const M=X.M;const P=@import("simulation/microbes.zig");
const area:f64=7669529600;
fn cell(r:f32)M.Cell{var c=M.initialized(123);c.cohorts[0]=.{.biomass=0.2,.support_mass=0.04,.organization=0.2,.lineage=1,.retention_allocation=r,.stored_water=if(r>0)0.05 else 0};return c;}
fn env()M.Environment{return .{.temperature=300,.depth_km=999,.light=1,.carbon_available=2,.oxygen_carbon_capacity=2};}
test "audit nominal depth and hydration have no material influence" {
 for([_]f32{0,0.001,1000})|pool|for([_]f32{0,0.5})|r|{
  var a=cell(r);var b=a;var al=pool;var bl=pool;var av:f32=0;var bv:f32=0;
  var e=env();var other=e;other.depth_km=std.math.nan(f32);other.qa_hydration=.{std.math.nan(f32),std.math.inf(f32),1,-1};e.qa_hydration=.{0,0,0,0};
  const af=X.step(&a,&al,&av,area,e,1440).?;const bf=X.step(&b,&bl,&bv,area,other,1440).?;
  try std.testing.expectEqualDeep(a,b);try std.testing.expectEqualDeep(af,bf);try std.testing.expectEqual(al,bl);try std.testing.expectEqual(av,bv);
 };
}
test "audit zero allocation parity across repeated ordinary intervals" {
 for([_]f32{0,0.001,1000})|initial|for([_]f32{60,1440,3600})|dt|{
  var c=cell(0);var p=P.initialized(123);inline for(std.meta.fields(P.Cohort))|f|@field(p.cohorts[0],f.name)=@field(c.cohorts[0],f.name);
  var liquid=initial;var vapor:f32=0;
  for(0..48)|i|{
   var e=env();e.light=if(i%2==0)1 else 0;
   const f=X.step(&c,&liquid,&vapor,area,e,dt).?;
   const pf=P.step(&p,.{.temperature=e.temperature,.depth_km=@floatCast(@as(f64,initial)*(1e9/area)/1e6),.light=e.light,.carbon_available=e.carbon_available,.oxygen_carbon_capacity=e.oxygen_carbon_capacity},dt);
   inline for(std.meta.fields(P.Flux))|field|try std.testing.expectEqual(@field(pf,field.name),@field(f,field.name));
   for(c.cohorts,p.cohorts)|a,b|{inline for(std.meta.fields(P.Cohort))|field|try std.testing.expectEqual(@field(b,field.name),@field(a,field.name));}
   try std.testing.expectEqual(p.nutrient,c.nutrient);try std.testing.expectEqual(p.detritus,c.detritus);try std.testing.expectEqual(p.rng,c.rng);try std.testing.expectEqual(initial,liquid);try std.testing.expectEqual(@as(f32,0),vapor);
  }
 };
}
test "audit represented take and deposit receipts" {
 for([_]f64{1,0.130386,-0.0+1e-6,1e6})|conv|for([_]f32{0,1e-20,0.001,1,1e20})|initial|for([_]f64{0,1e-20,0.0001,1,1e10})|want|{
  var pool=initial;const paid=X.take(&pool,want,conv);try std.testing.expect(paid>=0 and paid<=want);try std.testing.expectEqual((@as(f64,initial)-pool)*conv,paid);
  var escrow=paid;X.deposit(&pool,&escrow,conv);try std.testing.expect(pool<=initial and escrow>=0);try std.testing.expectApproxEqAbs(@as(f64,initial)*conv,@as(f64,pool)*conv+escrow,@max(1e-30,@as(f64,initial)*conv*4*std.math.floatEps(f64)));
 };
}
test "audit invalid explicit inputs refuse atomically" {
 for(0..11)|which|{
  var c=cell(0.5);var liquid:f32=1;var vapor:f32=0;var a=area;var dt:f32=1440;var e=env();
  switch(which){0=>a=0,1=>a=-1,2=>a=std.math.nan(f64),3=>a=std.math.inf(f64),4=>liquid=-1,5=>vapor=std.math.inf(f32),6=>e.temperature=std.math.nan(f32),7=>e.light=-1,8=>e.carbon_available=-1,9=>e.oxygen_carbon_capacity=std.math.nan(f32),else=>dt=0}
  const before=c;const lbits:@TypeOf(@as(u32,0))=@bitCast(liquid);const vbits:u32=@bitCast(vapor);
  try std.testing.expect(X.step(&c,&liquid,&vapor,a,e,dt)==null);try std.testing.expectEqualDeep(before,c);try std.testing.expectEqual(lbits,@as(u32,@bitCast(liquid)));try std.testing.expectEqual(vbits,@as(u32,@bitCast(vapor)));
 }
}
test "audit finite inputs whose derived depth overflows require atomic refusal" {
 var c=cell(0.5);c.liquid_return=0.1;var liquid:f32=1;var vapor:f32=0;const before=c;
 const result=X.step(&c,&liquid,&vapor,1e-250,env(),1440);
 std.debug.print("DERIVED_DEPTH_OVERFLOW accepted={} model_changed={} liquid={d} vapor={d}\n",.{result!=null,!std.meta.eql(before,c),liquid,vapor});
 try std.testing.expect(result==null);try std.testing.expectEqualDeep(before,c);try std.testing.expectEqual(@as(f32,1),liquid);try std.testing.expectEqual(@as(f32,0),vapor);
}
