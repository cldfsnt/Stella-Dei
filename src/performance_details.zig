//! Opt-in local diagnostic aggregates. Never saved and never used by simulation.
const std=@import("std");
pub const Sample=struct {
 frames:u32=0,ticks:u32=0,physics_frames:u32=0,
 frame_sum:f64=0,frame_max:f64=0,physics_sum:f64=0,physics_max:f64=0,render_sum:f64=0,render_max:f64=0,
};
pub const Metrics=struct {
 enabled:bool=false,current:Sample=.{},completed:Sample=.{},
 pub fn setEnabled(self:*Metrics,value:bool)void{self.*=.{.enabled=value};}
 pub fn physics(self:*Metrics,ms:f64,ticks:u8)void{
  if(!self.enabled or ticks==0 or !std.math.isFinite(ms) or ms<0)return;
  self.current.physics_sum+=ms;self.current.physics_max=@max(self.current.physics_max,ms);
  self.current.physics_frames+=1;self.current.ticks+=ticks;
 }
 pub fn frame(self:*Metrics,interval_ms:f64,render_cpu_ms:f64)void{
  if(!self.enabled)return;
  if(!std.math.isFinite(interval_ms) or interval_ms<0 or !std.math.isFinite(render_cpu_ms) or render_cpu_ms<0)return;
  self.current.frames+=1;self.current.frame_sum+=interval_ms;self.current.frame_max=@max(self.current.frame_max,interval_ms);
  self.current.render_sum+=render_cpu_ms;self.current.render_max=@max(self.current.render_max,render_cpu_ms);
  if(self.current.frames>=60){self.completed=self.current;self.current=.{};}
 }
 pub fn sample(self:*const Metrics)Sample{return if(self.completed.frames>0)self.completed else self.current;}
};
pub var metrics=Metrics{};
test "opt in, bounded windows, finite diagnostics and reset" {
 var m=Metrics{};m.physics(7,1);m.frame(16,4);try std.testing.expectEqualDeep(Sample{},m.sample());
 m.setEnabled(true);for(0..60)|_|{m.physics(7,1);m.frame(16,4);}
 const s=m.sample();try std.testing.expectEqual(@as(u32,60),s.frames);try std.testing.expectEqual(@as(f64,420),s.physics_sum);try std.testing.expectEqual(@as(f64,7),s.physics_max);
 m.frame(std.math.nan(f64),0);try std.testing.expectEqual(@as(u32,0),m.current.frames);
 for(0..60)|_|m.frame(20,5);try std.testing.expectEqual(@as(u32,0),m.sample().ticks);
 m.setEnabled(false);try std.testing.expectEqualDeep(Sample{},m.sample());
}
