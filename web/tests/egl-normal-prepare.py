from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-bio-visual-prepare.py'),str(out)],check=True)
p=out/'states/play.zig';s=p.read_text().replace('if (std.posix.getenv("STELLA_VISUAL_BASELINE") == null) .{ .data = biology_visuals.groundedRabbit','if (true) .{ .data = biology_visuals.groundedRabbit');s=s.replace('        if (std.posix.getenv("STELLA_VISUAL_BASELINE") != null) return;','');p.write_text(s)
p=out/'renderer.zig';s=p.read_text().replace('try ShaderProgram.createFromName("entity")','if(std.posix.getenv("STELLA_VISUAL_BASELINE") != null) try ShaderProgram.loadFromPath("src/shaders/entity-before") else try ShaderProgram.loadFromPath("src/shaders/entity")');p.write_text(s)
p=out/'main.zig';s=p.read_text().replace('point.length()+100','point.length()+35');p.write_text(s)
