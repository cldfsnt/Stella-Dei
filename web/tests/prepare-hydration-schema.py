"""Isolated proposed v7 schema; never mutates production or a stored save."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[2]
schema=root/'src/save_schema.zig'; core=root/'src/experimental/hydration_lifecycle_core.zig'
s= schema.read_text()
c=core.read_text()
(root/'src/experimental/hydration_schema_types.zig').write_text('// Frozen lifecycle types/functions for schema QA only. Not production.\n'+c)
s=s.replace('pub const VERSION: u32 = 6;', 'pub const VERSION: u32 = 7;')
s=s.replace('@import("simulation/microbes.zig")','@import("hydration_schema_types.zig")').replace('@import("simulation/ecology.zig")','@import("../simulation/ecology.zig")')
s=s.replace('    nutrient: f32 = 0.02,','    liquid_return: f64 = 0,\n    vapor_return: f64 = 0,\n    nutrient: f32 = 0.02,',1)
s=s.replace('.nutrient = cell.nutrient,', '.liquid_return = cell.liquid_return, .vapor_return = cell.vapor_return, .nutrient = cell.nutrient,')
s=s.replace('.nutrient = self.nutrient,', '.liquid_return = self.liquid_return, .vapor_return = self.vapor_return, .nutrient = self.nutrient,')
s=s.replace('        try writer.objectField("nutrient");','''        if (self.liquid_return != 0) {
            try writer.objectField("liquid_return");
            try writer.write(self.liquid_return);
        }
        if (self.vapor_return != 0) {
            try writer.objectField("vapor_return");
            try writer.write(self.vapor_return);
        }
        try writer.objectField("nutrient");''',1)
s=s.replace('                    const cell = saved_cell.runtime();','''                    if (self.version < 7 and (saved_cell.liquid_return != 0 or saved_cell.vapor_return != 0)) return error.IncompatibleSave;
                    try finiteRange(saved_cell.liquid_return, 0, 1e30);
                    try finiteRange(saved_cell.vapor_return, 0, 1e30);
                    const cell = saved_cell.runtime();''',1)
s=s.replace('                        if (self.version == 2 and cohort.structure', '''                        if (self.version < 7 and (cohort.retention_allocation != 0 or cohort.stored_water != 0)) return error.IncompatibleSave;
                        try finiteRange(cohort.retention_allocation, 0, 1);
                        try finiteRange(cohort.stored_water, 0, Microbes.waterCapacity(cohort));
                        if (self.version == 2 and cohort.structure''',1)
s='//! EXPERIMENTAL v7 schema QA only; no real-save writes or production imports.\n'+s+'\n'+(root/'web/tests/hydration-schema-tests.zig.part').read_text()
(root/'src/experimental/hydration_save_schema.zig').write_text(s)
(root/'src/qa_hydration_schema.zig').write_text('test { _ = @import("experimental/hydration_save_schema.zig"); }\n')
p=root/'web/tests/continuation-review/hydration-schema';p.mkdir(parents=True,exist_ok=True)
(p/'provenance.json').write_text(json.dumps({str(x.relative_to(root)):hashlib.sha256(x.read_bytes()).hexdigest() for x in [schema,core,root/'src/experimental/hydration_schema_types.zig',root/'src/experimental/hydration_save_schema.zig',Path(__file__),root/'web/tests/hydration-schema-tests.zig.part']},indent=2)+'\n')
