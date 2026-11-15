//! Opt-in local diagnostic aggregates. Never saved and never used by simulation.
const std=@import("std");
pub const Stage=enum(u8){terrain_upload,scene_draw,postprocess,ui};
pub const Sample=struct {
 stage_sum:[4]f64=.{0}**4,stage_max:[4]f64=.{0}**4,
 frames:u32=0,ticks:u32=0,physics_frames:u32=0,long_frames:u32=0,frame_p95:f64=0,
 frame_sum:f64=0,frame_max:f64=0,physics_sum:f64=0,physics_max:f64=0,render_sum:f64=0,render_max:f64=0,
};
/// Last observed render setup while diagnostics are enabled, not averaged timings.
pub const RenderContext=struct {
 valid:bool=false,world:[]const u8="unknown",map:[]const u8="unknown",
 canvas_width:i32=0,canvas_height:i32=0,scene_width:i32=0,scene_height:i32=0,
 bloom_active:bool=false,bloom_passes:u8=0,composite_passes:u8=1,
 stable_daylight:bool=false,orbit:bool=false,animals:usize=0,
 camera_radius:f32=0,planet_radius:f32=0,camera_valid:bool=false,
};
pub const Metrics=struct {
 enabled:bool=false,interrupted:bool=false,context:RenderContext=.{},current:Sample=.{},completed:Sample=.{},frame_intervals:[60]f64=[_]f64{0}**60,
 pub fn setEnabled(self:*Metrics,value:bool)void{self.*=.{.enabled=value};}
 pub fn renderContext(self:*Metrics,value:RenderContext)void{if(self.enabled)self.context=value;}
 pub fn stage(self:*Metrics,which:Stage,ms:f64)void{
  if(!self.enabled or !std.math.isFinite(ms) or ms<0)return;
  const i=@intFromEnum(which);self.current.stage_sum[i]+=ms;self.current.stage_max[i]=@max(self.current.stage_max[i],ms);
 }
 pub fn physics(self:*Metrics,ms:f64,ticks:u8)void{
  if(!self.enabled or ticks==0 or !std.math.isFinite(ms) or ms<0)return;
  self.current.physics_sum+=ms;self.current.physics_max=@max(self.current.physics_max,ms);
  self.current.physics_frames+=1;self.current.ticks+=ticks;
 }
 pub fn frame(self:*Metrics,interval_ms:f64,render_cpu_ms:f64)void{
  if(!self.enabled)return;
  if(!std.math.isFinite(interval_ms) or interval_ms<0 or !std.math.isFinite(render_cpu_ms) or render_cpu_ms<0)return;
  self.frame_intervals[self.current.frames]=interval_ms;
  if(interval_ms>50)self.current.long_frames+=1;
  self.current.frames+=1;self.current.frame_sum+=interval_ms;self.current.frame_max=@max(self.current.frame_max,interval_ms);
  self.current.render_sum+=render_cpu_ms;self.current.render_max=@max(self.current.render_max,render_cpu_ms);
  if(self.current.frames>=60){self.current.frame_p95=percentile95(self.frame_intervals[0..60]);self.completed=self.current;self.current=.{};}
 }
 pub fn sample(self:*const Metrics)Sample{
  if(self.completed.frames>0)return self.completed;
  var result=self.current;result.frame_p95=percentile95(self.frame_intervals[0..self.current.frames]);return result;
 }
};
/// Exact nearest-rank percentile of at most 60 accepted frame intervals.
/// Computed on a stack copy, only at block completion or diagnostic read.
fn percentile95(values:[]const f64)f64{
 if(values.len==0)return 0;
 std.debug.assert(values.len<=60);
 var copy:[60]f64=undefined;@memcpy(copy[0..values.len],values);
 std.mem.sort(f64,copy[0..values.len],{},std.sort.asc(f64));
 return copy[(95*values.len+99)/100-1];
}
pub var metrics=Metrics{};
// Volatile diagnostic generation only: never saved, sent or used by simulation.
pub var world_serial:u32=0;
pub fn worldChanged()void{@import("advance_day.zig").invalidate("world changed");@import("manual_transport.zig").reset();@import("habitat_preview.zig").cancel();world_serial+%=1;metrics.setEnabled(false);@import("patch_watch.zig").current.stop("world changed");}
pub fn interrupted()void{if(metrics.enabled)metrics.interrupted=true;}

test "opt in, bounded windows, finite diagnostics and reset" {
 var m=Metrics{};m.physics(7,1);m.frame(16,4);try std.testing.expectEqualDeep(Sample{},m.sample());
 m.setEnabled(true);for(0..60)|_|{m.physics(7,1);m.frame(16,4);}
 const s=m.sample();try std.testing.expectEqual(@as(u32,60),s.frames);try std.testing.expectEqual(@as(f64,420),s.physics_sum);try std.testing.expectEqual(@as(f64,7),s.physics_max);
 m.frame(std.math.nan(f64),0);try std.testing.expectEqual(@as(u32,0),m.current.frames);
 for(0..60)|_|m.frame(20,5);try std.testing.expectEqual(@as(u32,0),m.sample().ticks);
 m.setEnabled(false);try std.testing.expectEqualDeep(Sample{},m.sample());
}

test "nearest-rank p95 empty single ties sorted reversed and rare stalls" {
 try std.testing.expectEqual(@as(f64,0),percentile95(&.{}));
 try std.testing.expectEqual(@as(f64,12),percentile95(&.{12}));
 var values:[60]f64=undefined;for(&values,0..)|*v,i|v.*=@floatFromInt(60-i);
 try std.testing.expectEqual(@as(f64,57),percentile95(&values));
 for(&values)|*v|v.*=16;values[59]=200;
 try std.testing.expectEqual(@as(f64,16),percentile95(&values));
 values[58]=200;values[57]=200;try std.testing.expectEqual(@as(f64,16),percentile95(&values));
 values[56]=200;try std.testing.expectEqual(@as(f64,200),percentile95(&values));
 try std.testing.expectEqual(@as(f64,20),percentile95(&.{20,20,20}));
}
test "long frames strictly exceed50 and completed block remains paired with percentile" {
 var m=Metrics{};m.setEnabled(true);m.frame(50,0);m.frame(50.001,0);m.frame(200,0);
 try std.testing.expectEqual(@as(u32,2),m.sample().long_frames);try std.testing.expectEqual(@as(f64,200),m.sample().frame_p95);
 const before=m;_=m.sample();try std.testing.expectEqualDeep(before,m);
 m.frame(std.math.inf(f64),0);try std.testing.expectEqual(@as(u32,3),m.current.frames);
 for(0..57)|_|m.frame(16,0);
 const done=m.sample();try std.testing.expectEqual(@as(u32,2),done.long_frames);try std.testing.expectEqual(@as(f64,16),done.frame_p95);try std.testing.expectEqual(@as(f64,200),done.frame_max);
 m.frame(900,0);try std.testing.expectEqualDeep(done,m.sample());
 m.setEnabled(false);m.frame(900,0);try std.testing.expectEqualDeep(Sample{},m.sample());
 m.setEnabled(true);m.frame(10,0);try std.testing.expectEqual(@as(f64,10),m.sample().frame_p95);
}

test "render context is opt in and resets with measurement" {
 var m=Metrics{};const c=RenderContext{.valid=true,.world="origin",.canvas_width=390,.scene_width=390,.bloom_active=false,.bloom_passes=0};
 m.renderContext(c);try std.testing.expect(!m.context.valid);
 m.setEnabled(true);m.renderContext(c);try std.testing.expect(m.context.valid);try std.testing.expectEqual(@as(i32,390),m.context.canvas_width);
 m.setEnabled(false);try std.testing.expect(!m.context.valid);
}

/// Opt-in CPU/call wall timers; may include driver waits, never GPU timers.
extern "c" fn emscripten_get_now() f64;
const web_stage_clock=@import("builtin").target.cpu.arch==.wasm32;
pub const StageStart=if(web_stage_clock)f64 else std.time.Timer;
pub fn beginStage() ?StageStart {
 if(!metrics.enabled)return null;
 if(web_stage_clock)return emscripten_get_now();
 return std.time.Timer.start() catch null;
}
pub fn endStage(start:?StageStart,which:Stage)void{
 var timer=start orelse return;
 const ms=if(web_stage_clock)emscripten_get_now()-timer else @as(f64,@floatFromInt(timer.read()))/1e6;
 metrics.stage(which,ms);
}
test "stage aggregates disabled finite bounded and reset with blocks" {
 var m=Metrics{};m.stage(.ui,5);try std.testing.expectEqual(@as(f64,0),m.current.stage_sum[3]);
 m.setEnabled(true);for(0..60)|_|{m.stage(.terrain_upload,2);m.stage(.scene_draw,5);m.stage(.postprocess,3);m.stage(.ui,1);m.frame(16,9);}
 try std.testing.expectEqual(@as(f64,120),m.sample().stage_sum[0]);try std.testing.expectEqual(@as(f64,5),m.sample().stage_max[1]);
 m.stage(.ui,std.math.nan(f64));try std.testing.expectEqual(@as(f64,0),m.current.stage_sum[3]);m.setEnabled(false);try std.testing.expectEqual(@as(f64,0),m.sample().stage_sum[0]);
}

test "world lifecycle clears measurement and interrupted marks only enabled diagnostics" {
 metrics=.{};const old=world_serial;interrupted();try std.testing.expect(!metrics.interrupted);
 metrics.setEnabled(true);interrupted();try std.testing.expect(metrics.interrupted);
 worldChanged();try std.testing.expect(world_serial==old+%1);try std.testing.expect(!metrics.enabled and !metrics.interrupted);
}
