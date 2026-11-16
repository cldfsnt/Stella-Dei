// Isolated combined Wetlands storage. Existing classic/Wind storage remains unchanged.
(function(root){
  function createStorage(module,feedback,options={}){
    let available=false,busy=false,lastSaveError=null;
    let combinedBackup={status:'not-checked',durable:false};
    // The boundary describes the saved bytes to protect, not the running schema.
    // v20 still writes v6 but changes climate; it explicitly opts into this backup.
    const preserveLegacy=options.preserveLegacyThroughVersion===6||options.targetSchemaVersion===7;
    const worldPath='/wetlands-saves/world.json',backupPath='/wetlands-saves/world.pre-v7.json',backupTemp='/wetlands-saves/world.pre-v7.tmp';
    let backup={status:preserveLegacy?'not-checked':'disabled',durable:false,version:null};
    const sync=populate=>new Promise((resolve,reject)=>module.FS.syncfs(populate,error=>error?reject(error):resolve()));
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
      if(version===11)return 'Version 11 is a standalone Wind preview save. Open it in the original Wind preview. The current world is unchanged; the saved file was not replaced.';
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
      if(!v||!Number.isInteger(v.world_serial)||v.world_serial<0||v.world_serial>4294967295||![7,8,9,10,13].includes(v.writer_version))throw Error('Current writer identity unavailable; save not replaced.');
      return {world_serial:v.world_serial,writer_version:v.writer_version};
    }
    function checkWriter(expected){const now=writerIdentity();if(now.world_serial!==expected.world_serial||now.writer_version!==expected.writer_version)throw Error('World or save law changed during preparation; save not replaced.');}
    function equalBytes(a,b){if(a.length!==b.length)return false;for(let i=0;i<a.length;i++)if(a[i]!==b[i])return false;return true;}
    async function preserveBeforeCombined(expected,before){
      if(expected.writer_version!==13)return;
      let path='/wetlands-saves/world.pre-v13.json';
      if(!module.FS.analyzePath(worldPath).exists){combinedBackup={status:'not-needed',durable:false};return;}
      const version=savedVersion();
      if(unsupportedPreview(version))throw Error(unsupportedPreview(version));
      if(version===13){combinedBackup={status:'not-needed',durable:false};return;}
      if(!Number.isSafeInteger(version)||version<1||version>10)throw Error('Previous save version is unknown or incompatible; refusing to replace it.');
      const prior=before.bytes;
      if(module.FS.analyzePath(path).exists&&!equalBytes(prior,module.FS.readFile(path,{encoding:'binary'}))){
        if(!globalThis.crypto||!globalThis.crypto.subtle)throw Error('Secure backup hashing unavailable; previous save not replaced.');
        const hash=new Uint8Array(await globalThis.crypto.subtle.digest('SHA-256',prior));
        if(hash.length!==32)throw Error('Invalid backup hash; previous save not replaced.');
        checkWriter(expected);
        if(!module.FS.analyzePath(worldPath).exists||!equalBytes(prior,module.FS.readFile(worldPath,{encoding:'binary'})))throw Error('Saved bytes changed during hashing; refusing to serialize.');
        path='/wetlands-saves/world.pre-v13.sha256-'+Array.from(hash,v=>v.toString(16).padStart(2,'0')).join('')+'.json';
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
      lastSaveError=null;
      if(busy)return false;if(!available){feedback('Save unavailable: browser storage did not open.',true);return false;}
      busy=true;module.storageOperation=true;feedback('Saving to this browser…');
      try{
        const identity=writerIdentity();
        const beforeCombined={exists:module.FS.analyzePath(worldPath).exists,bytes:module.FS.analyzePath(worldPath).exists?module.FS.readFile(worldPath,{encoding:'binary'}):null};
        if(identity.writer_version===13)await preserveBeforeCombined(identity,beforeCombined);
        if(preserveLegacy)await preserveLegacySave();
        checkWriter(identity);
        if(beforeCombined&&(module.FS.analyzePath(worldPath).exists!==beforeCombined.exists||(beforeCombined.exists&&!equalBytes(beforeCombined.bytes,module.FS.readFile(worldPath,{encoding:'binary'})))))throw Error('Saved bytes changed during preparation; refusing to serialize.');
        const code=module._stella_save_expected(identity.world_serial,identity.writer_version);if(code!==0)throw Error(code===-1?'Create or load a planet first.':code===-6?'World or save law changed; previous save not replaced.':code===-5?'This world exceeds the 128 MiB save limit. Your previous save was not replaced. Current progress is still only in memory.':'The game could not serialize this world.');
        await sync(false);
        feedback('Saved in this browser. Clearing site data removes this save.'+(backup.durable||combinedBackup.durable?' Your pre-upgrade backup is also kept in this browser; automatic restore is not available.':''));
        return true;
      }
      catch(error){combinedBackup.durable=false;lastSaveError=error.message;feedback('Save failed: '+lastSaveError,true);return false;}
      finally{busy=false;module.storageOperation=false;}
    }
    async function load(){
      if(busy)return false;if(!available){feedback('Load unavailable: browser storage did not open.',true);return false;}
      busy=true;module.storageOperation=true;feedback('Loading your browser save…');
      try{await sync(true);if(preserveLegacy)backup.durable=false;if(module.FS.analyzePath(worldPath).exists){const reason=unsupportedPreview(savedVersion());if(reason)throw Error(reason);}const code=module._stella_load();if(code!==0)throw Error(code===-1?'No saved planet in this browser yet.':code===-2?'Saved data is invalid or from an incompatible version.':'The game is not ready to load.');feedback('Loaded your saved planet.');return true;}
      catch(error){feedback('Load failed: '+error.message,true);return false;}
      finally{busy=false;module.storageOperation=false;}
    }
    return{initialize,save,load,state:()=>({available,busy,lastSaveError,backup:{...backup},combinedBackup:{...combinedBackup}})};
  }
  if(typeof module!=='undefined'&&module.exports)module.exports={createStorage};else root.createStellaStorage=createStorage;
})(typeof window==='undefined'?globalThis:window);
