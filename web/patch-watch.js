/* Bounded local observation controller. Never starts or speeds simulation. */
(function(root){
 function create(h){
  let active=false,token=0,timer=null,deadline=null,startMs=0;
  function clear(){if(timer!==null)h.clearInterval(timer);if(deadline!==null)h.clearTimeout(deadline);timer=deadline=null;}
  function valid(s){return s&&Number.isInteger(s.cell)&&Number.isFinite(s.elapsed)&&s.elapsed>=0&&Number.isFinite(s.consumed)&&s.consumed>=0&&Number.isInteger(s.ticks)&&s.ticks>=0&&['fixed','recycled','start_biomass','end_biomass'].every(k=>Number.isFinite(s[k])&&s[k]>=0)&&['start_colonies','end_colonies'].every(k=>Number.isInteger(s[k])&&s[k]>=0&&s[k]<=4);}
  function show(s){if(!valid(s)){h.render('Observation unavailable.',false,null);return;}
   const time=(s.elapsed/3600).toFixed(2)+' simulated hours';
   const status=s.active?'Watching':s.status==='complete'?'Observation complete':'Stopped: '+s.status;
   const unit=' kg C/m²';
   h.render(status+' · Patch '+s.cell+' · '+time+(s.ticks===0?' · No simulation steps observed':'')+'\nLiving '+s.start_biomass.toPrecision(3)+' → '+s.end_biomass.toPrecision(3)+unit+' (net); colonies '+s.start_colonies+' → '+s.end_colonies+'\nFixed '+s.fixed.toPrecision(3)+' · Bio-return '+s.recycled.toPrecision(3)+' · Grazed '+s.consumed.toPrecision(3)+unit+'\nNet is not growth; bio-return excludes movement/god tools.'+(s.consumed===0?' No grazing intake recorded.':''),!!s.active,s);
  }
  function stop(complete=false){if(!active)return;active=false;++token;clear();try{h.stop(complete);show(h.read());}catch{h.render('Observation stopped; result unavailable.',false);}}
  function tick(){if(!active)return;try{if(h.blocked()){stop();return;}const s=h.read();if(!valid(s)){stop();return;}show(s);if(!s.active){active=false;++token;clear();}else if(h.now()-startMs>=10000)stop(true);}catch{stop();}}
  return {start(cell){stop();if(h.blocked())return false;try{if(h.start(cell)!==1)return false;active=true;startMs=h.now();const t=++token;timer=h.setInterval(()=>{if(token===t)tick();},200);deadline=h.setTimeout(()=>{if(token===t)stop(true);},10000);tick();return active;}catch{stop();return false;}},cancel:()=>stop(),tick,isActive:()=>active};
 }
 if(typeof module==='object'&&module.exports)module.exports={create};else root.StellaPatchWatch={create};
})(typeof globalThis!=='undefined'?globalThis:this);
