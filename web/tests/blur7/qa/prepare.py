#!/usr/bin/env python3
from pathlib import Path
import os,sys,subprocess,shutil
root=Path(os.environ['STELLA_SOURCE_ROOT']).resolve();here=Path(__file__).resolve().parent;r=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(root/'web/tests/empty-bloom/qa/prepare.py'),str(r)],check=True)
shutil.copy2(here/'postprocess-baseline.fs',r/'shaders/postprocess.fs')
shutil.copy2(here/'postprocess-candidate.fs',r/'shaders/postprocess_candidate.fs')
shutil.copy2(r/'shaders/postprocess.vs',r/'shaders/postprocess_candidate.vs')
p=r/'states/play.zig';s=p.read_text();s='pub var qa_force_atmosphere=false;\n'+s;s=s.replace('self.displayMode == .Normal and false','qa_force_atmosphere or (self.displayMode == .Normal and false)');p.write_text(s)
p=r/'main.zig';s=p.read_text();needle='    if(std.posix.getenv("QA_EMPTY_BLOOM")!=null){';assert needle in s;s=s.replace(needle,(here/'sandbox-qa.zig.part').read_text()+needle);s=s.replace('    if(std.posix.getenv("QA_CLOCK")!=null){', '    if(std.posix.getenv("QA_CLOCK")!=null){\n        renderer.postprocessProgram.deinit();renderer.postprocessProgram=try @TypeOf(renderer.postprocessProgram).createFromName("postprocess_candidate");',1)
s+='\n'+(here/'diff-helper.zig.part').read_text();p.write_text(s)
print(r/'main.zig')
