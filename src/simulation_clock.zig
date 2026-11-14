//! Bounded simulated-time demand. Real-time rate metrics are separate from physics time.
const std=@import("std");
pub const Clock=struct{
 pending:f64=0,last_requested:f64=0,sample_wall:f64=0,sample_sim:f64=0,achieved:f64=0,dropped:f64=0,
 pub fn reset(self:*Clock)void{self.pending=0;self.sample_wall=0;self.sample_sim=0;self.achieved=0;}
 /// Pause/menu/tab gaps discard debt; speed changes do not inherit a prior fast queue.
 pub fn begin(self:*Clock,real_seconds:f64,requested:f64,step:f64,paused:bool)void{
  if(paused or !std.math.isFinite(real_seconds) or real_seconds<=0 or !std.math.isFinite(requested) or requested<=0 or !std.math.isFinite(step) or step<=0 or step>1440){self.reset();return;}
  if(requested!=self.last_requested){self.reset();self.last_requested=requested;}
  self.sample_wall+=real_seconds;
  // A slow active frame still runs bounded work. A multi-second gap discards
  // demand, but counts wall time so achieved rate never masquerades as faster.
  if(real_seconds>2){self.pending=0;return;}
  const demand=self.pending+real_seconds*requested;
  const cap=step*2;self.dropped+=@max(0,demand-cap);self.pending=@min(cap,demand);
 }
 pub fn take(self:*Clock,step:f64)bool{if(!std.math.isFinite(step) or step<=0 or self.pending+0.000001<step)return false;self.pending=@max(0,self.pending-step);self.sample_sim+=step;return true;}
 pub fn finish(self:*Clock)void{if(self.sample_wall>=2.0){self.achieved=self.sample_sim/self.sample_wall;self.sample_wall=0;self.sample_sim=0;}}
};
test "fractional demand accumulated, achieved based on actual work, backlog bounded"{var c=Clock{};for(0..180)|_|{c.begin(1.0/60.0,86400,1440,false);try std.testing.expect(c.take(1440));try std.testing.expect(!c.take(1440));c.finish();}try std.testing.expectApproxEqAbs(@as(f64,86400),c.achieved,0.001);c.begin(0.1,604800,1440,false);try std.testing.expect(c.pending<=2880);try std.testing.expect(c.dropped>0);}
test "pause background resume and requested change never catch up"{var c=Clock{};c.begin(0.1,86400,1440,false);c.begin(0.1,86400,1440,true);try std.testing.expectEqual(@as(f64,0),c.pending);c.begin(0.01,3600,1440,false);try std.testing.expectEqual(@as(f64,36),c.pending);c.begin(60,3600,1440,false);try std.testing.expectEqual(@as(f64,0),c.pending);}
test "slow speed does not lose time fractional quantum and invalid never poison"{var c=Clock{};var total:f64=0;for(0..240)|_|{c.begin(1.0/60.0,3600,1440,false);if(c.take(1440))total+=1440;c.finish();}try std.testing.expectApproxEqAbs(@as(f64,14400),total+c.pending,0.001);c.begin(std.math.nan(f64),3600,1440,false);try std.testing.expectEqual(@as(f64,0),c.pending);}

test "slow active .3second frames retain actual rate observation"{var c=Clock{};for(0..8)|_|{c.begin(0.3,86400,1440,false);try std.testing.expect(c.take(1440));c.finish();}try std.testing.expectApproxEqAbs(@as(f64,4800),c.achieved,0.001);c.begin(60,86400,1440,false);try std.testing.expect(c.pending==0);c.finish();try std.testing.expect(c.achieved<4800);}
