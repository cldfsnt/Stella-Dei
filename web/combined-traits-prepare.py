from pathlib import Path
import shutil,sys,json
r=Path(__file__).resolve().parent;o=Path(sys.argv[1]).resolve();assert o.name=='web'and o.parent.name=='combined-playtest'
p=o/'shell.html';s=p.read_text();assert 'combined-traits.js'not in s;s=s.replace('<script src="combined-world.js"></script>','<script src="combined-traits.js"></script><script src="combined-world.js"></script>',1)
a="  document.getElementById('wetlands-readout').textContent=";assert s.count(a)==1;s=s.replace(a,"  let combined=null;try{if(typeof Module._stella_combined_snapshot==='function')combined=JSON.parse(Module.ccall('stella_combined_snapshot','string',[],[]));}catch{}\n"+a,1)
a="+producerFeedback(c.tissue)+movementFeedback(c)";assert s.count(a)==1;s=s.replace(a,"+(typeof StellaCombinedTraits==='undefined'?'':StellaCombinedTraits.aerial(c,data,combined))+producerFeedback(c.tissue)+movementFeedback(c)",1);p.write_text(s)
shutil.copy2(r/'combined-traits.js',o/'combined-traits.js');shutil.copy2(r/'tests/combined-traits.test.cjs',o/'tests/combined-traits.test.cjs')
p=o/'build.sh';s=p.read_text()+'\ncp web/combined-traits.js web/dist/combined-traits.js\n';p.write_text(s)
p=o/'tests/shell.test.cjs';s=p.read_text().replace('const sandbox={',"const sandbox={StellaCombinedTraits:require('../combined-traits.js'),",1)
a="console.log('PASS: production shell ID wiring, More/Close/Help flows, save and cancelled/confirmed load');";assert s.count(a)==1
s=s.replace(a,"""// Genuine day7 seed1337 descendant121 at3420, not assumed wind-born.
sandbox.Module._stella_combined_snapshot=()=>0;
const real={biomass:.012212320230901241,aerial_allocation:.45650163292884827,lineage:121,parent:28,generation:1};
sandbox.Module.ccall=name=>JSON.stringify(name==='stella_combined_snapshot'?{status:'combined',world_serial:4,writer_version:13,enabled:true,root_physiology:3,wind_law:1}:name==='stella_wetlands_snapshot'?{status:'unavailable'}:{status:'origin',cell:3420,world_serial:4,paused:true,cohorts:[real],identities:[{id:'121',parent:'28',living:true,generation:1}]});
sandbox.refreshLife();assert.match(el('life-cohorts').textContent,/Colony ID #121/);assert.match(el('life-cohorts').textContent,/Aerial route allocation 45.7%/);assert.match(el('life-cohorts').textContent,/Birth route not recorded/);
"""+a,1);p.write_text(s)
