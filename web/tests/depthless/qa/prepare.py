from pathlib import Path
import os,sys,subprocess
root=Path(os.environ['STELLA_SOURCE_ROOT']).resolve();here=Path(__file__).resolve().parent;out=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(root/'web/tests/unused-upload/qa/prepare.py'),str(out)],check=True)
subprocess.run(['patch','-p2','-i',str(here/'depthless.patch')],cwd=out,check=True)
for patch in ['instrument-renderer.patch','instrument-main.patch']:
 subprocess.run(['patch','-p1','-i',str(here/patch)],cwd=out,check=True)
print(out/'main.zig')
if os.environ.get('DEPTH_WEB_FORMATS'):
 for patch in ['web-formats-renderer.patch','web-formats-main.patch']:
  subprocess.run(['patch','-p1','-i',str(here/patch)],cwd=out,check=True)
