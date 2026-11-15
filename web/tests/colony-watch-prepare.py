#!/usr/bin/env python3
from pathlib import Path
import sys,subprocess
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1]);subprocess.run([sys.executable,str(root/'web/tests/egl-ecology-pulse-prepare.py'),str(out)],check=True)
(out/'colony_snapshot.zig').write_text((root/'web/tests/continuation-review/colony-watch/candidate/colony_snapshot.zig').read_text())
p=out/'patch_watch.zig';s=p.read_text().replace('const std=@import("std");','const std=@import("std");\nconst Colonies=@import("colony_snapshot.zig");')
s=s.replace(' pub const Population=struct{biomass:f64=0,colonies:u8=0};',' start_members:Colonies.Snapshot=.{.valid=false},end_members:Colonies.Snapshot=.{.valid=false},\n pub const Population=struct{biomass:f64=0,colonies:u8=0,members:Colonies.Snapshot=.{.valid=false}};')
s=s.replace('  var p=Population{};','  var p=Population{.members=Colonies.capture(cohorts)};')
s=s.replace('self.end_colonies=v.colonies;return true;','self.end_colonies=v.colonies;self.start_members=v.members;self.end_members=v.members;return true;')
s=s.replace('self.end_colonies=v.colonies;}','self.end_colonies=v.colonies;self.end_members=v.members;}');p.write_text(s)
p=out/'main.zig';s=p.read_text().replace('patch_watch_json:[1024]','patch_watch_json:[4096]')
s=s.replace('.end_colonies=PatchWatch.current.end_colonies}', '.end_colonies=PatchWatch.current.end_colonies,.start_members=if(PatchWatch.current.start_members.valid) @as(?[]const @import("colony_snapshot.zig").Entry,PatchWatch.current.start_members.entries[0..PatchWatch.current.start_members.len]) else null,.end_members=if(PatchWatch.current.end_members.valid) @as(?[]const @import("colony_snapshot.zig").Entry,PatchWatch.current.end_members.entries[0..PatchWatch.current.end_members.len]) else null}')
s=s.replace('std.debug.assert(watched.end_biomass==end_pop.biomass and watched.end_colonies==end_pop.colonies);','std.debug.assert(watched.end_biomass==end_pop.biomass and watched.end_colonies==end_pop.colonies);\n          std.debug.assert(std.meta.eql(watched.end_members,end_pop.members));\n          std.debug.assert(std.meta.eql(watched.start_members,start_pop.members));\n          std.debug.print("COLONY_ENDPOINTS exact_start_end=true max4=true\\n",.{});')
p.write_text(s)
