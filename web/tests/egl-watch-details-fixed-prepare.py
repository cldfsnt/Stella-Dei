from pathlib import Path
import sys,subprocess,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(r/'web/tests/egl-foraging-production-prepare.py'),str(o)],check=True)
p=o/'main.zig';s=p.read_text();a=s.index('          _=pm;_=pw;');b=s.index('\n        std.debug.print("FORAGING_PRODUCTION_COMPLETE',a);s=s[:a]+(r/'web/tests/watch-details-fixed-qa.txt').read_text().replace('OUTPUT',str(o.parent))+s[b:];p.write_text(s)
(o.parent/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},indent=2))
