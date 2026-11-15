#!/usr/bin/env python3
"""Actual shell, explicit mocked native API. Never a gameplay fixture."""
from pathlib import Path
import re,sys,shutil
r=Path(__file__).resolve().parents[2];out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
s=(r/'web/shell.html').read_text().replace('{{{ SCRIPT }}}','').replace('{{{SCRIPT}}}','')
s=s.replace('</head>','<style>#habitat-sheet,#life-sheet{width:358px;max-width:calc(100vw - 16px)}</style></head>')
s=s.replace('<body>','<body><aside style="padding:12px;background:#6d3c00;color:white"><strong>UI FIXTURE ONLY · 358px panel · mock engine · no game simulation</strong><div id="fixture-controls"></div></aside>')
for name in re.findall(r'<script src="([^"]+)"',s):
 source=r/'web'/name
 if source.exists():shutil.copy(source,out/name)
mock=(Path(sys.argv[2]) if len(sys.argv)>2 else r/'web/tests/continuation-review/habitat-ui/mock-native.js').read_text();s=s.replace('</body>','<script>'+mock+'</script></body>');(out/'index.html').write_text(s)
