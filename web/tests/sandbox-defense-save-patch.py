#!/usr/bin/env python3
"""Apply only schema/save changes to the handed-off isolated defense candidate."""
from pathlib import Path
import sys
p=Path(sys.argv[1]);f=p/'save_schema.zig';s=f.read_text();assert 'sandbox_defense:' not in s
s=s.replace('pub const VERSION: u32 = 6;','pub const VERSION: u32 = 7;\npub const CURRENT_ORIGIN_REVISION:u32=5;\npub fn originRevision(version:u32)u32{return if(version>=7) CURRENT_ORIGIN_REVISION else version-1;}')
s=s.replace('VERSION - 1','CURRENT_ORIGIN_REVISION')
s=s.replace('    origin: ?Origin = null,','    origin: ?Origin = null,\n    sandbox_defense: ?@import("simulation/ecology.zig").DefenseConfig = null,')
s=s.replace('origin.model_revision != self.version - 1','origin.model_revision != originRevision(self.version)')
s=s.replace('        const count = 10 *', '''        if(self.version<7 and self.sandbox_defense!=null)return error.IncompatibleSave;
        if(self.sandbox_defense)|cfg|{
            if(self.mode!=.sandbox or !cfg.enabled or !@import("sandbox_defense.zig").validConfig(cfg))return error.InvalidValue;
        }
        const count = 10 *''',1)
s=s.replace('        for (self.plants) |plant| try finiteRange(plant.optimum, 100, 1000);','''        for (self.plants) |plant| {
            try finiteRange(plant.optimum,100,1000);try finiteRange(plant.toughness,0,1);
            if(self.version<7 and plant.toughness!=0)return error.IncompatibleSave;
            if(self.mode==.sandbox and self.sandbox_defense==null and plant.toughness!=0)return error.InvalidValue;
        }''')
s+='''
test "v7 defense strict identity legacy refusal and Origin revision unchanged" {
 var saved=fixture();saved.version=7;try saved.validate();
 var plants=[_]Plant{.{.optimum=302,.toughness=0.5}}**12;saved.plants=&plants;
 try std.testing.expectError(error.InvalidValue,saved.validate());
 saved.sandbox_defense=.{.enabled=true,.law=1,.mutation_law=2,.stream_seed=std.math.maxInt(u64)};try saved.validate();
 const json=try std.json.stringifyAlloc(std.testing.allocator,saved,.{});defer std.testing.allocator.free(json);
 const parsed=try std.json.parseFromSlice(Save,std.testing.allocator,json,.{});defer parsed.deinit();try parsed.value.validate();try std.testing.expectEqualDeep(saved.sandbox_defense,parsed.value.sandbox_defense);
 for(1..7)|version|{saved.version=@intCast(version);try std.testing.expectError(error.IncompatibleSave,saved.validate());saved.sandbox_defense=null;try std.testing.expectError(error.IncompatibleSave,saved.validate());saved.sandbox_defense=.{.enabled=true,.law=1,.mutation_law=2,.stream_seed=0};}
 saved.version=7;saved.sandbox_defense.?.law=2;try std.testing.expectError(error.InvalidValue,saved.validate());saved.sandbox_defense.?.law=1;
 plants[11].toughness=std.math.nan(f32);try std.testing.expectError(error.InvalidValue,saved.validate());plants[11].toughness=0.5;
 try std.testing.expectEqual(@as(u32,5),originRevision(6));try std.testing.expectEqual(@as(u32,5),originRevision(7));
}
''';f.write_text(s)
f=p/'save_game.zig';s=f.read_text().replace('schema.VERSION - 1','schema.CURRENT_ORIGIN_REVISION');s=s.replace('.mode = p.worldMode, .origin = origin,','.mode = p.worldMode, .origin = origin, .sandbox_defense = if(p.worldMode==.sandbox and p.sandboxDefense.enabled) p.sandboxDefense else null,')
s=s.replace('    p.worldMode = saved.mode;','    p.worldMode = saved.mode;\n    p.sandboxDefense=saved.sandbox_defense orelse .{};\n    if(@hasField(@TypeOf(state.*),"defensePlantKind"))state.defensePlantKind=-1;')
f.write_text(s)

f=p/"save_schema.zig";f.write_text(f.read_text()+'\ntest "v7 Origin keeps dormant traits inert and rejects enabled Sandbox configuration" {\n var saved=fixture();saved.version=7;saved.mode=.origin;\n const cohorts=[_]Microbes.Cohort{.{}}**4;const cells=[_]SavedCell{.{.cohorts=&cohorts}}**12;\n saved.origin=.{.model_revision=5,.cells=&cells,.stats=.{}};\n const plants=[_]Plant{.{.toughness=0.5}}**12;saved.plants=&plants;try saved.validate();\n saved.sandbox_defense=.{.enabled=true,.law=1,.mutation_law=2,.stream_seed=0};try std.testing.expectError(error.InvalidValue,saved.validate());\n saved.sandbox_defense=null;saved.origin.?.model_revision=6;try std.testing.expectError(error.IncompatibleSave,saved.validate());\n saved.origin.?.model_revision=5;saved.version=6;try std.testing.expectError(error.IncompatibleSave,saved.validate());\n}\n')
