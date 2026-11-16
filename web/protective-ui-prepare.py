from pathlib import Path
import shutil
r=Path(__file__).resolve().parents[1];o=r.parent/'site-tmp/protective-ui/web'
if not o.exists():shutil.copytree(r.parent/'site-tmp/root-water-ui/web',o,ignore=shutil.ignore_patterns('dist','node_modules','.cache'))
for source,target in [('protective-combined.js','combined-world.js'),('protective-traits.js','combined-traits.js'),('protective-inspection.js','protective-inspection.js')]:shutil.copy2(r/'web'/source,o/target)
p=o/'shell.html';s=p.read_text()
if 'id="rooted-founder-help"' not in s:
 hint='<p id="rooted-founder-help">Pause and select a patch. <b>Plant rooted founder…</b> previews its water support before you confirm; Cancel plants nothing.<br>If root water is missing, try <b>Water +</b> on that patch, run the simulation or use Advance, then pause and preview again. Soil needs time to take up water; rain and drying vary.<br>Choose Standard or Hardy, then confirm only when you are ready. Water support is a current check, not a survival promise.</p>'
 s=s.replace('<button id="rooted-founder-open">Plant rooted founder…</button>','<button id="rooted-founder-open">Plant rooted founder…</button>'+hint)

if 'id="combined-protective"' not in s:
 needle='<button id="combined-new">';assert s.count(needle)==1
 s=s.replace(needle,'<label id="combined-protective-choice" hidden style="min-height:44px"><input id="combined-protective" type="checkbox" style="min-width:24px;min-height:24px">Evolving cold/heat protection (new world only) · Adds simulation work and may run slower</label>'+needle)
 s=s.replace("canCreate:choice=>choice!=='calmer'||typeof Module._stella_combined_calm_new==='function'", "canCreate:choice=>choice==='protective'?typeof Module._stella_combined_protective_new==='function':choice!=='calmer'||typeof Module._stella_combined_calm_new==='function'")
 s=s.replace("choice==='calmer'?'stella_combined_calm_new'", "choice==='protective'?'stella_combined_protective_new':choice==='calmer'?'stella_combined_calm_new'")
 s=s.replace('<script src="combined-traits.js"></script>','<script src="combined-traits.js"></script><script src="protective-inspection.js"></script>')
 needle='  rows.textContent=living.length?';assert s.count(needle)==1
 s=s.replace(needle,"  let protective=null;try{if(typeof Module._stella_protective_snapshot==='function')protective=JSON.parse(Module.ccall('stella_protective_snapshot','string',[],[]));}catch{}\n"+needle)
 needle='StellaCombinedTraits.aerial(c,data,combined))';assert s.count(needle)==1
 s=s.replace(needle,needle+"+(typeof StellaProtective==='undefined'?'':StellaProtective.describe(c,data,combined,protective))")
 p.write_text(s)
for name in ['protective-ui.test.cjs']:
 if (r/'web/tests'/name).exists():shutil.copy2(r/'web/tests'/name,o/'tests'/name)

p=o/'build.sh';s=p.read_text()
if '_stella_protective_snapshot,' not in s:s=s.replace('-sEXPORTED_FUNCTIONS=','-sEXPORTED_FUNCTIONS=_stella_combined_protective_new,_stella_protective_snapshot,')
if 'cp web/protective-inspection.js' not in s:s+='\ncp web/protective-inspection.js web/dist/protective-inspection.js\n'
p.write_text(s)
(o/'tests/fixtures').mkdir(exist_ok=True)
for state in ['active','protecting','recovering']:shutil.copy2(r/f'web/tests/continuation-review/protective-integration/{state}-snapshot.json',o/f'tests/fixtures/protective-{state}.json')
