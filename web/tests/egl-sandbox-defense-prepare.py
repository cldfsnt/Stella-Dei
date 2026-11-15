#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys,shutil,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve();shared=r.parent/'site-tmp/sandbox-defense-integration/src'
subprocess.run([sys.executable,str(r/'web/tests/egl-foraging-production-prepare.py'),str(o)],check=True)
for p in shared.rglob('*'):
 if p.is_file() and p.relative_to(shared)!=Path('main.zig') and (not (r/'src'/p.relative_to(shared)).exists() or p.read_bytes()!=(r/'src'/p.relative_to(shared)).read_bytes()):
  dest=o/p.relative_to(shared);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
p=o/'states/play.zig';s=p.read_text().replace('@import("builtin").target.cpu.arch == .wasm32','true').replace('@import("builtin").target.cpu.arch != .wasm32','false').replace('paused: bool = false','paused: bool = true').replace('var randomPrng = std.rand.DefaultPrng.init(@as(u64, @bitCast(std.time.milliTimestamp())));','var randomPrng = std.rand.DefaultPrng.init(if(std.posix.getenv("STELLA_PRODUCER_SEED")) |seed_text| std.fmt.parseInt(u64,seed_text,10) catch 1337 else 1337);');p.write_text(s)
p=o/'main.zig';s=p.read_text();owner=(shared/'main.zig').read_text();begin=owner.index('var defense_json:');end=owner.index('var advance_json:',begin);s=s.replace('var advance_json:',owner[begin:end]+'var advance_json:',1)
s=s.replace('          if(std.process.getEnvVarOwned(allocator,"QA_PULSE_SAVE")', '''          const untouched_origin_bytes=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const untouched_origin=try std.json.parseFromSlice(saves.schema.Save,a,untouched_origin_bytes,.{.allocate=.alloc_always});
          if(std.process.getEnvVarOwned(allocator,"QA_PULSE_SAVE")''',1)
a=s.index('          _=pm;_=pw;');b=s.index('\n        std.debug.print("FORAGING_PRODUCTION_COMPLETE',a);s=s[:a]+(r/'web/tests/sandbox-defense-native-qa.txt').read_text().replace('OUTPUT',str(o.parent))+s[b:];p.write_text(s)
subprocess.run([sys.executable,str(r/'web/tests/audit-zig-exports.py'),str(shared/'main.zig'),str(p)],check=True,stdout=(o.parent/'export-audit.json').open('w'))
(o.parent/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},indent=2)+'\n')
