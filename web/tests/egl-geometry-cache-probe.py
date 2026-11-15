#!/usr/bin/env python3
"""Hypothesis only: exact elevation/tilt detection and retain unchanged terrain vertex block."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1]);subprocess.run([sys.executable,str(root/'web/tests/egl-laptop-render-prepare.py'),str(out),sys.argv[2]],check=True)
p=out/'simulation/planet.zig';s=p.read_text();s=s.replace('    normalComputeJob: ?*Job(void) = null,','    normalComputeJob: ?*Job(void) = null,\n    qa_elevation:?[]f32=null,qa_tilt:u32=0,qa_valid:bool=false,qa_normal_dirty:bool=true,')
n='        const bufData = self.bufData;';i=s.index(n,s.index('    pub fn upload('));s=s[:i]+s[i:].replace(n,'''        const qa_cache=std.posix.getenv("STELLA_GEOMETRY_CACHE")!=null;
        var qa_changed=true;
        if(qa_cache){
            if(self.qa_elevation==null)self.qa_elevation=self.simulationArena.allocator().alloc(f32,self.elevation.len) catch unreachable;
            const prior=self.qa_elevation.?;
            qa_changed=!self.qa_valid or self.qa_tilt!=@as(u32,@bitCast(axialTilt)) or !std.mem.eql(u8,std.mem.sliceAsBytes(prior),std.mem.sliceAsBytes(self.elevation));
            if(qa_changed){@memcpy(prior,self.elevation);self.qa_tilt=@bitCast(axialTilt);self.qa_valid=true;}
        }
'''+n,1)
s=s.replace('                self.normalComputeJob = null;','                self.normalComputeJob = null;self.qa_normal_dirty=true;',1)
s=s.replace('if (self.uploadNo % 10 == 0 and self.normalComputeJob == null)', 'if ((if(qa_cache)qa_changed else self.uploadNo % 10 == 0) and self.normalComputeJob == null)',1)
a=s.index('            const rotationMatrix',s.index('    pub fn upload('));b=s.index('            // This one is special',a);part=s[a:b];part=part.replace('            gl.bindBuffer(gl.ARRAY_BUFFER, self.mesh.vbo);','');s=s[:a]+'''            gl.bindBuffer(gl.ARRAY_BUFFER, self.mesh.vbo);
            if(!qa_cache or qa_changed or self.qa_normal_dirty){
'''+part+'            self.qa_normal_dirty=false;\n            }\n'+s[b:];p.write_text(s)
p=out/'simulation/planet.zig';p.write_text(p.read_text().replace('    fn computeNormal(', '    pub fn computeNormal('))
p=out/'main.zig';s=p.read_text();s='extern fn qa_capture(path:[*:0]const u8) void;\n'+s
needle='  qa_report_draws();const physics=';assert needle in s;s=s.replace(needle,'''  if(std.posix.getenv("STELLA_GEOMETRY_PROOF"))|prefix|{const path=try std.fmt.allocPrintZ(a,"{s}-{s}-{d}.ppm",.{prefix,label,@as(u32,@intFromFloat(speed))});qa_capture(path);const bytes_after=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});var hash:[32]u8=undefined;std.crypto.hash.sha2.Sha256.hash(bytes_after,&hash,.{});std.debug.print("GEOMETRY_SAVE stage={s} speed={d} hash={s}\\n",.{label,speed,std.fmt.fmtSliceHexLower(&hash)});}
'''+needle,1);p.write_text(s)

p=out/'main.zig';s=p.read_text();s=s.replace(' std.debug.print("FRAME_RESTORE stage={s} exact_save=true\\n",.{label});',' std.debug.print("FRAME_RESTORE stage={s} exact_save=true\\n",.{label});\n if(std.posix.getenv("STELLA_GEOMETRY_CASES")!=null)try geometryCases(state,window,allocator,label);');s+=(root/'web/tests/geometry-invalidation.zig.part').read_text();p.write_text(s)
