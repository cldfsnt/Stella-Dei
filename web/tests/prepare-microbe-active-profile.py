#!/usr/bin/env python3
"""Research-only copied CPU fixture: phase audit and dynamic ordered activity bits."""
from pathlib import Path
import shutil,sys
root=Path(__file__).resolve().parents[2];src=Path(sys.argv[1]);out=Path(sys.argv[2]);assert not out.exists();shutil.copytree(src,out)
(out/'qa_micro_metrics.zig').write_text('''const std=@import("std");
pub var enabled:bool=false;pub var candidate:bool=false;pub var sums:[3]u64=.{0}**3;pub var ticks:u64=0;
pub fn mark(bits:[]u64,i:usize)void{bits[i/64]|=@as(u64,1)<<@as(u6,@intCast(i%64));}
pub fn next(bits:[]u64,cursor:*usize,limit:usize)?usize{
 if(cursor.*>=limit)return null;
 var word=cursor.*/64;var mask=bits[word]&(~@as(u64,0)<<@as(u6,@intCast(cursor.*%64)));
 while(true){if(mask!=0){const i=word*64+@ctz(mask);if(i>=limit)return null;cursor.*=i+1;return i;}word+=1;if(word>=bits.len)return null;mask=bits[word];}
}
test "ordered iterator sees future same-word writes but never revisits lower cells"{var bits=[_]u64{0,0};mark(&bits,2);mark(&bits,90);var c:usize=0;try std.testing.expectEqual(@as(?usize,2),next(&bits,&c,100));mark(&bits,3);mark(&bits,1);try std.testing.expectEqual(@as(?usize,3),next(&bits,&c,100));try std.testing.expectEqual(@as(?usize,90),next(&bits,&c,100));mark(&bits,99);mark(&bits,100);try std.testing.expectEqual(@as(?usize,99),next(&bits,&c,100));try std.testing.expectEqual(@as(?usize,null),next(&bits,&c,100));}
''')
(out/'active_cell_index.zig').write_text((root/'src/active_cell_index.zig').read_text())
p=out/'qa_micro_metrics.zig';q=p.read_text();i=q.index('pub fn mark(');j=q.index('test "',i);p.write_text(q[:i]+'pub const mark=@import("active_cell_index.zig").mark;\npub const next=@import("active_cell_index.zig").next;\n'+q[j:])
p=out/'simulation/planet.zig';s=p.read_text();a=s.index('    pub fn simulateMicrobes(');b=s.index('    pub fn simulateVegetation',a);part=s[a:b]
needle='        const watch=&@import("../patch_watch.zig").current;';assert needle in part
part=part.replace(needle,'''        const qa=@import("../qa_micro_metrics.zig");var micro_timer=std.time.Timer.start() catch unreachable;
        const active:?[]u64=if(qa.candidate)self.allocator.alloc(u64,(self.microbeCells.len+63)/64) catch null else null;
        defer if(active)|bits|self.allocator.free(bits);
        if(active)|bits|@memset(bits,0);
'''+needle,1)
needle='            if (Microbes.biomass(cell.*) <= 0 and cell.detritus <= 0) continue;';part=part.replace(needle,needle+'\n            if(active)|bits|qa.mark(bits,i);',1)
needle='        // A resident cohort may make at most one adjacent relocation per step.';part=part.replace(needle,'        if(qa.enabled)qa.sums[0]+=micro_timer.lap() else _=micro_timer.lap();\n'+needle,1)
needle='        for (0..self.microbeCells.len) |i| {';assert part.count(needle)==1
part=part.replace(needle,'''        var move_cursor:usize=0;
        while(if(active)|bits|qa.next(bits,&move_cursor,self.microbeCells.len) else blk:{if(move_cursor>=self.microbeCells.len)break :blk null;const index=move_cursor;move_cursor+=1;break :blk @as(?usize,index);})|i|{''',1)
part=part.replace('                if (moved.moved) {','                if (moved.moved) {\n                    if(active)|bits|qa.mark(bits,moved.to);',1)
needle='        // All growth precedes dispersal.';part=part.replace(needle,'        if(qa.enabled)qa.sums[1]+=micro_timer.lap() else _=micro_timer.lap();\n'+needle,1)
needle='        for (self.microbeCells, 0..) |*cell, i| {';assert part.count(needle)==2
idx=part.rindex(needle);part=part[:idx]+part[idx:].replace(needle,'''        var birth_cursor:usize=0;
        while(if(active)|bits|qa.next(bits,&birth_cursor,self.microbeCells.len) else blk:{if(birth_cursor>=self.microbeCells.len)break :blk null;const index=birth_cursor;birth_cursor+=1;break :blk @as(?usize,index);})|i|{
            const cell=&self.microbeCells[i];''',1)
part=part.replace('                            self.propaguleArrivals+|=1;', '                            if(active)|bits|qa.mark(bits,n);\n                            self.propaguleArrivals+|=1;',1)
needle='                    if (Microbes.reproduce(cell, cohort, &self.microbeCells[n], &self.microbeStats, true)) break;';assert needle in part
part=part.replace(needle,'                    if (Microbes.reproduce(cell, cohort, &self.microbeCells[n], &self.microbeStats, true)){if(active)|bits|qa.mark(bits,n);break;}',1)
idx=part.rfind('    }');part=part[:idx]+'        if(qa.enabled){qa.sums[2]+=micro_timer.read();qa.ticks+=1;}\n'+part[idx:];s=s[:a]+part+s[b:];p.write_text(s)
p=out/'main.zig';s=p.read_text();needle='    originReport("seeded",state);';assert needle in s
s=s.replace(needle,needle+'\n    if(std.posix.getenv("QA_MICRO_REPLAY"))|path|{try profileMicroReplay(state,allocator,path);game.loop.pump(16);return;}\n',1)
s+=(root/'web/tests/microbe-active-profile.zig.part').read_text();p.write_text(s)
