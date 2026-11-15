"""Stage the paid-founder UI on an existing isolated Wetlands web copy only."""
from pathlib import Path
import sys, shutil
root=Path(__file__).resolve().parent
out=Path(sys.argv[1]).resolve()
assert out.name=='web' and out.parent.name=='rooted-founder'
p=out/'shell.html';s=p.read_text();assert 'wetlands-notice' in s and 'rooted-founder-open' not in s
s=s.replace('<script src="wetlands-preview.js"></script>','<script src="wetlands-preview.js"></script><script src="rooted-founder.js"></script>',1)
needle='<button id="starter-seed">Seed colony</button>';assert s.count(needle)==1
s=s.replace(needle,needle+'<button id="rooted-founder-open">Plant rooted founder…</button><p id="rooted-founder-status" role="status" aria-live="polite"></p>',1)
needle="const storage=createStellaStorage(Module,feedback,{preserveLegacyThroughVersion:6});";assert s.count(needle)==1
s=s.replace(needle,needle+'''
const rootedFounder=StellaRootedFounder.create({
 available:()=>Module.started&&!Module.failed&&!document.hidden&&!storage.state().busy&&!advanceDay.isLocked()&&['_stella_rooted_founder_preview','_stella_seed_rooted','_stella_rooted_founder_cancel','_stella_wetlands_snapshot'].every(k=>typeof Module[k]==='function'),
 snapshot:()=>JSON.parse(Module.ccall('stella_wetlands_snapshot','string',[],[])),
 preview:(world,point)=>JSON.parse(Module.ccall('stella_rooted_founder_preview','string',['number','number'],[world,point])),
 apply:(world,point,token)=>JSON.parse(Module.ccall('stella_seed_rooted','string',['number','number','number'],[world,point,token])),
 cancel:token=>Module.ccall('stella_rooted_founder_cancel','number',['number'],[token]),
 confirm:message=>window.confirm(message),busy:value=>{document.getElementById('rooted-founder-open').disabled=value;},
 report:message=>{document.getElementById('rooted-founder-status').textContent=message;feedback(message);},
 inspect:()=>{document.getElementById('more-menu').close();refreshLife();document.getElementById('cohort-details').open=true;document.getElementById('life-sheet').showModal();}
});
document.getElementById('rooted-founder-open').onclick=()=>rootedFounder.plant();
''',1)
s=s.replace('Seed requires at least 0.2 m water.','Ordinary Seed requires at least 0.2 m water. Plant rooted founder chooses paid root genetics; shallow planting requires existing moist soil.')
s=s.replace('roots may arise in later offspring, not founders.','ordinary founders start rootless. Plant rooted founder is a separate paid choice.')
p.write_text(s)
f=out/'wetlands-preview.js';f.write_text(f.read_text().replace('seeded founders have no assigned roots.','ordinary seeded founders have no assigned roots.'))
shutil.copy2(root/'rooted-founder.js',out/'rooted-founder.js')
b=out/'build.sh';t=b.read_text();needle='-sEXPORTED_FUNCTIONS=';assert t.count(needle)==1
t=t.replace(needle,needle+'_stella_rooted_founder_preview,_stella_seed_rooted,_stella_rooted_founder_cancel,',1)
t+='\ncp web/rooted-founder.js web/dist/rooted-founder.js\n'
b.write_text(t)
print('Rooted-founder isolated UI staged; native and artifact gates still required.')
# Copied shell VM must load the actual new controller, just as the browser does.
test=out/'tests/shell.test.cjs'
if test.exists():
 t=test.read_text();needle='const sandbox={'
 assert t.count(needle)==1
 test.write_text(t.replace(needle,needle+"StellaRootedFounder:require('../rooted-founder.js'),",1))
