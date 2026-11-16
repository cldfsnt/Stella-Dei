from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];t=r.parent/'site-tmp';old=t/'combined-day21';base=t/'cutoff-trial';base.mkdir(exist_ok=True)
for n,h in json.loads((old/'source-hashes.json').read_text()).items():assert hashlib.sha256((old/'src'/n).read_bytes()).hexdigest()==h,n
for label,threshold in [('legacy','0.0025'),('small','0.001')]:
 b=base/label;o=b/'src';b.mkdir(exist_ok=True);shutil.copytree(old/'src',o,dirs_exist_ok=True)
 p=o/'main.zig';v=p.read_text();start=v.index('    const saves=@import("save_game.zig");const M=');end=v.index('\nfn qaWindTick',start);q=(r/'web/tests/combined-day21-qa.txt').read_text()
 q=q.replace('const pioneer=',f'const threshold:f32={threshold};const Envelope=struct{{format:enum{{cutoff_qa_v1}},threshold:f32,state:saves.schema.Save}};const pioneer=')
 q=q.replace('OUTPUT/{s}-day14.json','OUTPUT/{s}-day10.json').replace('else 420;','else 420;').replace('if(resumed)840','if(resumed)600').replace('first..1260','first..840').replace('tick+1==840 or tick+1==1260','tick+1==600 or tick+1==840').replace('DAY21_COMPLETE','CUTOFF_COMPLETE')
 oldparse='const parsed=try saves.schema.parse(a,bytes);try saves.apply(state,parsed.value);std.debug.assert(std.mem.eql(u8,bytes,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));'
 newparse='var payload:saves.schema.Save=undefined;if(resumed){const e=try std.json.parseFromSlice(Envelope,a,bytes,.{.allocate=.alloc_always});if(e.value.threshold!=threshold)return error.WrongCutoffIdentity;payload=e.value.state;}else{const original=try saves.schema.parse(a,bytes);payload=original.value;}try saves.apply(state,payload);const loaded=try saves.capture(a,state);if(resumed){std.debug.assert(std.mem.eql(u8,bytes,try std.json.stringifyAlloc(a,Envelope{.format=.cutoff_qa_v1,.threshold=threshold,.state=loaded},.{})));}else{std.debug.assert(std.mem.eql(u8,bytes,try std.json.stringifyAlloc(a,loaded,.{})));}'
 assert oldparse in q;q=q.replace(oldparse,newparse).replace('saves.apply(state,parsed.value)','saves.apply(state,payload)')
 needle='.data=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})'
 q=q.replace(needle,'.data=try std.json.stringifyAlloc(a,Envelope{.format=.cutoff_qa_v1,.threshold=threshold,.state=try saves.capture(a,state)},.{})')
 q=q.replace('INPUT',str(t/'combined-strategy')).replace('OUTPUT',str(b));v=v[:start]+q+v[end:];p.write_text(v)
 p=o/'simulation/microbes.zig';v=p.read_text();needle='        const wanted_dead=c.biomass*';assert v.count(needle)==1;v=v.replace(needle,'        const qa_before_mortality=c.*;\n'+needle)
 needle='if(c.biomass<0.0025){result.failed_patches+=1;';assert v.count(needle)==1;v=v.replace(needle,'if(c.biomass<'+threshold+'){ @import("land_journey_audit.zig").emit("CLEANUP",.{.tick=@import("land_journey_audit.zig").tick,.lineage=c.lineage,.before_mortality=qa_before_mortality,.after_mortality=c.*,.upkeep=upkeep,.continuous_dead=dead,.environment=env});result.failed_patches+=1;');p.write_text(v)
 (b/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},indent=2))
a=(base/'legacy/src/simulation/microbes.zig').read_text();b=(base/'small/src/simulation/microbes.zig').read_text();assert a.replace('if(c.biomass<0.0025){','if(c.biomass<0.001){')==b
for p in(base/'legacy/src/simulation').glob('*.zig'):
 if p.name!='microbes.zig':assert p.read_bytes()==(base/'small/src/simulation'/p.name).read_bytes(),p
print('MODEL_ONLY_CLEANUP_LITERAL_DIFF_PASS')
