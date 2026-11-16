from pathlib import Path
import json,hashlib,shutil
r=Path(__file__).resolve().parents[2];t=r.parent/'site-tmp';b=t/'protective-journey';b.mkdir(exist_ok=True)
qa=(r/'web/tests/natural-shoreline-qa.txt').read_text().replace('stella_combined_calm_new','stella_combined_protective_new').replace('c.organization==0);','c.organization==0 and c.protective_investment==0 and c.protective_clock == -1);')
qa=qa.replace('const QaSeen=struct{last:usize,alive:bool=true};','const QaSeen=struct{last:usize,alive:bool=true,clock:f32=-1};')
qa=qa.replace('e.value_ptr.*=.{.last=tick};','if(c.protective_investment>0 and (!e.found_existing or e.value_ptr.clock!=c.protective_clock))qaEmit("PROTECTION_STATE",.{.tick=tick,.point=p,.id=c.lineage,.investment=c.protective_investment,.clock=c.protective_clock,.temperature=s.planet.temperature[p]});e.value_ptr.*=.{.last=tick,.clock=c.protective_clock};')
qa=qa.replace('var mass:f64=0;','var protective:usize=0;var resting:usize=0;var mass:f64=0;').replace('living+=1;mass+=','living+=1;if(c.protective_investment>0){protective+=1;if(c.protective_clock>=0)resting+=1;}mass+=').replace('.supported=supported,.stats=', '.supported=supported,.protective=protective,.resting=resting,.stats=')
(r/'web/tests/protective-journey-qa.txt').write_text(qa)
s=(r/'web/tests/prepare-calm-release-native.py').read_text().replace("b=t/'calm-release-native'","b=t/'protective-journey'").replace("src=t/'root-calm/src'","src=t/'protective-integration/src'").replace('root-calm-engine/source-hashes.json','protective-integration/source-hashes.json').replace('calm-release-qa.txt','protective-journey-qa.txt')
exec(compile(s,str(r/'web/tests/prepare-calm-release-native.py'),'exec'),{'__file__':str(r/'web/tests/prepare-calm-release-native.py')})
o=b/'src';shutil.copy2(t/'natural-shoreline/src/simulation/shore_audit.zig',o/'simulation/shore_audit.zig')
p=o/'simulation/planet.zig';s=p.read_text();s=s.replace('self.waterMass[i]=column.state.liquid;','for(0..4)|slot|{@import("shore_audit.zig").credit(self.microbeCells[i].cohorts[slot].lineage,column.root_credits[slot]);}\n            self.waterMass[i]=column.state.liquid;');s=s.replace('if(paid>0)self.applyMicrobeFlux(.{.recycled=paid});','if(paid>0){if(@import("shore_audit.zig").enabled)std.debug.print("PROTECTION_PAID tick={} point={} kg_c_m2={e}\\n",.{@import("shore_audit.zig").tick,i,paid});self.applyMicrobeFlux(.{.recycled=paid});}');p.write_text(s)
p=o/'simulation/microbes.zig';s=p.read_text();s=s.replace('         const wet_mortality=0.04+','        @import("shore_audit.zig").hydration(c.lineage,hydrated);\n         const wet_mortality=0.04+');p.write_text(s)
ref=t/'protective-history-reference';shutil.copytree(t/'natural-shoreline/src',ref/'src')
# Same generic historical adapter in both copies; no model-field normalization.
block='''    if(std.posix.getenv("QA_HISTORY"))|path|{const bytes=try std.fs.cwd().readFileAlloc(a,path,128*1024*1024);const parsed=try saves.schema.parse(a,bytes);try saves.apply(state,parsed.value);loop.pump(4096);std.debug.assert(std.mem.eql(u8,bytes,try qaBytes(a,state)));for(0..4)|i|{qaTick(state);const output=try std.fmt.allocPrint(a,"DEST/history-{s}-{}.json",.{std.posix.getenv("QA_LABEL") orelse "unknown",i+1});try qaWrite(a,state,output);}std.debug.print("HISTORY_PASS\\n",.{});std.process.exit(0);}\n'''
for base in [b,ref]:
 p=base/'src/main.zig';s=p.read_text();needle='    const stage=std.posix.getenv("QA_STAGE")';assert s.count(needle)==1;s=s.replace(needle,block.replace('DEST',str(base))+needle);p.write_text(s)
 (base/'source-hashes.json').write_text(json.dumps({str(p.relative_to(base/'src')):hashlib.sha256(p.read_bytes()).hexdigest()for p in(base/'src').rglob('*.zig')},indent=2))
