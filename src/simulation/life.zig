const std = @import("std");
const za = @import("zalgebra");
const Planet = @import("planet.zig").Planet;
const ObjLoader = @import("../ObjLoader.zig");
const Allocator = std.mem.Allocator;
const Vec3 = za.Vec3;

var birthCounter = std.atomic.Value(u32).init(0);

var rabbitMesh: ?ObjLoader.Mesh = null;

const Gender = enum { Male, Female };

const Genome = struct {
    gender: Gender = .Male,
};

pub const Lifeform = struct {
    position: Vec3,
    velocity: Vec3 = Vec3.zero(),
    kind: Kind,
    state: State = .wander,
    /// Game time at which the lifeform was born
    timeBorn: f64,
    prng: std.rand.DefaultPrng,
    /// The minimum bar for a given rabbit's sexual attractiveness
    /// This goes up the more there are attemps at mating
    /// This goes down naturally over time (although this has a
    /// minimum depending on genome)
    sexualCriteria: f32 = 0.1,
    reproductionCooldown: f32 = 0,
    genome: Genome = .{},
    /// Opposite of hunger, goes down gradually.
    /// When it reaches 0, the lifeform dies.
    satiety: f32 = 100,

    pub const Kind = enum { Rabbit };

    pub const State = union(enum) {
        wander: void,
        go_to_point: Vec3,
        gestation: struct {
            /// Game time at which the lifeform started being 'pregnant'
            since: f64,
        },

        fn goToPoint(planet: *const Planet, idx: usize) State {
            // TODO, add some rng to the final position
            const pos = planet.transformedPoints[idx];
            return State{ .go_to_point = pos };
        }
    };

    pub fn initMeshes(allocator: Allocator) !void {
        if (rabbitMesh == null) {
            rabbitMesh = try ObjLoader.readObjFromFile(allocator, "assets/rabbit/rabbit.obj");
        }
    }

    pub fn init(position: Vec3, kind: Kind, gameTime: f64) Lifeform {
        // Births in the same millisecond must not share an identical RNG stream.
        const serial: u64 = birthCounter.fetchAdd(1, .monotonic);
        var prng = std.rand.DefaultPrng.init(@as(u64, @bitCast(std.time.milliTimestamp())) ^ (serial *% 0x9e3779b97f4a7c15));
        const gender: Gender = if (prng.random().boolean()) .Male else .Female;
        return Lifeform{ .position = position, .kind = kind, .prng = prng, .timeBorn = gameTime, .genome = .{ .gender = gender } };
    }

    pub fn getMesh(self: Lifeform) ObjLoader.Mesh {
        return switch (self.kind) {
            .Rabbit => rabbitMesh.?,
        };
    }

    /// Duration of gestations in in-game seconds
    const GESTATION_DURATION: f64 = 86400; // 1 day
    const SEXUAL_MATURITY_AGE: f64 = 86400 / 2; // 12 hours

    fn hasBreedingHabitat(self: *const Lifeform, planet: anytype, idx: usize) bool {
        // Food-limited reproduction avoids a fed population overshooting its
        // habitat and stripping every plant before hunger becomes visible.
        var food = planet.vegetation[idx];
        for (planet.getNeighbours(idx)) |n| food += planet.vegetation[n];
        if (food < 1.5) return false;
        var nearby: usize = 0;
        for (planet.lifeforms.items) |other| {
            if (self.position.distance(other.position) < 200) nearby += 1;
        }
        return @as(f32, @floatFromInt(nearby)) < food * 4;
    }

    /// Surface-bound animal ecology. Feeding is independent of behavioral state,
    /// so gestating mothers and travelling animals can eat rather than starving.
    pub fn aiStep(self: *Lifeform, planet: anytype, options: anytype) void {
        const dt = @max(0, options.dt * options.timeScale);
        if (dt == 0) return;
        const idx = planet.getNearestPointTo(self.position);
        const point = planet.transformedPoints[idx];
        const temperature = planet.temperature[idx];
        const age = options.gameTime - self.timeBorn;
        self.reproductionCooldown = @max(0, self.reproductionCooldown - dt);
        self.satiety -= dt * 0.00025;
        if (planet.waterMass[idx] * planet.getKmPerWaterMass() > 0.002 or temperature > 333.15 or temperature < 243.15 or self.satiety <= 0 or age > 30 * 86400) {
            for (planet.lifeforms.items, 0..) |*animal, i| {
                if (animal == self) {
                    _ = planet.lifeforms.orderedRemove(i);
                    planet.rabbitDeaths += 1;
                    return;
                }
            }
            return;
        }
        if (self.satiety < 85 and planet.vegetation[idx] > 0) {
            // Search/handling takes time, especially in sparse vegetation. Every
            // satiety gain is funded by actual cover removed; no refuge floor.
            const Foraging = @import("foraging.zig");
            const bite = Foraging.takeTough(planet.vegetation[idx], self.satiety, dt,planet.plantTraits[idx].toughness);
            if (bite.eaten > 0) {
                planet.vegetation[idx] = bite.after;
                self.satiety = Foraging.fedSatiety(self.satiety, bite.eaten);
                planet.rabbitMeals += 1; // positive feeding events, not full meals
            }
        }
        if (self.state == .gestation) {
            if (options.gameTime - self.state.gestation.since >= GESTATION_DURATION and self.satiety > 35 and planet.lifeforms.items.len < 512) {
                var child = Lifeform.init(point, self.kind, options.gameTime);
                child.prng = std.rand.DefaultPrng.init(self.prng.random().int(u64));
                child.genome.gender = if (child.prng.random().boolean()) .Male else .Female;
                self.state = .wander;
                self.reproductionCooldown = 86400;
                self.satiety -= 15;
                planet.rabbitBirths += 1;
                planet.addLifeformDuringStep(child);
                return;
            }
        } else if (age >= SEXUAL_MATURITY_AGE and self.satiety > 65 and self.reproductionCooldown == 0 and self.hasBreedingHabitat(planet, idx)) {
            for (planet.lifeforms.items) |*other| {
                if (other == self or other.genome.gender == self.genome.gender or other.state == .gestation or other.reproductionCooldown > 0 or other.satiety <= 65 or options.gameTime - other.timeBorn < SEXUAL_MATURITY_AGE) continue;
                if (self.position.distance(other.position) < 200) {
                    const mother = if (self.genome.gender == .Female) self else other;
                    mother.state = .{ .gestation = .{ .since = options.gameTime } };
                    self.reproductionCooldown = 2 * 86400;
                    other.reproductionCooldown = 2 * 86400;
                    break;
                }
            }
        }
        // Hungry rabbits seek actual neighboring food. Healthy rabbits remain
        // in their habitat, avoiding the old random march into oceans.
        var target = idx;
        var best = planet.vegetation[idx];
        if (self.satiety < 85) {
            for (planet.getNeighbours(idx)) |n| {
                if (planet.waterMass[n] * planet.getKmPerWaterMass() <= 0.002 and planet.temperature[n] > 253.15 and planet.temperature[n] < 328.15 and planet.vegetation[n] > best + 0.05) {
                    target = n;
                    best = planet.vegetation[n];
                }
            }
        }
        const destination = planet.transformedPoints[target];
        const delta = destination.sub(self.position);
        const distance = delta.length();
        if (target != idx and distance > 0.001) {
            // Clamp displacement to avoid overshoot at accelerated speeds.
            self.position = self.position.add(delta.scale(@min(1, dt * 0.02 / distance))).norm().scale(destination.length());
        } else {
            self.position = self.position.norm().scale(point.length());
        }
        self.velocity = Vec3.zero();
    }
};
