// ISOLATED wind integration candidate; production storage remains unchanged.
(function(root){
  function createStorage(module,feedback,options={}){
    let available=false,busy=false,lastSaveError=null;
    let windBackup={status:'not-checked',durable:false};
    const windPolicy=typeof options.readWriterIdentity==='function';
    // The boundary describes the saved bytes to protect, not the running schema.
    // v20 still writes v6 but changes climate; it explicitly opts into this backup.
    const preserveLegacy=options.preserveLegacyThroughVersion===6||options.targetSchemaVersion===7;
    const worldPath='/saves/world.json',backupPath='/saves/world.pre-v7.json',backupTemp='/saves/world.pre-v7.tmp';
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
          module.FS.rename(backupTemp,backupPath);
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
      const v=options.readWriterIdentity();
      if(!v||!Number.isInteger(v.world_serial)||v.world_serial<0||v.world_serial>4294967295||![7,11].includes(v.writer_version))throw Error('Current writer identity unavailable; save not replaced.');
      return {world_serial:v.world_serial,writer_version:v.writer_version};
    }
    function checkWriter(expected){const now=writerIdentity();if(now.world_serial!==expected.world_serial||now.writer_version!==expected.writer_version)throw Error('World or save law changed during preparation; save not replaced.');}
    function equalBytes(a,b){if(a.length!==b.length)return false;for(let i=0;i<a.length;i++)if(a[i]!==b[i])return false;return true;}
    async function preserveBeforeWind(expected,before){
      if(expected.writer_version!==11)return;
      let path='/saves/world.pre-v11.json';
      if(!module.FS.analyzePath(worldPath).exists){windBackup={status:'not-needed',durable:false};return;}
      const version=savedVersion();
      if(version===11){windBackup={status:'not-needed',durable:false};return;}
      if(!Number.isSafeInteger(version)||version<1||version>7)throw Error('Previous save version is unknown or incompatible; refusing to replace it.');
      const prior=before.bytes;
      if(module.FS.analyzePath(path).exists&&!equalBytes(prior,module.FS.readFile(path,{encoding:'binary'}))){
        if(!globalThis.crypto||!globalThis.crypto.subtle)throw Error('Secure backup hashing unavailable; previous save not replaced.');
        const hash=new Uint8Array(await globalThis.crypto.subtle.digest('SHA-256',prior));
        if(hash.length!==32)throw Error('Invalid backup hash; previous save not replaced.');
        checkWriter(expected);
        if(!module.FS.analyzePath(worldPath).exists||!equalBytes(prior,module.FS.readFile(worldPath,{encoding:'binary'})))throw Error('Saved bytes changed during hashing; refusing to serialize.');
        path='/saves/world.pre-v11.sha256-'+Array.from(hash,v=>v.toString(16).padStart(2,'0')).join('')+'.json';
      }
      if(module.FS.analyzePath(path).exists){
        if(!equalBytes(prior,module.FS.readFile(path,{encoding:'binary'})))throw Error('Backup hash path contains different bytes; refusing to replace either file.');
        windBackup={status:'present',durable:false,path};
      }else{
        const temp=path+'.tmp';module.FS.writeFile(temp,prior);module.FS.rename(temp,path);windBackup={status:'created',durable:false,path};
      }
      // Always resync a matching backup: a previous failure may leave only RAM bytes.
      await sync(false);windBackup.durable=true;
      checkWriter(expected);
      if(!module.FS.analyzePath(worldPath).exists||!equalBytes(prior,module.FS.readFile(worldPath,{encoding:'binary'})))throw Error('Saved bytes changed during backup; refusing to serialize.');
    }
    async function initialize(){
      try{if(!module.FS.analyzePath('/saves').exists)module.FS.mkdir('/saves');module.FS.mount(module.IDBFS,{},'/saves');await sync(true);available=true;return true;}
      catch(error){feedback('Browser storage unavailable. You can play, but saves will not persist here.',true);return false;}
    }
    async function save(){
      lastSaveError=null;
      if(busy)return false;if(!available){feedback('Save unavailable: browser storage did not open.',true);return false;}
      busy=true;module.storageOperation=true;feedback('Saving to this browser…');
      try{
        const identity=windPolicy?writerIdentity():null;
        const beforeWind=windPolicy&&identity.writer_version===11?{exists:module.FS.analyzePath(worldPath).exists,bytes:module.FS.analyzePath(worldPath).exists?module.FS.readFile(worldPath,{encoding:'binary'}):null}:null;
        if(windPolicy)await preserveBeforeWind(identity,beforeWind);
        if(preserveLegacy)await preserveLegacySave();
        if(windPolicy)checkWriter(identity);
        if(beforeWind&&(module.FS.analyzePath(worldPath).exists!==beforeWind.exists||(beforeWind.exists&&!equalBytes(beforeWind.bytes,module.FS.readFile(worldPath,{encoding:'binary'})))))throw Error('Saved bytes changed during preparation; refusing to serialize.');
        const code=windPolicy?module._stella_save_expected(identity.world_serial,identity.writer_version):module._stella_save();if(code!==0)throw Error(code===-1?'Create or load a planet first.':code===-6?'World or save law changed; previous save not replaced.':code===-5?'This world exceeds the 128 MiB save limit. Your previous save was not replaced. Current progress is still only in memory.':'The game could not serialize this world.');
        await sync(false);
        feedback('Saved in this browser. Clearing site data removes this save.'+(backup.durable||windBackup.durable?' Your pre-upgrade backup is also kept in this browser; automatic restore is not available.':''));
        return true;
      }
      catch(error){lastSaveError=error.message;feedback('Save failed: '+lastSaveError,true);return false;}
      finally{busy=false;module.storageOperation=false;}
    }
    async function load(){
      if(busy)return false;if(!available){feedback('Load unavailable: browser storage did not open.',true);return false;}
      busy=true;module.storageOperation=true;feedback('Loading your browser save…');
      try{await sync(true);if(preserveLegacy)backup.durable=false;const code=module._stella_load();if(code!==0)throw Error(code===-1?'No saved planet in this browser yet.':code===-2?'Saved data is invalid or from an incompatible version.':'The game is not ready to load.');feedback('Loaded your saved planet.');return true;}
      catch(error){feedback('Load failed: '+error.message,true);return false;}
      finally{busy=false;module.storageOperation=false;}
    }
    return{initialize,save,load,state:()=>({available,busy,lastSaveError,backup:{...backup},windBackup:{...windBackup}})};
  }
  if(typeof module!=='undefined'&&module.exports)module.exports={createStorage};else root.createStellaStorage=createStorage;
})(typeof window==='undefined'?globalThis:window);
