//! Browser-only caller: exact geometry reuse, never a biological/save-state cache.
//! Snapshot storage belongs to the Planet arena. Allocation failure keeps legacy uploads.
const std=@import("std");
pub const Key=struct{tilt:u32,radius:u32,vertices:usize,buffer:u32};
pub const Decision=struct{enabled:bool=false,changed:bool=true};
pub const Cache=struct{
 elevation:?[]f32=null,key:Key=.{.tilt=0,.radius=0,.vertices=0,.buffer=0},valid:bool=false,disabled:bool=false,normals_dirty:bool=true,
 pub fn observe(self:*Cache,allocator:std.mem.Allocator,heights:[]const f32,key:Key)Decision{
  if(self.disabled or heights.len==0)return .{};
  if(self.elevation==null)self.elevation=allocator.alloc(f32,heights.len) catch {self.disabled=true;return .{};};
  const previous=self.elevation.?;
  // A Planet's topology is immutable. Unexpected resizing falls back safely.
  if(previous.len!=heights.len){self.disabled=true;return .{};}
  const changed=!self.valid or !std.meta.eql(self.key,key) or !std.mem.eql(u8,std.mem.sliceAsBytes(previous),std.mem.sliceAsBytes(heights));
  if(changed){@memcpy(previous,heights);self.key=key;self.valid=true;}
  return .{.enabled=true,.changed=changed};
 }
 pub fn normalCompleted(self:*Cache)void{self.normals_dirty=true;}
 pub fn uploaded(self:*Cache)void{self.normals_dirty=false;}
};
test "exact elevation snapshot does not alias caller or scratch data"{
 var arena=std.heap.ArenaAllocator.init(std.testing.allocator);defer arena.deinit();var c=Cache{};var h=[_]f32{1,2,3};const key=Key{.tilt=0,.radius=1,.vertices=7,.buffer=8};
 try std.testing.expect(c.observe(arena.allocator(),&h,key).changed);c.uploaded();
 try std.testing.expect(!c.observe(arena.allocator(),&h,key).changed and !c.normals_dirty);
 h[1]=4;try std.testing.expect(c.observe(arena.allocator(),&h,key).changed);h[1]=2;try std.testing.expect(c.observe(arena.allocator(),&h,key).changed);
 c.normalCompleted();try std.testing.expect(c.normals_dirty and !c.observe(arena.allocator(),&h,key).changed);c.uploaded();try std.testing.expect(!c.normals_dirty);
}
test "tilt radius topology and destination buffer invalidate exactly"{
 var arena=std.heap.ArenaAllocator.init(std.testing.allocator);defer arena.deinit();var c=Cache{};const h=[_]f32{1};var key=Key{.tilt=0,.radius=1,.vertices=7,.buffer=8};_=c.observe(arena.allocator(),&h,key);
 key.tilt=0x80000000;try std.testing.expect(c.observe(arena.allocator(),&h,key).changed);
 key.radius=2;try std.testing.expect(c.observe(arena.allocator(),&h,key).changed);
 key.vertices=9;try std.testing.expect(c.observe(arena.allocator(),&h,key).changed);
 key.buffer=10;try std.testing.expect(c.observe(arena.allocator(),&h,key).changed);
 try std.testing.expect(!c.observe(arena.allocator(),&h,key).changed);
}
test "allocation failure and unexpected resize keep legacy path without repeated allocation"{
 var c=Cache{};const key=Key{.tilt=0,.radius=1,.vertices=7,.buffer=8};const h=[_]f32{1};try std.testing.expect(!c.observe(std.testing.failing_allocator,&h,key).enabled);try std.testing.expect(c.disabled);try std.testing.expect(!c.observe(std.testing.allocator,&h,key).enabled and c.elevation==null);
 var arena=std.heap.ArenaAllocator.init(std.testing.allocator);defer arena.deinit();c=.{};_=c.observe(arena.allocator(),&h,key);const bigger=[_]f32{1,2};try std.testing.expect(!c.observe(arena.allocator(),&bigger,key).enabled and c.disabled);
}
test "same geometry reload is reusable; changed values never skip even signed zero"{
 var arena=std.heap.ArenaAllocator.init(std.testing.allocator);defer arena.deinit();var c=Cache{};const key=Key{.tilt=0,.radius=1,.vertices=7,.buffer=8};const h=[_]f32{0};_=c.observe(arena.allocator(),&h,key);const same=[_]f32{0};try std.testing.expect(!c.observe(arena.allocator(),&same,key).changed);const changed=[_]f32{@bitCast(@as(u32,0x80000000))};try std.testing.expect(c.observe(arena.allocator(),&changed,key).changed);
}
