"""Stage storage only into the isolated protective-world candidate."""
from pathlib import Path
import shutil,sys
root=Path(__file__).resolve().parents[2]
web=Path(sys.argv[1]).resolve()
assert web.name=='web' and web.parent.name=='protective-ui'
for name in ['stella-storage.js','combined-recovery-storage.js','combined-storage.js','protective-storage.js']:
    shutil.copy2(root/'web/protective-storage.js',web/name)
