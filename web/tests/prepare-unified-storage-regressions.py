"""Adapt copied storage expectations to intentional Wind11 support/dirty-load guard.
No production tests altered; all unrelated assertions remain.
"""
from pathlib import Path
import sys
web=Path(sys.argv[1]).resolve();assert web.name=='web' and web.parent.name=='unified-ui'
base=web.parent.parent/'protective-ui/web/tests'
for name in ['combined-storage.test.cjs','combined-recovery-storage.test.cjs','storage-upgrade.test.cjs','storage.test.cjs']:
 s=(base/name).read_text()
 if name=='combined-storage.test.cjs':
  s=s.replace('save(0),save(11),save(12)','save(0),save(12)')
  s=s.replace('for(const version of [11,12])','for(const version of [12])')
  s=s.replace('standalone11 and research12 load refuse','research12 load refuses').replace('pre13 refusal names standalone11 and research12','pre13 refusal names research12').replace('opaque/unknown and standalone11/12','opaque/unknown and research12')
  s+='''\ntest('unified11 load now delegates native unchanged and before13write preserves exact11 recovery',async()=>{const original=save(11),m=mock({[W]:original});await m.init();assert(await m.finish(m.storage.load()));assert.equal(m.events.filter(e=>e[0]==='load').length,1);assert.deepEqual(m.files.get(W),original);assert(await m.finish(m.storage.save()));assert.deepEqual(m.durable.get('/wetlands-saves/world.recovery.sha256-'+hash(original)+'.json'),original);assert.deepEqual(m.calls,[[42,13]]);});\n'''
 elif name=='combined-recovery-storage.test.cjs':
  s=s.replace("hash(data(11))+'.json']:data(11)","hash(data(12))+'.json']:data(12)")
  s+='''\ntest('unified recovery discovers supported Wind11 unchanged',async()=>{const b=data(11),n='world.recovery.sha256-'+hash(b)+'.json',f=fixture({[n]:b});await f.store.initialize();const [r]=await f.store.listBackups();assert.equal(r.valid,true);assert.equal(r.version,11);assert.deepEqual((await f.store.exportBackup(n,r.sha256)).bytes,b);});\n'''
 elif name=='storage.test.cjs':
  needle=' module._stella_load=()=>-1;let pending=storage.load();'
  repl=" const countBeforeBlockedLoad=syncs.length;assert.equal(await storage.load(),false);assert.equal(syncs.length,countBeforeBlockedLoad);assert.match(feedback.at(-1)[0],/Load blocked/);module._stella_save=()=>0;const retry=storage.save();callback(null);assert.equal(await retry,true);\n"+needle
  assert needle in s;s=s.replace(needle,repl)
 else:
  old='s.loadCode=-2;const pl=s.storage.load();s.complete();assert.equal(await pl,false);assert.equal(s.saves,1);assert.equal(s.loads,1);assert.deepEqual(s.durable.get(W),old);'
  new="assert.equal(await s.storage.load(),false);assert.equal(s.pending.length,0);assert.equal(s.loads,0);assert.equal(s.saves,1);assert.deepEqual(s.durable.get(W),old);\n // A fresh instance (page reload equivalent) still exercises the original invalid native load assertions.\n const l=mock({[W]:old,[B]:old});await l.init();l.loadCode=-2;const pl=l.storage.load();l.complete();assert.equal(await pl,false);assert.equal(l.saves,0);assert.equal(l.loads,1);assert.deepEqual(l.durable.get(W),old);"
  assert old in s;s=s.replace(old,new)
  s=s.replace('const state=s.storage.state();state.backup.durable=true;assert.equal(s.storage.state().backup.durable,false);','const beforeState=s.storage.state().backup.durable;const state=s.storage.state();state.backup.durable=!beforeState;assert.equal(s.storage.state().backup.durable,beforeState);')
 (web/'tests'/name).write_text(s)
