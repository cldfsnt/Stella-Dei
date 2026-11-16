"""Adapt only three COPIED storage fixtures; preserve every assertion.
Writer6-only historical cases run unchanged legacy source through an FS namespace
proxy, never pretending a combined writer7 emits6. All supported writers use the
actual combined module with authoritative identity and guarded native forwarding.
"""
from pathlib import Path
import sys,hashlib,json
out=Path(sys.argv[1]).resolve();assert out.name=='web' and out.parent.name=='root-wind-ui'
r=Path(__file__).resolve().parents[2];tests=out/'tests'
p=tests/'storage.test.cjs';s=p.read_text();needle='const storage=createStorage(module,(...args)=>feedback.push(args));';assert s.count(needle)==1
s=s.replace(needle,"module._stella_save_expected=(world,writer)=>{assert.deepEqual([world,writer],[42,7]);return module._stella_save();};const storage=createStorage(module,(...args)=>feedback.push(args),{readWriterIdentity:()=>({world_serial:42,writer_version:7})});")
p.write_text(s)
p=tests/'save-size-safety.test.cjs';s=p.read_text();needle='const store=createStorage(module,(...x)=>messages.push(x));';assert s.count(needle)==1
s=s.replace(needle,"module.FS.readFile=()=>new TextEncoder().encode('{\"version\":10}');module._stella_save_expected=(world,writer)=>{assert.deepEqual([world,writer],[42,10]);return module._stella_save();};const store=createStorage(module,(...x)=>messages.push(x),{readWriterIdentity:()=>({world_serial:42,writer_version:10})});")
p.write_text(s)
p=tests/'storage-upgrade.test.cjs';s=p.read_text();needle='const storage=createStorage(module,(...args)=>feedback.push(args),options);';assert s.count(needle)==1
s=s.replace(needle,"""// Combined never has a writer6. Keep those old assertions against the exact
 // unchanged legacy reference, translating only its FS namespace in the mock.
 let storage;
 if(version===6){
  const path=require('node:path');const legacy=require(path.resolve(__dirname,'../../../../stella-independent-review/web/stella-storage.js'));
  const fsProxy=new Proxy(module.FS,{get(target,key){const value=target[key];return typeof value==='function'?function(...args){return value.apply(target,args.map(x=>typeof x==='string'&&x.startsWith('/saves')?'/wetlands-saves'+x.slice(6):x));}:value;}});
  const referenceModule=new Proxy(module,{get(target,key){return key==='FS'?fsProxy:target[key];}});
  storage=legacy.createStorage(referenceModule,(...args)=>feedback.push(args),options);
  console.log('LEGACY-REFERENCE ONLY: exact original writer6 storage behavior');
 }else{
  module._stella_save_expected=(world,writer)=>{assert.deepEqual([world,writer],[42,version]);return module._stella_save();};
  storage=createStorage(module,(...args)=>feedback.push(args),{...options,readWriterIdentity:()=>({world_serial:42,writer_version:version})});
 }""")
p.write_text(s)
reference=r/'web/stella-storage.js';print(json.dumps({'reference':str(reference),'sha256':hashlib.sha256(reference.read_bytes()).hexdigest(),'writer6_scope':'legacy-reference-only, unmodified source; mock namespace proxy','adapted_files':['storage.test.cjs','storage-upgrade.test.cjs','save-size-safety.test.cjs']},indent=2))
