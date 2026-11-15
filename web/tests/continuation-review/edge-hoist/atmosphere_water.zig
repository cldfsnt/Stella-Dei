//! Phenomenological column water cycle, not energy-balanced weather.
//! Mass units are arbitrary but identical across liquid/vapor/rain. Times are s;
//! geometry and wind are km and km/s. No biology-dependent constants.
const std=@import("std");
pub const evaporation_seconds:f64=86400;
pub const condensation_seconds:f64=3600;
pub const rain_memory_seconds:f64=86400;
pub const Phase=struct{liquid:f64,vapor:f64,evaporated:f64,condensed:f64,rain_rate:f64};
fn finiteNonnegative(x:f64) bool{return std.math.isFinite(x) and x>=0;}
pub fn relaxation(dt:f64,tau:f64) f64{return -std.math.expm1(-dt/tau);}
pub fn phase(liquid:f64,vapor:f64,saturation:f64,temperature:f64,dt:f64,old_rain_rate:f64) ?Phase {
 return PhaseStep.init(dt).phase(liquid,vapor,saturation,temperature,old_rain_rate);
}
/// Per-tick coefficients: construct once with init, then reuse across cells.
/// Pure arithmetic only; no cached world, geometry or persistent state.
pub const PhaseStep=struct{
 dt:f64,evaporation:f64=0,condensation:f64=0,rain_memory:f64=0,
 pub fn init(dt:f64)PhaseStep{
  var c=PhaseStep{.dt=dt};if(!std.math.isFinite(dt) or dt<=0)return c;
  c.evaporation=relaxation(dt,evaporation_seconds);c.condensation=relaxation(dt,condensation_seconds);c.rain_memory=relaxation(dt,rain_memory_seconds);return c;
 }
 pub fn phase(c:PhaseStep,liquid:f64,vapor:f64,saturation:f64,temperature:f64,old_rain_rate:f64)?Phase{
  if(!finiteNonnegative(liquid) or !finiteNonnegative(vapor) or !finiteNonnegative(saturation) or !std.math.isFinite(temperature) or !std.math.isFinite(c.dt) or c.dt<0 or !finiteNonnegative(old_rain_rate))return null;
  if(c.dt==0)return .{.liquid=liquid,.vapor=vapor,.evaporated=0,.condensed=0,.rain_rate=old_rain_rate};
  const evap=if(temperature>273.15)@min(liquid,@max(0,saturation-vapor)*c.evaporation) else 0;
  const moist=vapor+evap;const rain=@min(moist,@max(0,moist-saturation)*c.condensation);const a=c.rain_memory;
  return .{.liquid=liquid-evap+rain,.vapor=moist-rain,.evaporated=evap,.condensed=rain,.rain_rate=old_rain_rate*(1-a)+(rain/c.dt*86400)*a};
 }
};
pub fn edgeRate(from:[3]f64,to:[3]f64,wind:[3]f64) f64 {
 var d:[3]f64=undefined;var length2:f64=0;var dot:f64=0;
 for(0..3)|i|{if(!std.math.isFinite(from[i]) or !std.math.isFinite(to[i]) or !std.math.isFinite(wind[i]))return 0;d[i]=to[i]-from[i];length2+=d[i]*d[i];dot+=wind[i]*d[i];}
 if(length2<=0 or !std.math.isFinite(length2) or !std.math.isFinite(dot))return 0;
 // Projected speed / edge distance = dot(wind, displacement)/distance².
 return @max(0,dot/length2);
}
pub fn coefficient(mass:f64,total_rate:f64,dt:f64) f64 {
 if(!finiteNonnegative(mass) or !finiteNonnegative(total_rate) or !finiteNonnegative(dt) or total_rate==0 or dt==0)return 0;
 return mass*relaxation(dt,1/total_rate)/total_rate;
}
/// Scratch coefficient must not round UP enough to spend more than donor mass.
pub fn coefficient32(mass:f64,total_rate:f64,dt:f64) f32 {
 var c:f32=@floatCast(coefficient(mass,total_rate,dt));
 if(!std.math.isFinite(c) or c<=0)return 0;
 if(@as(f64,c)*total_rate>mass)c=@bitCast(@as(u32,@bitCast(c))-1);
 return c;
}
test "phase conserves mass never rains below saturation and has bounded finite rates" {
 const e=phase(1000,0,200,293.15,360,0).?;
 try std.testing.expectApproxEqAbs(@as(f64,1000),e.liquid+e.vapor,1e-10);
 try std.testing.expect(e.evaporated>0 and e.evaporated<1);try std.testing.expectEqual(@as(f64,0),e.condensed);
 const c=phase(0,400,200,293.15,1440,0).?;
 try std.testing.expect(c.condensed>0 and c.condensed<200);try std.testing.expectApproxEqAbs(@as(f64,400),c.liquid+c.vapor,1e-10);
 try std.testing.expectEqual(@as(f64,0),phase(100,0,200,270,360,0).?.evaporated);
 try std.testing.expect(phase(-1,0,1,293,360,0)==null);
}
test "rain diagnostic is a correctly weighted daily-rate mean not timestep multiplied" {
 const dt:f64=360;const rain:f64=2;const alpha=relaxation(dt,rain_memory_seconds);
 const initial_rate:f64=rain/dt*86400;
 // Keep constant supersaturation producing the requested per-step rainfall.
 const excess=rain/relaxation(dt,condensation_seconds);
 const p=phase(0,200+excess,200,293,dt,initial_rate).?;
 try std.testing.expectApproxEqRel(initial_rate,p.rain_rate,1e-12);
 try std.testing.expectApproxEqRel(initial_rate*alpha,phase(0,200+excess,200,293,dt,0).?.rain_rate,1e-12);
}
test "transport follows velocity and distance with donor-bounded outgoing budget" {
 const a=[3]f64{0,0,0};const b=[3]f64{100,0,0};
 try std.testing.expectEqual(@as(f64,0),edgeRate(a,b,.{0,0,0}));
 try std.testing.expectEqual(@as(f64,0),edgeRate(a,b,.{-0.01,0,0}));
 try std.testing.expectApproxEqAbs(@as(f64,0.0001),edgeRate(a,b,.{0.01,0,0}),1e-15);
 for([_]f64{1,60,360,1440,1e6})|dt|{const r:f64=0.1;const c=coefficient32(100,r,dt);try std.testing.expect(@as(f64,c)*r<=100);try std.testing.expect(c>=0);}
}
test "phase one-day and fifteen-day outcomes converge at 1 60 360 1440 second steps" {
 for([_]f64{86400,15*86400})|duration|{
  var reference:f64=0;
  for([_]f64{1,60,360,1440},0..)|dt,j|{
   var liquid:f64=1000;var vapor:f64=0;var elapsed:f64=0;
   while(elapsed<duration){const step=@min(dt,duration-elapsed);const p=phase(liquid,vapor,200,293.15,step,0).?;liquid=p.liquid;vapor=p.vapor;elapsed+=step;}
   if(j==0)reference=vapor;
   try std.testing.expectApproxEqAbs(@as(f64,1000),liquid+vapor,1e-7);
   try std.testing.expectApproxEqAbs(reference,vapor,1e-7);
   std.debug.print("PHASE_DT days={d} dt={d} vapor={d} mass_error={d}\n",.{duration/86400,dt,vapor,liquid+vapor-1000});
  }
 }
}
test "two-cell coupled exchange and gather transport stay conservative across timesteps" {
 for([_]f64{86400,15*86400})|duration|{
 var reference:[2]f64=undefined;
 for([_]f64{1,60,360,1440},0..)|dt,j|{
  var liquid=[2]f64{1000,1000};var vapor=[2]f64{0,0};var elapsed:f64=0;
  while(elapsed<duration){const step=@min(dt,duration-elapsed);
   for(0..2)|i|{const p=phase(liquid[i],vapor[i],if(i==0)200 else 100,293.15,step,0).?;liquid[i]=p.liquid;vapor[i]=p.vapor;}
   const rate:f64=0.0001;const moved=coefficient(vapor[0],rate,step)*rate;vapor[0]-=moved;vapor[1]+=moved;
   try std.testing.expect(liquid[0]>=0 and liquid[1]>=0 and vapor[0]>=0 and vapor[1]>=0);elapsed+=step;
  }
  if(j==0)reference=liquid;
  const total=liquid[0]+liquid[1]+vapor[0]+vapor[1];try std.testing.expectApproxEqAbs(@as(f64,2000),total,1e-6);
  std.debug.print("COUPLED_DT days={d} dt={d} liquid={any} vapor={any} liquid_error_vs1s={any}\n",.{duration/86400,dt,liquid,vapor,[2]f64{liquid[0]-reference[0],liquid[1]-reference[1]}});
 }
}

}

test "f32 scratch gather is bounded and conservative within float roundoff" {
    const points=[4][3]f64{.{0,0,0},.{100,0,0},.{0,100,0},.{100,100,0}};
    const winds=[4][3]f64{.{0.03,0.01,0},.{-0.02,0.01,0},.{0.02,-0.02,0},.{-0.01,-0.01,0}};
    for([_]f64{1,60,360,1440})|dt|{
        var mass=[4]f32{100,200,50,0};const total:f64=350;
        var elapsed:f64=0;
        while(elapsed<86400){
            const step=@min(dt,86400-elapsed);var coeff:[4]f32=undefined;var next:[4]f32=undefined;
            for(0..4)|i|{
                var rate:f64=0;for(0..4)|j|rate+=edgeRate(points[i],points[j],winds[i]);
                coeff[i]=coefficient32(mass[i],rate,step);

            }
            for(0..4)|i|{
                var own_rate:f64=0;for(0..4)|j|own_rate+=edgeRate(points[i],points[j],winds[i]);
                var gathered:f64=@max(0,@as(f64,mass[i])-@as(f64,coeff[i])*own_rate);for(0..4)|j|gathered+=@as(f64,coeff[j])*edgeRate(points[j],points[i],winds[j]);
                next[i]=@floatCast(gathered);try std.testing.expect(std.math.isFinite(next[i]) and next[i]>=0);
            }
            mass=next;elapsed+=step;
        }
        var actual:f64=0;for(mass)|m|actual+=m;
        std.debug.print("FLOAT_GATHER dt={d} relative_mass_error={d}\n",.{dt,(actual-total)/total});
        try std.testing.expectApproxEqRel(total,actual,0.0001);
    }
}
