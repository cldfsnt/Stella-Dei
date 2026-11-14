//! Bounded targets from actually rendered, de-cluttered colony glyphs.
//! Read-only inspection only: never redirects seeding or god tools.
const std=@import("std");
pub const Target=struct{cell:usize,x:f32,y:f32,scale:f32};
pub const List=struct{
 items:[64]Target=undefined,count:usize=0,
 pub fn add(self:*List,t:Target) void {
  if(self.count==self.items.len or !std.math.isFinite(t.x) or !std.math.isFinite(t.y) or !std.math.isFinite(t.scale) or t.scale<=0)return;
  self.items[self.count]=t;self.count+=1;
 }
 pub fn pick(self:*const List,x:f32,y:f32) ?usize {
  if(!std.math.isFinite(x) or !std.math.isFinite(y))return null;
  // Preserve precise root taps before testing overlapping upright bodies.
  var root:?usize=null;var nearest:f32=64;
  for(self.items[0..self.count])|t|{const dx=(x-t.x)/t.scale;const dy=(y-t.y)/t.scale;const d=dx*dx+dy*dy;if(d<=nearest){nearest=d;root=t.cell;}}
  if(root) |cell| return cell;
  // Later painted glyphs win body overlaps. Bounds include atlas and fallback canopy.
  var i=self.count;while(i>0){i-=1;const t=self.items[i];
   if(x>=t.x-22*t.scale and x<=t.x+22*t.scale and y>=t.y-41*t.scale and y<=t.y+8*t.scale)return t.cell;
  }return null;
 }
};
test "root and body select rendered cell, not terrain neighbour" {
 var targets=List{};targets.add(.{.cell=42,.x=100,.y=200,.scale=1});
 try std.testing.expectEqual(@as(?usize,42),targets.pick(100,200));
 try std.testing.expectEqual(@as(?usize,42),targets.pick(100,175));
 try std.testing.expectEqual(@as(?usize,null),targets.pick(100,150));
 targets.add(.{.cell=43,.x=110,.y=200,.scale=1});try std.testing.expectEqual(@as(?usize,43),targets.pick(105,180));
 targets.count=0;try std.testing.expectEqual(@as(?usize,null),targets.pick(100,200));
}
test "bounded, invalid and scaled targets" {
 var list=List{};list.add(.{.cell=9,.x=50,.y=50,.scale=0.5});
 try std.testing.expectEqual(@as(?usize,9),list.pick(50,35));try std.testing.expectEqual(@as(?usize,null),list.pick(50,20));
 try std.testing.expectEqual(@as(?usize,null),list.pick(std.math.nan(f32),50));
 for(0..100)|i|list.add(.{.cell=i,.x=100,.y=100,.scale=1});try std.testing.expectEqual(@as(usize,64),list.count);
}

test "declutter-distance vertical neighbour cannot steal an exact root tap" {
 var list=List{};list.add(.{.cell=1,.x=100,.y=200,.scale=1});list.add(.{.cell=2,.x=100,.y=238,.scale=1});
 try std.testing.expectEqual(@as(?usize,1),list.pick(100,200));
 try std.testing.expectEqual(@as(?usize,2),list.pick(100,238));
 try std.testing.expectEqual(@as(?usize,1),list.pick(100,175));
}
