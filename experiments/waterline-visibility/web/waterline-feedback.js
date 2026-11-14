(function(root){'use strict';
function describe(data){
 const s=data&&data.waterline;if(!s)return {kind:'unknown',label:'Waterline evidence unavailable',help:'Refresh to inspect the current patch.',evidence:''};
 const kinds={dry:['Dry patch','No photosynthesis here. Add water or return life to a suitable wet habitat.'],exposed_film:['Exposed water film','Below 20 cm: this version blocks photosynthesis, even with living support. Arrivals here are not proof of shore adaptation.'],wet_edge:['Wet edge','20 cm–1 m of water. Watch real descendants while keeping the habitat suitable.'],aquatic:['Aquatic habitat','These are aquatic microbial forms, not terrestrial plants.'],deep:['Deep water','Beyond 50 m: this version blocks microbial photosynthesis.'],unknown:['Unknown habitat','No adaptation claim can be made from this snapshot.']};
 const item=kinds[s.zone]||kinds.unknown;
 const n=v=>Number.isSafeInteger(v)&&v>=0?v:0;
 return {kind:s.growth_environment_ok?'suitable':'limited',label:item[0]+(s.growth_environment_ok?' · growth conditions possible':' · growth blocked'),help:item[1]+(!s.growth_environment_ok&&['wet_edge','aquatic'].includes(s.zone)?' Temperature is outside the supported range.':''),evidence:n(s.living_descendants)+' living descendants · '+n(s.supported_descendants)+' with actual support tissue. '+n(s.observed_paid_arrivals_still_present)+' recent paid arrivals still here. Arrival records are session-only and bounded; zero does not mean no past arrivals. Generation alone does not prove reproduction in this patch.'};
}
root.StellaWaterlineFeedback={describe};if(typeof module==='object'&&module.exports)module.exports={describe};
})(typeof globalThis!=='undefined'?globalThis:this);
