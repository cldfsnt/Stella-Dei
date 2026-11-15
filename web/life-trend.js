/* Observed net biomass change, not a fabricated production or survival rate. */
(function(root,factory){if(typeof module==='object'&&module.exports)module.exports=factory();else root.StellaLifeTrend=factory();})(typeof globalThis!=='undefined'?globalThis:this,function(){
 'use strict';
 function create(){
  const cells=new Map();let latestDay=-Infinity;
  function reset(){cells.clear();latestDay=-Infinity;}
  function forget(cell){cells.delete(cell);}
  function sample(d){
   if(!d||d.status!=='origin'||!Number.isSafeInteger(d.cell)||d.cell<0||!Number.isFinite(d.day)||d.day<0||!Array.isArray(d.cohorts))return null;
   let mass=0;for(const c of d.cohorts){if(!c||!Number.isFinite(c.biomass)||c.biomass<0)return null;mass+=c.biomass;}if(!Number.isFinite(mass))return null;
   if(d.day<latestDay)reset();latestDay=d.day;
   let history=cells.get(d.cell)||[];cells.delete(d.cell);cells.set(d.cell,history);
   while(cells.size>32)cells.delete(cells.keys().next().value);
   if(!history.length||d.day>history[history.length-1].day)history.push({day:d.day,mass});
   else history[history.length-1]={day:d.day,mass};
   while(history.length>1&&history[1].day<=d.day-2)history.shift();
   // A long gap is not a continuously observed trend. Restart instead.
   if(history.length>1&&d.day-history[history.length-2].day>2){history.splice(0,history.length-1);return null;}
   const first=history[0],days=d.day-first.day;if(days<2||first.mass<=0)return null;
   const delta=mass-first.mass,pct=delta/first.mass*100;
   const direction=mass===0?'lost':Math.abs(delta)<0.0001||Math.abs(pct)<5?'steady':delta>0?'rising':'falling';
   return {direction,days,percent:pct,from:first.mass,to:mass,label:direction==='lost'?'No living biomass observed here':direction==='steady'?'Net biomass steady':'Net biomass '+direction};
  }
  return {sample,reset,forget};
 }
 return {create};
});
