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
        PerformanceDetails.metrics.physics(12.5,1);PerformanceDetails.metrics.frame(20,3.25);
        const snapshot=try al.dupe(u8,std.mem.span(stella_performance_snapshot()));
        const after=try std.json.stringifyAlloc(al,try saves.capture(al,state),.{});
        std.debug.assert(std.mem.eql(u8,before,after));std.debug.assert(std.meta.eql(clock_before,state.simulationClock));
        std.debug.assert(stella_performance_enable(0)==1 and PerformanceDetails.metrics.sample().frames==0);
        const after_off=try std.json.stringifyAlloc(al,try saves.capture(al,state),.{});std.debug.assert(std.mem.eql(u8,before,after_off));
        std.debug.print("PERFORMANCE_CALLBACKS save_bytes={d} hash={x} unchanged=true clock_unchanged=true snapshot={s}\\n",.{before.len,std.hash.Wyhash.hash(0,before),snapshot});
        loop.pump(1024);return;
    }
'''+needle)
p.write_text(s)
