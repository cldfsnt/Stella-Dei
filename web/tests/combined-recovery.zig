//! Explicit user recovery only. Never writes canonical world.json or a backup.
const std=@import("std");const S=@import("save_game.zig");const V=@import("combined_view.zig");
const directory="/wetlands-saves";
const Plan=struct{token:u32,world:u32,writer:u32,epoch:u64,hash:[32]u8};var plan:?Plan=null;var sequence:u32=0;var buffer:[512]u8=undefined;
fn reply(status:[]const u8,world:u32,writer:u32,token:u32,hash:[]const u8,bytes:usize)[*:0]const u8{var s=std.io.fixedBufferStream(buffer[0..buffer.len-1]);std.json.stringify(.{.status=status,.world_serial=world,.writer_version=writer,.token=token,.sha256=hash,.bytes=bytes},.{},s.writer()) catch return "{}";buffer[s.pos]=0;return @ptrCast(&buffer);}
fn digest(bytes:[]const u8)[32]u8{var h:[32]u8=undefined;std.crypto.hash.sha2.Sha256.hash(bytes,&h,.{});return h;}
const HashWriter=struct{hash:std.crypto.hash.sha2.Sha256=std.crypto.hash.sha2.Sha256.init(.{}),bytes:usize=0,fn write(self:*@This(),data:[]const u8)error{SaveTooLarge}!usize{if(data.len>S.save_io.max_save_bytes-self.bytes)return error.SaveTooLarge;self.hash.update(data);self.bytes+=data.len;return data.len;}fn writer(self:*@This())std.io.Writer(*@This(),error{SaveTooLarge},write){return .{.context=self};}};
fn stateHash(a:std.mem.Allocator,state:anytype)![32]u8{const save=try S.capture(a,state);try save.validate();var w=HashWriter{};try std.json.stringify(save,.{},w.writer());var h:[32]u8=undefined;w.hash.final(&h);return h;}
pub fn cancel(token:u32)i32{if(plan)|p|if(token!=0 and token==p.token){plan=null;return 1;};return 0;}
pub fn prepare(state:anytype,world:u32,expected:u32,writer:u32)[*:0]const u8{
 plan=null;if(world!=expected or writer!=V.writerVersion(state) or writer==0)return reply("stale",world,V.writerVersion(state),0,"",0);
 if(!state.paused)return reply("pause_required",world,writer,0,"",0);
 if(sequence==std.math.maxInt(u32))return reply("unavailable",world,writer,0,"",0);
 var arena=std.heap.ArenaAllocator.init(std.heap.page_allocator);defer arena.deinit();const a=arena.allocator();
 const save=S.capture(a,state) catch return reply("invalid",world,writer,0,"",0);save.validate() catch return reply("invalid",world,writer,0,"",0);
 std.fs.cwd().makePath(directory) catch return reply("storage_error",world,writer,0,"",0);var dir=std.fs.cwd().openDir(directory,.{}) catch return reply("storage_error",world,writer,0,"",0);defer dir.close();
 S.save_io.writeJsonAtomic(dir,"world.recovery-current.json","world.recovery-current.tmp",save,S.save_io.max_save_bytes) catch return reply("storage_error",world,writer,0,"",0);
 const bytes=dir.readFileAlloc(a,"world.recovery-current.json",S.save_io.max_save_bytes) catch return reply("storage_error",world,writer,0,"",0);const h=digest(bytes);sequence+=1;plan=.{.token=sequence,.world=world,.writer=writer,.epoch=@import("rooted_founder.zig").epoch,.hash=h};const hex=std.fmt.bytesToHex(h,.lower);return reply("ready",world,writer,sequence,&hex,bytes.len);
}
///0success,-1unavailable/busy,-2stale,-3invalidtarget,-4backupmissing,-5applyfailure.
pub fn apply(state:anytype,world:u32,token:u32,kind:u32,hex:[]const u8)i32{
 const p=plan orelse return -2;if(token==0 or token!=p.token)return -2;plan=null;
 if(!state.paused or world!=p.world or V.writerVersion(state)!=p.writer or @import("rooted_founder.zig").epoch!=p.epoch)return -2;
 if(hex.len!=64)return -3;for(hex)|c|if(!((c>='0' and c<='9')or(c>='a' and c<='f')))return -3;
 var expected:[32]u8=undefined;_=std.fmt.hexToBytes(&expected,hex) catch return -3;
 var arena=std.heap.ArenaAllocator.init(std.heap.page_allocator);defer arena.deinit();const a=arena.allocator();var name:[160]u8=undefined;
 const path=switch(kind){0=>"world.pre-v7.json",1=>"world.pre-v13.json",2=>std.fmt.bufPrint(&name,"world.pre-v13.sha256-{s}.json",.{hex}) catch return -3,3=>std.fmt.bufPrint(&name,"world.recovery.sha256-{s}.json",.{hex}) catch return -3,else=>return -3};
 var dir=std.fs.cwd().openDir(directory,.{}) catch return -3;defer dir.close();const target=dir.readFileAlloc(a,path,S.save_io.max_save_bytes) catch return -3;if(!std.mem.eql(u8,&digest(target),&expected))return -3;
 var parsed=S.schema.parse(a,target) catch return -3;defer parsed.deinit();parsed.value.validate() catch return -3;if(parsed.value.subdivisions!=6 and parsed.value.subdivisions!=7)return -3;
 const current_hex=std.fmt.bytesToHex(p.hash,.lower);var backup_name:[160]u8=undefined;const backup_path=std.fmt.bufPrint(&backup_name,"world.recovery.sha256-{s}.json",.{current_hex}) catch return -4;
 const backup=dir.readFileAlloc(a,backup_path,S.save_io.max_save_bytes) catch return -4;if(!std.mem.eql(u8,&digest(backup),&p.hash))return -4;
 const now=stateHash(a,state) catch return -2;if(!std.mem.eql(u8,&now,&p.hash))return -2;
 S.replaceWorld(state,parsed.value) catch return -5;return 0;
}
