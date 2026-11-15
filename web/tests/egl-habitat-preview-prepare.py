#!/usr/bin/env python3
"""Actual public confirmation versus frozen existing actions, no elapsed biology."""
from pathlib import Path
import sys,subprocess
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]);subprocess.run([sys.executable,str(r/'web/tests/egl-habitat-engineering-prepare.py'),str(o)],check=True)
p=o/'main.zig';s=p.read_text();start=s.index('          for(0..3)|arm|{');end=s.index('\n        try originSaveCheck',start)
s=s[:start]+r'''
          _=first_id;
          for(0..2)|kind|{
            try saves.apply(state,baseline.value);state.selectedPoint=target;state.paused=true;
            const original=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
            const old=if(kind==0)stella_make_pond(@intCast(target)) else stella_make_nursery(@intCast(target));std.debug.assert(old>0);
            const expected=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
            try saves.apply(state,baseline.value);state.selectedPoint=target;state.paused=true;
            const prepared=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_habitat_prepare(PerformanceDetails.world_serial,@intCast(target),@intCast(kind))),.{.allocate=.alloc_always});
            std.debug.assert(prepared.value.object.get("ok").?.bool);
            std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
            const token:u32=@intCast(prepared.value.object.get("token").?.integer);
            const result=std.mem.span(stella_habitat_execute(token));std.debug.print("HABITAT_PREVIEW_RECEIPT {s}\n",.{result});
            const parsed=try std.json.parseFromSlice(std.json.Value,a,result,.{});std.debug.assert(parsed.value.object.get("ok").?.bool);
            const actual=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});std.debug.assert(std.mem.eql(u8,expected,actual));
            _=stella_habitat_execute(token);std.debug.assert(std.mem.eql(u8,actual,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
            const pending_result=try std.json.parseFromSlice(std.json.Value,a,std.mem.span(stella_habitat_prepare(PerformanceDetails.world_serial,@intCast(target),@intCast(kind))),.{});const pending_token:u32=@intCast(pending_result.value.object.get("token").?.integer);
            try saves.apply(state,baseline.value);state.selectedPoint=target;const restored=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
            _=stella_habitat_execute(pending_token);std.debug.assert(std.mem.eql(u8,restored,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          }
          try saves.apply(state,baseline.value);std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.print("HABITAT_PREVIEW_PASS both_kinds_full_save_exact=true preview_no_mutation=true duplicate_noop=true load_invalidates=true\n",.{});
        }
''' +s[end:];p.write_text(s)
subprocess.run([sys.executable,str(r/'web/tests/audit-zig-exports.py'),str(r/'src/main.zig'),str(p)],check=True)
