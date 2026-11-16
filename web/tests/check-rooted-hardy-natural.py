from pathlib import Path
import json,subprocess,os,hashlib,sys
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/rooted-hardy-natural';old=r.parent/'site-tmp/rooted-natural'
if '--analyze-only' not in sys.argv:
 for arm,point in enumerate((126,1845)):
  with(b/f'initial-{arm}.log').open('wb')as f:subprocess.run([str(b/'install/bin/stella-egl')],env=os.environ|{'LIBGL_ALWAYS_SOFTWARE':'1','QA_ARM':str(arm),'QA_END':'0'},stdout=f,stderr=subprocess.STDOUT,check=True,timeout=90)
  current=json.load(open(b/f'arm-{arm}-0.json'));prior=json.load(open(old/f'arm-{arm}-0.json'));co=current['origin']['cells'][point]['sparse'][0]['value'];assert co['structure']==.5;co['structure']=0;assert current==prior,('initial-only-structure',arm)
 print('INITIAL_COMPLETE_STATE_ONLY_STRUCTURE_DIFF_PASS')
s=(r/'web/tests/check-rooted-natural.py').read_text().replace("site-tmp/rooted-natural'","site-tmp/rooted-hardy-natural'");exec(compile(s,str(r/'web/tests/check-rooted-natural.py'),'exec'))
a=(r/'web/tests/rooted-natural-attribution.py').read_text().replace("site-tmp/rooted-natural'","site-tmp/rooted-hardy-natural'");exec(compile(a,str(r/'web/tests/rooted-natural-attribution.py'),'exec'))
print('HARDY_FIXED_NATIVE_PAIR_AND_SOURCE_FUNDING_RESTART_PASS')
