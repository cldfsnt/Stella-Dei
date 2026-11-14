from pathlib import Path
import os,sys,subprocess
root=Path(os.environ['STELLA_SOURCE_ROOT']);out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-nursery-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text().replace('if (!is_web or !web_initialized or !game.state_init) return null;','if (!game.state_init) return null;')
needle='    if (std.posix.getenv("STELLA_ORIGIN_COUPLED") != null) {'
code=r'''
    if(std.posix.getenv("QA_LIVING_TRAITS")!=null){
        const saves=@import("save_game.zig");var arena=std.heap.ArenaAllocator.init(allocator);defer arena.deinit();const al=arena.allocator();
        const before=try std.json.stringifyAlloc(al,try saves.capture(al,state),.{});
        for(0..3)|_|{
            const json=std.mem.span(stella_life_snapshot());
            std.debug.assert(json.len<8192);
            const parsed=try std.json.parseFromSlice(std.json.Value,al,json,.{});defer parsed.deinit();
            std.debug.assert(parsed.value.object.get("tissues").?.array.items.len==4);
            for(parsed.value.object.get("tissues").?.array.items)|t|std.debug.assert(t.object.contains("living_traits"));
            std.debug.print("LIVING_TRAITS_SNAPSHOT bytes={d} valid=true cohorts=4\n",.{json.len});
        }
        const after=try std.json.stringifyAlloc(al,try saves.capture(al,state),.{});
        std.debug.assert(std.mem.eql(u8,before,after));
        std.debug.print("LIVING_TRAITS_INVARIANCE bytes={d} hash={x} unchanged=true\n",.{before.len,std.hash.Wyhash.hash(0,before)});
        loop.pump(1024);return;
    }
'''
assert needle in s;s=s.replace(needle,code+needle);p.write_text(s)
