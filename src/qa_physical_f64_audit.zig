const std=@import("std");const B=@import("experimental/physical_water_f64.zig");const K=@import("experimental/soil_root_kernel_f64.zig");
fn perm(k:usize)[4]usize{var a=[_]usize{0,1,2,3};var o:[4]usize=undefined;var n:usize=4;var r=k;for(0..4)|i|{const j=r%n;r/=n;o[i]=a[j];for(j..n-1)|t|a[t]=a[t+1];n-=1;}return o;}
pub fn main()!void{var rng=std.Random.DefaultPrng.init(973912);const random=rng.random();const output=std.io.getStdOut().writer();var accepted:usize=0;
 for(0..2000)|n|{const scale=std.math.pow(f64,2,@as(f64,@floatFromInt(n%401))-200);var s=K.State{.surface=scale*(1+random.float(f64)),.soil=scale*random.float(f64),.vapor=if(n%3==0)250 else scale*random.float(f64)};var p=K.Params{.dt=1,.capacity=scale*2,.infiltration_rate=scale*random.float(f64)/8,.evaporation_rate=scale*random.float(f64)/16,.drainage_rate=scale*random.float(f64)/16,.conductance=1};for(0..4)|i|{s.cohorts[i]=.{.biomass=scale,.support=scale/2,.root_fraction=0.25,.storage_fraction=0.25,.water=scale*random.float(f64)/4};p.demand[i]=scale*random.float(f64)/4;p.exposure[i]=1;}
 const result=K.step(s,p) orelse continue;accepted+=1;const r=result.result;
 // Replay only physical prefix to expose true intermediate endpoints to oracle.
 var surface=s.surface;var soil=s.soil;var vapor=s.vapor;var ledger=B.Ledger{};
 _=B.transfer(&surface,&soil,@min(B.downDifference(p.capacity,soil),p.infiltration_rate),&ledger).?;const a=.{surface,soil,vapor};
 _=B.transfer(&soil,&vapor,p.evaporation_rate,&ledger).?;const b=.{surface,soil,vapor};
 var wanted:[4]f64=undefined;for(0..4)|i|wanted[i]=@min(p.demand[i],B.downProduct(B.downProduct(B.downProduct(r.root_carbon[i],p.conductance),soil/p.capacity),p.dt));
 _=B.transfer(&soil,&vapor,B.lowerSum(wanted),&ledger).?;const c=.{surface,soil,vapor};
 var h32:[4]f32=undefined;for(0..4)|i|h32[i]=B.signal32(B.lowerSum(.{r.root_receipts[i],r.store_receipts[i],0,0}),p.demand[i]);
 try std.json.stringify(.{.before=s,.params=p,.result=result,.after_infiltration=a,.after_evaporation=b,.after_roots=c,.h32=h32},.{},output);try output.writeByte('\n');
 for(0..24)|j|{const order=perm(j);var ss=s;var pp=p;for(0..4)|i|{ss.cohorts[i]=s.cohorts[order[i]];pp.demand[i]=p.demand[order[i]];pp.exposure[i]=p.exposure[order[i]];}const other=K.step(ss,pp).?;try std.testing.expectEqual(r.state.surface,other.result.state.surface);try std.testing.expectEqual(r.state.soil,other.result.state.soil);try std.testing.expectEqual(r.state.vapor,other.result.state.vapor);try std.testing.expectEqualDeep(result.ledger,other.ledger);try std.testing.expectEqual(result.allocation_deficit,other.allocation_deficit);for(0..4)|i|{try std.testing.expectEqual(r.root_receipts[order[i]],other.result.root_receipts[i]);try std.testing.expectEqual(r.store_receipts[order[i]],other.result.store_receipts[i]);}}
 }
 var source:f64=1;var target:f64=std.math.floatMax(f64);var ledger=B.Ledger{};try std.testing.expect(B.transfer(&source,&target,1,&ledger)==null);try std.testing.expectEqual(@as(f64,1),source);try std.testing.expectEqual(std.math.floatMax(f64),target);try std.testing.expectEqualDeep(B.Ledger{},ledger);
 for([_]f64{-1,std.math.inf(f64),std.math.nan(f64)})|bad|{source=1;target=0;ledger=.{};try std.testing.expect(B.transfer(&source,&target,bad,&ledger)==null);try std.testing.expectEqual(@as(f64,1),source);try std.testing.expectEqual(@as(f64,0),target);try std.testing.expectEqualDeep(B.Ledger{},ledger);}
 try std.testing.expect(!std.math.isFinite(B.downProduct(std.math.floatMax(f64),2)));
 std.debug.print("2000 full-kernel probes accepted={d}; 24permutations each; invalid/overflow scalar atomic gates passed\n",.{accepted});
}
