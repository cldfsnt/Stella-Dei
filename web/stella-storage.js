(function(root){
  function createStorage(module,feedback){
    let available=false,busy=false;
    const sync=populate=>new Promise((resolve,reject)=>module.FS.syncfs(populate,error=>error?reject(error):resolve()));
    async function initialize(){
      try{if(!module.FS.analyzePath('/saves').exists)module.FS.mkdir('/saves');module.FS.mount(module.IDBFS,{},'/saves');await sync(true);available=true;return true;}
      catch(error){feedback('Browser storage unavailable. You can play, but saves will not persist here.',true);return false;}
    }
    async function save(){
      if(busy)return false;if(!available){feedback('Save unavailable: browser storage did not open.',true);return false;}
      busy=true;module.storageOperation=true;feedback('Saving to this browser…');
      try{const code=module._stella_save();if(code!==0)throw Error(code===-1?'Create or load a planet first.':'The game could not serialize this world.');await sync(false);feedback('Saved in this browser. Clearing site data removes this save.');return true;}
      catch(error){feedback('Save failed: '+error.message,true);return false;}
      finally{busy=false;module.storageOperation=false;}
    }
    async function load(){
      if(busy)return false;if(!available){feedback('Load unavailable: browser storage did not open.',true);return false;}
      busy=true;module.storageOperation=true;feedback('Loading your browser save…');
      try{await sync(true);const code=module._stella_load();if(code!==0)throw Error(code===-1?'No saved planet in this browser yet.':code===-2?'Saved data is invalid or from an incompatible version.':'The game is not ready to load.');feedback('Loaded your saved planet.');return true;}
      catch(error){feedback('Load failed: '+error.message,true);return false;}
      finally{busy=false;module.storageOperation=false;}
    }
    return{initialize,save,load,state:()=>({available,busy})};
  }
  if(typeof module!=='undefined'&&module.exports)module.exports={createStorage};else root.createStellaStorage=createStorage;
})(typeof window==='undefined'?globalThis:window);
