const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const html=fs.readFileSync(require('node:path').join(__dirname,'../shell.html'),'utf8');
assert.match(html,/a <b>Water \+<\/b> tap adds 1 m to the selected patch/);assert.match(html,/no automatic refill or guaranteed evolution/);assert.match(html,/Water −<\/b> removes up to 1 m per tap from only the selected patch/);assert.match(html,/never drains neighbors/);
assert.match(html,/body #origin-starter\{position:static;flex:none;display:block;width:auto;inset:auto;max-height:180px/);
assert.match(html,/body #origin-starter:not\(\[open\]\)\{display:block\}/);
assert.match(html,/body #origin-starter:not\(\[open\]\)>:not\(summary\)\{display:none\}/);
assert.match(html,/body #origin-starter\[hidden\]\{display:none\}/);
assert.match(html,/body #performance-details\{position:static;display:block;inset:auto/);assert.match(html,/body #performance-details:not\(\[open\]\)\{display:block\}/);
assert.match(html,/#life-sheet \.sheet-heading,#god-sheet \.sheet-heading,#speed-sheet \.sheet-heading\{position:sticky;top:-16px;background:#102c30/);
assert.match(html,/body #close-speed\{flex:none;min-width:64px;min-height:44px\}/);
assert.match(html,/body #speed-sheet\{overscroll-behavior:contain;scroll-padding-top:68px\}/);
assert.match(html,/#life-sheet,#god-sheet,#speed-sheet\{[^}]*width:min\(450px,calc\(100vw - 16px\)\);max-height:80dvh;overflow:auto/);
assert.match(html,/body #speed-sheet \.sheet-heading\{z-index:5/);
assert.match(html,/Nothing is uploaded; closing stops measurement/);
const godDialog=html.slice(html.indexOf('<dialog id="god-sheet"'),html.indexOf('</dialog>',html.indexOf('<dialog id="god-sheet"')));
for(const id of ['god-wave','god-heat','god-scorch','god-ignite'])assert.ok(godDialog.indexOf('id="'+id+'"')<godDialog.indexOf('id="god-help"'),'All actions precede long explanations');
assert.ok(godDialog.indexOf('id="ignition-ledger"')<godDialog.indexOf('id="god-help"'),'Last receipt independent before help');
assert.match(html,/body #god-sheet details\{position:static;display:block;inset:auto/);
assert.match(html,/body #god-sheet details:not\(\[open\]\)\{display:block\}/);
assert.match(html,/body #god-sheet details:not\(\[open\]\)>:not\(summary\)\{display:none\}/);
assert.match(html,/body #god-sheet details\[hidden\]\{display:none\}/);
assert.match(html,/body #god-actions\{display:grid;grid-template-columns:1fr 1fr/);
const ids=[...html.matchAll(/id="([^"]+)"/g)].map(m=>m[1]);assert.equal(new Set(ids).size,ids.length,'Duplicate DOM ids');
const elements=new Map(ids.map(id=>[id,{id,hidden:id==='guide',disabled:false,open:false,dataset:{},handlers:{},addEventListener(type,fn){this.handlers[type]=fn;},setAttribute(k,v){this[k]=v;},focus(){},setPointerCapture(){},hasPointerCapture(){return false;},dispatchEvent(){},appendChild(){},querySelector(){return {textContent:''}},getBoundingClientRect(){return{left:10,top:100,right:300,bottom:400,width:390,height:700}},showModal(){this.open=true},close(){this.open=false}}]));
elements.set('diagnostics',{textContent:''});
const preferences=new Map();
let reset=0,saves=0,loads=0;const state={available:true,busy:false};
const documentEvents={};
const intervalJobs=[];let fakeNow=0;
const sandbox={StellaRendererInfo:require('../renderer-info.js'),StellaPatchWatch:require('../patch-watch.js'),clearInterval(){},createGameplayMeasure:require('../gameplay-measure.js').create,performance:{now:()=>fakeNow},StellaLifeTrend:require('../life-trend.js'),console,setInterval(fn,ms){intervalJobs.push({fn,ms})},localStorage:{getItem:k=>preferences.get(k),setItem:(k,v)=>preferences.set(k,v)},setTimeout:()=>1,clearTimeout(){},requestAnimationFrame(){},ResizeObserver:class{observe(){}},MouseEvent:class{},KeyboardEvent:class{},confirm:()=>false,location:{reload(){}},createStellaTouchControls:()=>({reset(){reset++},setMode(){},down(){},move(){},up(){}}),createStellaStorage:()=>({state:()=>state,initialize:async()=>true,save:async()=>{saves++},load:async()=>{loads++;return true}})};
sandbox.window=sandbox;sandbox.addEventListener=()=>{};sandbox.document={getElementById:id=>{assert.ok(elements.has(id),`Missing id ${id}`);return elements.get(id)},createElement:()=>({innerHTML:'',open:false}),querySelector:()=>({append(){}}),querySelectorAll:()=>[],addEventListener(type,fn){(documentEvents[type]??=[]).push(fn)},body:{classList:{add(){},remove(){}}},documentElement:{requestFullscreen:async()=>{}},fullscreenElement:null};
vm.createContext(sandbox);vm.runInContext(html.split('<script>')[1].split('</script>')[0],sandbox);
const observed={status:'origin',cohorts:[{biomass:.08,feeding:.2,support_mass:.01},{biomass:.02,feeding:0,support_mass:0}]};
const immutable=JSON.stringify(observed);const competition=sandbox.competitionFeedback(observed);
assert.match(competition,/largest holds 80%/);assert.match(competition,/1 grazing-capable resident/);assert.match(competition,/not grazing armor/);assert.equal(JSON.stringify(observed),immutable);
assert.equal(sandbox.competitionFeedback({status:'sandbox',cohorts:[]}), '');
assert.equal(sandbox.competitionFeedback({status:'origin',cohorts:[{biomass:NaN}]}), '');
assert.match(sandbox.competitionFeedback({status:'origin',cohorts:[]}),/not necessarily safe/);
assert.doesNotMatch(sandbox.competitionFeedback({status:'origin',cohorts:[{biomass:.1,feeding:0,support_mass:0}]}),/grazing-capable|Paid support/);
assert.match(sandbox.competitionFeedback({status:'origin',cohorts:Array.from({length:4},()=>({biomass:.02}))}),/All four colony slots/);

(async()=>{const el=id=>elements.get(id);el('more-toggle').onclick();assert.ok(el('more-menu').open);el('close-more').onclick();assert.ok(!el('more-menu').open);el('more-toggle').onclick();el('help-toggle').onclick();assert.ok(!el('more-menu').open);assert.equal(el('guide').hidden,false);el('close-guide').onclick();assert.equal(el('guide').hidden,true);
sandbox.Module.started=true;el('more-toggle').onclick();await el('save-world').onclick();assert.equal(saves,1);assert.equal(el('more-menu').open,false);assert.equal(el('save-world').disabled,false);
await el('load-world').onclick();assert.equal(loads,0,'Cancelled load must not load');sandbox.confirm=()=>true;await el('load-world').onclick();assert.equal(loads,1);assert.ok(reset>=5);
// No runtime / missing goal export yields honest setup guidance, never a success.
sandbox.Module.started=false;el('help-toggle').onclick();assert.match(el('goal-title').textContent,/Start or load/);
sandbox.Module.started=true;el('check-habitat').onclick();assert.match(el('goal-title').textContent,/Start or load/);
sandbox.Module._stella_goal_stage=()=>2;el('check-habitat').onclick();assert.ok(el('goal-text').textContent.length>20);
el('repeat-guide').onclick();assert.equal(el('manual').open,true);assert.equal(el('goal-title').textContent,'Start a habitat');
el('close-guide').onclick();el('help-toggle').onclick();assert.equal(el('guide').hidden,false);
preferences.clear();sandbox.showWelcome();assert.equal(el('welcome-tip').hidden,false);el('dismiss-guide').onclick();assert.equal(el('welcome-tip').hidden,true);sandbox.showWelcome();assert.equal(el('welcome-tip').hidden,true);
sandbox.localStorage.getItem=()=>{throw Error('blocked')};sandbox.localStorage.setItem=()=>{throw Error('blocked')};sandbox.showWelcome();el('dismiss-guide').onclick();assert.equal(el('welcome-tip').hidden,true);
sandbox.Module._stella_focus_land=()=>0;el('guide-land').onclick();assert.match(el('goal-text').textContent,/No dry land/);sandbox.Module._stella_focus_land=()=>1;el('guide-land').onclick();assert.equal(el('guide').hidden,true);
sandbox.Module._stella_goal_stage=()=>0;el('help-toggle').onclick();assert.equal(el('goal-title').textContent,'Start a habitat');
sandbox.Module._stella_world_mode=()=>1;sandbox.Module._stella_goal_stage=()=>100;el('help-toggle').onclick();assert.equal(el('land').textContent,'Habitat');assert.match(el('goal-text').textContent,/does not simulate abiogenesis/);el('repeat-guide').onclick();assert.equal(el('goal-title').textContent,'Seed existing simple life');sandbox.Module._stella_world_mode=()=>0;sandbox.syncWorldMode();assert.equal(el('land').textContent,'Land');
el('life-toggle').onclick();assert.equal(el('life-sheet').open,true);assert.match(el('life-summary').textContent,/Start or load/);el('close-life').onclick();assert.equal(el('life-sheet').open,false);
sandbox.Module._stella_life_snapshot=()=>1;sandbox.Module.ccall=()=>JSON.stringify({status:'origin',day:5,water_m:3,temperature_c:21,nutrients:.02,detritus:.001,simulation_light:0,cohorts:[{lineage:1,parent:0,biomass:.1,generation:0,optimum:303,efficiency:1},{lineage:2,parent:1,biomass:.02,generation:1,optimum:299,efficiency:1.1}]});
el('life-toggle').onclick();assert.match(el('life-cohorts').textContent,/parent ID #1/);assert.match(el('life-summary').textContent,/2 living colonies/);assert.match(el('life-glossary').textContent,/one in 512/);assert.match(el('life-glossary').textContent,/help, harm or make little difference/);assert.match(el('life-conditions').textContent,/Biological light 0.00/);
sandbox.Module.ccall=()=>JSON.stringify({status:'origin',cohorts:[]});el('refresh-life').onclick();assert.match(el('life-cohorts').textContent,/No living cohort/);
sandbox.Module.ccall=()=>JSON.stringify({status:'origin',cohorts:[{lineage:'<script>literal</script>',parent:'9007199254740999',biomass:.1,generation:3,optimum:300,efficiency:1,structure:.3}]});el('refresh-life').onclick();assert.match(el('life-cohorts').textContent,/<script>literal/);assert.match(el('life-cohorts').textContent,/Structure investment 30%/);assert.match(el('life-glossary').textContent,/not a real-world taxonomic/);
sandbox.Module.ccall=()=>JSON.stringify({status:'origin',cohorts:[{lineage:3,parent:1,biomass:.02,generation:2,optimum:300,efficiency:1,structure:.2,feeding:.08,lifetime_grazed:0},{lineage:4,parent:3,biomass:.03,generation:3,optimum:301,efficiency:1,feeding:.1,lifetime_grazed:.012345}]});el('refresh-life').onclick();assert.match(el('life-cohorts').textContent,/Grazing investment 8% · grazing-capable/);assert.match(el('life-cohorts').textContent,/No feeding recorded for this cohort/);assert.match(el('life-cohorts').textContent,/Has fed · recorded intake 0.012345 kg C\/m²/);assert.match(el('life-glossary').textContent,/resets in offspring/);assert.match(el('life-glossary').textContent,/not animals or new species/);
sandbox.Module.ccall=()=>JSON.stringify({status:'origin',cohorts:[{lineage:5,parent:0,biomass:.02,generation:0,optimum:300,efficiency:1,feeding:0,lifetime_grazed:0}]});el('refresh-life').onclick();assert.match(el('life-cohorts').textContent,/Grazing investment 0% · photosynthetic/);assert.doesNotMatch(el('life-cohorts').textContent,/Has fed/);
sandbox.Module.ccall=()=>JSON.stringify({status:'origin',cohorts:[{lineage:7,parent:2,biomass:.1,mobility:.25,relocations:2,last_from:25,last_to:26,last_move_time:129600}]});el('refresh-life').onclick();assert.match(el('life-cohorts').textContent,/Mobility investment 25%/);assert.match(el('life-cohorts').textContent,/Recorded patch relocations: 2/);assert.match(el('life-cohorts').textContent,/Moved to neighboring habitat on day 1.50\nPatch 25 → 26/);assert.match(el('life-glossary').textContent,/not individual animal travel/);
sandbox.Module.ccall=()=>JSON.stringify({status:'origin',cohorts:[{lineage:8,parent:7,biomass:.1,mobility:.25,relocations:0,last_from:25,last_to:26,last_move_time:129600}]});el('refresh-life').onclick();assert.match(el('life-cohorts').textContent,/No relocation recorded/);assert.doesNotMatch(el('life-cohorts').textContent,/Moved to neighboring habitat/);
assert.equal(sandbox.movementFeedback({}), '');assert.doesNotMatch(sandbox.movementFeedback({mobility:.1,relocations:1,last_from:NaN,last_to:3,last_move_time:0}),/Moved to neighboring habitat/);
sandbox.Module.ccall=()=>JSON.stringify({status:'origin',movement_reasons:['no_living_cohort','no_better_prey','eligible','no_mobility'],cohorts:[{biomass:0},{lineage:9,biomass:.1},{lineage:10,biomass:.2},{biomass:0}]});el('refresh-life').onclick();assert.match(el('life-cohorts').textContent,/Colony ID #9[\s\S]*No suitable neighbor has more living food/);assert.match(el('life-cohorts').textContent,/Colony ID #10[\s\S]*May move on a future simulation step/);assert.doesNotMatch(el('life-cohorts').textContent,/no mobility investment/);
assert.equal(sandbox.movementOpportunity('unknown'),'');assert.equal(sandbox.movementOpportunity('__proto__'),'');for(const reason of ['no_grazing','no_mobility','source_unsuitable','already_moved','no_suitable_neighbor','no_better_prey','no_capacity','insufficient_oxygen','eligible'])assert.match(sandbox.movementOpportunity(reason),/^\nMovement now:/);
assert.match(sandbox.producerFeedback({form:"Ribbon",support_mass:.01,frond_mass:.02,height_m:.1}),/Growth form: Ribbon/);
const tiny=sandbox.producerFeedback({support_mass:.0003455,frond_mass:.0001,height_m:.000382,maintenance_potential:.00004146});assert.match(tiny,/Support 0.000345 kg C\/m²/);assert.match(tiny,/Collecting height 0.000382 m/);assert.match(tiny,/upkeep 0.000041 kg/);assert.match(sandbox.producerFeedback({support_mass:1e-10,frond_mass:1e-10,height_m:1e-10}),/1.00e-10/);assert.match(sandbox.producerFeedback({support_mass:0,frond_mass:0,height_m:0}),/Support 0.000 kg C\/m²/);
sandbox.Module._stella_adjust_water=()=>0;let applied=[];sandbox.Module.ccall=(name,type,args,values)=>{if(name==='stella_adjust_water'){applied.push(values);return values[1]<0?-.03:.1;}return JSON.stringify({status:'origin',cell:12,tissues:[null,{support_mass:.01,frond_mass:.03,height_m:.04,available_light:.5}],cohorts:[{biomass:0},{lineage:9,biomass:.04}]});};el('refresh-life').onclick();assert.equal(el('fine-water').hidden,false);assert.match(el('life-cohorts').textContent,/Collecting tissue 0.030 kg C\/m² · Support 0.010/);el('water-minus').onclick();assert.equal(JSON.stringify(applied[0]),'[12,-0.1]');assert.match(el('water-feedback').textContent,/Removed 0.03 m/);el('water-plus').onclick();assert.match(el('water-feedback').textContent,/Added 0.10 m/);
sandbox.Module._stella_set_water_target=()=>0;let targets=[];sandbox.Module.ccall=(name,t,a,v)=>{if(name==='stella_set_water_target'){targets.push(v);return .3;}return JSON.stringify({status:'origin',cell:12,cohorts:[]});};el('refresh-life').onclick();assert.equal(el('target-water').hidden,false);el('water-shallow').onclick();assert.equal(JSON.stringify(targets[0]),'[12,0.5]');assert.match(el('water-feedback').textContent,/Set to 0.5 m. Added 0.30 m/);assert.match(el('water-feedback').textContent,/One-time external/);el('water-target').value='5';el('water-target-apply').onclick();assert.equal(JSON.stringify(targets[1]),'[12,5]');for(const invalid of ['', '-1', '5.1', 'NaN', 'Infinity']){el('water-target').value=invalid;el('water-target-apply').onclick();assert.match(el('water-feedback').textContent,/Enter a target/);}assert.equal(targets.length,2);sandbox.Module.ccall=(name)=>name==='stella_set_water_target'?NaN:JSON.stringify({status:'origin',cell:12,cohorts:[]});el('water-shallow').onclick();assert.match(el('water-feedback').textContent,/Patch changed/);
sandbox.Module.ccall=(name)=>name==='stella_adjust_water'?-.00038:JSON.stringify({status:'origin',cell:12,cohorts:[]});el('water-minus').onclick();assert.match(el('water-feedback').textContent,/Removed less than 0.01 m/);sandbox.Module.ccall=(name)=>name==='stella_adjust_water'?0:JSON.stringify({status:'origin',cell:12,cohorts:[]});el('water-minus').onclick();assert.match(el('water-feedback').textContent,/No water removed/);
sandbox.Module.ccall=(name)=>name==='stella_adjust_water'?NaN:JSON.stringify({status:'origin',cell:12,cohorts:[]});el('water-minus').onclick();assert.match(el('water-feedback').textContent,/Patch changed/);
sandbox.Module.ccall=()=>JSON.stringify({status:'sandbox'});el('refresh-life').onclick();assert.equal(el('fine-water').hidden,true);el('water-minus').onclick();assert.match(el('water-feedback').textContent,/Start an Origin/);
sandbox.Module.ccall=()=>'{bad';el('refresh-life').onclick();assert.match(el('life-summary').textContent,/Could not read/);
sandbox.Module.ccall=()=>JSON.stringify({status:'sandbox'});el('refresh-life').onclick();assert.match(el('life-summary').textContent,/Sandbox/);assert.equal(el('competition-panel').hidden,true);assert.equal(el('life-competition').textContent,'');el('close-life').onclick();
// Current-goal affordance follows living stage, including regression and fallback.
sandbox.Module._stella_goal_stage=()=>103;sandbox.refreshJourney();assert.equal(el('journey').textContent,'Next: producer diversity');
sandbox.Module._stella_goal_stage=()=>100;sandbox.refreshJourney();assert.equal(el('journey').textContent,'Next: seed simple life');
sandbox.Module._stella_goal_stage=()=>-1;sandbox.refreshJourney();assert.equal(el('journey').textContent,'Your next step');
el('journey').onclick();assert.equal(el('guide').hidden,false);
sandbox.Module._stella_make_pond=()=>0;let ponds=[];
sandbox.Module.ccall=(name,t,a,v)=>{if(name==='stella_make_pond'){ponds.push(v);return 7;}return JSON.stringify({status:'origin',cell:12,cohorts:[]});};
el('refresh-life').onclick();el('make-pond').onclick();assert.equal(JSON.stringify(ponds), '[[12]]');assert.match(el('water-feedback').textContent,/7 terrain patches, with 15 m water/);assert.match(el('water-feedback').textContent,/no automatic refill or new life/);
sandbox.Module.ccall=(name)=>name==='stella_make_pond'?-1:JSON.stringify({status:'origin',cell:12,cohorts:[]});el('make-pond').onclick();assert.match(el('water-feedback').textContent,/Patch changed/);
sandbox.Module.ccall=()=>JSON.stringify({status:'sandbox'});el('refresh-life').onclick();el('make-pond').onclick();assert.match(el('water-feedback').textContent,/Start an Origin/);
// Compact starter uses real snapshots and separate guarded actions.
sandbox.Module._stella_world_mode=()=>1;sandbox.Module._stella_seed_colony=()=>0;sandbox.Module._stella_make_nursery=()=>0;
let seedResult=1,starterCalls=[];
sandbox.Module.ccall=(name,t,a,v)=>{if(name==='stella_seed_colony'){starterCalls.push(v);return seedResult;}if(name==='stella_make_nursery')return 19;return JSON.stringify({status:'origin',cell:22,water_m:15,temperature_c:24,seed_reason:'eligible',cohorts:[]});};
sandbox.refreshStarter();assert.equal(el('origin-starter').hidden,false);assert.match(el('starter-summary').textContent,/22.*15.0 m water.*24°C/);
el('starter-basin').onclick();assert.match(el('starter-info').textContent,/19 patches, 5 m center, 15 m neighboring reservoir/);assert.equal(starterCalls.length,0,'Basin must not seed');
el('origin-starter').open=true;el('starter-seed').onclick();assert.equal(JSON.stringify(starterCalls),'[[22]]');assert.equal(el('origin-starter').open,true);assert.match(el('status').textContent,/Existing colony seeded/);assert.match(el('notice').textContent,/Existing colony seeded/);assert.equal(el('notice').hidden,false);
seedResult=0;el('starter-seed').onclick();assert.match(el('starter-info').textContent,/No colony added/);
seedResult=-1;el('starter-seed').onclick();assert.match(el('starter-info').textContent,/Patch changed/);
sandbox.Module.ccall=()=>JSON.stringify({status:'origin',cell:22,water_m:0,temperature_c:24,seed_reason:'too_dry'});sandbox.refreshStarter();assert.equal(el('starter-seed').disabled,true);assert.match(el('starter-summary').textContent,/Too dry/);
sandbox.Module._stella_world_mode=()=>0;sandbox.refreshStarter();assert.equal(el('origin-starter').hidden,true);assert.equal(el('starter-seed').disabled,true);el('starter-seed').onclick();assert.match(el('starter-info').textContent,/Choose an Origin/);
sandbox.Module._stella_world_mode=()=>1;sandbox.Module.ccall=()=>JSON.stringify({status:'origin',cell:22,water_m:null,temperature_c:24});sandbox.refreshStarter();assert.equal(el('starter-seed').disabled,true);
sandbox.Module._stella_god_target=()=>22;sandbox.Module._stella_god_action=()=>0;
let godCalls=[];sandbox.Module.ccall=(name,t,a,v)=>{if(name==='stella_god_target')return JSON.stringify({status:'ready',cell:22,water_m:3,temperature_c:25,eligibility:{wave:'none',lightning:'none',scorch:'origin'}});godCalls.push(v);return JSON.stringify({failure:'none',count:7,moved_mass:1,moved_depth_m:0.5,affected:[{temperature_k:40}],heat_joules:40000});};
el('god-toggle').onclick();assert.equal(el('god-sheet').open,true);assert.match(el('god-target').textContent,/22/);el('god-wave').onclick();assert.equal(JSON.stringify(godCalls),'[[0,22]]');assert.equal(el('god-sheet').open,false);assert.match(el('notice').textContent,/No water added/);
el('god-heat').onclick();assert.match(el('notice').textContent,/40.0°C/);
assert.equal(el('god-scorch').disabled,true);
sandbox.Module._stella_world_mode=()=>0;
sandbox.Module.ccall=(name,t,a,v)=>name==='stella_god_target'?JSON.stringify({status:'ready',cell:22,water_m:0,temperature_c:2,eligibility:{wave:'dry',lightning:'none',scorch:'none'}}):JSON.stringify({failure:'none',count:1,affected:[{temperature_k:40,cover_removed:0.15}],heat_joules:40000});
el('god-refresh').onclick();assert.equal(el('god-scorch').disabled,false);el('god-scorch').onclick();assert.match(el('notice').textContent,/15.0 percentage points/);assert.match(el('notice').textContent,/Not combustion/);
sandbox.Module.ccall=()=>JSON.stringify({failure:'wet',count:0});el('god-scorch').onclick();assert.match(el('god-result').textContent,/No cover or heat changed/);
sandbox.Module._stella_world_mode=()=>1;
sandbox.Module.ccall=()=>JSON.stringify({status:'ready',cell:22,water_m:3,temperature_c:25,eligibility:{wave:'none',lightning:'none',scorch:'origin'}});el('god-refresh').onclick();sandbox.Module.ccall=()=>JSON.stringify({failure:'dry',count:0});el('god-wave').onclick();assert.match(el('god-result').textContent,/No water here/);
sandbox.Module.ccall=()=>JSON.stringify({status:'no_world'});el('god-refresh').onclick();assert.equal(el('god-wave').disabled,true);el('god-wave').onclick();assert.match(el('god-result').textContent,/Select a planet/);
sandbox.Module._stella_watch_life=()=>1;el('starter-watch').onclick();assert.equal(el('origin-starter').open,false);assert.match(el('notice').textContent,/Pause or Play stays/);
// Actual observed biomass trend is shown, without labeling a cause or guaranteed growth.
let td=0,tm=.02;
sandbox.Module._stella_world_mode=()=>1;
sandbox.Module.ccall=(name)=>name==='stella_seed_colony'?1:JSON.stringify({status:'origin',cell:29,day:td,water_m:5,temperature_c:22,seed_reason:'eligible',cohorts:[{biomass:tm}]});
for(let i=0;i<=4;i++){td=i*.5;tm=.02-i*.001;sandbox.refreshStarter();}
assert.match(el('starter-summary').textContent,/Net biomass falling/);
el('refresh-life').onclick();assert.match(el('life-conditions').textContent,/does not prove a cause/);
el('starter-seed').onclick();assert.doesNotMatch(el('starter-summary').textContent,/Net biomass/);
for(let i=1;i<=4;i++){td=2+i*.5;tm=.016+i*.001;sandbox.refreshStarter();}
assert.match(el('starter-summary').textContent,/Net biomass rising/);
await el('load-world').onclick();sandbox.refreshStarter();assert.doesNotMatch(el('starter-summary').textContent,/Net biomass/);

// Explicit speed targets display measured progress separately; changing pace never resumes.
sandbox.Module._stella_speed_snapshot=()=>0;sandbox.Module._stella_set_speed=()=>0;
let speedState={requested:21600,achieved:18000,paused:true,step:1440,steps_last_frame:1},speedCalls=[],speedAccept=true;
sandbox.Module.ccall=(name,t,a,args)=>{if(name==='stella_speed_snapshot')return JSON.stringify(speedState);if(name==='stella_set_speed'){speedCalls.push(args);if(speedAccept)speedState.requested=args[0];return speedAccept?1:-1;}return '{}';};
el('more-toggle').onclick();el('speed-toggle').onclick();assert.equal(el('more-menu').open,false);assert.equal(el('speed-sheet').open,true);assert.match(el('speed-readout').textContent,/Paused/);assert.equal(el('speed-grow')['aria-pressed'],'true');
el('speed-fast').onclick();assert.equal(JSON.stringify(speedCalls),'[[86400]]');assert.equal(speedState.paused,true);assert.match(el('speed-result').textContent,/Still paused/);assert.equal(el('speed-fast')['aria-pressed'],'true');
speedState.paused=false;el('refresh-speed').onclick();assert.match(el('speed-readout').textContent,/Target: 24.0 hours\/sec.*Measured: 5.0 hours\/sec/);
speedAccept=false;el('speed-slow').onclick();assert.match(el('speed-result').textContent,/not changed/);assert.equal(speedState.requested,86400);
el('close-speed').onclick();assert.equal(el('speed-sheet').open,false);el('starter-speed').onclick();assert.equal(el('speed-sheet').open,true);
sandbox.Module.ccall=()=>'{bad';el('refresh-speed').onclick();assert.equal(el('speed-fast').disabled,true);const speedCallCount=speedCalls.length;el('speed-fast').onclick();assert.equal(speedCalls.length,speedCallCount);
sandbox.Module.started=false;el('starter-speed').onclick();assert.match(el('speed-readout').textContent,/Start or load/);el('close-speed').onclick();sandbox.Module.started=true;
const perf={enabled:true,cells:40962,frames:60,ticks:30,physics_frames:30,frame_avg_ms:33,frame_max_ms:80,frame_p95_ms:60,long_frames:5,physics_avg_ms:22,physics_max_ms:45,render_cpu_avg_ms:4,render_cpu_max_ms:8};
assert.match(sandbox.performanceText(perf),/40962|40,962/);assert.match(sandbox.performanceText(perf),/Render call/);
for(const d of [{}, {...perf,frame_avg_ms:NaN},{...perf,render_cpu_max_ms:-1},{...perf,frames:61},{...perf,enabled:false},{...perf,physics_frames:61}])assert.equal(sandbox.performanceText(d),null);
assert.match(sandbox.performanceText(perf),/Frame interval p95: 60.0 ms/);assert.match(sandbox.performanceText(perf),/intervals >50 ms: 5\/60/);
for(const d of [{...perf,frame_p95_ms:81},{...perf,long_frames:61},{...perf,long_frames:1.5},{...perf,frame_p95_ms:NaN}])assert.equal(sandbox.performanceText(d),null);
let perfEnabled=[];sandbox.Module._stella_performance_enable=n=>{perfEnabled.push(n);return 1};sandbox.Module._stella_performance_snapshot=()=>1;
el('speed-sheet').open=true;el('performance-details').open=true;sandbox.Module.ccall=()=>JSON.stringify(perf);el('performance-details').handlers.toggle();assert.equal(perfEnabled.at(-1),1);assert.match(el('performance-readout').textContent,/60 frames/);
sandbox.Module.ccall=()=>'{bad';sandbox.refreshPerformance();assert.match(el('performance-readout').textContent,/unavailable/);
delete sandbox.Module._stella_performance_snapshot;sandbox.refreshPerformance();assert.match(el('performance-readout').textContent,/unavailable/);
el('performance-details').open=false;el('performance-details').handlers.toggle();assert.equal(perfEnabled.at(-1),0);el('performance-details').open=true;el('speed-sheet').handlers.close();assert.equal(el('performance-details').open,false);
el('close-speed').onclick();assert.equal(perfEnabled.at(-1),0);assert.equal(el('performance-details').open,false);
// Repeated open starts at the heading and never leaves an old measurement running.
el('speed-sheet').scrollTop=999;el('performance-details').open=true;el('starter-speed').onclick();
assert.equal(el('speed-sheet').scrollTop,0);assert.equal(el('speed-sheet').open,true);assert.equal(el('performance-details').open,false);assert.equal(perfEnabled.at(-1),0);
el('starter-speed').onclick();assert.equal(el('speed-sheet').scrollTop,0);assert.equal(perfEnabled.at(-1),0);
// Native Escape dispatches the dialog close event; exercise that production handler.
el('performance-details').open=true;el('speed-sheet').close();el('speed-sheet').handlers.close();assert.equal(perfEnabled.at(-1),0);assert.equal(el('performance-details').open,false);
el('starter-speed').onclick();el('performance-details').open=true;sandbox.document.hidden=true;
for(const f of documentEvents.visibilitychange??[])f();assert.equal(perfEnabled.at(-1),0);assert.equal(el('performance-details').open,false);sandbox.document.hidden=false;
el('close-speed').onclick();
const captureData={...perf,world_serial:1,paused:false,menu_open:false,interrupted:false,game_time:100,requested:86400};
sandbox.Module._stella_performance_snapshot=()=>1;sandbox.Module._stella_performance_enable=n=>{perfEnabled.push(n);captureData.enabled=!!n;if(n)captureData.interrupted=false;return 1};sandbox.Module.ccall=()=>JSON.stringify(captureData);
el('starter-speed').onclick();el('measure-gameplay').onclick();assert.equal(el('speed-sheet').open,false);assert.equal(perfEnabled.at(-1),1);
// Queued close/toggle events from dismissing the panel must not kill gameplay capture.
el('speed-sheet').handlers.close();el('performance-details').handlers.toggle();assert.equal(perfEnabled.at(-1),1);
const tickCapture=intervalJobs.find(x=>x.ms===250).fn;for(fakeNow=250;fakeNow<10000;fakeNow+=250)tickCapture();fakeNow=10500;captureData.game_time=36100;tickCapture();assert.equal(perfEnabled.at(-1),0);assert.match(el('gameplay-measure-message').textContent,/sample ready/);assert.equal(el('speed-sheet').open,false);
el('starter-speed').onclick();assert.equal(el('gameplay-result').hidden,false);assert.match(el('gameplay-result-summary').textContent,/10.5 seconds/);assert.match(el('gameplay-result-summary').textContent,/not the whole-run average/);assert.match(el('gameplay-result-summary').textContent,/not live data/);
el('measure-gameplay').onclick();el('cancel-gameplay-measure').onclick();assert.equal(perfEnabled.at(-1),0);assert.match(el('gameplay-measure-message').textContent,/Previous sample kept/);
el('starter-speed').onclick();el('measure-gameplay').onclick();sandbox.document.hidden=true;for(const f of documentEvents.visibilitychange??[])f();assert.equal(perfEnabled.at(-1),0);sandbox.document.hidden=false;
el('starter-speed').onclick();el('measure-gameplay').onclick();el('more-toggle').onclick();assert.equal(perfEnabled.at(-1),0);assert.match(el('gameplay-measure-message').textContent,/menu opened/);el('more-menu').close();
captureData.paused=true;el('starter-speed').onclick();el('measure-gameplay').onclick();assert.match(el('gameplay-measure-message').textContent,/press Play/);captureData.paused=false;captureData.world_serial=2;el('starter-speed').onclick();assert.match(el('gameplay-result-summary').textContent,/previous world/);el('close-speed').onclick();
let fits=0;sandbox.Module._stella_fit_life=()=>{fits++;return 1};
el('more-toggle').onclick();el('fit-life').onclick();assert.equal(fits,1);assert.equal(el('more-menu').open,false);assert.match(el('notice').textContent,/Framed nearby connected life/);
sandbox.Module._stella_fit_life=()=>0;el('fit-life').onclick();assert.match(el('notice').textContent,/Pan toward a living patch/);
for(const [code,message] of [[-2,/Origin colonies only/],[-3,/canvas is too small/],[-4,/near the poles/],[-5,/could not be framed safely/],[-6,/too wide/]]){
 sandbox.Module._stella_fit_life=()=>code;el('fit-life').onclick();assert.match(el('notice').textContent,message);assert.doesNotMatch(el('notice').textContent,/Pan toward/);assert.equal(el('more-menu').open,false);
}
sandbox.Module._stella_fit_life=()=>-1;el('fit-life').onclick();assert.match(el('notice').textContent,/unavailable/);
sandbox.Module._stella_find_life=()=>1;el('more-toggle').onclick();el('find-life').onclick();assert.equal(el('more-menu').open,false);assert.match(el('notice').textContent,/Found existing life/);
sandbox.Module._stella_find_life=()=>0;el('find-life').onclick();assert.match(el('notice').textContent,/No visible-size/);
sandbox.Module._stella_find_life=()=>-2;el('find-life').onclick();assert.match(el('notice').textContent,/Origin colonies/);
sandbox.Module._stella_find_life=()=>-4;el('find-life').onclick();assert.match(el('notice').textContent,/view has not changed/);
delete sandbox.Module._stella_find_life;el('find-life').onclick();assert.match(el('notice').textContent,/Start or load/);
sandbox.Module.started=false;el('fit-life').onclick();assert.match(el('notice').textContent,/Start or load/);sandbox.Module.started=true;
delete sandbox.Module._stella_fit_life;el('fit-life').onclick();assert.match(el('notice').textContent,/Start or load/);
sandbox.Module.started=true;sandbox.Module._stella_life_snapshot=()=>1;
sandbox.Module.ccall=()=>JSON.stringify({status:'origin',cell:12,seed_reason:'too_cold',water_m:.1,temperature_c:0,cohorts:[],producer_habitat:{state:'frozen',compatible:0}});
el('life-toggle').onclick();assert.match(el('life-conditions').textContent,/photosynthesis is blocked/);el('close-life').onclick();
sandbox.Module.ccall=()=>JSON.stringify({status:'origin',cell:12,seed_reason:'too_dry',water_m:.1,temperature_c:20,cohorts:[],producer_habitat:{state:'thin_film',compatible:0}});
el('life-toggle').onclick();assert.match(el('life-conditions').textContent,/no current cohort/);el('close-life').onclick();
assert.match(sandbox.producerHabitatFeedback({state:'frozen'}),/blocked/);
assert.match(sandbox.producerHabitatFeedback({state:'thin_film',compatible:0}),/no current cohort/);
assert.match(sandbox.producerHabitatFeedback({state:'thin_film',compatible:2}),/not dryland/);
assert.match(sandbox.producerHabitatFeedback({state:'submergence_margin',supported_film_capable:0}),/not proof/);

assert.match(sandbox.livingTraitLabel({living_traits:{film_potential:true,film_compatible_now:false,habitat_factor:1}}),/potential/);
assert.match(sandbox.livingTraitLabel({living_traits:{film_potential:true,film_compatible_now:true,habitat_factor:.3}}),/compatible here/);
assert.match(sandbox.livingTraitLabel({living_traits:{film_potential:false,film_compatible_now:false,habitat_factor:0}}),/No supported/);
assert.match(sandbox.livingTraitLabel(null),/unavailable/);
for(let i=0;i<3;i++){
 sandbox.Module.ccall=()=>JSON.stringify({status:'origin',cell:12,cohorts:[{biomass:.02,lineage:9}],tissues:[{form:'cushion',living_traits:{film_potential:true,film_compatible_now:false,habitat_factor:1}}]});
 el('life-toggle').onclick();assert.equal(el('living-traits').hidden,false);assert.match(el('living-traits-copy').textContent,/cushion: Thin-film potential/);
 sandbox.Module.ccall=()=>JSON.stringify({status:'origin',cell:12,cohorts:[]});el('refresh-life').onclick();assert.equal(el('living-traits').hidden,true);assert.equal(el('living-traits-copy').textContent,'');el('close-life').onclick();
}
assert.match(sandbox.producerHabitatFeedback(null),/unavailable/);
// Eligibility snapshot prevents known-invalid clicks but never replaces server revalidation.
let blockedGodCalls=0;
sandbox.Module.ccall=(name)=>{if(name==='stella_god_target')return JSON.stringify({status:'ready',cell:22,water_m:0,temperature_c:227,eligibility:{wave:'dry',lightning:'invalid',scorch:'no_cover'}});blockedGodCalls++;return '{}';};
el('god-refresh').onclick();for(const id of ['god-wave','god-heat','god-scorch'])assert.equal(el(id).disabled,true);assert.match(el('god-availability').textContent,/Needs water/);assert.match(el('god-availability').textContent,/Needs vegetation/);el('god-wave').onclick();assert.equal(blockedGodCalls,0);
sandbox.Module.ccall=()=>JSON.stringify({status:'ready',cell:22,water_m:1,temperature_c:25});el('god-refresh').onclick();assert.equal(el('god-wave').disabled,true);assert.match(el('god-availability').textContent,/checks unavailable/);

// Real receipt fields required for separate Origin detritus action; missing readiness fails closed.
assert.equal(el('god-ignite').disabled,true);
const ignitionRecord={failure:'none',cell:22,burned_carbon_per_area:.02,burned_carbon_kg:200,oxygen_allocation_carbon_per_area:1,oxygen_consumed_kg:533.333,oxygen_ideal_kg:533.3333,oxygen_rounding_kg:-.0003,oxygen_rounding_budget_kg:.001,carbon_dioxide_added_kg:733.333,carbon_dioxide_ideal_kg:733.3333,carbon_dioxide_rounding_kg:-.0003,carbon_dioxide_rounding_budget_kg:.001,fuel_heat_joules:6000000000,stored_heat_joules:5999999999,thermal_rounding_joules:1,temperature_delta:1.5};
let ignitionCalls=[];sandbox.Module.ccall=(name,t,a,v)=>{if(name==='stella_god_target')return JSON.stringify({status:'ready',cell:22,water_m:0,temperature_c:25,eligibility:{wave:'dry',lightning:'none',scorch:'origin',ignition:'none'}});ignitionCalls.push(v);return JSON.stringify(ignitionRecord);};
el('god-refresh').onclick();assert.equal(el('god-ignite').disabled,false);assert.equal(el('god-scorch').disabled,true);el('god-ignite').onclick();assert.equal(JSON.stringify(ignitionCalls),'[[3,22]]');assert.equal(el('ignition-ledger').hidden,false);assert.match(el('ignition-summary').textContent,/not wildfire/);assert.match(el('ignition-summary').textContent,/numerical gas\/heat residuals/);assert.equal(el('ignition-receipt').textContent,JSON.stringify(ignitionRecord,null,2));
const preservedReceipt=el('ignition-receipt').textContent;el('god-refresh').onclick();assert.equal(el('ignition-receipt').textContent,preservedReceipt);
sandbox.Module.ccall=()=>JSON.stringify({failure:'wet',cell:22});el('god-ignite').onclick();assert.match(el('god-result').textContent,/completely dry/);assert.equal(el('ignition-receipt').textContent,preservedReceipt);
sandbox.Module.ccall=()=>JSON.stringify({failure:'stale',cell:23});el('god-ignite').onclick();assert.match(el('god-result').textContent,/Selection changed/);
sandbox.Module.ccall=()=>JSON.stringify({failure:'none',cell:22,burned_carbon_kg:1});el('god-ignite').onclick();assert.match(el('god-result').textContent,/Inspect the patch before trying again/);assert.equal(el('ignition-receipt').textContent,preservedReceipt);
for(const reason of ['wet','no_fuel','no_oxygen','heat_limit','precision','mode','invalid']){sandbox.Module.ccall=()=>JSON.stringify({status:'ready',cell:22,water_m:0,temperature_c:25,eligibility:{wave:'dry',lightning:'none',scorch:'origin',ignition:reason}});el('god-refresh').onclick();assert.equal(el('god-ignite').disabled,true);}
sandbox.confirm=()=>true;await sandbox.storageAction('load');assert.equal(el('ignition-ledger').hidden,true);assert.equal(el('ignition-receipt').textContent,'');
// Discovery yields bounded requests, never calls a god action, and dismissal cancels queued navigation.
const fuelFrames=[];sandbox.requestAnimationFrame=fn=>fuelFrames.push(fn);let fuelCalls=[];let fuelResults=[2,3];sandbox.Module._stella_find_detritus=restart=>{fuelCalls.push(restart);return restart===2?-4:fuelResults.shift();};
sandbox.Module.ccall=name=>JSON.stringify({status:'ready',cell:23,water_m:2,temperature_c:25,eligibility:{wave:'none',lightning:'none',scorch:'origin',ignition:'wet'}});
el('find-detritus').onclick();assert.equal(el('cancel-detritus').hidden,false);assert.match(el('god-result').textContent,/small batches/);assert.equal(JSON.stringify(fuelCalls),'[2,1]');fuelFrames.shift()();assert.equal(JSON.stringify(fuelCalls),'[2,1,0]');assert.match(el('notice').textContent,/wet dead carbon/);assert.match(el('notice').textContent,/Nothing was drained or ignited/);assert.equal(el('cancel-detritus').hidden,true);
fuelCalls=[];fuelResults=[2,1];el('find-detritus').onclick();el('close-god').onclick();const callsAtCancel=fuelCalls.length;fuelFrames.shift()();assert.equal(fuelCalls.length,callsAtCancel);assert.equal(el('cancel-detritus').hidden,true);assert.match(el('god-result').textContent,/Search cancelled/);el('god-toggle').onclick();assert.match(el('god-result').textContent,/Search cancelled/);assert.doesNotMatch(el('god-result').textContent,/Searching/);
fuelResults=[0];el('find-detritus').onclick();assert.match(el('god-result').textContent,/in this scan/);
fuelResults=[-2];el('find-detritus').onclick();assert.match(el('god-result').textContent,/Origin worlds/);
// Recorded feeding uses actual living history, not capability, and cancels pending navigation.
let feedingCalls=[];let feedingResults=[2,1];sandbox.Module._stella_find_feeding=x=>{feedingCalls.push(x);return x===2?-4:feedingResults.shift();};
sandbox.Module.ccall=()=>JSON.stringify({status:'origin',cell:3421,day:30,cohorts:[{biomass:.01,feeding:.08,lifetime_grazed:.00794,lineage:38,optimum:300,efficiency:1}]});
el('find-feeding').onclick();assert.match(el('feeding-result').textContent,/small batches/);fuelFrames.shift()();assert.match(el('notice').textContent,/Colony ID #38/);assert.match(el('notice').textContent,/Past feeding, not eating now/);assert.equal(JSON.stringify(feedingCalls),'[2,1,0]');
feedingResults=[2,1];el('find-feeding').onclick();el('close-life').onclick();const beforeCancel=feedingCalls.length;fuelFrames.shift()();assert.equal(feedingCalls.length,beforeCancel);assert.match(el('feeding-result').textContent,/cancelled/);
feedingResults=[0];el('find-feeding').onclick();assert.match(el('feeding-result').textContent,/Capability alone does not count/);
feedingResults=[1];sandbox.Module.ccall=()=>JSON.stringify({status:'origin',cohorts:[{biomass:0,feeding:.1,lifetime_grazed:.2}]});el('find-feeding').onclick();assert.match(el('feeding-result').textContent,/changed before inspection/);
feedingResults=[2,1];el('find-feeding').onclick();await sandbox.storageAction('load');const afterLoadCancel=feedingCalls.length;fuelFrames.shift()();assert.equal(feedingCalls.length,afterLoadCancel);assert.match(el('feeding-result').textContent,/cancelled/);
feedingResults=[1];sandbox.Module.ccall=()=>JSON.stringify({status:'origin',cohorts:[{biomass:.01,feeding:.1,lifetime_grazed:1e-12,lineage:17,optimum:300,efficiency:1}]});el('find-feeding').onclick();assert.match(el('notice').textContent,/1.00e-12/);assert.doesNotMatch(el('notice').textContent,/intake 0.000000/);
console.log('PASS: production shell ID wiring, More/Close/Help flows, save and cancelled/confirmed load');})().catch(e=>{console.error(e);process.exit(1)});
