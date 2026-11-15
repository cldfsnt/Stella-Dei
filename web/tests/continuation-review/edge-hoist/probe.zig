const std=@import("std");const W=@import("atmosphere_water.zig");
export fn baseline(points:[*]const [3]f32,winds:[*]const [3]f32,neighbors:[*]const [6]u32,out:[*][6]f64,count:usize)void{
 for(0..count)|i|{for(neighbors[i],0..)|n,j|{const a=points[i];const b=points[n];const w=winds[i];out[i][j]=W.edgeRate(.{a[0],a[1],a[2]},.{b[0],b[1],b[2]},.{w[0],w[1],w[2]});}}
}
export fn candidate(points:[*]const [3]f32,winds:[*]const [3]f32,neighbors:[*]const [6]u32,out:[*][6]f64,count:usize)void{
 for(0..count)|i|{const a=points[i];const w=winds[i];var valid=true;for(0..3)|k|{if(!std.math.isFinite(a[k]) or !std.math.isFinite(w[k]))valid=false;}
 for(neighbors[i],0..)|n,j|{if(!valid){out[i][j]=0;continue;}const b=points[n];var length2:f64=0;var dot:f64=0;var dest_valid=true;
 for(0..3)|k|{if(!std.math.isFinite(b[k])){dest_valid=false;break;}const d=@as(f64,b[k])-a[k];length2+=d*d;dot+=@as(f64,w[k])*d;}
 out[i][j]=if(!dest_valid or length2<=0 or !std.math.isFinite(length2) or !std.math.isFinite(dot))0 else @max(0,dot/length2);
 }}
}
pub fn main()!void{
 const a=std.heap.page_allocator;const n=40962;const points=try a.alloc([3]f32,n);const winds=try a.alloc([3]f32,n);const ns=try a.alloc([6]u32,n);const x=try a.alloc([6]f64,n);const y=try a.alloc([6]f64,n);
 var rng=std.rand.DefaultPrng.init(2027);const random=rng.random();for(0..n)|i|{for(0..3)|k|{points[i][k]=random.float(f32)*2000-1000;winds[i][k]=random.float(f32)*0.02-0.01;}for(0..6)|j|ns[i][j]=@intCast((i+j+1)%n);}
 baseline(points.ptr,winds.ptr,ns.ptr,x.ptr,n);candidate(points.ptr,winds.ptr,ns.ptr,y.ptr,n);
 for(x,y)|xx,yy|for(xx,yy)|v,w|{if(@as(u64,@bitCast(v))!=@as(u64,@bitCast(w)))return error.Parity;};
 std.debug.print("EDGE_PARITY edges={d} exact=true\n",.{n*6});
 for([_]f32{0,-0.0,std.math.inf(f32),-std.math.inf(f32),std.math.nan(f32)})|special|{points[0][0]=special;winds[1][2]=special;baseline(points.ptr,winds.ptr,ns.ptr,x.ptr,n);candidate(points.ptr,winds.ptr,ns.ptr,y.ptr,n);for(x,y)|xx,yy|for(xx,yy)|v,w|{if(@as(u64,@bitCast(v))!=@as(u64,@bitCast(w)))return error.SpecialParity;};}
 points[0][0]=0;winds[1][2]=0;
 for(0..6)|trial|{for([_]usize{if(trial%2==0)0 else 1,if(trial%2==0)1 else 0})|arm|{var timer=try std.time.Timer.start();for(0..50)|_|{if(arm==0)baseline(points.ptr,winds.ptr,ns.ptr,x.ptr,n) else candidate(points.ptr,winds.ptr,ns.ptr,x.ptr,n);std.mem.doNotOptimizeAway(x.ptr);}const elapsed=timer.read();std.debug.print("EDGE_MICRO trial={d} arm={d} ns={d} checksum={d}\n",.{trial,arm,elapsed,x[100][3]});}}
}
