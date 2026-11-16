"""Patch a NEW isolated conditions-web clone; never modify prior artifacts."""
from pathlib import Path
import shutil,sys
out=Path(sys.argv[1]).resolve();assert out.name=='web' and out.parent.name=='rooted-hardy-ui'
root=Path(__file__).resolve().parent
p=out/'shell.html';s=p.read_text();assert 'rooted-founder-variant' not in s
needle='<button id="rooted-founder-open">';assert s.count(needle)==1
s=s.replace(needle,'<label for="rooted-founder-variant">Rooted founder</label><select id="rooted-founder-variant" aria-describedby="rooted-founder-choice"><option value="standard" selected>Standard · structure 0%</option><option value="hardy">Hardy · structure 50%</option></select><p id="rooted-founder-choice">Better survival in shallow cold/dry conditions, slower growth and extra wet-habitat costs. Not frost-proof. Same paid body cost. Chosen founder genetics, not evolved adaptation.</p>'+needle)
s=s.replace(" preview:(world,point)=>JSON.parse(Module.ccall('stella_rooted_founder_preview'"," variant:()=>document.getElementById('rooted-founder-variant').value,\n preview:(world,point,variant)=>JSON.parse(Module.ccall(variant==='hardy'?'stella_hardy_rooted_founder_preview':'stella_rooted_founder_preview'")
s=s.replace("['_stella_rooted_founder_preview'","['_stella_hardy_rooted_founder_preview','_stella_rooted_founder_preview'")
s=s.replace("document.getElementById('rooted-founder-open').disabled=value;","document.getElementById('rooted-founder-open').disabled=value;document.getElementById('rooted-founder-variant').disabled=value;")
p.write_text(s);shutil.copy2(root/'rooted-founder.js',out/'rooted-founder.js')
p=out/'build.sh';s=p.read_text();assert '_stella_hardy_rooted_founder_preview' not in s;s=s.replace('-sEXPORTED_FUNCTIONS=','-sEXPORTED_FUNCTIONS=_stella_hardy_rooted_founder_preview,',1);p.write_text(s)
