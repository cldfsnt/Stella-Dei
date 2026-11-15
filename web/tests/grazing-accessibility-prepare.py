#!/usr/bin/env python3
"""Isolated core-step candidate; production files stay untouched."""
from pathlib import Path
import sys,shutil
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
s=(root/'src/simulation/microbes.zig').read_text();s=s[:s.index('\ntest ')]
a=s.index('pub fn graze(');b=s.index('\n/// Whole resident',a)
s=s[:a]+'''pub var accessibility_strength:f32=0;
pub var grazing_enabled:bool=true;
pub fn graze(cell:*Cell,days:f32,oxygen_capacity:f32) GrazingFlux {
 if(!grazing_enabled)return .{};
 return @import("grazing_accessibility.zig").graze(@This(),cell,days,oxygen_capacity,accessibility_strength);
}
'''+s[b:]
(out/'candidate.zig').write_text(s)
shutil.copy(root/'src/experimental/grazing_accessibility.zig',out/'grazing_accessibility.zig')
shutil.copy(root/'src/qa_grazing_accessibility.zig',out/'main.zig')
shutil.copy(root/'src/simulation/microbes.zig',out/'original.zig')

if len(sys.argv)>2 and sys.argv[2]=='--evolved':
 shutil.copytree(root/'src',out,dirs_exist_ok=True)
 s=(root/'src/qa_reciprocal_transplant.zig').read_text();s=s[:s.index('fn transplant(')]
 (out/'main.zig').write_text(s+(root/'src/qa_grazing_evolved.zig.part').read_text())
