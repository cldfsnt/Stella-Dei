"""Apply to exact extracted single-dock source, not the legacy root source tree."""
from pathlib import Path
import sys,json,hashlib,subprocess
here=Path(__file__).resolve().parent;root=Path(sys.argv[1]).resolve();changes=json.loads((here/'changed-hashes.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for name,h in changes.items():
 p=root/name
 assert (sha(p) if p.exists() else None)==h['before'],f'Wrong baseline: {name}'
subprocess.run(['patch','--batch','-p1','-i',str(here/'source.patch')],cwd=root,check=True)
for name,h in changes.items():assert sha(root/name)==h['after'],f'Wrong result: {name}'
for name,h in json.loads((here/'source-hashes.json').read_text()).items():assert sha(root/name)==h,f'Native source mismatch: {name}'
print('Exact planted-discovery source reconstructed and verified; build separately.')
