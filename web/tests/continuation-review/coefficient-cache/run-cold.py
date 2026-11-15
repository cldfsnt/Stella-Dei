from pathlib import Path
import os,subprocess,json,hashlib,sys
r=Path(sys.argv[1]).resolve()
for kind in ['base','coefficient']:
 e=os.environ.copy();e.pop('STELLA_CPU_LOAD',None);e.update(STELLA_CPU_COLD='1',STELLA_CPU_RESULT_PREFIX=str(r/('cold-'+kind)),STELLA_ORIGIN_COUPLED='1',STELLA_ORIGIN_FAST='1',STELLA_PRODUCER_LONG='1',STELLA_DIAGNOSTIC_DAYS='30',STELLA_FORMS_SINGLE='1',STELLA_ORIGIN_WIDTH='390',STELLA_CPU_LEVEL='6',STELLA_EGL_CAPTURE_PREFIX=str(r/('cold-frame-'+kind)),STELLA_EGL_SAVE_PATH=str(r/('cold-save-'+kind+'.json')))
 with (r/('cold-'+kind+'.log')).open('w') as f:
  p=subprocess.Popen([str(r/('replay-'+kind+'-build/bin/stella-egl'))],env=e,stdout=f,stderr=subprocess.STDOUT);_,status,usage=os.wait4(p.pid,0);p.returncode=os.waitstatus_to_exitcode(status)
 (r/('cold-'+kind+'-rss.json')).write_text(json.dumps({'exit':p.returncode,'max_rss_kib':usage.ru_maxrss,'user_seconds':usage.ru_utime,'system_seconds':usage.ru_stime}))
 print(kind,p.returncode,flush=True)
 if p.returncode:raise SystemExit(p.returncode)
for stage in ['early','established30d']:
 hashes=[hashlib.sha256((r/f'cold-{kind}-{stage}.json').read_bytes()).hexdigest() for kind in ['base','coefficient']]
 print(stage,*hashes,'MATCH' if hashes[0]==hashes[1] else 'FAIL',flush=True)
 assert hashes[0]==hashes[1]
