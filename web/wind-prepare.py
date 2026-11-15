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
