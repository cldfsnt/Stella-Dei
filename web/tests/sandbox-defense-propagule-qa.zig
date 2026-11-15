const std=@import("std");const P=@import("simulation/planet.zig").Planet;const E=@import("simulation/ecology.zig");const V=@import("zalgebra").Vec3;
test "defended offspring require positive represented cover addition"{
 for([_]f32{0,1,std.math.nextAfter(f32,1,0),0.5})|d|for([_]f32{0,std.math.floatTrueMin(f32),0.000000001,1440})|dt|for([_]f32{0,0.3})|initial|{
  var arena=std.heap.ArenaAllocator.init(std.testing.allocator);defer arena.deinit();const a=arena.allocator();var p:P=undefined;p.radius=100;p.seed=42;p.sandboxDefense=.{.enabled=true,.law=1,.mutation_law=2,.stream_seed=0};
  p.vertices=try a.alloc(V,7);@memset(p.vertices,V.new(100,0,0));p.transformedPoints=p.vertices;p.verticesNeighbours=try a.alloc([6]u32,7);@memset(p.verticesNeighbours,[_]u32{1}**6);
  p.vegetation=try a.alloc(f32,7);@memset(p.vegetation,0);p.vegetation[0]=initial;p.vegetation[1]=0.35;p.vegetationSnapshot=try a.alloc(f32,7);p.plantTraits=try a.alloc(E.Plant,7);@memset(p.plantTraits,.{.optimum=295.15});p.plantTraits[0].optimum=260;p.plantTraits[1].toughness=d;
  p.temperature=try a.alloc(f32,7);@memset(p.temperature,295.15);p.waterMass=try a.alloc(f32,7);@memset(p.waterMass,0);p.averageCarbonDioxideMass=100;p.averageOxygenMass=100;p.plantBirths=0;p.plantGenerations=0;
  const before=p.plantTraits[0];const grown=E.growTough(initial,295.15,260,0,1,true,dt,0);const gift=@min(@as(f32,0.08),dt/86400*@as(f32,0.35))*(1-d);const representable=d<1 and std.math.isFinite(gift) and gift>0 and grown+gift>grown;
  p.simulateVegetation(.{.dt=dt,.timeScale=1,.gameTime=0,.solarVector=V.new(1,0,0),.solarConstant=1361,.planetRotationTime=86400},0,1);
  std.debug.print("DEFENSE_PROP d={d} dt={d} initial={d} grown={d} gift={d} birth={} expected={}\n",.{d,dt,initial,grown,gift,p.plantBirths,representable});
  try std.testing.expectEqual(@as(u64,if(representable)1 else 0),p.plantBirths);
  if(!representable){try std.testing.expectEqualDeep(before,p.plantTraits[0]);try std.testing.expectEqual(grown,p.vegetation[0]);}
  };
}
