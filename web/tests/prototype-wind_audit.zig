//! QA observer only, disabled by default; no model decisions use this data.
const std=@import("std");pub var enabled=false;
fn write(comptime tag:[]const u8,value:anytype)void{if(!enabled)return;var b:[4096]u8=undefined;var s=std.io.fixedBufferStream(&b);std.json.stringify(value,.{},s.writer()) catch return;std.debug.print("{s} {s}\n",.{tag,s.getWritten()});}
pub fn emit(value:anytype)void{write("WIND_PACKET",value);}
pub fn opportunity(value:anytype)void{write("WIND_OPPORTUNITY",value);}
