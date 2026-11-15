const test=require('node:test'),assert=require('node:assert/strict');const api=require('../sandbox-defense.js');
function fixture(){let v={status:'ready',world:1,cell:20,mode:'sandbox',enabled:false,kind:-1};let count=0,focus=0,last='';let response;const ui=api.create({read:()=>({...v}),act:(w,c,a)=>{count++;if(response)return response;v={...v,status:a===0?'enabled':a===3?'cancelled':'selected',enabled:a===0?true:v.enabled,kind:a===1?0:a===2?1:a===3?-1:v.kind};return {...v};},render:(_v,m)=>last=m,focus:()=>focus++});ui.refresh();return {ui,set:x=>Object.assign(v,x),response:x=>response=x,get:()=>({v,count,focus,last})};}
test('viewing is inert; explicit enable then choice and cancel never plant',()=>{const f=fixture();assert.equal(f.get().count,0);assert(f.ui.action(0));assert.equal(f.get().focus,0);assert(f.ui.action(2));assert.equal(f.get().v.kind,1);assert.equal(f.get().focus,1);assert(f.ui.action(3));assert.equal(f.get().v.kind,-1);assert.equal(f.get().v.enabled,true);});
test('stale selection/world and Origin refuse before command',()=>{for(const change of [{cell:21},{world:2},{mode:'origin'}]){const f=fixture();f.set(change);assert.equal(f.ui.action(0),false);assert.equal(f.get().count,0);}});
test('malformed or mismatched postcommand is unknown not false failed promise',()=>{for(const r of [{},{status:'enabled',world:2,cell:20,mode:'sandbox',enabled:true,kind:-1},{status:'enabled',world:1,cell:20,mode:'sandbox',enabled:false,kind:-1}]){const f=fixture();f.response(r);assert.equal(f.ui.action(0),false);assert.match(f.get().last,/Result unknown/);}});
test('refusal remains visible and no silent focus or retry',()=>{const f=fixture();f.response({status:'disabled',world:1,cell:20,mode:'sandbox',enabled:false,kind:-1});assert.equal(f.ui.action(2),false);assert.equal(f.get().focus,0);assert.equal(f.get().count,1);});
test('isolated shell hides whole Origin auto-seed block across mode flips',()=>{
 const fs=require('node:fs'),vm=require('node:vm');
 const source=fs.readFileSync(require('node:path').join(__dirname,'sandbox-defense-ui-patch.py'),'utf8');
 assert(source.includes('<div id="origin-auto-seed" hidden><button id="auto-seed-open" disabled>'));assert(source.includes('No ongoing automatic seeding.</p></div>'));
 const statement=source.match(/document\.getElementById\('origin-auto-seed'\)\.hidden=!origin;/)[0];
 const block={hidden:true};for(const origin of [false,true,false,true]){vm.runInNewContext(statement,{origin,document:{getElementById:id=>{assert.equal(id,'origin-auto-seed');return block;}}});assert.equal(block.hidden,!origin);}
});
test('tool selection preserves valid phenotype and defaults only Plant; shared native routes',()=>{
 const fs=require('node:fs');const patch=fs.readFileSync(require('node:path').join(__dirname,'sandbox-defense-tool-patch.py'),'utf8');
 assert.match(patch,/tool == \.PlaceVegetation and self\.planet\.worldMode == \.sandbox/);
 assert.match(patch,/self\.defensePlantKind < 0 or self\.defensePlantKind > 1/);
 assert(patch.includes('self.selectGameTool(tool)'));
 assert(patch.includes('v.selectGameTool(.PlaceVegetation)'));
 assert(patch.includes('Plant toughness: {d:.3}'));
});

test('retained seed choice does not promise a planting tap after another tool',()=>{const f=fixture();f.ui.action(0);f.ui.action(2);f.ui.refresh();assert.equal(f.get().last,'Seed choice: Tough.');assert.doesNotMatch(f.get().last,/Tap/);});
