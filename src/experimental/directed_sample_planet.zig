//! Research-only current-world ticket, actual Planet adjacency and exact stale-state guard.
const std=@import("std");const P=@import("../simulation/planet.zig").Planet;const M=@import("../simulation/microbes.zig");const D=@import("directed_sample.zig");const World=@import("../performance_details.zig");
pub const Ticket=struct{owner:usize,serial:u32,from:usize,slot:usize,to:usize,id:u64,source:M.Cell,target:M.Cell};
pub fn prepare(p:*P,from:usize,slot:usize,to:usize)?Ticket{
 if(p.worldMode!=.origin or from>=p.microbeCells.len or to>=p.microbeCells.len or from==to or slot>=4)return null;
 var adjacent=false;for(p.getNeighbours(from))|n|if(n==to){adjacent=true;break;};if(!adjacent)return null;
 const co=p.microbeCells[from].cohorts[slot];if(co.biomass<=0 or co.lineage==0)return null;
 return .{.owner=@intFromPtr(p),.serial=World.world_serial,.from=from,.slot=slot,.to=to,.id=co.lineage,.source=p.microbeCells[from],.target=p.microbeCells[to]};
}
pub fn execute(p:*P,t:Ticket)D.Receipt{
 if(t.owner!=@intFromPtr(p) or t.serial!=World.world_serial or p.worldMode!=.origin or t.from>=p.microbeCells.len or t.to>=p.microbeCells.len or t.slot>=4)return .{};
 if(!std.meta.eql(t.source,p.microbeCells[t.from]) or !std.meta.eql(t.target,p.microbeCells[t.to]) or p.microbeCells[t.from].cohorts[t.slot].lineage!=t.id)return .{};
 var neighbors:[6]usize=undefined;for(p.getNeighbours(t.from),0..)|n,i|neighbors[i]=n;
 return D.apply(p.microbeCells,&p.microbeStats,t.from,t.slot,t.to,t.id,World.world_serial,t.serial,&neighbors);
}
