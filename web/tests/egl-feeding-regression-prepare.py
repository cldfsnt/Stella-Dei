#!/usr/bin/env python3
"""Bounded paused presentation-frame regression; actual saved world, not device FPS."""
from pathlib import Path
import subprocess,sys
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(r/'web/tests/egl-feeding-marker-prepare.py'),str(o)],check=True)
p=o/'main.zig';s=p.read_text()
s=s.replace('for([_]bool{false,true})|candidate|{','for([_]bool{false,true,true,false,false,true},0..)|candidate,arm|{',1)
needle='              const prefix=std.posix.getenv("STELLA_EGL_CAPTURE_PREFIX").?;'
pos=s.index(needle,s.index('FEEDING_VISUAL_MISSING'))
s=s[:pos]+'''              for(0..20)|_|{game.loop.pump(16);render(window);gl.finish();window.swapBuffers();}
              var timer=try std.time.Timer.start();
              for(0..120)|_|{game.loop.pump(16);render(window);gl.finish();window.swapBuffers();}
              const elapsed=timer.read();
              std.debug.print("MARKER_FRAME arm={d} kind={s} candidate={} frames=120 ns={d} glyphs={d}\\n",.{arm,@tagName(kind),candidate,elapsed,state.colonyTargets.count});
'''+s[pos:]
p.write_text(s)
# Exact release function bodies, not a baseline carrying candidate scratch writes.
def body(s):
    a=s.index('    fn renderSprouts(');b=s.index('\n    }\n',a)+7
    return s[a:b]
old=body(subprocess.check_output(['git','show','b308b37:src/states/play.zig'],cwd=r,text=True))
new=body(subprocess.check_output(['git','show','be1abc8:src/states/play.zig'],cwd=r,text=True))
p=o/'states/play.zig';s=p.read_text();existing=body(s)
wrapper='''    fn renderSprouts(self: *PlayState, vg: nvg, vp: Mat4, width: f32, height: f32, toolBottom: f32) void {
        if(qa_history_marker) self.renderSproutsV58(vg,vp,width,height,toolBottom) else self.renderSproutsV57(vg,vp,width,height,toolBottom);
    }
'''
s=s.replace(existing,wrapper+old.replace('fn renderSprouts(','fn renderSproutsV57(',1)+'\n'+new.replace('fn renderSprouts(','fn renderSproutsV58(',1),1);p.write_text(s)
import hashlib,json
(o.parent/'source-proof.json').write_text(json.dumps({'v57':'b308b37','v58':'be1abc8','v57_function':hashlib.sha256(old.encode()).hexdigest(),'v58_function':hashlib.sha256(new.encode()).hexdigest(),'input_sha256':hashlib.sha256((r.parent/'site-tmp/natural60-day60.json').read_bytes()).hexdigest(),'copied_main':hashlib.sha256((o/'main.zig').read_bytes()).hexdigest(),'copied_play':hashlib.sha256(p.read_bytes()).hexdigest()},indent=2)+'\n')
