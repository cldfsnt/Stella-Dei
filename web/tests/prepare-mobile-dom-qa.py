#!/usr/bin/env python3
"""Actual production HTML/CSS/controllers, explicit mocked native bridge, no WebGL/IDB."""
from pathlib import Path
import shutil,json
R=Path(__file__).resolve().parents[2]; W=R.parent/'site-tmp/mobile-ux/web'; Q=R.parent/'mobile-ux-dom-qa'; D=Q/'staticdist';D.mkdir(parents=True,exist_ok=True);(Q/'.openai').mkdir(exist_ok=True)
(Q/'.openai/hosting.json').write_text('{"static":{"directory":"staticdist"}}\n')
for p in W.glob('*.js'):shutil.copy2(p,D/p.name)
shutil.copy2(W/'mobile-navigation.css',D/'mobile-navigation.css')
s=(W/'shell.html').read_text().replace('{{{ SCRIPT }}}','').replace('<script src="mobile-navigation-bindings.js">','<script src="qa-native-mock.js"></script><script src="mobile-navigation-bindings.js">')
(D/'game.html').write_text(s)
(D/'qa-native-mock.js').write_text(r'''
// QA ONLY: native calls mocked, no engine or storage initialized.
const QA={calls:[],state:{available:true,paused:true,world_serial:1,tool:0,day:7,speed:21600}};window.QA=QA;
Module.started=true;Module.failed=false;document.body.classList.add('playing');document.getElementById('cover').hidden=true;document.getElementById('welcome-tip').hidden=true;
const fixture={status:'origin',world_serial:1,cell:334,paused:true,water_m:.01,temperature_c:24,simulation_light:1,seed_reason:'eligible'};
const combined={status:'combined',world_serial:1,writer_version:15,enabled:true,root_physiology:3,wind_law:1,ground_thermal_law:1,protective_law:1,aerial_allocations:[]};
const names=['Microbial mat','Cushion','Rosette','Ribbon','Branching','Canopy'];
Module.ccall=(name,type,types,args=[])=>{QA.calls.push({name,args});let value;
if(name==='stella_mobile_snapshot')value=QA.state;
else if(name==='stella_mobile_pause'){QA.state.paused=!!args[1];return 1;}
else if(name==='stella_mobile_tool'){QA.state.tool=args[1];return 1;}
else if(name==='stella_combined_snapshot')value=combined;
else if(name==='stella_wetlands_snapshot')value={status:'wetlands',enabled:true,world_serial:1,currentcell:334,cell:334,physiology_law:3,root_allocations:[],soil_kg_m2:.1,receipt_available:false};
else if(name==='stella_life_snapshot')value=fixture;
else if(name==='stella_speed_snapshot')value={requested:QA.state.speed,achieved:20000,paused:QA.state.paused,step:1440};
else if(name==='stella_world_ecology')value={status:'ready',mode:'origin',world:1,colonies:21,forms:names.map((form,i)=>({form,form_id:i,colony_count:i+1,biomass_sum:(i+1)/100})),census_start_time:604800,census_end_time:604800,recent:null};
else if(name==='stella_god_target')value={status:'ready',cell:334,water_m:.01,temperature_c:24,eligibility:{wave:'none',lightning:'none',scorch:'origin',ignition:'wet'}};
else if(name==='stella_set_speed'){QA.state.speed=args[0];return 1;}
else if(type==='string')value={status:'unavailable'};else return 1;
return JSON.stringify(value);};
for(const n of ['web_shell_set','mobile_snapshot','mobile_pause','mobile_tool','mobile_climate','combined_snapshot','wetlands_snapshot','life_snapshot','world_ecology','speed_snapshot','god_target','set_speed','seed_colony','auto_seed_start','wetlands_combined_new','combined_protective_new','seed_pioneer','save_expected','hardy_rooted_founder_preview','rooted_founder_preview','seed_rooted','rooted_founder_cancel'])Module['_stella_'+n]=(...a)=>Module.ccall('stella_'+n,'number',[],a);
Module._stella_world_mode=()=>1;Module._stella_seed_targets=()=>1;Module._stella_arrival_effects=()=>1;Module._stella_scene_resolution_get=()=>100;Module._stella_scene_resolution_set=()=>1;
window.confirm=()=>false;syncWorldMode();refreshStarter();
''')
(D/'index.html').write_text('''<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><title>Mobile navigation DOM QA</title><style>body{font:16px system-ui;background:#e7edf0;color:#10212b}iframe{border:2px solid #637582;display:block;margin:12px 0}button{min-height:44px}pre{white-space:pre-wrap}</style><h1>Actual HTML/CSS · mocked native engine</h1><p>No game rendering, physics, device performance or actual save operations. Fresh QA page only.</p><button onclick="size(320,568)">320 × 568</button><button onclick="size(390,700)">390 × 700</button><button onclick="size(700,390)">700 × 390</button><button onclick="run()">Run DOM checks</button><pre id="result">Choose a viewport; interact with the dock below.</pre><iframe id="game" title="Actual game navigation with mocked native actions" src="game.html" width="390" height="700"></iframe><script>
function size(w,h){game.width=w;game.height=h;}async function run(){const w=game.contentWindow,d=w.document,out=[];const check=(name,ok)=>{out.push({name,pass:!!ok});if(!ok)throw Error(name);};try{check('no startup error',!w.Module.failed);check('exactly six dock controls',d.querySelectorAll('#mobile-dock>button').length===6);check('no horizontal overflow',d.documentElement.scrollWidth<=d.documentElement.clientWidth);check('old navigation hidden',w.getComputedStyle(d.getElementById('controls')).display==='none');check('group navigation hidden',w.getComputedStyle(d.getElementById('menu-groups')).display==='none');for(const b of d.querySelectorAll('#mobile-dock>button'))check('touch target '+b.id,b.getBoundingClientRect().height>=44);d.getElementById('dock-god').click();check('God opens directly',d.getElementById('god-sheet').open);d.querySelector('[data-mobile-tool="1"]').click();check('Water chosen second tap',w.QA.state.tool===1);check('sheet closes after brush',d.querySelectorAll('dialog[open]').length===0);d.getElementById('mobile-brush-cancel').click();check('Explore cancels actual selection',w.QA.state.tool===0);d.getElementById('dock-stats').click();check('six current form buttons',d.querySelectorAll('#world-form-actions button').length===6);d.getElementById('dock-world').click();check('one sheet only',d.querySelectorAll('dialog[open]').length===1);check('World selected',!d.getElementById('group-world').hidden);check('no save/new/load dispatch from navigation',!w.QA.calls.some(x=>/save_expected|combined_protective_new|recovery_apply|seed_rooted/.test(x.name)));}catch(e){out.push({error:String(e)});}result.textContent=JSON.stringify({viewport:[game.width,game.height],checks:out},null,2);}
</script>''')
print(Q)
