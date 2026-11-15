(function(root){'use strict';
 const id=x=>typeof x==='string'&&/^[1-9][0-9]{0,19}$/.test(x)&&BigInt(x)<=18446744073709551615n;
 const uint=x=>Number.isInteger(x)&&x>=0&&x<=4294967295;
 function parents(s){return s&&s.status==='origin'&&uint(s.world_serial)&&uint(s.cell)&&Array.isArray(s.identities)?s.identities.slice(0,4).filter(c=>c&&c.living===true&&id(c.id)&&Number.isInteger(c.generation)&&c.generation>=0):[];}
 function create(h){let source=null,busy=false,epoch=0,message='';const emit=()=>h.render({source,busy,message,parents:parents(source)});
  function cancel(){const was=busy;epoch++;busy=false;if(was)message='Search cancelled. No life changed.';try{h.cancel();}catch{}emit();}
  function setSource(s){cancel();source=parents(s).length?s:null;message='';emit();}
  function start(parent){cancel();if(!source||!parents(source).some(c=>c.id===parent)||!h.available())return false;const expected={world:source.world_serial,cell:source.cell,parent},ticket=epoch;busy=true;message='Searching the whole world in small batches…';emit();
   function next(restart){if(ticket!==epoch||!busy)return;if(!h.available()){cancel();return;}let result;try{result=h.step(restart?1:0,expected);}catch{busy=false;message='Search unavailable. No life changed.';emit();return;}
    if(result===2){h.schedule(()=>next(false));return;}busy=false;
    if(result===1){try{const s=h.snapshot();if(!s||s.world_serial!==expected.world)throw Error('World changed');const c=parents(s).find(c=>c.parent===parent);if(!c)throw Error('Changed');h.found(s,c,expected);message='Found direct living offspring #'+c.id+' of #'+parent+'. Compare inherited traits below; not proof of adaptation.';}catch{message='Found patch changed before inspection. Refresh and search again.';}}
    else message=result===0?'No safely frameable direct living offspring found during this scan.':'Search stopped: world, selected patch or living parent changed. Refresh first.';
    emit();
   }next(true);return true;
  }
  return {start,cancel,setSource};
 }
 const api={parents,create};if(typeof module==='object'&&module.exports)module.exports=api;else root.StellaOffspringSearch=api;
})(typeof globalThis!=='undefined'?globalThis:this);
