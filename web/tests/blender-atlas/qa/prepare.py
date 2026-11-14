#!/usr/bin/env python3
from pathlib import Path
import subprocess,os,sys
here=Path(__file__).resolve().parent;root=Path(os.environ['STELLA_SOURCE_ROOT']).resolve();out=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(root/'web/tests/egl-nursery-prepare.py'),str(out),'--replay'],check=True)
p=out/'main.zig';s=p.read_text().replace('if (!is_web or !web_initialized or !game.state_init) return null;','if (!game.state_init) return null; // native callback-body test only')
a=s.index('    if(std.posix.getenv("QA_REPLAY_SAVE"))');b=s.index('    { std.debug.assert(state.focusSeedableHabitat());',a);s=s[:a]+(here/'fit-empty.zig.part').read_text()+(here/'fit-replay.zig.part').read_text()+s[b:];p.write_text(s)
s=(root/'web/tests/egl-origin-shim.c').read_text().replace('h=700;width=w','h=atoi(getenv("STELLA_ORIGIN_HEIGHT")?getenv("STELLA_ORIGIN_HEIGHT"):"700");width=w');(out/'egl-fit-shim.c').write_text(s)
prefix=os.path.relpath(root,out)+'/'
s=(root/'web/tests/egl-origin-build.zig').read_text().replace('b.path("../../" ++ entry[1])','b.path("'+prefix+'" ++ entry[1])').replace('b.path("../../deps','b.path("'+prefix+'deps').replace('"../../deps/','"'+prefix+'deps/').replace('"egl-origin-shim.c"','"egl-fit-shim.c"');(out/'build.zig').write_text(s)

# Native-only asset ownership diagnostics, no production instrumentation.
p=out/'states/play.zig';s=p.read_text().replace('gl.deleteTextures(1,&texture.texture);','std.debug.assert(gl.isTexture(texture.texture)==gl.TRUE); const old=texture.texture; gl.deleteTextures(1,&texture.texture); std.debug.assert(gl.isTexture(old)==gl.FALSE); std.debug.print("ATLAS owned_unregistered_deleted=true\\n",.{});')
s=s.replace('if(!self.blenderAtlasAttempted){','if(std.posix.getenv("QA_REPEAT_ATLAS_LOAD")!=null) self.blenderAtlasAttempted=false; if(!self.blenderAtlasAttempted){');p.write_text(s)
