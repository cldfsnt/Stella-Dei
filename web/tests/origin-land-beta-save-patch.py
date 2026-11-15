#!/usr/bin/env python3
"""Isolated schema8 adapter only; never edits production or regenerates scheduler."""
from pathlib import Path
import sys
p=Path(sys.argv[1]);f=p/'save_schema.zig';s=f.read_text();assert 'beta_origin' not in s
s=s.replace('pub const VERSION: u32 = 7;','pub const VERSION: u32 = 8;\npub const BetaOrigin=struct{format:enum{origin_land_beta_v1},config:@import("simulation/land_beta.zig").Config,soil:[]const f64,vapor:[]const f64};')
s=s.replace('    sandbox_defense: ?', '    beta_origin:?BetaOrigin=null,\n    sandbox_defense: ?')
needle='        switch (self.mode) {'
s=s.replace(needle,'''        if(self.beta_origin)|beta|{
            if(self.version!=8)return error.IncompatibleSave;
            if(self.mode!=.origin or !beta.config.enabled or !beta.config.valid())return error.InvalidValue;
            if(beta.soil.len!=count or beta.vapor.len!=count)return error.InvalidShape;
            for(beta.soil)|v|try finiteRange(v,0,1);
            for(beta.vapor,self.vapor)|v,projection|{
                try finiteRange(v,0,std.math.floatMax(f32));
                if(@as(f32,@floatCast(v))!=projection)return error.InvalidValue;
            }
        }
'''+needle,1)
s=s.replace('                    for (cell.cohorts) |cohort| {','''                    for (cell.cohorts) |cohort| {
                        try finiteRange(cohort.root_fraction,0,1);
                        if(self.beta_origin==null and @as(u32,@bitCast(cohort.root_fraction))!=0)return error.IncompatibleSave;''',1)
s=s.replace('for (self.vapor) |v| try finiteRange(v, 0, 1e15);','for (self.vapor) |v| try finiteRange(v, 0, if(self.beta_origin!=null) std.math.floatMax(f32) else 1e15);')
f.write_text(s)
f=p/'save_game.zig';s=f.read_text();s=s.replace('    var origin: ?schema.Origin = null;','''    if(!p.landBeta.enabled)for(p.microbeCells)|cell|{for(cell.cohorts)|c|{if(@as(u32,@bitCast(c.root_fraction))!=0)return error.InvalidValue;}};
    var beta:?schema.BetaOrigin=null;
    var vapor:[]const f32=p.waterVaporMass;
    if(p.landBeta.enabled){
        if(p.worldMode!=.origin or !p.landBeta.valid() or p.landSoil.len!=p.waterMass.len or p.landVapor.len!=p.waterMass.len)return error.InvalidValue;
        const projection=try allocator.alloc(f32,p.landVapor.len);
        for(p.landVapor,projection)|v,*out|{if(!std.math.isFinite(v) or v<0 or v>std.math.floatMax(f32))return error.InvalidValue;out.*=@floatCast(v);}
        vapor=projection;beta=.{.format=.origin_land_beta_v1,.config=p.landBeta,.soil=p.landSoil,.vapor=p.landVapor};
    }
    var origin: ?schema.Origin = null;''')
s=s.replace('.version = schema.VERSION,','.version = if(beta!=null) schema.VERSION else 7, .beta_origin=beta,',1).replace('.vapor = p.waterVaporMass,','.vapor = vapor,',1)
s=s.replace('    // Capacity changes may allocate', '    if(saved.beta_origin!=null)try p.ensureLandBetaStorage();\n    // Capacity changes may allocate',1)
s=s.replace('    p.worldMode = saved.mode;','''    if(saved.beta_origin)|beta|{
        p.landBeta=beta.config;
        @memcpy(p.landSoil,beta.soil);@memcpy(p.landVapor,beta.vapor);@memcpy(p.landNewVapor,beta.vapor);
        @memset(p.landCoefficient,0);@memset(p.landRootH,.{0,0,0,0});
    }else p.resetLandBeta();
    p.worldMode = saved.mode;''',1)
f.write_text(s)
f=p/'save_schema.zig';f.write_text(f.read_text()+'\n'+Path(__file__).with_name('origin-land-beta-save-tests.zig').read_text())
f=p/'save_schema.zig';s=f.read_text();needle='    pub fn validate(self: Save) !void {'
s=s.replace(needle,'''    pub fn jsonStringify(self:Save,writer:anytype)!void {
        if(self.beta_origin==null){try legacyWire(self,writer);return;}
        try writer.beginObject();
        inline for(std.meta.fields(Save))|field|{try writer.objectField(field.name);try writer.write(@field(self,field.name));}
        try writer.endObject();
    }
'''+needle,1);s+='\n'+Path(__file__).with_name('origin-land-beta-wire.zig').read_text();f.write_text(s)
