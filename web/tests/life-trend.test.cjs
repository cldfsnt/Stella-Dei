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
