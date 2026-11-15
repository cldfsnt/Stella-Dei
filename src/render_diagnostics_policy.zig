//! Per-draw NanoVG GL error polling is diagnostic, not shader validation.
//! Native retains its historical checks; web diagnostic builds opt in explicitly.
pub fn nanoVGDebug(is_web:bool,web_opt_in:bool)bool{return !is_web or web_opt_in;}
test "native diagnostics preserved and web polling explicitly opt in" {
    const std=@import("std");
    try std.testing.expect(nanoVGDebug(false,false));
    try std.testing.expect(nanoVGDebug(false,true));
    try std.testing.expect(!nanoVGDebug(true,false));
    try std.testing.expect(nanoVGDebug(true,true));
}
