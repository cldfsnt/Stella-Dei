const C=@import("experimental/liquid_gather_cached.zig");
export fn qa_cached(mass:[*]const f32,elevation:[*]const f32,neighbors:[*]const [6]usize,reverse:[*]const [6]u8,edges:[*][6]f64,out:[*]f32,n:usize,km:f32,dt:f32)bool{
 _=C.step(mass[0..n],elevation[0..n],neighbors[0..n],reverse[0..n],edges[0..n],out[0..n],km,dt,false) catch return false;return true;
}
