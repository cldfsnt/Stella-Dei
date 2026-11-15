//! Session-only receipt for actual exposed dead-carbon oxidation, never wildfire.
const std=@import("std");
pub const lifetime:f32=2.4;
pub const Cue=struct{world:u32,owner:usize,cell:usize,burned_carbon_kg:f64,temperature_delta:f64};
pub fn fromReceipt(receipt:anytype,world:u32,owner:usize) ?Cue {
 if(!receipt.success() or !std.math.isFinite(receipt.burned_carbon_kg) or receipt.burned_carbon_kg<=0 or !std.math.isFinite(receipt.temperature_delta) or receipt.temperature_delta<=0)return null;
 return .{.world=world,.owner=owner,.cell=receipt.cell,.burned_carbon_kg=receipt.burned_carbon_kg,.temperature_delta=receipt.temperature_delta};
}
pub fn visible(cue:Cue,remaining:f32,world:u32,owner:usize) bool{return cue.world==world and cue.owner==owner and std.math.isFinite(remaining) and remaining>0 and std.math.isFinite(cue.burned_carbon_kg) and cue.burned_carbon_kg>0 and std.math.isFinite(cue.temperature_delta) and cue.temperature_delta>0;}
pub fn fade(remaining:f32) f32{return if(std.math.isFinite(remaining)) std.math.clamp(remaining/lifetime,0,1) else 0;}
test "only successful funded heat receipts make a finite world-bound cue" {
 const R=struct{ok:bool=true,cell:usize=4,burned_carbon_kg:f64=2,temperature_delta:f64=1,pub fn success(self:@This())bool{return self.ok;}};
 const cue=fromReceipt(R{},7,9).?;try std.testing.expect(visible(cue,lifetime,7,9));
 try std.testing.expect(!visible(cue,0,7,9));try std.testing.expect(!visible(cue,lifetime,8,9));try std.testing.expect(!visible(cue,lifetime,7,10));
 try std.testing.expect(fromReceipt(R{.ok=false},7,9)==null);try std.testing.expect(fromReceipt(R{.burned_carbon_kg=0},7,9)==null);try std.testing.expect(fromReceipt(R{.temperature_delta=std.math.nan(f64)},7,9)==null);
 try std.testing.expectEqual(@as(f32,0.5),fade(lifetime/2));
}
