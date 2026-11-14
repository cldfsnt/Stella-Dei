const assert=require('node:assert/strict');const{createStorage}=require('../stella-storage.js');
(async()=>{
 const feedback=[],syncs=[];let callback;const module={FS:{analyzePath:()=>({exists:false}),mkdir(){},mount(){},syncfs:(populate,cb)=>{syncs.push(populate);callback=cb;}},IDBFS:{},_stella_save:()=>0,_stella_load:()=>0};const storage=createStorage(module,(...args)=>feedback.push(args));
 const init=storage.initialize();assert.equal(storage.state().available,false);callback(null);assert.equal(await init,true);
 const save=storage.save();assert.equal(storage.state().busy,true);assert.equal(await storage.save(),false);assert.ok(!feedback.some(([text])=>text.startsWith('Saved')));callback(null);assert.equal(await save,true);assert.ok(feedback.at(-1)[0].startsWith('Saved'));assert.deepEqual(syncs,[true,false]);
 const fail=storage.save();callback(Error('Quota exceeded'));assert.equal(await fail,false);assert.equal(feedback.at(-1)[1],true);assert.equal(module.storageOperation,false);
 module._stella_save=()=>-1;assert.equal(await storage.save(),false);assert.match(feedback.at(-1)[0],/Create or load/);
 module._stella_load=()=>-1;let pending=storage.load();callback(null);assert.equal(await pending,false);assert.match(feedback.at(-1)[0],/No saved planet/);
 module._stella_load=()=>-2;pending=storage.load();callback(null);assert.equal(await pending,false);assert.match(feedback.at(-1)[0],/invalid/);
 module._stella_load=()=>0;pending=storage.load();callback(null);assert.equal(await pending,true);
 const unavailable=createStorage({...module,FS:{analyzePath(){throw Error('blocked')}}},()=>{});assert.equal(await unavailable.initialize(),false);assert.equal(await unavailable.save(),false);
 console.log('PASS: initialize sync, persistence completion gate, busy dedup, quota errors, missing/corrupt loads, unavailable storage');
})().catch(e=>{console.error(e);process.exit(1)});
