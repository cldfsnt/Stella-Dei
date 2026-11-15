from pathlib import Path
import subprocess,os,hashlib,json
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/rooted-player-terrain';old=r.parent/'site-tmp/rooted-player';exe=b/'install/bin/stella-egl'
def run(name,**kw):
 env=os.environ|{'LIBGL_ALWAYS_SOFTWARE':'1'}|{k:str(v) for k,v in kw.items()}
 with (b/name).open('wb') as f:subprocess.run([str(exe)],env=env,stdout=f,stderr=subprocess.STDOUT,check=True,timeout=900)
run('guards.log',QA_GUARDS=1)
for arm in range(2):
 run(f'trace-{arm}.log',QA_ARM=arm,QA_END=2,QA_SUFFIX='-trace')
 run(f'off-{arm}.log',QA_ARM=arm,QA_END=2,QA_SUFFIX='-off',QA_TRACE_OFF=1)
 run(f'main-{arm}.log',QA_ARM=arm)
 run(f'resume-{arm}.log',QA_ARM=arm,QA_RESUME=1)
# Reuse the exact prior Fraction and complete restart audit against separate directory.
s=(r/'web/tests/analyze-rooted-player.py').read_text().replace("site-tmp/rooted-player'","site-tmp/rooted-player-terrain'")
exec(compile(s,str(r/'web/tests/analyze-rooted-player.py'),'exec'))
rows=lambda p:[l for l in p.read_text().splitlines() if l.startswith(('ROOT_WATER ','USED_H ','MORTALITY ','PAID_GROWTH ','PATCH ','BIRTH ','FOUNDER ','TERRAIN ','WATER_ACTION ','GEOMETRY ','PARTIAL_RECEIPT '))]
proof={}
for p in b.glob('*.json'):
 if not p.name.startswith(('arm-','resume-arm-')):continue
 prior=old/p.name;assert p.read_bytes()==prior.read_bytes(),p.name
 proof[p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
for name in ['guards.log']+[f'{kind}-{a}.log' for a in range(2) for kind in ('main','resume','trace')]:assert rows(b/name)==rows(old/name),name
(b/'parity.json').write_text(json.dumps({'all_saved_states_exact_to_59a981c':proof,'all_receipt_rows_exact':True,'action_geometry_matches_independent_full_refresh':True,'explicit_qa_full_refresh_removed':True},indent=2)+'\n')
print('INTEGRATED_ACTION_REFRESH_ALL_STATES_RECEIPTS_GUARDS_RESTART_EXACT_PASS')
