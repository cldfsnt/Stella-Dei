const std=@import("std");
const P=@import("simulation/planet.zig").Planet;
const S=@import("save_schema.zig");
const za=@import("zalgebra");
const Loop=@import("loop.zig").EventLoop;
extern fn emscripten_get_now() f64;
var output:[]const u8=&.{};
const Graph=struct{points:[]const [3]f32,neighbors:[]const [6]u32};
export fn qa_output() [*]const u8{return output.ptr;}
export fn qa_output_len() usize{return output.len;}
export fn qa_width() u32{return std.simd.suggestVectorLength(f32) orelse 4;}
export fn qa_run(bytes:[*]const u8,len:usize,graph:[*]const u8,graph_len:usize,ticks:u32) u32 {run(bytes[0..len],graph[0..graph_len],ticks) catch |err| {std.debug.print("QA_ERROR {s}\n",.{@errorName(err)});return 1;};return 0;}
fn dupFloat(a:std.mem.Allocator,values:[]const f32)![]f32{const out=try a.alignedAlloc(f32,@alignOf(@Vector(std.simd.suggestVectorLength(f32) orelse 4,f32)),values.len);@memcpy(out,values);return out;}
fn run(bytes:[]const u8,graph_bytes:[]const u8,ticks:u32)!void{
 const a=std.heap.c_allocator;
 const parsed=try S.parse(a,bytes);var saved=parsed.value;try saved.validate();

 const g=(try std.json.parseFromSlice(Graph,a,graph_bytes,.{.allocate=.alloc_always})).value;
 const n=saved.water.len;if(g.points.len!=n or g.neighbors.len!=n)return error.Shape;
 var p:P=undefined;
 inline for(std.meta.fields(P)) |field| {@field(p,field.name)=if(field.default_value)|v| @as(*const field.type,@ptrCast(@alignCast(v))).* else if(comptime std.mem.eql(u8,field.name,"allocator") or std.mem.eql(u8,field.name,"simulationArena") or std.mem.eql(u8,field.name,"temperaturePtrOrg")) undefined else std.mem.zeroes(field.type);}
 p.allocator=a;p.simulationArena=std.heap.ArenaAllocator.init(a);p.radius=saved.radius;p.seed=saved.seed;p.numSubdivisions=saved.subdivisions;
 p.vertices=try a.alloc(za.Vec3,n);for(p.vertices,g.points)|*v,d|v.*=.{.data=d};
 p.verticesNeighbours=try a.dupe([6]u32,g.neighbors);p.transformedPoints=try a.alloc(za.Vec3,n);
 p.elevation=try dupFloat(a,saved.elevation);p.temperature=try dupFloat(a,saved.temperature);p.temperaturePtrOrg=p.temperature.ptr;p.newTemperature=try dupFloat(a,saved.temperature);
 p.waterMass=try dupFloat(a,saved.water);p.newWaterMass=try dupFloat(a,saved.water);p.waterVaporMass=try dupFloat(a,saved.vapor);p.newWaterVaporMass=try dupFloat(a,saved.vapor);
 p.rainfall=try dupFloat(a,saved.rainfall);p.vegetation=try dupFloat(a,saved.vegetation);p.vegetationSnapshot=try dupFloat(a,saved.vegetation);p.plantTraits=try a.dupe(S.Plant,saved.plants);p.heatCapacityCache=try a.alloc(f32,n);
 p.airVelocity=try a.alloc(za.Vec2,n);p.airPositionError=try a.alloc(za.Vec2,n);for(p.airVelocity,saved.wind)|*v,d|v.data=d;for(p.airPositionError,saved.wind_error)|*v,d|v.data=d;
 p.averageNitrogenMass=saved.nitrogen;p.averageOxygenMass=saved.oxygen;p.averageCarbonDioxideMass=saved.carbon_dioxide;
 p.worldMode=saved.mode;
 if(saved.origin)|origin|{p.microbeCells=try a.alloc(S.Microbes.Cell,n);for(p.microbeCells,origin.cells)|*c,s|c.*=s.runtime();p.microbeStats=origin.stats;}
 p.sandboxDefense=saved.sandbox_defense orelse .{};
 if(saved.wind_dispersal)|w|p.windDispersal=.{.enabled=w.enabled,.law=w.law,.stream_seed=w.stream_seed,.serial=w.serial};


 p.plantGenerations=saved.plant_generations;p.plantBirths=saved.plant_births;p.rabbitBirths=saved.rabbit_births;p.rabbitMeals=saved.rabbit_meals;p.rabbitDeaths=saved.rabbit_deaths;p.plantColorWavelength=saved.plant_color;
 for(0..n)|i|{const ns=p.getNeighbours(i);for(ns,g.neighbors[i])|actual,expected|if(actual!=expected)return error.GraphIdentity;}
    for (saved.rabbits) |rabbit| {
        const Life = @TypeOf(p.lifeforms.items[0]);
        var life: Life = undefined;
        life.position = .{ .data = rabbit.position };
        life.velocity = .{ .data = rabbit.velocity };
        life.kind = .Rabbit;
        life.timeBorn = rabbit.born;
        life.genome = .{ .gender = if (rabbit.female) .Female else .Male };
        life.satiety = rabbit.satiety;
        life.sexualCriteria = rabbit.criteria;
        life.reproductionCooldown = rabbit.cooldown;
        life.prng = .{ .s = rabbit.random };
        life.state = switch (rabbit.state) {
            .wander => .wander,
            .go_to_point => .{ .go_to_point = .{ .data = rabbit.target } },
            .gestation => .{ .gestation = .{ .since = rabbit.gestation_since } },
        };
        try p.lifeforms.append(p.simulationArena.allocator(),life);
    }
 if(saved.beta_origin)|beta|{try p.ensureLandBetaStorage();p.landBeta=beta.config;@memcpy(p.landSoil,beta.soil);@memcpy(p.landVapor,beta.vapor);@memcpy(p.landNewVapor,beta.vapor);}
 p.refreshTransformedPoints(saved.axial_tilt);
 std.debug.print("LAYOUT plant={d} planet={d} cells={d}\n",.{@sizeOf(S.Plant),@sizeOf(P),n});
 std.debug.print("BETA_LAYOUT enabled={} soil_bytes={} vapor_bytes={} scratch_bytes={} cohort_bytes={}\n",.{p.landBeta.enabled,p.landSoil.len*8,p.landVapor.len*8,p.landNewVapor.len*8+p.landCoefficient.len*8+p.landRootH.len*32+p.landRootOwner.len*32,@sizeOf(S.Microbes.Cohort)});
 std.debug.print("ENGINE_MEMORY cell_size={} cohort_size={} cell_array_bytes={} amount_bytes={} owner_bytes={}\n",.{@sizeOf(S.Microbes.Cell),@sizeOf(S.Microbes.Cohort),p.microbeCells.len*@sizeOf(S.Microbes.Cell),p.landRootH.len*32,p.landRootOwner.len*32});
 var loop=Loop.init();try loop.start(a);loop.beginEvent();
 var first_ms:f64=0;var first_stages:[4]f64=.{0,0,0,0};var first_sub:[5]f64=.{0,0,0,0,0};
 var begin=emscripten_get_now();const warmup:u32=if(ticks>=72)12 else 0;
 for(0..ticks)|tick|{
  if(tick==warmup)begin=emscripten_get_now();
  const phi:f32=@floatCast(@mod(saved.game_time/saved.rotation_time*2*std.math.pi,2*std.math.pi));const theta:f32=std.math.pi/2.0;
  p.simulate(&loop,.{.dt=1440,.timeScale=1,.gameTime=saved.game_time,.solarConstant=saved.solar_constant,.planetRotationTime=saved.rotation_time,.solarVector=za.Vec3.new(@cos(phi)*@sin(theta),@sin(phi)*@sin(theta),@cos(theta))});saved.game_time+=1440;
  if(tick==warmup){first_ms=emscripten_get_now()-begin;first_stages=@import("simulation/planet.zig").qa_stages;first_sub=@import("simulation/planet.zig").qa_substages;}
 }
 const elapsed=emscripten_get_now()-begin;
 std.debug.print("CELL_LAYOUT cohort={} cell={} cell_array={}\n",.{@sizeOf(S.Microbes.Cohort),@sizeOf(S.Microbes.Cell),p.microbeCells.len*@sizeOf(S.Microbes.Cell)});
 std.debug.print("FIRST_TICK ms={d} stages={any} sub={any}\n",.{first_ms,first_stages,first_sub});
 std.debug.print("ATMOSPHERE_SUBSTAGES ms={any}\n",.{@import("simulation/planet.zig").qa_substages});
    const rabbits = try a.alloc(S.Rabbit, p.lifeforms.items.len);
    for (p.lifeforms.items, rabbits) |life, *out| {
        out.* = .{ .position = life.position.data, .velocity = life.velocity.data, .born = life.timeBorn, .state = switch (life.state) {
            .wander => .wander,
            .go_to_point => .go_to_point,
            .gestation => .gestation,
        }, .female = life.genome.gender == .Female, .satiety = life.satiety, .criteria = life.sexualCriteria, .cooldown = life.reproductionCooldown, .random = life.prng.s };
        switch (life.state) {
            .go_to_point => |v| out.target = v.data,
            .gestation => |info| out.gestation_since = info.since,
            else => {},
        }
    }
 saved.version=if(p.landBeta.enabled) (if(p.landBeta.physiology_law==3) @as(u32,10) else if(p.landBeta.physiology_law==2) @as(u32,9) else @as(u32,8)) else 7;saved.sandbox_defense=if(p.sandboxDefense.enabled)p.sandboxDefense else null;
 saved.rabbits=rabbits;if(p.worldMode==.origin){const sparse=try S.captureSparse(a,p.microbeCells);saved.origin=.{.model_revision=5,.cohort_encoding=.sparse_indexed,.cells=sparse.cells,.stats=p.microbeStats};}else saved.origin=null;
 saved.plant_generations=p.plantGenerations;saved.plant_births=p.plantBirths;saved.rabbit_births=p.rabbitBirths;saved.rabbit_meals=p.rabbitMeals;saved.rabbit_deaths=p.rabbitDeaths;saved.plant_color=p.plantColorWavelength;

 saved.elevation=p.elevation;saved.temperature=p.temperature;saved.vegetation=p.vegetation;saved.water=p.waterMass;saved.vapor=p.waterVaporMass;saved.rainfall=p.rainfall;saved.plants=p.plantTraits;
 const wind=try a.alloc([2]f32,n);const wind_error=try a.alloc([2]f32,n);for(wind,p.airVelocity)|*v,d|v.*=d.data;for(wind_error,p.airPositionError)|*v,d|v.*=d.data;saved.wind=wind;saved.wind_error=wind_error;
 saved.nitrogen=p.averageNitrogenMass;saved.oxygen=p.averageOxygenMass;saved.carbon_dioxide=p.averageCarbonDioxideMass;
 if(p.landBeta.enabled){for(p.waterVaporMass,0..)|*v,i|v.*=p.vaporMass32(i);saved.beta_origin=.{.format=if(p.landBeta.physiology_law==3).origin_land_beta_v3 else if(p.landBeta.physiology_law==2).origin_land_beta_v2 else .origin_land_beta_v1,.config=p.landBeta,.soil=p.landSoil,.vapor=p.landVapor};}
 if(p.windDispersal.enabled){saved.version=S.COMBINED_VERSION;saved.wind_dispersal=.{.enabled=true,.law=p.windDispersal.law,.stream_seed=p.windDispersal.stream_seed,.serial=p.windDispersal.serial};}else saved.wind_dispersal=null;
 std.debug.print("WIND_FINAL enabled={} serial={}\n",.{p.windDispersal.enabled,p.windDispersal.serial});
 try saved.validate();output=try std.json.stringifyAlloc(a,saved,.{});
 std.debug.print("WASM_PLANET ticks={d} cells={d} width={d} parallel={d} total_ms={d} temperature_ms={d} liquid_wind_ms={d} atmosphere_ms={d} ecology_ms={d}\n",.{ticks,n,qa_width(),loop.getParallelCount(),elapsed,@import("simulation/planet.zig").qa_stages[0],@import("simulation/planet.zig").qa_stages[1],@import("simulation/planet.zig").qa_stages[2],@import("simulation/planet.zig").qa_stages[3]});
}

var qa_enabled:bool=false;
export fn qa_set_candidate(on:u32)void{qa_enabled=on!=0;}
