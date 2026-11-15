//! Actual production aiStep feeding checks; mock one-patch physical environment only.
const std=@import("std");const za=@import("zalgebra");const Life=@import("simulation/life.zig").Lifeform;const F=@import("simulation/foraging.zig");
const World=struct{
 vegetation:[1]f32=.{0.02},temperature:[1]f32=.{295.15},waterMass:[1]f32=.{0},transformedPoints:[1]za.Vec3=.{za.Vec3.new(100,0,0)},lifeforms:std.ArrayListUnmanaged(Life)=.{},rabbitMeals:u64=0,rabbitBirths:u64=0,rabbitDeaths:u64=0,
 pub fn getNearestPointTo(_: *@This(),_:za.Vec3)usize{return 0;}
 pub fn getNeighbours(_: *@This(),_:usize)[]const usize{return &.{};}
 pub fn getKmPerWaterMass(_: *@This())f32{return 1;}
 pub fn addLifeformDuringStep(self:*@This(),child:Life)void{self.lifeforms.appendAssumeCapacity(child);}
};
test "production aiStep uses finite actual-debit feeding and preserves nonfeeding state" {
 for([_]f32{0,0.001,360,720,1440,86400})|dt|{
  var w=World{};defer w.lifeforms.deinit(std.testing.allocator);try w.lifeforms.ensureTotalCapacity(std.testing.allocator,4);
  var rabbit=Life.init(w.transformedPoints[0],.Rabbit,0);rabbit.satiety=84;rabbit.prng=std.rand.DefaultPrng.init(42);rabbit.genome.gender=.Female;w.lifeforms.appendAssumeCapacity(rabbit);
  const hungry=@as(f32,84)-dt*0.00025;const bite=F.take(0.02,hungry,dt);
  w.lifeforms.items[0].aiStep(&w,.{.dt=dt,.timeScale=@as(f32,1),.gameTime=@as(f64,0)});
  try std.testing.expectEqual(bite.after,w.vegetation[0]);try std.testing.expectEqual(F.fedSatiety(hungry,bite.eaten),w.lifeforms.items[0].satiety);
  try std.testing.expectEqual(@as(u64,@intFromBool(bite.eaten>0)),w.rabbitMeals);try std.testing.expectEqual(@as(u64,0),w.rabbitBirths);
  try std.testing.expectEqual(rabbit.prng,w.lifeforms.items[0].prng);
 }
}
test "production final fragment can disappear but tiny elapsed time cannot take it" {
 for([_]f32{0.001,1440})|dt|{
  var w=World{.vegetation=.{0.00005}};defer w.lifeforms.deinit(std.testing.allocator);try w.lifeforms.ensureTotalCapacity(std.testing.allocator,4);
  var rabbit=Life.init(w.transformedPoints[0],.Rabbit,0);rabbit.satiety=50;w.lifeforms.appendAssumeCapacity(rabbit);
  w.lifeforms.items[0].aiStep(&w,.{.dt=dt,.timeScale=@as(f32,1),.gameTime=@as(f64,0)});
  if(dt<1)try std.testing.expect(w.vegetation[0]>0) else try std.testing.expectEqual(@as(f32,0),w.vegetation[0]);
 }
}
