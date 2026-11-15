#!/usr/bin/env python3
"""Isolated schema10 root-only patch; never modifies production or source worlds."""
from pathlib import Path
import sys
p=Path(sys.argv[1]);s=(p/'save_schema.zig').read_text()
def once(s,a,b):
 assert s.count(a)==1,(a,s.count(a));return s.replace(a,b,1)
s=once(s,'pub const VERSION: u32 = 6;','pub const VERSION: u32 = 10;')
s=once(s,'pub const Origin = struct {','pub const RootConfig = struct { enabled:bool=false, law:u8=0, conductance:u8=1 };\npub const Origin = struct {\n    root_config:?RootConfig=null,\n    root_soil:[]const f64=&.{},')
s=once(s,'        if (self.version == 1 and','        if (self.version>=7 and self.version<=9)return error.IncompatibleSave;\n        if (self.version == 1 and')
s=once(s,'                if (origin.cells.len != count)', '''                if(self.version<10){
                    if(origin.root_config!=null or origin.root_soil.len!=0)return error.IncompatibleSave;
                }else{
                    const cfg=origin.root_config orelse return error.IncompatibleSave;
                    if(cfg.enabled){
                        if(cfg.law!=1 or (cfg.conductance!=1 and cfg.conductance!=10) or origin.root_soil.len!=count)return error.IncompatibleSave;
                        for(origin.root_soil)|water|try finiteRange(water,0,1);
                    }else if(cfg.law!=0 or cfg.conductance!=1 or origin.root_soil.len!=0)return error.IncompatibleSave;
                }
                if (origin.cells.len != count)''')
s=once(s,'                    for (cell.cohorts) |cohort| {','''                    for (cell.cohorts) |cohort| {
                        try finiteRange(cohort.root_fraction,0,1);
                        if((self.version<10 or !(origin.root_config orelse RootConfig{}).enabled) and cohort.root_fraction!=0)return error.IncompatibleSave;''')
(p/'save_schema.zig').write_text(s)
s=(p/'save_game.zig').read_text()
s=once(s,'.cells = sparse.cells, .stats = p.microbeStats };','.cells = sparse.cells, .stats = p.microbeStats, .root_config=.{.enabled=p.rootConfig.enabled,.law=p.rootConfig.law,.conductance=p.rootConfig.conductance}, .root_soil=if(p.rootConfig.enabled)p.rootSoil else &.{} };')
s=once(s,'    @import("patch_watch.zig").current.stop("world loaded");','''    if(saved.origin)|origin|{if(origin.root_config)|cfg|{if(cfg.enabled)try p.ensureRootSoil();}}
    @import("patch_watch.zig").current.stop("world loaded");''')
s=once(s,'    p.worldMode = saved.mode;','    p.resetRootModel();\n    p.worldMode = saved.mode;')
s=once(s,'        p.microbeStats = origin.stats;','''        p.microbeStats = origin.stats;
        if(origin.root_config)|cfg|{
            p.rootConfig=.{.enabled=cfg.enabled,.law=cfg.law,.conductance=cfg.conductance};
            if(cfg.enabled)@memcpy(p.rootSoil,origin.root_soil);
        }''')
(p/'save_game.zig').write_text(s)
print('ROOT_SAVE_PATCH schema10/model9 applied',p)
