"""Stage only storage into the unified candidate."""
from pathlib import Path
import shutil,sys
root=Path(__file__).resolve().parents[2];web=Path(sys.argv[1]).resolve()
assert web.name=='web' and web.parent.name=='unified-ui'
for name in ['stella-storage.js','combined-recovery-storage.js','combined-storage.js','unified-storage.js']:
 shutil.copy2(root/'web/unified-storage.js',web/name)
