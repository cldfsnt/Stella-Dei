const std=@import("std");
const M=@import("simulation/microbes.zig");
const T=@import("manual_transport.zig");
// Exact rows from the actual 40,962-cell Planet graph, enum/getNeighbours order.
const pentagon=[_]usize{10242,10244,11826,30746,30748,0};
const hexagon=[_]usize{10350,10352,10866,10868,12035,12726};
const P=struct{
 worldMode:M.Mode=.origin,microbeCells:[]M.Cell,microbeStats:M.Stats=.{},
 waterMass:[]f32,temperature:[]f32,elevation:[]f32,row:[6]usize=pentagon,
 pub fn getNeighbours(self:*@This(),_:usize)[6]usize{return self.row;}
 pub fn getKmPerWaterMass(_: *@This())f32{return 0.001;}
};
const S=struct{planet:P,paused:bool=true,gameTime:f64=123,selectedPoint:usize=0};
test "actual pentagon and hexagon options preserve state and RNG; duplicate self invalid targets excluded"{
 const a=std.testing.allocator;const cells=try a.alloc(M.Cell,40962);defer a.free(cells);
 for(cells,0..)|*c,i|c.*=M.initialized(i+1);
 const water=try a.alloc(f32,cells.len);defer a.free(water);@memset(water,5);
 const temp=try a.alloc(f32,cells.len);defer a.free(temp);@memset(temp,303);
 const elevation=try a.alloc(f32,cells.len);defer a.free(elevation);@memset(elevation,0);
 const before=try a.dupe(M.Cell,cells);defer a.free(before);
 var s=S{.planet=.{.microbeCells=cells,.waterMass=water,.temperature=temp,.elevation=elevation}};
 T.reset();defer T.reset();
 const cases=[_]struct{cell:usize,row:[6]usize,want:[]const usize}{
 .{.cell=0,.row=pentagon,.want=pentagon[0..5]},
 .{.cell=12,.row=hexagon,.want=&hexagon},
 .{.cell=0,.row=.{0,10242,10242,40962,10244,0},.want=&.{10242,10244}},
 .{.cell=0,.row=.{0,0,0,0,0,0},.want=&.{}},
 };
 for(cases)|c|{
 s.selectedPoint=c.cell;s.planet.row=c.row;const snapshot=s;
 const parsed=try std.json.parseFromSlice(std.json.Value,a,T.options(&s,7),.{.allocate=.alloc_always});defer parsed.deinit();
 const rows=parsed.value.object.get("neighbors").?.array.items;
 try std.testing.expectEqual(c.want.len,rows.len);
 for(rows,c.want)|r,n|try std.testing.expectEqual(@as(i64,@intCast(n)),r.object.get("cell").?.integer);
 try std.testing.expectEqualDeep(snapshot,s);try std.testing.expectEqualDeep(before,cells);
 for(water,temp,elevation)|w,t,e|{try std.testing.expectEqual(@as(f32,5),w);try std.testing.expectEqual(@as(f32,303),t);try std.testing.expectEqual(@as(f32,0),e);}
 }
}
