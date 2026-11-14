#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent
out=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/stella-sandbox-reg-src')
subprocess.run([sys.executable,str(here/'egl-prepare.py'),str(out),'--mobile','--paused'],check=True)
p=out/'states/play.zig';p.write_text(p.read_text().replace('var randomPrng = std.rand.DefaultPrng.init(@as(u64, @bitCast(std.time.milliTimestamp())));','var randomPrng = std.rand.DefaultPrng.init(1337);'))
p=out/'main.zig';s=p.read_text().replace('            const i = state.selectedPoint;','''            if(frame==215) sandboxSaveCheck(state,game.allocator) catch |err| { std.debug.panic("Save failed {s}",.{@errorName(err)}); };
            std.debug.print("MODAL frame={d} open={} camera={any} target={any} mode={s}\\n",.{frame,state.showPointDetails,state.cameraPos.data,state.targetCameraPos.data,@tagName(state.planet.worldMode)});
            const i = state.selectedPoint;''');p.write_text(s+(here/'egl-sandbox-save.zig.part').read_text())
