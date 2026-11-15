//! Optional experimental proposal only. Not wired to model or saves.
const std=@import("std");
pub const Pair=struct{root:f32,storage:f32};
pub const Draw=struct{event:bool,root:bool,positive:bool};
pub fn valid(p:Pair)bool{return std.math.isFinite(p.root) and std.math.isFinite(p.storage) and p.root>=0 and p.storage>=0 and @as(f64,p.root)+p.storage<=1;}
pub fn draw(seed:u64,parent:u64,child:u64,generation:u32)Draw{
 var bytes=[_]u8{0}**48;@memcpy(bytes[0..15],"STELLA-ALLOC-V1");std.mem.writeInt(u64,bytes[16..24],seed,.little);std.mem.writeInt(u64,bytes[24..32],parent,.little);std.mem.writeInt(u64,bytes[32..40],child,.little);std.mem.writeInt(u32,bytes[40..44],generation,.little);var hash:[32]u8=undefined;std.crypto.hash.sha2.Sha256.hash(&bytes,&hash,.{});return .{.event=hash[0]&63==0,.root=hash[1]&1==0,.positive=hash[2]&1==0};
}
pub fn apply(legacy:Pair,enabled:bool,d:Draw)?Pair{
 if(!valid(legacy))return null;if(!enabled or !d.event)return legacy;var next=legacy;const delta:f32=if(d.positive)1.0/32.0 else -1.0/32.0;if(d.root)next.root+=delta else next.storage+=delta;return if(valid(next))next else legacy;
}
