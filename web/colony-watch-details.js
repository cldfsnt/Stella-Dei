/* Endpoint comparison only. No species grouping, cause inference, timers or I/O. */
(function(root){
 const max='18446744073709551615';
 function members(list){
  if(!Array.isArray(list)||list.length>4)return null;
  const found=new Map();
  for(const c of list){
   if(!c||typeof c.id!=='string'||! /^[1-9][0-9]{0,19}$/.test(c.id)||c.id.length===20&&c.id>max||!Number.isFinite(c.biomass)||c.biomass<=0||found.has(c.id))return null;
   found.set(c.id,c.biomass);
  }
  return found;
 }
 function describe(snapshot){
  const before=members(snapshot&&snapshot.start_members),after=members(snapshot&&snapshot.end_members);
  if(!before||!after)return 'Colony-level detail unavailable for this observation.';
  const ids=[...before.keys(),...after.keys()].filter((id,i,a)=>a.indexOf(id)===i);
  if(!ids.length)return 'No living colonies at either observed endpoint. This does not rule out activity between endpoints.';
  return ids.map(id=>{
   const start=before.get(id),end=after.get(id),label='Colony ID #'+id+': ';
   if(start===undefined)return label+'present only at end · '+end.toPrecision(3)+' kg C/m²';
   if(end===undefined)return label+'no longer present at end · started with '+start.toPrecision(3)+' kg C/m²';
   const delta=end-start;return label+start.toPrecision(3)+' → '+end.toPrecision(3)+' kg C/m² · '+(delta===0?'unchanged':(delta>0?'net gain +':'net loss ')+delta.toPrecision(3));
  }).join('\n')+'\nEndpoint changes include growth, feeding, movement and offspring. They do not establish a cause or prove death; colonies appearing and disappearing between endpoints are not tracked.';
 }
 const api={describe};if(typeof module==='object'&&module.exports)module.exports=api;else root.StellaColonyWatchDetails=api;
})(typeof globalThis==='undefined'?this:globalThis);
