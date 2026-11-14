//! NEW WORLD initial-condition planning only; never drains an existing save.
//! No atmosphere, temperatures, terrain, organisms or runtime rates are changed.
const std=@import("std");
pub const Plan=struct{
 sea_level:f32,
 requested_ocean_fraction:f32,
 ocean_cells:usize,
 cell_count:usize,
 initial_mass:f64, // sum of exactly representable f32 engine water masses
 pub fn massAt(self:Plan,elevation:f32,km_per_mass:f32) f32{
  return @max(0,self.sea_level-elevation)/km_per_mass;
 }
 pub fn oceanFraction(self:Plan) f64{return @as(f64,@floatFromInt(self.ocean_cells))/@as(f64,@floatFromInt(self.cell_count));}
};
pub fn plan(allocator:std.mem.Allocator,elevation:[]const f32,km_per_mass:f32,ocean_fraction:f32) !Plan {
 if(elevation.len==0 or !std.math.isFinite(km_per_mass) or km_per_mass<=0 or !std.math.isFinite(ocean_fraction) or ocean_fraction<=0 or ocean_fraction>=1)return error.InvalidInitialInventory;
 for(elevation)|height|if(!std.math.isFinite(height))return error.InvalidInitialInventory;
 const sorted=try allocator.dupe(f32,elevation);defer allocator.free(sorted);
 std.mem.sort(f32,sorted,{},std.sort.asc(f32));
 const rank:usize=@intFromFloat(@floor(@as(f64,ocean_fraction)*@as(f64,@floatFromInt(sorted.len-1))));
 var result=Plan{.sea_level=sorted[rank],.requested_ocean_fraction=ocean_fraction,.ocean_cells=0,.cell_count=elevation.len,.initial_mass=0};
 for(elevation)|height|{
  const mass=result.massAt(height,km_per_mass);
  if(!std.math.isFinite(mass))return error.InvalidInitialInventory;
  if(mass>0)result.ocean_cells+=1;
  result.initial_mass+=mass;
 }
 if(!std.math.isFinite(result.initial_mass))return error.InvalidInitialInventory;
 return result;
}
test "continents plan sets explicit initial inventory without altering supplied terrain" {
 const heights=[_]f32{10,1,8,3,7,5,9,0,4,2,6};const original=heights;
 const p=try plan(std.testing.allocator,&heights,0.25,0.7);
 try std.testing.expectEqualSlices(f32,&original,&heights);
 try std.testing.expectEqual(@as(f32,6),p.sea_level); // f32 0.7 is just below exact7/10
 var sum:f64=0;var wet:usize=0;
 for(heights)|h|{const mass=p.massAt(h,0.25);sum+=mass;if(mass>0)wet+=1;try std.testing.expect(mass>=0);}
 try std.testing.expectEqual(sum,p.initial_mass);try std.testing.expectEqual(wet,p.ocean_cells);
 try std.testing.expect(p.oceanFraction()<=0.7);
}
test "ties report actual coverage rather than inventing land or deleting water later" {
 const p=try plan(std.testing.allocator,&.{1,1,1,1,1},1,0.7);
 try std.testing.expectEqual(@as(usize,0),p.ocean_cells);try std.testing.expectEqual(@as(f64,0),p.initial_mass);
}
test "invalid inventory plans reject before producing a world" {
 try std.testing.expectError(error.InvalidInitialInventory,plan(std.testing.allocator,&.{},1,0.7));
 try std.testing.expectError(error.InvalidInitialInventory,plan(std.testing.allocator,&.{1,2},0,0.7));
 try std.testing.expectError(error.InvalidInitialInventory,plan(std.testing.allocator,&.{1,std.math.nan(f32)},1,0.7));
 try std.testing.expectError(error.InvalidInitialInventory,plan(std.testing.allocator,&.{1,2},1,1));
}
