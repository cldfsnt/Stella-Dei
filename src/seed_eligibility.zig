//! Read-only predicate used by seed action, UI and discovery.
const std=@import("std");
const Microbes=@import("simulation/microbes.zig");
pub const Reason=enum{eligible,invalid,too_dry,too_deep,too_cold,too_hot,no_space,no_nutrients,no_carbon};
/// Current eligibility always wins over transient, possibly stale focus feedback.
pub fn reasonText(reason:Reason) []const u8 {
 return switch(reason) {
  .eligible=>"Can seed: tap a green + target",
  .invalid=>"Cannot seed: choose a valid patch",
  .too_dry=>"Too dry: add water or find a green +",
  .too_deep=>"Too deep: drain water to 0.2–50m",
  .too_cold=>"Frozen: warm above 0°C before seeding",
  .too_hot=>"Too hot: cool this habitat first",
  .no_space=>"Patch full: choose another green +",
  .no_nutrients=>"No nutrients: use Nutr. + first",
  .no_carbon=>"No carbon: habitat cannot seed now",
 };
}
pub fn displayHint(reason:Reason,feedback:[]const u8,targets_visible:bool)[]const u8{
 if(targets_visible)return seedHint(reason,feedback);
 return switch(reason){.eligible=>"Seed hints hidden: tap terrain or use Seed colony",.too_dry=>"Too dry: add water or Find habitat",.no_space=>"Patch full: select another patch",else=>reasonText(reason)};
}
test "hidden seed hints retain current eligibility without invisible target directions"{
 try std.testing.expectEqualStrings("Seed hints hidden: tap terrain or use Seed colony",displayHint(.eligible,"Tap closer to a green + or use Seed colony",false));
 try std.testing.expectEqualStrings("Patch full: select another patch",displayHint(.no_space,"",false));
 try std.testing.expectEqualStrings("Too dry: add water or Find habitat",displayHint(.too_dry,"",false));
 for(std.enums.values(Reason))|reason|try std.testing.expectEqualStrings(seedHint(reason,""),displayHint(reason,"",true));
}
pub fn seedHint(reason:Reason, feedback:[]const u8) []const u8 {
 if(reason==.eligible and std.mem.eql(u8,feedback,"Tap closer to a green + or use Seed colony"))return feedback;
 return reasonText(reason);
}
test "current invalid seed status overrides stale success or focus feedback" {
 try std.testing.expectEqualStrings("Too dry: add water or find a green +",seedHint(.too_dry,"Can seed here: Seed colony adds existing life"));
 try std.testing.expectEqualStrings("Patch full: choose another green +",seedHint(.no_space,"Colony seeded. Light and resources drive growth"));
 try std.testing.expectEqualStrings("Can seed: tap a green + target",seedHint(.eligible,"Too dry"));
 try std.testing.expectEqualStrings("Tap closer to a green + or use Seed colony",seedHint(.eligible,"Tap closer to a green + or use Seed colony"));
 try std.testing.expectEqualStrings("Too dry: add water or find a green +",seedHint(.too_dry,"Tap closer to a green + or use Seed colony"));
}
pub fn evaluate(cell:Microbes.Cell,depth:f32,temp:f32,carbon:f32) Reason {
 if(!std.math.isFinite(depth) or !std.math.isFinite(temp) or !std.math.isFinite(carbon) or !std.math.isFinite(cell.nutrient))return .invalid;
 if(depth<0.0002)return .too_dry;if(depth>0.05)return .too_deep;
 if(temp<=273.15)return .too_cold;if(temp>=355)return .too_hot;
 var space=false;for(cell.cohorts)|c|{if(!std.math.isFinite(c.biomass))return .invalid;if(c.biomass==0)space=true;}
 if(!space)return .no_space;if(cell.nutrient<=0)return .no_nutrients;if(carbon<=0)return .no_carbon;
 return .eligible;
}
test "eligibility matches seed resource and habitat boundaries without mutation" {
 var cell=Microbes.Cell{};cell.nutrient=0.01;var stats=Microbes.Stats{};
 try std.testing.expectEqual(Reason.eligible,evaluate(cell,0.0002,300,1));
 try std.testing.expectEqual(Reason.too_dry,evaluate(cell,0,300,1));
 try std.testing.expectEqual(Reason.too_deep,evaluate(cell,0.051,300,1));
 try std.testing.expectEqual(Reason.too_cold,evaluate(cell,0.001,260,1));
 try std.testing.expectEqual(Reason.too_hot,evaluate(cell,0.001,355,1));
 try std.testing.expectEqual(Reason.no_carbon,evaluate(cell,0.001,300,0));
 cell.nutrient=0;try std.testing.expectEqual(Reason.no_nutrients,evaluate(cell,0.001,300,1));cell.nutrient=0.01;
 for(0..4)|_|{try std.testing.expectEqual(Reason.eligible,evaluate(cell,0.001,300,1));try std.testing.expect(Microbes.seed(&cell,&stats,1)>0);}
 try std.testing.expectEqual(Reason.no_space,evaluate(cell,0.001,300,1));
 try std.testing.expectEqual(Reason.invalid,evaluate(cell,std.math.nan(f32),300,1));
}

test "frozen seedlings never advertised eligible at boundary" {
 const cell=Microbes.Cell{};const before=cell;
 for([_]f32{260,273,273.15})|temp|try std.testing.expectEqual(Reason.too_cold,evaluate(cell,0.001,temp,1));
 try std.testing.expectEqual(Reason.eligible,evaluate(cell,0.001,273.16,1));
 try std.testing.expectEqualDeep(before,cell);
}
