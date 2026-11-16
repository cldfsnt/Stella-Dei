const std=@import("std");const M=@import("simulation/microbes.zig");const C=@import("simulation/compact_microbes.zig");
fn validClock(clock:f32)bool{return std.math.isFinite(clock) and (clock == -1 or clock>=0);}
fn toCompact(c:M.Cohort)C.Cohort{var out:C.Cohort=.{};inline for(std.meta.fields(C.Cohort))|f|{if(comptime std.mem.eql(u8,f.name,"protective_clock"))out.protective_clock=if(c.protective_rest)c.protective_recovery else -1 else @field(out,f.name)=@field(c,f.name);}return out;}
fn decode(c:C.Cohort)!M.Cohort{if(!validClock(c.protective_clock))return error.InvalidClock;var out:M.Cohort=.{};inline for(std.meta.fields(M.Cohort))|f|{if(comptime std.mem.eql(u8,f.name,"protective_rest"))out.protective_rest=c.protective_clock>=0 else if(comptime std.mem.eql(u8,f.name,"protective_recovery"))out.protective_recovery=if(c.protective_clock>=0)c.protective_clock else 0 else @field(out,f.name)=@field(c,f.name);}return out;}
fn cellEqual(a:M.Cell,b:C.Cell)!void{try std.testing.expectEqual(a.nutrient,b.nutrient);try std.testing.expectEqual(a.detritus,b.detritus);try std.testing.expectEqual(a.rng,b.rng);for(a.cohorts,b.cohorts)|x,y|try std.testing.expectEqualDeep(x,try decode(y));}
fn env(e:M.Environment)C.Environment{var out:C.Environment=undefined;inline for(std.meta.fields(C.Environment))|f|@field(out,f.name)=@field(e,f.name);return out;}
test "sentinel exact domain and layout"{
 std.debug.print("LAYOUT old_cohort={} compact_cohort={} old_cell={} compact_cell={}\n",.{@sizeOf(M.Cohort),@sizeOf(C.Cohort),@sizeOf(M.Cell),@sizeOf(C.Cell)});
 try std.testing.expectEqual(@as(usize,96),@sizeOf(C.Cohort));try std.testing.expectEqual(@as(usize,400),@sizeOf(C.Cell));
 for([_]f32{-2,-0.5,-std.math.inf(f32),std.math.inf(f32),std.math.nan(f32)})|v|try std.testing.expectError(error.InvalidClock,decode(.{.protective_clock=v}));
 for([_]f32{-1,0,0.125,7199.5,7200,8640,std.math.floatMax(f32)})|v|{const c=C.Cohort{.protective_clock=v};try std.testing.expectEqualDeep(c,toCompact(try decode(c)));}
}
test "exact state flux RNG through entry fractional recovery extreme death and research JSON restart"{
 for([_]bool{false,true})|enabled|{M.qa_protection_enabled=enabled;C.qa_protection_enabled=enabled;
 for([_]f32{0,0.03125,0.5,1})|investment|for([_]f32{0.125,60,1440,7200})|dt|{
 var old=M.initialized(42);old.cohorts[0]=.{.biomass=0.02,.support_mass=0.005,.root_fraction=0.5,.organization=0.25,.lineage=1,.protective_investment=investment};var compact=C.initialized(42);compact.cohorts[0]=toCompact(old.cohorts[0]);
 for(0..180)|i|{const temp:f32=if(i<12)263 else if(i<90)298 else if(i<120)326 else if(i<150)297 else 240;const e=M.Environment{.temperature=temp,.depth_km=0.001,.light=1,.carbon_available=1,.oxygen_carbon_capacity=1,.immersion_physiology=true,.final_demand_physiology=true};const ce=env(e);
 try std.testing.expectEqual(M.protectBefore(&old,e,dt),C.protectBefore(&compact,ce,dt));const x=M.step(&old,e,dt);const y=C.step(&compact,ce,dt);inline for(std.meta.fields(M.Flux))|f|try std.testing.expectEqual(@field(x,f.name),@field(y,f.name));try cellEqual(old,compact);
 if(i==89){const bytes=try std.json.stringifyAlloc(std.testing.allocator,compact,.{});defer std.testing.allocator.free(bytes);const parsed=try std.json.parseFromSlice(C.Cell,std.testing.allocator,bytes,.{});defer parsed.deinit();try std.testing.expectEqualDeep(compact,parsed.value);compact=parsed.value;}
 }
 };}
}
test "actual paid child reset and inherited state semantic parity"{
 M.qa_protection_enabled=true;C.qa_protection_enabled=true;
 for([_]f32{0,0.03125,0.5,1})|investment|{var a=M.initialized(42);a.cohorts[0]=.{.biomass=0.1,.support_mass=0.025,.lineage=1,.reproduction_credit=0.1,.protective_investment=investment};var b=C.initialized(42);b.cohorts[0]=toCompact(a.cohorts[0]);var ad=M.initialized(43);var bd=C.initialized(43);var ast=M.Stats{.next_lineage=2};var bst=C.Stats{.next_lineage=2};try std.testing.expectEqual(M.propagate(&a,0,&ad,&ast),C.propagate(&b,0,&bd,&bst));try cellEqual(a,b);try cellEqual(ad,bd);inline for(std.meta.fields(M.Stats))|f|try std.testing.expectEqual(@field(ast,f.name),@field(bst,f.name));try std.testing.expectEqual(@as(f32,-1),bd.cohorts[0].protective_clock);}
}
test "resting partial-cohort movement preserves exact state and identity"{
 M.qa_protection_enabled=true;C.qa_protection_enabled=true;
 for([_]bool{false,true})|rest|{
 var a=[_]M.Cell{M.initialized(1),M.initialized(2)};a[0].cohorts[0]=.{.biomass=0.08,.support_mass=0.03,.organization=0.4,.feeding=0.5,.mobility=0.5,.lineage=1,.protective_investment=0.5,.protective_rest=rest,.protective_recovery=if(rest)123.125 else 0};a[1].cohorts[0]=.{.biomass=0.2,.lineage=2};var b=[_]C.Cell{C.initialized(1),C.initialized(2)};for(0..2)|i|for(0..4)|j|{b[i].cohorts[j]=toCompact(a[i].cohorts[j]);};const e=M.Environment{.temperature=298,.depth_km=0.001,.light=1,.carbon_available=1,.oxygen_carbon_capacity=1};const ce=env(e);
 const x=M.relocate(&a,0,0,e,&.{.{.index=1,.environment=e}},86400000,1);const y=C.relocate(&b,0,0,ce,&.{.{.index=1,.environment=ce}},86400000,1);try std.testing.expect(x.moved);inline for(std.meta.fields(M.Movement))|f|try std.testing.expectEqual(@field(x,f.name),@field(y,f.name));for(0..2)|i|try cellEqual(a[i],b[i]);
 }
}
