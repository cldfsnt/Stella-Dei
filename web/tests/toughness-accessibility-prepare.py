#!/usr/bin/env python3
from pathlib import Path
import sys,subprocess,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve();subprocess.run([sys.executable,str(r/'web/tests/toughness-mutation-prepare.py'),str(o)],check=True)
p=o/'simulation/ecology.zig';s=p.read_text().replace('var child=offspring(parent,seed);','qa_calls+=1;var child=offspring(parent,seed);');s+='''
pub var qa_calls:u64=0;pub var qa_accepted:u64=0;pub var qa_plus:u64=0;pub var qa_minus:u64=0;pub var qa_clipped:u64=0;pub var qa_changed:u64=0;
pub fn qaAccepted(parent:Plant,child:Plant,seed:u64,config:MutationConfig,destination:usize,source:usize,time:f64)void{
 qa_accepted+=1;const proposal=if(config.enabled) @import("../toughness_mutation.zig").proposal(config.stream_seed,seed,parent.generation) else 0;
 if(proposal>0)qa_plus+=1;if(proposal<0)qa_minus+=1;if(proposal!=0 and child.toughness==parent.toughness)qa_clipped+=1;if(child.toughness!=parent.toughness)qa_changed+=1;
 std.debug.print("ACCESS_BIRTH stream={} destination={} source={} event={} parent_generation={} proposal={d} parent_d={d} child_d={d} time={d}\\n",.{config.stream_seed,destination,source,seed,parent.generation,proposal,parent.toughness,child.toughness,time});
}
''';p.write_text(s)
p=o/'simulation/planet.zig';s=p.read_text().replace('self.plantTraits[i] = child;','Ecology.qaAccepted(self.plantTraits[n],child,self.seed ^ (@as(u64,@intCast(i))*%0x9e3779b97f4a7c15) ^ epoch,self.toughnessMutation,i,n,options.gameTime);\n                        self.plantTraits[i] = child;');p.write_text(s)
p=o/'main.zig';s=p.read_text();a=s.index('          _=pm;_=pw;');b=s.index('\n        std.debug.print("FORAGING_PRODUCTION_COMPLETE',a);s=s[:a]+(r/'web/tests/toughness-accessibility-qa.txt').read_text().replace('OUTPUT',str(o.parent))+s[b:];p.write_text(s)
(o.parent/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},indent=2)+'\n')
