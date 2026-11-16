from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];t=r.parent/'site-tmp';old=t/'combined-strategy';b=t/'combined-day21';o=b/'src';b.mkdir(exist_ok=True)
expected=json.loads((old/'source-hashes.json').read_text())
for n,h in expected.items():assert hashlib.sha256((old/'src'/n).read_bytes()).hexdigest()==h,n
shutil.copytree(old/'src',o,dirs_exist_ok=True)
p=o/'main.zig';v=p.read_text();start=v.index('    const saves=@import("save_game.zig");const M=');end=v.index('\nfn qaWindTick',start)
qa=r.joinpath('web/tests/combined-day21-qa.txt').read_text().replace('INPUT',str(old)).replace('OUTPUT',str(b));v=v[:start]+qa+v[end:];p.write_text(v)
p=o/'simulation/land_journey_audit.zig';p.write_text('''const std=@import("std");pub var tick:usize=0;pub var enabled=false;
pub const Summary=struct{root_rows:usize=0,credit:f64=0,demand:f64=0,used_rows:usize=0,positive_used:usize=0,max_h:f32=0,supported_rows:usize=0,exposed_demand_rows:usize=0,min_depth:f32=std.math.inf(f32),max_depth:f32=0};pub var summary:Summary=.{};
pub fn emit(comptime tag:[]const u8,value:anytype)void{if(!enabled)return;if(comptime std.mem.eql(u8,tag,"ROOT_WATER")){summary.root_rows+=1;summary.credit+=value.credit;summary.demand+=value.demand;if(value.credit<=0)return;}else if(comptime std.mem.eql(u8,tag,"USED_H")){summary.used_rows+=1;if(value.cohort.support_mass>0)summary.supported_rows+=1;if(value.current_demand>0)summary.exposed_demand_rows+=1;summary.min_depth=@min(summary.min_depth,value.depth_km);summary.max_depth=@max(summary.max_depth,value.depth_km);summary.max_h=@max(summary.max_h,value.effective_h);if(value.effective_h>0)summary.positive_used+=1; if(value.effective_h<=0)return;}var buffer:[8192]u8=undefined;var stream=std.io.fixedBufferStream(&buffer);std.json.stringify(value,.{},stream.writer()) catch unreachable;std.debug.print("{s} {s}\\n",.{tag,stream.getWritten()});}
''')
(b/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},indent=2))
inputs={}
for seed in (42,1337):
 for kind in ('ordinary','pioneer'):
  p=old/f'{seed}-{kind}-day7.json';inputs[p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
(b/'input-hashes.json').write_text(json.dumps(inputs,indent=2));print('PREPARED',b,inputs)
