const assert=require('node:assert/strict');const W=require('./wetlands-preview.js');
assert.match(W.summary({}),/unavailable/);
const d={world_serial:7,cell:2,identities:[{id:'9007199254740993',living:true}],wetlands:{status:'wetlands',world_serial:7,cell:2,enabled:true,soil_kg_m2:.5,root_allocations:[{id:'9007199254740993',fraction:.25,root_tissue_kg_c_m2:.01}]}};
assert.match(W.summary(d),/9007199254740993/);assert.match(W.summary(d),/25.0%/);assert.match(W.summary(d),/not evidence/);
for(const v of [NaN,Infinity,-1,2,'0.5'])assert.match(W.summary({...d,wetlands:{...d.wetlands,soil_kg_m2:v}}),/Soil water unavailable/);
assert.doesNotMatch(W.summary({...d,identities:[]}),/paid root tissue/);
assert.match(W.graphicsFailure('error: WindowCreationFailed'),/WebGL2/);assert.equal(W.graphicsFailure('bad save'),null);
console.log('Wetlands formatter gates passed');
const fs=require('node:fs'),vm=require('node:vm');
const patched=fs.readFileSync('../site-tmp/wetlands-frontend-test/wetlands/index.html','utf8');
assert.match(patched,/id="wetlands-notice"/);assert.match(patched,/id="wetlands-readout"/);assert.match(patched,/StellaWetlands.summary\(\{\.\.\.data,wetlands\}\)/);
assert.match(patched,/at least 0.2 m/);assert.match(patched,/No automatic migration/);
const storageText=fs.readFileSync('../site-tmp/wetlands-frontend-test/wetlands/stella-storage.js','utf8');
assert(!storageText.includes('/saves'));assert(storageText.includes('/wetlands-saves/world.pre-v7.json'));
const context={module:{exports:{}},TextDecoder,Uint8Array};vm.runInNewContext(storageText,context);
const paths=[];const mock={FS:{analyzePath:p=>({exists:false}),mkdir:p=>paths.push(p),mount:(kind,options,p)=>paths.push(p),syncfs:(populate,cb)=>cb()},IDBFS:{}};
(async()=>{assert(await context.module.exports.createStorage(mock,()=>{}).initialize());assert.deepEqual(paths,['/wetlands-saves','/wetlands-saves']);console.log('Copied shell and isolated IDBFS namespace gates passed');})().catch(e=>{console.error(e);process.exitCode=1;});

assert.match(W.summary({...d,cell:3}),/unavailable/);assert.match(W.summary({...d,world_serial:8}),/unavailable/);
function flow({code=1,confirm=true,available=true,after={status:'wetlands',enabled:true,physiology_law:3,world_serial:8}}={}){
 const nodes={'wetlands-new':{},'wetlands-new-status':{}};let calls=0,changed=0,reads=0;
 W.mount({getElementById:id=>nodes[id]},{available:()=>available,snapshot:()=>++reads===1?{world_serial:7}:after,confirm:()=>confirm,create:world=>{assert.equal(world,7);calls++;return code;},created:()=>changed++});nodes['wetlands-new'].onclick();return{calls,changed,text:nodes['wetlands-new-status'].textContent,disabled:nodes['wetlands-new'].disabled};
}
assert.equal(flow().changed,1);assert.equal(flow({confirm:false}).calls,0);assert.equal(flow({available:false}).calls,0);
for(const code of [-1,-2,-3,0,99]){const r=flow({code});assert.equal(r.calls,1);assert.equal(r.changed,0);assert.equal(r.disabled,false);}
assert.equal(flow({after:{status:'legacy',world_serial:8}}).changed,0);
assert.equal(flow({after:{status:'wetlands',enabled:true,physiology_law:3,world_serial:7}}).changed,0);
assert.match(patched,/ccall\('stella_wetlands_new','number',\['number'\],\[world\]\)/);
assert(!patched.includes('fetch(\'day-30'));
console.log('Fresh-world DOM handler exact API success/cancel/stale/busy/unknown gates passed');
assert.match(W.activeLaw({status:'legacy'}),/NOT active/);
assert.match(W.activeLaw({status:'historical_beta',physiology_law:1}),/Not converted/);
assert.match(W.activeLaw({status:'wetlands',enabled:true,physiology_law:3}),/Active: Wetlands/);
assert.match(W.activeLaw(null),/No verified/);
const banner=fs.readFileSync('web/wetlands-banner.html','utf8');
assert.match(banner,/#wetlands-notice:not\(\[open\]\)\{display:block\}/);
assert.match(banner,/#wetlands-notice>summary\{min-height:44px/);
assert.match(banner,/#wetlands-notice:not\(\[open\]\)>:not\(summary\)\{display:none\}/);
assert.match(banner,/<summary>Wetlands/);
assert.match(banner,/#wetlands-notice\{bottom:auto\}/);
