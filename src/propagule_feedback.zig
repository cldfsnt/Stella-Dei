//! Session-only bounded observation of actual paid arrivals and their actual loss.
//! This module creates no organisms, never advances RNG, and is not save state.
const std=@import("std");
pub const Kind=enum{arrival,failed};
pub const Event=struct{serial:u64=0,kind:Kind=.arrival,from:usize=0,cell:usize=0,lineage:u64=0,sim_time:f64=0};
const Pending=struct{from:usize,cell:usize,lineage:u64,arrived_at:f64};
pub const Tracker=struct{
 events:[32]Event=.{.{}}**32,
 next_serial:u64=1,
 pending:[32]?Pending=.{null}**32,
 cursor:usize=0,
 fn emit(self:*Tracker,kind:Kind,p:Pending,time:f64) void {
  const serial=self.next_serial;
  self.events[@intCast((serial-1)%self.events.len)]=.{.serial=serial,.kind=kind,.from=p.from,.cell=p.cell,.lineage=p.lineage,.sim_time=time};
  self.next_serial+|=1;
 }
 /// Caller must already have accepted and paid for this real child.
 pub fn arrived(self:*Tracker,from:usize,cell:usize,lineage:u64,time:f64) void {
  if(lineage==0 or from==cell or !std.math.isFinite(time))return;
  for(self.pending)|p|{if(p!=null and p.?.lineage==lineage)return;}
  const p=Pending{.from=from,.cell=cell,.lineage=lineage,.arrived_at=time};
  self.pending[self.cursor]=p;self.cursor=(self.cursor+1)%self.pending.len;
  self.emit(.arrival,p,time);
 }
 /// Caller must have observed actual disappearance through mortality, not movement.
 /// An old/untracked colony loss is NOT relabeled a failed arrival.
 pub fn failed(self:*Tracker,cell:usize,lineage:u64,time:f64) bool {
  if(!std.math.isFinite(time))return false;
  for(&self.pending)|*entry|{
   const p=entry.* orelse continue;
   if(p.cell==cell and p.lineage==lineage){entry.*=null;if(time<p.arrived_at)return false;self.emit(.failed,p,time);return true;}
  }
  return false;
 }
 /// Forget a tracked lineage when it demonstrably establishes or relocates.
 /// No celebration or establishment event is invented by this observer.
 pub fn forget(self:*Tracker,lineage:u64) void {
  for(&self.pending)|*p|{if(p.*!=null and p.*.?.lineage==lineage)p.*=null;}
 }
};
test "only real registered cross-cell arrivals can later report failure once" {
 var t=Tracker{};try std.testing.expect(!t.failed(2,7,1));
 t.arrived(1,2,7,0);try std.testing.expectEqual(@as(u64,2),t.next_serial);
 t.arrived(1,2,7,0);try std.testing.expectEqual(@as(u64,2),t.next_serial);
 try std.testing.expect(!t.failed(3,7,1));try std.testing.expect(t.failed(2,7,1));try std.testing.expect(!t.failed(2,7,2));
 try std.testing.expectEqual(Kind.failed,t.events[1].kind);try std.testing.expectEqual(@as(usize,1),t.events[1].from);
}
test "bounded tracker evicts old arrivals without inventing failures" {
 var t=Tracker{};for(1..41)|i|t.arrived(0,i,i,@floatFromInt(i));
 try std.testing.expect(!t.failed(1,1,42));try std.testing.expect(t.failed(40,40,42));
 t.forget(39);try std.testing.expect(!t.failed(39,39,42));
 try std.testing.expectEqual(@as(usize,32),t.events.len);
}

test "tracked older colony loss remains observable without claiming failed establishment" {
 var t=Tracker{};t.arrived(1,2,9,0);try std.testing.expect(t.failed(2,9,30*86400));
 try std.testing.expectEqual(@as(u64,3),t.next_serial);
}
