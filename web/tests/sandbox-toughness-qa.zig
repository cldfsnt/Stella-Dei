const std=@import("std");const P=@import("simulation/planet.zig").Planet;const L=@import("simulation/life.zig");const E=@import("simulation/ecology.zig");const F=@import("simulation/foraging.zig");const V=@import("zalgebra").Vec3;
const candidate=@hasField(E.Plant,"toughness");
fn trait(d:f32)E.Plant{var p=E.Plant{.optimum=295.1499938964844};if(comptime candidate)p.toughness=d;return p;}
test "fixed actual local plant rabbit matrix"{
 for([_]f32{1440,720,360})|dt|for([_]usize{0,2})|stock|for([_]f32{0,0.5})|d|{
  if(!candidate and d!=0)continue;
  var arena=std.heap.ArenaAllocator.init(std.testing.allocator);defer arena.deinit();const a=arena.allocator();var p:P=undefined;p.allocator=a;p.simulationArena=arena;p.radius=100;p.seed=1337;
  p.vertices=try a.alloc(V,7);p.transformedPoints=p.vertices;p.verticesNeighbours=try a.alloc([6]u32,7);
  for(0..7)|i|{p.vertices[i]=V.new(100,@as(f32,@floatFromInt(i))*3,0).norm().scale(100);var k:usize=0;for(0..7)|j|if(j!=i){p.verticesNeighbours[i][k]=@intCast(j);k+=1;};}
  p.vegetation=try a.alloc(f32,7);p.vegetationSnapshot=try a.alloc(f32,7);p.plantTraits=try a.alloc(E.Plant,7);p.temperature=try a.alloc(f32,7);p.waterMass=try a.alloc(f32,7);
  @memset(p.vegetation,0);p.vegetation[0]=0.35;@memset(p.plantTraits,trait(d));@memset(p.temperature,297.9569091796875);@memset(p.waterMass,0);
  p.averageCarbonDioxideMass=100;p.averageOxygenMass=100;p.plantGenerations=0;p.plantBirths=0;p.rabbitBirths=0;p.rabbitMeals=0;p.rabbitDeaths=0;
  p.lifeforms=try std.ArrayListUnmanaged(L.Lifeform).initCapacity(a,1024);
  for(0..stock)|i|{var rabbit=L.Lifeform.init(p.vertices[0],.Rabbit,0);rabbit.genome.gender=if(i==0).Female else .Male;rabbit.prng=std.rand.DefaultPrng.init(1337000+i);p.lifeforms.appendAssumeCapacity(rabbit);}
  L.qa_removed=0;L.qa_credit=0;L.qa_error=0;var time:f64=0;var peak=stock;var extinctions:usize=0;var recolonizations:usize=0;var prev:[7]f32=undefined;@memcpy(&prev,p.vegetation);
  for(0..14)|day|{
   for(0..@as(usize,@intFromFloat(86400/dt)))|_|{
    const opt=P.SimulationOptions{.dt=dt,.timeScale=1,.gameTime=time,.solarVector=V.new(1,0,0),.solarConstant=1361,.planetRotationTime=86400};var remaining=p.lifeforms.items.len;while(remaining>0){remaining-=1;p.lifeforms.items[remaining].aiStep(&p,opt);}p.simulateVegetation(opt,0,7);time+=dt;peak=@max(peak,p.lifeforms.items.len);
    try std.testing.expectEqual(stock+p.rabbitBirths-p.rabbitDeaths,p.lifeforms.items.len);
    for(p.vegetation,0..)|v,i|{try std.testing.expect(std.math.isFinite(v) and v>=0 and v<=1);if(prev[i]>0 and v==0)extinctions+=1;if(prev[i]==0 and v>0)recolonizations+=1;prev[i]=v;if(comptime candidate)try std.testing.expectEqual(d,p.plantTraits[i].toughness);}
   }
   var cover:f64=0;var occupied:usize=0;var low:usize=0;for(p.vegetation)|v|{cover+=v;if(v>0)occupied+=1;if(v>0 and v<0.01)low+=1;}
   std.debug.print("TOUGH_DAY {s}\n",.{try std.json.stringifyAlloc(a,.{.dt=dt,.stock=stock,.d=d,.day=day+1,.cover=cover,.occupied=occupied,.low=low,.extinctions=extinctions,.zero_to_positive=recolonizations,.rabbits=p.lifeforms.items.len,.peak=peak,.births=p.rabbitBirths,.deaths=p.rabbitDeaths,.meals=p.rabbitMeals,.plant_births=p.plantBirths,.plant_generation=p.plantGenerations,.removed=L.qa_removed,.satiety_credit=L.qa_credit,.credit_error_abs=L.qa_error,.co2=p.averageCarbonDioxideMass,.oxygen=p.averageOxygenMass},.{})});
  }
  const old_plants=try a.alloc(struct{optimum:f32,generation:u32},7);for(p.plantTraits,old_plants)|c,*o|o.*=.{.optimum=c.optimum,.generation=c.generation};
  std.debug.print("TOUGH_ENDPOINT {s}\n",.{try std.json.stringifyAlloc(a,.{.dt=dt,.stock=stock,.d=d,.vegetation=p.vegetation,.plants=old_plants,.rabbits=p.lifeforms.items,.births=p.rabbitBirths,.deaths=p.rabbitDeaths,.plant_births=p.plantBirths,.plant_generation=p.plantGenerations,.co2=p.averageCarbonDioxideMass,.oxygen=p.averageOxygenMass},.{})});
 };
}
test "zero trait parity, inherited fixed trait and finite defense never creates a floor"{
 if(comptime candidate){
  for([_]f32{0,0.00005,0.1,0.35,1})|cover|for([_]f32{360,720,1440,86400})|dt|{
   try std.testing.expectEqualDeep(F.take(cover,50,dt),F.takeTough(cover,50,dt,0));
   try std.testing.expectEqual(E.grow(cover,298,295,0,1,true,dt),E.growTough(cover,298,295,0,1,true,dt,0));
   const bite=F.takeTough(cover,50,dt,0.5);try std.testing.expect(bite.eaten<=bite.budget);try std.testing.expectEqual(@as(f64,cover)-bite.after,bite.eaten);
  };
  var cover:f32=0.01;for(0..840)|_|cover=F.takeTough(cover,0,1440,0.5).after;try std.testing.expectEqual(@as(f32,0),cover);
  try std.testing.expect(F.takeTough(0.00005,50,0.001,0.5).after>0);try std.testing.expectEqual(@as(f32,0),E.growTough(0,298,295,0,1,true,86400,0.5));
  try std.testing.expectEqual(E.grow(0.35,400,295,0,1,true,86400),E.growTough(0.35,400,295,0,1,true,86400,0.5));
  for(0..128)|seed|{const plain=E.offspring(trait(0),seed);const hard=E.offspring(trait(0.5),seed);try std.testing.expectEqual(plain.optimum,hard.optimum);try std.testing.expectEqual(plain.generation,hard.generation);try std.testing.expectEqual(@as(f32,0.5),hard.toughness);}
 }
}
