#!/usr/bin/env python3
"""Summarize actual paired game runs and reject any final-state difference."""
import hashlib,json,re,statistics,sys
from pathlib import Path
rows=[]
for stem in sys.argv[1:]:
 p=Path(stem); data=p.with_suffix('.json').read_bytes(); log=p.with_suffix('.log').read_text()
 times=[float(x) for x in re.findall(r'update_ms=([0-9.]+)',log)]
 assert len(times)==60,(stem,len(times))
 rows.append(dict(run=p.name,sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),median_ms=statistics.median(times),mean_ms=statistics.mean(times),p95_ms=sorted(times)[56]))
assert len({r['sha256'] for r in rows})==1,'COMPLETE STATE DIFFERS'
print(json.dumps({'exact_state_equal':True,'runs':rows},indent=2))
