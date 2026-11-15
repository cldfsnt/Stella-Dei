//! Explicit atomic all-seed-point intervention. Private staging only until Apply.
const std=@import("std");const P=@import("simulation/planet.zig").Planet;const M=@import("simulation/microbes.zig");
pub const Phase=enum{idle,planning,ready,applied,cancelled,failed};
pub const batch_size:usize=512;
const Plan=struct{original:P,staged:P,owner:usize,storage:usize,water_storage:usize,temp_storage:usize,world:u32,time:f64,pace:f32};
var arena:?std.heap.ArenaAllocator=null;var plan:?Plan=null;var sequence:u32=0;
var phase:Phase=.idle;var token:u32=0;var world_id:u32=0;var scanned:usize=0;var total:usize=0;var eligible:usize=0;var planted:usize=0;var skipped:usize=0;var resource_skips:usize=0;var identity_skips:usize=0;var reason:[]const u8="No plan";var buffer:[2048]u8=undefined;
fn release()void{plan=null;if(arena)|*a|a.deinit();arena=null;}
fn reply(ok:bool)[:0]const u8{var s=std.io.fixedBufferStream(buffer[0..buffer.len-1]);std.json.stringify(.{.ok=ok,.phase=@tagName(phase),.token=token,.world=world_id,.scanned=scanned,.total=total,.eligible=eligible,.planted=planted,.skipped=skipped,.ineligible=scanned-eligible,.resource_skips=resource_skips,.identity_skips=identity_skips,.reason=reason,.batch_size=batch_size},.{},s.writer()) catch return "{\"ok\":false,\"phase\":\"failed\",\"reason\":\"Reply unavailable\"}";buffer[s.pos]=0;return buffer[0..s.pos:0];}
fn fail(why:[]const u8)[:0]const u8{release();phase=.failed;reason=why;return reply(false);}
pub fn invalidate(why:[]const u8)void{if(plan!=null){release();phase=.cancelled;reason=why;}}
fn identity(state:anytype,world:u32,p:*const Plan)bool{return state.paused and std.math.isFinite(state.gameTime) and state.gameTime==p.time and state.timeScale==p.pace and world==p.world and @intFromPtr(&state.planet)==p.owner and state.planet.worldMode==.origin and state.planet.radius==p.original.radius and state.planet.seed==p.original.seed and state.planet.vertices.len==p.original.vertices.len and state.planet.microbeCells.len==total and state.planet.waterMass.len==total and state.planet.temperature.len==total and @intFromPtr(state.planet.microbeCells.ptr)==p.storage and @intFromPtr(state.planet.waterMass.ptr)==p.water_storage and @intFromPtr(state.planet.temperature.ptr)==p.temp_storage;}
pub fn guard(state:anytype,world:u32)void{if(plan)|*p|{if(!identity(state,world,p))invalidate("World, pause or time changed; nothing seeded");}}
fn unchanged(state:anytype,p:*const Plan)bool{
 const live=&state.planet;
 if(live.averageCarbonDioxideMass!=p.original.averageCarbonDioxideMass or live.averageOxygenMass!=p.original.averageOxygenMass or !std.meta.eql(live.microbeStats,p.original.microbeStats))return false;
 if(!std.mem.eql(f32,live.waterMass,p.original.waterMass) or !std.mem.eql(f32,live.temperature,p.original.temperature) or !std.mem.eql(f32,live.elevation,p.original.elevation))return false;
 for(live.microbeCells,p.original.microbeCells)|a,b|{if(!std.meta.eql(a,b))return false;}return true;
}
pub fn start(state:anytype,world:u32,expected:u32)[:0]const u8{return startWithAllocator(state,world,expected,std.heap.page_allocator);}
pub fn startWithAllocator(state:anytype,world:u32,expected:u32,backing:std.mem.Allocator)[:0]const u8{
 if(plan!=null){reason="Finish or cancel the current plan first";return reply(false);}
 if(world!=expected or !state.paused or state.planet.worldMode!=.origin or !std.math.isFinite(state.gameTime) or !std.math.isFinite(state.timeScale))return fail("Requires the same paused Origin world");
 const p=&state.planet;const n=p.microbeCells.len;if(n==0 or n!=p.vertices.len or n!=p.waterMass.len or n!=p.temperature.len or n!=p.elevation.len or !std.math.isFinite(p.radius) or p.radius<=0 or !std.math.isFinite(p.averageCarbonDioxideMass) or p.averageCarbonDioxideMass<0 or !std.math.isFinite(p.averageOxygenMass) or p.averageOxygenMass<0)return fail("World resources unavailable");
 if(sequence==std.math.maxInt(u32))return fail("Plan limit reached; reload before another plan");
 scanned=0;total=n;eligible=0;planted=0;skipped=0;resource_skips=0;identity_skips=0;
 arena=std.heap.ArenaAllocator.init(backing);const a=arena.?.allocator();
 var original=p.*;original.microbeCells=a.dupe(M.Cell,p.microbeCells) catch return fail("Not enough memory; nothing seeded");original.waterMass=a.dupe(f32,p.waterMass) catch return fail("Not enough memory; nothing seeded");original.temperature=a.dupe(f32,p.temperature) catch return fail("Not enough memory; nothing seeded");original.elevation=a.dupe(f32,p.elevation) catch return fail("Not enough memory; nothing seeded");
 var staged=original;staged.microbeCells=a.dupe(M.Cell,original.microbeCells) catch return fail("Not enough memory; nothing seeded");
 sequence+=1;token=sequence;world_id=world;scanned=0;total=n;eligible=0;planted=0;skipped=0;resource_skips=0;identity_skips=0;
 plan=.{.original=original,.staged=staged,.owner=@intFromPtr(p),.storage=@intFromPtr(p.microbeCells.ptr),.water_storage=@intFromPtr(p.waterMass.ptr),.temp_storage=@intFromPtr(p.temperature.ptr),.world=world,.time=state.gameTime,.pace=state.timeScale};phase=.planning;reason="Planning all initially eligible seed points; world unchanged";return reply(true);
}
pub fn step(state:anytype,world:u32,wanted:u32)[:0]const u8{
 guard(state,world);if(plan==null or wanted==0 or wanted!=token or phase!=.planning){reason="Plan unavailable or token changed";return reply(false);}
 var p=&plan.?;const end=@min(total,scanned+@min(batch_size,total-scanned));
 for(scanned..end)|i|{
  scanned=i+1;
  if(!M.validCell(p.original.microbeCells[i],p.original.microbeStats.next_lineage))return fail("Invalid colony state; nothing seeded");
  if(p.original.seedEligibility(i)==.eligible){eligible+=1;
   if(p.staged.microbeStats.next_lineage==std.math.maxInt(u64)){skipped+=1;identity_skips+=1;}else if(p.staged.seedMicrobes(i)){planted+=1;}else{skipped+=1;resource_skips+=1;}
  }
 }
 scanned=end;if(scanned==total){if(!unchanged(state,p))return fail("World resources changed; nothing seeded");phase=.ready;reason="Review staged result; Apply seeds once, Cancel changes nothing";}
 return reply(true);
}
pub fn status(state:anytype,world:u32)[:0]const u8{guard(state,world);if(plan)|*p|{if(phase==.ready and !unchanged(state,p))return fail("World resources changed; nothing seeded");}return reply(phase!=.failed);}
pub fn cancel(wanted:u32)[:0]const u8{if(wanted==0 or wanted!=token){reason="Plan token changed";return reply(false);}if(plan!=null){release();phase=.cancelled;reason="Cancelled; nothing seeded";}return reply(true);}
pub fn apply(state:anytype,world:u32,wanted:u32)[:0]const u8{
 guard(state,world);if(plan==null or phase!=.ready or wanted==0 or wanted!=token){reason="Plan unavailable or already applied";return reply(false);}
 const p=&plan.?;if(!unchanged(state,p))return fail("World resources changed; nothing seeded");
 // seedMicrobes mutates exactly cohort/nutrient state, stats and atmospheric C/O.
 @memcpy(state.planet.microbeCells,p.staged.microbeCells);state.planet.microbeStats=p.staged.microbeStats;state.planet.averageCarbonDioxideMass=p.staged.averageCarbonDioxideMass;state.planet.averageOxygenMass=p.staged.averageOxygenMass;
 state.communitySample=.{};state.colonyPeek.clear();@import("patch_watch.zig").current.stop("World seeded explicitly");
 release();phase=.applied;reason="Applied one resource-paid seed per planned point where funding succeeded";return reply(true);
}
