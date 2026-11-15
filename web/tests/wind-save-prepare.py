from pathlib import Path
import sys
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[2].parent/'site-tmp/wind-dispersal/src'
p=root/'simulation/microbes.zig';s=p.read_text();needle='    aerial_allocation:f32=0,\n';assert needle in s
method='''    pub fn jsonStringify(self:@This(),writer:anytype)!void{
        try writer.beginObject();
        inline for(std.meta.fields(@This())) |field| {
            const value=@field(self,field.name);
            if(comptime std.mem.eql(u8,field.name,"aerial_allocation")) {
                // +0 only is canonical legacy; validation rejects hidden -0.
                if(@as(u32,@bitCast(value))!=0){try writer.objectField(field.name);try writer.write(value);}
            } else {try writer.objectField(field.name);try writer.write(value);}
        }
        try writer.endObject();
    }
'''
assert 'pub fn jsonStringify(self:@This()' not in s;s=s.replace(needle,method+needle,1);p.write_text(s)
p=root/'save_schema.zig';s=p.read_text().replace('pub const VERSION: u32 = 7;','pub const VERSION: u32 = 7;\npub const WIND_VERSION:u32=11;\npub const WindConfig=@import("simulation/wind_genetics.zig").Config;\npub const SavedWind=struct{enabled:bool,law:u8,stream_seed:u64,serial:u64,pub fn runtime(c:@This())WindConfig{return .{.enabled=c.enabled,.law=c.law,.stream_seed=c.stream_seed,.serial=c.serial};}};')
s=s.replace('    sandbox_defense: ?', '    wind_dispersal:?SavedWind=null,\n    sandbox_defense: ?',1)
needle='    pub fn validate(self: Save) !void {'
method='''    pub fn jsonStringify(self:Save,writer:anytype)!void{
        try writer.beginObject();
        inline for(std.meta.fields(Save))|field|{
            const value=@field(self,field.name);
            if(comptime std.mem.eql(u8,field.name,"wind_dispersal")){
                if(value!=null){try writer.objectField(field.name);try writer.write(value);}
            }else{try writer.objectField(field.name);try writer.write(value);}
        }
        try writer.endObject();
    }
'''
s=s.replace(needle,method+needle,1)
s=s.replace('(self.version < 1 or self.version > VERSION)', '(self.version < 1 or (self.version > VERSION and self.version != WIND_VERSION))',1)
needle='        if (self.version == 1'
checks='''        if(self.version==WIND_VERSION){
            const cfg=self.wind_dispersal orelse return error.IncompatibleSave;
            if(self.mode!=.origin or !cfg.enabled or !cfg.runtime().valid())return error.InvalidValue;
        }else if(self.wind_dispersal!=null)return error.IncompatibleSave;
'''
s=s.replace(needle,checks+needle,1)
needle='                    for (cell.cohorts) |cohort| {\n'
checks='''                        try finiteRange(cohort.aerial_allocation,0,1);
                        if(@as(u32,@bitCast(cohort.aerial_allocation))==0x80000000)return error.InvalidValue;
                        if(self.wind_dispersal==null and cohort.aerial_allocation!=0)return error.IncompatibleSave;
'''
s=s.replace(needle,needle+checks,1);p.write_text(s)
p=root/'save_game.zig';s=p.read_text();needle='    const p = &state.planet;';start=s.index(needle,s.index('pub fn capture'))
s=s[:start]+s[start:].replace(needle,needle+'''
    if(!p.windDispersal.valid() or (p.windDispersal.enabled and p.worldMode!=.origin))return error.InvalidValue;
    for(p.microbeCells)|cell|for(cell.cohorts)|cohort|{
        if(!std.math.isFinite(cohort.aerial_allocation) or cohort.aerial_allocation<0 or cohort.aerial_allocation>1 or @as(u32,@bitCast(cohort.aerial_allocation))==0x80000000)return error.InvalidValue;
        if(!p.windDispersal.enabled and cohort.aerial_allocation!=0)return error.IncompatibleSave;
    };
''',1)
s=s.replace('.version = schema.VERSION,', '.version = if(p.windDispersal.enabled)schema.WIND_VERSION else schema.VERSION, .wind_dispersal = if(p.windDispersal.enabled) .{.enabled=true,.law=p.windDispersal.law,.stream_seed=p.windDispersal.stream_seed,.serial=p.windDispersal.serial} else null,',1)
s=s.replace('    p.worldMode = saved.mode;', '    p.worldMode = saved.mode;\n    p.windDispersal=if(saved.wind_dispersal)|cfg|cfg.runtime() else .{};',1);p.write_text(s)
