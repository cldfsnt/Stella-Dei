"""Stage HTML-only nurture guidance; never edit released artifacts or native code."""
from pathlib import Path
import shutil,hashlib,json
r=Path(__file__).resolve().parents[2];base=r.parent/'site-tmp/root-water-ui/web';out=r.parent/'site-tmp/rooted-guidance/web'
assert not out.exists(), 'Refuse to overwrite an existing candidate'
shutil.copytree(base,out,ignore=shutil.ignore_patterns('dist','node_modules','.cache'))
p=out/'shell.html';s=p.read_text();needle='<button id="rooted-founder-open">Plant rooted founder…</button>'
assert s.count(needle)==1
hint='<p id="rooted-founder-help">Pause and select a patch. <b>Plant rooted founder…</b> previews its water support before you confirm; Cancel plants nothing.<br>If root water is missing, try <b>Water +</b> on that patch, run the simulation or use Advance, then pause and preview again. Soil needs time to take up water; rain and drying vary.<br>Choose Standard or Hardy, then confirm only when you are ready. Water support is a current check, not a survival promise.</p>'
s=s.replace(needle,needle+hint);p.write_text(s)
proof={'change':'HTML-only inline guidance; no new control, receipt, storage, or engine change','baseline_shell_sha256':hashlib.sha256((base/'shell.html').read_bytes()).hexdigest(),'candidate_shell_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'unchanged_files':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in base.glob('*.js') if x.read_bytes()==(out/x.name).read_bytes()}}
e=r/'web/tests/continuation-review/rooted-guidance';e.mkdir(parents=True,exist_ok=True);(e/'source-proof.json').write_text(json.dumps(proof,indent=2)+'\n')
print(out)
