from pathlib import Path
import sys
root=Path(sys.argv[1]);p=root/'save_schema.zig';s=p.read_text()
s=s.replace('pub const VERSION: u32 = 10;','''pub const VERSION: u32 = 10;
pub const COMBINED_VERSION:u32=13;
pub const WindConfig=@import("simulation/wind_genetics.zig").Config;
pub const SavedWind=struct{enabled:bool,law:u8,stream_seed:u64,serial:u64,pub fn runtime(c:@This())WindConfig{return .{.enabled=c.enabled,.law=c.law,.stream_seed=c.stream_seed,.serial=c.serial};}};''',1)
s=s.replace('    beta_origin:?BetaOrigin=null,','    beta_origin:?BetaOrigin=null,\n    wind_dispersal:?SavedWind=null,',1)
s=s.replace('        try writer.beginObject();\n        inline for(std.meta.fields(Save))','        if(self.wind_dispersal==null){try historicalWire(self,writer);return;}\n        try writer.beginObject();\n        inline for(std.meta.fields(Save))',1)
s=s.replace('self.version > VERSION','(self.version > VERSION and self.version != COMBINED_VERSION)',1)
s=s.replace('        if (self.version == 1', '''        if(self.version==COMBINED_VERSION){
            const cfg=self.wind_dispersal orelse return error.IncompatibleSave;
            const beta=self.beta_origin orelse return error.IncompatibleSave;
            if(self.mode!=.origin or !cfg.enabled or !cfg.runtime().valid() or !beta.config.enabled or beta.config.physiology_law!=3)return error.InvalidValue;
        }else if(self.wind_dispersal!=null)return error.IncompatibleSave;
        if (self.version == 1''',1)
s=s.replace('self.version!=10 or beta.format','(self.version!=10 and self.version!=COMBINED_VERSION) or beta.format',1)
needle='                    for (cell.cohorts) |cohort| {\n';assert needle in s
s=s.replace(needle,needle+'''                        try finiteRange(cohort.aerial_allocation,0,1);
                        if(@as(u32,@bitCast(cohort.aerial_allocation))==0x80000000)return error.InvalidValue;
                        if(self.wind_dispersal==null and cohort.aerial_allocation!=0)return error.IncompatibleSave;
''',1)
s=s.replace('std.mem.eql(u8,field.name,"root_fraction")','(std.mem.eql(u8,field.name,"root_fraction") or std.mem.eql(u8,field.name,"aerial_allocation"))',1)
s=s.replace('!std.mem.eql(u8,field.name,"beta_origin")','!std.mem.eql(u8,field.name,"beta_origin") and !std.mem.eql(u8,field.name,"wind_dispersal")',1)
s+='''
// Preserve the historical beta serializer, including sparse cells and law1's
// custom config emission. Only newly introduced wind fields are omitted.
fn historicalWire(value:anytype,writer:anytype) @TypeOf(writer.*).Error!void {
    const T=@TypeOf(value);
    if(T==SavedCell){
        try writer.beginObject();
        if(value.sparse)|entries|{try writer.objectField("sparse");try historicalWire(entries,writer);}else{try writer.objectField("cohorts");try historicalWire(value.cohorts,writer);}
        try writer.objectField("nutrient");try writer.write(value.nutrient);
        try writer.objectField("detritus");try writer.write(value.detritus);
        try writer.objectField("rng");try writer.write(value.rng);
        try writer.endObject();return;
    }
    switch(@typeInfo(T)){
        .Optional=>{if(value)|v|try historicalWire(v,writer) else try writer.write(null);},
        .Struct=>{
            if(T!=Save and T!=Microbes.Cohort and @hasDecl(T,"jsonStringify")){try writer.write(value);return;}
            try writer.beginObject();
            inline for(std.meta.fields(T))|field|{
                if(comptime std.mem.eql(u8,field.name,"aerial_allocation")){std.debug.assert(@as(u32,@bitCast(@field(value,field.name)))==0);}
                else if(comptime !std.mem.eql(u8,field.name,"wind_dispersal")){try writer.objectField(field.name);try historicalWire(@field(value,field.name),writer);}
            }
            try writer.endObject();
        },
        .Array=>{try writer.beginArray();for(value)|v|try historicalWire(v,writer);try writer.endArray();},
        .Pointer=>|ptr|{if(ptr.size==.Slice and ptr.child!=u8){try writer.beginArray();for(value)|v|try historicalWire(v,writer);try writer.endArray();}else try writer.write(value);},
        else=>try writer.write(value),
    }
}
''';p.write_text(s)
p=root/'save_game.zig';s=p.read_text();needle='    const p = &state.planet;';i=s.index(needle,s.index('pub fn capture'))
s=s[:i]+s[i:].replace(needle,needle+'''
    if(!p.windDispersal.valid())return error.InvalidValue;
    if(p.windDispersal.enabled and (p.worldMode!=.origin or !p.landBeta.enabled or p.landBeta.physiology_law!=3))return error.InvalidValue;
    for(p.microbeCells)|cell|for(cell.cohorts)|cohort|{
        const a=cohort.aerial_allocation;
        if(!std.math.isFinite(a) or a<0 or a>1 or @as(u32,@bitCast(a))==0x80000000 or (!p.windDispersal.enabled and a!=0))return error.InvalidValue;
    };
''',1)
s=s.replace('.version = if(beta!=null)', '.version = if(p.windDispersal.enabled) schema.COMBINED_VERSION else if(beta!=null)',1)
s=s.replace('.beta_origin=beta,','.beta_origin=beta, .wind_dispersal=if(p.windDispersal.enabled) .{.enabled=true,.law=p.windDispersal.law,.stream_seed=p.windDispersal.stream_seed,.serial=p.windDispersal.serial} else null,',1)
s=s.replace('    }else p.resetLandBeta();','    }else p.resetLandBeta();\n    p.windDispersal=if(saved.wind_dispersal)|cfg|cfg.runtime() else .{};',1)
p.write_text(s)
