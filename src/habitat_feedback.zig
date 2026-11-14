//! Read-only guidance derived from actual current habitat and engine history.
const std = @import("std");
pub const GoalStage = enum(u8) { plant, add_pair, feeding, offspring, growth, living };
pub const GoalFacts = struct {
    planted: bool = false,
    grown: bool = false,
    descendants: bool = false,
    rabbits: usize = 0,
    meals: u64 = 0,
    births: u64 = 0,
    deaths: u64 = 0,
};
pub fn stage(f: GoalFacts) GoalStage {
    // A past birth/meal does not mean an extinct habitat is complete.
    if (!f.planted) return .plant;
    if (f.rabbits == 0) return .add_pair;
    if (f.meals == 0) return .feeding;
    if (f.births == 0) return .offspring;
    if (!f.grown or !f.descendants) return .growth;
    return .living;
}
pub fn facts(planet: anytype) GoalFacts {
    var f = GoalFacts{ .rabbits=planet.lifeforms.items.len, .meals=planet.rabbitMeals, .births=planet.rabbitBirths, .deaths=planet.rabbitDeaths };
    for (planet.vegetation,planet.plantTraits) |cover,trait| {
        f.planted = f.planted or cover > 0.01;
        f.grown = f.grown or cover > 0.5;
        f.descendants = f.descendants or (cover > 0.01 and trait.generation > 0);
    }
    return f;
}
pub fn goalStage(planet: anytype) GoalStage { return stage(facts(planet)); }
pub fn instruction(f: GoalFacts) []const u8 {
    return switch (stage(f)) {
        .plant => if(f.deaths>0) "Restore food: check water and temperature, then plant." else "Find dry land and plant a patch of food.",
        .add_pair => if(f.deaths>0) "Habitat has no rabbits. Check water and temperature before adding a new pair." else "Add a rabbit pair to your planted patch.",
        .feeding => "Press Play and watch fullness and grazing. Meals are not recorded yet.",
        .offspring => "Feeding observed. Keep food available and allow time for offspring.",
        .growth => "Births recorded. Let living plants grow and spread to nearby ground.",
        .living => "Keep habitat growing. Try a small change, then inspect its effects.",
    };
}
pub const AnimalLabel = enum { flooded, too_hot, too_cold, expecting, hungry, young, resting, fed };
pub fn animalLabelText(label: AnimalLabel) []const u8 {
    return switch(label) {
        .flooded=>"Flooded ground", .too_hot=>"Dangerous heat", .too_cold=>"Dangerous cold",
        .expecting=>"Expecting offspring", .hungry=>"Hungry", .young=>"Young rabbit", .resting=>"Breeding cooldown", .fed=>"Fed; resting",
    };
}
pub const RabbitStatus = struct { label:AnimalLabel, age_hours:f64, fullness:f32, gestation_hours:?f64, cooldown_hours:f32 };
pub fn inspectRabbit(planet:anytype,index:usize,game_time:f64) ?RabbitStatus {
    if(index>=planet.lifeforms.items.len)return null;
    const rabbit=planet.lifeforms.items[index];
    const point=planet.getNearestPointTo(rabbit.position);
    const age=@max(0,game_time-rabbit.timeBorn)/3600;
    const gestation:?f64=if(rabbit.state==.gestation) @max(0,86400-(game_time-rabbit.state.gestation.since))/3600 else null;
    const label:AnimalLabel=if(planet.waterMass[point]*planet.getKmPerWaterMass()>0.002) .flooded else if(planet.temperature[point]>333.15) .too_hot else if(planet.temperature[point]<243.15) .too_cold else if(gestation!=null) .expecting else if(rabbit.satiety<85) .hungry else if(age<12) .young else if(rabbit.reproductionCooldown>0) .resting else .fed;
    return .{.label=label,.age_hours=age,.fullness=std.math.clamp(rabbit.satiety,0,100),.gestation_hours=gestation,.cooldown_hours=@max(0,rabbit.reproductionCooldown)/3600};
}
/// Recompute on each inspection; never retain a pointer/index across removals.
/// This identifies a nearby animal, not an implied stable selected identity.
pub fn nearestRabbit(planet:anytype,point:usize) ?usize {
    if(point>=planet.transformedPoints.len)return null;
    var best:f32=120;
    var result:?usize=null;
    for(planet.lifeforms.items,0..) |rabbit,i| {
        const distance=rabbit.position.distance(planet.transformedPoints[point]);
        if(distance<best){best=distance;result=i;}
    }
    return result;
}
test "goals advance from real observations and regress after habitat loss" {
    var f:GoalFacts=.{};
    try std.testing.expectEqual(GoalStage.plant,stage(f));
    f.planted=true;try std.testing.expectEqual(GoalStage.add_pair,stage(f));
    f.rabbits=2;try std.testing.expectEqual(GoalStage.feeding,stage(f));
    f.meals=1;try std.testing.expectEqual(GoalStage.offspring,stage(f));
    f.births=1;f.rabbits=3;try std.testing.expectEqual(GoalStage.growth,stage(f));
    f.grown=true;f.descendants=true;try std.testing.expectEqual(GoalStage.living,stage(f));
    f.rabbits=0;f.deaths=3;try std.testing.expectEqual(GoalStage.add_pair,stage(f));
    f.planted=false;try std.testing.expectEqual(GoalStage.plant,stage(f));
    f.planted=true;try std.testing.expectEqual(GoalStage.add_pair,stage(f));
    try std.testing.expect(std.mem.indexOf(u8,instruction(f),"no rabbits")!=null);
    try std.testing.expectEqual(GoalStage.plant,stage(.{}));
}
test "animal feedback reports state not invented movement and rejects removed index" {
    const Rabbit=struct { position:u32=0,timeBorn:f64=0,state:union(enum){wander:void,gestation:struct{since:f64}}=.wander,satiety:f32=100,reproductionCooldown:f32=0 };
    const P=struct {
        lifeforms:struct{items:[]Rabbit},waterMass:[]f32,temperature:[]f32,
        pub fn getNearestPointTo(_: @This(), _:u32) usize{return 0;}
        pub fn getKmPerWaterMass(_: @This()) f32{return 1;}
    };
    var animals=[_]Rabbit{.{}};var water=[_]f32{0};var temp=[_]f32{295};
    var p=P{.lifeforms=.{.items=&animals},.waterMass=&water,.temperature=&temp};
    try std.testing.expectEqual(AnimalLabel.young,inspectRabbit(p,0,0).?.label);
    try std.testing.expectEqual(AnimalLabel.fed,inspectRabbit(p,0,86400).?.label);
    animals[0].satiety=50;try std.testing.expectEqual(AnimalLabel.hungry,inspectRabbit(p,0,86400).?.label);
    animals[0].state=.{.gestation=.{.since=86400}};
    const s=inspectRabbit(p,0,129600).?;try std.testing.expectEqual(AnimalLabel.expecting,s.label);try std.testing.expectEqual(@as(?f64,12),s.gestation_hours);
    water[0]=0.003;try std.testing.expectEqual(AnimalLabel.flooded,inspectRabbit(p,0,129600).?.label);
    p.lifeforms.items=p.lifeforms.items[0..0];try std.testing.expectEqual(@as(?RabbitStatus,null),inspectRabbit(p,0,129600));
}
