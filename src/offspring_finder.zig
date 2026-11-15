//! Direct living offspring only; no reconstructed genealogy or simulation writes.
const std=@import("std");const M=@import("simulation/microbes.zig");
pub const Search=struct{scan:@import("detritus_finder.zig").Scanner=.{},world:u32=0,parent:u64=0,time:f64=0};
pub fn alive(c:M.Cohort)bool{return c.lineage>0 and std.math.isFinite(c.biomass) and c.biomass>0;}
pub fn parentPresent(cell:M.Cell,id:u64)bool{if(id==0)return false;for(cell.cohorts)|c|if(alive(c) and c.lineage==id)return true;return false;}
pub fn child(cell:M.Cell,id:u64)?u64{if(id==0)return null;for(cell.cohorts)|c|if(alive(c) and c.parent==id and c.lineage!=id)return c.lineage;return null;}
pub fn parseId(text:[]const u8)?u64{if(text.len==0 or text.len>20 or text[0]=='0')return null;for(text)|c|if(c<'0' or c>'9')return null;return std.fmt.parseInt(u64,text,10) catch null;}
test "exact direct offspring ignores dominance unrelated dead and invalid cohorts"{var c=M.Cell{};c.cohorts[0]=.{.lineage=9,.parent=8,.biomass=1};c.cohorts[1]=.{.lineage=18446744073709551614,.parent=9007199254740993,.biomass=0.01};try std.testing.expectEqual(@as(?u64,18446744073709551614),child(c,9007199254740993));try std.testing.expect(child(c,9)==null);c.cohorts[1].biomass=std.math.nan(f32);try std.testing.expect(child(c,9007199254740993)==null);c.cohorts[0].biomass=0;try std.testing.expect(!parentPresent(c,9));}
test "IDs remain exact and malformed IDs refuse"{try std.testing.expectEqual(@as(?u64,9007199254740993),parseId("9007199254740993"));for([_] []const u8{"0","01","-1","1.0","18446744073709551616",""})|s|try std.testing.expect(parseId(s)==null);}
