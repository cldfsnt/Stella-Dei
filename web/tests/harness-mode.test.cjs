const vm=require('node:vm'),fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
let touched=0;
const context={setTimeout,Date,innerWidth:390,innerHeight:700,devicePixelRatio:1};
context.Module={started:true,_stella_camera_distance:()=>5100,_stella_world_mode:()=>1};
vm.createContext(context);vm.runInContext(fs.readFileSync(path.join(__dirname,'../gameplay-harness.js'),'utf8'),context);
context.StellaHarness.run({canvas:{getContext(){touched++;throw Error('must not execute')}}}).then(report=>{assert.equal(report.status,'blocked');assert.equal(touched,0);assert.equal(report.tests.length,0);console.log('PASS: Sandbox harness rejects Origin before touching game state');}).catch(error=>{console.error(error);process.exit(1)});
