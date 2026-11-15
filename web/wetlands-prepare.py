"""Patch an already isolated frontend copy only; never deploy or modify root source.
Native build must use /wetlands-saves and explicit experimental new-world law.
"""
from pathlib import Path
import sys,shutil
root=Path(__file__).resolve().parent
out=Path(sys.argv[1]).resolve()
if not (out.name=='wetlands' or (out.name=='web' and out.parent.name=='wetlands-preview')) or out==root:raise SystemExit('Expected isolated output directory named wetlands')
html=out/('shell.html' if out.name=='web' else 'index.html');storage=out/'stella-storage.js'
s=html.read_text();t=storage.read_text()
if 'wetlands-notice' in s:raise SystemExit('Already patched')
def once(a,b):
 global s
 if s.count(a)!=1:raise RuntimeError('Expected one seam: '+a)
 s=s.replace(a,b,1)
once('<script src="stella-storage.js"></script>','<script src="wetlands-preview.js"></script><script src="stella-storage.js"></script>')
once('<aside id="patch-watch-hud"', (root/'wetlands-banner.html').read_text()+'<aside id="patch-watch-hud"')
once("document.getElementById('life-habitat').textContent='';", "document.getElementById('wetlands-readout').textContent='';document.getElementById('life-habitat').textContent='';")
once('<p id="life-habitat"', '<p id="wetlands-readout" style="white-space:pre-line"></p><p id="life-habitat"')
once("  if(!Array.isArray(data.cohorts))throw Error('Invalid snapshot');", "  if(!Array.isArray(data.cohorts))throw Error('Invalid snapshot');\n  let wetlands=null;try{if(typeof Module._stella_wetlands_snapshot==='function')wetlands=JSON.parse(Module.ccall('stella_wetlands_snapshot','string',[],[]));}catch{}\n  document.getElementById('wetlands-readout').textContent=(typeof StellaWetlands==='undefined'?'Wetlands conditions unavailable.':StellaWetlands.summary({...data,wetlands}));")
once("status.textContent='Startup failed. The diagnostics below show the exact error.';", "status.textContent=(typeof StellaWetlands==='undefined'?null:StellaWetlands.graphicsFailure(reason))||'Startup failed. The diagnostics below show the exact error.';")
once("const storage=createStellaStorage(Module,feedback,{preserveLegacyThroughVersion:6});", """const storage=createStellaStorage(Module,feedback,{preserveLegacyThroughVersion:6});
if(typeof StellaWetlands!=='undefined'){StellaWetlands.mount(document,{
 available:()=>Module.started&&!Module.failed&&!document.hidden&&!storage.state().busy&&typeof Module._stella_wetlands_new==='function'&&typeof Module._stella_wetlands_snapshot==='function'&&(typeof advanceDay==='undefined'||!advanceDay.isLocked()),
 snapshot:()=>JSON.parse(Module.ccall('stella_wetlands_snapshot','string',[],[])),
 confirm:message=>window.confirm(message),
 create:world=>Module.ccall('stella_wetlands_new','number',['number'],[world]),
 created:()=>{syncWorldMode();refreshStarter();feedback('Fresh Wetlands preview. Seed uses existing resources; roots may arise in later offspring, not founders.');}
});
function refreshWetlandsLaw(){
 if(document.hidden)return;
 let state=null;try{if(Module.started&&!Module.failed&&typeof Module._stella_wetlands_snapshot==='function')state=JSON.parse(Module.ccall('stella_wetlands_snapshot','string',[],[]));}catch{}
 document.getElementById('wetlands-active-law').textContent=StellaWetlands.activeLaw(state);
}
setInterval(refreshWetlandsLaw,1500);
document.getElementById('wetlands-notice').addEventListener('toggle',refreshWetlandsLaw);}
""")
once("const welcomeKey='stella-guide-dismissed-v1';","const welcomeKey='stella-wetlands-guide-dismissed-v1';")
if '/saves' not in t:raise RuntimeError('Missing storage namespace')
t=t.replace('/saves','/wetlands-saves')
assert '/saves' not in t
build=out/'build.sh'
build_text=build.read_text() if build.exists() else None
if build_text is not None:
 seam='cp web/stella-storage.js web/dist/stella-storage.js'
 if build_text.count(seam)!=1:raise RuntimeError('Missing unique build storage seam')
 if 'cp web/wetlands-preview.js web/dist/wetlands-preview.js' not in build_text:build_text=build_text.replace(seam,seam+'\ncp web/wetlands-preview.js web/dist/wetlands-preview.js')
# Complete validation before writing either file.
if build_text is not None:build.write_text(build_text)
html.write_text(s);storage.write_text(t);shutil.copy2(root/'wetlands-preview.js',out/'wetlands-preview.js')
print('Patched isolated Wetlands frontend; native namespace and law gates still required.')

# Existing storage fixtures must exercise the same isolated namespace, not root saves.
fixture=out/'tests/storage-upgrade.test.cjs'
if fixture.exists():fixture.write_text(fixture.read_text().replace('/saves','/wetlands-saves'))
