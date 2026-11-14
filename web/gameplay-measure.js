/* One local, bounded gameplay sample; no telemetry or persistent storage. */
(function(root){
 function create({now,read,enable,notify,durationMs=10000}){
  let running=null,retained=null,lastNotice='';
  function status(text){const key=text+'|'+!!running;if(key===lastNotice)return;lastNotice=key;notify(text,!!running);}
  function cancel(reason='Measurement canceled.'){if(!running)return;running=null;enable(false);status(reason+(retained?' Previous sample kept.':''));}
  function valid(d){return d&&Number.isInteger(d.world_serial)&&typeof d.paused==='boolean'&&typeof d.menu_open==='boolean'&&typeof d.interrupted==='boolean'&&Number.isFinite(d.game_time)&&Number.isFinite(d.requested)&&d.requested>0;}
  function start(){
   cancel('Restarting measurement.');const d=read(),t=now();
   if(!valid(d)||!Number.isFinite(t)){status('Measurement unavailable. Start a world first.');return false;}
   if(d.paused||d.menu_open){status('Close in-game menus and press Play before measuring.');return false;}
   if(!enable(true)){status('Measurement could not start.');return false;}
   running={start:t,lastTick:t,world:d.world_serial,game:d.game_time,requested:d.requested};status('Measuring gameplay · 10 seconds');return true;
  }
  function tick(){
   if(!running)return;const d=read(),t=now();
   if(!valid(d)||!Number.isFinite(t)||t<running.start){cancel('Measurement stopped: unavailable data.');return;}
   if(t-running.lastTick>2000){cancel('Measurement stopped: browser stalled or suspended.');return;}running.lastTick=t;
   if(d.world_serial!==running.world){cancel('Measurement stopped: world changed.');return;}
   if(d.paused||d.menu_open||d.interrupted){cancel('Measurement stopped: paused or a menu opened.');return;}
   if(d.requested!==running.requested){cancel('Measurement stopped: speed changed.');return;}
   if(d.enabled!==true||d.game_time<running.game){cancel('Measurement stopped: diagnostic session changed.');return;}
   const elapsed=t-running.start;
   if(elapsed<durationMs){status('Measuring gameplay · '+Math.ceil((durationMs-elapsed)/1000)+' seconds');return;}
   if(!Number.isInteger(d.frames)||d.frames<1||d.frames>60){cancel('Measurement stopped: no completed frames.');return;}
   retained={sample:JSON.parse(JSON.stringify(d)),elapsed_ms:elapsed,requested:running.requested,achieved:(d.game_time-running.game)/(elapsed/1000)};
   running=null;enable(false);status('Gameplay sample ready · open Speed to review.');
  }
  return {start,tick,cancel,isRunning:()=>!!running,result:()=>retained};
 }
 if(typeof module!=='undefined'&&module.exports)module.exports={create};else root.createGameplayMeasure=create;
})(typeof window==='undefined'?globalThis:window);
