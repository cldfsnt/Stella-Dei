const std=@import("std");const Q=@import("experimental/near_quantum.zig");
fn perm(k:usize)[4]usize{var a=[_]usize{0,1,2,3};var out:[4]usize=undefined;var n:usize=4;var r=k;for(0..4)|i|{const j=r%n;r/=n;out[i]=a[j];for(j..n-1)|t|a[t]=a[t+1];n-=1;}return out;}
pub fn main() !void {
 const zero=[_]f64{0,0,0,0};try std.testing.expect(Q.plan(1,1,zero,.{3*0x1p-26,0x1p-200,0,0})==null);
 var rng=std.Random.DefaultPrng.init(574893);const random=rng.random();const out=std.io.getStdOut().writer();var count:usize=0;
 for(0..6000)|k|{const source:f32=@floatCast(std.math.pow(f64,2,@as(f64,@floatFromInt(k%241))-120)*(1+random.float(f64)));const conv=std.math.pow(f64,10,@as(f64,@floatFromInt(k%81))-40);const q=(@as(f64,source)-std.math.nextAfter(f32,source,0))*conv;var ss:[4]f64=undefined;var cc:[4]f64=undefined;for(0..4)|i|{ss[i]=q*random.float(f64);cc[i]=ss[i]+q*(0.1+0.15*random.float(f64));}const before=if(k%2==0)@as(f64,0) else q*random.float(f64);const reference=Q.plan(source,conv,ss,cc);const merged=if(reference)|p|Q.mergeEscrow(p,before,ss,source,conv) else null;
 for(0..24)|j|{const order=perm(j);var s:[4]f64=undefined;var c:[4]f64=undefined;for(0..4)|i|{s[i]=ss[order[i]];c[i]=cc[order[i]];}const plan=Q.plan(source,conv,s,c);try std.testing.expect((plan==null)==(reference==null));if(plan)|p|{const m=Q.mergeEscrow(p,before,s,source,conv);try std.testing.expect((m==null)==(merged==null));if(m)|after|{try std.testing.expectEqual(merged.?,after);for(0..4)|i|try std.testing.expectEqual(reference.?.stores[order[i]],p.stores[i]);}}}
 if(merged)|after|{count+=1;try std.json.stringify(.{.source=source,.pool=reference.?.pool,.conversion=conv,.before=before,.after=after,.stores=ss,.caps=cc,.receivers=reference.?.stores},.{},out);try out.writeByte('\n');}
 }
 std.debug.print("6000 cases x24 permutations; exact ledger rows={d}; mixed-scale witness refused\n",.{count});try std.testing.expect(count>0);
}
