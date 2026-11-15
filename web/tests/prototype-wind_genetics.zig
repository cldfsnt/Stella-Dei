//! Explicit experimental game genetics; domain-keyed, no fitness input.
const std=@import("std");
pub const Config=struct{enabled:bool=false,law:u8=0,stream_seed:u64=0,serial:u64=0,pub fn valid(c:@This())bool{return if(c.enabled)c.law==1 else c.law==0 and c.stream_seed==0 and c.serial==0;}};
pub fn draw(seed:u64,event:u64,parent:u64,domain:u64)f64{var b:[32]u8=undefined;std.mem.writeInt(u64,b[0..8],seed,.little);std.mem.writeInt(u64,b[8..16],event,.little);std.mem.writeInt(u64,b[16..24],parent,.little);std.mem.writeInt(u64,b[24..32],domain,.little);var out:[32]u8=undefined;std.crypto.hash.sha2.Sha256.hash(&b,&out,.{});return @as(f64,@floatFromInt(std.mem.readInt(u64,out[0..8],.little)>>11))/9007199254740992.0;}
pub fn mutation(old:f32,seed:u64,parent:u64,child:u64,generation:u32)f32{const u=draw(seed,child,parent,0x57494e4447454e31 ^ @as(u64,generation));return @floatCast(std.math.clamp(@as(f64,old)+(u-0.5)*0.2,0,1));}

test "fixed inherited mutation symmetry bounds and memory"{
 var positive:usize=0;var negative:usize=0;for(1..8193)|id|{const v=mutation(0.5,42,17,id,1);try std.testing.expect(v>=0.4 and v<=0.6);try std.testing.expectEqual(v,mutation(0.5,42,17,id,1));if(v>0.5)positive+=1 else if(v<0.5)negative+=1;try std.testing.expect(mutation(0,42,17,id,1)>=0);try std.testing.expect(mutation(1,42,17,id,1)<=1);}
 try std.testing.expect(positive>0 and negative>0);std.debug.print("WIND_MUTATION keys8192 positive{} negative{} config_bytes{}\n",.{positive,negative,@sizeOf(Config)});
}
