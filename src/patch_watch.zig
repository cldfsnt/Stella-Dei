//! Transient, O(1) observation of actual selected-patch grazing flux. Not save data.
const std=@import("std");
pub const Watch=struct {
 owner:usize=0, active:bool=false, status:[]const u8="idle", cell:usize=0, world:u32=0,
 start_game:f64=0, elapsed:f64=0, consumed:f64=0, ticks:u32=0,
 start_ms:f64=0,last_ms:f64=0,
 pub fn start(self:*Watch,cell:usize,world:u32,game:f64,ms:f64)bool{
  if(!std.math.isFinite(game) or !std.math.isFinite(ms))return false;
  self.*=.{.active=true,.status="watching",.cell=cell,.world=world,.start_game=game,.start_ms=ms,.last_ms=ms};return true;
 }
 pub fn stop(self:*Watch,reason:[]const u8)void{if(self.active){self.active=false;self.status=reason;}}
 pub fn guard(self:*Watch,cell:usize,world:u32,game:f64,ms:f64,blocked:bool)void{
  if(!self.active)return;
  if(world!=self.world){self.stop("world changed");return;}
  if(cell!=self.cell){self.stop("selection changed");return;}
  if(blocked){self.stop("paused or menu opened");return;}
  if(!std.math.isFinite(game) or game<self.start_game or !std.math.isFinite(ms) or ms<self.last_ms){self.stop("clock changed");return;}
  self.last_ms=ms;
  if(ms-self.start_ms>=10000)self.stop("complete");
 }
 pub fn beginTick(self:*Watch,owner:usize,game:f64,ms:f64)bool{
  if(!self.active or self.owner!=owner)return false;
  if(game<self.start_game+self.elapsed){self.stop("clock changed");return false;}
  self.guard(self.cell,self.world,game,ms,false);return self.active;
 }
 pub fn record(self:*Watch,cell:usize,grazed:f32)void{
  if(!self.active or cell!=self.cell)return;
  if(!std.math.isFinite(grazed) or grazed<0){self.stop("invalid flux");return;}
  const sum=self.consumed+@as(f64,grazed);
  if(!std.math.isFinite(sum)){self.stop("invalid flux");return;}
  self.consumed=sum;
 }
 pub fn finishTick(self:*Watch,game:f64,dt:f64)void{
  if(!self.active)return;
  if(!std.math.isFinite(game) or !std.math.isFinite(dt) or dt<=0 or game<self.start_game or !std.math.isFinite(game+dt) or game+dt<self.start_game+self.elapsed){self.stop("clock changed");return;}
  if(self.ticks==std.math.maxInt(u32)){self.stop("observation limit");return;}
  self.elapsed=game+dt-self.start_game;self.ticks+=1;
 }
};
pub var current:Watch=.{};
extern "c" fn emscripten_get_now()f64;
var native_timer:?std.time.Timer=null;
pub fn nowMs()f64{
 if(@import("builtin").target.cpu.arch==.wasm32)return emscripten_get_now();
 if(native_timer==null)native_timer=std.time.Timer.start() catch return 0;
 return @as(f64,@floatFromInt(native_timer.?.read()))/1000000;
}
test "exact patch flux, empty ticks, no identity/lifetime dependence" {
 var w=Watch{};try std.testing.expect(w.start(2,1,0,0));
 w.record(1,99);w.record(2,0.25);w.record(2,0.5);w.finishTick(0,1440);w.finishTick(1440,1440);
 try std.testing.expectEqual(@as(f64,0.75),w.consumed);try std.testing.expectEqual(@as(f64,2880),w.elapsed);
 w.guard(2,1,2880,10000,false);w.record(2,10);try std.testing.expect(!w.active and std.mem.eql(u8,w.status,"complete"));try std.testing.expectEqual(@as(f64,0.75),w.consumed);
}
test "pause selection load clock and invalid flux stop immediately" {
 var w=Watch{};
 _=w.start(2,1,0,0);w.guard(2,1,0,1,true);try std.testing.expect(!w.active);
 _=w.start(2,1,0,0);w.guard(3,1,0,1,false);try std.testing.expect(!w.active);
 _=w.start(2,1,0,0);w.guard(2,2,0,1,false);try std.testing.expect(!w.active);
 _=w.start(2,1,10,0);w.guard(2,1,9,1,false);try std.testing.expect(!w.active);
 _=w.start(2,1,0,0);w.record(2,std.math.nan(f32));try std.testing.expect(!w.active);
 _=w.start(2,1,0,0);w.stop("cancelled");w.finishTick(0,1440);try std.testing.expectEqual(@as(f64,0),w.elapsed);
}
test "no grazing records zero and zero simulated duration is not inferred" {
 var w=Watch{};_=w.start(0,1,0,0);w.guard(0,1,0,10000,false);
 try std.testing.expectEqual(@as(f64,0),w.elapsed);try std.testing.expectEqual(@as(f64,0),w.consumed);
 _=w.start(0,1,0,0);w.finishTick(0,1440);try std.testing.expectEqual(@as(f64,0),w.consumed);
}

test "owner isolation and tick-boundary deadline" {
 var w=Watch{};_=w.start(2,1,0,100);w.owner=7;
 try std.testing.expect(!w.beginTick(8,0,101));try std.testing.expect(w.active);
 try std.testing.expect(w.beginTick(7,0,101));w.record(2,0.5);w.finishTick(0,1440);
 try std.testing.expect(!w.beginTick(7,1440,10100));try std.testing.expectEqual(@as(f64,0.5),w.consumed);
 _=w.start(2,1,0,100);w.owner=7;w.finishTick(0,1440);try std.testing.expect(!w.beginTick(7,0,101));
}
test "bad time and counter overflow stop without wrapping" {
 var w=Watch{};_=w.start(1,1,0,0);w.finishTick(0,std.math.inf(f64));try std.testing.expect(!w.active);
 _=w.start(1,1,0,0);w.ticks=std.math.maxInt(u32);w.finishTick(0,1440);try std.testing.expect(!w.active);
 _=w.start(1,1,0,0);w.consumed=std.math.inf(f64);w.record(1,1);try std.testing.expect(!w.active);
}
