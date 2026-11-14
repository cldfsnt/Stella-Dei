const assert=require('node:assert/strict');
const{createStorage}=require('../stella-storage.js');
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
 const storage=createStorage(module,(...args)=>feedback.push(args),options);
 return{storage,module,feedback,events,reads,durable,get files(){return files;},get saves(){return saves;},get loads(){return loads;},get pending(){return pending;},set saveCode(v){saveCode=v;},set loadCode(v){loadCode=v;},set writeError(v){writeError=v;},set readError(v){readError=v;},
  complete(error=null){assert.ok(pending.length,'Expected a pending storage sync');const next=pending.shift();if(!error){if(next.populate)files=copy(durable);else{durable.clear();for(const[k,v]of files)durable.set(k,Uint8Array.from(v));}}next.cb(error);},
  async init(){const p=storage.initialize();this.complete();assert.equal(await p,true);},
 };
}
(async()=>{
 // Backup is exact and durable BEFORE the native writer runs; one busy gate
 // spans both syncs and serialization. The backup remains immutable thereafter.
 const old=bytes('{"version":6,"world":"old","unicode":"🌍"}');
 const a=mock({[W]:old});await a.init();
 const first=a.storage.save();assert.equal(a.saves,0);assert.equal(a.storage.state().busy,true);
 assert.equal(await a.storage.save(),false);assert.equal(await a.storage.load(),false);
 assert.equal(a.storage.state().backup.durable,false);assert.deepEqual(a.files.get(W),old);assert.deepEqual(a.files.get(B),old);
 assert.equal(a.durable.has(B),false);a.complete();await tick();
 assert.equal(a.saves,1);assert.deepEqual(a.durable.get(B),old);assert.deepEqual(a.durable.get(W),old);
 assert.equal(a.storage.state().backup.status,'created');assert.equal(a.storage.state().backup.durable,true);
 assert.ok(!a.feedback.some(([s])=>s.startsWith('Saved in')));a.complete();assert.equal(await first,true);
 assert.match(a.feedback.at(-1)[0],/automatic restore is not available/);
 const backed=Uint8Array.from(a.durable.get(B));
 const second=a.storage.save();await tick();assert.equal(a.pending.length,1);a.complete();assert.equal(await second,true);
 assert.deepEqual(a.durable.get(B),backed);assert.equal(a.events.filter(e=>e[0]==='rename').length,1);
 assert.ok(a.reads.every(n=>n<=256));

 // A failed backup sync must abort BEFORE overwrite and cannot turn mere local
 // existence into permission to overwrite on retry.
 const q=mock({[W]:old});await q.init();const failed=q.storage.save();q.complete(Error('Quota exceeded'));
 assert.equal(await failed,false);assert.equal(q.saves,0);assert.deepEqual(q.files.get(W),old);assert.deepEqual(q.durable.get(W),old);
 assert.equal(q.storage.state().busy,false);assert.equal(q.module.storageOperation,false);assert.equal(q.storage.state().backup.durable,false);
 assert.match(q.feedback.at(-1)[0],/previous save was not replaced/);assert.match(q.feedback.at(-1)[0],/Quota exceeded/);
 const retry=q.storage.save();assert.equal(q.saves,0);assert.equal(q.pending.length,1);q.complete();await tick();assert.equal(q.saves,1);q.complete();assert.equal(await retry,true);
 assert.deepEqual(q.durable.get(B),old);assert.equal(q.events.filter(e=>e[0]==='rename').length,1);

 // Existing backup is not replaced by a different legacy save. It must be
 // readable and synced before this instance trusts it as durable.
 const e=mock({[W]:'{"version":6,"world":"later"}',[B]:old});await e.init();const existing=e.storage.save();
 assert.equal(e.saves,0);assert.equal(e.storage.state().backup.status,'present');e.complete();await tick();e.complete();assert.equal(await existing,true);
 assert.deepEqual(e.durable.get(B),old);assert.equal(e.events.filter(x=>x[0]==='write').length,0);

 // New worlds and confidently v7 files need no legacy-copy sync. The default
 // legacy caller is separately covered by storage.test.cjs; v6 opt-in is inert.
 for(const state of [{},{[W]:'{"version":7,"world":"current"}'}]){
  const m=mock(state);await m.init();const p=m.storage.save();await tick();assert.equal(m.saves,1);assert.equal(m.pending.length,1);m.complete();assert.equal(await p,true);assert.equal(m.durable.has(B),false);
 }
 const v6=mock({[W]:old},6);await v6.init();const p6=v6.storage.save();assert.equal(v6.saves,1);v6.complete();assert.equal(await p6,true);assert.equal(v6.durable.has(B),false);assert.equal(v6.reads.length,0);

 // Explicit preservation boundary is independent of the runtime writer schema:
 // climate v20 still writes v6, but protects the pre-update v6 world exactly once.
 for(const previous of [old,bytes('opaque old climate save')]){
  const climate=mock({[W]:previous},6,{preserveLegacyThroughVersion:6});await climate.init();
  const pc=climate.storage.save();assert.equal(climate.saves,0);assert.deepEqual(climate.files.get(B),previous);
  climate.complete();await tick();assert.equal(climate.saves,1);assert.deepEqual(climate.durable.get(B),previous);
  climate.complete();assert.equal(await pc,true);assert.equal(JSON.parse(new TextDecoder().decode(climate.durable.get(W))).version,6);
  const again=climate.storage.save();await tick();assert.equal(climate.pending.length,1);climate.complete();assert.equal(await again,true);
  assert.deepEqual(climate.durable.get(B),previous);assert.equal(climate.events.filter(x=>x[0]==='rename').length,1);
 }

 // Nonstandard/long headers and opaque bytes are preserved without JSON.parse.
 const opaque=bytes(' '.repeat(300)+'{"payload":"legacy","version":6}');opaque[opaque.length-1]=255;
 const u=mock({[W]:opaque});await u.init();const pu=u.storage.save();assert.equal(u.saves,0);assert.deepEqual(u.files.get(B),opaque);assert.equal(u.storage.state().backup.version,null);u.complete();await tick();u.complete();assert.equal(await pu,true);assert.deepEqual(u.durable.get(B),opaque);

 // Read/write failures cannot invoke the serializer. A final world-sync quota
 // failure still leaves the already durable original backup available.
 const w=mock({[W]:old});await w.init();w.writeError=Error('Write quota');assert.equal(await w.storage.save(),false);assert.equal(w.saves,0);assert.deepEqual(w.files.get(W),old);
 const r=mock({[W]:old,[B]:old});await r.init();r.readError=B;assert.equal(await r.storage.save(),false);assert.equal(r.saves,0);assert.deepEqual(r.files.get(W),old);
 const f=mock({[W]:old});await f.init();const pf=f.storage.save();f.complete();await tick();f.complete(Error('World quota'));assert.equal(await pf,false);assert.deepEqual(f.durable.get(B),old);assert.deepEqual(f.durable.get(W),old);assert.equal(f.module.storageOperation,false);

 // Serialization and invalid-load failures retain the immutable backup and
 // never trigger an automatic restore or an extra native writer.
 const s=mock({[W]:old});await s.init();s.saveCode=-2;const ps=s.storage.save();s.complete();assert.equal(await ps,false);assert.deepEqual(s.files.get(W),old);assert.deepEqual(s.durable.get(B),old);
 s.loadCode=-2;const pl=s.storage.load();s.complete();assert.equal(await pl,false);assert.equal(s.saves,1);assert.equal(s.loads,1);assert.deepEqual(s.durable.get(W),old);
 const state=s.storage.state();state.backup.durable=true;assert.equal(s.storage.state().backup.durable,false);
 console.log('PASS: opt-in v7 exact durable pre-upgrade backup, ordering, immutable retries, quota/read/write failure gates, bounded unknown headers, busy dedup, no automatic restore');
})().catch(error=>{console.error(error);process.exit(1)});
