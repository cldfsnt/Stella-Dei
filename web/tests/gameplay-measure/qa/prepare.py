from pathlib import Path
import subprocess,os,sys
root=Path(os.environ['STELLA_SOURCE_ROOT']);out=Path(sys.argv[1]);here=Path(__file__).parent
subprocess.run([sys.executable,str(root/'web/tests/egl-nursery-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text().replace('if (!is_web or !web_initialized or !game.state_init) return null;','if (!game.state_init) return null; // Native callback availability shim only')
needle='    if (std.posix.getenv("STELLA_ORIGIN_COUPLED") != null) {'
s=s.replace(needle,'''    if(std.posix.getenv("QA_PERFORMANCE")!=null){
        const saves=@import("save_game.zig");var arena=std.heap.ArenaAllocator.init(allocator);defer arena.deinit();const al=arena.allocator();
        const before=try std.json.stringifyAlloc(al,try saves.capture(al,state),.{});
        const clock_before=state.simulationClock;
        std.debug.assert(stella_performance_enable(1)==1);
        // Exercise real callback body and diagnostic accumulator; no physical ticks.
        for(0..60)|i|{PerformanceDetails.metrics.physics(12.5,1);PerformanceDetails.metrics.frame(if(i==59)200 else 20,3.25);}
        std.debug.assert(PerformanceDetails.metrics.sample().frame_p95==20 and PerformanceDetails.metrics.sample().long_frames==1);
        const snapshot=try al.dupe(u8,std.mem.span(stella_performance_snapshot()));
        const after=try std.json.stringifyAlloc(al,try saves.capture(al,state),.{});
        std.debug.assert(std.mem.eql(u8,before,after));std.debug.assert(std.meta.eql(clock_before,state.simulationClock));
        std.debug.assert(stella_performance_enable(0)==1 and PerformanceDetails.metrics.sample().frames==0);
        const after_off=try std.json.stringifyAlloc(al,try saves.capture(al,state),.{});std.debug.assert(std.mem.eql(u8,before,after_off));
        std.debug.print("PERFORMANCE_CALLBACKS save_bytes={d} hash={x} unchanged=true clock_unchanged=true snapshot={s}\\n",.{before.len,std.hash.Wyhash.hash(0,before),snapshot});
        const old_time=state.gameTime;const old_scale=state.timeScale;const old_metrics=PerformanceDetails.metrics;const old_serial=PerformanceDetails.world_serial;
        state.gameTime=std.math.floatMax(f64);state.timeScale=std.math.floatMax(f32);PerformanceDetails.world_serial=std.math.maxInt(u32);
        const huge=std.math.floatMax(f64)/2;
        PerformanceDetails.metrics.current=.{};
        PerformanceDetails.metrics.completed=.{.frames=1,.ticks=2,.physics_frames=1,.long_frames=1,.frame_p95=huge,.frame_sum=huge,.frame_max=huge,.physics_sum=huge,.physics_max=huge,.render_sum=huge,.render_max=huge,.stage_sum=.{huge}**4,.stage_max=.{huge}**4};
        PerformanceDetails.metrics.context=.{.valid=true,.world="sandbox",.map="AtmosphericPressure",.canvas_width=std.math.maxInt(i32),.canvas_height=std.math.maxInt(i32),.scene_width=std.math.maxInt(i32),.scene_height=std.math.maxInt(i32),.bloom_active=true,.bloom_passes=255,.composite_passes=255,.animals=std.math.maxInt(usize),.camera_radius=std.math.floatMax(f32),.planet_radius=std.math.floatMax(f32),.camera_valid=true};
        const boundary=std.mem.span(stella_performance_snapshot());std.debug.assert(boundary.len>1000 and boundary.len<performance_json.len);
        const json=try std.json.parseFromSlice(std.json.Value,al,boundary,.{});defer json.deinit();std.debug.assert(json.value.object.contains("world_serial") and json.value.object.contains("stage_max_ms"));
        std.debug.print("PERFORMANCE_JSON_BOUNDARY bytes={d} capacity={d} valid=true world_serial_max=true\\n",.{boundary.len,performance_json.len});
        state.gameTime=old_time;state.timeScale=old_scale;PerformanceDetails.metrics=old_metrics;PerformanceDetails.world_serial=old_serial;
        const restored=try std.json.stringifyAlloc(al,try saves.capture(al,state),.{});std.debug.assert(std.mem.eql(u8,before,restored));
        loop.pump(1024);return;
    }
'''+needle)
p.write_text(s)
