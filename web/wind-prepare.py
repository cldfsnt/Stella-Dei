"""Stage main-game candidate frontend only. Never touch root/Wetlands or deploy."""
from pathlib import Path
import shutil,sys
root=Path(__file__).resolve().parent
out=Path(sys.argv[1]).resolve()
if out.name!='web' or out.parent.name!='wind-dispersal':raise SystemExit('Expected isolated wind-dispersal/web')
out.mkdir(parents=True,exist_ok=True)
for p in root.iterdir():
 if p.is_file() and p.suffix in ('.html','.js','.css','.svg'):shutil.copy2(p,out/p.name)
s=(root/'shell.html').read_text()
def once(a,b):
 global s
 assert s.count(a)==1,a
 s=s.replace(a,b,1)
once('<script src="stella-storage.js"></script>','<script src="wind-origin.js"></script><script src="stella-storage.js"></script>')
once('<h3>World</h3>','<h3>World</h3><button id="wind-new">New Origin · wind dispersal…</button><button id="wind-refresh">Refresh wind-law status</button><p id="wind-law-status" role="status"></p><details id="wind-disclosure"><summary>How wind dispersal works</summary><p id="wind-law-details" style="white-space:pre-line"></p></details>')
once('<section id="group-plant" aria-label="Plant"><h3>Plant</h3>','<section id="group-plant" aria-label="Plant"><h3>Plant</h3><button id="wind-pioneer" disabled>Seed Pioneer here · paid, 50% aerial allocation</button>')
once("const storage=createStellaStorage(Module,feedback,{preserveLegacyThroughVersion:6});", """const storage=createStellaStorage(Module,feedback,{preserveLegacyThroughVersion:6,readWriterIdentity:()=>JSON.parse(Module.ccall('stella_wind_snapshot','string',[],[]))});
const windUI=StellaWind.mount(document,{
 available:()=>Module.started&&!Module.failed&&!document.hidden&&!storage.state().busy&&(typeof advanceDay==='undefined'||!advanceDay.isLocked())&&typeof Module._stella_wind_new==='function'&&typeof Module._stella_seed_pioneer==='function',
 read:()=>JSON.parse(Module.ccall('stella_wind_snapshot','string',[],[])),
 confirm:text=>window.confirm(text),fresh:world=>Module.ccall('stella_wind_new','number',['number'],[world]),
 pioneer:(world,cell)=>Module.ccall('stella_seed_pioneer','number',['number','number'],[world,cell]),
 message:feedback,changed:()=>{syncWorldMode();refreshStarter();}
});
""")
once('function selectToolGroup(group){',"function selectToolGroup(group){if(typeof windUI!=='undefined')windUI.refresh();")
(out/'shell.html').write_text(s)
shutil.copy2(root/'wind-storage.js',out/'stella-storage.js')
print('Staged isolated main-game wind frontend only. Native exports/build/actual-flow gates remain required.')

# Test adapter supplies the newly loaded controller in the existing shell VM.
tests=out/'tests';tests.mkdir(exist_ok=True)
for p in (root/'tests').glob('*.test.cjs'):shutil.copy2(p,tests/p.name)
p=tests/'shell.test.cjs';t=p.read_text();needle="sandbox.WorldEcology=require('../world-ecology.js');";assert t.count(needle)==1;t=t.replace(needle,needle+"sandbox.StellaWind=require('../wind-origin.js');");p.write_text(t)

for p in (root/'tests').glob('*.py'):shutil.copy2(p,tests/p.name)

# Build packaging is idempotent and does not change native exports.
build=out/'build.sh'
if build.exists():
 t=build.read_text();line='cp web/wind-origin.js web/dist/wind-origin.js'
 if line not in t:
  needle='cp web/stella-storage.js web/dist/stella-storage.js'
  assert t.count(needle)==1
  build.write_text(t.replace(needle,needle+'\n'+line))

# Unchanged license and preload packager needed by the isolated full build.
shutil.copy2(root/'package.py',out/'package.py')
shutil.copy2(root.parent/'LICENSE',out.parent/'LICENSE')

# Temporary opt-in runtime boundary: no main/Wetlands storage fallback.
html=out/'shell.html';s=html.read_text()
needle='<aside id="patch-watch-hud"';assert s.count(needle)==1
s=s.replace(needle,(root/'wind-banner.html').read_text()+needle,1)
needle="const welcomeKey='stella-guide-dismissed-v1';";assert s.count(needle)==1
s=s.replace(needle,"const welcomeKey='stella-wind-guide-dismissed-v1';",1)
html.write_text(s)
for name in ['stella-storage.js','wind-storage.js']:
 p=out/name;t=p.read_text();assert '/saves' in t;t=t.replace('/saves','/wind-saves');assert '/saves' not in t;p.write_text(t)
for name in ['storage-upgrade.test.cjs','wind-storage.test.cjs']:
 p=tests/name;p.write_text(p.read_text().replace('/saves','/wind-saves'))

# Separate Pioneer batch uses the same planned transaction and dialog, never a seed loop.
shutil.copy2(root/'wind-auto-seed.js',out/'auto-seed.js')
p=out/'shell.html';s=p.read_text()
def patch(a,b):
 global s
 assert s.count(a)==1,a
 s=s.replace(a,b,1)
patch('<button id="auto-seed-open" disabled>Auto-seed world…</button>','<button id="auto-seed-open" disabled>Auto-seed world…</button><button id="auto-seed-pioneer-open">Plan Pioneer Auto-seed…</button>')
patch('AutoSeed.create({available:', 'AutoSeed.create({requireFounderKind:true,available:')
a=s.index("document.getElementById('auto-seed-open').onclick=()=>{")
b=s.index("\ndocument.getElementById('auto-seed-apply')",a)
old=s[a:b]
body=old.replace("document.getElementById('auto-seed-open').onclick=()=>{",'function openAutoSeed(kind){')
body=body.replace('autoSeed.start(data.world_serial);',"if(kind==='pioneer'){const w=JSON.parse(Module.ccall('stella_wind_snapshot','string',[],[]));if(w.status!=='wind'||!w.enabled||w.world_serial!==data.world_serial)throw Error('Pioneer planning requires the current wind-enabled world.');}autoSeed.start(data.world_serial,kind);")
body=body.replace("const sheet=document.getElementById('auto-seed-sheet');", "document.getElementById('auto-seed-title').textContent=kind==='pioneer'?'Pioneer Auto-seed · 50% inherited aerial allocation':'Auto-seed world · ordinary local founders';const sheet=document.getElementById('auto-seed-sheet');")
body=body.replace("function openAutoSeed(kind){", "function openAutoSeed(kind){if(storage.state().busy||advanceDay.isLocked()){feedback('Save or action busy. Wait before planning.',true);return;}")
s=s[:a]+body+"\ndocument.getElementById('auto-seed-open').onclick=()=>openAutoSeed('ordinary');\ndocument.getElementById('auto-seed-pioneer-open').onclick=()=>openAutoSeed('pioneer');"+s[b:]
p.write_text(s)

p=out/'shell.html';s=p.read_text()
a='<b>Choose your living world.</b> Origin begins with simple microbes; Sandbox offers plants and rabbits. Choose Random or Continents for a new world. Pinch to zoom; drag to explore.'
b='<b>Explore wind dispersal.</b> This preview starts a fresh Origin world. Seed or plan paid Pioneer founders from Tools → Plant, or Load this preview’s save from Tools → World. The main game opens separately from the preview notice. Pinch to zoom; drag to explore.'
assert s.count(a)==1;s=s.replace(a,b,1);p.write_text(s)

# Current-state descendant navigation, not reconstructed flight history.
p=out/'shell.html';s=p.read_text()
def patch_desc(a,b):
 global s
 assert s.count(a)==1,a
 s=s.replace(a,b,1)
patch_desc('<script src="wind-origin.js"></script>','<script src="wind-descendant.js"></script><script src="wind-origin.js"></script>')
patch_desc('<h3>Observe</h3>','<h3>Observe</h3><button id="find-aerial-descendant">Find aerial descendant</button><p>Find a living descendant with inherited aerial allocation. Its birth route is not recorded.</p>')
patch_desc('<p id="life-colony-shares"','<p id="wind-descendant-detail" role="status"></p><p id="life-colony-shares"')
patch_desc(" document.getElementById('life-habitat').textContent='';", " document.getElementById('wind-descendant-detail').textContent='';document.getElementById('life-habitat').textContent='';")
patch_desc("  if(!Array.isArray(data.cohorts))throw Error('Invalid snapshot');", "  if(!Array.isArray(data.cohorts))throw Error('Invalid snapshot');\n  let descendantWind=null;try{if(typeof Module._stella_wind_snapshot==='function')descendantWind=JSON.parse(Module.ccall('stella_wind_snapshot','string',[],[]));}catch{}\n  document.getElementById('wind-descendant-detail').textContent=typeof StellaWindDescendant==='undefined'?'':StellaWindDescendant.label(descendantWind,data);")
patch_desc("function selectToolGroup(group){", """const aerialDescendant=StellaWindDescendant.create({
 available:()=>Module.started&&!Module.failed&&!document.hidden&&!storage.state().busy&&!advanceDay.isLocked()&&typeof Module._stella_find_aerial_descendant==='function',
 wind:()=>JSON.parse(Module.ccall('stella_wind_snapshot','string',[],[])),life:()=>JSON.parse(Module.ccall('stella_life_snapshot','string',[],[])),
 call:world=>Module.ccall('stella_find_aerial_descendant','number',['number'],[world]),message:feedback,
 found:()=>{touchControls.reset();moreMenu.close();refreshLife();document.getElementById('cohort-details').open=true;const sheet=document.getElementById('life-sheet');if(!sheet.open)sheet.showModal();}
});
document.getElementById('find-aerial-descendant').onclick=()=>aerialDescendant.visit();
function selectToolGroup(group){""")
p.write_text(s)
build=out/'build.sh';t=build.read_text();line='cp web/wind-descendant.js web/dist/wind-descendant.js'
if line not in t:
 needle='cp web/wind-origin.js web/dist/wind-origin.js';assert t.count(needle)==1;t=t.replace(needle,needle+'\n'+line);build.write_text(t)
p=tests/'shell.test.cjs';t=p.read_text();needle="sandbox.StellaWind=require('../wind-origin.js');";assert t.count(needle)==1;p.write_text(t.replace(needle,needle+"sandbox.StellaWindDescendant=require('../wind-descendant.js');"))
