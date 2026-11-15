/* Opt-in local diagnostic: invoked only by an explicit gameplay measurement.
   No storage, network, device enumeration or privileged browser APIs. */
(function(root){
 const clean=v=>typeof v==='string'?v.replace(/[\x00-\x1f\x7f]/g,' ').slice(0,256):'';
 function capture(canvas){
  try{
   const gl=canvas&&canvas.getContext('webgl2');
   if(!gl)return {available:false};
   const read=p=>{try{return clean(gl.getParameter(p));}catch{return '';}};
   const data={available:true,vendor:read(gl.VENDOR),renderer:read(gl.RENDERER),version:read(gl.VERSION),width:0,height:0};
   for(const [key,value] of [['width',gl.drawingBufferWidth],['height',gl.drawingBufferHeight]])if(Number.isSafeInteger(value)&&value>0)data[key]=value;
   try{const ext=gl.getExtension('WEBGL_debug_renderer_info');if(ext){data.renderer=read(ext.UNMASKED_RENDERER_WEBGL)||data.renderer;data.vendor=read(ext.UNMASKED_VENDOR_WEBGL)||data.vendor;}}catch{}
   data.software_hint=/llvmpipe|softpipe|swiftshader|microsoft basic render driver|software rasterizer/i.test(data.renderer);
   return data;
  }catch{return {available:false};}
 }
 function text(data){
  if(!data||!data.available)return 'Renderer details unavailable; timing sample remains valid.';
  const lines=['Local renderer at measurement start',data.width&&data.height?'Drawing buffer: '+data.width+' × '+data.height:'Drawing buffer unavailable'];
  if(data.renderer)lines.push('Renderer: '+clean(data.renderer));
  if(data.vendor)lines.push('Vendor: '+clean(data.vendor));
  if(data.version)lines.push('API: '+clean(data.version));
  lines.push(data.software_hint?'Renderer name suggests software rendering; confirm in your browser settings.':'Renderer name alone does not establish hardware acceleration or explain performance.');
  return lines.join('\n');
 }
 const api={capture,text};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.StellaRendererInfo=api;
})(typeof window==='undefined'?globalThis:window);
