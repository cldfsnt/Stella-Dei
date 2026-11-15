#!/usr/bin/env python3
from pathlib import Path
import sys,re,shutil,hashlib,json
r=Path(__file__).resolve().parents[2];source=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
s=(source/'shell.html').read_text().replace('{{{ SCRIPT }}}','').replace('{{{SCRIPT}}}','')
s=s.replace('</head>','<style>#more-menu{width:358px;max-width:calc(100vw - 16px)}</style></head>')
s=s.replace('<body>','<body><aside style="padding:12px;background:#6d3c00;color:white"><strong>UI MOCK ONLY · 358px panel · no game simulation</strong><div id="fixture-controls"></div></aside>')
for name in re.findall(r'<script src="([^"]+)"',s):
 if(source/name).is_file():shutil.copy2(source/name,out/name)
mock=r/'web/tests/continuation-review/defense-world-stats/mock-native.js';s=s.replace('</body>','<script>'+mock.read_text()+'</script></body>');(out/'index.html').write_text(s)
(r/'web/tests/continuation-review/defense-world-stats/fixture-hashes.json').write_text(json.dumps({'source_shell':hashlib.sha256((source/'shell.html').read_bytes()).hexdigest(),'controller':hashlib.sha256((source/'sandbox-defense.js').read_bytes()).hexdigest(),'stats_controller':hashlib.sha256((source/'world-ecology.js').read_bytes()).hexdigest(),'mock':hashlib.sha256(mock.read_bytes()).hexdigest(),'fixture':hashlib.sha256((out/'index.html').read_bytes()).hexdigest()},indent=2)+'\n')
