//! Read-only description of actual producer physiology; not a growth guarantee.
const std=@import("std");const M=@import("simulation/microbes.zig");
pub const State=enum{unknown,dry,frozen,too_hot,too_deep,thin_film,submergence_margin,aquatic};
pub const Snapshot=struct{state:State,living:usize=0,compatible:usize=0,supported_film_capable:usize=0,max_habitat_factor:f32=0};
pub fn inspect(cell:M.Cell,depth:f32,temp:f32)Snapshot{
 var s:Snapshot=.{.state=if(!std.math.isFinite(depth) or !std.math.isFinite(temp)) .unknown else if(temp<=273.15) .frozen else if(temp>=355) .too_hot else if(depth<=0) .dry else if(depth>0.05) .too_deep else if(depth<=0.00015) .thin_film else if(depth<0.0002) .submergence_margin else .aquatic};
 for(cell.cohorts)|c|{if(c.biomass<=0)continue;s.living+=1;const f=M.photosyntheticHabitat(c,depth,temp);s.max_habitat_factor=@max(s.max_habitat_factor,f);if(f>0){s.compatible+=1;if(depth<0.0002 and M.filmProtection(c)>0)s.supported_film_capable+=1;}}
 return s;
}
test "actual tissue and water determine film feedback without mutation"{
 var c=M.initialized(4);c.cohorts[0]=.{.biomass=0.02,.lineage=1,.structure=0.2};const before=c;
 try std.testing.expectEqual(@as(usize,0),inspect(c,0.0001,300).compatible);try std.testing.expectEqualDeep(before,c);
 c.cohorts[0].support_mass=0.002;const paid=c;const s=inspect(c,0.0001,300);
 try std.testing.expectEqual(State.thin_film,s.state);try std.testing.expectEqual(@as(usize,1),s.compatible);try std.testing.expectEqual(@as(usize,1),s.supported_film_capable);try std.testing.expect(s.max_habitat_factor>0 and s.max_habitat_factor<1);try std.testing.expectEqualDeep(paid,c);
 for([_]f32{0,0.0001,0.001})|depth|{try std.testing.expectEqual(@as(usize,0),inspect(c,depth,273.15).compatible);try std.testing.expectEqual(State.frozen,inspect(c,depth,273.15).state);}
 try std.testing.expectEqual(@as(usize,0),inspect(c,0,300).compatible);
 try std.testing.expectEqual(@as(usize,0),inspect(c,0.051,300).compatible);
}
test "submergence margin does not falsely claim inherited support"{
 var c=M.initialized(1);c.cohorts[0]=.{.biomass=0.02,.lineage=1};const s=inspect(c,0.00019,300);try std.testing.expectEqual(State.submergence_margin,s.state);try std.testing.expectEqual(@as(usize,1),s.compatible);try std.testing.expectEqual(@as(usize,0),s.supported_film_capable);
}

/// Capability is current inherited investment AND actual paid tissue, not a
/// lineage milestone. Compatibility permits photosynthesis, not net growth.
pub const LivingTraits=struct{
    film_potential:bool,
    film_compatible_now:bool,
    habitat_factor:f32,
};
pub fn livingTraits(c:M.Cohort,depth:f32,temp:f32)LivingTraits{
    const potential=std.math.isFinite(c.biomass) and std.math.isFinite(c.support_mass) and std.math.isFinite(c.structure) and M.filmProtection(c)>0;
    const factor=M.photosyntheticHabitat(c,depth,temp);
    return .{.film_potential=potential,.film_compatible_now=potential and depth>0 and depth<=0.00015 and factor>0,.habitat_factor=factor};
}
test "living trait capability is reversible, read only, and not a growth claim" {
    var c:M.Cohort=.{.biomass=0.02,.lineage=1,.structure=0.2};
    try std.testing.expect(!livingTraits(c,0.0001,300).film_potential);
    c.support_mass=0.002; const before=c;
    try std.testing.expect(livingTraits(c,0.005,300).film_potential);
    try std.testing.expect(!livingTraits(c,0.005,300).film_compatible_now);
    try std.testing.expect(livingTraits(c,0.00015,300).film_compatible_now);
    try std.testing.expect(!livingTraits(c,0.000151,300).film_compatible_now);
    try std.testing.expect(!livingTraits(c,0.0002,300).film_compatible_now);
    try std.testing.expect(!livingTraits(c,0,300).film_compatible_now);
    try std.testing.expect(!livingTraits(c,0.0001,273.15).film_compatible_now);
    try std.testing.expectEqualDeep(before,c);
    c.structure=0;try std.testing.expect(!livingTraits(c,0.0001,300).film_potential);
    c.structure=0.2;c.support_mass=0;try std.testing.expect(!livingTraits(c,0.0001,300).film_potential);
}
