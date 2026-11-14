//! Actual Planet.simulateMicrobes scheduler, controlled topology/climate; no engine edits.
const std=@import("std");const P=@import("simulation/planet.zig").Planet;const M=@import("simulation/microbes.zig");const V=@import("zalgebra").Vec3;
const N=19;const A=std.testing.allocator;
const Fate=struct{birth:usize,seen:usize,peak:f32,birth_mass:f32,offspring:u32=0,moves:u32=0,last_cell:usize,birth_neighbors_full:u32,dead:bool=false,death_age:usize=0};
fn totals(p:*const P)[2]f64{const area=p.getMeanPointArea();var c=p.averageCarbonDioxideMass*1e9*@as(f64,@floatFromInt(N))*12/44/area;var n:f64=0;for(p.microbeCells)|cell|{c+=M.carbon(cell);n+=M.nutrientTotal(cell);}return .{c,n};}
fn run(seed:u64,kind:u8,seconds:usize)!void{
 const ticks_per_day=86400/seconds;
 var p:P=undefined;p.simulationArena=std.heap.ArenaAllocator.init(A);defer p.simulationArena.deinit();const a=p.simulationArena.allocator();p.seed=seed;p.radius=100;
 p.vertices=try a.alloc(V,N);p.transformedPoints=p.vertices;p.verticesNeighbours=try a.alloc([6]u32,N);
 for(0..N)|i|{const t=@as(f32,@floatFromInt(i))*6.283185/@as(f32,N);p.vertices[i]=V.new(100,5*@cos(t),5*@sin(t)).norm().scale(100);p.verticesNeighbours[i]=.{@intCast((i+1)%N),@intCast((i+2)%N),@intCast((i+3)%N),@intCast((i+N-1)%N),@intCast((i+N-2)%N),@intCast((i+N-3)%N)};}
 p.vegetation=try a.alloc(f32,N);@memset(p.vegetation,0);p.temperature=try a.alloc(f32,N);@memset(p.temperature,303);p.waterMass=try a.alloc(f32,N);@memset(p.waterMass,0.001/p.getKmPerWaterMass());
 p.lifeforms=.{};p.worldMode=.sandbox;p.microbeCells=&.{};p.microbeStats=.{};p.propaguleFeedback=.{};p.propaguleAttempts=0;p.propaguleArrivals=0;p.propaguleTrackedLosses=0;
 // Finite shared atmospheric inventory: ten carbon-equivalent units per cell each gas.
 p.averageCarbonDioxideMass=10*p.getMeanPointArea()/1e9*(44.0/12.0);p.averageOxygenMass=10*p.getMeanPointArea()/1e9*(32.0/12.0);
 try p.beginOrigin();for(p.microbeCells)|*c|c.nutrient=0.12;
 const initial=totals(&p);try std.testing.expect(p.seedMicrobes(0));
 var fates=std.AutoHashMap(u64,Fate).init(A);defer fates.deinit();var maxgen:u32=0;var eligible_credit:u64=0;var eligible_full_edges:u64=0;var eligible_edges:u64=0;
 for(0..180*ticks_per_day)|tick|{
  const day=tick/ticks_per_day;
  if(tick==60*ticks_per_day and kind==1){for(p.microbeCells,0..)|*cell,i|{if(i%3!=0)continue;for(&cell.cohorts)|*co|{cell.detritus+=co.biomass;cell.nutrient+=co.biomass*M.nutrient_per_carbon;co.*=.{};}}}
  @memset(p.waterMass,(if(kind==2 and day>=60 and day<63)@as(f32,0.00008) else @as(f32,0.001))/p.getKmPerWaterMass());
  if(kind==3)for(0..N)|i|{if(i%3==2){p.waterMass[i]=0.00008/p.getKmPerWaterMass();p.temperature[i]=293;}};
  const prior=p.microbeStats.next_lineage;
  if(day>=30)for(p.microbeCells,0..)|cell,i|{for(cell.cohorts)|co|{if(co.biomass>=0.02 and co.reproduction_credit>=0.01){eligible_credit+=1;for(p.getNeighbours(i))|j|{eligible_edges+=1;var full=true;for(p.microbeCells[j].cohorts)|v|{if(v.biomass==0)full=false;}if(full)eligible_full_edges+=1;}}}};
  p.simulateMicrobes(.{.dt=@floatFromInt(seconds),.timeScale=1,.gameTime=@as(f64,@floatFromInt(tick*seconds)),.solarVector=V.new(1,0,0),.solarConstant=if(tick%ticks_per_day<ticks_per_day/2)1361 else 0,.planetRotationTime=86400});
  for(p.microbeCells,0..)|cell,i|{try std.testing.expect(M.validCell(cell,p.microbeStats.next_lineage));for(cell.cohorts)|co|{
   if(co.biomass<=0)continue;maxgen=@max(maxgen,co.generation);
   if(co.lineage>=prior and day>=30){var full:u32=0;for(p.getNeighbours(i))|j|{var count:u32=0;for(p.microbeCells[j].cohorts)|v|{if(v.biomass>0)count+=1;}if(count==4)full+=1;}
    try fates.put(co.lineage,.{.birth=tick,.seen=tick,.peak=co.biomass,.birth_mass=co.biomass,.last_cell=i,.birth_neighbors_full=full});
   }
   if(fates.getPtr(co.lineage))|f|{try std.testing.expect(!f.dead);f.seen=tick;f.peak=@max(f.peak,co.biomass);if(f.last_cell!=i)f.moves+=1;f.last_cell=i;}
  }}
  // Second pass handles parents independently of cell order; relocation preserves ID.
  if(day>=30)for(p.microbeCells)|cell|{for(cell.cohorts)|co|{if(co.biomass>0 and co.lineage>=prior)if(fates.getPtr(co.parent))|f|{f.offspring+=1;};}};
  var it=fates.valueIterator();while(it.next())|f|{if(!f.dead and f.seen!=tick){f.dead=true;f.death_age=tick-f.birth;}}
  const current=totals(&p);try std.testing.expectApproxEqAbs(initial[0],current[0],0.001);try std.testing.expectApproxEqAbs(initial[1],current[1],0.001);
  try std.testing.expect(p.averageCarbonDioxideMass>=0 and p.averageOxygenMass>=0);
  if((tick+1)%ticks_per_day==0 and (day+1==30 or day+1==60 or day+1==63 or day+1==100 or day+1==180)){
   var dead:usize=0;var quick:usize=0;var established:usize=0;var parents:usize=0;var moves:usize=0;var full_birth:usize=0;var massive:u32=0;
   it=fates.valueIterator();while(it.next())|f|{if(f.dead){dead+=1;if(f.death_age<=ticks_per_day)quick+=1;}if(f.peak>=0.02)established+=1;if(f.offspring>0)parents+=1;moves+=f.moves;if(f.birth_neighbors_full==6)full_birth+=1;if(f.birth_mass>0.006)massive+=1;}
   var mass:f64=0;var cohorts:usize=0;var occupied:usize=0;var full:usize=0;for(p.microbeCells)|cell|{var count:usize=0;mass+=M.biomass(cell);for(cell.cohorts)|co|{if(co.biomass>0)count+=1;}cohorts+=count;if(count>0)occupied+=1;if(count==4)full+=1;}
   std.debug.print("PLANET seed={d} dt={d} treatment={d} day={d} biomass={d:.6} occupied={d} cohorts={d} full_cells={d} births={d} maxgen={d} tracked_post30={d} deaths={d} dead_within1day={d} peak_ge002={d} became_parent={d} observed_moves={d} full_neighbors_at_birth={d} larger_births={d} eligible_parent_samples={d} full_edges={d}/{d} grazed_per_area={d:.6} carbon_error={e} nutrient_error={e}\n",.{seed,seconds,kind,day+1,mass,occupied,cohorts,full,p.microbeStats.births,maxgen,fates.count(),dead,quick,established,parents,moves,full_birth,massive,eligible_credit,eligible_full_edges,eligible_edges,p.microbeStats.grazed_carbon/p.getMeanPointArea(),current[0]-initial[0],current[1]-initial[1]});
  }
 }
}
test "actual Planet daughter establishment after day30"{for([_]u64{42,1337,2027})|seed|for(0..3)|kind|try run(seed,@intCast(kind),1440);try run(42,0,720);try run(42,3,1440);}
