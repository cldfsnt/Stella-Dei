"""Fresh isolated unified engine; historical inputs are never edited."""
from pathlib import Path
import sys,shutil,subprocess,json,hashlib
r=Path(__file__).resolve().parents[2];out=Path(sys.argv[1]);assert not(out/'src').exists()
shutil.copytree(r.parent/'site-tmp/protective-integration/src',out/'src')
for script in ['unified-wind-save-prepare.py','patch-unified-native.py']:
 subprocess.run([sys.executable,str(r/'web/tests'/script),str(out/'src')],check=True)
shutil.copy2(r/'web/tests/unified-identity-tests.zig',out/'src/unified_identity_tests.zig')
(out/'source-hashes.json').write_text(json.dumps({str(p.relative_to(out/'src')):hashlib.sha256(p.read_bytes()).hexdigest() for p in (out/'src').rglob('*.zig')},indent=2)+'\n')
