const assert=require('node:assert/strict');
const{createStorage}=require('../wind-storage.js');
const W='/saves/world.json',B='/saves/world.pre-v7.json';
const bytes=s=>typeof s==='string'?new TextEncoder().encode(s):Uint8Array.from(s);
const copy=m=>new Map([...m].map(([k,v])=>[k,Uint8Array.from(v)]));
const tick=()=>new Promise(resolve=>setImmediate(resolve));
function mock(initial={},version=7,options={targetSchemaVersion:version}){
 const durable=new Map(Object.entries(initial).map(([k,v])=>[k,bytes(v)]));let files=copy(durable);
 const pending=[],events=[],feedback=[],reads=[];let saves=0,loads=0,saveCode=0,loadCode=0,writeError=null,readError=null;
 const module={IDBFS:{},FS:{
  analyzePath:path=>({exists:path==='/saves'||files.has(path)}),mkdir(){},mount(){},
  open(path){if(!files.has(path))throw Error('Missing file');return{path};},close(){},
  read(stream,target,offset,length,position){reads.push(length);const source=files.get(stream.path).subarray(position,position+length);target.set(source,offset);return source.length;},
  readFile(path){if(readError===path)throw Error('Read blocked');if(!files.has(path))throw Error('Missing file');return Uint8Array.from(files.get(path));},
  writeFile(path,value){events.push(['write',path]);if(writeError)throw writeError;files.set(path,Uint8Array.from(value));},
  rename(a,b){assert.ok(files.has(a));events.push(['rename',a,b]);files.set(b,files.get(a));files.delete(a);},
  syncfs(populate,cb){events.push(['sync',populate]);pending.push({populate,cb});},
 },_stella_save(){saves++;events.push(['native-save']);if(saveCode===0)files.set(W,bytes('{"version":'+version+',"world":"new"}'));return saveCode;},_stella_load(){loads++;return loadCode;}};
 module._stella_save_expected=(world,writer)=>module._stella_save();
 const storage=createStorage(module,(...args)=>feedback.push(args),options);
 return{storage,module,feedback,events,reads,durable,get files(){return files;},get saves(){return saves;},get loads(){return loads;},get pending(){return pending;},set saveCode(v){saveCode=v;},set loadCode(v){loadCode=v;},set writeError(v){writeError=v;},set readError(v){readError=v;},
  complete(error=null){assert.ok(pending.length,'Expected a pending storage sync');const next=pending.shift();if(!error){if(next.populate)files=copy(durable);else{durable.clear();for(const[k,v]of files)durable.set(k,Uint8Array.from(v));}}next.cb(error);},
  async init(){const p=storage.initialize();this.complete();assert.equal(await p,true);},
 };
}
(async()=>{
 const P='/saves/world.pre-v11.json';let identity={world_serial:42,writer_version:7};
 const opts={preserveLegacyThroughVersion:6,readWriterIdentity:()=>({...identity})};
 const old7=bytes('{"version":7,"world":"before-wind"}'),old6=bytes('{"version":6,"world":"older"}');
 const m=mock({[W]:old7,[B]:old6},7,opts);await m.init();
 const classic=m.storage.save();await tick();assert.equal(m.saves,1);assert.equal(m.files.has(P),false);m.complete();assert.equal(await classic,true);
 // Capture the actual most recent classic save, not its earlier ancestor.
 const latest=Uint8Array.from(m.files.get(W));identity={world_serial:43,writer_version:11};m.module._stella_save=()=>{m.events.push(['wind-native']);m.files.set(W,bytes('{"version":11,"world":"wind"}'));return 0;};
 const first=m.storage.save();assert.equal(m.events.some(e=>e[0]==='wind-native'),false);assert.deepEqual(m.files.get(P),latest);assert.deepEqual(m.files.get(B),old6);m.complete();await tick();assert.equal(m.events.filter(e=>e[0]==='wind-native').length,1);m.complete();assert.equal(await first,true);assert.deepEqual(m.durable.get(P),latest);
 const again=m.storage.save();await tick();assert.equal(m.pending.length,1);m.complete();assert.equal(await again,true);assert.deepEqual(m.durable.get(P),latest);
 // Mismatched immutable backup, opaque/unknown prior bytes, missing identity fail closed.
 for(const initial of [{[W]:'opaque'},{[W]:'{"version":10}'},{[W]:' '.repeat(300)+'{"version":7}'}]){
  const x=mock(initial,11,opts);await x.init();const before=copy(x.files);assert.equal(await x.storage.save(),false);assert.equal(x.saves,0);assert.deepEqual(x.files,before);
 }
 const missing=mock({[W]:old7},11,{readWriterIdentity:()=>null});await missing.init();assert.equal(await missing.storage.save(),false);assert.equal(missing.saves,0);
 // Distinct later classic saves get immutable content-addressed backups; first remains untouched.
 const digest=b=>require('node:crypto').createHash('sha256').update(b).digest('hex');
 const hashed='/saves/world.pre-v11.sha256-'+digest(old7)+'.json';
 const pending=async x=>{for(let i=0;i<10000&&!x.pending.length;i++)await tick();assert.ok(x.pending.length,'hash must finish before backup sync');};
 const second=mock({[W]:old7,[P]:old6},11,opts);await second.init();const sp=second.storage.save();await pending(second);assert.deepEqual(second.files.get(P),old6);assert.deepEqual(second.files.get(hashed),old7);assert.equal(second.saves,0);second.complete();await tick();second.complete();assert.equal(await sp,true);
 const same=mock({[W]:old7,[P]:old6,[hashed]:old7},11,opts);await same.init();const dp=same.storage.save();await pending(same);assert.equal(same.events.filter(e=>e[0]==='write').length,0);same.complete();await tick();same.complete();assert.equal(await dp,true);
 const corrupt=mock({[W]:old7,[P]:old6,[hashed]:old6},11,opts);await corrupt.init();assert.equal(await corrupt.storage.save(),false);assert.equal(corrupt.saves,0);assert.deepEqual(corrupt.files.get(hashed),old6);
 const cryptoDescriptor=Object.getOwnPropertyDescriptor(globalThis,'crypto');Object.defineProperty(globalThis,'crypto',{value:undefined,configurable:true});
 try{const nohash=mock({[W]:old7,[P]:old6},11,opts);await nohash.init();assert.equal(await nohash.storage.save(),false);assert.equal(nohash.saves,0);}finally{Object.defineProperty(globalThis,'crypto',cryptoDescriptor);}
 // Quota aborts before native save; retry resyncs the same in-memory backup.
 const q=mock({[W]:old7},11,opts);await q.init();const fail=q.storage.save();q.complete(Error('quota'));assert.equal(await fail,false);assert.equal(q.saves,0);assert.deepEqual(q.durable.get(W),old7);
 const retry=q.storage.save();assert.equal(q.saves,0);q.complete();await tick();assert.equal(q.saves,1);q.complete();assert.equal(await retry,true);assert.deepEqual(q.durable.get(P),old7);
 // Async world/law changes and prior-byte changes cannot serialize a different world.
 for(const change of ['world','law','bytes']){identity={world_serial:43,writer_version:11};const x=mock({[W]:old7},11,opts);await x.init();const saving=x.storage.save();assert.equal(await x.storage.save(),false);assert.equal(await x.storage.load(),false);if(change==='world')identity.world_serial++;if(change==='law')identity.writer_version=7;if(change==='bytes')x.files.set(W,old6);x.complete();assert.equal(await saving,false);assert.equal(x.saves,0);}
 identity={world_serial:43,writer_version:11};
 const absent=mock({[W]:old7},11,opts);await absent.init();delete absent.module._stella_save_expected;assert.equal(await absent.storage.save(),false);assert.equal(absent.saves,0);assert.equal(absent.files.has(P),false);
 const staleNative=mock({[W]:old7},11,opts);await staleNative.init();let nativeArgs;staleNative.module._stella_save_expected=(w,v)=>{nativeArgs=[w,v];return -6;};const sn=staleNative.storage.save();staleNative.complete();assert.equal(await sn,false);assert.deepEqual(nativeArgs,[43,11]);assert.equal(staleNative.saves,0);assert.deepEqual(staleNative.files.get(W),old7);
 const hashQuota=mock({[W]:old7,[P]:old6},11,opts);await hashQuota.init();const hq=hashQuota.storage.save();await pending(hashQuota);hashQuota.complete(Error('hash branch quota'));assert.equal(await hq,false);assert.equal(hashQuota.saves,0);assert.deepEqual(hashQuota.durable.get(W),old7);assert.deepEqual(hashQuota.durable.get(P),old6);
 const fresh=mock({},11,opts);await fresh.init();const f=fresh.storage.save();await tick();assert.equal(fresh.saves,1);assert.equal(fresh.files.has(P),false);fresh.complete();assert.equal(await f,true);
 console.log('PASS wind candidate: latest v7 protected only before v11, prior backup intact, unknown/mismatch/quota/async identity fail closed, busy gate and retry');
})().catch(e=>{console.error(e);process.exitCode=1;});
