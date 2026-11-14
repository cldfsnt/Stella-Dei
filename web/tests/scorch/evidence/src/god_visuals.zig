//! Read-only visual contract for successful bounded intervention receipts.
const std=@import("std");
const Actions=@import("god_actions.zig");
pub const lifetime:f32=1.2;
pub fn visible(receipt:Actions.Receipt,remaining:f32) bool {
    if(!std.math.isFinite(remaining) or remaining<=0 or !receipt.success() or receipt.count>receipt.affected.len)return false;
    for(receipt.affected[0..receipt.count]) |delta| {
        if(receipt.kind==.wave and std.math.isFinite(delta.water_mass) and delta.water_mass!=0)return true;
        if(receipt.kind==.scorch and std.math.isFinite(delta.cover_removed) and delta.cover_removed>0 and std.math.isFinite(delta.temperature_k) and delta.temperature_k>0)return true;
        if(receipt.kind==.lightning and std.math.isFinite(delta.temperature_k) and delta.temperature_k>0)return true;
    }
    return false;
}
pub fn fade(remaining:f32) f32 {return if(std.math.isFinite(remaining)) std.math.clamp(remaining/lifetime,0,1) else 0;}
test "failed empty expired or unchanged receipts cannot animate" {
    var r=Actions.Receipt{.kind=.wave,.count=1};
    try std.testing.expect(!visible(r,lifetime));
    r.affected[0].water_mass=-0.1;try std.testing.expect(visible(r,lifetime));
    r.failure=.dry;try std.testing.expect(!visible(r,lifetime));
    r.failure=.none;try std.testing.expect(!visible(r,0));try std.testing.expect(!visible(r,std.math.nan(f32)));
    r.count=0;try std.testing.expect(!visible(r,lifetime));r.count=8;try std.testing.expect(!visible(r,lifetime));
}
test "localized heat visuals require actual positive delta and fade once" {
    var r=Actions.Receipt{.kind=.lightning,.count=1};r.affected[0].temperature_k=40;
    try std.testing.expect(visible(r,lifetime));r.affected[0].temperature_k=0;try std.testing.expect(!visible(r,lifetime));
    try std.testing.expectEqual(@as(f32,1),fade(lifetime));try std.testing.expectEqual(@as(f32,0.5),fade(0.6));try std.testing.expectEqual(@as(f32,0),fade(0));
}

test "scorch scar requires actual destruction and heat" {var r=Actions.Receipt{.kind=.scorch,.count=1};try std.testing.expect(!visible(r,lifetime));r.affected[0].cover_removed=0.5;try std.testing.expect(!visible(r,lifetime));r.affected[0].temperature_k=40;try std.testing.expect(visible(r,lifetime));r.failure=.wet;try std.testing.expect(!visible(r,lifetime));}
