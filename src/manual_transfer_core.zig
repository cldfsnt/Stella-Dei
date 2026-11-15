//! Manual god transport, not autonomous movement or reproduction.
const std=@import("std");const M=@import("simulation/microbes.zig");
pub const Ticket=struct{owner:usize,serial:u32,time:f64,from:usize,slot:usize,to:usize,id:u64,source:M.Cell,target:M.Cell,stats:M.Stats};
pub const Receipt=struct{ok:bool=false,id:u64=0,from:usize=0,to:usize=0,slot:usize=0,mass:f32=0,support:f32=0};
pub fn prepare(state:anytype,serial:u32,from:usize,slot:usize,to:usize)?Ticket{
 const p=&state.planet;
 if(!state.paused or !std.math.isFinite(state.gameTime) or state.gameTime<0 or p.worldMode!=.origin or from>=p.microbeCells.len or to>=p.microbeCells.len or from==to or slot>=4)return null;
 var adjacent=false;for(p.getNeighbours(from))|n|if(n==to){adjacent=true;break;};if(!adjacent)return null;
 const c=p.microbeCells[from].cohorts[slot];if(c.biomass<=0 or c.lineage==0 or c.relocations!=0 or c.last_from!=0 or c.last_to!=0 or c.last_move_time!=0)return null;
 if(!M.validCell(p.microbeCells[from],p.microbeStats.next_lineage) or !M.validCell(p.microbeCells[to],p.microbeStats.next_lineage))return null;
 return .{.owner=@intFromPtr(p),.serial=serial,.time=state.gameTime,.from=from,.slot=slot,.to=to,.id=c.lineage,.source=p.microbeCells[from],.target=p.microbeCells[to],.stats=p.microbeStats};
}
pub fn execute(state:anytype,serial:u32,t:Ticket)Receipt{
 const p=&state.planet;
 if(t.owner!=@intFromPtr(p) or serial!=t.serial or state.gameTime!=t.time)return .{};
 const fresh=prepare(state,serial,t.from,t.slot,t.to) orelse return .{};
 if(fresh.id!=t.id or !std.meta.eql(fresh.source,t.source) or !std.meta.eql(fresh.target,t.target) or !std.meta.eql(fresh.stats,t.stats))return .{};
 const co=t.source.cohorts[t.slot];var target=t.target;var empty:?usize=null;var total:f64=co.biomass;
 for(target.cohorts,0..)|c,i|{total+=c.biomass;if(c.biomass==0 and empty==null)empty=i;}
 const dest=empty orelse return .{};if(total>1)return .{};
 var source=t.source;source.cohorts[t.slot]=.{};target.cohorts[dest]=co;
 if(!M.validCell(source,p.microbeStats.next_lineage) or !M.validCell(target,p.microbeStats.next_lineage))return .{};
 p.microbeCells[t.from]=source;p.microbeCells[t.to]=target;
 return .{.ok=true,.id=co.lineage,.from=t.from,.to=t.to,.slot=dest,.mass=co.biomass,.support=co.support_mass};
}
