//! Transient sampled global counts. No simulation mutation or per-frame scan.
const std=@import("std");
pub const Sample=struct{
 valid:bool=false,world:u32=0,storage:usize=0,day_time:f64=0,colonies:usize=0,patches:usize=0,
 pub fn capture(self:*Sample,summary:anytype,world:u32,storage:usize,time:f64)void{
  self.*=.{.valid=summary.valid and std.math.isFinite(time) and time>=0,.world=world,.storage=storage,.day_time=time,.colonies=summary.colonies,.patches=summary.patches};
 }
 pub fn line(self:Sample,buffer:[]u8,world:u32,storage:usize,time:f64)[]const u8{
  if(!self.valid or world!=self.world or storage!=self.storage or !std.math.isFinite(time) or time<self.day_time)return "Global count pending";
  return std.fmt.bufPrint(buffer,"Last count: {d} colonies · {d} patches",.{self.colonies,self.patches}) catch "Global count unavailable";
 }
};
test "sampled counts are explicit unknown until captured and reject old world or clock"{
 var s=Sample{};var b:[160]u8=undefined;
 try std.testing.expectEqualStrings("Global count pending",s.line(&b,1,2,0));
 s.capture(.{.valid=true,.colonies=@as(usize,64),.patches=@as(usize,37)},1,2,60);
 try std.testing.expectEqualStrings("Last count: 64 colonies · 37 patches",s.line(&b,1,2,61));
 try std.testing.expectEqualStrings("Global count pending",s.line(&b,2,2,61));
 try std.testing.expectEqualStrings("Global count pending",s.line(&b,1,3,61));
 try std.testing.expectEqualStrings("Global count pending",s.line(&b,1,2,59));
 s.capture(.{.valid=true,.colonies=@as(usize,0),.patches=@as(usize,0)},1,2,62);
 try std.testing.expectEqualStrings("Last count: 0 colonies · 0 patches",s.line(&b,1,2,62));
 s=.{};try std.testing.expectEqualStrings("Global count pending",s.line(&b,1,2,62));
}
