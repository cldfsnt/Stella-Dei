const assert=require('node:assert/strict'),{create}=require('../life-trend.js');
const snap=(day,mass,cell=1)=>({status:'origin',cell,day,cohorts:[{biomass:mass}]});
function observe(t,values,cell=1){return values.map((v,i)=>t.sample(snap(i*.5,v,cell))).at(-1)}
let t=create();assert.equal(observe(t,[.02,.019,.018,.017,.016]).direction,'falling');
t=create();assert.equal(observe(t,[.02,.023,.024,.025,.026]).direction,'rising');
t=create();assert.equal(observe(t,[.02,.02,.02,.02,.0201]).direction,'steady');
t=create();assert.equal(observe(t,[.02,.015,.01,.005,0]).direction,'lost');
t=create();assert.equal(observe(t,[0,.01,.02,.03,.04]),null); // no percent against zero
assert.equal(t.sample(snap(0,.02)),null); // rewind/load resets
t=create();t.sample(snap(0,.02));assert.equal(t.sample(snap(10,.01)),null);
t=create();t.sample(snap(0,.02));t.forget(1);assert.equal(t.sample(snap(2,.03)),null);
t=create();observe(t,[.02,.02,.02,.02,.02]);t.reset();assert.equal(t.sample(snap(2,.1)),null);
assert.equal(t.sample(snap(3,NaN)),null);assert.equal(t.sample(snap(3,-1)),null);
console.log('PASS net biomass trend: measured window, death, no zero baseline, gaps, load/rewind/action reset and invalid data');
// Inspect retained arrays without adding a production diagnostics API.
const vm=require('node:vm'),fs=require('node:fs');let storage;
class ObservedMap extends Map{constructor(){super();storage=this;}}
const context={module:{exports:{}},Map:ObservedMap};
vm.runInNewContext(fs.readFileSync(require.resolve('../life-trend.js'),'utf8'),context);
const bounded=context.module.exports.create;
t=bounded();
for(let i=0;i<100000;i++){
 assert.equal(t.sample(snap(i*1e-8,1+i*1e-6)),null);
 assert.ok(storage.get(1).length<=64);
 assert.equal(storage.get(1)[0].day,0);
 assert.equal(storage.get(1).at(-1).day,i*1e-8);
}
let result=t.sample(snap(2,2));assert.equal(result.days,2);assert.equal(result.from,1);assert.equal(result.to,2);
// Equal time updates the actual endpoint, not a new point or a false gap.
let length=storage.get(1).length;result=t.sample(snap(2,3));assert.equal(storage.get(1).length,length);assert.equal(result.to,3);
// Long real gap resets even after heavy decimation.
assert.equal(t.sample(snap(4.000001,4)),null);assert.equal(storage.get(1).length,1);
assert.equal(t.sample(snap(0,1)),null);assert.equal(storage.get(1).length,1);
// Cross the window repeatedly; compare reported endpoints with retained REAL samples.
t=bounded();
for(let i=0;i<100000;i++){
 const day=i*0.0001,mass=1+day;result=t.sample(snap(day,mass));
 const history=storage.get(1);assert.ok(history.length<=64);
 for(const point of history)assert.equal(point.mass,1+point.day);
 if(result){assert.equal(result.days,day-history[0].day);assert.equal(result.from,history[0].mass);assert.equal(result.to,mass);}
}
// Zero baseline never yields an invented percentage after thinning.
t=bounded();for(let i=0;i<100000;i++)t.sample(snap(i*1e-8,i*1e-6));assert.equal(t.sample(snap(2,1)),null);
// LRU bound and explicit reset/forget remain intact.
t=bounded();for(let cell=0;cell<100;cell++)t.sample(snap(0,1,cell));assert.equal(storage.size,32);
assert.ok(!storage.has(0));t.forget(99);assert.ok(!storage.has(99));t.reset();assert.equal(storage.size,0);
console.log('PASS bounded trend: 100k tiny advances, actual endpoints, repeated windows, same-time updates, real gaps, rewind, zero baseline and 32×64 storage');
