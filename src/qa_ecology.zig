//! Real production ecology on a small controlled habitat. Not a replacement model.
const std = @import("std");
const Planet = @import("simulation/planet.zig").Planet;
const Lifeform = @import("simulation/life.zig").Lifeform;
const Ecology = @import("simulation/ecology.zig");
const Vec3 = @import("zalgebra").Vec3;
test "actual production ecosystem grows inherited plants and feeds and breeds rabbits" {
    var arena = std.heap.ArenaAllocator.init(std.testing.allocator);
    defer arena.deinit();
    const a = arena.allocator();
    var planet: Planet = undefined;
    planet.simulationArena = arena;
    planet.radius = 100;
    planet.seed = 42;
    planet.vertices = try a.alloc(Vec3, 7);
    planet.transformedPoints = planet.vertices;
    planet.verticesNeighbours = try a.alloc([6]u32, 7);
    for (0..7) |i| {
        planet.vertices[i] = Vec3.new(100, @as(f32,@floatFromInt(i))*3, 0).norm().scale(100);
        planet.verticesNeighbours[i] = .{0,1,2,3,4,5};
    }
    planet.vegetation = try a.alloc(f32, 7);
    planet.vegetationSnapshot = try a.alloc(f32, 7);
    planet.plantTraits = try a.alloc(Ecology.Plant, 7);
    planet.temperature = try a.alloc(f32, 7);
    planet.waterMass = try a.alloc(f32, 7);
    @memset(planet.vegetation, 0);
    @memset(planet.plantTraits, .{});
    @memset(planet.temperature, 295.15);
    @memset(planet.waterMass, 0);
    planet.vegetation[0] = 0.35;
    planet.averageCarbonDioxideMass = 100;
    planet.averageOxygenMass = 100;
    planet.plantGenerations = 0;
    planet.plantBirths = 0;
    planet.rabbitBirths = 0;
    planet.rabbitMeals = 0;
    planet.rabbitDeaths = 0;
    planet.lifeforms = try std.ArrayListUnmanaged(Lifeform).initCapacity(a, 1024);
    var mother = Lifeform.init(planet.vertices[0], .Rabbit, 0);
    mother.genome.gender = .Female;
    mother.prng = std.rand.DefaultPrng.init(1);
    var father = Lifeform.init(planet.vertices[0], .Rabbit, 0);
    father.genome.gender = .Male;
    father.prng = std.rand.DefaultPrng.init(2);
    planet.lifeforms.appendAssumeCapacity(mother);
    planet.lifeforms.appendAssumeCapacity(father);
    var time: f64 = 0;
    for (0..1008) |_| {
        const options: Planet.SimulationOptions = .{.dt=600,.timeScale=1,.gameTime=time,.solarVector=Vec3.new(1,0,0),.solarConstant=1360,.planetRotationTime=86400};
        var remaining=planet.lifeforms.items.len;
        while(remaining>0) { remaining-=1; planet.lifeforms.items[remaining].aiStep(&planet,options); }
        planet.simulateVegetation(options,0,7);
        time+=600;
    }
    var total: f32=0;
    for(planet.vegetation) |v| { try std.testing.expect(std.math.isFinite(v)); try std.testing.expect(v>=0 and v<=1); total+=v; }
    std.debug.print("REAL ECOLOGY 7 days: biomass={d} population={d} births={d} meals={d} generations={d}\n",.{total,planet.lifeforms.items.len,planet.rabbitBirths,planet.rabbitMeals,planet.plantGenerations});
    try std.testing.expect(planet.rabbitBirths>0);
    try std.testing.expect(planet.rabbitMeals>0);
    try std.testing.expect(planet.lifeforms.items.len>2);
    try std.testing.expect(total>0.35);
    try std.testing.expect(planet.plantGenerations>0);
    try std.testing.expect(planet.plantTraits[1].optimum!=295.15);
    try std.testing.expect(planet.averageCarbonDioxideMass<100);
    // A heritable warm-adapted lineage outcompetes sparse cold-adapted
    // populations in a warm habitat; this exercises production colonization.
    @memset(planet.vegetation, 0.1);
    @memset(planet.temperature, 315);
    @memset(planet.plantTraits, .{ .optimum=280, .generation=1 });
    planet.vegetation[0]=0.8;
    planet.plantTraits[0]=.{ .optimum=315, .generation=2 };
    planet.simulateVegetation(.{.dt=600,.timeScale=1,.gameTime=time,.solarVector=Vec3.new(1,0,0),.solarConstant=1360,.planetRotationTime=86400},0,7);
    try std.testing.expect(planet.plantTraits[1].generation>=3);
    try std.testing.expect(@abs(planet.plantTraits[1].optimum-315)<4);
    std.debug.print("SELECTION warm habitat: inherited optimum={d:.2}K generation={d}\n",.{planet.plantTraits[1].optimum,planet.plantTraits[1].generation});

    var peak: usize = planet.lifeforms.items.len;
    for (0..4320) |_| {
        const options: Planet.SimulationOptions = .{.dt=600,.timeScale=1,.gameTime=time,.solarVector=Vec3.new(1,0,0),.solarConstant=1360,.planetRotationTime=86400};
        var remaining=planet.lifeforms.items.len;
        while(remaining>0) { remaining-=1; planet.lifeforms.items[remaining].aiStep(&planet,options); }
        planet.simulateVegetation(options,0,7);
        time+=600;
        peak=@max(peak,planet.lifeforms.items.len);
        for(planet.lifeforms.items) |animal| {
            try std.testing.expect(std.math.isFinite(animal.position.length()));
            try std.testing.expect(animal.satiety>0 and animal.satiety<=100);
        }
    }
    std.debug.print("SOAK endpoint population={d} peak={d} births={d} deaths={d}\n",.{planet.lifeforms.items.len,peak,planet.rabbitBirths,planet.rabbitDeaths});
    var final_biomass: f32=0;
    for(planet.vegetation) |v| { try std.testing.expect(std.math.isFinite(v)); final_biomass+=v; }
    try std.testing.expect(final_biomass>0.35);
    std.debug.print("SOAK final biomass={d}\n",.{final_biomass});
    try std.testing.expect(peak<=512);
    try std.testing.expect(planet.lifeforms.items.len>0);
    std.debug.print("SOAK 37 days: living={d} peak={d} births={d} meals={d} deaths={d}\n",.{planet.lifeforms.items.len,peak,planet.rabbitBirths,planet.rabbitMeals,planet.rabbitDeaths});

}
