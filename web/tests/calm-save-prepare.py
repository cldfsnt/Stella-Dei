from pathlib import Path
import sys
r=Path(sys.argv[1]);p=r/'save_schema.zig';s=p.read_text();assert 'CALM_VERSION' not in s
s=s.replace('pub const COMBINED_VERSION:u32=13;','pub const COMBINED_VERSION:u32=13;\npub const CALM_VERSION:u32=14;\npub const GroundThermal=struct{law:u8};',1)
s=s.replace('    wind_dispersal:?SavedWind=null,','    wind_dispersal:?SavedWind=null,\n    ground_thermal:?GroundThermal=null,',1)
s=s.replace('inline for(std.meta.fields(Save))|field|{try writer.objectField(field.name);try writer.write(@field(self,field.name));}', '''inline for(std.meta.fields(Save))|field|{
            if(comptime std.mem.eql(u8,field.name,"ground_thermal")){
                if(self.ground_thermal!=null){try writer.objectField(field.name);try writer.write(self.ground_thermal);}
            }else{try writer.objectField(field.name);try writer.write(@field(self,field.name));}
        }''',1)
s=s.replace('self.version != COMBINED_VERSION))','self.version != COMBINED_VERSION and self.version != CALM_VERSION))',1)
s=s.replace('        if(self.version==COMBINED_VERSION){','''        if(self.version==CALM_VERSION){
            const thermal=self.ground_thermal orelse return error.IncompatibleSave;
            if(thermal.law!=1)return error.InvalidValue;
        }else if(self.ground_thermal!=null)return error.IncompatibleSave;
        if(self.version==COMBINED_VERSION or self.version==CALM_VERSION){''',1)
s=s.replace('self.version!=10 and self.version!=COMBINED_VERSION)','self.version!=10 and self.version!=COMBINED_VERSION and self.version!=CALM_VERSION)',1)
s=s.replace('!std.mem.eql(u8,field.name,"wind_dispersal")','!std.mem.eql(u8,field.name,"wind_dispersal") and !std.mem.eql(u8,field.name,"ground_thermal")')
p.write_text(s)
p=r/'save_game.zig';s=p.read_text();s=s.replace('    if(!p.windDispersal.valid())','''    if(p.groundThermalLaw>1 or (p.groundThermalLaw==1 and (!p.windDispersal.enabled or p.worldMode!=.origin or !p.landBeta.enabled or p.landBeta.physiology_law!=3)))return error.InvalidValue;
    if(!p.windDispersal.valid())''',1)
s=s.replace('.version = if(p.windDispersal.enabled)', '.version = if(p.groundThermalLaw==1) schema.CALM_VERSION else if(p.windDispersal.enabled)',1)
s=s.replace('.beta_origin=beta,','.beta_origin=beta, .ground_thermal=if(p.groundThermalLaw==1) .{.law=1} else null,',1)
s=s.replace('    p.windDispersal=if(saved.wind_dispersal)|cfg|cfg.runtime() else .{};', '    p.windDispersal=if(saved.wind_dispersal)|cfg|cfg.runtime() else .{};\n    p.groundThermalLaw=if(saved.ground_thermal)|cfg|cfg.law else 0;',1)
p.write_text(s)
