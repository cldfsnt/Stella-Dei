//! Experimental v1 deterministic lineage-keyed stream; not independent true randomness.
const std=@import("std");
pub fn digest(seed:u64,parent:u64,child:u64,generation:u32)[32]u8{
 var input=[_]u8{0}**44;@memcpy(input[0..13],"STELLA-RET-V1");
 std.mem.writeInt(u64,input[16..24],seed,.little);std.mem.writeInt(u64,input[24..32],parent,.little);std.mem.writeInt(u64,input[32..40],child,.little);std.mem.writeInt(u32,input[40..44],generation,.little);
 var out:[32]u8=undefined;std.crypto.hash.sha2.Sha256.hash(&input,&out,.{});return out;
}
pub fn proposal(seed:u64,parent:u64,child:u64,generation:u32)f32{const d=digest(seed,parent,child,generation);if(d[0]&63!=0)return 0;return if(d[1]&1==0)@as(f32,1.0/32.0) else -@as(f32,1.0/32.0);}
pub fn allocation(old:f32,seed:u64,parent:u64,child:u64,generation:u32)f32{return std.math.clamp(old+proposal(seed,parent,child,generation),0,1);}
