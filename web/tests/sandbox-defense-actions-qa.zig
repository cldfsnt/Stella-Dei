const std=@import("std");const E=@import("simulation/ecology.zig");const A=@import("sandbox_defense.zig");
const Fixture=struct{
 worldMode:enum{sandbox,origin}=.sandbox,seed:u64=42,sandboxDefense:E.DefenseConfig=.{},
 vegetation:[]f32,waterMass:[]f32,temperature:[]f32,plantTraits:[]E.Plant,
 pub fn getKmPerWaterMass(_: *@This())f32{return 1;}
};
test "explicit enable and empty dry founder transaction preserve other state"{
 var v=[_]f32{0,0.1,0,0};var w=[_]f32{0,0,0.01,0};var t=[_]f32{295,295,295,240};var p=[_]E.Plant{.{.generation=9,.optimum=310},.{},.{},.{}};
 var f=Fixture{.vegetation=&v,.waterMass=&w,.temperature=&t,.plantTraits=&p};const oldv=v;const oldp=p;
 try std.testing.expectEqual(A.Status.disabled,A.plantDefended(&f,0,0.5).status);try std.testing.expectEqualDeep(oldv,v);try std.testing.expectEqualDeep(oldp,p);
 try std.testing.expectEqual(A.Status.enabled,A.enableDefenses(&f).status);try std.testing.expectEqualDeep(oldv,v);try std.testing.expectEqualDeep(oldp,p);
 try std.testing.expectEqual(@as(u64,42),f.sandboxDefense.stream_seed);try std.testing.expect(A.validConfig(f.sandboxDefense));
 const config=f.sandboxDefense;try std.testing.expectEqual(A.Status.already_enabled,A.enableDefenses(&f).status);try std.testing.expectEqualDeep(config,f.sandboxDefense);
 try std.testing.expectEqual(A.Status.occupied,A.plantDefended(&f,1,0.5).status);try std.testing.expectEqual(A.Status.water,A.plantDefended(&f,2,0.5).status);
 for([_]f32{-1,0.25,1,std.math.nan(f32),std.math.inf(f32)})|d|try std.testing.expectEqual(A.Status.invalid,A.plantDefended(&f,0,d).status);
 try std.testing.expectEqual(A.Status.invalid,A.plantDefended(&f,4,0).status);try std.testing.expectEqualDeep(oldv,v);try std.testing.expectEqualDeep(oldp,p);
 const result=A.plantDefended(&f,0,0.5);try std.testing.expectEqual(A.Status.planted,result.status);try std.testing.expectEqual(@as(f32,0.35),result.cover_added);try std.testing.expectEqual(E.Plant{.toughness=0.5},p[0]);try std.testing.expectEqual(@as(f32,0.35),v[0]);
 try std.testing.expectEqual(A.Status.occupied,A.plantDefended(&f,0,0).status);try std.testing.expectEqual(@as(f32,0.5),p[0].toughness);
 // Temperature is not fabricated to guarantee success: a dry cold patch can be planted and die later.
 try std.testing.expectEqual(A.Status.planted,A.plantDefended(&f,3,0).status);try std.testing.expectEqual(@as(f32,240),t[3]);
 try std.testing.expectEqualDeep([_]f32{0,0,0.01,0},w);try std.testing.expectEqualDeep([_]f32{295,295,295,240},t);
 f.worldMode=.origin;try std.testing.expectEqual(A.Status.wrong_mode,A.enableDefenses(&f).status);try std.testing.expectEqual(A.Status.wrong_mode,A.plantDefended(&f,2,0).status);
}
test "malformed configs refuse while shallow films remain eligible"{
 var v=[_]f32{0};var w=[_]f32{std.math.floatTrueMin(f32)};var t=[_]f32{295};var p=[_]E.Plant{.{}};var f=Fixture{.vegetation=&v,.waterMass=&w,.temperature=&t,.plantTraits=&p};
 f.sandboxDefense.stream_seed=1;try std.testing.expectEqual(A.Status.invalid,A.enableDefenses(&f).status);f.sandboxDefense=.{};_=A.enableDefenses(&f);
 try std.testing.expectEqual(A.Status.eligible,A.previewPlantDefended(&f,0,0.5).status);try std.testing.expectEqual(@as(f32,0),v[0]);w[0]=0;t[0]=std.math.nan(f32);try std.testing.expectEqual(A.Status.invalid,A.plantDefended(&f,0,0.5).status);try std.testing.expectEqual(@as(f32,0),v[0]);
}
test "classic offspring exactly retains old thermal sequence and no mutation"{
 for(0..4096)|seed|{const parent=E.Plant{.optimum=299,.generation=4};try std.testing.expectEqualDeep(E.offspring(parent,seed),E.offspringWithDefense(parent,seed,.{}));}
}

test "preview and apply share existing fifty centimetre productive boundary"{
 var v=[_]f32{0};var w=[_]f32{0.0005};var t=[_]f32{295};var p=[_]E.Plant{.{}};var f=Fixture{.vegetation=&v,.waterMass=&w,.temperature=&t,.plantTraits=&p};_=A.enableDefenses(&f);
 try std.testing.expectEqual(A.Status.eligible,A.previewPlantDefended(&f,0,0.5).status);try std.testing.expectEqual(@as(f32,0),v[0]);
 w[0]=std.math.nextAfter(f32,w[0],std.math.inf(f32));try std.testing.expectEqual(A.Status.water,A.previewPlantDefended(&f,0,0.5).status);try std.testing.expectEqual(A.Status.water,A.plantDefended(&f,0,0.5).status);try std.testing.expectEqual(@as(f32,0),v[0]);
 w[0]=0.0005;try std.testing.expectEqual(A.Status.planted,A.plantDefended(&f,0,0.5).status);try std.testing.expectEqual(@as(f32,0.0005),w[0]);
}
