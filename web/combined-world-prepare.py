"""Patch a new isolated hardy Wetlands frontend, never existing runtimes."""
from pathlib import Path
import shutil,sys
root=Path(__file__).resolve().parent;out=Path(sys.argv[1]).resolve();assert out.name=='web'and out.parent.name=='root-wind-ui'
p=out/'shell.html';s=p.read_text();assert 'combined-new'not in s
s=s.replace('<script src="wetlands-preview.js"></script>','<script src="combined-world.js"></script><script src="wetlands-preview.js"></script>',1)
s=s.replace('<h3>World</h3>','<h3>World</h3><button id="combined-new">Save + new combined Wetlands world…</button><button id="combined-refresh">Refresh combined-law status</button><p id="combined-status" role="status"></p><details id="combined-disclosure"><summary>Combined roots and dispersal</summary><p>Explicit new-world choice only. Finite soil and inherited roots remain; paid Pioneer founders start with 50% aerial allocation and no roots. Aerial allocation redirects existing reproductive opportunities, not extra births. Wind arrivals can fail; surviving descendants are not guaranteed. Standard Wetlands and imported older worlds are not converted.</p></details>',1)
s=s.replace('<h3>Plant</h3>','<h3>Plant</h3><button id="combined-pioneer" disabled>Plant paid Pioneer here · 50% aerial allocation</button><button id="combined-pioneer-batch" disabled>Plan Pioneer Auto-seed…</button>',1)
needle="const storage=createStellaStorage(Module,feedback,{preserveLegacyThroughVersion:6});";assert s.count(needle)==1
s=s.replace(needle,"""const storage=createStellaStorage(Module,feedback,{preserveLegacyThroughVersion:6,readWriterIdentity:()=>JSON.parse(Module.ccall('stella_combined_snapshot','string',[],[]))});
const combinedUI=StellaCombined.mount(document,{
 available:()=>Module.started&&!Module.failed&&!document.hidden&&!storage.state().busy&&!advanceDay.isLocked()&&['_stella_combined_snapshot','_stella_wetlands_combined_new','_stella_seed_pioneer','_stella_save_expected'].every(k=>typeof Module[k]==='function'),
 read:()=>JSON.parse(Module.ccall('stella_combined_snapshot','string',[],[])),life:()=>JSON.parse(Module.ccall('stella_life_snapshot','string',[],[])),
 confirm:message=>window.confirm(message),save:()=>storage.save(),fresh:world=>Module.ccall('stella_wetlands_combined_new','number',['number'],[world]),
 pioneer:(world,point)=>Module.ccall('stella_seed_pioneer','number',['number','number'],[world,point]),message:feedback,changed:()=>{syncWorldMode();refreshStarter();}
});
""",1)
s=s.replace('function selectToolGroup(group){','function selectToolGroup(group){if(typeof combinedUI!==\'undefined\')combinedUI.refresh();',1)
s=s.replace('AutoSeed.create({available:','AutoSeed.create({requireFounderKind:true,available:',1)
a=s.index("document.getElementById('auto-seed-open').onclick=()=>{");b=s.index("\ndocument.getElementById('auto-seed-apply')",a)
body=s[a:b].replace("document.getElementById('auto-seed-open').onclick=()=>{","function openCombinedSeed(kind){if(storage.state().busy||advanceDay.isLocked()){feedback('Finish saving or advancing before planning.');return;}")
body=body.replace("const sheet=document.getElementById('auto-seed-sheet');","document.getElementById('auto-seed-title').textContent=kind==='pioneer'?'Pioneer Auto-seed · chosen 50% aerial allocation':'Auto-seed world · ordinary founders';const sheet=document.getElementById('auto-seed-sheet');")
body=body.replace('autoSeed.start(data.world_serial);',"if(kind==='pioneer'){const w=JSON.parse(Module.ccall('stella_combined_snapshot','string',[],[]));if(w.status!=='combined'||!w.enabled||w.world_serial!==data.world_serial)throw Error('Pioneer planning requires the current combined world.');}autoSeed.start(data.world_serial,kind);")
s=s[:a]+body+"\ndocument.getElementById('auto-seed-open').onclick=()=>openCombinedSeed('ordinary');\ndocument.getElementById('combined-pioneer-batch').onclick=()=>openCombinedSeed('pioneer');"+s[b:]
s=s.replace('<script src="combined-world.js">','<style>#rooted-founder-variant{min-height:44px;font:inherit;width:100%;max-width:100%;min-width:0;box-sizing:border-box;background:#102c30;color:#f4fff8;border:1px solid #8aada6;border-radius:6px}#combined-disclosure{position:static;bottom:auto;max-width:100%;overflow-wrap:anywhere}#combined-disclosure:not([open]){display:block}</style>'+'<script src="combined-world.js">',1)
p.write_text(s)
for source,dest in [('combined-world.js','combined-world.js'),('combined-storage.js','stella-storage.js'),('wind-auto-seed.js','auto-seed.js')]:shutil.copy2(root/source,out/dest)
p=out/'build.sh';s=p.read_text();s=s.replace('-sEXPORTED_FUNCTIONS=','-sEXPORTED_FUNCTIONS=_stella_wetlands_combined_new,_stella_combined_snapshot,_stella_save_expected,_stella_seed_pioneer,_stella_auto_seed_pioneer_start,',1);s+='\ncp web/combined-world.js web/dist/combined-world.js\n';p.write_text(s)
p=out/'tests/shell.test.cjs';s=p.read_text().replace('const sandbox={',"const sandbox={StellaCombined:require('../combined-world.js'),",1);p.write_text(s)
