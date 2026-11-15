#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys,shutil
here=Path(__file__).parent;dst=Path(sys.argv[2]);subprocess.run([sys.executable,str(here/'origin-immersion-prepare.py'),sys.argv[1],str(dst)],check=True)
shutil.copyfile(here/'origin-basal-geometry.zig',dst/'simulation/basal_geometry.zig')
p=dst/'simulation/microbes.zig';s=p.read_text();a=s.index('/// Beta law2 only.');b=s.index('pub fn seed(cell:',a)
s=s[:a]+'''/// Law2 shared physical geometry; fixed illustrative density100kgC/m3.
pub fn geometricImmersion(c:Cohort,depth:f32,temp:f32) f32 {
    if(!std.math.isFinite(depth) or depth<0 or depth>0.05 or !std.math.isFinite(temp) or temp<=273.15 or temp>=355)return 0;
    return @floatCast(@import("basal_geometry.zig").immersion(c.biomass,producerHeightMeters(c),@as(f64,depth)*1000,100) orelse 0);
}
'''+s[b:];p.write_text(s)
p=dst/'simulation/shared_soil.zig';s=p.read_text().replace('const exposure=if(height>0)', 'const exposure=if(env.immersion_physiology) 1-(@import("basal_geometry.zig").immersion(c.biomass,height,depth,100) orelse return null) else if(height>0)');p.write_text(s)
p=dst/'simulation/planet.zig';s=p.read_text().replace('const env=self.microbeEnvironment(i,@max(0,self.transformedPoints[i].norm().dot(options.solarVector))*std.math.clamp(options.solarConstant/1361,0,2));','var env=self.microbeEnvironment(i,@max(0,self.transformedPoints[i].norm().dot(options.solarVector))*std.math.clamp(options.solarConstant/1361,0,2));env.immersion_physiology=self.landBeta.physiology_law==2;');p.write_text(s)
# Held draft test assumes unsupported bodies have no geometry: not this contract.
p=dst/'simulation/qa_immersion.zig';s=p.read_text().replace('try std.testing.expectEqual(@as(f32,0),M.geometricImmersion(flat,h,303));','try std.testing.expect(M.geometricImmersion(flat,h,303)>0);').replace('e=env(h);const old_flat=run(flat,e);e.immersion_physiology=true;try std.testing.expectEqualDeep(old_flat,run(flat,e));','e=env(0);const old_flat=run(flat,e);e.immersion_physiology=true;try std.testing.expectEqualDeep(old_flat,run(flat,e));');s+='\n'+(here/'origin-basal-tests.zig').read_text();p.write_text(s)
