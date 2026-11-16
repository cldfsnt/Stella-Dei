"""Rebuild a new isolated candidate; never modifies its frozen inputs."""
from pathlib import Path
import shutil,subprocess,sys,json,hashlib
r=Path(__file__).resolve().parents[2];t=r.parent/'site-tmp';out=Path(sys.argv[1])if len(sys.argv)>1 else t/'protective-integration-reproduced';assert not(out/'src').exists();shutil.copytree(t/'root-water-ui/src',out/'src')
for script in ['patch-protective-engine.py','patch-protective-factory.py','protective-save-prepare.py']:subprocess.run([sys.executable,str(r/'web/tests'/script),str(out/'src')],check=True)
shutil.copy2(r/'web/tests/protective-view.zig',out/'src/protective_view.zig')
shutil.copy2(r/'web/tests/protective-integration-tests.zig',out/'src/protective_tests.zig')
(out/'source-hashes.json').write_text(json.dumps({str(p.relative_to(out/'src')):hashlib.sha256(p.read_bytes()).hexdigest()for p in(out/'src').rglob('*.zig')},indent=2)+'\n')
