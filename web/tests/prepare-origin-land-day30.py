#!/usr/bin/env python3
from pathlib import Path
import shutil,hashlib,json
r=Path(__file__).resolve().parents[2];base=r.parent/'site-tmp/origin-land-day30';o=base/'src';source=r.parent/'site-tmp/origin-land-journey/src';assert not o.exists();shutil.copytree(source,o)
p=o/'main.zig';s=p.read_text();a=s.index('    if(std.mem.eql(u8,mode,"preview"))');b=s.index('    const resumed=',a);s=s[:a]+s[b:];s=s.replace('const P=@import("simulation/planet.zig").Planet;','');s=s.replace('orelse "preview"','orelse "main"');old=str(source.parent);new=str(base)
s=s.replace(old,new).replace('"'+new+'/day-3.json"else "'+new+'/day-0.json"','"'+new+'/day-14.json"else "'+old+'/day-7.json"')
s=s.replace('if(resumed)180 else 0','if(resumed)840 else 420').replace('for(start..420)','for(start..1800)').replace('420-start','1800-start')
needle='    Audit.enabled=true;';s=s.replace(needle,'''    if(std.mem.eql(u8,mode,"verify")){std.debug.print("POSITIVE_CHECKPOINT full_reload_exact=true\\n",.{});std.process.exit(0);}
    var positive_saved=false;var max_tick_ns:u64=0;var peak_living:usize=0;const initial_log_bytes=@as(u64,0);_=initial_log_bytes;
'''+needle,1)
s=s.replace('const input=if(resumed)', 'const input=if(std.mem.eql(u8,mode,"verify"))"'+new+'/first-positive.json"else if(resumed)')
s=s.replace('      Audit.tick=tick+1;', '      const tick_start=std.time.nanoTimestamp();Audit.tick=tick+1;')
s=s.replace('      std.debug.print("TICK', '      max_tick_ns=@max(max_tick_ns,@as(u64,@intCast(std.time.nanoTimestamp()-tick_start)));peak_living=@max(peak_living,living);\n      std.debug.print("TICK',1)
s=s.replace('      if((tick+1)%60==0){','''      if(!resumed and !positive_saved and roots>0){var checkpoint_arena=std.heap.ArenaAllocator.init(allocator);const ca=checkpoint_arena.allocator();const checkpoint=try std.json.stringifyAlloc(ca,try saves.capture(ca,state),.{});try std.fs.cwd().writeFile(.{.sub_path="'''+new+'''/first-positive.json",.data=checkpoint});checkpoint_arena.deinit();positive_saved=true;std.debug.print("FIRST_POSITIVE_CHECKPOINT tick={}\\n",.{tick+1});}
      if((tick+1)==840 or (tick+1)==1260 or (tick+1)==1800){''')
s=s.replace('      if(timer.read()>900*std.time.ns_per_s)', '''      const log_path=if(resumed)"'''+new+'''/resume.log"else "'''+new+'''/main.log";const log_stat=try std.fs.cwd().statFile(log_path);if(log_stat.size>512*1024*1024)return error.FixedLogBudget;
      if(timer.read()>900*std.time.ns_per_s)''')
s=s.replace('    std.debug.print("JOURNEY_COMPLETE', '    std.debug.print("COST max_tick_ms={d} peak_living={}\\n",.{@as(f64,@floatFromInt(max_tick_ns))/1e6,peak_living});\n    std.debug.print("JOURNEY_COMPLETE',1)
p.write_text(s)
(base/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},indent=2))
# Exact core hash proof: only the QA main differs from the completed seven-day source.
changes=[str(p.relative_to(o)) for p in o.rglob('*.zig')if p.read_bytes()!=(source/p.relative_to(o)).read_bytes()];assert changes==['main.zig'],changes
(base/'changes.json').write_text(json.dumps(changes))
