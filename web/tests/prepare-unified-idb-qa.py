"""Reproduce the static real-IDB QA directory; never starts a server."""
from pathlib import Path
import shutil,json,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1]).resolve()
assert out.name=='unified-idb-qa'
(out/'.openai').mkdir(parents=True,exist_ok=True);d=out/'staticdist';d.mkdir(exist_ok=True)
(out/'.openai/hosting.json').write_text(json.dumps({'static':{'directory':'staticdist'}})+'\n')
for f in ['unified-storage.js','combined-recovery.js','world-library.js']:shutil.copy2(root/'web'/f,d/f)
for f in ['harness.js','index.html']:shutil.copy2(root/'web/tests/continuation-review/unified-storage/real-idb-static'/f,d/f)
