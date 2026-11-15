#!/usr/bin/env python3
"""Isolated current-engine one-binary shader branch experiment; no production edits."""
from pathlib import Path
import shutil,sys,subprocess
root=Path(__file__).resolve().parents[2];source=Path(sys.argv[1]);out=Path(sys.argv[2]);shutil.copytree(source,out,dirs_exist_ok=True)
p=out/'shaders/terrain.fs';s=p.read_text();a=s.index('            float height =');b=s.index('            // Depth is km:',a);initial=s[a:b];s=s[:a]+s[b:]
a=s.index('            vec3 mapColor = mix(land, water, wet);');s=s[:a]+s[a:].replace('            vec3 mapColor = mix(land, water, wet);','            vec3 mapColor;',1)
old='''            mapColor = mix(mapColor, vec3(0.80, 0.90, 0.96), ice);
            float relief = 0.72 + 0.28 * max(dot(normalize(worldNormal), lightDir), 0.0);
            mapColor *= relief;
''';assert old in s;s=s.replace(old,'',1)
needle='''            }
            float ringDistance''';assert needle in s;s=s.replace(needle,'''            } else {
'''+initial+'''                mapColor = mix(land, water, wet);
                mapColor = mix(mapColor, vec3(0.80, 0.90, 0.96), ice);
                float relief = 0.72 + 0.28 * max(dot(normalize(worldNormal), lightDir), 0.0);
                mapColor *= relief;
            }
            float ringDistance''',1)
(out/'shaders/terrain-branch.fs').write_text(s)
p=out/'renderer.zig';s=p.read_text();needle='try fragmentShader.setSource(@embedFile("shaders/" ++ name ++ ".fs"));';assert needle in s;s=s.replace(needle,'try fragmentShader.setSource(if (comptime std.mem.eql(u8,name,"terrain")) (if(std.posix.getenv("STELLA_TERRAIN_BRANCH")!=null) @embedFile("shaders/terrain-branch.fs") else @embedFile("shaders/terrain.fs")) else @embedFile("shaders/" ++ name ++ ".fs"));',1);p.write_text(s)
p=out/'main.zig';s=p.read_text();s='extern fn qa_capture(path:[*:0]const u8) void;\n'+s;s=s.replace('for([_]f32{86400})|speed|','for([_]f32{0,21600,86400})|speed|',1)
s=s.replace('"{s}-{s}.json",.{prefix,label}','"{s}-{s}-{d}.json",.{prefix,label,@as(u32,@intFromFloat(speed))}',1)
needle='      try profileFrames("loaded",state,window,allocator);';assert needle in s;s=s.replace(needle,'''      if(std.posix.getenv("STELLA_SHADER_PROOF"))|prefix|{
       state.paused=true;
       const before=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
       for(0..5)|mode|{
        state.displayMode=@enumFromInt(mode);
        for(0..3)|_|{render(window);gl.finish();window.swapBuffers();}
        const image_path=try std.fmt.allocPrintZ(a,"{s}-mode{d}.ppm",.{prefix,mode});qa_capture(image_path);
       }
       state.displayMode=.Normal;
       const after=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
       std.debug.assert(std.mem.eql(u8,before,after));
       std.debug.print("SHADER_RENDER_OBSERVATIONAL exact_save=true modes=5\\n",.{});
      }
'''+needle,1);p.write_text(s)
p=out/'shader-shim.c';s=(root/'web/tests/egl-propagule-visual-shim.c').read_text().replace('h=700;width=w;','h=atoi(getenv("STELLA_ORIGIN_HEIGHT")?getenv("STELLA_ORIGIN_HEIGHT"):"700");width=w;');p.write_text(s)
