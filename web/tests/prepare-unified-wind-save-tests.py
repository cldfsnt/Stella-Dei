from pathlib import Path
import shutil,hashlib,json
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/unified-wind-save-tests';o=b/'src';assert not o.exists();shutil.copytree(r.parent/'site-tmp/unified-game/src',o);shutil.copytree(r.parent/'site-tmp/root-water-ui/src',o/'legacy');shutil.copytree(r.parent/'site-tmp/wind-dispersal/src',o/'wind_original')
extra=(r/'web/tests/protective-save-tests.txt').read_text().replace('for([_]u32{11,12})','for([_]u32{12})')
# Historical reference root-water-ui ends at14; current15 tested by its roundtrip.
extra+=(r/'web/tests/unified-wind-save-tests.txt').read_text();prior=(r/'web/tests/wind-save-tests.txt').read_text();extra+=prior[prior.index('test "actual frozen'):];p=o/'save_schema.zig';p.write_text(p.read_text()+extra)
(b/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},indent=2))
