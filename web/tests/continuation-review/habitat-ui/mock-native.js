
(()=>{let paused=true,world=3,cell=10,token=0,pending=null,unknown=false,moves=0;
Module.started=true;Module.failed=false;Module._stella_world_mode=()=>1;Module._stella_selected_point=()=>cell;Module._stella_adjust_water=()=>0;
for(const k of ['prepare','execute','status','cancel'])Module['_stella_habitat_'+k]=()=>0;
Module._stella_habitat_cancel=()=>{pending=null;};
Module.ccall=(name,type,args,v=[])=>{
 if(name==='stella_life_snapshot')return JSON.stringify({status:'origin',world_serial:world,cell,paused,cohorts:[],water_m:1,temperature_c:25});
 if(name==='stella_habitat_prepare'){if(!paused)return JSON.stringify({ok:false,reason:'pause required'});pending={ok:true,token:++token,world,cell,kind:v[2]?'nursery':'pond',floor_ids:[10,11,12,13,14,15,16],rim_ids:Array.from({length:12},(_,i)=>20+i),floor_count:7,rim_count:12,living_floor_patches:2,living_rim_patches:3,water_added_depth_sum_m:100.25,water_removed_depth_sum_m:17.75,water_added_kg:1.234e12,water_removed_kg:2.345e11,center_depth_m:v[2]?5:15,other_floor_depth_m:15,rim_depth_m:0};return JSON.stringify(pending);}
 if(name==='stella_habitat_status')return JSON.stringify({available:true,paused,pending:!!pending,token:pending?.token||0,world,cell});
 if(name==='stella_habitat_execute'){const p=pending;pending=null;if(!p||!paused)return JSON.stringify({ok:false,reason:'stale'});moves++;document.getElementById('fixture-count').textContent='Mock applications: '+moves;if(unknown)return '{}';return JSON.stringify({...p,manual:true});}
 return '{}';
};
const controls=document.getElementById('fixture-controls');for(const [label,fn] of [['Preview nursery',()=>startHabitatPlan(cell,true)],['Preview pond',()=>startHabitatPlan(cell,false)],['Mock paused',()=>paused=true],['Mock running',()=>paused=false]]){const b=document.createElement('button');b.textContent=label;b.onclick=fn;controls.append(b);}
const panel=document.createElement('div');panel.innerHTML='<p><b>MOCK responses only</b></p><span id="fixture-count">Mock applications: 0</span>';document.getElementById('habitat-sheet').append(panel);
for(const [label,fn] of [['Invalidate selection',()=>{cell++;habitatController.check();}],['Mock unpause',()=>{paused=false;habitatController.check();}],['Unknown execute result',()=>unknown=true],['Reset mock',()=>{paused=true;cell=10;unknown=false;pending=null;habitatController.cancel();}]]){const b=document.createElement('button');b.textContent=label;b.onclick=fn;panel.append(b);}
document.getElementById('cover').hidden=true;document.getElementById('status').textContent='MOCK habitat preview UI only. No game or persistent save.';
})();
