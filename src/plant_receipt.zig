//! Explicitly requested selected-patch net balance. No vegetation-pass hooks.
const std=@import("std");
pub var enabled=true;
pub const Receipt=struct{start_time:f64=0,end_time:f64=0,seconds:f64=0,before:f64=0,after:f64=0,grazed:f64=0,net:f64=0,other:f64=0,bites:u32=0};
const Observer=struct{owner:usize=0,storage:usize=0,world:u32=0,cell:usize=0,bound:bool=false,in_tick:bool=false,ready:bool=false,r:Receipt=.{}};
var current:Observer=.{};
pub fn reset()void{current=.{};}
pub fn invalidate()void{reset();}
/// Explicit user request only. Guard/update must never implicitly rearm.
pub fn arm(p:anytype,world:u32,cell:usize)void{
 reset();if(!enabled or p.worldMode!=.sandbox or cell>=p.vegetation.len)return;
 current=.{.owner=@intFromPtr(p),.storage=@intFromPtr(p.vegetation.ptr),.world=world,.cell=cell,.bound=true};
}
fn matches(p:anytype,world:u32)bool{return enabled and current.bound and p.worldMode==.sandbox and current.owner==@intFromPtr(p) and current.storage==@intFromPtr(p.vegetation.ptr) and current.world==world and current.cell<p.vegetation.len;}
pub fn guard(p:anytype,world:u32,cell:usize)void{if(!matches(p,world) or cell!=current.cell)reset();}
pub fn begin(p:anytype,world:u32,time:f64,dt:f64)void{
 current.in_tick=false;current.ready=false;
 if(!matches(p,world) or !std.math.isFinite(time) or !std.math.isFinite(dt) or dt<=0 or !std.math.isFinite(time+dt))return;
 const v=p.vegetation[current.cell];if(!std.math.isFinite(v) or v<0 or v>1)return;
 current.r=.{.start_time=time,.end_time=time+dt,.seconds=dt,.before=v};current.in_tick=true;
}
pub inline fn observedCell(owner:usize)usize{return if(enabled and current.in_tick and current.owner==owner)current.cell else std.math.maxInt(usize);}
pub fn recordBite(owner:usize,cell:usize,before:f32,after:f32)void{
 @setFloatMode(.strict);
 if(cell!=observedCell(owner))return;
 if(!std.math.isFinite(before) or !std.math.isFinite(after) or before<after or after<0){invalidate();return;}
 current.r.grazed+=@as(f64,before)-@as(f64,after);if(after<before)current.r.bites+=1;
}
pub fn finish(p:anytype,world:u32)void{
 @setFloatMode(.strict);
 if(!current.in_tick or !matches(p,world)){current.ready=false;current.in_tick=false;return;}
 const v=p.vegetation[current.cell];if(!std.math.isFinite(v) or v<0 or v>1){invalidate();return;}
 current.r.after=v;current.r.net=@as(f64,v)-current.r.before;
 // This is a derived remainder, NOT an independent physiological measurement.
 current.r.other=current.r.net+current.r.grazed;
 current.ready=std.math.isFinite(current.r.other);current.in_tick=false;
}
pub fn view(p:anytype,world:u32,cell:usize,time:f64)?Receipt{
 if(!matches(p,world) or !current.ready or current.in_tick or cell!=current.cell or time!=current.r.end_time or @as(f64,p.vegetation[cell])!=current.r.after)return null;
 return current.r;
}
test "explicit arm, actual bites and derived other net"{
 const Mock=struct{worldMode:enum{sandbox,origin}=.sandbox,vegetation:[]f32};var v=[_]f32{0.5,0.2};var p=Mock{.vegetation=&v};reset();defer reset();guard(&p,1,0);begin(&p,1,0,60);finish(&p,1);try std.testing.expect(view(&p,1,0,60)==null);
 arm(&p,1,0);begin(&p,1,0,60);recordBite(@intFromPtr(&p),0,0.5,0.375);v[0]=0.625;finish(&p,1);
 const r=view(&p,1,0,60).?;try std.testing.expectEqual(@as(f64,0.125),r.grazed);try std.testing.expectEqual(@as(f64,0.125),r.net);try std.testing.expectEqual(@as(f64,0.25),r.other);try std.testing.expectEqual(@as(u32,1),r.bites);
 try std.testing.expect(view(&p,1,0,61)==null);guard(&p,1,1);guard(&p,1,0);try std.testing.expect(view(&p,1,0,60)==null);try std.testing.expect(!current.bound);
}
test "no auto-rearm after intervention/load and unavailable incomplete interval"{
 const Mock=struct{worldMode:enum{sandbox,origin}=.sandbox,vegetation:[]f32};var v=[_]f32{0.5};var p=Mock{.vegetation=&v};reset();defer reset();arm(&p,1,0);begin(&p,1,0,60);try std.testing.expect(view(&p,1,0,60)==null);finish(&p,1);try std.testing.expect(view(&p,1,0,60)!=null);invalidate();guard(&p,1,0);begin(&p,1,60,60);finish(&p,1);try std.testing.expect(view(&p,1,0,120)==null);
 arm(&p,1,0);begin(&p,1,120,0);finish(&p,1);try std.testing.expect(view(&p,1,0,120)==null);p.worldMode=.origin;guard(&p,1,0);try std.testing.expect(!current.bound);reset();
}
