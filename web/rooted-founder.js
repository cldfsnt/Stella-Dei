(function(root){'use strict';
const u32=x=>Number.isInteger(x)&&x>=0&&x<=4294967295;
const positive=x=>typeof x==='number'&&Number.isFinite(x)&&x>0;
const nonnegative=x=>typeof x==='number'&&Number.isFinite(x)&&x>=0;
const id=x=>typeof x==='string'&&/^[1-9][0-9]{0,19}$/.test(x)&&BigInt(x)<=18446744073709551615n;
function current(s){return s&&s.status==='wetlands'&&s.enabled===true&&s.physiology_law===3&&u32(s.world_serial)&&u32(s.cell);}
function receipt(r,s,status,token){return r&&r.status===status&&r.world_serial===s.world_serial&&r.cell===s.cell&&u32(r.token)&&r.token>0&&(token===undefined||r.token===token)&&id(r.founder_id)&&positive(r.carbon_kg_m2)&&positive(r.nitrogen_kg_m2)&&positive(r.carbon_source_kg)&&nonnegative(r.carbon_rounding_kg)&&positive(r.support_kg_c_m2)&&r.support_kg_c_m2<=r.carbon_kg_m2&&Math.fround(r.support_kg_c_m2)===Math.fround(Math.fround(r.carbon_kg_m2)*.25)&&positive(r.root_kg_c_m2)&&r.root_kg_c_m2<=r.support_kg_c_m2&&Math.fround(r.root_kg_c_m2)===Math.fround(Math.fround(r.support_kg_c_m2)*.5)&&r.root_fraction===.5&&r.organization===.25&&nonnegative(r.soil_kg_m2)&&r.soil_kg_m2<=1&&nonnegative(r.depth_m)&&r.depth_m<=50;}
const reasons={disabled:'Requires the current Wetlands world.',invalid:'Patch data unavailable.',stale:'World, selection or resources changed. Request a fresh preview.',busy:'Finish Advance or close native Details first.',too_cold:'Patch is too cold.',too_hot:'Patch is too hot.',too_deep:'Water is too deep.',no_soil:'This shallow patch has no soil water. Planting does not supply water.',no_space:'No free colony slot or biomass capacity.',no_nutrients:'Not enough mineral nutrients.',no_carbon:'Not enough atmospheric carbon.',unrepresentable:'The resource payment cannot be represented safely.'};
const num=x=>x.toPrecision(4);
function payment(r){return num(r.carbon_kg_m2)+' kg C/m² living tissue, including '+num(r.support_kg_c_m2)+' support and '+num(r.root_kg_c_m2)+' roots; '+num(r.nitrogen_kg_m2)+' kg N/m² mineral debit. Atmospheric C debit: '+num(r.carbon_source_kg)+' kg (rounding excess ≤ '+num(r.carbon_rounding_kg)+' kg).';}
function create(h){let busy=false;
 return {plant(){if(busy)return;busy=true;h.busy(true);let token=0;
 try{
  if(!h.available()){h.report('Finish saving, loading or advancing first. Nothing planted.');return;}
  const s=h.snapshot();if(!current(s)){h.report('Select a patch in the current Wetlands world. Nothing planted.');return;}
  const p=h.preview(s.world_serial,s.cell);if(p&&u32(p.token))token=p.token;
  if(!receipt(p,s,'eligible')){h.report((reasons[p&&p.status]||'Could not verify the preview.')+' Nothing planted.');return;}
  if(!h.confirm('Plant one rooted founder here?\nChosen genetics: 50% root allocation, 25% organization. Support is part of paid tissue, not extra carbon.\n'+payment(p)+'\nCurrent soil: '+num(p.soil_kg_m2)+' kg water/m²; standing depth: '+num(p.depth_m)+' m. No water or soil is supplied. These chosen founder traits are not evolved adaptation or a survival guarantee. The colony may decline or die.')){h.report('Cancelled. Nothing planted.');return;}
  const now=h.snapshot();if(!h.available()||!current(now)||now.world_serial!==s.world_serial||now.cell!==s.cell){h.report('World, selection or operation changed. Nothing planted.');return;}
  const r=h.apply(s.world_serial,s.cell,token);
  if(!receipt(r,s,'planted',token)){h.report(r&&reasons[r.status]?(reasons[r.status]+' Nothing planted.'):'Planting outcome could not be verified. Inspect before trying again.');return;}
  const confirmed=['founder_id','carbon_kg_m2','nitrogen_kg_m2','carbon_source_kg','carbon_rounding_kg','support_kg_c_m2','root_kg_c_m2','root_fraction','organization','soil_kg_m2','depth_m'];
  if(!confirmed.every(k=>r[k]===p[k])){h.report('Planting returned a different receipt from the confirmed preview. Outcome unknown; inspect before trying again.');return;}
  const after=h.snapshot();const found=current(after)&&after.world_serial===s.world_serial&&after.cell===s.cell&&Array.isArray(after.root_allocations)&&after.root_allocations.some(c=>c.id===r.founder_id&&c.living===true&&c.fraction===.5);
  if(!found){h.report('Planting returned a receipt, but the new colony could not be verified. Inspect before trying again.');return;}
  h.report('Planted colony #'+r.founder_id+'. '+payment(r)+' No water supplied. Chosen genetics, not proof of uptake or survival.');h.inspect(r.founder_id);
 }catch{h.report('Outcome unavailable. Inspect the patch before trying again.');}
 finally{if(token)try{h.cancel(token);}catch{}busy=false;h.busy(false);}
 }};
}
const api={create,current,receipt,payment};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.StellaRootedFounder=api;
})(typeof window==='undefined'?globalThis:window);
