#!/usr/bin/env python3
from pathlib import Path
import shutil,sys,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve();frozen=r.parent/'site-tmp/toughness-mosaic/src';shutil.copytree(frozen,o,dirs_exist_ok=True)
for src,dest in [('toughness-mutation.zig','toughness_mutation.zig'),('toughness-mutation-qa.zig','qa_toughness_mutation.zig')]:shutil.copy2(r/'web/tests'/src,o/dest)
p=o/'simulation/ecology.zig';s=p.read_text();s+='''\npub const MutationConfig=@import("../toughness_mutation.zig").Config;
pub fn offspringWithMutation(parent:Plant,seed:u64,config:MutationConfig)Plant{
 var child=offspring(parent,seed);
 child.toughness=@import("../toughness_mutation.zig").allocation(parent.toughness,seed,parent.generation,config);
 return child;
}
''';p.write_text(s)
p=o/'simulation/planet.zig';s=p.read_text().replace('pub const Planet = struct {','pub const Planet = struct {\n    toughnessMutation:Ecology.MutationConfig=. {},').replace('const child = Ecology.offspring(self.plantTraits[n], self.seed ^ (@as(u64, @intCast(i)) *% 0x9e3779b97f4a7c15) ^ epoch);','const child = Ecology.offspringWithMutation(self.plantTraits[n], self.seed ^ (@as(u64, @intCast(i)) *% 0x9e3779b97f4a7c15) ^ epoch,self.toughnessMutation);');p.write_text(s)
shutil.copy2(r/'web/tests/sandbox-toughness-save.zig',o/'sandbox-toughness-save.zig')
if (r/'web/tests/sandbox-toughness-save-v2.zig').exists():shutil.copy2(r/'web/tests/sandbox-toughness-save-v2.zig',o/'toughness_save_v2.zig')
p=o/'main.zig';s=p.read_text();a=s.index('          _=pm;_=pw;');b=s.index('\n        std.debug.print("FORAGING_PRODUCTION_COMPLETE',a);s=s[:a]+(r/'web/tests/toughness-mutation-native-qa.txt').read_text().replace('OUTPUT',str(o.parent))+s[b:];p.write_text(s)
(o.parent/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},indent=2)+'\n')
