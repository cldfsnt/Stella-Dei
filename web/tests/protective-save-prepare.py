from pathlib import Path
import sys
r=Path(sys.argv[1]);p=r/'save_schema.zig';s=p.read_text();assert 'PROTECTIVE_VERSION' not in s
s=s.replace('pub const CALM_VERSION:u32=14;','''pub const CALM_VERSION:u32=14;
pub const PROTECTIVE_VERSION:u32=15;
pub const SavedProtective=struct{law:u8,mutation_law:u8,stream_seed:u64,pub fn runtime(c:@This())@import("simulation/protective_strategy.zig").Config{return .{.enabled=true,.law=c.law,.mutation_law=c.mutation_law,.stream_seed=c.stream_seed};}};''',1)
s=s.replace('    ground_thermal:?GroundThermal=null,','    ground_thermal:?GroundThermal=null,\n    protective_strategy:?SavedProtective=null,',1)
s=s.replace('        try writer.beginObject();\n        inline for(std.meta.fields(Save))','        if(self.protective_strategy==null){try protectiveLegacyWire(self,writer);return;}\n        try writer.beginObject();\n        inline for(std.meta.fields(Save))',1)
s=s.replace('self.version != CALM_VERSION))','self.version != CALM_VERSION and self.version != PROTECTIVE_VERSION))',1)
s=s.replace('        if(self.version==CALM_VERSION){','''        if(self.version==PROTECTIVE_VERSION){
            const cfg=self.protective_strategy orelse return error.IncompatibleSave;
            if(!cfg.runtime().valid())return error.InvalidValue;
        }else if(self.protective_strategy!=null)return error.IncompatibleSave;
        if(self.version==CALM_VERSION or self.version==PROTECTIVE_VERSION){''',1)
s=s.replace('self.version==COMBINED_VERSION or self.version==CALM_VERSION){','self.version==COMBINED_VERSION or self.version==CALM_VERSION or self.version==PROTECTIVE_VERSION){',1)
s=s.replace('self.version!=CALM_VERSION) or beta.format','self.version!=CALM_VERSION and self.version!=PROTECTIVE_VERSION) or beta.format',1)
s=s.replace('                    for (cell.cohorts) |cohort| {\n','''                    for (cell.cohorts) |cohort| {
                        try validateProtective(cohort,self.protective_strategy!=null);
''',1)
# Old recursive serializers must omit both new cohort fields and new config.
s=s.replace('if(comptime (std.mem.eql(u8,field.name,"root_fraction")', '''if(comptime std.mem.eql(u8,field.name,"protective_investment") or std.mem.eql(u8,field.name,"protective_clock")){
        std.debug.assert(@field(value,field.name)==(if(comptime std.mem.eql(u8,field.name,"protective_clock")) @as(f32,-1) else @as(f32,0)));
    }else if(comptime (std.mem.eql(u8,field.name,"root_fraction")''',1)
s=s.replace('if(comptime std.mem.eql(u8,field.name,"aerial_allocation")){std.debug.assert', '''if(comptime std.mem.eql(u8,field.name,"protective_investment") or std.mem.eql(u8,field.name,"protective_clock")){
                    std.debug.assert(@field(value,field.name)==(if(comptime std.mem.eql(u8,field.name,"protective_clock")) @as(f32,-1) else @as(f32,0)));
                }else if(comptime std.mem.eql(u8,field.name,"aerial_allocation")){std.debug.assert''',1)
s=s.replace('!std.mem.eql(u8,field.name,"ground_thermal")','!std.mem.eql(u8,field.name,"ground_thermal") and !std.mem.eql(u8,field.name,"protective_strategy")')
s+='''
pub fn validateProtective(c:Microbes.Cohort,enabled:bool)!void{
    try finiteRange(c.protective_investment,0,1);
    if(!std.math.isFinite(c.protective_clock) or (c.protective_clock != -1 and c.protective_clock<0))return error.InvalidValue;
    if(c.protective_investment==0 and c.protective_clock != -1)return error.InvalidValue;
    if(!enabled and (c.protective_investment!=0 or c.protective_clock != -1))return error.IncompatibleSave;
}
fn protectiveLegacyWire(value:anytype,writer:anytype) @TypeOf(writer.*).Error!void {
    const T=@TypeOf(value);
    if(T==SavedCell){
        try writer.beginObject();
        if(value.sparse)|entries|{try writer.objectField("sparse");try protectiveLegacyWire(entries,writer);}else{try writer.objectField("cohorts");try protectiveLegacyWire(value.cohorts,writer);}
        try writer.objectField("nutrient");try writer.write(value.nutrient);try writer.objectField("detritus");try writer.write(value.detritus);try writer.objectField("rng");try writer.write(value.rng);try writer.endObject();return;
    }
    switch(@typeInfo(T)){
        .Optional=>{if(value)|v|try protectiveLegacyWire(v,writer) else try writer.write(null);},
        .Struct=>{
            if(T!=Save and T!=Microbes.Cohort and @hasDecl(T,"jsonStringify")){try writer.write(value);return;}
            try writer.beginObject();inline for(std.meta.fields(T))|field|{
                if(comptime std.mem.eql(u8,field.name,"protective_investment") or std.mem.eql(u8,field.name,"protective_clock")){}
                else if(comptime std.mem.eql(u8,field.name,"protective_strategy")){}
                else if(comptime T==Save and std.mem.eql(u8,field.name,"ground_thermal")){
                    if(value.ground_thermal!=null){try writer.objectField(field.name);try writer.write(value.ground_thermal);}
                }else{try writer.objectField(field.name);try protectiveLegacyWire(@field(value,field.name),writer);}
            }try writer.endObject();
        },
        .Array=>{try writer.beginArray();for(value)|v|try protectiveLegacyWire(v,writer);try writer.endArray();},
        .Pointer=>|ptr|{if(ptr.size==.Slice and ptr.child!=u8){try writer.beginArray();for(value)|v|try protectiveLegacyWire(v,writer);try writer.endArray();}else try writer.write(value);},
        else=>try writer.write(value),
    }
}
''';p.write_text(s)
p=r/'save_game.zig';s=p.read_text();s=s.replace('    if(p.groundThermalLaw>1','''    if(!p.protectiveStrategy.valid() or (p.protectiveStrategy.enabled and (p.groundThermalLaw!=1 or !p.windDispersal.enabled or !p.landBeta.enabled or p.landBeta.physiology_law!=3 or p.worldMode!=.origin)))return error.InvalidValue;
    for(p.microbeCells)|cell|for(cell.cohorts)|cohort|{try schema.validateProtective(cohort,p.protectiveStrategy.enabled);};
    if(p.groundThermalLaw>1''',1)
s=s.replace('.version = if(p.groundThermalLaw==1)', '.version = if(p.protectiveStrategy.enabled) schema.PROTECTIVE_VERSION else if(p.groundThermalLaw==1)',1)
s=s.replace('.beta_origin=beta,','.beta_origin=beta, .protective_strategy=if(p.protectiveStrategy.enabled) .{.law=p.protectiveStrategy.law,.mutation_law=p.protectiveStrategy.mutation_law,.stream_seed=p.protectiveStrategy.stream_seed} else null,',1)
s=s.replace('    p.groundThermalLaw=if(saved.ground_thermal)|cfg|cfg.law else 0;','    p.groundThermalLaw=if(saved.ground_thermal)|cfg|cfg.law else 0;\n    p.protectiveStrategy=if(saved.protective_strategy)|cfg|cfg.runtime() else .{};',1);p.write_text(s)
