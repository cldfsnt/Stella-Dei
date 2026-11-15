from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/terrain-geometry';o=b/'native-src';assert not o.exists();shutil.copytree(b/'src',o);old=r.parent/'site-tmp/origin-land-gate/candidate/src'
for n in ['main.zig','audio.zig','loop.zig']:shutil.copyfile(old/n,o/n)
p=o/'main.zig';s=p.read_text().replace('startOriginNext: bool = false,','startOriginNext: bool = false,\n    startWetlandsNext:bool=false,');start=s.index('    const saves=@import("save_game.zig");const P=',s.index('pub fn main'));end=s.index('std.process.exit(0);',start)+len('std.process.exit(0);');s=s[:start]+(r/'web/tests/terrain-geometry-native-qa.txt').read_text()+s[end:];p.write_text(s)
p=o/'simulation/planet.zig';s=p.read_text();s=s.replace('    pub fn setTerrainElevation(', '    pub var qa_terrain_refreshes:usize=0;\n    pub var qa_assert_fresh:bool=false;\n    pub var qa_tilt:f32=0;\n    fn qaAssertFresh(self:*Planet)void{@setFloatMode(.optimized);const rotation=za.Mat4.fromRotation(qa_tilt,Vec3.right());for(self.vertices,0..)|point,i|std.debug.assert(std.meta.eql(self.transformedPoints[i],self.terrainPoint(point,i,rotation)));}\n    pub fn setTerrainElevation(',1).replace('        self.elevation[index]=value;','        qa_terrain_refreshes+=1;\n        self.elevation[index]=value;',1)
needle='    pub fn simulate(self: *Planet, loop: *EventLoop, options: SimulationOptions) void {';assert needle in s;s=s.replace(needle,needle+'\n        if(qa_assert_fresh)self.qaAssertFresh();',1)
# Freshness already compared to exact full refresh immediately after real tool; no hidden geometry edits follow.
p.write_text(s)


p=o/"states/play.zig";s=p.read_text().replace('const subdivisions: usize = if (@import("builtin").target.cpu.arch == .wasm32 or @import("builtin").mode == .Debug) 6 else 7;', 'const subdivisions: usize = 6; // QA matches immutable saved topology');p.write_text(s)

(b/'native-source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},indent=2)+'\n')
