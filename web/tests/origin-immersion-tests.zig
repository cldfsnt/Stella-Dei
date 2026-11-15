const std=@import("std");const M=@import("microbes.zig");const R=@import("microbes_law1_reference.zig");
fn cohort() M.Cohort{return .{.biomass=0.1,.support_mass=0.004,.organization=0.04,.structure=0.1,.lineage=1};}
fn env(depth:f32) M.Environment{return .{.temperature=303,.depth_km=depth,.light=1,.carbon_available=1,.oxygen_carbon_capacity=1};}
fn run(c:M.Cohort,e:M.Environment) M.Cell {var cell=M.initialized(42);cell.cohorts[0]=c;_=M.step(&cell,e,1440);return cell;}
test "law1 actual step identical reference across depth temperature and roots" {
 for([_]f32{0,0.000001,0.0001,0.0002,0.01,0.051})|depth|{for([_]f32{260,273.15,303,355})|temp|{for([_]f32{0,0.25})|root|{
 var e=env(depth);e.temperature=temp;e.root_hydration=.{0.25,0,0,0};var c=cohort();c.root_fraction=root;const a=run(c,e);
 var b=R.initialized(42);inline for(std.meta.fields(M.Cohort))|f|{@field(b.cohorts[0],f.name)=@field(c,f.name);}var re:R.Environment=undefined;inline for(std.meta.fields(R.Environment))|f|{@field(re,f.name)=@field(e,f.name);}_=R.step(&b,re,1440);
 const ab=try std.json.stringifyAlloc(std.testing.allocator,a,.{});defer std.testing.allocator.free(ab);const bb=try std.json.stringifyAlloc(std.testing.allocator,b,.{});defer std.testing.allocator.free(bb);try std.testing.expectEqualStrings(ab,bb);
 }}}
}
test "immersion endpoints continuity zero height and finite guards" {
 const c=cohort();const h=M.producerHeightMeters(c)/1000;
 try std.testing.expectEqual(@as(f32,0),M.geometricImmersion(c,0,303));try std.testing.expectApproxEqAbs(@as(f32,0.5),M.geometricImmersion(c,h/2,303),0.000001);try std.testing.expectApproxEqAbs(@as(f32,1),M.geometricImmersion(c,h,303),0.000001);try std.testing.expectEqual(@as(f32,1),M.geometricImmersion(c,2*h,303));
 try std.testing.expectApproxEqAbs(M.geometricImmersion(c,h,303),M.geometricImmersion(c,std.math.nextAfter(f32,h,0),303),0.000001);
 var flat=c;flat.support_mass=0;try std.testing.expectEqual(@as(f32,0),M.geometricImmersion(flat,h,303));
 for([_]f32{0,273.15,355,std.math.nan(f32),std.math.inf(f32)})|t|try std.testing.expectEqual(@as(f32,0),M.geometricImmersion(c,h,t));
 for([_]f32{-1,0.051,std.math.nan(f32),std.math.inf(f32)})|d|try std.testing.expectEqual(@as(f32,0),M.geometricImmersion(c,d,303));
 var e=env(0);const old=run(c,e);e.immersion_physiology=true;try std.testing.expectEqualDeep(old,run(c,e));
 e=env(h);const old_flat=run(flat,e);e.immersion_physiology=true;try std.testing.expectEqualDeep(old_flat,run(flat,e));
}
test "fully immersed shallow response wet response without free resources or root credit" {
 const c=cohort();var shallow=env(0.0001);shallow.immersion_physiology=true;var wet=shallow;wet.depth_km=0.0002;
 // Light attenuation legitimately differs; darkness isolates wet mortality.
 shallow.light=0;wet.light=0;try std.testing.expectEqualDeep(run(c,wet),run(c,shallow));
 shallow.light=1;shallow.carbon_available=0;var cell=M.initialized(42);cell.cohorts[0]=c;const flux=M.step(&cell,shallow,1440);try std.testing.expectEqual(@as(f32,0),flux.fixed);try std.testing.expect(cell.cohorts[0].biomass<c.biomass);
 cell=M.initialized(42);cell.cohorts[0]=c;cell.nutrient=0;shallow.carbon_available=1;const nf=M.step(&cell,shallow,1440);try std.testing.expect(nf.fixed<=0.001); // recycling may fund small fixation; never free nutrient.
 const S=@import("shared_soil.zig");var rooted=c;rooted.root_fraction=0.25;cell=M.initialized(42);cell.cohorts[0]=rooted;const result=S.step(cell,1,1,1e9,shallow,1440,10,0).?;try std.testing.expectEqual(@as(f64,0),result.paid);try std.testing.expectEqual(@as(f32,0),result.h[0]);
}
