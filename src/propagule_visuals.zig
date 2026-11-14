//! Bounded real-time visual receipts; never biology or saved simulation state.
const std=@import("std");
const Feedback=@import("propagule_feedback.zig");
pub const duration:f32=1.6;
pub const Pulse=struct{event:Feedback.Event=.{},remaining:f32=0};
pub const Pool=struct{
 pulses:[12]Pulse=.{.{}}**12,last_serial:u64=0,
 pub fn advance(self:*Pool,dt:f32) void {
  if(!std.math.isFinite(dt) or dt<=0)return;
  for(&self.pulses)|*p|p.remaining=@max(0,p.remaining-dt);
 }
 pub fn take(self:*Pool,event:Feedback.Event) void {
  if(event.serial==0 or event.lineage==0)return;
  if(event.kind==.failed)for(&self.pulses)|*p|{if(p.event.lineage==event.lineage)p.remaining=0;};
  var oldest:usize=0;
  for(self.pulses,0..)|p,i|{if(p.remaining<=0){oldest=i;break;}if(p.remaining<self.pulses[oldest].remaining or (p.remaining==self.pulses[oldest].remaining and p.event.serial<self.pulses[oldest].event.serial))oldest=i;}
  self.pulses[oldest]=.{.event=event,.remaining=duration};
 }
};
test "only twelve actual receipts animate and expire in real time" {
 var p=Pool{};p.take(.{});try std.testing.expectEqual(@as(f32,0),p.pulses[0].remaining);
 for(1..50)|i|p.take(.{.serial=i,.lineage=i});
 for(p.pulses)|v|{try std.testing.expect(v.remaining>0);try std.testing.expect(v.event.serial>=38);}
 p.advance(duration);for(p.pulses)|v|try std.testing.expectEqual(@as(f32,0),v.remaining);
}

test "actual failure replaces arrival pulse instead of leaving ghost success" {
 var p=Pool{};p.take(.{.serial=1,.lineage=7});p.take(.{.serial=2,.lineage=7,.kind=.failed});
 var active:usize=0;for(p.pulses)|v|{if(v.remaining>0){active+=1;try std.testing.expectEqual(Feedback.Kind.failed,v.event.kind);}}
 try std.testing.expectEqual(@as(usize,1),active);
}
