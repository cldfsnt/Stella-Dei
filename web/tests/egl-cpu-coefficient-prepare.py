#!/usr/bin/env python3
"""Isolated exact atmospheric relaxation cache, keyed by total-rate and dt bits."""
from pathlib import Path
import shutil,sys
source=Path(sys.argv[1]);out=Path(sys.argv[2]);shutil.copytree(source,out,dirs_exist_ok=True)
p=out/'simulation/planet.zig';s=p.read_text();needle='    transformedPoints: []Vec3,';assert needle in s;s=s.replace(needle,needle+'\n    qaCoefficient: []@import("../qa_coefficient_cache.zig").Entry = &.{},',1)
a=s.index('    pub fn deinit(');i=s.index('\n',a);s=s[:i]+'\n        self.allocator.free(self.qaCoefficient);'+s[i:]
a=s.index('    fn simulateAtmosphereWater(');s=s[:a]+'''    fn ensureQaCoefficient(self:*Planet)void {
        if(self.qaCoefficient.len==self.transformedPoints.len)return;
        const replacement=self.allocator.alloc(@import("../qa_coefficient_cache.zig").Entry,self.transformedPoints.len) catch return;
        @memset(replacement,.{});self.allocator.free(self.qaCoefficient);self.qaCoefficient=replacement;
    }
'''+s[a:]
a=s.index('    fn simulateAtmosphereWater(');needle='        if(!std.math.isFinite(dt) or dt<=0)return;';i=s.index(needle,a);s=s[:i]+s[i:].replace(needle,needle+'\n        self.ensureQaCoefficient();',1)
needle='            const coefficient=AtmosphereWater.coefficient32(vapor,total_rate,dt);';assert needle in s
s=s.replace(needle,'''            const coefficient=if(self.qaCoefficient.len==self.transformedPoints.len) blk:{
                if(phase.enabled and total_rate>0 and std.math.isFinite(total_rate)){phase.coefficient_checks+=1;if(!self.qaCoefficient[i].matches(total_rate,dt))phase.coefficient_misses+=1;}
                break :blk self.qaCoefficient[i].coefficient32(vapor,total_rate,dt);
            } else AtmosphereWater.coefficient32(vapor,total_rate,dt);''',1);p.write_text(s)
p=out/'qa_phase_metrics.zig';p.write_text(p.read_text()+'\npub var coefficient_checks:u64=0;pub var coefficient_misses:u64=0;\n')
p=out/'main.zig';s=p.read_text().replace('phase.enabled=true;','phase.coefficient_checks=0;phase.coefficient_misses=0;phase.enabled=true;');s=s.replace('  phase.enabled=false;','  phase.enabled=false;std.debug.print("COEFFICIENT_CACHE checks={d} misses={d} hits={d} bytes_per_cell=24\\n",.{phase.coefficient_checks,phase.coefficient_misses,phase.coefficient_checks-phase.coefficient_misses});',1);p.write_text(s)
(out/'qa_coefficient_cache.zig').write_text(r'''
//! Research only. Cache expm1 relaxation, never mass or the final coefficient.
const std=@import("std");const Reference=@import("simulation/atmosphere_water.zig");
fn nonnegative(x:f64)bool{return std.math.isFinite(x) and x>=0;}
pub const Entry=struct {
 rate_bits:u64=0,dt_bits:u64=0,relaxation:f64=0,
 pub fn matches(e:Entry,rate:f64,dt:f64)bool{return e.rate_bits==@as(u64,@bitCast(rate)) and e.dt_bits==@as(u64,@bitCast(dt));}
 pub fn coefficient32(e:*Entry,mass:f64,rate:f64,dt:f64)f32{
  if(!nonnegative(mass) or !nonnegative(rate) or !nonnegative(dt) or rate==0 or dt==0)return 0;
  if(!e.matches(rate,dt)){e.*=.{.rate_bits=@bitCast(rate),.dt_bits=@bitCast(dt),.relaxation=Reference.relaxation(dt,1/rate)};}
  // Preserve the original mass multiplication then rate division and f32 bound.
  var c:f32=@floatCast(mass*e.relaxation/rate);if(!std.math.isFinite(c) or c<=0)return 0;
  if(@as(f64,c)*rate>mass)c=@bitCast(@as(u32,@bitCast(c))-1);return c;
 }
};
test "cached coefficient exact bits, changing mass rate dt and bounds" {
 var e=Entry{};var n:usize=0;var rng=std.rand.DefaultPrng.init(2027);const random=rng.random();
 for(0..100000)|_|{
  const rate=@exp(random.float(f64)*40-30);const dt=@exp(random.float(f64)*20-10);const mass=@exp(random.float(f64)*50-20);
  for([_]f64{mass,mass*0.13,mass*0.9})|m|{const expected=Reference.coefficient32(m,rate,dt);const got=e.coefficient32(m,rate,dt);try std.testing.expectEqual(@as(u32,@bitCast(expected)),@as(u32,@bitCast(got)));try std.testing.expect(@as(f64,got)*rate<=m);n+=1;}
 }
 for([_]f64{0,-0.0,-1,1e-300,1e300,std.math.nan(f64),std.math.inf(f64)})|m|for([_]f64{0,-1,1e-300,1e300,std.math.nan(f64),std.math.inf(f64)})|r|for([_]f64{0,-1,1e-300,1e300,std.math.nan(f64),std.math.inf(f64)})|dt|{
  try std.testing.expectEqual(@as(u32,@bitCast(Reference.coefficient32(m,r,dt))),@as(u32,@bitCast(e.coefficient32(m,r,dt))));n+=1;
 };
 std.debug.print("COEFFICIENT_CACHE exact_f32_cases={d} mass_dynamic=true rate_dt_bit_keys=true bytes_per_entry={d}\n",.{n,@sizeOf(Entry)});
}
''')
