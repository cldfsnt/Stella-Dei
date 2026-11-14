const assert=require('node:assert/strict'),{create}=require('../gameplay-measure');
let time=0,enables=[],notes=[],data={world_serial:1,paused:false,menu_open:false,interrupted:false,game_time:100,requested:86400,enabled:true,frames:60};
const m=create({now:()=>time,read:()=>data,enable:v=>(enables.push(v),true),notify:(text,running)=>notes.push({text,running})});
assert(m.start());for(time=250;time<=9750;time+=250)m.tick();time=9999;data.game_time=200;m.tick();assert(m.isRunning());time=10250;data.game_time=300;m.tick();assert(!m.isRunning());assert.equal(m.result().elapsed_ms,10250);assert.equal(m.result().achieved,200/10.25);assert.equal(enables.at(-1),false);
const previous=m.result();data.game_time=999;assert.equal(previous.sample.game_time,300,'retained copy owned');
for(const [field,value] of [['paused',true],['menu_open',true],['interrupted',true],['world_serial',2],['requested',3600],['enabled',false]]){
 data={world_serial:1,paused:false,menu_open:false,interrupted:false,game_time:400,requested:86400,enabled:true,frames:60};assert(m.start());data[field]=value;time+=100;m.tick();assert(!m.isRunning());assert.equal(m.result(),previous);assert.equal(enables.at(-1),false);
}
data={world_serial:1,paused:false,menu_open:false,interrupted:false,game_time:500,requested:86400,enabled:true,frames:60};assert(m.start());time+=500;assert(m.start());for(let i=0;i<39;i++){time+=250;m.tick();}assert(m.isRunning());m.cancel('Canceled');assert(!m.isRunning());assert.equal(m.result(),previous);
data.interrupted=true;assert(m.start(),'prior interruption does not reject a new reset session');data.interrupted=false;time+=250;m.tick();assert(m.isRunning());time+=5000;m.tick();assert(!m.isRunning());assert.match(notes.at(-1).text,/stalled or suspended/);
data.paused=true;assert(!m.start());data=null;assert(!m.start());assert.equal(m.result(),previous);
console.log('PASS: actual elapsed time, immutable retained copy, pause/menu/background cancel API, world/speed/session guards, repeat/cancel and prior result preservation');
