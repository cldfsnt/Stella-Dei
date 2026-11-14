//! Exact rendered Seed targets, reused for touch selection. No world-ray guessing.
const std=@import("std");
pub const radius:f32=24;
pub const Target=struct{cell:usize,x:f32,y:f32};
pub const List=struct {
 items:[65]Target=undefined,count:usize=0,
 pub fn add(self:*List,t:Target,declutter:bool) bool {
  if(self.count==self.items.len or !std.math.isFinite(t.x) or !std.math.isFinite(t.y))return false;
  for(self.items[0..self.count])|old|{
   if(old.cell==t.cell)return false;
   const dx=t.x-old.x;const dy=t.y-old.y;
   if(declutter and dx*dx+dy*dy<38*38)return false;
  }
  self.items[self.count]=t;self.count+=1;return true;
 }
 pub fn pick(self:*const List,x:f32,y:f32) ?usize {
  if(!std.math.isFinite(x) or !std.math.isFinite(y))return null;
  var best:?usize=null;var distance:f32=radius*radius;
  for(self.items[0..self.count])|t|{
   const dx=x-t.x;const dy=y-t.y;const d=dx*dx+dy*dy;
   if(d<distance or (d==distance and (best==null or t.cell<best.?))){best=t.cell;distance=d;}
  }
  if(best) |chosen| {
   // At a shared boundary do not silently choose a neighboring patch.
   for(self.items[0..self.count])|t|{
    if(t.cell==chosen)continue;
    const dx=x-t.x;const dy=y-t.y;const d=dx*dx+dy*dy;
    if(d<=radius*radius and @abs(@sqrt(d)-@sqrt(distance))<=1)return null;
   }
  }
  return best;
 }
};
test "center and phone offsets choose exactly visible cell not world ray" {
 var list=List{};_=list.add(.{.cell=42,.x=100,.y=200},true);
 for([_][2]f32{.{0,0},.{22,0},.{-22,0},.{0,22},.{0,-22},.{16,16},.{24,0}})|offset|try std.testing.expectEqual(@as(?usize,42),list.pick(100+offset[0],200+offset[1]));
 try std.testing.expectEqual(@as(?usize,null),list.pick(125,200));
 try std.testing.expectEqual(@as(?usize,null),list.pick(std.math.nan(f32),200));
}
test "overlap picks nearest, ambiguous boundary rejects; absent invalid target cannot hit" {
 var list=List{};_=list.add(.{.cell=9,.x=100,.y=200},false);_=list.add(.{.cell=3,.x=140,.y=200},false);
 try std.testing.expectEqual(@as(?usize,null),list.pick(120,200));try std.testing.expectEqual(@as(?usize,9),list.pick(118,200));
 var empty=List{};try std.testing.expectEqual(@as(?usize,null),empty.pick(100,200));
}
