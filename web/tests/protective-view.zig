//! Current exact selected cohort state only, never ancestry or survival forecasts.
const std=@import("std");const M=@import("simulation/microbes.zig");var buffer:[4096]u8=undefined;
pub fn snapshot(state:anytype,world:u32)[*:0]const u8{
 var out=std.io.fixedBufferStream(buffer[0..buffer.len-1]);const Row=struct{id:[]const u8,investment:f32,status:[]const u8,recovery_seconds:?f32};var ids:[4][24]u8=undefined;var rows:[4]Row=undefined;var count:usize=0;var point:?u32=null;var enabled=false;
 if(state)|s|{enabled=@import("combined_view.zig").writerVersion(s)==15;if(enabled and s.selectedPoint<s.planet.microbeCells.len and s.selectedPoint<=std.math.maxInt(u32)){point=@intCast(s.selectedPoint);for(s.planet.microbeCells[s.selectedPoint].cohorts)|c|{if(c.biomass<=0 or c.lineage==0 or !M.validProtection(c))continue;const id=std.fmt.bufPrint(&ids[count],"{d}",.{c.lineage}) catch return "{}";rows[count]=.{.id=id,.investment=c.protective_investment,.status=if(c.protective_clock<0)"active"else if(c.protective_clock==0)"protecting"else"recovering",.recovery_seconds=if(c.protective_clock<0)null else c.protective_clock};count+=1;}}}
 std.json.stringify(.{.status=if(enabled)"protective"else"unavailable",.world_serial=world,.cell=point,.law=if(enabled)@as(u8,1)else 0,.cohorts=rows[0..count]},.{},out.writer()) catch return "{}";buffer[out.pos]=0;return @ptrCast(&buffer);
}
