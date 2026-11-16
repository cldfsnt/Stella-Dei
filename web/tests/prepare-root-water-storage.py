"""Stage storage only into the isolated calmer-world candidate."""
from pathlib import Path
import shutil,sys
root=Path(__file__).resolve().parents[2]
web=Path(sys.argv[1]).resolve()
assert web.name=='web' and web.parent.name=='root-water-ui'
for name in ['stella-storage.js','combined-recovery-storage.js','combined-storage.js','root-water-storage.js']:
    shutil.copy2(root/'web/root-water-storage.js',web/name)
