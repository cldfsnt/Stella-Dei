#!/usr/bin/env python3
"""Isolated real nursery update/render timings; production source unchanged."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-nursery-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text()
s=s.replace('    originReport("seeded",state);','    originReport("seeded",state);\n    try profileFrames("early",state,window,allocator);',1)
s=s.replace('        try originSaveCheck(state,allocator);','        try profileFrames("established30d",state,window,allocator);\n        try originSaveCheck(state,allocator);',1)
s+=r'''
fn profileFrames(label:[]const u8,state:anytype,window:anytype,allocator:std.mem.Allocator)!void{
 const saves=@import("save_game.zig");const perf=@import("performance_details.zig");
 var arena=std.heap.ArenaAllocator.init(allocator);defer arena.deinit();const a=arena.allocator();
 const bytes=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
 const frozen=try std.json.parseFromSlice(saves.schema.Save,a,bytes,.{.allocate=.alloc_always});
 var occupied:usize=0;var cohorts:usize=0;for(state.planet.microbeCells)|cell|{if(@import("simulation/microbes.zig").biomass(cell)>0)occupied+=1;for(cell.cohorts)|c|{if(c.biomass>0)cohorts+=1;}}
 std.debug.print("FRAME_PLATFORM renderer={s} version={s}\n",.{std.mem.span(gl.getString(gl.RENDERER).?),std.mem.span(gl.getString(gl.VERSION).?)});
 for([_]f32{0,21600,86400})|speed|{
  try saves.apply(state,frozen.value);state.paused=speed==0;state.timeScale=speed;state.simulationClock.reset();state.pointerOnPlanet=false;
  // Warm up shader/render caches before recording; screenshot shim's first12 frames excluded.
  for(0..12)|_|{state.update(&game,1.0/60.0);render(window);gl.finish();window.swapBuffers();}
  perf.metrics.setEnabled(true);const start_time=state.gameTime;
  var total_update:f64=0;var total_render:f64=0;var total_frame:f64=0;var max_frame:f64=0;var frames:[60]f64=undefined;var ticks:usize=0;
  for(0..60)|i|{
   var timer=try std.time.Timer.start();state.update(&game,1.0/60.0);const update_ms=@as(f64,@floatFromInt(timer.lap()))/1e6;
   render(window);gl.finish();const render_ms=@as(f64,@floatFromInt(timer.lap()))/1e6;window.swapBuffers();const swap_ms=@as(f64,@floatFromInt(timer.lap()))/1e6;
   const frame_ms=update_ms+render_ms+swap_ms;total_update+=update_ms;total_render+=render_ms;total_frame+=frame_ms;max_frame=@max(max_frame,frame_ms);frames[i]=frame_ms;ticks+=state.simulationStepsLastFrame;
   std.debug.print("FRAME_PROFILE stage={s} requested_hps={d} frame={d} ticks={d} update_ms={d:.4} render_finish_ms={d:.4} swap_ms={d:.4} total_ms={d:.4}\n",.{label,speed/3600,i,state.simulationStepsLastFrame,update_ms,render_ms,swap_ms,frame_ms});
  }
  const physics=perf.metrics.sample();const context=perf.metrics.context;
  std.debug.print("FRAME_RENDER_CONTEXT stage={s} requested_hps={d} valid={} canvas={d}x{d} scene={d}x{d} bloom={} bloom_passes={d} terrain_upload_mean_ms={d:.4} scene_draw_mean_ms={d:.4} postprocess_mean_ms={d:.4} ui_mean_ms={d:.4}\n",.{label,speed/3600,context.valid,context.canvas_width,context.canvas_height,context.scene_width,context.scene_height,context.bloom_active,context.bloom_passes,physics.stage_sum[0]/60,physics.stage_sum[1]/60,physics.stage_sum[2]/60,physics.stage_sum[3]/60});perf.metrics.setEnabled(false);std.mem.sort(f64,&frames,{},std.sort.asc(f64));
  std.debug.print("FRAME_SUMMARY stage={s} requested_hps={d} cells={d} occupied_start={d} cohorts_start={d} frames=60 ticks={d} sim_hours={d:.3} update_mean_ms={d:.4} physics_mean_per_frame_ms={d:.4} physics_max_ms={d:.4} render_finish_mean_ms={d:.4} total_mean_ms={d:.4} total_p95_ms={d:.4} total_max_ms={d:.4} compute_throughput_hps={d:.3} fixed_input_dt=0.016666667 gpu_finish=true\n",.{label,speed/3600,state.planet.microbeCells.len,occupied,cohorts,ticks,(state.gameTime-start_time)/3600,total_update/60,physics.physics_sum/60,physics.physics_max,total_render/60,total_frame/60,frames[56],max_frame,(state.gameTime-start_time)/3600/(total_frame/1000)});
 }
 try saves.apply(state,frozen.value);std.debug.assert(std.mem.eql(u8,bytes,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
 std.debug.print("FRAME_RESTORE stage={s} exact_save=true\n",.{label});
}
'''
p.write_text(s)
