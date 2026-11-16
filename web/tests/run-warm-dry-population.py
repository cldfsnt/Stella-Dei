from pathlib import Path
import os,subprocess,json,hashlib,shutil,time
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/warm-dry-population';exe=b/'build/bin/stella-egl';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def run(name,stage='main',candidate=False,off=False):
 assert shutil.disk_usage(b).free>500*1024**2,'Disk headroom gate'
 env={**os.environ,'EGL_PLATFORM':'surfaceless','LIBGL_ALWAYS_SOFTWARE':'1','QA_STAGE':stage}
 if candidate:env['QA_CANDIDATE']='1'
 if off:env['QA_OFF']='1'
 with (b/(name+'.log')).open('w')as f:subprocess.run([str(exe)],cwd=r,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
 print(name,'complete',time.strftime('%FT%TZ',time.gmtime()),flush=True)
run('control')
assert sha(b/'final.json')=='bfb28fe690d5f7fdbd65884a5f65de206764a447e2b9f434235da2fefbbb3ccc','control mismatch'
for n in ['fresh','seeded','day7','day14','final']:shutil.copy2(b/(n+'.json'),b/('control-'+n+'.json'))
run('parity','parity');run('parity-off','parity',off=True)
assert (b/'parity-on.json').read_bytes()==(b/'parity-off.json').read_bytes(),'observer mismatch'
run('candidate',candidate=True)
assert (b/'seeded.json').read_bytes()==(b/'control-seeded.json').read_bytes(),'candidate initial mismatch'
for n in ['fresh','seeded','day7','day14','final']:shutil.copy2(b/(n+'.json'),b/('candidate-'+n+'.json'))
run('candidate-resume','resume',candidate=True)
assert (b/'final.json').read_bytes()==(b/'resumed.json').read_bytes(),'candidate continuation mismatch'
print('ALL_FULL_STATE_GATES_PASS',flush=True)
(b/'state-hashes.json').write_text(json.dumps({p.name:sha(p)for p in b.glob('*.json')if not p.name.endswith('hashes.json')},indent=2)+'\n')
