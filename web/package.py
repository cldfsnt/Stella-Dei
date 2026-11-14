"""Split original preload bytes into static-host-safe files, preserving contents."""
from pathlib import Path
p=Path('web/dist'); data=(p/'index.data').read_bytes(); chunk=16*1024*1024
parts=[]
for i,off in enumerate(range(0,len(data),chunk)):
 name=f'assets-{i}.bin'; (p/name).write_bytes(data[off:off+chunk]);parts.append(name)
js=(p/'index.js').read_text()
needle='function fetchRemotePackage(packageName,packageSize,callback,errback){'
replacement=needle+'''Promise.all(PARTS.map(name=>fetch(new URL(name,location.href)).then(r=>{if(!r.ok)throw Error('Asset download failed');return r.arrayBuffer()}))).then(parts=>{const result=new Uint8Array(packageSize);let offset=0;for(const part of parts){result.set(new Uint8Array(part),offset);offset+=part.byteLength;}callback(result.buffer)}).catch(errback);return;'''.replace('PARTS',str(parts))
assert needle in js
(p/'index.js').write_text(js.replace(needle,replacement,1));(p/'index.data').unlink()
