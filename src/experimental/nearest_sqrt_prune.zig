//! Isolated exact-metric experiment; no persistent geometry/cache state.
const std=@import("std");
pub fn nearest(points:anytype,position:anytype)usize {
    var best_distance:f32=std.math.inf(f32);
    var best_squared:f32=std.math.inf(f32);
    var best:usize=undefined; // Same undefined domain as original: no finite winner.
    for(points,0..)|point,i|{
        const delta=point.sub(position);
        const squared=delta.dot(delta);
        if(squared>=best_squared)continue;
        const distance=@sqrt(squared);
        if(distance<best_distance){best=i;best_distance=distance;best_squared=squared;}
    }
    return best;
}
pub fn reference(points:anytype,position:anytype)usize {
    var best_distance:f32=std.math.inf(f32);var best:usize=undefined;
    for(points,0..)|point,i|{const distance=point.distance(position);if(distance<best_distance){best=i;best_distance=distance;}}
    return best;
}
