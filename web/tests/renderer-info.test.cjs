const assert=require('node:assert/strict'),info=require('../renderer-info');
let calls=0;const params={1:'masked',2:'WebGL',3:'WebGL 2',4:'Mesa',5:'ANGLE llvmpipe'};
const gl={VENDOR:1,RENDERER:2,VERSION:3,drawingBufferWidth:1366,drawingBufferHeight:768,getParameter:p=>params[p],getExtension:()=>({UNMASKED_VENDOR_WEBGL:4,UNMASKED_RENDERER_WEBGL:5})};
const canvas={getContext:name=>{calls++;assert.equal(name,'webgl2');return gl;}};
assert.equal(calls,0);const d=info.capture(canvas);assert.equal(calls,1);assert.equal(d.width,1366);assert.equal(d.renderer,'ANGLE llvmpipe');assert.equal(d.software_hint,true);assert.match(info.text(d),/suggests software/);
gl.getExtension=()=>{throw Error('restricted')};params[2]='ordinary GPU';assert.equal(info.capture(canvas).software_hint,false);assert.match(info.text(info.capture(canvas)),/does not establish hardware acceleration/);
params[2]='a\n'+'b'.repeat(300);assert.equal(info.capture(canvas).renderer.length,256);assert(!info.capture(canvas).renderer.includes('\n'));
assert.deepEqual(info.capture({getContext:()=>null}),{available:false});assert.deepEqual(info.capture({getContext:()=>{throw Error()}}),{available:false});assert.match(info.text(null),/unavailable/);
console.log('PASS: explicit local capture, extension fallback, bounded strings, software hint without hardware inference');
