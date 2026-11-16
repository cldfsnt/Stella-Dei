/* Loaded after the existing controller wiring, never used by native standalone. */
(function(){
'use strict';
const $=id=>document.getElementById(id),dialogs=[...document.querySelectorAll('dialog')];
let lastDock='world';
function cancelSheet(d){
 touchControls.reset();
 if(d.id==='more-menu'){worldLibrary.cancel();clearWorldEcology();}
 if(d.id==='auto-seed-sheet')autoSeed.cancel();
 if(d.id==='habitat-sheet'){if(habitatController)habitatController.cancel();habitatChoice=null;}
 if(d.id==='god-sheet'){cancelDetritusSearch();if(transportController)transportController.cancel();}
 if(d.id==='life-sheet'){cancelFeedingSearch();cancelOffspringSearch();clearWaterWatch();}
}
const closeSheets=StellaMobileNavigation.installSheets({dialogs,busy:()=>storage.state().busy,advance:()=>advanceDay.isLocked(),cancel:cancelSheet,feedback,reset:()=>{$('guide').hidden=true;touchControls.reset();}});
for(const d of dialogs)d.addEventListener('close',()=>{if(!dialogs.some(x=>x.open))$('dock-'+lastDock).focus();});
const move=(id,parent)=>{const e=$(id);if(e)parent.appendChild(e);};
const details=(label,parent)=>{const d=document.createElement('details'),s=document.createElement('summary');s.textContent=label;d.appendChild(s);parent.appendChild(d);return d;};
// Secondary view controls do not compete with the primary dock.
const view=details('View & visibility',$('group-observe'));const viewButtons=document.createElement('div');viewButtons.id='mobile-view';view.appendChild(viewButtons);
for(const e of document.querySelectorAll('#controls [data-zoom]'))viewButtons.appendChild(e);
for(const id of ['globe','fit-life','seed-targets-toggle','arrival-effects-toggle'])move(id,viewButtons);
// Keep the actual paid actions prominent, descriptions available rather than repeated.
$('starter-seed').textContent='Seed here';$('auto-seed-open').textContent='Seed all…';$('starter-find').textContent='Find habitat';
const totals=document.createElement('p');totals.id='mobile-community-total';totals.setAttribute('role','status');$('world-ecology-panel').insertBefore(totals,$('world-form-actions'));
const statsDetails=details('Sample details',$('world-ecology-panel'));move('world-ecology-readout',statsDetails);
const sandboxTools=document.createElement('div');sandboxTools.className='mobile-tool-grid';sandboxTools.id='mobile-sandbox-tools';sandboxTools.hidden=true;$('group-plant').insertBefore(sandboxTools,$('group-plant').firstChild);for(const [tool,label] of [[3,'Plants'],[4,'Rabbits']]){const b=document.createElement('button');b.textContent=label;b.dataset.mobileTool=tool;b.dataset.mode='0';sandboxTools.appendChild(b);}
const seedBrush=document.createElement('button');seedBrush.textContent='Choose seed patch';seedBrush.dataset.mobileTool='3';seedBrush.dataset.mode='1';seedBrush.hidden=true;$('starter-actions').appendChild(seedBrush);
const seedHelp=details('Habitat care & assistance',$('group-plant'));move('starter-basin',seedHelp);move('starter-info',seedHelp);move('help-toggle',seedHelp);
const world=$('group-world');world.insertBefore($('load-world'),world.firstChild);world.insertBefore($('save-world'),world.firstChild);
$('load-world').textContent='Load saved planet…';$('combined-new').textContent='Save + new planet…';
const worldHelp=details('Help & advanced',world);for(const id of ['fullscreen','land','combined-disclosure','combined-refresh','combined-status'])move(id,worldHelp);
for(const p of [...world.querySelectorAll(':scope > p')]){if(p.textContent.startsWith('New living planets'))worldHelp.appendChild(p);else if(p.textContent.startsWith('Save stays'))p.textContent='Saved on this device, in this browser. No cloud backup; download a copy for safekeeping.';}
world.insertBefore($('combined-new'),$('world-library'));
$('welcome-tip').hidden=true;
const settings=document.createElement('button');settings.textContent='Advanced world settings…';settings.id='mobile-settings';worldHelp.appendChild(settings);const warning=document.createElement('p');warning.textContent='Save first. Leaving the planet can discard unsaved progress. Advanced worlds includes Sandbox.';worldHelp.appendChild(warning);
const guide=document.createElement('button');guide.textContent='How to play';guide.onclick=openGuide;worldHelp.appendChild(guide);
// Preserve actual target/receipt element identities while reducing first-view prose.
const god=$('god-sheet');$('god-title').textContent='God tools';
const intro=god.querySelector(':scope > p');if(intro)intro.textContent='Deliberate assistance. Tools can harm existing life.';
const brushes=document.createElement('div');brushes.className='mobile-tool-grid';brushes.id='mobile-brushes';god.insertBefore(brushes,$('assisted-founders'));
for(const [tool,label] of [[1,'Water +'],[2,'Water −'],[5,'Raise land'],[6,'Lower land']]){const b=document.createElement('button');b.textContent=label;b.dataset.mobileTool=tool;brushes.appendChild(b);}
const nutrients=document.createElement('button');nutrients.textContent='Nutrients +';nutrients.dataset.mobileTool='4';nutrients.dataset.mode='1';nutrients.hidden=true;brushes.appendChild(nutrients);
const target=document.createElement('button');target.textContent='Set water depth…';brushes.appendChild(target);target.onclick=()=>{refreshLife();$('advanced-water').open=true;$('life-sheet').showModal();$('water-target').focus();};
const climate=document.createElement('button');climate.textContent='Climate…';climate.id='mobile-climate';brushes.appendChild(climate);
const founderHelp=details('Chosen traits & habitat care',$('assisted-founders'));for(const id of ['rooted-founder-choice','rooted-founder-help'])move(id,founderHelp);
const pioneers=details('Pioneer assistance',$('assisted-founders'));move('combined-pioneer',pioneers);move('combined-pioneer-batch',pioneers);
god.insertBefore($('god-actions'),$('assisted-founders'));
const fire=details('Target checks & tool details',god);for(const id of ['god-availability','find-detritus','cancel-detritus','god-refresh','ignition-ledger','god-help'])move(id,fire);
const speed=$('speed-sheet'),advanced=details('Display & diagnostics',speed);
for(const node of [...speed.children])if(node!==advanced&&(node.matches('section[aria-label="3D scene resolution"]')||['measure-gameplay','gameplay-result','refresh-speed','performance-details'].includes(node.id)))advanced.appendChild(node);
// Menu actions remain separate from world replacement, save, load and import.
const nav=StellaMobileNavigation.create({
 available:()=>!storage.state().busy&&!advanceDay.isLocked()&&!document.hidden,
 read:()=>{if(!Module.started||Module.failed||typeof Module._stella_mobile_snapshot!=='function')return null;const s=JSON.parse(Module.ccall('stella_mobile_snapshot','string',[],[]));s.mode=typeof Module._stella_world_mode==='function'?Module._stella_world_mode():null;return s;},
 action:(kind,world,value)=>Module.ccall(kind==='pause'?'stella_mobile_pause':'stella_mobile_tool','number',['number','number'],[world,value]),
 open:name=>{if(name==='speed')openSpeed();else if(name==='god')$('god-toggle').click();else openToolGroup({seed:'plant',stats:'observe',world:'world'}[name]);},
 close:closeSheets,setGesture:paint=>{dragMode=paint?'paint':'navigate';touchControls.setMode(dragMode);},
 show:({section,state})=>{for(const n of ['speed','seed','god','stats','world'])$('dock-'+n).setAttribute('aria-expanded',String(section===n));const b=$('dock-pause');b.disabled=!state;b.querySelector('.dock-label').textContent=state?(state.paused?'Play':'Pause'):'Play';b.querySelector('.dock-icon').textContent=state&&!state.paused?'Ⅱ':'▶';b.setAttribute('aria-label',state&&!state.paused?'Pause simulation':'Play simulation');$('mobile-status').textContent=state?('Day '+Number(state.day||0).toFixed(1)+' · '+(state.paused?'Paused':Number(state.speed||0)/3600+' h/s')):'';for(const name of ['speed','seed','god','stats','world'])$('dock-'+name).disabled=!!(state&&state.blocked);b.disabled=!state||state.blocked===true;sandboxTools.hidden=!state||state.mode!==0;nutrients.hidden=!state||state.mode!==1;seedBrush.hidden=!state||state.mode!==1;const tool=state&&state.tool||0;$('mobile-brush').hidden=tool===0;$('mobile-brush-label').textContent=({1:'Water +',2:'Water −',3:state&&state.mode===0?'Plants':'Seed',4:state&&state.mode===0?'Rabbits':state&&state.mode===1?'Nutrients +':'Tool',5:'Raise land',6:'Lower land'})[tool]||'Selected tool';}
});
for(const name of ['speed','seed','god','stats','world'])$('dock-'+name).onclick=()=>{lastDock=name;nav.choose(name);};
$('dock-pause').onclick=()=>{if(!nav.pause())feedback('Pause control unavailable. Finish the current action or close its panel.');};$('mobile-brush-cancel').onclick=()=>{if(!nav.brush(0))feedback('Could not leave the tool yet. Finish the current action.');};
for(const b of document.querySelectorAll('[data-mobile-tool]'))b.onclick=()=>{if(!nav.brush(Number(b.dataset.mobileTool),b.dataset.mode===undefined?undefined:Number(b.dataset.mode)))feedback('Tool unavailable or world changed. Check the current planet and choose again.');};
climate.onclick=()=>{const s=nav.refresh();if(!s||storage.state().busy||advanceDay.isLocked())return;closeSheets();const result=Module.ccall('stella_mobile_climate','number',['number'],[s.world_serial]);if(result!==1)feedback('Climate controls unavailable. Finish the current action or close its panel.');};
settings.onclick=()=>{const s=nav.refresh();if(!s||storage.state().busy||advanceDay.isLocked())return;closeSheets();const result=Module.ccall('stella_mobile_menu','number',['number'],[s.world_serial]);if(result!==1)feedback('World settings unavailable. Finish the current action or close its panel.');};
for(const d of dialogs)d.addEventListener('close',()=>{if(!dialogs.some(x=>x.open))nav.dismissed();});
let owned=false,lastTool=null,lastFeedback='';
function layout(){const h=$('mobile-dock').getBoundingClientRect().height;document.documentElement.style.setProperty('--dock',h+'px');}
window.addEventListener('resize',layout);layout();
function tick(){layout();if(Module.started&&!Module.failed&&typeof Module._stella_web_shell_set==='function'&&!owned){owned=Module.ccall('stella_web_shell_set','number',['number','number','number'],[1,28,0])===1;}const state=nav.refresh();if(state&&typeof state.feedback==='string'&&state.feedback&&state.feedback!==lastFeedback){lastFeedback=state.feedback;feedback(state.feedback);}if(state&&state.tool!==lastTool){lastTool=state.tool;dragMode=lastTool===0?'navigate':'paint';touchControls.setMode(dragMode);}if(owned){const top=$('mobile-brush').hidden?28:Math.ceil($('mobile-brush').getBoundingClientRect().bottom);Module.ccall('stella_web_shell_set','number',['number','number','number'],[1,top,0]);}}
setInterval(tick,500);tick();
window.StellaMobileUX={nav,closeSheets};
})();
