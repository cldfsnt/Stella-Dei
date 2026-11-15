const std=@import("std");const Q=@import("experimental/near_quantum.zig");
fn permutation(k:usize)[4]usize{var left=[_]usize{0,1,2,3};var out:[4]usize=undefined;var n:usize=4;var r=k;for(0..4)|i|{const idx=r%n;r/=n;out[i]=left[idx];for(idx..n-1)|j|left[j]=left[j+1];n-=1;}return out;}
test "independent staged receipts across scales and all slot permutations" {
 var rng=std.Random.DefaultPrng.init(9237401);const random=rng.random();var accepted:usize=0;var refused:usize=0;
 for(0..10000)|iteration|{
  const exponent:i32=@as(i32,@intCast(iteration%241))-120;
  const pool:f32=@floatCast(std.math.pow(f64,2,@floatFromInt(exponent))*(1+random.float(f64)));
  const conversion=std.math.pow(f64,10,@as(f64,@floatFromInt(iteration%61))-30);
  const q=(@as(f64,pool)-std.math.nextAfter(f32,pool,0))*conversion;
  var stores:[4]f64=undefined;var caps:[4]f64=undefined;
  for(0..4)|i|{stores[i]=q*random.float(f64)*8;caps[i]=stores[i]+q*(0.02+random.float(f64)*0.3);}
  const reference=Q.plan(pool,conversion,stores,caps);
  if(reference)|p|{accepted+=1;var actual:f128=0;var deficit:f128=0;for(0..4)|i|{try std.testing.expect(p.stores[i]>=stores[i] and p.stores[i]<=caps[i]);actual+=@as(f128,p.stores[i])-stores[i];deficit+=@as(f128,caps[i])-stores[i];}const debit=(@as(f128,pool)-p.pool)*@as(f128,conversion);const excess=@as(f128,p.debit)-actual;try std.testing.expect(excess>=0 and excess<=actual and excess<=deficit);const tol=@max(@as(f128,1e-300),@abs(debit)*4*std.math.floatEps(f64));try std.testing.expect(@abs(debit-actual-@as(f128,p.remainder))<=tol);try std.testing.expect(p.pool==std.math.nextAfter(f32,pool,0));}else{refused+=1;}
  for(0..24)|k|{const order=permutation(k);var ss:[4]f64=undefined;var cc:[4]f64=undefined;for(0..4)|i|{ss[i]=stores[order[i]];cc[i]=caps[order[i]];}const candidate=Q.plan(pool,conversion,ss,cc);try std.testing.expect((reference==null)==(candidate==null));if(reference)|p|{const c=candidate.?;try std.testing.expectEqual(p.pool,c.pool);try std.testing.expectEqual(p.debit,c.debit);try std.testing.expectEqual(p.remainder,c.remainder);for(0..4)|i|try std.testing.expectEqual(p.stores[order[i]],c.stores[i]);}}
 }
 std.debug.print("independent: 10000 scale cases, 240000 permutations, accepted={d}, refused={d}\n",.{accepted,refused});try std.testing.expect(accepted>0 and refused>0);
}
test "independent zero ordinary and extreme refusals" {
 const zero=[_]f64{0,0,0,0};const ordinary=[_]f64{1,0,0,0};
 try std.testing.expect(Q.plan(1,1,zero,zero)==null);try std.testing.expect(Q.plan(0,1,zero,ordinary)==null);try std.testing.expect(Q.plan(1,1,zero,ordinary)==null);
 try std.testing.expect(Q.plan(std.math.inf(f32),1,zero,ordinary)==null);try std.testing.expect(Q.plan(1,std.math.inf(f64),zero,ordinary)==null);
 try std.testing.expect(Q.plan(std.math.floatMax(f32),std.math.floatMax(f64),zero,ordinary)==null);
 try std.testing.expect(Q.plan(1,1,ordinary,zero)==null);
 const tiny=[_]f64{1e-100,0,0,0};try std.testing.expect(Q.plan(1,1,zero,tiny)==null);
}
test "roundoff witnesses remain explicit and escrow merge is not validated by Plan" {
 var rng=std.Random.DefaultPrng.init(33123);const random=rng.random();var upward:usize=0;var downward:usize=0;var merge_loss:usize=0;var witness=false;
 for(0..10000)|_|{
  const pool:f32=@floatCast(1+random.float(f64));const conv=0.1+random.float(f64);const q=(@as(f64,pool)-std.math.nextAfter(f32,pool,0))*conv;
  var ss:[4]f64=undefined;var cc:[4]f64=undefined;for(0..4)|i|{ss[i]=q*random.float(f64);cc[i]=ss[i]+q*(0.1+0.15*random.float(f64));}
  if(Q.plan(pool,conv,ss,cc))|p|{var received:f128=0;for(0..4)|i|received+=@as(f128,p.stores[i])-ss[i];const exact=@as(f128,p.debit)-received;const delta=@as(f128,p.remainder)-exact;if(delta>0)upward+=1 else if(delta<0)downward+=1;
   const old_escrow:f64=1;const new_escrow=old_escrow+p.remainder;const actual_escrow=@as(f128,new_escrow)-old_escrow;const merge_delta=actual_escrow-exact;if(merge_delta<0)merge_loss+=1;
   if(!witness and delta>0 and merge_delta!=0){std.debug.print("witness pool={d} conversion={d} debit={d} remainder={d} cast_error={e} existing_escrow=1 merge_error={e}\n",.{pool,conv,p.debit,p.remainder,delta,merge_delta});witness=true;}
  }
 }
 std.debug.print("roundoff: upward={d}, downward={d}, lossy merges={d}\n",.{upward,downward,merge_loss});try std.testing.expect(upward>0 and downward>0 and merge_loss>0 and witness);
}
