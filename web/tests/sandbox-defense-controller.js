(function(root,factory){if(typeof module==='object'&&module.exports)module.exports=factory();else root.SandboxDefense=factory();})(typeof globalThis!=='undefined'?globalThis:this,function(){
'use strict';
function valid(v){return !!v&&Number.isInteger(v.world)&&v.world>=0&&Number.isInteger(v.cell)&&v.cell>=0&&['sandbox','origin'].includes(v.mode)&&typeof v.enabled==='boolean'&&[-1,0,1].includes(v.kind)&&typeof v.status==='string';}
function create(io){let current=null,message='';
 function refresh(){try{const v=io.read();if(!valid(v)){current=null;io.render(null,'World unavailable');return null;}if(current&&(current.world!==v.world||current.mode!==v.mode))message='';current=v;io.render(v,message);return v;}catch{current=null;io.render(null,'World unavailable');return null;}}
 function action(action){const before=current;let v;try{v=io.read();}catch{}if(!before||!valid(v)||v.world!==before.world||v.cell!==before.cell||v.mode!=='sandbox'){message='World or selection changed. Review before trying again.';refresh();return false;}
  let r;try{r=io.act(v.world,v.cell,action);}catch{message='Result unknown. Inspect or refresh before retrying.';io.render(current,message);return false;}
  const expected=action===0?['enabled','already_enabled']:action===3?['cancelled']:['selected'];
  if(!valid(r)||r.world!==v.world||r.cell!==v.cell||r.mode!=='sandbox'||(expected.includes(r.status)&&((action===0&&!r.enabled)||(action===1&&(!r.enabled||r.kind!==0))||(action===2&&(!r.enabled||r.kind!==1))))){message='Result unknown. Inspect or refresh before retrying.';io.render(current,message);return false;}
  current=r;if(!expected.includes(r.status)){message='Action refused: '+r.status+'. Nothing further was requested.';io.render(r,message);return false;}
  message=action===0?'Enabled for future offspring worldwide. Existing plants unchanged.':action===3?'Planting cancelled. No plant added.':action===1?'Seed choice: Tender.':'Seed choice: Tough.';io.render(r,message);if(action===1||action===2||action===3)io.focus();return true;
 }
 return {refresh,action};
}
return {create,valid};
});
