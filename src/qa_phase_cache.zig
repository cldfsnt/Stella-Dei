const std=@import("std");const W=@import("experimental/phase_reference.zig");const C=@import("experimental/phase_cache.zig").Cache;
const Production=@import("simulation/atmosphere_water.zig");
const Input=struct{liquid:f64,vapor:f64,saturation:f64,temperature:f64,rain:f64};
fn equal(a:?W.Phase,b:?W.Phase)!void{
 try std.testing.expectEqual(a==null,b==null);if(a)|p|{inline for(.{"liquid","vapor","evaporated","condensed","rain_rate"})|f|try std.testing.expectEqual(@as(u64,@bitCast(@field(p,f))),@as(u64,@bitCast(@field(b.?,f))));}
}
fn check(i:Input,dt:f64)!void{
 const reference=W.phase(i.liquid,i.vapor,i.saturation,i.temperature,dt,i.rain);
 try equal(reference,C.init(dt).phase(i.liquid,i.vapor,i.saturation,i.temperature,i.rain));
 try equal(reference,Production.PhaseStep.init(dt).phase(i.liquid,i.vapor,i.saturation,i.temperature,i.rain));
 try equal(reference,Production.phase(i.liquid,i.vapor,i.saturation,i.temperature,dt,i.rain));
}
test "cached phase exact field bits for finite randomized invalid and dt edges"{
 var random=std.Random.DefaultPrng.init(20271115);const r=random.random();
 const edges=[_]f64{0,-0.0,1e-320,1e-200,1e-12,1,60,360,1440,86400,1e300,std.math.floatMax(f64),-1,std.math.inf(f64),-std.math.inf(f64),std.math.nan(f64)};
 for(edges)|dt|{for(0..1000)|_|try check(.{.liquid=r.float(f64)*1e6,.vapor=r.float(f64)*1e6,.saturation=r.float(f64)*1e6,.temperature=250+r.float(f64)*70,.rain=r.float(f64)*1000},dt);}
 const base=Input{.liquid=1000,.vapor=120,.saturation=200,.temperature=293,.rain=3};
 for(edges)|x|{inline for(.{"liquid","vapor","saturation","temperature","rain"})|f|{var i=base;@field(i,f)=x;for(edges)|dt|try check(i,dt);}}
 for(0..20000)|_|{var i=base;inline for(.{"liquid","vapor","saturation","temperature","rain"})|f|@field(i,f)=@bitCast(r.int(u64));try check(i,@bitCast(r.int(u64)));}
 // Include distinct quiet NaN payload, signed zeros, overflow-producing finite sums.
 try check(.{.liquid=std.math.floatMax(f64),.vapor=std.math.floatMax(f64),.saturation=0,.temperature=300,.rain=std.math.floatMax(f64)},1e300);
 try check(.{.liquid=-0.0,.vapor=-0.0,.saturation=-0.0,.temperature=273.15,.rain=-0.0},-0.0);
 try check(base,@bitCast(@as(u64,0x7ff8000000000123)));
 std.debug.print("PHASE_PARITY 16000 bounded random +1280 field/dt edges +20000 random-bit +3 special cases; all5fields bitwise reference vs prototype, productionPhaseStep, productionScalar\n",.{});
}
noinline fn batch(comptime cached:bool,data:[]Input,dt:f64)u64{
 const c=if(cached)C.init(dt) else undefined;var hash:u64=0;
 for(data)|*i|{
  const p=if(cached)c.phase(i.liquid,i.vapor,i.saturation,i.temperature,i.rain).? else W.phase(i.liquid,i.vapor,i.saturation,i.temperature,dt,i.rain).?;
  i.liquid=p.liquid;i.vapor=p.vapor;i.rain=p.rain_rate;
  inline for(.{"liquid","vapor","evaporated","condensed","rain_rate"})|f|hash=(hash*%16777619)^@as(u64,@bitCast(@field(p,f)));
 }
 return hash;
}
test "40962 cells actual phase versus cached batch runtime dt"{
 const a=std.testing.allocator;const input=try a.alloc(Input,40962);defer a.free(input);const scratch=try a.alloc(Input,input.len);defer a.free(scratch);
 var random=std.Random.DefaultPrng.init(42);const r=random.random();for(input)|*i|i.*=.{.liquid=r.float(f64)*10000,.vapor=r.float(f64)*500,.saturation=r.float(f64)*500,.temperature=260+r.float(f64)*60,.rain=r.float(f64)*100};
 var hashes:[2]u64=undefined;
 for(0..7)|repeat|{
  // Reverse order every pass; inputs identical per implementation, evolving8ticks.
  for(0..2)|order|{const kind=order^(repeat%2);@memcpy(scratch,input);var h:u64=0;var timer=try std.time.Timer.start();
   for(0..8)|tick|{const dt:f64=360+@as(f64,@floatFromInt((repeat+tick)%3));h^=if(kind==0)batch(false,scratch,dt) else batch(true,scratch,dt);}
   const ns=timer.read();hashes[kind]=h;std.debug.print("PHASE_CACHE repeat={d} kind={d} cells={d} ticks=8 ns={d} hash={d}\n",.{repeat,kind,input.len,ns,h});
  }
  try std.testing.expectEqual(hashes[0],hashes[1]);
 }
}
