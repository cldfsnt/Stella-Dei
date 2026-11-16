"""Isolated one-main-flow frontend only; native/storage ownership is separate."""
from pathlib import Path
import shutil,re
r=Path(__file__).resolve().parents[1];o=r.parent/'site-tmp/unified-ui/web';base=r.parent/'site-tmp/protective-ui/web'
if not o.exists():shutil.copytree(base,o,ignore=shutil.ignore_patterns('dist','node_modules','.cache'))
s=(base/'shell.html').read_text()
s,n=re.subn(r'<details id="wetlands-notice"[\s\S]*?</details>','',s,count=1);assert n==1
start=s.index("if(typeof StellaWetlands!=='undefined'){StellaWetlands.mount")
end=s.index("\nconst lifeTrend=",start);s=s[:start]+s[end:]
# Retain read-only root/soil summary and graphics diagnostic helper; remove only its obsolete mount.
a=s.index('<label for="combined-climate">');b=s.index('<button id="combined-new">',a);s=s[:a]+s[b:]
s=s.replace('Save + new combined Wetlands world…','Save + new living planet…').replace('Refresh combined-law status','Refresh world details').replace('Wetlands · optional roots + wind','Stella Dei · evolving worlds')
s=s.replace('<h3>World</h3>','<h3>World</h3><button id="continue-world">Continue open world</button><p>New living planets include finite soil, wind dispersal and evolving cold/heat protection. Open older saves keeps their original rules.</p>',1)
a=s.index('<details id="combined-disclosure">');b=s.index('</details>',a)+len('</details>');s=s[:a]+'<details id="combined-disclosure"><summary>How this world evolves</summary><p>New worlds begin with simple life. Roots, wind dispersal and cold/heat protection are inherited strategies with costs, not guaranteed land establishment. Evolving protection adds simulation work and may run slower. Older loaded worlds keep their saved rules.</p></details>'+s[b:]
s=s.replace('<b>Choose your living world.</b> Origin begins with simple microbes; Sandbox offers plants and rabbits. Choose Random or Continents for a new world. Pinch to zoom; drag to explore.','<b>Start a living planet.</b> Find water, seed simple aquatic life, then watch its descendants. World opens your saved planets; God tools are optional assistance. Pinch to zoom; drag to explore.')
s=s.replace('Open older saves keeps','Opening older saves keeps')
# Move chosen founder tools, not their IDs/controllers, out of the normal aquatic start path.
a=s.index('<label for="rooted-founder-variant">');b=s.index('<button id="seed-targets-toggle"',a);rooted=s[a:b];s=s[:a]+s[b:]
rooted=rooted.replace('Plant rooted founder…','Preview land starter…').replace('Rooted founder</label>','Assisted rooted founder</label>')
pioneer='<button id="combined-pioneer" disabled>Plant paid Pioneer here · 50% aerial allocation</button><button id="combined-pioneer-batch" disabled>Plan Pioneer Auto-seed…</button>';assert s.count(pioneer)==1;s=s.replace(pioneer,'')
needle='<p id="god-target">';assert s.count(needle)==1
s=s.replace(needle,'<p>Optional assisted actions, not natural evolution. Founders use real resources and suitable habitat; choosing genetics does not guarantee survival. Water and terrain tools deliberately change the environment.</p><details id="assisted-founders"><summary>Jump-start life · chosen founders</summary>'+rooted+pioneer+'</details>'+needle)
s=s.replace('God tools · deliberate interventions','God tools · optional assistance').replace('<button id="god-toggle">God tools</button>','<button id="god-toggle">Show God tools</button>')
s=s.replace("document.getElementById('more-menu').close();refreshLife();document.getElementById('cohort-details').open=true", "document.getElementById('more-menu').close();document.getElementById('god-sheet').close();refreshLife();document.getElementById('cohort-details').open=true")
s=s.replace("canCreate:choice=>choice==='protective'?typeof Module._stella_combined_protective_new==='function':choice!=='calmer'||typeof Module._stella_combined_calm_new==='function'", "canCreate:()=>typeof Module._stella_combined_protective_new==='function'")
s=s.replace("fresh:(world,choice)=>Module.ccall(choice==='protective'?'stella_combined_protective_new':choice==='calmer'?'stella_combined_calm_new':'stella_wetlands_combined_new','number',['number'],[world])", "fresh:world=>Module.ccall('stella_combined_protective_new','number',['number'],[world])")
s=s.replace("const combinedUI=StellaCombined.mount(document,{", "document.getElementById('continue-world').onclick=()=>document.getElementById('more-menu').close();\nconst combinedUI=StellaCombined.mount(document,{")
s=s.replace('<details id="assisted-founders"><summary>Jump-start life · chosen founders</summary>','<section id="assisted-founders"><h3>Land starter · assisted life</h3><p>Select a patch → Preview land starter → Plant. Uses existing resources and suitable moist habitat; does not supply water. Lasting land life is not guaranteed.</p>').replace(pioneer+'</details>'+needle,pioneer+'</section>'+needle)
library='<details id="world-library"><summary>Open a saved planet</summary><p>Start Play, then pause before opening a save. Starting the game does not save over your planet. Choose a save explicitly; originals remain unchanged. Multiple histories are never merged.</p><label for="world-library-source">Save history</label><select id="world-library-source"><option value="current">Saved planets</option><option value="main">Earlier main game</option><option value="wind">Earlier Wind worlds</option></select><button id="world-library-refresh">Find saved planets</button><label for="world-library-entry">Planet</label><select id="world-library-entry"></select><button id="world-library-import" disabled>Open selected planet…</button><button id="world-library-download" disabled>Download a copy</button><button id="world-library-cancel">Cancel selection</button><p id="world-library-status" role="status" aria-live="polite"></p></details>'
s=s.replace('<details id="backup-recovery">',library+'<details id="backup-recovery">',1)
s=s.replace('<script src="combined-recovery.js"></script>','<script src="combined-recovery.js"></script><script src="world-library.js"></script>')
needle='const combinedUI=StellaCombined.mount(document,{'
s=s.replace(needle,'''const worldLibrary=StellaWorldLibrary.mount(document,{
 storage,available:()=>Module.started&&!Module.failed&&!document.hidden&&!storage.state().busy&&!advanceDay.isLocked(),confirm:message=>window.confirm(message),
 message:message=>{document.getElementById('world-library-status').textContent=message;feedback(message);},changed:()=>{syncWorldMode();refreshStarter();},
 download:(bytes,name)=>{const url=URL.createObjectURL(new Blob([bytes],{type:'application/json'})),a=document.createElement('a');a.href=url;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),30000);}
});
'''+needle)
s=s.replace("#rooted-founder-variant{", "#world-library select{min-height:44px;font:inherit;width:100%;max-width:100%;background:#102c30;color:#f4fff8}#world-library{position:static;bottom:auto}#world-library:not([open]){display:block}#rooted-founder-variant{")
(o/'shell.html').write_text(s)
shutil.copy2(r/'web/world-library.js',o/'world-library.js')
shutil.copy2(r/'web/unified-world.js',o/'combined-world.js')

shutil.copy2(r/'web/unified-habitat-summary.js',o/'wetlands-preview.js')
p=o/'shell.html';s=p.read_text();needle='function refreshStarter(){'
s=s.replace(needle,"""function refreshRootedAccess(){let w=null;try{if(Module.started&&!Module.failed&&typeof Module._stella_wetlands_snapshot==='function')w=JSON.parse(Module.ccall('stella_wetlands_snapshot','string',[],[]));}catch{}const allowed=w&&w.status==='wetlands'&&w.enabled===true&&w.physiology_law===3;document.getElementById('rooted-founder-open').disabled=!allowed||storage.state().busy;document.getElementById('rooted-founder-variant').disabled=!allowed||storage.state().busy;if(!allowed)document.getElementById('rooted-founder-status').textContent='Available in a new living planet; this saved world is unchanged.';}
function refreshStarter(){
 refreshRootedAccess();""")
s=s.replace("refreshGodTarget();document.getElementById('god-sheet').showModal();", "refreshRootedAccess();refreshGodTarget();document.getElementById('god-sheet').showModal();")
p.write_text(s)
p=o/'build.sh';s=p.read_text()
if 'cp web/world-library.js' not in s:s+='\ncp web/world-library.js web/dist/world-library.js\n'
p.write_text(s)

for name in ['world-library.test.cjs']:shutil.copy2(r/'web/tests'/name,o/'tests'/name)
