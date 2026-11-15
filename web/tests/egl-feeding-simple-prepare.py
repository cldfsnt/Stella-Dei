#!/usr/bin/env python3
"""Attribute v58 marker cost separately from selection; isolated polygon candidate."""
from pathlib import Path
import subprocess,sys
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(r/'web/tests/egl-feeding-regression-prepare.py'),str(o)],check=True)
p=o/'states/play.zig';s=p.read_text();s='pub var qa_marker_mode:u8=1;\n'+s
needle='''                {
                    const history=@import("../feeding_marker.zig").classify(self.planet.microbeCells[index].cohorts);'''
replacement='''                if(qa_marker_mode==2){
                    if(biology_visuals.hasFed(self.planet.microbeCells[index].cohorts)){
                        vg.beginPath();vg.fillColor(nvg.rgb(255,191,89));vg.circle(12,0,3);vg.fill();
                    }
                }else{
                    const history=@import("../feeding_marker.zig").classify(self.planet.microbeCells[index].cohorts);'''
assert s.count(needle)==1;s=s.replace(needle,replacement)
a=s.index('                        vg.beginPath();vg.fillColor(nvg.rgba(247,177,65,235))');b=s.index('                    }else if(history==.mixed)',a)
old=s[a:b]
simple='''                        vg.beginPath();vg.fillColor(nvg.rgb(247,177,65));vg.strokeColor(nvg.rgb(66,38,12));vg.strokeWidth(1.7);
                        vg.moveTo(-13,0);vg.lineTo(-8,-2);vg.lineTo(-4,1);vg.lineTo(0,-1);vg.lineTo(4,1);vg.lineTo(8,-2);vg.lineTo(13,0);vg.lineTo(10,5);vg.lineTo(4,5);vg.lineTo(0,7);vg.lineTo(-4,5);vg.lineTo(-10,5);vg.closePath();vg.fill();vg.stroke();
'''
s=s[:a]+'                        if(qa_marker_mode==3){\n'+simple+'                        }else{\n'+old+'                        }\n'+s[b:];p.write_text(s)
p=o/'main.zig';s=p.read_text();s=s.replace('for([_]bool{false,true,true,false,false,true},0..)|candidate,arm|{','for([_]u8{0,1,2,3,3,2,1,0,0,2,1,3},0..)|mode,arm|{\n              const candidate=mode!=0;play.qa_marker_mode=mode;',1)
s=s.replace('candidate={} frames=120 ns={d} glyphs={d}','candidate={} mode={d} frames=120 ns={d} glyphs={d}',1).replace('candidate,elapsed,state.colonyTargets.count','candidate,mode,elapsed,state.colonyTargets.count',1)
s=s.replace('"{s}-{s}-{s}.png",.{prefix,@tagName(kind),if(candidate)"candidate" else "baseline"}','"{s}-{s}-mode{d}.png",.{prefix,@tagName(kind),mode}',1);p.write_text(s)
