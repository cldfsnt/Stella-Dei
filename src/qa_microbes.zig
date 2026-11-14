//! Real Planet microbial integration on a controlled seven-cell environment.
const std=@import("std");
const Planet=@import("simulation/planet.zig").Planet;
const Microbes=@import("simulation/microbes.zig");
const Vec3=@import("zalgebra").Vec3;
fn totalCarbon(p:*const Planet) f64 {
    var total=p.averageCarbonDioxideMass*1e9*@as(f64,@floatFromInt(p.vertices.len))*(12.0/44.0);
    for(p.microbeCells) |c| total+=@as(f64,Microbes.carbon(c))*p.getMeanPointArea();
    return total;
}
test "actual Origin route conserves atmospheric carbon and nutrients and never spawns sandbox life" {
    var p:Planet=undefined;p.simulationArena=std.heap.ArenaAllocator.init(std.testing.allocator);defer p.simulationArena.deinit();
    const a=p.simulationArena.allocator();p.seed=42;p.radius=100;
    p.vertices=try a.alloc(Vec3,7);p.transformedPoints=p.vertices;p.verticesNeighbours=try a.alloc([6]u32,7);
    for(0..7)|i|{p.vertices[i]=Vec3.new(100,@as(f32,@floatFromInt(i))*3,0).norm().scale(100);p.verticesNeighbours[i]=.{0,1,2,3,4,5};}
    p.vegetation=try a.alloc(f32,7);@memset(p.vegetation,0);
    p.temperature=try a.alloc(f32,7);@memset(p.temperature,303);
    p.waterMass=try a.alloc(f32,7);@memset(p.waterMass,0.002/p.getKmPerWaterMass());
    p.lifeforms=.{};p.worldMode=.sandbox;p.microbeCells=&.{};p.microbeStats=.{};
    p.averageCarbonDioxideMass=100;p.averageOxygenMass=100;
    try std.testing.expectEqual(@as(usize,0),p.microbeCells.len);
    try p.beginOrigin();const initialCarbon=totalCarbon(&p);
    try std.testing.expect(p.seedMicrobes(0));
    try std.testing.expectApproxEqRel(initialCarbon,totalCarbon(&p),0.000001);
    var initialN:f32=0;for(p.microbeCells)|c|initialN+=Microbes.nutrientTotal(c);
    for(0..2400)|tick|{
        p.simulateMicrobes(.{.dt=3600,.timeScale=1,.gameTime=@as(f64,@floatFromInt(tick))*3600,.solarVector=Vec3.new(1,0,0),.solarConstant=1361,.planetRotationTime=86400});
        for(p.microbeCells)|c|try std.testing.expect(Microbes.validCell(c,p.microbeStats.next_lineage));
    }
    var finalN:f32=0;var biomass:f32=0;var active:usize=0;var generation:u32=0;
    for(p.microbeCells)|c|{finalN+=Microbes.nutrientTotal(c);biomass+=Microbes.biomass(c);if(Microbes.biomass(c)>0)active+=1;for(c.cohorts)|cohort|generation=@max(generation,cohort.generation);}
    try std.testing.expectApproxEqAbs(initialN,finalN,0.00001);
    try std.testing.expectApproxEqRel(initialCarbon,totalCarbon(&p),0.000005);
    try std.testing.expect(p.microbeStats.births>0 and active>1 and generation>0);
    try std.testing.expectEqual(@as(usize,0),p.lifeforms.items.len);
    for(p.vegetation)|v|try std.testing.expectEqual(@as(f32,0),v);
    std.debug.print("ORIGIN100DAY biomass={d:.5} cells={d} births={d} generation={d} carbon_relative_error={e} nutrient_error={e}\n",.{biomass,active,p.microbeStats.births,generation,@abs(initialCarbon-totalCarbon(&p))/initialCarbon,@abs(initialN-finalN)});
    try std.testing.expect(p.microbeStats.grazed_carbon>0);
    try std.testing.expectApproxEqRel(p.microbeStats.grazed_carbon*0.25,p.microbeStats.grazing_respired_carbon,0.000001);
    try std.testing.expect(p.averageOxygenMass>=0 and p.averageCarbonDioxideMass>=0);
    std.debug.print("GRAZING_PLANET consumed_kgC={d} respired_kgC={d} oxygen={d}\n",.{p.microbeStats.grazed_carbon,p.microbeStats.grazing_respired_carbon,p.averageOxygenMass});
    try std.testing.expect(p.microbeStats.relocations>0 and p.microbeStats.movement_respired_carbon>0);
    var resident_moves:u64=0;
    for(p.microbeCells,0..)|cell,index|for(cell.cohorts)|co|{
        if(co.biomass>0 and co.relocations>0){try std.testing.expectEqual(@as(u32,@intCast(index)),co.last_to);try std.testing.expect(co.last_from!=co.last_to);resident_moves+=co.relocations;}
        if(co.biomass>0){var copies:usize=0;for(p.microbeCells)|other|for(other.cohorts)|candidate|{if(candidate.biomass>0 and candidate.lineage==co.lineage)copies+=1;};try std.testing.expectEqual(@as(usize,1),copies);}
    };
    try std.testing.expect(resident_moves<=p.microbeStats.relocations);
    std.debug.print("MOTILITY_PLANET relocations={d} respired_kgC={d}\n",.{p.microbeStats.relocations,p.microbeStats.movement_respired_carbon});
    const stats_before_explanation=p.microbeStats;
    for(p.microbeCells,0..)|cell,index| {
        for(0..4)|which| {
            _=p.microbeRelocationOpportunity(index,which,8640000);
            try std.testing.expectEqualDeep(cell,p.microbeCells[index]);
        }
    }
    try std.testing.expectEqualDeep(stats_before_explanation,p.microbeStats);
    var support_total:f32=0;var organized_descendants:usize=0;
    for(p.microbeCells)|cell|for(cell.cohorts)|co|{support_total+=co.support_mass;if(co.generation>0 and co.support_mass>0)organized_descendants+=1;};
    try std.testing.expect(support_total>0 and organized_descendants>0);
    const old_depth=p.waterMass[0]*p.getKmPerWaterMass();
    try std.testing.expectApproxEqAbs(@as(f32,0.1),p.adjustWaterDepth(0,0.0001),0.00001);
    try std.testing.expectApproxEqAbs(@as(f32,-0.1),p.adjustWaterDepth(0,-0.0001),0.00001);
    try std.testing.expectApproxEqAbs(old_depth,p.waterMass[0]*p.getKmPerWaterMass(),0.00000001);
    try std.testing.expectEqual(@as(f32,0),p.adjustWaterDepth(0,1));
    std.debug.print("PRODUCER_PLANET support={d} actual_descendants={d} fine_water_roundtrip=true\n",.{support_total,organized_descendants});
    const before=p.microbeStats.fixed_carbon;
    p.simulateMicrobes(.{.dt=3600,.timeScale=1,.gameTime=8640000,.solarVector=Vec3.new(1,0,0),.solarConstant=0,.planetRotationTime=86400});
    try std.testing.expectEqual(before,p.microbeStats.fixed_carbon);
}
