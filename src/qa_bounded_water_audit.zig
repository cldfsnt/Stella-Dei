const std=@import("std");const B=@import("experimental/bounded_water.zig");
fn perm(k:usize)[4]usize{var a=[_]usize{0,1,2,3};var out:[4]usize=undefined;var n:usize=4;var r=k;for(0..4)|i|{const j=r%n;r/=n;out[i]=a[j];for(j..n-1)|t|a[t]=a[t+1];n-=1;}return out;}
pub fn main()!void{
 var rng=std.Random.DefaultPrng.init(77003);const r=rng.random();const out=std.io.getStdOut().writer();var nonzero:usize=0;
 for(0..3000)|k|{const scale=std.math.pow(f64,2,@as(f64,@floatFromInt(k%2001))-1000);const source=scale*(1+r.float(f64)*7);const target=if(k%5==0)0 else scale*r.float(f64)*8;var sources:[4]f64=undefined;var wanted:[4]f64=undefined;for(0..4)|i|{sources[i]=scale*(r.float(f64)*8);wanted[i]=scale*r.float(f64)*8;}const s=B.scatter(source,target,wanted);const g=B.gather(sources,target,wanted);if(s.source<source or g.target>target)nonzero+=1;
 try std.json.stringify(.{.source=source,.sources=sources,.target=target,.wanted=wanted,.scatter=s,.gather=g},.{},out);try out.writeByte('\n');
 for(0..24)|j|{const o=perm(j);var ps:[4]f64=undefined;var pw:[4]f64=undefined;for(0..4)|i|{ps[i]=sources[o[i]];pw[i]=wanted[o[i]];}const a=B.scatter(source,target,pw);const b=B.gather(ps,target,pw);try std.testing.expectEqual(s.source,a.source);try std.testing.expectEqual(s.target,a.target);try std.testing.expectEqual(g.target,b.target);for(0..4)|i|{try std.testing.expectEqual(s.paid[o[i]],a.paid[i]);try std.testing.expectEqual(g.paid[o[i]],b.paid[i]);try std.testing.expectEqual(g.sources[o[i]],b.sources[i]);}}
 }
 const base=B.gather(.{1,0,0,0},0,.{1,0,0,0});const blocked=B.gather(.{1,1e100,0,0},0,.{1,0,0,0});try std.testing.expectEqual(base.paid[0],blocked.paid[0]);std.debug.print("inactive-source witness base={d}, with-unused-huge={d}; cases3000 permutations72000 nonzero={d}\n",.{base.paid[0],blocked.paid[0],nonzero});
}
