(function(root){'use strict';
function aerial(cohort,life,world){
 if(!life||life.status!=='origin'||!Number.isInteger(life.world_serial)||!world||world.status!=='combined'||world.enabled!==true||!((world.writer_version===13&&(world.ground_thermal_law===undefined||world.ground_thermal_law===0))||(world.writer_version===14&&world.ground_thermal_law===1)||(world.writer_version===15&&world.ground_thermal_law===1&&world.protective_law===1))||world.root_physiology!==3||world.wind_law!==1||world.world_serial!==life.world_serial)return '';
 if(!cohort||!Number.isFinite(cohort.biomass)||cohort.biomass<=0)return '';
 const a=cohort.aerial_allocation;
 if(typeof a!=='number'||!Number.isFinite(a)||a<0||a>1)return '\nAerial route allocation unavailable.';
 return '\nAerial route allocation '+(a*100).toFixed(1)+'% · heritable share of existing dispersal opportunities, not extra births. Birth route not recorded.';
}
const api={aerial};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.StellaCombinedTraits=api;
})(typeof globalThis==='undefined'?this:globalThis);
