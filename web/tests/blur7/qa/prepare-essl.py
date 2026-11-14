from pathlib import Path
import sys,subprocess
here=Path(__file__).resolve().parent;out=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(here/'prepare.py'),str(out)],check=True)
p=out/'renderer.zig';s=p.read_text().replace('@import("builtin").cpu.arch.isWasm()', 'true').replace('const is_web = true;', 'const is_web = false;')
s=s.replace('if (is_web) gl.RGBA16F else gl.RGB16F','gl.RGBA16F').replace('if (is_web) gl.RGBA else gl.RGB','gl.RGBA').replace('if (is_web) gl.HALF_FLOAT else gl.UNSIGNED_BYTE','gl.HALF_FLOAT').replace('if (is_web) gl.DEPTH_COMPONENT32F else gl.DEPTH_COMPONENT','gl.DEPTH_COMPONENT32F');p.write_text(s)
