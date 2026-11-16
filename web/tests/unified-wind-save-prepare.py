from pathlib import Path
import sys
r=Path(sys.argv[1]);p=r/'save_schema.zig';s=p.read_text();assert 'STANDALONE_WIND_VERSION' not in s
s=s.replace('pub const COMBINED_VERSION:u32=13;','pub const COMBINED_VERSION:u32=13;\npub const STANDALONE_WIND_VERSION:u32=11;',1)
s=s.replace('    pub fn jsonStringify(self:Save,writer:anytype)!void {','    pub fn jsonStringify(self:Save,writer:anytype)!void {\n        if(self.version==STANDALONE_WIND_VERSION){try standaloneWindWire(self,writer);return;}',1)
s=s.replace('self.version != COMBINED_VERSION and','self.version != STANDALONE_WIND_VERSION and self.version != COMBINED_VERSION and',1)
s=s.replace('        }else if(self.wind_dispersal!=null)return error.IncompatibleSave;','''        }else if(self.version==STANDALONE_WIND_VERSION){
            const cfg=self.wind_dispersal orelse return error.IncompatibleSave;
            if(self.mode!=.origin or !cfg.enabled or !cfg.runtime().valid())return error.InvalidValue;
            if(self.beta_origin!=null)return error.IncompatibleSave;
        }else if(self.wind_dispersal!=null)return error.IncompatibleSave;''',1)
s+='''
// Exact original Wind11 writer: no hidden root/thermal/protection conversion.
fn standaloneWindWire(value:anytype,writer:anytype) @TypeOf(writer.*).Error!void {
    const T=@TypeOf(value);
    if(T==SavedCell){
        try writer.beginObject();
        if(value.sparse)|entries|{try writer.objectField("sparse");try standaloneWindWire(entries,writer);}else{try writer.objectField("cohorts");try standaloneWindWire(value.cohorts,writer);}
        try writer.objectField("nutrient");try writer.write(value.nutrient);try writer.objectField("detritus");try writer.write(value.detritus);try writer.objectField("rng");try writer.write(value.rng);try writer.endObject();return;
    }
    switch(@typeInfo(T)){
        .Optional=>{if(value)|v|try standaloneWindWire(v,writer) else try writer.write(null);},
        .Struct=>{
            if(T!=Save and T!=Microbes.Cohort and @hasDecl(T,"jsonStringify")){try writer.write(value);return;}
            try writer.beginObject();inline for(std.meta.fields(T))|field|{
                if(comptime std.mem.eql(u8,field.name,"protective_investment") or std.mem.eql(u8,field.name,"protective_clock") or std.mem.eql(u8,field.name,"root_fraction") or std.mem.eql(u8,field.name,"beta_origin") or std.mem.eql(u8,field.name,"ground_thermal") or std.mem.eql(u8,field.name,"protective_strategy")){}
                else if(comptime T==Microbes.Cohort and std.mem.eql(u8,field.name,"aerial_allocation")){
                    if(@as(u32,@bitCast(value.aerial_allocation))!=0){try writer.objectField(field.name);try writer.write(value.aerial_allocation);}
                }else{try writer.objectField(field.name);try standaloneWindWire(@field(value,field.name),writer);}
            }try writer.endObject();
        },
        .Array=>{try writer.beginArray();for(value)|v|try standaloneWindWire(v,writer);try writer.endArray();},
        .Pointer=>|ptr|{if(ptr.size==.Slice and ptr.child!=u8){try writer.beginArray();for(value)|v|try standaloneWindWire(v,writer);try writer.endArray();}else try writer.write(value);},
        else=>try writer.write(value),
    }
}
''';p.write_text(s)
p=r/'save_game.zig';s=p.read_text();old='if(p.windDispersal.enabled and (p.worldMode!=.origin or !p.landBeta.enabled or p.landBeta.physiology_law!=3))';new='if(p.windDispersal.enabled and (p.worldMode!=.origin or !p.landBeta.valid() or (p.landBeta.enabled and p.landBeta.physiology_law!=3)))';assert old in s;s=s.replace(old,new,1)
s=s.replace('else if(p.windDispersal.enabled) schema.COMBINED_VERSION','else if(p.windDispersal.enabled) (if(p.landBeta.enabled) schema.COMBINED_VERSION else schema.STANDALONE_WIND_VERSION)',1);p.write_text(s)
