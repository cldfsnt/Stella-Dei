from pathlib import Path
import subprocess,sys,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(r/'web/tests/egl-foraging-production-prepare.py'),str(o)],check=True)
p=o/'main.zig';s=p.read_text();start=s.index('          _=pm;_=pw;');end=s.index('\n        std.debug.print("FORAGING_PRODUCTION_COMPLETE',start)
s=s[:start]+(r/'web/tests/defense-player14-qa.txt').read_text().replace('OUTPUT',str(o.parent))+s[end:];p.write_text(s)
subprocess.run([sys.executable,str(r/'web/tests/audit-zig-exports.py'),str(r/'src/main.zig'),str(p)],check=True,stdout=(o.parent/'export-audit.json').open('w'))
(o.parent/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},indent=2))
