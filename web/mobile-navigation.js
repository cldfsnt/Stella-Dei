/* Navigation only. Engine state and existing transactional controllers remain authoritative. */
(function(root){
'use strict';
function create({read,action,available,open,close,show,setGesture}){
 let section=null;
 function refresh(){let s=null;try{s=read();}catch{}const valid=s&&s.available===true&&typeof s.paused==='boolean'&&Number.isInteger(s.world_serial)&&Number.isInteger(s.tool);show({section,state:valid?s:null});return valid?s:null;}
 function choose(name){if(!['speed','seed','god','stats','world'].includes(name))return false;if(!available())return false;const s=refresh();if(s&&s.blocked)return false;close();section=name;open(name);refresh();return true;}
 function pause(){if(!available())return false;const s=refresh();if(!s||s.blocked)return false;close();const ok=action('pause',s.world_serial,s.paused?0:1)===1;refresh();return ok;}
 function brush(tool,expectedMode){if(!available()||!Number.isInteger(tool))return false;const s=refresh();if(!s||s.blocked)return false;if(expectedMode!==undefined&&s.mode!==expectedMode)return false;const ok=action('tool',s.world_serial,tool)===1;if(ok){close();section=null;setGesture(tool!==0);}refresh();return ok;}
 function dismissed(){section=null;refresh();}
 return {choose,pause,brush,refresh,dismissed};
}
function installSheets({dialogs,busy,advance,cancel,feedback,reset}){
 const closeAll=()=>{if(advance()||busy())return false;for(const d of dialogs)if(d.open&&d.id!=='advance-day-overlay')d.close();reset();return true;};
 for(const d of dialogs){
  d.addEventListener('close',e=>{if(d.open)e.stopImmediatePropagation();},true);
  const show=d.showModal.bind(d),close=d.close.bind(d);
  d.close=function(){if(!d.open)return;cancel(d);if(busy()){feedback('Finish saving or loading before closing this panel.');return;}close();};
  d.showModal=function(){if(d.open)return;if(d.id!=='advance-day-overlay'&&advance())return;if(!closeAll()&&d.id!=='advance-day-overlay')return;show();};
  d.addEventListener('cancel',e=>{cancel(d);if(busy()){e.preventDefault();feedback('Finish saving or loading before closing this panel.');}});
 }
 return closeAll;
}
if(typeof module!=='undefined'&&module.exports)module.exports={create,installSheets};else root.StellaMobileNavigation={create,installSheets};
})(typeof window==='undefined'?globalThis:window);
