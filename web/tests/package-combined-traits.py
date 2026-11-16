from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];base=r.parent/'site-tmp/root-wind-recovery/web/dist';p=r.parent/'site-tmp/combined-playtest';d=p/'web/dist';assert not d.exists();shutil.copytree(base,d)
s=(p/'web/shell.html').read_text();assert s.count('{{{ SCRIPT }}}')==1
s=s.replace('{{{ SCRIPT }}}','<script src="index.js" async></script>');(d/'index.html').write_text(s);shutil.copy2(p/'web/combined-traits.js',d/'combined-traits.js')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();unchanged={}
for x in base.iterdir():
 if x.is_file()and x.name!='index.html':assert sha(x)==sha(d/x.name),x.name;unchanged[x.name]=sha(x)
e=r/'web/tests/continuation-review/combined-playtest';e.mkdir(exist_ok=True);(e/'initial-artifact-proof.json').write_text(json.dumps({'html_before':sha(base/'index.html'),'html_after':sha(d/'index.html'),'unchanged':unchanged,'new_script_sha256':sha(d/'combined-traits.js')},indent=2)+'\n');shutil.copy2(p/'full-js.log',e/'full-js.log')
