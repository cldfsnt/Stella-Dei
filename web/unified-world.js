(function(root){'use strict';
const uint=x=>Number.isInteger(x)&&x>=0&&x<=4294967295;
function valid(s){if(!s||!uint(s.world_serial)||typeof s.enabled!=='boolean')return false;
if(s.status==='combined')return s.enabled&&((s.writer_version===13&&(s.ground_thermal_law===undefined||s.ground_thermal_law===0))||(s.writer_version===14&&s.ground_thermal_law===1)||(s.writer_version===15&&s.ground_thermal_law===1&&s.protective_law===1))&&(s.writer_version===15||s.protective_law===undefined||s.protective_law===0)&&s.root_physiology===3&&s.wind_law===1;
if(s.status==='wind')return s.writer_version===11&&!s.enabled&&s.wind_law===1&&s.root_physiology===1&&s.ground_thermal_law===0&&s.protective_law===0;
if(s.status==='unavailable')return !s.enabled&&s.writer_version===0;
if(s.enabled||s.wind_law!==0)return false;
if(s.status==='wetlands')return s.writer_version===10&&(s.writer_version===15||s.protective_law===undefined||s.protective_law===0)&&s.root_physiology===3;
if(s.status==='historical_beta')return (s.writer_version===8&&s.root_physiology===1)||(s.writer_version===9&&s.root_physiology===2);
return s.status==='legacy'&&s.writer_version===7;
}
function describe(s){if(!valid(s)||s.writer_version===0)return 'No verified active world. Start Play first.';if(s.status==='wind')return 'Loaded saved world: inherited wind dispersal. Soil roots and cold/heat protection are not enabled; its original rules are unchanged.';return s.status==='combined'?('Living world: finite soil/roots + wind dispersal. '+(s.writer_version===15?'Calmer ground-temperature response. Evolving cold/heat protection enabled; founders start with no investment.':s.writer_version===14?'Calmer ground-temperature response.':'Historical ground-temperature response.')):'Existing world retained with its original rules. Newer mechanics start on a new living planet.';}
function create(h){let busy=false;function read(){try{const s=h.read();return valid(s)?s:null;}catch{return null;}}
 function refresh(){const s=read();h.render(s,describe(s),busy);return s;}
 async function fresh(){if(busy||!h.available())return false;const before=read();if(!before||before.writer_version===0){h.message('Start Play first. No world replaced.');return false;}
  const choice=h.choice?h.choice():'historical';if(!['historical','calmer','protective'].includes(choice)){h.message('Choose a valid new-world climate response. Nothing replaced.');return false;}
  if(h.canCreate&&!h.canCreate(choice)){h.message('This new-world setting is unavailable in the current runtime. Nothing replaced.');return false;}
  if(!h.confirm((choice==='protective'?'New living planet: finite soil, wind dispersal and evolving cold/heat protection. Founders start with zero investment; paid offspring may inherit changes. Protection costs favorable growth, is not drought immunity and does not guarantee survival.\n':choice==='calmer'?'Chosen new-world setting: calmer ground-temperature response. This does not add rain or soil water, and does not guarantee survival.\n':'Chosen new-world setting: historical ground-temperature response.\n')+'Save the current world to this game browser slot, then replace the active world with a new living planet? This replaces the existing game browser save slot with the current world. Eligible older-format saved bytes are backed up before a newer-format write; this is not a backup of every prior save. This saves your current world, not the new one. Older saved worlds are not converted. Cancel keeps the current world unchanged.'))return false;
  busy=true;refresh();try{
   let now=read();if(!h.available()||!now||now.world_serial!==before.world_serial||now.writer_version!==before.writer_version||(h.choice&&h.choice()!==choice)){h.message('World or action changed. Nothing replaced.');return false;}
   if(!await h.save()){h.message('Save or backup failed. Current world was NOT replaced.');return false;}
   now=read();if(!h.available()||!now||now.world_serial!==before.world_serial||now.writer_version!==before.writer_version||(h.choice&&h.choice()!==choice)){h.message('World changed while saving. Nothing replaced.');return false;}
   const code=h.fresh(before.world_serial,choice);const after=read();
   if(code===1&&after&&after.status==='combined'&&after.writer_version===(choice==='protective'?15:choice==='calmer'?14:13)&&after.world_serial!==before.world_serial){h.message('New living planet created. Prior world saved; save again explicitly to retain this new world. No organisms planted.');h.changed();return true;}
   h.message(code===-2?'World changed; no replacement requested again.':code===-3?'Game is busy; nothing replaced.':code===-1?'Creation unavailable; nothing replaced.':'Creation outcome unknown. Inspect before trying again.');return false;
  }catch{h.message('Operation outcome unknown. Inspect the current world before retrying.');return false;}finally{busy=false;refresh();}
 }
 function pioneer(){if(busy||!h.available())return false;const s=read();let life;try{life=h.life();}catch{}
  if(!s||s.status!=='combined'||!life||life.status!=='origin'||life.world_serial!==s.world_serial||!uint(life.cell)){h.message('Select a patch in the combined world first.');return false;}
  const code=h.pioneer(s.world_serial,life.cell);const after=read();if(code===1&&after&&after.status==='combined'&&after.world_serial===s.world_serial){h.message('Paid Pioneer planted: chosen 50% aerial allocation, roots0. No successful flight or establishment is implied.');h.changed();return true;}h.message(code===0?'Pioneer refused: habitat, resources or space unavailable.':code===-2?'World or selected patch changed.':code===-3?'Game is busy.':'Pioneer outcome unavailable; inspect before retrying.');return false;
 }
 return {fresh,pioneer,refresh};
}
function mount(doc,h){const ui=create({...h,choice:()=>'protective',render:(s,text,busy)=>{doc.getElementById('combined-status').textContent=text;doc.getElementById('combined-new').disabled=busy||!h.available()||!s||s.writer_version===0;for(const id of ['combined-pioneer','combined-pioneer-batch'])doc.getElementById(id).disabled=busy||!h.available()||!s||s.status!=='combined';}});doc.getElementById('combined-new').onclick=ui.fresh;doc.getElementById('combined-pioneer').onclick=ui.pioneer;doc.getElementById('combined-refresh').onclick=ui.refresh;return ui;}
const api={valid,describe,create,mount};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.StellaCombined=api;
})(typeof globalThis==='undefined'?this:globalThis);
