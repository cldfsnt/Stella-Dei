//! Actual Planet.simulateMicrobes scheduler, controlled topology/climate; no engine edits.
const std=@import("std");const P=@import("simulation/planet.zig").Planet;const M=@import("simulation/microbes.zig");const V=@import("zalgebra").Vec3;
const N=19;const A=std.testing.allocator;
const Fate=struct{birth:usize,seen:usize,peak:f32,birth_mass:f32,offspring:u32=0,moves:u32=0,last_cell:usize,birth_neighbors_full:u32,dead:bool=false,death_age:usize=0};
fn totals(p:*const P)[2]f64{const area=p.getMeanPointArea();var c=p.averageCarbonDioxideMass*1e9*@as(f64,@floatFromInt(N))*12/44/area;var n:f64=0;for(p.microbeCells)|cell|{c+=M.carbon(cell);n+=M.nutrientTotal(cell);}return .{c,n};}
fn run(seed:u64,kind:u8,seconds:usize,force_oom:bool)!void{
 const ticks_per_day=86400/seconds;
 var p:P=undefined;p.simulationArena=std.heap.ArenaAllocator.init(A);defer p.simulationArena.deinit();const a=p.simulationArena.allocator();p.allocator=A;p.seed=seed;p.radius=100;
 p.vertices=try a.alloc(V,N);p.transformedPoints=p.vertices;p.verticesNeighbours=try a.alloc([6]u32,N);
 for(0..N)|i|{const t=@as(f32,@floatFromInt(i))*6.283185/@as(f32,N);p.vertices[i]=V.new(100,5*@cos(t),5*@sin(t)).norm().scale(100);p.verticesNeighbours[i]=.{@intCast((i+1)%N),@intCast((i+2)%N),@intCast((i+3)%N),@intCast((i+N-1)%N),@intCast((i+N-2)%N),@intCast((i+N-3)%N)};}
 p.vegetation=try a.alloc(f32,N);@memset(p.vegetation,0);p.temperature=try a.alloc(f32,N);@memset(p.temperature,303);p.waterMass=try a.alloc(f32,N);@memset(p.waterMass,0.001/p.getKmPerWaterMass());
 p.lifeforms=.{};p.worldMode=.sandbox;p.microbeCells=&.{};p.microbeStats=.{};p.propaguleFeedback=.{};p.propaguleAttempts=0;p.propaguleArrivals=0;p.propaguleTrackedLosses=0;
 // Finite shared atmospheric inventory: ten carbon-equivalent units per cell each gas.
 p.averageCarbonDioxideMass=10*p.getMeanPointArea()/1e9*(44.0/12.0);p.averageOxygenMass=10*p.getMeanPointArea()/1e9*(32.0/12.0);
 try p.beginOrigin();for(p.microbeCells)|*c|c.nutrient=0.12;
 const initial=totals(&p);try std.testing.expect(p.seedMicrobes(0));
 var other=p;other.microbeCells=try a.dupe(M.Cell,p.microbeCells);
 var failing=std.testing.FailingAllocator.init(A,.{.fail_index=0});if(force_oom)other.allocator=failing.allocator();
 const qa=@import("qa_micro_metrics.zig");
 for(0..180*ticks_per_day)|tick|{
  for(0..N)|i|{p.waterMass[i]=(if(kind==3 and i%3==2)@as(f32,0.00008)else @as(f32,0.001))/p.getKmPerWaterMass();}
  const options=P.SimulationOptions{.dt=@floatFromInt(seconds),.timeScale=1,.gameTime=@as(f64,@floatFromInt(tick*seconds)),.solarVector=V.new(1,0,0),.solarConstant=if(tick%ticks_per_day<ticks_per_day/2)1361 else 0,.planetRotationTime=86400};
  qa.candidate=false;p.simulateMicrobes(options);qa.candidate=true;other.simulateMicrobes(options);
  try std.testing.expectEqualDeep(p.microbeCells,other.microbeCells);try std.testing.expectEqualDeep(p.microbeStats,other.microbeStats);try std.testing.expectEqualDeep(p.propaguleFeedback,other.propaguleFeedback);
  try std.testing.expectEqual(p.averageCarbonDioxideMass,other.averageCarbonDioxideMass);try std.testing.expectEqual(p.averageOxygenMass,other.averageOxygenMass);
  try std.testing.expectEqual(p.propaguleAttempts,other.propaguleAttempts);try std.testing.expectEqual(p.propaguleArrivals,other.propaguleArrivals);try std.testing.expectEqual(p.propaguleTrackedLosses,other.propaguleTrackedLosses);
  const current=totals(&p);try std.testing.expectApproxEqAbs(initial[0],current[0],0.001);try std.testing.expectApproxEqAbs(initial[1],current[1],0.001);
 }
 if(force_oom)try std.testing.expect(failing.has_induced_failure);
 std.debug.print("ACTIVE_PARITY oom={} seed={d} habitat={d} ticks={d} births={d} moves={d} arrivals={d} exact_each_tick=true\n",.{force_oom,seed,kind,180*ticks_per_day,p.microbeStats.births,p.microbeStats.relocations,p.propaguleArrivals});
}
test "activity index preserves actual inherited descendants and all runtime cell state"{for([_]u64{42,1337,2027})|seed|for([_]u8{0,3})|kind|try run(seed,kind,1440,false);try run(42,0,1440,true);}
