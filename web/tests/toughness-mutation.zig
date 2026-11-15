//! Isolated mutation law2. Deterministic event-keyed domain separation, not true independent randomness.
const std=@import("std");
pub const Config=struct{enabled:bool=false,stream_seed:u64=0};
pub fn digest(stream_seed:u64,event_seed:u64,generation:u32)[32]u8{
 var input=[_]u8{0}**48;
 @memcpy(input[0..16],"STELLA-TOUGH-V2!");
 std.mem.writeInt(u32,input[16..20],2,.little);
 std.mem.writeInt(u64,input[24..32],stream_seed,.little);
 std.mem.writeInt(u64,input[32..40],event_seed,.little);
 std.mem.writeInt(u32,input[40..44],generation,.little);
 var result:[32]u8=undefined;std.crypto.hash.sha2.Sha256.hash(&input,&result,.{});return result;
}
pub fn proposal(stream_seed:u64,event_seed:u64,generation:u32)f32{
 const bytes=digest(stream_seed,event_seed,generation);
 if(bytes[0]&63!=0)return 0;
 return if(bytes[1]&1==0) @as(f32,1.0/32.0) else -@as(f32,1.0/32.0);
}
pub fn allocation(old:f32,event_seed:u64,generation:u32,config:Config)f32{
 if(!config.enabled)return old;
 return std.math.clamp(old+proposal(config.stream_seed,event_seed,generation),0,1);
}
