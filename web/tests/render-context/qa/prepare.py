#!/usr/bin/env python3
from pathlib import Path
import os,sys,subprocess
root=Path(os.environ['STELLA_SOURCE_ROOT']).resolve();here=Path(__file__).resolve().parent;out=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(root/'web/tests/empty-bloom/qa/prepare.py'),str(out)],check=True)
assert 'renderContext' in (out/'performance_details.zig').read_text(),'Integrate reviewed context patch before current-tree QA'
p=out/'main.zig';s=p.read_text();needle='    if(std.posix.getenv("QA_EMPTY_BLOOM")!=null){';assert needle in s;s=s.replace(needle,(here/'context-qa.zig.part').read_text()+needle);p.write_text(s);print(out/'main.zig')
