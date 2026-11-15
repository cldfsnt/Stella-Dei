(function(root){'use strict';
function describe(d){
 if(!d||d.status!=='ready'||!['origin','sandbox'].includes(d.mode))throw Error('Unavailable census');
 const number=v=>{if(!Number.isFinite(v)||v<0)throw Error('Invalid count');return v;};
 const count=v=>{if(!Number.isSafeInteger(number(v)))throw Error('Invalid count');return String(v);};
 let lines=[];
 if(d.mode==='origin'){
  if(!Array.isArray(d.forms)||d.forms.length>6)throw Error('Invalid forms');
  lines.push('Worldwide: '+count(d.colonies)+' living colonies sampled. Top forms by summed biomass density (not species):');
  const forms=d.forms.filter(f=>number(f.biomass_sum)>0).slice(0,3);
  lines.push(...forms.map(f=>{if(!/^[a-z -]{1,40}$/i.test(f.form))throw Error('Invalid form');return f.form+': '+count(f.colony_count)+' colonies · '+number(f.biomass_sum).toPrecision(3)+' summed kg C/m²';}));
  if(!forms.length)lines.push('No living forms found in this sample.');
 }else lines.push('Worldwide: '+count(d.rabbits)+' rabbits · '+count(d.vegetated_patches)+' patches with plants · '+number(d.cover_sum).toFixed(2)+' summed patch cover (not trees).');
 const start=number(d.census_start_time),end=number(d.census_end_time);if(end<start)throw Error('Invalid time');
 lines.push('Sampled day '+(start/86400).toFixed(2)+'–'+(end/86400).toFixed(2)+'. Running worlds can change during the scan.');
 if(d.recent){const r=d.recent;const seconds=number(r.observed_seconds);lines.push((r.saturated?'At least ':'')+count(r.counts.births)+' births · '+count(r.counts.deaths)+(d.mode==='origin'?' colony deaths over ':' rabbit deaths over ')+(seconds/3600).toFixed(1)+' observed simulation hours.');lines.push(d.mode==='origin'?'Paid colony births and physiology deaths only; excludes seeding, moves and god-tool losses.':'Rabbit births and deaths only; not plant births or losses.');lines.push('Up to 24 simulation hours, grouped in hourly buckets; session only, reset on load.');}
 else lines.push('Recent events unavailable until simulation is observed; not zero.');
 return lines.join('\n');
}
function create(h){let epoch=0;return {cancel(){epoch++;},start(){const mine=++epoch;let first=true,world=null;function step(){if(mine!==epoch||!h.available())return;try{const d=h.read(first?1:0);first=false;if(world===null)world=d.world;else if(d.world!==world)throw Error('World changed');if(d.status==='pending'){h.show('Sampling living community…');h.schedule(step);return;}h.show(describe(d));}catch{h.show('Community sample unavailable or changed. Refresh to try again.');}}step();}};}
const api={describe,create};if(typeof module==='object'&&module.exports)module.exports=api;else root.WorldEcology=api;
})(typeof globalThis!=='undefined'?globalThis:this);
