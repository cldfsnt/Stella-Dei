const assert = require('node:assert/strict');
const { createTouchControls } = require('../touch-controls.js');
const events=[], zooms=[], timers=new Map(); let timerId=0;
const input=createTouchControls({mouse:(type,p,button)=>events.push({type,...p,button}),zoom:s=>zooms.push(s),schedule:fn=>{timers.set(++timerId,fn);return timerId;},cancel:id=>timers.delete(id)});
const event=(id,x,y,type='pointerdown',pointerType='touch')=>({pointerId:id,clientX:x,clientY:y,type,pointerType,preventDefault(){}});
const clean=()=>{input.reset();events.length=0;zooms.length=0;};
const flush=()=>{for(const [id,fn] of [...timers]){timers.delete(id);fn();}};
// Two-finger pinch produces zoom only, not a plant/rabbit placement.
input.down(event(1,100,100)); input.down(event(2,200,100)); input.move(event(2,300,100,'pointermove'));
assert.equal(events.length,0); assert.ok(zooms[0]>0);
input.up(event(2,300,100,'pointerup')); input.move(event(1,130,140,'pointermove'));input.up(event(1,130,140,'pointerup'));
assert.equal(events.length,0); assert.equal(input.state().pointers,0);
// Pinch inward reverses zoom, and behaves identically in paint mode.
clean(); input.setMode('paint'); input.down(event(1,100,100)); input.down(event(2,300,100)); input.move(event(2,200,100,'pointermove'));
assert.ok(zooms[0]<0); assert.equal(events.length,0); input.reset();
// Tap remains held over frames so polling engine sees it, then releases.
clean(); input.down(event(1,100,100)); assert.equal(events.length,0); input.up(event(1,100,100,'pointerup'));
assert.deepEqual(events.map(e=>e.type),['mousemove','mousedown']); assert.equal(events[1].button,0);flush();assert.equal(events.at(-1).type,'mouseup');
// Navigate drag uses right mouse, paint drag left mouse, both release.
for(const [mode,button] of [['navigate',2],['paint',0]]){
 clean(); input.setMode(mode);input.down(event(1,100,100));input.move(event(1,120,110,'pointermove'));input.up(event(1,120,110,'pointerup'));
 assert.deepEqual(events.map(e=>e.type),['mousemove','mousedown','mousemove','mouseup']);assert.ok(events.every(e=>e.button===button));
}
// Cancellation never becomes a tap; blur/mode switch releases a held drag.
clean();input.down(event(1,10,10));input.up(event(1,10,10,'pointercancel'));assert.equal(events.length,0);
input.down(event(1,10,10));input.move(event(1,30,30,'pointermove'));input.reset();assert.equal(events.at(-1).type,'mouseup');assert.equal(input.state().mouseDown,false);
// Quick repeated taps and third finger don't leave a button stuck.
clean();for(let i=0;i<4;i++){input.down(event(i,10,10));input.up(event(i,10,10,'pointerup'));}flush();assert.equal(input.state().mouseDown,false);
clean();input.down(event(1,0,0));input.down(event(2,100,0));input.down(event(3,50,50));input.up(event(1,0,0,'pointerup'));input.move(event(3,80,50,'pointermove'));input.up(event(2,100,0,'pointerup'));input.up(event(3,80,50,'pointerup'));assert.equal(events.length,0);
// Mouse remains handled by GLFW, not duplicated by the bridge.
clean();input.down(event(1,10,10,'pointerdown','mouse'));input.move(event(1,30,30,'pointermove','mouse'));input.up(event(1,30,30,'pointerup','mouse'));assert.equal(events.length,0);
console.log('PASS: pinch in/out, paint isolation, post-pinch suppression, taps, navigation, painting, cancellation, repeat/third finger, mouse pass-through');
// Default browser scheduler: two actual frames and 120ms minimum, cancel safe.
const saved={setTimeout:global.setTimeout,clearTimeout:global.clearTimeout,requestAnimationFrame:global.requestAnimationFrame,cancelAnimationFrame:global.cancelAnimationFrame};
const queue=new Map(),frames=new Map();let seq=0;
global.setTimeout=(fn,ms)=>{queue.set(++seq,{fn,ms});return seq};global.clearTimeout=id=>queue.delete(id);
global.requestAnimationFrame=fn=>{frames.set(++seq,fn);return seq};global.cancelAnimationFrame=id=>frames.delete(id);
const realEvents=[];const defaults=createTouchControls({mouse:type=>realEvents.push(type),zoom(){}});
const frame=()=>{for(const [id,fn]of [...frames]){frames.delete(id);fn();}};
const fire=ms=>{for(const[id,item]of [...queue])if(item.ms===ms){queue.delete(id);item.fn();}};
defaults.down(event(1,20,20));defaults.up(event(1,20,20,'pointerup'));frame();frame();assert.equal(defaults.state().mouseDown,true);fire(120);assert.equal(defaults.state().mouseDown,false);assert.equal(realEvents.at(-1),'mouseup');
defaults.down(event(1,20,20));defaults.up(event(1,20,20,'pointerup'));fire(500);assert.equal(defaults.state().mouseDown,false);
defaults.down(event(1,20,20));defaults.up(event(1,20,20,'pointerup'));defaults.reset();assert.equal(queue.size,0);assert.equal(frames.size,0);
Object.assign(global,saved);console.log('PASS: frame-aware tap minimum, timeout ceiling, cancellation cleanup');
