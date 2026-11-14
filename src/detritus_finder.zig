//! Transient on-demand scan state. No allocations, simulation writes or background scan.
const std=@import("std");
pub const batch_size:usize=512;
pub const Scanner=struct {
 active:bool=false,cursor:usize=0,total:usize=0,storage:usize=0,geometry:usize=0,seed:u64=0,radius:f32=0,selection:usize=0,
 fallback:?usize=null,fallback_mass:f32=0,
 pub fn begin(self:*Scanner,total:usize,storage:usize)void{self.*=.{.active=true,.total=total,.storage=storage};}
 pub fn end(self:*Scanner)usize{return @min(self.total,self.cursor+|batch_size);}
 pub fn consider(self:*Scanner,index:usize,mass:f32)void{if(std.math.isFinite(mass) and mass>self.fallback_mass){self.fallback=index;self.fallback_mass=mass;}}
};
test "incremental fuel scan bounded ties stable and invalid fuel ignored" {
 var s=Scanner{};s.begin(40962,123);var batches:usize=0;
 while(s.cursor<s.total){const end=s.end();try std.testing.expect(end-s.cursor<=512);for(s.cursor..end)|i|s.consider(i,if(i==1200 or i==1600)2 else 0);s.cursor=end;batches+=1;}
 try std.testing.expectEqual(@as(usize,81),batches);try std.testing.expectEqual(@as(?usize,1200),s.fallback);
 s.consider(3,std.math.nan(f32));s.consider(4,std.math.inf(f32));s.consider(5,-1);try std.testing.expectEqual(@as(?usize,1200),s.fallback);
 s.begin(0,7);try std.testing.expectEqual(@as(usize,0),s.end());try std.testing.expectEqual(@as(?usize,null),s.fallback);
}
