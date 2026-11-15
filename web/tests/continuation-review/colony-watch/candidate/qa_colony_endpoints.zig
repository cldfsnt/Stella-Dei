//! Controlled two-patch actual-scheduler acceptance, not naturally evolved biology.
const std=@import("std");
const P=@import("simulation/planet.zig").Planet;
const M=@import("simulation/microbes.zig");
const V=@import("zalgebra").Vec3;
const W=@import("patch_watch.zig");
test "empty watched target receives actual donor-funded offspring after growth phase" {
 const A=std.testing.allocator;
 var arena=std.heap.ArenaAllocator.init(A);defer arena.deinit();const a=arena.allocator();
 var p:P=undefined;p.allocator=A;p.radius=100;p.seed=42;
 p.vertices=try a.alloc(V,2);@memset(p.vertices,V.new(100,0,0));p.transformedPoints=p.vertices;
 p.verticesNeighbours=try a.alloc([6]u32,2);p.verticesNeighbours[0]=.{1,1,1,1,1,1};p.verticesNeighbours[1]=.{0,0,0,0,0,0};
 p.temperature=try a.alloc(f32,2);@memset(p.temperature,303);p.waterMass=try a.alloc(f32,2);@memset(p.waterMass,0.001/p.getKmPerWaterMass());
 p.microbeCells=try a.alloc(M.Cell,2);@memset(p.microbeCells,.{});p.worldMode=.origin;
 p.microbeStats=.{.next_lineage=2};p.propaguleFeedback=.{};p.propaguleAttempts=0;p.propaguleArrivals=0;p.propaguleTrackedLosses=0;
 p.averageCarbonDioxideMass=10*p.getMeanPointArea()/1e9*(44.0/12.0);p.averageOxygenMass=10*p.getMeanPointArea()/1e9*(32.0/12.0);
 // Explicit test arrangement: assigned donor biomass and credit, not earned progression.
 // The actual scheduler must still debit donor tissue/credit through production APIs.
 p.microbeCells[0].cohorts[0]=.{.biomass=0.1,.reproduction_credit=0.02,.lineage=1};
 var off=p;off.microbeCells=try a.dupe(M.Cell,p.microbeCells);
 defer W.current=.{};
 try std.testing.expect(W.current.start(1,1,0,W.nowMs()));W.current.owner=@intFromPtr(&p);
 try std.testing.expect(W.current.startPopulation(W.Watch.population(p.microbeCells[1].cohorts)));
 const options=P.SimulationOptions{.dt=1,.timeScale=1,.gameTime=0,.solarVector=V.new(1,0,0),.solarConstant=0,.planetRotationTime=86400};
 p.simulateMicrobes(options);const pulse=W.current;
 try std.testing.expect(p.propaguleArrivals==1 and p.microbeStats.births==1);
 try std.testing.expectEqual(@as(f64,0),pulse.start_biomass);try std.testing.expectEqual(@as(u8,0),pulse.start_colonies);
 try std.testing.expectEqual(@as(u8,1),pulse.end_colonies);
 try std.testing.expect(pulse.start_members.valid and pulse.start_members.len==0 and pulse.end_members.valid and pulse.end_members.len==1);try std.testing.expectEqual(p.microbeCells[1].cohorts[0].lineage,pulse.end_members.entries[0].id);try std.testing.expectEqual(@as(f64,p.microbeCells[1].cohorts[0].biomass),pulse.end_biomass);
 try std.testing.expect(pulse.end_biomass>0 and pulse.fixed==0 and pulse.recycled==0 and pulse.consumed==0 and pulse.ticks==1 and pulse.elapsed==1);
 try std.testing.expect(p.microbeCells[0].cohorts[0].biomass<0.0961 and p.microbeCells[0].cohorts[0].reproduction_credit<0.011);
 W.current.stop("test complete");off.simulateMicrobes(options);
 try std.testing.expectEqualDeep(p.microbeCells,off.microbeCells);try std.testing.expectEqualDeep(p.microbeStats,off.microbeStats);try std.testing.expectEqualDeep(p.propaguleFeedback,off.propaguleFeedback);
 try std.testing.expectEqual(p.averageCarbonDioxideMass,off.averageCarbonDioxideMass);try std.testing.expectEqual(p.averageOxygenMass,off.averageOxygenMass);
 std.debug.print("PULSE_CONTROLLED_ARRIVAL start_mass={d} end_mass={d} counts={d}->{d} births={d} actual_scheduler=true donor_paid=true observer_parity=true natural_evolution_claim=false\n",.{pulse.start_biomass,pulse.end_biomass,pulse.start_colonies,pulse.end_colonies,p.microbeStats.births});
}

test "actual scheduler movement endpoints and observer parity without death inference" {
 var moved:usize=0;
 for(1..33)|seed|{for(0..2)|target|{
 const A=std.testing.allocator;
 var arena=std.heap.ArenaAllocator.init(A);defer arena.deinit();const a=arena.allocator();
 var p:P=undefined;p.allocator=A;p.radius=100;p.seed=42;
 p.vertices=try a.alloc(V,2);@memset(p.vertices,V.new(100,0,0));p.transformedPoints=p.vertices;
 p.verticesNeighbours=try a.alloc([6]u32,2);p.verticesNeighbours[0]=.{1,1,1,1,1,1};p.verticesNeighbours[1]=.{0,0,0,0,0,0};
 p.temperature=try a.alloc(f32,2);@memset(p.temperature,303);p.waterMass=try a.alloc(f32,2);@memset(p.waterMass,0.001/p.getKmPerWaterMass());
 p.microbeCells=try a.alloc(M.Cell,2);@memset(p.microbeCells,.{});p.worldMode=.origin;
 p.microbeStats=.{.next_lineage=3};p.propaguleFeedback=.{};p.propaguleAttempts=0;p.propaguleArrivals=0;p.propaguleTrackedLosses=0;
 p.averageCarbonDioxideMass=10*p.getMeanPointArea()/1e9*(44.0/12.0);p.averageOxygenMass=10*p.getMeanPointArea()/1e9*(32.0/12.0);
 // Explicit test arrangement: assigned donor biomass and credit, not earned progression.
 // The actual scheduler must still debit donor tissue/credit through production APIs.
 p.microbeCells[0].rng=seed; p.microbeCells[0].cohorts[0]=.{.biomass=0.1,.lineage=1,.feeding=1,.mobility=1};p.microbeCells[1].cohorts[0]=.{.biomass=0.3,.lineage=2};

 var off=p;off.microbeCells=try a.dupe(M.Cell,p.microbeCells);defer W.current=.{};
 try std.testing.expect(W.current.start(target,1,0,W.nowMs()));W.current.owner=@intFromPtr(&p);
 try std.testing.expect(W.current.startPopulation(W.Watch.population(p.microbeCells[target].cohorts)));
 const options=P.SimulationOptions{.dt=86400,.timeScale=1,.gameTime=0,.solarVector=V.new(1,0,0),.solarConstant=0,.planetRotationTime=86400};
 p.simulateMicrobes(options);const pulse=W.current;
 try std.testing.expectEqualDeep(@import("colony_snapshot.zig").capture(p.microbeCells[target].cohorts),pulse.end_members);
 W.current.stop("test complete");off.simulateMicrobes(options);
 try std.testing.expectEqualDeep(p.microbeCells,off.microbeCells);try std.testing.expectEqualDeep(p.microbeStats,off.microbeStats);try std.testing.expectEqualDeep(p.propaguleFeedback,off.propaguleFeedback);try std.testing.expectEqual(p.averageCarbonDioxideMass,off.averageCarbonDioxideMass);try std.testing.expectEqual(p.averageOxygenMass,off.averageOxygenMass);
 if(p.microbeStats.relocations>0){moved+=1;if(target==0){try std.testing.expectEqual(@as(u8,1),pulse.start_members.len);try std.testing.expectEqual(@as(u8,0),pulse.end_members.len);}else{var found=false;for(pulse.end_members.entries[0..pulse.end_members.len])|entry|{if(entry.id==1)found=true;}try std.testing.expect(found);}}
 }}
 try std.testing.expect(moved>0);std.debug.print("COLONY_MOVEMENT controlled_actual_scheduler=true cases=64 moved={d} endpoints_exact=true observer_parity=true\n",.{moved});
}
