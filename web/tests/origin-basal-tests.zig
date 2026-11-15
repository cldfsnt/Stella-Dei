test "fixed density sensitivity and continuous support/root boundaries" {
 const G=@import("basal_geometry.zig");
 for([_]f64{10,100,1000})|density|{
  const b:f64=0.1;const basal=b/density;
  try std.testing.expectEqual(basal,G.height(b,0,density).?);
  for([_]f64{0,0.5,1,2})|fraction|{
   const i=G.immersion(b,0,basal*fraction,density).?;
   try std.testing.expectEqual(@min(fraction,1),i);try std.testing.expectEqual(@as(f64,1),i+(1-i));
  }
  const arch:f64=0.02;try std.testing.expectEqual(arch,G.height(b,arch,density).?);
  try std.testing.expectApproxEqAbs(basal,G.height(b,std.math.nextAfter(f64,basal,0),density).?,1e-15);
  try std.testing.expectApproxEqAbs(basal,G.height(b,std.math.nextAfter(f64,basal,std.math.inf(f64)),density).?,1e-15);
  var c=cohort();c.support_mass=0;const flat=G.immersion(c.biomass,M.producerHeightMeters(c),0.0001,density).?;
  for([_]f32{std.math.nextAfter(f32,0,1),1e-12})|support|{c.support_mass=support;try std.testing.expectEqual(flat,G.immersion(c.biomass,M.producerHeightMeters(c),0.0001,density).?);}
  c=cohort();c.root_fraction=1;const allroot=G.immersion(c.biomass,M.producerHeightMeters(c),0.0001,density).?;c.root_fraction=std.math.nextAfter(f32,1,0);try std.testing.expectEqual(allroot,G.immersion(c.biomass,M.producerHeightMeters(c),0.0001,density).?);
  std.debug.print("BASAL density={d} biomass=.1 height_m={d} immersion_0.1mm={d}\n",.{density,basal,flat});
 }
 try std.testing.expect(G.height(0,0,100)==null);try std.testing.expect(G.height(std.math.nan(f64),0,100)==null);try std.testing.expect(G.height(1,0,0)==null);
}
test "basal physiology respects no carbon darkness nutrient accounting and root source" {
 var c=cohort();c.support_mass=0;c.structure=0;var e=env(0.0001);e.immersion_physiology=true;
 for([_]f32{0,1})|light|{var cell=M.initialized(42);cell.cohorts[0]=c;e.light=light;e.carbon_available=0;const f=M.step(&cell,e,1440);try std.testing.expectEqual(@as(f32,0),f.fixed);try std.testing.expect(M.biomass(cell)<c.biomass);}
 var cell=M.initialized(42);cell.cohorts[0]=c;cell.nutrient=0;e.carbon_available=1;e.light=1;const f=M.step(&cell,e,1440);
 // Initial live N plus mineral N: recycling can feed photosynthesis but cannot create N.
 try std.testing.expect(cell.nutrient+M.biomass(cell)*M.nutrient_per_carbon<=c.biomass*M.nutrient_per_carbon+1e-7);try std.testing.expect(f.fixed>=0);
 const S=@import("shared_soil.zig");c=cohort();c.root_fraction=1;cell=M.initialized(42);cell.cohorts[0]=c;e.depth_km=0.0001;const wet=S.step(cell,1,1,1e9,e,1440,10,0).?;try std.testing.expectEqual(@as(f64,0),wet.paid);
 e.depth_km=0;const empty=S.step(cell,0,1,1e9,e,1440,10,0).?;try std.testing.expectEqual(@as(f64,0),empty.paid);try std.testing.expectEqual(@as(f32,0),empty.h[0]);
 for([_]f32{273.15,355})|t|{e.temperature=t;const cold=S.step(cell,1,1,1e9,e,1440,10,0).?;try std.testing.expectEqual(@as(f64,0),cold.paid);}
}
