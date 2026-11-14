const {describe}=require('../waterline-feedback.js');const assert=require('node:assert/strict');
const data={waterline:{zone:'exposed_film',growth_environment_ok:false,living_descendants:2,supported_descendants:1,observed_paid_arrivals_still_present:1}};const before=JSON.stringify(data);
assert.match(describe(data).label,/growth blocked/);assert.match(describe(data).help,/not proof of shore adaptation/);assert.match(describe(data).evidence,/session-only/);assert.equal(JSON.stringify(data),before);
assert.match(describe({}).label,/unavailable/);
assert.match(describe({waterline:{zone:'wet_edge',growth_environment_ok:true}}).label,/growth conditions possible/);
assert.match(describe({waterline:{zone:'wet_edge',growth_environment_ok:false}}).help,/Temperature/);
assert.match(describe({waterline:{zone:'dry',growth_environment_ok:false}}).help,/No photosynthesis/);
console.log('Waterline feedback:5 conditions and immutability pass');
