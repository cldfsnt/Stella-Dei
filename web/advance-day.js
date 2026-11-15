/* Explicit bounded advancement. Native state owns all ticks and redraw gating. */
(function(root){
 function valid(s){return !!s&&typeof s.available==='boolean'&&Number.isInteger(s.token)&&s.token>=0&&s.token<=4294967295&&Number.isInteger(s.world)&&s.world>=0&&s.world<=4294967295&&['idle','running','redraw','done','cancelled'].includes(s.phase)&&typeof s.busy==='boolean'&&s.busy===['running','redraw'].includes(s.phase)&&Number.isInteger(s.completed)&&s.completed>=0&&s.completed<=60&&s.total===60&&s.seconds===s.completed*1440&&typeof s.redraw_complete==='boolean'&&!(s.busy&&s.redraw_complete)&&typeof s.reason==='string'&&(s.phase!=='done'||s.completed===60);}
 function create(h){
  let locked=false,timer=null,token=null,world=null,completed=0,ready=false,priorToken=null,closing=false,requestWorld=null;
  function render(text,s=null){h.render({locked,ready,text,snapshot:s});}
  function uncertain(){ready=false;render('Status unavailable. Progress may have been made. Waiting for the game to confirm a safe redraw; no new advance will start.');}
  function accept(s){
   if(!valid(s)||(token!==null&&(s.token!==token||s.world!==world||s.completed<completed))){uncertain();return false;}
   if(token===null&&s.token===priorToken){ready=!s.busy&&s.redraw_complete;render('Advance was not confirmed as started. '+(s.reason||'No new run was recorded.'),s);return true;}
   if(token===null&&s.token>0){if(s.world!==requestWorld){uncertain();return false;}token=s.token;world=s.world;}completed=s.completed;
   ready=!s.busy&&s.redraw_complete&&s.recovery_required!==true;
   if(s.recovery_required===true){closing=false;render('Simulation stopped. Graphics context was lost; a reload is required. '+s.completed+' / 60 steps · '+(s.seconds/3600).toFixed(1)+' simulated hours completed. Progress remains in memory, not necessarily saved. A context-restored event does not rebuild the renderer.',s);return true;}
   if(closing&&ready&&s.dismissed===true&&s.input_blocked===false){unlock();return true;}
   const prefix=s.phase==='done'?'One simulated day completed.':s.phase==='cancelled'?'Advance stopped; completed progress is kept.':s.phase==='idle'?'Advance not started.':s.phase==='redraw'?(s.waiting_for_view?'Simulation stopped. Waiting for the visible tab and graphics context before restoring the globe.':'Simulation stopped. Restoring the globe…'):'Advancing simulation; globe hidden.';
   render(prefix+' '+s.completed+' / 60 steps · '+(s.seconds/3600).toFixed(1)+' / 24 simulated hours.'+(s.reason?' '+s.reason:''),s);
   return true;
  }
  function unlock(){h.clearInterval(timer);timer=null;locked=false;closing=false;h.lock(false);render('');}
  function poll(){if(!locked)return;try{accept(h.status());}catch{uncertain();}}
  function cancel(){if(!locked||ready)return;try{if(token===null){poll();if(token===null)return;}accept(h.cancel(token));}catch{uncertain();}}
  return {start(expectedWorld){if(locked)return false;const before=h.status();if(!valid(before)||before.busy||before.input_blocked===true||!before.redraw_complete)throw Error('Cannot safely start: native status is unavailable or busy.');priorToken=before.token;requestWorld=expectedWorld;closing=false;locked=true;ready=false;token=null;world=null;completed=0;h.lock(true);render('Requesting one simulated day. Globe hidden; completed progress will be kept if cancelled.');timer=h.setInterval(poll,100);try{accept(h.start(expectedWorld));}catch{uncertain();}return true;},poll,cancel,
   environment(visible,contextOk){try{const s=h.environment(visible?1:0,contextOk?1:0);if(!locked&&valid(s)&&s.recovery_required===true){locked=true;ready=false;closing=false;token=s.token;world=s.world;requestWorld=s.world;completed=s.completed;h.lock(true);timer=h.setInterval(poll,100);}if(locked)accept(s);}catch{if(locked)uncertain();}},
   dismiss(){if(!locked||!ready)return false;if(token===null){unlock();return true;}try{const s=h.dismiss(token);if(!valid(s)||s.token!==token||s.world!==world||s.dismissed!==true){ready=false;render('Return was not confirmed. Waiting for the game; no new advance will start.');return false;}closing=true;accept(s);return !locked;}catch{uncertain();return false;}},isLocked:()=>locked,isReady:()=>ready};
 }
 if(typeof module==='object'&&module.exports)module.exports={create,valid};else root.StellaAdvanceDay={create,valid};
})(typeof globalThis!=='undefined'?globalThis:this);
