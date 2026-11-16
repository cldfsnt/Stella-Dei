"""Stage only the recovery storage module in the isolated recovery candidate."""
from pathlib import Path
import shutil,sys
root=Path(__file__).resolve().parents[2]
web=Path(sys.argv[1]).resolve()
assert web.name=='web' and web.parent.name=='root-wind-recovery'
for name in ['stella-storage.js','combined-recovery-storage.js']:
    shutil.copy2(root/'web/combined-recovery-storage.js',web/name)

p=web/'tests/storage-upgrade.test.cjs'
s=p.read_text()
old='/automatic restore is not available/'
new='/Use World → Recovery backups to download or restore a verified checkpoint/'
assert s.count(old)+s.count(new)==1
p.write_text(s.replace(old,new))
