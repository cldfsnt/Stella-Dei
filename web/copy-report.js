/* Explicit-click clipboard helper. No network, storage or clipboard reads. */
(function(root){
 async function copy({text,clipboard,show}){
  if(typeof text!=='string'||!text.trim()||text.length>12000)return 'unavailable';
  // Keep a manual route available even when clipboard access is restricted.
  show(text);
  if(clipboard&&typeof clipboard.writeText==='function'){
   try{await clipboard.writeText(text);return 'copied';}catch{}
  }
  return 'manual';
 }
 if(typeof module!=='undefined'&&module.exports)module.exports={copy};else root.StellaCopyReport={copy};
})(typeof window==='undefined'?globalThis:window);
