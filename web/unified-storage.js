// Isolated combined Wetlands storage. Existing classic/Wind storage remains unchanged.
(function(root){
  const legacyNamespaces={main:'/saves',wind:'/wind-saves'};
  function legacyName(name){return name==='world.json'||/^world\.pre-v(?:7|11)(?:\.sha256-[0-9a-f]{64})?\.json$/.test(name);}
  function readLegacy(source,name){
    const namespace=legacyNamespaces[source];
    if(!namespace||(name!==undefined&&!legacyName(name)))return Promise.reject(Error('Invalid historical source or file.'));
    return new Promise((resolve,reject)=>{
      const idb=globalThis.indexedDB;if(!idb)return reject(Error('Browser history storage unavailable.'));
      let request,db,missing=false,settled=false;
      const finish=(error,value)=>{if(settled)return;settled=true;if(db)db.close();error?reject(error):resolve(value);};
      try{request=idb.open(namespace);}catch(e){finish(e);return;}
      request.onupgradeneeded=event=>{missing=true;db=event.target.result;event.target.transaction.abort();};
      request.onerror=()=>missing?finish(null,name===undefined?[]:null):finish(request.error||Error('Historical storage read failed.'));
      request.onblocked=()=>finish(Error('Historical storage is busy; close other game tabs and retry.'));
      request.onsuccess=()=>{
        db=request.result;if(settled){db.close();return;}
        if(!db.objectStoreNames.contains('FILE_DATA'))return finish(Error('Historical storage format unavailable.'));
        let tx,query,result=name===undefined?[]:null;
        try{tx=db.transaction(['FILE_DATA'],'readonly');const store=tx.objectStore('FILE_DATA');query=name===undefined?store.openCursor():store.get(namespace+'/'+name);}catch(e){finish(e);return;}
        tx.onerror=tx.onabort=()=>finish(tx.error||Error('Historical storage read failed.'));
        tx.oncomplete=()=>finish(null,result);
        query.onerror=()=>finish(query.error||Error('Historical file read failed.'));
        query.onsuccess=()=>{
          if(name===undefined){const cursor=query.result;if(!cursor)return;const key=cursor.key;if(typeof key==='string'&&key.startsWith(namespace+'/')){const n=key.slice(namespace.length+1);if(legacyName(n))result.push(n);}if(result.length>512){tx.abort();return;}cursor.continue();}
          else{const entry=query.result;if(!entry)return;const raw=entry.contents;if((entry.mode&61440)!==32768||!(raw instanceof Uint8Array)||raw.byteLength<1||raw.byteLength>128*1024*1024){finish(Error('Historical file is not a bounded regular save.'));return;}result=new Uint8Array(raw);}
        };
      };
    });
  }
  function createStorage(module,feedback,options={}){
    let available=false,busy=false,lastSaveError=null,lastRecoveryError=null;
    let combinedBackup={status:'not-checked',durable:false};
    // The boundary describes the saved bytes to protect, not the running schema.
    // v20 still writes v6 but changes climate; it explicitly opts into this backup.
    const preserveLegacy=options.preserveLegacyThroughVersion===6||options.targetSchemaVersion===7;
    const worldPath='/wetlands-saves/world.json',backupPath='/wetlands-saves/world.pre-v7.json',backupTemp='/wetlands-saves/world.pre-v7.tmp';
    let backup={status:preserveLegacy?'not-checked':'disabled',durable:false,version:null};
    const sync=populate=>new Promise((resolve,reject)=>module.FS.syncfs(populate,error=>error?reject(error):resolve()));
    function versionFromBytes(bytes){
      const match=/^\uFEFF?\s*\{\s*"version"\s*:\s*(\d+)\s*[,}]/.exec(new TextDecoder().decode(bytes.subarray(0,256)));
      return match?Number(match[1]):null;
    }
    function savedVersion(){
      // Native serializers put version first. Unknown/long/nonstandard headers
      // are backed up conservatively; never parse the whole world just to inspect it.
      const stream=module.FS.open(worldPath,'r');
      try{
        const bytes=new Uint8Array(256);
        const count=module.FS.read(stream,bytes,0,bytes.length,0);
        const match=/^\uFEFF?\s*\{\s*"version"\s*:\s*(\d+)\s*[,}]/.exec(new TextDecoder().decode(bytes.subarray(0,count)));
        return match?Number(match[1]):null;
      }finally{module.FS.close(stream);}
    }
    function unsupportedPreview(version){

      if(version===12)return 'Version 12 is a research preview save. Use its original research preview, not this Wetlands preview. The current world is unchanged; the saved file was not replaced.';
      return null;
    }
    async function preserveLegacySave(){
      if(!preserveLegacy)return;
      try{
        if(!module.FS.analyzePath(worldPath).exists){if(backup.status==='not-checked')backup.status='not-needed';return;}
        const version=savedVersion();
        if(Number.isSafeInteger(version)&&version>6){if(backup.status==='not-checked')backup.status='not-needed';return;}
        const exists=module.FS.analyzePath(backupPath).exists;
        if(exists){
          // Confirm it is a readable file, not a directory or broken entry.
          module.FS.readFile(backupPath,{encoding:'binary'});
          if(backup.status!=='created')backup.status='present';
        }else{
          backup={status:'creating',durable:false,version:version>=1&&version<=6?version:null};
          feedback('Keeping an exact copy of your previous browser save before upgrading…');
          const bytes=module.FS.readFile(worldPath,{encoding:'binary'});
          module.FS.writeFile(backupTemp,bytes);
          if(!equalBytes(bytes,module.FS.readFile(backupTemp,{encoding:'binary'})))throw Error('Legacy backup write verification failed');
          module.FS.rename(backupTemp,backupPath);
          if(!equalBytes(bytes,module.FS.readFile(backupPath,{encoding:'binary'})))throw Error('Legacy backup readback verification failed');
          backup.status='created';
        }
        // A prior failed sync may leave a backup only in memory. Do not let
        // mere file existence authorize overwriting the older canonical save.
        if(!backup.durable){await sync(false);backup.durable=true;}
      }catch(error){
        backup.durable=false;
        throw Error('Could not safely preserve the previous save ('+error.message+'). The previous save was not replaced; free browser space and try again.');
      }
    }
    function writerIdentity(){
      if(typeof module._stella_save_expected!=='function')throw Error('Guarded save unavailable; previous save not replaced.');
      if(typeof options.readWriterIdentity!=='function')throw Error('Current writer identity unavailable; save not replaced.');
      const v=options.readWriterIdentity();
      if(!v||!Number.isInteger(v.world_serial)||v.world_serial<0||v.world_serial>4294967295||![7,8,9,10,11,13,14,15].includes(v.writer_version))throw Error('Current writer identity unavailable; save not replaced.');
      if(v.writer_version===11&&(v.status!=='wind'||v.enabled!==false||v.root_physiology!==1||v.wind_law!==1||v.ground_thermal_law!==0||v.protective_law!==0))throw Error('Invalid standalone Wind writer identity.');
      if((v.writer_version===14||v.writer_version===15)&&(v.status!=='combined'||v.enabled!==true||v.root_physiology!==3||v.wind_law!==1||v.ground_thermal_law!==1))throw Error('Invalid calmer-world writer identity; save not replaced.');
      if(v.writer_version===15&&v.protective_law!==1)throw Error('Invalid protective writer identity; save not replaced.');
      if(v.writer_version!==15&&v.protective_law!==undefined&&v.protective_law!==0)throw Error('Historical writer has incompatible protective law.');
      if(v.writer_version===13&&v.ground_thermal_law!==undefined&&v.ground_thermal_law!==0)throw Error('Historical combined writer has incompatible thermal law.');
      return {world_serial:v.world_serial,writer_version:v.writer_version};
    }
    function checkWriter(expected){const now=writerIdentity();if(now.world_serial!==expected.world_serial||now.writer_version!==expected.writer_version)throw Error('World or save law changed during preparation; save not replaced.');}
    function equalBytes(a,b){if(a.length!==b.length)return false;for(let i=0;i<a.length;i++)if(a[i]!==b[i])return false;return true;}
    async function preserveBeforeCombined(expected,before){
      let path='/wetlands-saves/world.pre-v13.json';
      if(!module.FS.analyzePath(worldPath).exists){combinedBackup={status:'not-needed',durable:false};return;}
      const version=savedVersion();
      if(unsupportedPreview(version))throw Error(unsupportedPreview(version));
      if(version===expected.writer_version){combinedBackup={status:'not-needed',durable:false};return;}
      if(!Number.isSafeInteger(version)||version<1||!(version<=11||[13,14,15].includes(version)))throw Error('Previous save version is unknown or incompatible; refusing to replace it.');
      const prior=before.bytes;
      if(version===14||version===15){let old;try{old=JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(prior));}catch(_){throw Error('Malformed saved law envelope; refusing replacement.');}if(old?.ground_thermal?.law!==1||old?.wind_dispersal?.enabled!==true||old?.wind_dispersal?.law!==1||old?.beta_origin?.config?.physiology_law!==3)throw Error('Invalid saved law identity; refusing replacement.');if(version===15&&(old.protective_strategy?.law!==1||old.protective_strategy?.mutation_law!==1||!Number.isInteger(old.protective_strategy?.stream_seed)||old.protective_strategy.stream_seed<0||old.protective_strategy.stream_seed>18446744073709551615))throw Error('Invalid version15 protective law identity; refusing replacement.');if(version===14&&old.protective_strategy!=null)throw Error('Invalid version14 protective law identity; refusing replacement.');}
      if(expected.writer_version>=14||version>=14||expected.writer_version===11||version===11||(module.FS.analyzePath(path).exists&&!equalBytes(prior,module.FS.readFile(path,{encoding:'binary'})))){
        if(!globalThis.crypto||!globalThis.crypto.subtle)throw Error('Secure backup hashing unavailable; previous save not replaced.');
        const hash=new Uint8Array(await globalThis.crypto.subtle.digest('SHA-256',prior));
        if(hash.length!==32)throw Error('Invalid backup hash; previous save not replaced.');
        checkWriter(expected);
        if(!module.FS.analyzePath(worldPath).exists||!equalBytes(prior,module.FS.readFile(worldPath,{encoding:'binary'})))throw Error('Saved bytes changed during hashing; refusing to serialize.');
        path='/wetlands-saves/'+(expected.writer_version>=14||version>=14||expected.writer_version===11||version===11?'world.recovery.sha256-':'world.pre-v13.sha256-')+Array.from(hash,v=>v.toString(16).padStart(2,'0')).join('')+'.json';
      }
      if(module.FS.analyzePath(path).exists){
        if(!equalBytes(prior,module.FS.readFile(path,{encoding:'binary'})))throw Error('Backup hash path contains different bytes; refusing to replace either file.');
        combinedBackup={status:'present',durable:false,path};
      }else{
        const temp=path+'.tmp';module.FS.writeFile(temp,prior);if(!equalBytes(prior,module.FS.readFile(temp,{encoding:'binary'})))throw Error('Backup write verification failed; previous save not replaced.');module.FS.rename(temp,path);combinedBackup={status:'created',durable:false,path};
      }
      if(!equalBytes(prior,module.FS.readFile(path,{encoding:'binary'})))throw Error('Backup readback verification failed; previous save not replaced.');
      // Always resync a matching backup: a previous failure may leave only RAM bytes.
      await sync(false);
      if(!equalBytes(prior,module.FS.readFile(path,{encoding:'binary'})))throw Error('Backup changed during sync; previous save not replaced.');
      combinedBackup.durable=true;
      checkWriter(expected);
      if(!module.FS.analyzePath(worldPath).exists||!equalBytes(prior,module.FS.readFile(worldPath,{encoding:'binary'})))throw Error('Saved bytes changed during backup; refusing to serialize.');
    }
    async function initialize(){
      try{if(!module.FS.analyzePath('/wetlands-saves').exists)module.FS.mkdir('/wetlands-saves');module.FS.mount(module.IDBFS,{},'/wetlands-saves');await sync(true);available=true;return true;}
      catch(error){feedback('Browser storage unavailable. You can play, but saves will not persist here.',true);return false;}
    }
    async function save(){
      if(busy)return false;if(!available){feedback('Save unavailable: browser storage did not open.',true);return false;}
      busy=true;module.storageOperation=true;feedback('Saving to this browser…');
      try{
        const identity=writerIdentity();
        const beforeCombined={exists:module.FS.analyzePath(worldPath).exists,bytes:module.FS.analyzePath(worldPath).exists?module.FS.readFile(worldPath,{encoding:'binary'}):null};
        if([11,13,14,15].includes(identity.writer_version)||(beforeCombined.exists&&[11,15].includes(versionFromBytes(beforeCombined.bytes))))await preserveBeforeCombined(identity,beforeCombined);
        if(preserveLegacy)await preserveLegacySave();
        checkWriter(identity);
        if(beforeCombined&&(module.FS.analyzePath(worldPath).exists!==beforeCombined.exists||(beforeCombined.exists&&!equalBytes(beforeCombined.bytes,module.FS.readFile(worldPath,{encoding:'binary'})))))throw Error('Saved bytes changed during preparation; refusing to serialize.');
        const code=module._stella_save_expected(identity.world_serial,identity.writer_version);if(code!==0)throw Error(code===-1?'Create or load a planet first.':code===-6?'World or save law changed; previous save not replaced.':code===-5?'This world exceeds the 128 MiB save limit. Your previous save was not replaced. Current progress is still only in memory.':'The game could not serialize this world.');
        await sync(false);
        lastSaveError=null;
        feedback('Saved in this browser. Clearing site data removes this save.'+(backup.durable||combinedBackup.durable?' Use World → Recovery backups to download or restore a verified checkpoint.':''));
        return true;
      }
      catch(error){combinedBackup.durable=false;lastSaveError=error.message;feedback('Save failed: '+lastSaveError,true);return false;}
      finally{busy=false;module.storageOperation=false;}
    }
    const recoveryMaxBytes=128*1024*1024;
    function backupName(name){
      return typeof name==='string'&&(/^(world\.pre-v(?:7|13)\.json)$/.test(name)||/^world\.pre-v13\.sha256-[0-9a-f]{64}\.json$/.test(name)||/^world\.recovery\.sha256-[0-9a-f]{64}\.json$/.test(name));
    }
    async function verifiedBackup(name,expectedHash,allowCurrent=false){
      if(!backupName(name)&&!(allowCurrent&&name==='world.recovery-current.json'))throw Error('Unknown backup name; no file opened.');
      const path='/wetlands-saves/'+name,stat=module.FS.stat(path);
      if(!module.FS.isFile(stat.mode)||!Number.isSafeInteger(stat.size)||stat.size<1||stat.size>recoveryMaxBytes)throw Error('Backup is not a regular save file within the 128 MiB limit.');
      const bytes=new Uint8Array(module.FS.readFile(path,{encoding:'binary'}));
      if(bytes.length!==stat.size)throw Error('Backup changed while reading.');
      if(!globalThis.crypto?.subtle)throw Error('Secure backup hashing unavailable.');
      const digest=new Uint8Array(await globalThis.crypto.subtle.digest('SHA-256',bytes));
      if(digest.length!==32)throw Error('Invalid backup digest.');
      const sha256=Array.from(digest,v=>v.toString(16).padStart(2,'0')).join('');
      const embedded=/sha256-([0-9a-f]{64})\.json$/.exec(name);
      if((embedded&&embedded[1]!==sha256)||(expectedHash!==undefined&&expectedHash!==sha256))throw Error('Backup hash mismatch; no recovery or export performed.');
      if(!equalBytes(bytes,module.FS.readFile(path,{encoding:'binary'})))throw Error('Backup changed during verification.');
      let value;try{value=JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(bytes));}catch(_){throw Error('Backup is not valid JSON.');}
      const version=value&&value.version;
      if(!value||Array.isArray(value)||!Number.isSafeInteger(version)||!((version>=1&&version<=10)||version===11||version===13||version===14||version===15))throw Error(unsupportedPreview(version)||'Unknown backup save version.');
      return {name,version,size:bytes.length,sha256,bytes};
    }
    async function listBackups(){
      if(!available||busy)throw Error('Storage unavailable or busy.');
      busy=true;module.storageOperation=true;
      try{
        const names=module.FS.readdir('/wetlands-saves').filter(backupName).sort();
        if(names.length>512)throw Error('Too many backups to list safely.');
        const rows=[];
        for(const name of names){try{const {bytes,...row}=await verifiedBackup(name);rows.push({...row,valid:true});}catch(error){rows.push({name,valid:false,error:error.message});}}
        return rows;
      }finally{busy=false;module.storageOperation=false;}
    }
    async function exportBackup(name,expectedHash){
      if(!available||busy)throw Error('Storage unavailable or busy.');
      if(typeof expectedHash!=='string'||! /^[0-9a-f]{64}$/.test(expectedHash))throw Error('Select a verified backup first.');
      busy=true;module.storageOperation=true;
      try{return await verifiedBackup(name,expectedHash);}finally{busy=false;module.storageOperation=false;}
    }
    async function restoreVerifiedBackup(name,expectedHash,externalCheck,owned=false,assertActive=()=>{}){
      if(!available||(busy&&!owned)){lastRecoveryError='Recovery unavailable: storage is busy or unavailable.';feedback(lastRecoveryError,true);return false;}
      lastRecoveryError=null;
      if(lastSaveError){lastRecoveryError='Recovery blocked after an unsuccessful Save: browser memory may contain an unsynced saved slot. Complete a successful Save first, or reload this page before restoring. Reloading loses unsaved active progress.';feedback(lastRecoveryError,true);return false;}
      busy=true;module.storageOperation=true;let token=0,applied=false,applyInvoked=false;
      try{
        if(typeof expectedHash!=='string'||!/^[0-9a-f]{64}$/.test(expectedHash))throw Error('Select a verified backup first.');
        if(typeof module.ccall!=='function')throw Error('Guarded recovery unavailable.');
        const identity=writerIdentity();
        await verifiedBackup(name,expectedHash);assertActive();checkWriter(identity);
        const reply=JSON.parse(module.ccall('stella_recovery_prepare','string',['number','number'],[identity.world_serial,identity.writer_version]));
        if(Number.isInteger(reply?.token)&&reply.token>0&&reply.token<=4294967295)token=reply.token;
        if(reply?.status!=='ready')throw Error(reply?.status==='pause_required'?'Pause the world before restoring a backup.':'Recovery preparation refused ('+String(reply?.status||'invalid reply')+').');
        if(!token||reply.world_serial!==identity.world_serial||reply.writer_version!==identity.writer_version||!Number.isSafeInteger(reply.bytes)||reply.bytes<1||reply.bytes>recoveryMaxBytes||typeof reply.sha256!=='string'||!/^[0-9a-f]{64}$/.test(reply.sha256))throw Error('Invalid recovery preparation receipt.');
        const current=await verifiedBackup('world.recovery-current.json',reply.sha256,true);assertActive();
        if(current.size!==reply.bytes||current.version!==identity.writer_version)throw Error('Current recovery checkpoint does not match its receipt.');
        checkWriter(identity);
        const checkpoint='world.recovery.sha256-'+reply.sha256+'.json',path='/wetlands-saves/'+checkpoint;
        if(module.FS.analyzePath(path).exists){await verifiedBackup(checkpoint,reply.sha256);assertActive();}
        else{
          const tmp=path+'.tmp';module.FS.writeFile(tmp,current.bytes);
          if(!equalBytes(current.bytes,module.FS.readFile(tmp,{encoding:'binary'})))throw Error('Recovery checkpoint write verification failed.');
          module.FS.rename(tmp,path);
        }
        await verifiedBackup(checkpoint,reply.sha256);assertActive();
        await sync(false);assertActive();
        await verifiedBackup(checkpoint,reply.sha256);assertActive();
        await verifiedBackup(name,expectedHash);if(externalCheck)await externalCheck();assertActive();checkWriter(identity);
        const kind=name==='world.pre-v7.json'?0:name==='world.pre-v13.json'?1:name.startsWith('world.pre-v13.sha256-')?2:3;
        applyInvoked=true;
        const code=module.ccall('stella_recovery_apply','number',['number','number','string'],[token,kind,expectedHash]);
        if(Number.isInteger(code)&&code>=-5&&code<=0)applyInvoked=false;
        if(code!==0)throw Error(({[-1]:'Recovery unavailable or busy.',[-2]:'The current world changed; recovery refused.',[-3]:'Selected backup is invalid or changed.',[-4]:'Current recovery checkpoint is missing or corrupt.',[-5]:'The native loader could not apply this backup.'})[code]||'Unexpected recovery response; inspect the current world before retrying.');
        applied=true;feedback('Backup restored in memory. Your previous world is preserved as a recovery backup. Browser save is unchanged; choose Save to keep this restored world.');return true;
      }catch(error){lastRecoveryError='Recovery failed: '+error.message+((applied||applyInvoked)?' Outcome uncertain; inspect the current world before retrying.':' No automatic save was performed.');feedback(lastRecoveryError,true);return false;}
      finally{if(token)try{module.ccall('stella_recovery_cancel','number',['number'],[token]);}catch(_){}if(!owned){busy=false;module.storageOperation=false;}}
    }
    async function restoreBackup(name,hash){return restoreVerifiedBackup(name,hash);}
    async function worldBytes(source,name){
      if(source==='current'){
        if(name!=='world.json'&&!backupName(name))throw Error('Invalid current save name.');
        const path='/wetlands-saves/'+name,stat=module.FS.stat(path);
        if(!module.FS.isFile(stat.mode)||stat.size<1||stat.size>recoveryMaxBytes)throw Error('Current file exceeds save limits.');
        return new Uint8Array(module.FS.readFile(path,{encoding:'binary'}));
      }
      const b=await readLegacy(source,name);if(!b)throw Error('Historical save is missing.');return b;
    }
    async function verifiedWorld(source,name,expectedHash){
      const bytes=await worldBytes(source,name);
      const raw=new Uint8Array(await globalThis.crypto.subtle.digest('SHA-256',bytes));
      if(raw.length!==32)throw Error('Invalid save digest.');
      const sha256=Array.from(raw,x=>x.toString(16).padStart(2,'0')).join('');
      const embedded=/sha256-([0-9a-f]{64})\.json$/.exec(name);
      if((expectedHash!==undefined&&expectedHash!==sha256)||(embedded&&embedded[1]!==sha256))throw Error('Selected save changed or its hash is invalid.');
      let value;try{value=JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(bytes));}catch(_){throw Error('Save is not valid JSON.');}
      const version=value?.version;if(!Number.isInteger(version)||!((version>=1&&version<=11)||[13,14,15].includes(version)))throw Error('Unsupported save version; research version12 is not imported.');
      return{source,name,version,size:bytes.length,sha256,bytes};
    }
    async function listWorlds(source){
      if(!available||busy)throw Error('Storage unavailable or busy.');busy=true;module.storageOperation=true;
      try{const names=source==='current'?module.FS.readdir('/wetlands-saves').filter(n=>n==='world.json'||backupName(n)):await readLegacy(source);
        if(names.length>512)throw Error('Too many saves to list.');const rows=[];
        for(const name of names.sort()){try{const {bytes,...row}=await verifiedWorld(source,name);rows.push({...row,valid:true});}catch(e){rows.push({source,name,valid:false,error:e.message});}}return rows;
      }finally{busy=false;module.storageOperation=false;}
    }
    async function exportWorld(source,name,hash){
      if(!available||busy)throw Error('Storage unavailable or busy.');if(!/^[0-9a-f]{64}$/.test(hash||''))throw Error('Select a verified save first.');busy=true;module.storageOperation=true;
      try{return await verifiedWorld(source,name,hash);}finally{busy=false;module.storageOperation=false;}
    }
    let importEpoch=0;
    function cancelImport(){importEpoch++;}
    async function importWorld(source,name,hash){
      if(!available||busy||lastSaveError){lastRecoveryError='Import unavailable. Finish a successful Save first if the previous Save failed; reloading loses unsaved active progress.';feedback(lastRecoveryError,true);return false;}
      busy=true;module.storageOperation=true;const epoch=++importEpoch;
      const active=()=>{if(epoch!==importEpoch||globalThis.document?.hidden)throw Error('Import cancelled before apply.');};
      try{active();if(!/^[0-9a-f]{64}$/.test(hash||''))throw Error('Select a verified save first.');const identity=writerIdentity(),selected=await verifiedWorld(source,name,hash);active();checkWriter(identity);
        const target='world.recovery.sha256-'+hash+'.json',path='/wetlands-saves/'+target;
        if(module.FS.analyzePath(path).exists){await verifiedBackup(target,hash);}else{const tmp=path+'.tmp';module.FS.writeFile(tmp,selected.bytes);if(!equalBytes(selected.bytes,module.FS.readFile(tmp,{encoding:'binary'})))throw Error('Import copy readback failed.');module.FS.rename(tmp,path);await verifiedBackup(target,hash);}
        active();
        return await restoreVerifiedBackup(target,hash,async()=>{await verifiedWorld(source,name,hash);active();checkWriter(identity);},true,active);
      }catch(e){lastRecoveryError='Import failed: '+e.message;feedback(lastRecoveryError,true);return false;}finally{busy=false;module.storageOperation=false;}
    }
    async function load(){
      if(lastSaveError){feedback('Load blocked after unsuccessful Save. Finish a successful Save or reload the page; reload loses unsaved active progress.',true);return false;}
      if(busy)return false;if(!available){feedback('Load unavailable: browser storage did not open.',true);return false;}
      busy=true;module.storageOperation=true;feedback('Loading your browser save…');
      try{await sync(true);if(preserveLegacy)backup.durable=false;if(module.FS.analyzePath(worldPath).exists){const reason=unsupportedPreview(savedVersion());if(reason)throw Error(reason);}const code=module._stella_load();if(code!==0)throw Error(code===-1?'No saved planet in this browser yet.':code===-2?'Saved data is invalid or from an incompatible version.':'The game is not ready to load.');feedback('Loaded your saved planet.');return true;}
      catch(error){feedback('Load failed: '+error.message,true);return false;}
      finally{busy=false;module.storageOperation=false;}
    }
    return{initialize,save,load,listBackups,exportBackup,restoreBackup,listWorlds,exportWorld,importWorld,cancelImport,state:()=>({available,busy,lastSaveError,lastRecoveryError,backup:{...backup},combinedBackup:{...combinedBackup}})};
  }
  if(typeof module!=='undefined'&&module.exports)module.exports={createStorage};else root.createStellaStorage=createStorage;
})(typeof window==='undefined'?globalThis:window);
