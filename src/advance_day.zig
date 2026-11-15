//! Explicit paused-only time advance. Volatile controller, never saved.
const std=@import("std");
pub const Phase=enum{idle,running,redraw,done,cancelled};
pub const Controller=struct{
 phase:Phase=.idle,token:u32=0,world:u32=0,owner:usize=0,completed:u32=0,
 start_time:f64=0,pace:f32=0,reason:[]const u8="",cancelled:bool=false,
 visible:bool=true,context_ok:bool=true,input_latched:bool=false,dismissed:bool=true,recovery_required:bool=false,
 pub fn busy(self:*const Controller)bool{return self.phase==.running or self.phase==.redraw;}
 pub fn blocks(self:*const Controller)bool{return self.recovery_required or self.busy() or self.input_latched;}
 pub fn start(self:*Controller,state:anytype,world:u32,expected:u32)bool{
  if(self.recovery_required or self.busy() or self.input_latched or !self.visible or !self.context_ok or world!=expected or state.planet.worldMode!=.origin or !state.paused or state.showEscapeMenu or state.showPlanetControl or state.showPointDetails or !std.math.isFinite(state.gameTime) or !std.math.isFinite(state.timeScale) or state.timeScale<0 or state.gameTime+86400-state.gameTime!=86400 or state.gameTime+1440-state.gameTime!=1440 or self.token==std.math.maxInt(u32))return false;
  self.token+=1;self.phase=.running;self.world=world;self.owner=@intFromPtr(&state.planet);self.completed=0;self.start_time=state.gameTime;self.pace=state.timeScale;self.reason="advancing";self.cancelled=false;self.input_latched=true;self.dismissed=false;
  state.simulationClock.reset();state.rawFrameDelta=null;state.simulationStepsLastFrame=0;state.pointerOnPlanet=false;
  return true;
 }
 pub fn cancel(self:*Controller,why:[]const u8)void{if(self.recovery_required or !self.busy())return;self.phase=.redraw;self.cancelled=true;self.reason=why;self.input_latched=true;}
 pub fn environment(self:*Controller,visible:bool,context_ok:bool)void{
  self.visible=visible;
  if(!context_ok){self.recovery_required=true;self.context_ok=false;self.phase=.cancelled;self.cancelled=true;self.reason="graphics context lost: save progress and reload";self.input_latched=true;self.dismissed=false;return;}
  if(self.recovery_required)return;
  self.context_ok=true;if(!visible)self.cancel("tab hidden");
 }
 pub fn canRecoverySave(self:*const Controller,state:anytype,world:u32)bool{return self.recovery_required and self.owner==@intFromPtr(&state.planet) and self.world==world and state.paused and state.planet.worldMode==.origin and state.timeScale==self.pace and state.gameTime==self.start_time+@as(f64,@floatFromInt(self.completed))*1440;}
 pub fn guard(self:*Controller,state:anytype,world:u32)bool{
  if(self.phase!=.running)return false;
  if(self.owner!=@intFromPtr(&state.planet) or self.world!=world or state.planet.worldMode!=.origin){self.cancel("world changed");return false;}
  if(!state.paused or state.timeScale!=self.pace or state.gameTime!=self.start_time+@as(f64,@floatFromInt(self.completed))*1440 or state.showEscapeMenu or state.showPlanetControl or state.showPointDetails){self.cancel("world state changed");return false;}
  if(!self.visible or !self.context_ok){self.cancel("view unavailable");return false;}
  return true;
 }
 pub fn tick(self:*Controller,state:anytype,loop:anytype,world:u32,raw_dt:f64)bool{
  if(!self.guard(state,world))return false;
  if(!std.math.isFinite(raw_dt) or raw_dt<0 or raw_dt>2){self.cancel("frame interrupted");return false;}
  state.planet.simulate(loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});
  state.gameTime+=1440;state.renderGameTime=state.gameTime;state.simulationClock.reset();state.rawFrameDelta=null;state.simulationStepsLastFrame=0;self.completed+=1;
  if(self.completed==60){self.phase=.redraw;self.reason="one day completed";}
  return true;
 }
 pub fn dismiss(self:*Controller,token:u32)bool{if(self.recovery_required or token==0 or token!=self.token or self.busy() or (self.phase!=.done and self.phase!=.cancelled))return false;self.dismissed=true;return true;}
 pub fn releaseInput(self:*Controller,neutral:bool)void{if(!self.recovery_required and self.dismissed and !self.busy() and neutral)self.input_latched=false;}
 pub fn didRedraw(self:*Controller)void{if(!self.recovery_required and self.phase==.redraw and self.visible and self.context_ok)self.phase=if(self.cancelled).cancelled else .done;}
};
pub var current=Controller{};
pub fn busy()bool{return current.busy();}
pub fn blocksInput()bool{return current.blocks();}
pub fn invalidate(why:[]const u8)void{current.cancel(why);}

const Mock=struct{
 const Mode=enum{origin,sandbox};
 const Planet=struct{worldMode:Mode=.origin,ticks:u32=0,pub fn simulate(p:*@This(),_:void,options:anytype)void{std.debug.assert(options.dt==1440 and options.timeScale==1);p.ticks+=1;}};
 planet:Planet=.{},paused:bool=true,showEscapeMenu:bool=false,showPlanetControl:bool=false,showPointDetails:bool=false,gameTime:f64=0,renderGameTime:f64=0,timeScale:f32=21600,solarConstant:f32=1361,planetRotationTime:f32=86400,simulationClock:@import("simulation_clock.zig").Clock=.{},rawFrameDelta:?f32=null,simulationStepsLastFrame:u8=0,pointerOnPlanet:bool=true,
 pub fn simulationSolarVector(_: *@This())u32{return 0;}
};
test "sixty exact ticks paused pace and redraw barrier"{var c=Controller{};var s=Mock{};try std.testing.expect(c.start(&s,1,1));try std.testing.expect(!c.start(&s,1,1));for(0..60)|_|try std.testing.expect(c.tick(&s,{},1,0.016));try std.testing.expect(c.phase==.redraw and c.busy());try std.testing.expect(!c.tick(&s,{},1,0.016));try std.testing.expect(s.gameTime==86400 and s.planet.ticks==60 and s.paused and s.timeScale==21600);c.didRedraw();try std.testing.expect(c.phase==.done and !c.busy() and c.blocks());}
test "cancel preserves partial progress and visibility gates redraw"{var c=Controller{};var s=Mock{};try std.testing.expect(c.start(&s,2,2));for(0..7)|_|_=c.tick(&s,{},2,0.016);c.environment(false,true);try std.testing.expect(!c.tick(&s,{},2,0.016));c.didRedraw();try std.testing.expect(c.busy());c.environment(true,true);c.didRedraw();try std.testing.expect(c.phase==.cancelled and c.completed==7 and s.gameTime==10080 and s.paused);}
test "stale world paused and state refusals are atomic"{var c=Controller{};var s=Mock{};try std.testing.expect(!c.start(&s,1,2));s.paused=false;try std.testing.expect(!c.start(&s,1,1));try std.testing.expect(c.token==0 and s.planet.ticks==0);s.paused=true;try std.testing.expect(c.start(&s,1,1));try std.testing.expect(!c.tick(&s,{},2,0.01));try std.testing.expect(s.gameTime==0 and s.paused);}
test "background gap context loss token exhaustion cannot advance"{var c=Controller{};var s=Mock{};try std.testing.expect(c.start(&s,1,1));try std.testing.expect(!c.tick(&s,{},1,3));try std.testing.expect(s.planet.ticks==0);c.environment(true,false);c.didRedraw();try std.testing.expect(c.recovery_required and !c.busy());c.environment(true,true);c.didRedraw();try std.testing.expect(!c.context_ok and c.recovery_required and c.canRecoverySave(&s,1));try std.testing.expect(!c.dismiss(c.token));try std.testing.expect(!c.start(&s,1,1));var exhausted=Controller{.token=std.math.maxInt(u32)};try std.testing.expect(!exhausted.start(&s,1,1));}

test "dismissal requires correct terminal ticket and neutral input"{var c=Controller{};var s=Mock{};try std.testing.expect(c.start(&s,1,1));try std.testing.expect(!c.dismiss(c.token));c.cancel("cancel");c.didRedraw();try std.testing.expect(!c.dismiss(c.token+1));c.releaseInput(true);try std.testing.expect(c.blocks());try std.testing.expect(c.dismiss(c.token));c.releaseInput(false);try std.testing.expect(c.blocks());c.releaseInput(true);try std.testing.expect(!c.blocks());}

test "recovery save belongs only to unchanged paused job world"{var c=Controller{};var s=Mock{};try std.testing.expect(c.start(&s,1,1));_=c.tick(&s,{},1,0.016);c.environment(true,false);try std.testing.expect(c.canRecoverySave(&s,1));try std.testing.expect(!c.canRecoverySave(&s,2));s.paused=false;try std.testing.expect(!c.canRecoverySave(&s,1));s.paused=true;s.gameTime+=1440;try std.testing.expect(!c.canRecoverySave(&s,1));}
