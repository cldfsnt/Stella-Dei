from pathlib import Path
import shutil,hashlib,json
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/wind-save-tests';o=b/'src';assert not o.exists();shutil.copytree(r.parent/'site-tmp/wind-dispersal/src',o);shutil.copytree(r/'src',o/'legacy')
p=o/'save_schema.zig';p.write_text(p.read_text()+(r/'web/tests/wind-save-tests.txt').read_text())
(b/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},indent=2))
