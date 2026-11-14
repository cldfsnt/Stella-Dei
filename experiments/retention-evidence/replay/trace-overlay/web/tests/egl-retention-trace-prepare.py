from pathlib import Path
import sys,subprocess
here=Path(__file__).resolve().parent;out=Path(sys.argv[1]);subprocess.run([sys.executable,str(here/'egl-continents-prepare.py'),str(out)],check=True)
p=out/'simulation/planet.zig';s=p.read_text();needle='        for (self.microbeCells, 0..) |*cell, i| {';a=s.index('    pub fn simulateMicrobes');pos=s.index(needle,a)
s=s[:pos]+'''        for([_]usize{35503,6787,30111})|index|{
            const light=@max(0,self.transformedPoints[index].norm().dot(options.solarVector))*std.math.clamp(options.solarConstant/1361,0,2);
            const e=self.microbeEnvironment(index,light);
            std.debug.print("RETENTION_TRACE,{d},{d},{d},{d},{d},{d},{d},{d}\\n",.{options.gameTime,index,dt,e.temperature,e.depth_km,e.light,e.carbon_available,e.oxygen_carbon_capacity});
        }
'''+s[pos:];p.write_text(s)
