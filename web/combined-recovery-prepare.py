from pathlib import Path
import shutil,sys
r=Path(__file__).resolve().parent;o=Path(sys.argv[1]).resolve();assert o.name=='web' and o.parent.name=='root-wind-recovery'
p=o/'shell.html';s=p.read_text();assert 'recovery-refresh'not in s
s=s.replace('<script src="combined-world.js"></script>','<script src="combined-recovery.js"></script><script src="combined-world.js"></script>',1)
a='<h3>World</h3>';assert s.count(a)==1
s=s.replace(a,a+'''<details id="backup-recovery"><summary>Recovery backups</summary><p>Pause the world before restoring. Backups stay in this browser. Download a copy for safekeeping. Restore replaces only the open world after preserving it in a verified recovery checkpoint; the normal saved slot stays unchanged until you choose Save.</p><button id="recovery-refresh">Find saved backups</button><label for="recovery-backup">Verified backup</label><select id="recovery-backup"><option value="">Find backups first</option></select><button id="recovery-download" disabled>Download selected backup</button><button id="recovery-restore" disabled>Restore selected backup…</button><p id="recovery-status" role="status" aria-live="polite"></p></details>''',1)
a="const combinedUI=StellaCombined.mount(document,{";assert s.count(a)==1
s=s.replace(a,'''const recoveryUI=StellaRecovery.mount(document,{
 storage,available:()=>Module.started&&!Module.failed&&!document.hidden&&!storage.state().busy&&!advanceDay.isLocked(),confirm:message=>window.confirm(message),message:feedback,
 changed:()=>{syncWorldMode();refreshStarter();},download:(bytes,name)=>{const blob=new Blob([bytes],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),30000);}
});
'''+a,1)
s=s.replace('No cloud backup or restore button yet.','No cloud backup. Use Recovery backups in this panel to download or restore verified local checkpoints.')
s=s.replace('</style><script src="combined-recovery.js">','''#recovery-backup{min-height:44px;font:inherit;width:100%;max-width:100%;min-width:0;box-sizing:border-box;background:#102c30;color:#f4fff8}#backup-recovery{position:static;bottom:auto;max-width:100%;overflow-wrap:anywhere}#backup-recovery:not([open]){display:block}</style><script src="combined-recovery.js">''',1)
s=s.replace('<p id="release-label">Build v54 · paused day advance and exact climate-work reuse</p>','<p id="release-label">Wetlands · optional roots + wind</p>')
p.write_text(s)
for n in ['combined-recovery.js','combined-recovery-storage.js']:shutil.copy2(r/n,o/n)
shutil.copy2(r/'combined-recovery-storage.js',o/'stella-storage.js')
p=o/'build.sh';s=p.read_text();s=s.replace('-sEXPORTED_FUNCTIONS=','-sEXPORTED_FUNCTIONS=_stella_recovery_prepare,_stella_recovery_apply,_stella_recovery_cancel,',1);s+='\ncp web/combined-recovery.js web/dist/combined-recovery.js\n';p.write_text(s)
p=o/'tests/shell.test.cjs';s=p.read_text();s=s.replace('const sandbox={',"const sandbox={StellaRecovery:require('../combined-recovery.js'),",1);p.write_text(s)
shutil.copy2(r/'tests/combined-recovery.test.cjs',o/'tests/combined-recovery.test.cjs')
