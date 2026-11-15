const std=@import("std");const M=@import("simulation/microbes.zig");
// Illustrative wrapper layout, not a committed production state design.
const ProposedCohort=struct{current:M.Cohort,retention:f32=0,stored_water:f64=0};
const ProposedCell=struct{cohorts:[4]ProposedCohort,nutrient:f32,detritus:f32,rng:u64,liquid_return:f64=0,vapor_return:f64=0};
pub fn main()void{
 std.debug.print("current_cohort={d} current_cell={d} illustrative_cohort={d} illustrative_cell={d}\n",.{@sizeOf(M.Cohort),@sizeOf(M.Cell),@sizeOf(ProposedCohort),@sizeOf(ProposedCell)});
 for([_]usize{40962,163842})|n|std.debug.print("cells={d} illustrative_extra_bytes={d}\n",.{n,n*(@sizeOf(ProposedCell)-@sizeOf(M.Cell))});
}
