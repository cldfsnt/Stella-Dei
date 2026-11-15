const std=@import("std");const W=@import("simulation/atmosphere_water.zig");
fn checked(from:[3]f64,to:[3]f64,wind:[3]f64) !void{
 var valid=true;for(to)|v|if(!std.math.isFinite(v)){valid=false;};
 const src=W.EdgeSource.init(from,wind);const a=src.rate(to);const b=if(valid)src.rateFiniteTarget(to) else src.rate(to);
 try std.testing.expectEqual(@as(u64,@bitCast(a)),@as(u64,@bitCast(b)));
}
test "target-only finite hoist preserves exact extreme and invalid results"{
 const values=[_]f64{0,-0.0,1,-1,std.math.floatMax(f32),-std.math.floatMax(f32),@as(f32,@bitCast(@as(u32,1))),std.math.inf(f64),-std.math.inf(f64),std.math.nan(f64)};
 for(values)|x|for(values)|y|for(values)|z|try checked(.{x,1,-1},.{y,z,x},.{z,-y,1});
 try checked(.{0,0,0},.{1e200,1e200,1e200},.{1,1,1});
 try checked(.{0,0,0},.{1,1,1},.{1e308,1e308,1e308});
 var rng=std.rand.DefaultPrng.init(0x35d116);const random=rng.random();
 var count:usize=0;for(0..200000)|_|{var from:[3]f64=undefined;var to:[3]f64=undefined;var wind:[3]f64=undefined;for(0..3)|i|{from[i]=@as(f32,@bitCast(random.int(u32)));to[i]=@as(f32,@bitCast(random.int(u32)));wind[i]=@as(f32,@bitCast(random.int(u32)));}try checked(from,to,wind);count+=1;}
 std.debug.print("EDGE_VALIDATION exact randomized={d} boundary=1002\n",.{count});
}
test "one nonfinite target makes whole batch use generic branch"{
 const points=[_][3]f64{.{1,2,3},.{std.math.nan(f64),0,0},.{-1,2,3}};
 var all=true;for(points)|p|for(p)|v|{if(!std.math.isFinite(v))all=false;};try std.testing.expect(!all);
 for(points)|p|try checked(.{1,0,0},p,.{0,1,0});
}
fn batch(points:[]const [3]f32,out:[]f64)bool{
 var all=true;for(points)|p|{if(!std.math.isFinite(p[0]) or !std.math.isFinite(p[1]) or !std.math.isFinite(p[2])){all=false;break;}}
 for(points,0..)|from,i|{const source=W.EdgeSource.init(.{from[0],from[1],from[2]},.{0.1,-0.2,0.3});for(points,0..)|to,j|{out[i*points.len+j]=if(all)source.rateFiniteTarget(.{to[0],to[1],to[2]}) else source.rate(.{to[0],to[1],to[2]});}}
 return all;
}
test "actual full-batch branch refreshes finite invalid finite without stale flag"{
 var points=[_][3]f32{.{1,2,3},.{-2,3,4},.{0,0,-0.0}};var out:[9]f64=undefined;
 for(0..3)|pass|{points[1][0]=if(pass==1)std.math.nan(f32) else -2;try std.testing.expectEqual(pass!=1,batch(&points,&out));for(points,0..)|from,i|for(points,0..)|to,j|{
 const expected=W.edgeRate(.{from[0],from[1],from[2]},.{to[0],to[1],to[2]},.{0.1,-0.2,0.3});try std.testing.expectEqual(@as(u64,@bitCast(expected)),@as(u64,@bitCast(out[i*3+j])));
 };}
}
