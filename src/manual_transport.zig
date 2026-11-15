//! Bounded session-only preview/one-use ticket. Never creates organisms or advances time.
const std=@import("std");const M=@import("simulation/microbes.zig");const Core=@import("manual_transfer_core.zig");
const Id=struct{value:u64,pub fn jsonStringify(self:@This(),w:anytype)!void{var b:[20]u8=undefined;try w.write(std.fmt.bufPrint(&b,"{d}",.{self.value}) catch unreachable);}};
const Pending=struct{ticket:Core.Ticket,token:u32,source_water:f32,target_water:f32,source_temp:f32,target_temp:f32,source_elevation:f32,target_elevation:f32};
const LastMove=struct{owner:usize,world:u32,target:usize,id:u64};
var last_move:?LastMove=null;
var pending:?Pending=null;var sequence:u32=0;var buffer:[8192]u8=undefined;
pub fn cancel()void{pending=null;}
pub fn reset()void{cancel();last_move=null;}
fn json(value:anytype)[:0]const u8{var stream=std.io.fixedBufferStream(buffer[0..buffer.len-1]);std.json.stringify(value,.{},stream.writer()) catch return "{\"ok\":false,\"reason\":\"Snapshot unavailable\"}";buffer[stream.pos]=0;return buffer[0..stream.pos:0];}
fn failure(reason:[]const u8)[:0]const u8{return json(.{.ok=false,.reason=reason});}
fn baseReason(state:anytype)?[]const u8{if(state.planet.worldMode!=.origin)return "Origin colonies only";if(!state.paused)return "Pause the game first";if(state.selectedPoint>=state.planet.microbeCells.len)return "Select a patch first";return null;}
fn eligible(c:M.Cohort)bool{return c.relocations==0 and c.last_from==0 and c.last_to==0 and c.last_move_time==0;}
pub fn guard(state:anytype,world:u32)void{
 const p=pending orelse return;const t=p.ticket;const planet=&state.planet;
 if(baseReason(state)!=null or world!=t.serial or @intFromPtr(planet)!=t.owner or state.gameTime!=t.time or state.selectedPoint!=t.from or t.to>=planet.microbeCells.len){cancel();return;}
 if(!std.meta.eql(planet.microbeCells[t.from],t.source) or !std.meta.eql(planet.microbeCells[t.to],t.target) or !std.meta.eql(planet.microbeStats,t.stats) or planet.waterMass[t.from]!=p.source_water or planet.waterMass[t.to]!=p.target_water or planet.temperature[t.from]!=p.source_temp or planet.temperature[t.to]!=p.target_temp or planet.elevation[t.from]!=p.source_elevation or planet.elevation[t.to]!=p.target_elevation)cancel();
}
pub fn status(state:anytype,world:u32)[:0]const u8{guard(state,world);return json(.{.pending=pending!=null,.token=if(pending)|p|p.token else @as(u32,0),.paused=state.paused,.world=world,.cell=state.selectedPoint});}
pub fn options(state:anytype,world:u32)[:0]const u8{
 guard(state,world);if(baseReason(state))|reason|return json(.{.available=false,.reason=reason,.paused=state.paused,.world=world});
 const p=&state.planet;const cell=state.selectedPoint;
 const Source=struct{slot:usize,id:Id,biomass:f32,support:f32,credit:f32,form:[]const u8,eligible:bool,reason:[]const u8,efficiency:f32,optimum_k:f32,structure:f32,organization:f32,feeding:f32,mobility:f32};
 var sources:[4]Source=undefined;var ns:usize=0;
 for(p.microbeCells[cell].cohorts,0..)|co,slot|if(co.biomass>0){sources[ns]=.{.slot=slot,.id=.{.value=co.lineage},.biomass=co.biomass,.support=co.support_mass,.credit=co.reproduction_credit,.form=M.producerFormName(M.producerForm(co)),.eligible=eligible(co),.reason=if(eligible(co)) "" else "Recorded autonomous travel cannot be rewritten",.efficiency=co.efficiency,.optimum_k=co.optimum,.structure=co.structure,.organization=co.organization,.feeding=co.feeding,.mobility=co.mobility};ns+=1;};
 const Neighbor=struct{cell:usize,depth_m:f32,temp_k:f32,count:usize,biomass:f64,free_slots:usize};var neighbors:[6]Neighbor=undefined;var nn:usize=0;
 for(p.getNeighbours(cell))|n|{if(nn==6)break;var count:usize=0;var mass:f64=0;for(p.microbeCells[n].cohorts)|co|{mass+=co.biomass;if(co.biomass>0)count+=1;}neighbors[nn]=.{.cell=n,.depth_m=p.waterMass[n]*p.getKmPerWaterMass()*1000,.temp_k=p.temperature[n],.count=count,.biomass=mass,.free_slots=4-count};nn+=1;}
 return json(.{.available=true,.reason="",.paused=true,.world=world,.cell=cell,.sources=sources[0..ns],.neighbors=neighbors[0..nn]});
}
pub fn prepare(state:anytype,world:u32,expected:u32,cell:i32,slot:i32,target:i32,id_text:[]const u8)[:0]const u8{
 cancel();if(baseReason(state))|reason|return failure(reason);
 if(expected!=world or cell<0 or @as(usize,@intCast(cell))!=state.selectedPoint or slot<0 or slot>=4 or target<0)return failure("Selection or world changed; refresh");
 if(id_text.len==0 or id_text.len>20 or id_text[0]=='0')return failure("Invalid colony ID");for(id_text)|c|if(c<'0' or c>'9')return failure("Invalid colony ID");
 const id=std.fmt.parseInt(u64,id_text,10) catch return failure("Invalid colony ID");
 const ticket=Core.prepare(state,world,@intCast(cell),@intCast(slot),@intCast(target)) orelse return failure("Colony or destination is not eligible");if(ticket.id!=id)return failure("Colony changed; refresh");
 var free:usize=0;var mass:f64=0;for(ticket.target.cohorts)|co|{mass+=co.biomass;if(co.biomass==0)free+=1;}if(free==0 or mass+@as(f64,ticket.source.cohorts[ticket.slot].biomass)>1)return failure("Destination lacks a vacant slot or capacity");
 if(sequence==std.math.maxInt(u32))return failure("Session ticket limit reached; reload");sequence+=1;
 const p=&state.planet;pending=.{.ticket=ticket,.token=sequence,.source_water=p.waterMass[ticket.from],.target_water=p.waterMass[ticket.to],.source_temp=p.temperature[ticket.from],.target_temp=p.temperature[ticket.to],.source_elevation=p.elevation[ticket.from],.target_elevation=p.elevation[ticket.to]};
 const co=ticket.source.cohorts[ticket.slot];return json(.{.ok=true,.token=sequence,.source=ticket.from,.target=ticket.to,.id=Id{.value=id},.mass=co.biomass,.support=co.support_mass,.credit=co.reproduction_credit,.form=M.producerFormName(M.producerForm(co)),.efficiency=co.efficiency,.optimum_k=co.optimum,.structure=co.structure,.organization=co.organization,.feeding=co.feeding,.mobility=co.mobility,.target_count=4-free,.target_free_slots=free,.target_biomass=mass,.depth_m=p.waterMass[ticket.to]*p.getKmPerWaterMass()*1000,.temp_k=p.temperature[ticket.to]});
}
pub fn execute(state:anytype,world:u32,token:u32)[:0]const u8{
 guard(state,world);const p=pending orelse return failure("Preview expired; refresh and choose again");cancel();if(token==0 or token!=p.token)return failure("Preview expired; refresh and choose again");
 const r=Core.execute(state,world,p.ticket);if(!r.ok)return failure("World changed; nothing moved");
 // Manual relocation is not mortality: retire only this ID from pending arrival-loss observation.
 state.planet.propaguleFeedback.forget(r.id);
 last_move=.{.owner=@intFromPtr(&state.planet),.world=world,.target=r.to,.id=r.id};
 state.colonyPeek.clear();state.communitySample=.{};@import("patch_watch.zig").current.stop("manual transport");
 return json(.{.ok=true,.manual=true,.world=world,.source=r.from,.target=r.to,.id=Id{.value=r.id},.mass=r.mass,.support=r.support,.credit=p.ticket.source.cohorts[p.ticket.slot].reproduction_credit,.sim_time=state.gameTime,.session_receipt=true});
}

pub fn inspect(state:anytype,world:u32,expected:u32,target:i32,id_text:[]const u8)[:0]const u8{
 const last=last_move orelse return failure("No manual transport receipt in this world");
 if(expected!=world or world!=last.world or @intFromPtr(&state.planet)!=last.owner or state.planet.worldMode!=.origin or target<0 or @as(usize,@intCast(target))!=last.target or last.target>=state.planet.microbeCells.len)return failure("Receipt belongs to another world or destination");
 if(id_text.len==0 or id_text.len>20 or id_text[0]=='0')return failure("Invalid colony ID");for(id_text)|c|if(c<'0' or c>'9')return failure("Invalid colony ID");const id=std.fmt.parseInt(u64,id_text,10) catch return failure("Invalid colony ID");if(id!=last.id)return failure("Receipt colony changed");
 var present=false;for(state.planet.microbeCells[last.target].cohorts)|co|if(co.biomass>0 and co.lineage==last.id){present=true;break;};if(!present)return failure("That colony is no longer living at the destination");
 cancel();state.selectedPoint=last.target;state.colonyPeek.clear();@import("patch_watch.zig").current.stop("selection changed");
 return json(.{.ok=true,.cell=last.target,.id=Id{.value=last.id},.world=world});
}
