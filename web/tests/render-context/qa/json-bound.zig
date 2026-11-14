const std=@import("std");const PerformanceDetails=@import("candidate/src/performance_details.zig");
pub fn main() !void {
 const max=std.math.floatMax(f64);const state=.{.planet=.{.transformedPoints=[_]u8{0}}};
 var sample=PerformanceDetails.Sample{.frames=60,.ticks=120,.physics_frames=60,.long_frames=60,.frame_p95=max,.frame_sum=max,.frame_max=max,.physics_sum=max,.physics_max=max,.render_sum=max,.render_max=max,.stage_sum=.{max}**4,.stage_max=.{max}**4};_=&sample;
 PerformanceDetails.metrics.enabled=true;PerformanceDetails.metrics.context=.{.valid=true,.world="sandbox",.map="WindMagnitude",.canvas_width=2147483647,.canvas_height=2147483647,.scene_width=2147483647,.scene_height=2147483647,.bloom_active=true,.bloom_passes=5,.animals=std.math.maxInt(usize),.camera_radius=std.math.floatMax(f32),.planet_radius=std.math.floatMax(f32),.camera_valid=true};
 var performance_json:[2048]u8=undefined;var stream=std.io.fixedBufferStream(&performance_json);
    std.json.stringify(.{.enabled=PerformanceDetails.metrics.enabled,.cells=state.planet.transformedPoints.len,.frames=sample.frames,.ticks=sample.ticks,.physics_frames=sample.physics_frames,
      .frame_avg_ms=sample.frame_sum/@max(@as(f64,@floatFromInt(sample.frames)),1),.frame_max_ms=sample.frame_max,.frame_p95_ms=sample.frame_p95,.long_frames=sample.long_frames,
      .physics_avg_ms=sample.physics_sum/@max(@as(f64,@floatFromInt(sample.physics_frames)),1),.physics_max_ms=sample.physics_max,
      .render_cpu_avg_ms=sample.render_sum/@max(@as(f64,@floatFromInt(sample.frames)),1),.render_cpu_max_ms=sample.render_max,.render_context=PerformanceDetails.metrics.context,.stage_sum_ms=sample.stage_sum,.stage_max_ms=sample.stage_max},.{},stream.writer()) catch return error.SerializationFailed;

 std.debug.assert(stream.pos<performance_json.len);const parsed=try std.json.parseFromSlice(std.json.Value,std.heap.page_allocator,performance_json[0..stream.pos],.{});defer parsed.deinit();std.debug.assert(parsed.value.object.get("render_context")!=null);
 std.debug.print("PERFORMANCE_JSON_WORST_FINITE bytes={d} capacity={d} parsed=true\n",.{stream.pos,performance_json.len});
}
