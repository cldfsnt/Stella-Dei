const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const shell=fs.readFileSync('web/shell.html','utf8');
test('arrival effects control uses authoritative result and is independent of seed hints',()=>{
 const b={setAttribute(k,v){this[k]=v;}};let state=1,blocked=false,calls=[];
 const Module={started:true,failed:false,_stella_arrival_effects(m){calls.push(m);if(m>=0&&!blocked)state=m;return blocked&&m>=0?-1:state;}};
 const document={getElementById(id){assert.equal(id,'arrival-effects-toggle');return b;}};
 const start=shell.indexOf('function refreshArrivalEffects()'),end=shell.indexOf("document.getElementById('seed-targets-toggle').onclick",start);
 const ctx=vm.createContext({Module,document});vm.runInContext(shell.slice(start,end),ctx);
 vm.runInContext('refreshArrivalEffects()',ctx);assert.equal(b['aria-pressed'],'true');
 b.onclick();assert.equal(state,0);assert.equal(b.textContent,'Show arrival/loss effects');assert.equal(b['aria-pressed'],'false');
 b.onclick();assert.equal(state,1);blocked=true;b.onclick();assert.equal(state,1);assert.equal(b['aria-pressed'],'true');
 Module.failed=true;vm.runInContext('refreshArrivalEffects()',ctx);assert.equal(b.disabled,true);
 assert.deepEqual(calls.filter(x=>x>=0),[0,1,0]);
});
test('native hide discards only visual receipts and export remains guarded',()=>{
 const play=fs.readFileSync('src/states/play.zig','utf8'),main=fs.readFileSync('src/main.zig','utf8');
 const setter=play.slice(play.indexOf('pub fn setArrivalEffectsVisible'),play.indexOf('pub fn setSeedTargetsVisible'));
 assert.match(setter,/discardThrough\(self\.planet\.propaguleFeedback\.next_serial-1\)/);assert.doesNotMatch(setter,/propaguleFeedback\s*=/);
 const render=play.slice(play.indexOf('fn renderPropaguleFeedback'),play.indexOf('fn renderSeedZones'));
 assert.ok(render.indexOf('!self.arrivalEffectsVisible')<render.indexOf('const tracker='));assert.match(render,/discardThrough/);
 const bridge=main.slice(main.indexOf('export fn stella_arrival_effects'),main.indexOf('export fn stella_seed_colony'));
 assert.match(bridge,/webEditableState/);assert.match(bridge,/mode < -1 or mode > 1/);
 assert.match(shell,/id="arrival-effects-toggle" aria-pressed="true"/);
 assert.match(fs.readFileSync('web/build.sh','utf8'),/_stella_arrival_effects,/);
});
