(function(root){
'use strict';
const finite=x=>typeof x==='number'&&Number.isFinite(x);
function summary(data){
 const w=data&&data.wetlands;
 if(w&&w.enabled===false&&w.world_serial===data.world_serial)return 'Loaded saved world. Its original rules are unchanged; soil/root mechanics require a new living planet.';
 if(!w||w.enabled!==true||w.status!=='wetlands'||!Number.isSafeInteger(w.world_serial)||w.world_serial!==data.world_serial||!Number.isSafeInteger(w.cell)||w.cell!==data.cell)return 'Wetlands conditions unavailable. No root uptake is inferred.';
 const lines=[];
 if(finite(w.soil_kg_m2)&&w.soil_kg_m2>=0&&w.soil_kg_m2<=1)lines.push('Soil water: '+w.soil_kg_m2.toPrecision(4)+' kg/m² (finite shared supply).');
 else lines.push('Soil water unavailable.');
 const ids=Array.isArray(data.identities)?data.identities:[];
 if(Array.isArray(w.root_allocations)&&w.root_allocations.length<=4){
  for(const r of w.root_allocations){
   if(!r||typeof r.id!=='string'||!/^\d+$/.test(r.id)||!ids.some(i=>i.id===r.id&&i.living===true)||!finite(r.fraction)||r.fraction<0||r.fraction>1||!finite(r.root_tissue_kg_c_m2)||r.root_tissue_kg_c_m2<0)continue;
   lines.push('Colony #'+r.id+': root allocation '+(r.fraction*100).toPrecision(3)+'%; paid root tissue '+r.root_tissue_kg_c_m2.toPrecision(4)+' kg C/m².');
  }
 }
 lines.push('Allocation is not evidence of current uptake. Actual root-water receipt is not available in this view.');
 return lines.join('\n');
}
function graphicsFailure(reason){return /WindowCreationFailed/.test(String(reason))?'Graphics could not start: this browser could not create the graphics context required by the WebGL2 game. Detailed error below.':null;}
function activeLaw(s){
 if(s&&s.status==='wetlands'&&s.enabled===true&&s.physiology_law===3)return 'Active: Wetlands experimental law 3. Finite soil and inherited roots; no land-establishment guarantee.';
 if(s&&s.status==='historical_beta')return 'Active: historical experimental law '+String(s.physiology_law)+'. Not converted to Wetlands law 3. Start a fresh Wetlands world to use the current preview.';
 if(s&&s.status==='legacy')return 'Active: classic world. Experimental Wetlands physics are NOT active. Start a fresh Wetlands world explicitly; imports are not automatically converted.';
 return 'No verified Wetlands world active. Use Play, then Start a fresh Wetlands world.';
}
function mount(doc,h){
 const button=doc.getElementById('wetlands-new'),out=doc.getElementById('wetlands-new-status');let busy=false;
 button.onclick=()=>{
  if(busy)return;busy=true;button.disabled=true;
  try{
   if(!h.available()){out.textContent='Start the game first and finish any save or Advance operation. No world changed.';return;}
   const before=h.snapshot();
   if(!before||!Number.isSafeInteger(before.world_serial)||before.world_serial<0||before.world_serial>4294967295){out.textContent='World identity unavailable. No world changed.';return;}
   if(!h.confirm('Create a fresh experimental Wetlands world? Unsaved progress in the current preview world will be discarded. Existing browser save is not overwritten. Main-game saves are separate.')){out.textContent='Cancelled. Current world unchanged.';return;}
   if(!h.available()){out.textContent='Game became busy. No world change requested.';return;}
   const code=h.create(before.world_serial);
   if(code!==1){out.textContent=code===-2?'World changed while confirming. Refresh and try again.':code===-3?'Game is busy with Advance or graphics work. Try again when it finishes.':code===-1?'Game is not ready. Start it first.':'Creation outcome unknown. Inspect the current world before retrying.';return;}
   const after=h.snapshot();
   if(!after||after.status!=='wetlands'||after.enabled!==true||after.physiology_law!==3||!Number.isSafeInteger(after.world_serial)||after.world_serial===before.world_serial){out.textContent='Creation returned success but the experimental world could not be verified. Do not retry automatically.';return;}
   out.textContent='Fresh Wetlands world created. Soil starts empty and ordinary seeded founders have no assigned roots. No demo was loaded. Save explicitly to retain this world.';h.created();
  }catch{out.textContent='Could not verify the operation. Inspect the current world before retrying.';}
  finally{busy=false;button.disabled=false;}
 };
}
const api={summary,graphicsFailure,mount,activeLaw};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.StellaWetlands=api;
})(typeof window==='undefined'?globalThis:window);
