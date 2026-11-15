/* Observed net biomass change, not a fabricated production or survival rate. */
(function(root,factory){if(typeof module==='object'&&module.exports)module.exports=factory();else root.StellaLifeTrend=factory();})(typeof globalThis!=='undefined'?globalThis:this,function(){
 'use strict';
 // Fixed storage: at most 32 patches × 64 actual observations.
 const maxSamples=64;
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
   // Check the last actual observation BEFORE thinning. Retained samples may
   // be farther apart after decimation; that is not a real observation gap.
   if(history.length&&d.day-history[history.length-1].day>2)history.length=0;
   if(!history.length||d.day>history[history.length-1].day)history.push({day:d.day,mass});
   else history[history.length-1]={day:d.day,mass};
   while(history.length>1&&history[1].day<=d.day-2)history.shift();
   // Thin only interior observations, preserving actual first/latest endpoints.
   // No interpolation or clock rounding. The reported days remain the exact
   // observed interval, which can exceed two days after thinning.
   if(history.length>maxSamples){
    let write=1;const last=history.length-1;
    for(let read=2;read<last;read+=2)history[write++]=history[read];
    history[write++]=history[last];history.length=write;
   }
   const first=history[0],days=d.day-first.day;if(days<2||first.mass<=0)return null;
   const delta=mass-first.mass,pct=delta/first.mass*100;
   const direction=mass===0?'lost':Math.abs(delta)<0.0001||Math.abs(pct)<5?'steady':delta>0?'rising':'falling';
   return {direction,days,percent:pct,from:first.mass,to:mass,label:direction==='lost'?'No living biomass observed here':direction==='steady'?'Net biomass steady':'Net biomass '+direction};
  }
  return {sample,reset,forget};
 }
 return {create};
});
