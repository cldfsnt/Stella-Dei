//! Only the browser's non-emissive Origin map in radial daylight has provably
//! empty bloom. Preserve the ordinary HDR path for every unsupported scene.
//! Contract: Normal clearSurface/mapContext RGB <= .96; RGB8 sky <= 1;
//! sun is a unit sphere scaled8000 at300000 along radial camera daylight.
//! Origin overlays are drawn after postprocessing. Any new HDR scene producer
//! must invalidate/update this guard rather than silently losing its bloom.
const std=@import("std");
pub fn canSkip(web:bool,origin:bool,normal_map:bool,radial_daylight:bool,orbit:bool,animals:usize,camera_radius:f32) bool {
    return web and origin and normal_map and radial_daylight and orbit and animals==0 and
        std.math.isFinite(camera_radius) and camera_radius>0 and camera_radius<250000;
}
test "only nonemissive radial Origin scene qualifies" {
    try std.testing.expect(canSkip(true,true,true,true,true,0,6000));
    try std.testing.expect(!canSkip(false,true,true,true,true,0,6000));
    try std.testing.expect(!canSkip(true,false,true,true,true,0,6000));
    try std.testing.expect(!canSkip(true,true,false,true,true,0,6000));
    try std.testing.expect(!canSkip(true,true,true,false,true,0,6000));
    try std.testing.expect(!canSkip(true,true,true,true,false,0,6000));
    try std.testing.expect(!canSkip(true,true,true,true,true,1,6000));
}
test "camera beyond safe sun separation and invalid geometry retain HDR" {
    for([_]f32{0,-1,250000,300000,std.math.inf(f32),std.math.nan(f32)})|distance|
        try std.testing.expect(!canSkip(true,true,true,true,true,0,distance));
}
