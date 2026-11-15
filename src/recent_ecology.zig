//! Session-only event histogram. No inferred events or saved historical backfill.
//! Includes current simulation hour and previous 23 hours: actual covered interval
//! varies from 23 to 24 hours once warm. Events are assigned their supplied time.
const std=@import("std");
pub const Counts=struct{births:u64=0,deaths:u64=0};
const Bucket=struct{hour:i64=-1,counts:Counts=.{}};
pub const View=struct{counts:Counts,from:f64,to:f64,observed_seconds:f64,saturated:bool};
pub const Observer=struct{
 active:bool=false,world:u64=0,start:f64=0,last:f64=0,
 buckets:[24]Bucket=.{.{}}**24,saturated:bool=false,
 baseline:?Counts=null,
 pub fn reset(self:*Observer)void{self.*=.{};}
 fn hour(time:f64)?i64{
  if(!std.math.isFinite(time) or time<0 or time>=0x1p62)return null;
  return @intFromFloat(@floor(time/3600));
 }
 fn sync(self:*Observer,world:u64,time:f64)bool{
  _=hour(time) orelse return false;
  if(!self.active or self.world!=world or time<self.last){self.*=.{.active=true,.world=world,.start=time,.last=time};}
  self.last=time;return true;
 }
 fn add(self:*Observer,time:f64,event:Counts)void{
  const h=hour(time).?;const slot:@TypeOf(@as(usize,0))=@intCast(@mod(h,24));
  var b=&self.buckets[slot];if(b.hour!=h)b.*=.{.hour=h};
  const births=@addWithOverflow(b.counts.births,event.births);const deaths=@addWithOverflow(b.counts.deaths,event.deaths);
  if(births[1]!=0 or deaths[1]!=0)self.saturated=true;
  b.counts.births +|=event.births;b.counts.deaths +|=event.deaths;
 }
 /// Events are caller-observed, timestamped at the end of their physics tick.
 /// Repeated calls at identical time intentionally add distinct events.
 pub fn record(self:*Observer,world:u64,time:f64,event:Counts)bool{
  if(!self.sync(world,time))return false;self.add(time,event);return true;
 }
 /// Optional adapter for cumulative counters. First call establishes baseline;
 /// counter decrease restarts observation rather than inventing negative events.
 /// Do not mix record and sampleCounters for the same event stream.
 pub fn sampleCounters(self:*Observer,world:u64,time:f64,totals:Counts)bool{
  if(!self.sync(world,time))return false;
  if(self.baseline)|old|{
   if(totals.births<old.births or totals.deaths<old.deaths){self.*=.{.active=true,.world=world,.start=time,.last=time,.baseline=totals};return true;}
   self.add(time,.{.births=totals.births-old.births,.deaths=totals.deaths-old.deaths});
  }
  self.baseline=totals;return true;
 }
 /// Pure query. Only the latest recorded simulation time is available; callers
 /// record zero events each completed tick so gaps cannot imply observation.
 /// from/to explicitly identify the bucket-aligned observed interval, NOT an
 /// exact rolling 24h window. Reads never reset or advance observation.
 pub fn view(self:Observer,world:u64,time:f64)?View{
  const h=hour(time) orelse return null;
  if(!self.active or world!=self.world or time!=self.last)return null;
  const first=@max(@as(i64,0),h-23);var total:Counts=.{};var overflow=self.saturated;
  for(self.buckets)|b|if(b.hour>=first and b.hour<=h){
   if(@addWithOverflow(total.births,b.counts.births)[1]!=0 or @addWithOverflow(total.deaths,b.counts.deaths)[1]!=0)overflow=true;
   total.births +|=b.counts.births;total.deaths +|=b.counts.deaths;
  };
  const from=@max(self.start,@as(f64,@floatFromInt(first))*3600);
  return .{.counts=total,.from=from,.to=time,.observed_seconds=time-from,.saturated=overflow};
 }
};
test "bucket edges expose exact observed interval not exact rolling day"{
 var o=Observer{};try std.testing.expect(o.record(1,1800,.{.births=2}));
 try std.testing.expect(o.record(1,3600,.{.deaths=3}));
 _=o.record(1,24*3600-1,.{});const a=o.view(1,24*3600-1).?;try std.testing.expectEqual(@as(u64,2),a.counts.births);try std.testing.expectEqual(@as(f64,1800),a.from);
 _=o.record(1,24*3600,.{});const b=o.view(1,24*3600).?;try std.testing.expectEqual(@as(u64,0),b.counts.births);try std.testing.expectEqual(@as(u64,3),b.counts.deaths);try std.testing.expectEqual(@as(f64,3600),b.from);try std.testing.expectEqual(@as(f64,23*3600),b.observed_seconds);
}
test "same-time events accumulate paused pure reads large jumps expire"{
 var o=Observer{};_=o.record(7,10,.{.births=1});_=o.record(7,10,.{.births=2,.deaths=1});const before=o;
 try std.testing.expectEqual(@as(u64,3),o.view(7,10).?.counts.births);try std.testing.expectEqualDeep(before,o);
 try std.testing.expect(o.view(7,100*86400)==null);_=o.record(7,100*86400,.{});try std.testing.expectEqual(@as(u64,0),o.view(7,100*86400).?.counts.births);_=o.record(7,100*86400,.{.births=4});try std.testing.expectEqual(@as(u64,4),o.view(7,100*86400).?.counts.births);
}
test "load world rollback and counter reset never backfill"{
 var o=Observer{};_=o.sampleCounters(1,100,.{.births=900,.deaths=400});try std.testing.expectEqual(@as(u64,0),o.view(1,100).?.counts.births);
 _=o.sampleCounters(1,101,.{.births=903,.deaths=402});try std.testing.expectEqual(@as(u64,3),o.view(1,101).?.counts.births);
 _=o.sampleCounters(1,102,.{.births=1});try std.testing.expectEqual(@as(u64,0),o.view(1,102).?.counts.births);
 _=o.sampleCounters(2,102,.{.births=999});try std.testing.expect(o.view(1,102)==null);try std.testing.expectEqual(@as(u64,0),o.view(2,102).?.counts.births);
 _=o.record(2,50,.{.deaths=1});try std.testing.expectEqual(@as(u64,0),o.view(2,50).?.counts.births);try std.testing.expectEqual(@as(u64,1),o.view(2,50).?.counts.deaths);
 o.reset();try std.testing.expect(o.view(2,50)==null);
}
test "invalid time atomic and overflow explicit"{
 var o=Observer{};_=o.record(1,1,.{.births=std.math.maxInt(u64)});_=o.record(1,1,.{.births=1});try std.testing.expect(o.view(1,1).?.saturated);
 const before=o;for([_]f64{-1,std.math.nan(f64),std.math.inf(f64),0x1p62})|t|{try std.testing.expect(!o.record(1,t,.{.births=1}));try std.testing.expect(o.view(1,t)==null);try std.testing.expectEqualDeep(before,o);}
 var sum=Observer{};_=sum.record(1,1,.{.births=std.math.maxInt(u64)});_=sum.record(1,3600,.{.births=1});try std.testing.expect(sum.view(1,3600).?.saturated);
}
