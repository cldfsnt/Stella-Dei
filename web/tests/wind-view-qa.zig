const std=@import("std");const V=@import("wind_view.zig");const M=@import("simulation/microbes.zig");const G=@import("simulation/wind_genetics.zig");
const State=struct{selectedPoint:usize=0,planet:struct{windDispersal:G.Config=.{},worldMode:enum{origin,sandbox}=.origin,microbeCells:[]M.Cell}};
test "read only exact world writer and selected trait identity" {
 var cells=[_]M.Cell{.{}};cells[0].cohorts[0]=.{.biomass=0.02,.lineage=18446744073709551614,.aerial_allocation=0.5};
 var state=State{.planet=.{.microbeCells=&cells}};
 const before=state;const cell_before=cells;
 const a=V.snapshot(@as(?*State,&state),19);try std.testing.expect(std.mem.indexOf(u8,std.mem.span(a),"\"writer_version\":7")!=null);
 state.planet.windDispersal=.{.enabled=true,.law=1};
 const b=V.snapshot(@as(?*State,&state),20);try std.testing.expect(std.mem.indexOf(u8,std.mem.span(b),"18446744073709551614")!=null);try std.testing.expect(std.mem.indexOf(u8,std.mem.span(b),"\"writer_version\":11")!=null);
 state.planet.worldMode=.sandbox;try std.testing.expectEqual(@as(u32,0),V.writerVersion(&state));
 const n=V.snapshot(@as(?*State,null),21);try std.testing.expect(std.mem.indexOf(u8,std.mem.span(n),"\"world_serial\":21")!=null);
 state=before;try std.testing.expectEqualDeep(cell_before,cells);
}
