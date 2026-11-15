//! QA observer only, disabled by default; no model decisions use this data.
const std=@import("std");pub var enabled=false;
pub fn emit(value:anytype)void{if(!enabled)return;var b:[4096]u8=undefined;var s=std.io.fixedBufferStream(&b);std.json.stringify(value,.{},s.writer())catch return;std.debug.print("WIND_PACKET {s}\n",.{s.getWritten()});}
