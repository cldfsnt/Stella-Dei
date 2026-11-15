//! Transient on-demand scan state. No allocations, simulation writes or background scan.
const std=@import("std");
pub const batch_size:usize=512;
pub const Scanner=struct {
 active:bool=false,cursor:usize=0,total:usize=0,storage:usize=0,geometry:usize=0,seed:u64=0,radius:f32=0,selection:usize=0,
 fallback:?usize=null,fallback_mass:f32=0,fallback_taps:f64=std.math.inf(f64),blocked:?usize=null,blocked_mass:f32=0,
 pub fn begin(self:*Scanner,total:usize,storage:usize)void{self.*=.{.active=true,.total=total,.storage=storage};}
 pub fn end(self:*Scanner)usize{return @min(self.total,self.cursor+|batch_size);}
 /// Nominal count only: actual f32 removal and running hydrology can differ.
 pub fn considerWet(self:*Scanner,index:usize,mass:f32,depth_m:f64)void{
  const taps=nominalTaps(depth_m) orelse return;if(taps==0)return;
  if(!std.math.isFinite(mass) or mass<=0)return;
  if(taps<self.fallback_taps or (taps==self.fallback_taps and (mass>self.fallback_mass or (mass==self.fallback_mass and (self.fallback==null or index<self.fallback.?))))){self.fallback=index;self.fallback_mass=mass;self.fallback_taps=taps;}
 }
 pub fn considerBlocked(self:*Scanner,index:usize,mass:f32)void{if(std.math.isFinite(mass) and mass>self.blocked_mass){self.blocked=index;self.blocked_mass=mass;}}
 pub fn consider(self:*Scanner,index:usize,mass:f32)void{if(std.math.isFinite(mass) and mass>self.fallback_mass){self.fallback=index;self.fallback_mass=mass;}}
};
test "incremental fuel scan bounded ties stable and invalid fuel ignored" {
 var s=Scanner{};s.begin(40962,123);var batches:usize=0;
 while(s.cursor<s.total){const end=s.end();try std.testing.expect(end-s.cursor<=512);for(s.cursor..end)|i|s.consider(i,if(i==1200 or i==1600)2 else 0);s.cursor=end;batches+=1;}
 try std.testing.expectEqual(@as(usize,81),batches);try std.testing.expectEqual(@as(?usize,1200),s.fallback);
 s.consider(3,std.math.nan(f32));s.consider(4,std.math.inf(f32));s.consider(5,-1);try std.testing.expectEqual(@as(?usize,1200),s.fallback);
 s.begin(0,7);try std.testing.expectEqual(@as(usize,0),s.end());try std.testing.expectEqual(@as(?usize,null),s.fallback);
}

/// One displayed metre per tap; estimate deliberately does not simulate editing.
pub fn nominalTaps(depth_m:f64)?f64{if(!std.math.isFinite(depth_m) or depth_m<0)return null;return @ceil(depth_m);}
test "wet fallback minimizes nominal taps then fuel then stable index" {
 var s=Scanner{};s.begin(100,1);s.considerWet(1,9,4.2);s.considerWet(8,0.1,0.1);s.considerWet(9,0.2,0.9);s.considerWet(7,0.2,0.8);try std.testing.expectEqual(@as(?usize,7),s.fallback);
 s.considerWet(0,100,0);s.considerBlocked(1,100);try std.testing.expectEqual(@as(?usize,1),s.blocked);
 s.considerWet(0,100,std.math.nan(f64));s.considerWet(0,100,std.math.inf(f64));try std.testing.expectEqual(@as(?usize,7),s.fallback);
 for([_]f64{0,0.999999,1,1.000001,1e20},[_]f64{0,1,1,2,1e20})|d,n|try std.testing.expectEqual(n,nominalTaps(d).?);
 try std.testing.expect(nominalTaps(-1)==null);try std.testing.expect(nominalTaps(std.math.nan(f64))==null);try std.testing.expect(nominalTaps(std.math.inf(f64))==null);
}
