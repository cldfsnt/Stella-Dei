/* Bounded local observation controller. Never starts or speeds simulation. */
(function(root){
 function create(h){
  let active=false,token=0,timer=null,deadline=null,startMs=0;
  function clear(){if(timer!==null)h.clearInterval(timer);if(deadline!==null)h.clearTimeout(deadline);timer=deadline=null;}
  function valid(s){return s&&Number.isInteger(s.cell)&&Number.isFinite(s.elapsed)&&s.elapsed>=0&&Number.isFinite(s.consumed)&&s.consumed>=0&&Number.isInteger(s.ticks)&&s.ticks>=0;}
  function show(s){if(!valid(s)){h.render('Observation unavailable.',false);return;}
   const time=(s.elapsed/3600).toFixed(2)+' simulated hours';
   const intake=s.consumed>0?s.consumed.toPrecision(3)+' kg C/m² consumed':'No grazing intake recorded';
   h.render((s.active?'Watching':s.status==='complete'?'Observation complete':'Stopped: '+s.status)+'. Patch '+s.cell+' · '+time+' · '+intake+'.'+(s.ticks===0?' No simulation steps observed.':'')+' This patch only, during this observation.',!!s.active);
  }
  function stop(complete=false){if(!active)return;active=false;++token;clear();try{h.stop(complete);show(h.read());}catch{h.render('Observation stopped; result unavailable.',false);}}
  function tick(){if(!active)return;try{if(h.blocked()){stop();return;}const s=h.read();if(!valid(s)){stop();return;}show(s);if(!s.active){active=false;++token;clear();}else if(h.now()-startMs>=10000)stop(true);}catch{stop();}}
  return {start(cell){stop();if(h.blocked())return false;try{if(h.start(cell)!==1)return false;active=true;startMs=h.now();const t=++token;timer=h.setInterval(()=>{if(token===t)tick();},200);deadline=h.setTimeout(()=>{if(token===t)stop(true);},10000);tick();return active;}catch{stop();return false;}},cancel:()=>stop(),tick,isActive:()=>active};
 }
 if(typeof module==='object'&&module.exports)module.exports={create};else root.StellaPatchWatch={create};
})(typeof globalThis!=='undefined'?globalThis:this);
