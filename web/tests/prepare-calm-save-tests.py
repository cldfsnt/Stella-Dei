from pathlib import Path
import shutil
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/calm-save-tests/src';assert not b.exists();shutil.copytree(r.parent/'site-tmp/root-calm/src',b);shutil.copytree(r.parent/'site-tmp/root-water-preview/src',b/'legacy');p=b/'save_schema.zig';extra=(r/'web/tests/calm-save-tests.txt').read_text();prior=(r/'web/tests/wind-save-tests.txt').read_text();extra+=prior[prior.index('test "actual frozen'):];p.write_text(p.read_text()+extra)
