(function(root){'use strict';
function describe(d){
 if(!d||d.status!=='ready'||!['origin','sandbox'].includes(d.mode))throw Error('Unavailable census');
 const number=v=>{if(!Number.isFinite(v)||v<0)throw Error('Invalid count');return v;};
 const count=v=>{if(!Number.isSafeInteger(number(v)))throw Error('Invalid count');return String(v);};
 let lines=[];
 if(d.mode==='origin'){
  if(!Array.isArray(d.forms)||d.forms.length>6)throw Error('Invalid forms');
  lines.push('Worldwide: '+count(d.colonies)+' living colonies sampled. Living growth forms by summed biomass density (not species):');
  const forms=d.forms.filter(f=>number(f.biomass_sum)>0);
  lines.push(...forms.map(f=>{if(!/^[a-z -]{1,40}$/i.test(f.form))throw Error('Invalid form');return f.form+': '+count(f.colony_count)+' colonies · '+number(f.biomass_sum).toPrecision(3)+' summed kg C/m²';}));
  if(!forms.length)lines.push('No living forms found in this sample.');
 }else lines.push('Worldwide: '+count(d.rabbits)+' rabbits · '+count(d.vegetated_patches)+' patches with plants · '+number(d.cover_sum).toFixed(2)+' summed patch cover (not trees).');
 if(d.mode==='sandbox'&&d.plant_defenses){
  const p=d.plant_defenses;if(typeof p.enabled!=='boolean')throw Error('Invalid defense state');
  if(p.tender_patches+p.defended_patches!==d.vegetated_patches)throw Error('Invalid plant partition');
  const tender=count(p.tender_patches),defended=count(p.defended_patches);
  if(!p.enabled){if(p.defended_patches!==0)throw Error('Invalid classic traits');lines.push('Classic plants: inherited defenses are off.');}
  else {
   lines.push('Plant traits, not species: Tender (0): '+tender+' patches · '+number(p.tender_cover).toFixed(2)+' full-patch equivalents; defended (>0): '+defended+' patches · '+number(p.defended_cover).toFixed(2)+' full-patch equivalents.');
   if(d.vegetated_patches>0){const lo=number(p.minimum),hi=number(p.maximum);if(lo>hi||hi>1)throw Error('Invalid toughness range');lines.push('Living plant toughness range: '+(lo===0?'0':lo.toPrecision(3))+'–'+(hi===0?'0':hi.toPrecision(3))+'. Defended includes inherited variants, not only manually planted Tough.');}
   else {if(p.minimum!==null||p.maximum!==null)throw Error('Invalid empty range');lines.push('No living plant traits in this sample.');}
  }
 }
 const start=number(d.census_start_time),end=number(d.census_end_time);if(end<start)throw Error('Invalid time');
 lines.push('Sampled day '+(start/86400).toFixed(2)+'–'+(end/86400).toFixed(2)+'. Running worlds can change during the scan.');
 if(d.recent){const r=d.recent;const seconds=number(r.observed_seconds);lines.push((r.saturated?'At least ':'')+count(r.counts.births)+' births · '+count(r.counts.deaths)+(d.mode==='origin'?' colony deaths over ':' rabbit deaths over ')+(seconds/3600).toFixed(1)+' observed simulation hours.');lines.push(d.mode==='origin'?'Paid colony births and physiology deaths only; excludes seeding, moves and god-tool losses.':'Rabbit births and deaths only; not plant births or losses.');lines.push('Up to 24 simulation hours, grouped in hourly buckets; session only, reset on load.');}
 else lines.push('Recent events unavailable until simulation is observed; not zero.');
 return lines.join('\n');
}
const names=['Microbial mat','Cushion','Rosette','Ribbon','Branching','Canopy'];
function formRows(d){
 if(!d||d.status!=='ready'||d.mode!=='origin'||!Number.isInteger(d.world)||d.world<0||d.world>4294967295)return [];
 if(!Array.isArray(d.forms)||d.forms.length!==6)return [];
 const seen=new Set();let total=0;
 const rows=d.forms.map(f=>{const id=f.form_id;if(!Number.isInteger(id)||id<0||id>5||seen.has(id)||f.form!==names[id]||!Number.isSafeInteger(f.colony_count)||f.colony_count<0||!Number.isFinite(f.biomass_sum)||f.biomass_sum<0)throw Error('Invalid forms');seen.add(id);total+=f.colony_count;return {id,name:names[id],count:f.colony_count,world:d.world};});
 if(total!==d.colonies)throw Error('Invalid form total');return rows;
}
function create(h){let epoch=0,rows=[];
 const publish=r=>{rows=r;if(h.forms)h.forms(r);};
 function cancel(){epoch++;publish([]);}
 return {cancel,start(){const mine=++epoch;publish([]);let first=true,world=null;function step(){if(mine!==epoch)return;if(!h.available()){publish([]);return;}try{const d=h.read(first?1:0);first=false;if(world===null)world=d.world;else if(d.world!==world)throw Error('World changed');if(d.status==='pending'){h.show('Sampling living community…');h.schedule(step);return;}const text=describe(d),next=formRows(d);h.show(text);publish(next);}catch{publish([]);h.show('Community sample unavailable or changed. Refresh to try again.');}}step();},visit(id){const row=rows.find(r=>r.id===id);if(!row||row.count===0||!h.available()||!h.visit)return false;cancel();let result;try{result=h.visit(row.world,id);}catch{result=null;}
 const message=result===1?'Visiting an existing '+row.name+' colony. Growth form, not species; no life changed.':result===0?'No living '+row.name+' remains. Refresh the community sample.':result===-2?'World changed or an action is busy. Refresh before visiting.':result===-4?'A matching colony could not be framed safely. No life changed.':'Visit unavailable. Refresh the community sample; no life changed.';
 h.show(message);if(h.result)h.result(result,message);return result===1;
 }};
}
const api={describe,create,formRows};if(typeof module==='object'&&module.exports)module.exports=api;else root.WorldEcology=api;
})(typeof globalThis!=='undefined'?globalThis:this);
