from pathlib import Path
import os,sys,subprocess
root=Path(os.environ['STELLA_SOURCE_ROOT']);out=Path(sys.argv[1]);here=Path(__file__).parent
subprocess.run([sys.executable,str(root/'web/tests/egl-nursery-prepare.py'),str(out)],check=True)
p=out/'renderer.zig';s=p.read_text();s='pub var qa_uniform_bypass=false;\npub var qa_uniform_lookups:u64=0;\npub var qa_program_created:u64=0;\npub var qa_program_deleted:u64=0;\n'+s
s=s.replace('return ShaderProgram{ .program = gl.createProgram() };','qa_program_created+=1;return ShaderProgram{ .program = gl.createProgram() };')
s=s.replace('if(self.program!=0)gl.deleteProgram(self.program);','if(self.program!=0){qa_program_deleted+=1;gl.deleteProgram(self.program);}')
s=s.replace('if(self.uniformLocations.get(name))|location|return location;', 'if(!qa_uniform_bypass)if(self.uniformLocations.get(name))|location|return location;\n        qa_uniform_lookups+=1;')
s=s.replace('self.uniformLocations.put(name,location);','if(!qa_uniform_bypass)self.uniformLocations.put(name,location);');p.write_text(s)
p=out/'main.zig';s=p.read_text();needle='    if (std.posix.getenv("STELLA_ORIGIN_COUPLED") != null) {';s=s.replace(needle,(here/'acceptance.zig.part').read_text()+needle);p.write_text(s)

# Isolated reload failure fixture; never modifies production shader files.
import shutil
bad=out.parent/'bad-shaders'/'src'/'shaders'
bad.mkdir(parents=True,exist_ok=True)
shutil.copytree(root/'src'/'shaders',bad,dirs_exist_ok=True)
(bad/'postprocess.fs').write_text('intentional malformed GLSL for failed reload QA\n')
