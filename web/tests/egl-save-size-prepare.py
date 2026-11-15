#!/usr/bin/env python3
"""Actual native save write/read with explicit platform bridge and injected write limit."""
from pathlib import Path
import sys,subprocess,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]);subprocess.run([sys.executable,str(r/'web/tests/egl-habitat-preview-prepare.py'),str(o)],check=True)
p=o/'main.zig';s=p.read_text();start=s.index('          _=first_id;');end=s.index('\n        try originSaveCheck',start)
s=s[:start]+r'''
          _=first_id;
          try saves.apply(state,baseline.value);state.selectedPoint=target;state.paused=true;AdvanceDay.current=.{};
          const original=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          std.debug.assert(stella_save()==0);
          const bytes=try std.fs.cwd().readFileAlloc(a,saves.path,128*1024*1024);std.debug.assert(std.mem.eql(u8,original,bytes));
          const readback=try saves.read(a);std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,readback.value,.{})));
          try std.testing.expectError(error.FileNotFound,std.fs.cwd().access("/workspace/scratch/f67c3ac60ca3/site-tmp/save-size-native/saves/world.tmp",.{}));
          saves.qa_write_limit=bytes.len-1;
          std.debug.assert(stella_save()==-5);
          std.debug.assert(std.mem.eql(u8,bytes,try std.fs.cwd().readFileAlloc(a,saves.path,128*1024*1024)));
          try std.testing.expectError(error.FileNotFound,std.fs.cwd().access("/workspace/scratch/f67c3ac60ca3/site-tmp/save-size-native/saves/world.tmp",.{}));
          std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.assert(AdvanceDay.current.start(state,PerformanceDetails.world_serial,PerformanceDetails.world_serial));AdvanceDay.current.environment(true,false);
          std.debug.assert(stella_save()==-5);
          std.debug.assert(std.mem.eql(u8,bytes,try std.fs.cwd().readFileAlloc(a,saves.path,128*1024*1024)));
          try std.testing.expectError(error.FileNotFound,std.fs.cwd().access("/workspace/scratch/f67c3ac60ca3/site-tmp/save-size-native/saves/world.tmp",.{}));
          saves.qa_write_limit=bytes.len;std.debug.assert(stella_save()==0);
          std.debug.assert(std.mem.eql(u8,bytes,try std.fs.cwd().readFileAlloc(a,saves.path,128*1024*1024)));
          std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          AdvanceDay.current=.{};saves.qa_write_limit=saves.save_io.max_save_bytes;
          std.debug.print("SAVE_SIZE_NATIVE_PASS bytes={d} normal_read_write_exact=true oversized_normal_minus5=true oversized_recovery_minus5=true canonical_preserved=true temp_absent=true model_unchanged=true exact_limit_recovery_success=true\n",.{bytes.len});
        }
''' +s[end:]
# Named stella_save exception only: native platform availability and web-only pump.
a=s.index('export fn stella_save()');b=s.index('\nexport fn stella_load()',a);body=s[a:b];body=body.replace('if (!is_web or !web_initialized) return -1;','// QA native initialized state; original platform gate bypassed.').replace('web_loop.pump(1024);','// QA no web task queue; native simulation already joined.');s=s[:a]+body+s[b:];p.write_text(s)
p=o/'save_game.zig';s=p.read_text().replace('"/saves','"/workspace/scratch/f67c3ac60ca3/site-tmp/save-size-native/saves');s=s.replace('pub const path =','pub var qa_write_limit:usize=save_io.max_save_bytes;\npub const path =');s=s.replace('saved, save_io.max_save_bytes);','saved, qa_write_limit);');p.write_text(s)
subprocess.run([sys.executable,str(r/'web/tests/audit-zig-exports.py'),str(r/'src/main.zig'),str(o/'main.zig'),'--allow','stella_save','--output',str(o.parent/'exports-audit.json')],check=True)
files=['main.zig','save_game.zig','save_io.zig','save_schema.zig'];(o.parent/'provenance.json').write_text(json.dumps({f:{'production':hashlib.sha256((r/'src'/f).read_bytes()).hexdigest(),'copied':hashlib.sha256((o/f).read_bytes()).hexdigest()} for f in files},indent=2)+'\n')
