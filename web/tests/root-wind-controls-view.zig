//! Read-only explicit runtime/writer identity; no conversions or mutation.
const std=@import("std");var buffer:[512]u8=undefined;
pub fn writerVersion(s:anytype)u32{
 const p=&s.planet;if(!p.windDispersal.valid())return 0;
 if(p.windDispersal.enabled)return if(p.worldMode==.origin and p.landBeta.valid() and p.landBeta.enabled and p.landBeta.physiology_law==3)13 else 0;
 if(p.landBeta.enabled)return if(p.landBeta.valid())switch(p.landBeta.physiology_law){1=>8,2=>9,3=>10,else=>0} else 0;
 return 7;
}
pub fn snapshot(state:anytype,world:u32)[*:0]const u8{
 var out=std.io.fixedBufferStream(buffer[0..buffer.len-1]);const writer=if(state)|s|writerVersion(s)else 0;
 std.json.stringify(.{.status=if(writer==13)"combined" else if(writer==10)"wetlands" else if(writer==8 or writer==9)"historical_beta" else if(writer==7)"legacy" else "unavailable",.world_serial=world,.writer_version=writer,.enabled=writer==13,.root_physiology=if(state)|s|s.planet.landBeta.physiology_law else @as(u8,0),.wind_law=if(state)|s|s.planet.windDispersal.law else @as(u8,0)},.{},out.writer()) catch return "{}";buffer[out.pos]=0;return @ptrCast(&buffer);
}
