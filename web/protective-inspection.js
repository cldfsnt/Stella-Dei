(function(root){'use strict';
const u32=x=>Number.isInteger(x)&&x>=0&&x<=4294967295;
function describe(cohort,life,world,s){
 if(!world||world.writer_version!==15||world.status!=='combined'||world.enabled!==true||world.protective_law!==1||world.ground_thermal_law!==1||world.root_physiology!==3||world.wind_law!==1)return '';
 const unavailable='\nProtective investment/state unavailable.';
 if(!life||!u32(life.world_serial)||!u32(life.cell)||life.world_serial!==world.world_serial||!s||s.status!=='protective'||s.law!==1||s.world_serial!==life.world_serial||s.cell!==life.cell||!Array.isArray(s.cohorts)||s.cohorts.length>4)return unavailable;
 const id=cohort&&cohort.lineage;if(typeof id!=='string'||!/^\d+$/.test(id))return unavailable;
 const matches=s.cohorts.filter(c=>c&&c.id===id);if(matches.length!==1)return unavailable;const c=matches[0];
 if(!Number.isFinite(c.investment)||c.investment<0||c.investment>1)return unavailable;
 const clock=c.recovery_seconds;if(c.status==='active'){if(clock!==null)return unavailable;}else if(c.status==='protecting'){if(clock!==0||c.investment===0)return unavailable;}else if(c.status==='recovering'){if(!Number.isFinite(clock)||clock<=0||c.investment===0)return unavailable;}else return unavailable;
 const state=c.status==='active'?'Active':c.status==='protecting'?'Protecting':'Recovering · '+(clock/60).toFixed(1)+' minutes of favorable recovery elapsed (not a countdown)';
 return '\nCold/heat protection investment '+(c.investment*100).toFixed(1)+'% · '+state+'. Protection costs favorable growth; partial investment retains partial activity. Not drought immunity or a survival guarantee.';
}
const api={describe};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.StellaProtective=api;
})(typeof globalThis==='undefined'?this:globalThis);
