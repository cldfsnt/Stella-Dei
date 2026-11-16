"""Execute fixed d6752e7 through actual variant preview; no model edits."""
from pathlib import Path
import hashlib,json
r=Path(__file__).resolve().parents[2];source=r.parent/'site-tmp/rooted-hardy/src';expected=json.loads((r/'web/tests/continuation-review/rooted-hardy/owner-hashes.json').read_text())
for n,h in expected.items():assert hashlib.sha256((source/n).read_bytes()).hexdigest()==h,n
s=(r/'web/tests/prepare-rooted-natural.py').read_text().replace("b=t/'rooted-natural'","b=t/'rooted-hardy-natural'").replace("src=t/'rooted-natural-owner/src'","src=t/'rooted-hardy/src'")
s=s.replace("qa=re.sub(","qa=qa.replace('stella_rooted_founder_preview(world,6)','stella_hardy_rooted_founder_preview(world,6)')\nqa=re.sub(")
exec(compile(s,str(r/'web/tests/prepare-rooted-natural.py'),'exec'))
