#!/usr/bin/env python3
"""Isolated exact latitude-transcendental cache. Production sources are untouched."""
from pathlib import Path
import shutil,sys
source=Path(sys.argv[1]);out=Path(sys.argv[2]);shutil.copytree(source,out,dirs_exist_ok=True)
p=out/'simulation/planet.zig';s=p.read_text();needle='    transformedPoints: []Vec3,';assert needle in s;s=s.replace(needle,needle+'\n    qaLatitude: []@import("../qa_latitude_cache.zig").Entry = &.{},',1)
a=s.index('    pub fn deinit(');i=s.index('\n',a);s=s[:i]+'\n        self.allocator.free(self.qaLatitude);'+s[i:]
a=s.index('    fn simulateWater(');s=s[:a]+'''    fn ensureQaLatitude(self:*Planet)void {
        if(self.qaLatitude.len==self.vertices.len)return;
        const replacement=self.allocator.alloc(@import("../qa_latitude_cache.zig").Entry,self.vertices.len) catch return;
        for(self.vertices,replacement)|vertex,*entry|entry.*=@import("../qa_latitude_cache.zig").Entry.init(vertex.z());
        self.allocator.free(self.qaLatitude);self.qaLatitude=replacement;
    }
'''+s[a:]
a=s.index('                    var latitude = std.math.acos(vert.z());');b=s.index('                    // note:',a)
s=s[:a]+'''                    const latitude_sine=if(self.qaLatitude.len==self.vertices.len)self.qaLatitude[i].sample(vert.z()) else @import("../qa_latitude_cache.zig").value(vert.z());
'''+s[b:];s=s.replace('spinRate * 2.0 * @sin(latitude) * dt','spinRate * 2.0 * latitude_sine * dt',1)
needle='        if (dt < 15000) {';assert needle in s;s=s.replace(needle,needle+'\n            self.ensureQaLatitude();',1);p.write_text(s)
(out/'qa_latitude_cache.zig').write_text(r'''
//! Research only. Cache the original acos/sign/sin value, not an algebraic approximation.
const std=@import("std");
pub fn value(z:f32)f32{var latitude=std.math.acos(z);if(latitude>std.math.pi/2.0)latitude=-latitude;return @sin(latitude);}
pub const Entry=struct {
 z_bits:u32,sine:f32,
 pub fn init(z:f32)Entry{return .{.z_bits=@bitCast(z),.sine=value(z)};}
 pub fn sample(e:*Entry,z:f32)f32{const bits:u32=@bitCast(z);if(bits!=e.z_bits)e.*=init(z);return e.sine;}
};
fn reference(z:f32)f32{var latitude=std.math.acos(z);if(latitude>std.math.pi/2.0)latitude=-latitude;return @sin(latitude);}
test "exact cached latitude values and bit-key refresh" {
 var rng=std.rand.DefaultPrng.init(2027);const random=rng.random();var e=Entry.init(0);
 for(0..100000)|_|{const z=random.float(f32)*2-1;const expected=reference(z);try std.testing.expectEqual(@as(u32,@bitCast(expected)),@as(u32,@bitCast(e.sample(z))));try std.testing.expectEqual(@as(u32,@bitCast(expected)),@as(u32,@bitCast(e.sample(z))));}
 for([_]f32{-1,-0.0,0,1})|z|{try std.testing.expectEqual(@as(u32,@bitCast(reference(z))),@as(u32,@bitCast(e.sample(z))));try std.testing.expectEqual(@as(u32,@bitCast(z)),e.z_bits);}
 std.debug.print("LATITUDE_CACHE samples=100004 repeated_reads=100000 exact_bits=true bytes_per_vertex={d}\n",.{@sizeOf(Entry)});
}
''')
