from pathlib import Path
s=Path('src/experimental/hydration_lifecycle_core.zig').read_text()
old='if(env.depth_km==0 and env.temperature>273.15 and env.temperature<355) std.math.clamp(env.qa_hydration[i],0,1) else @as(f32,0)'
assert s.count(old)==2
s=s.replace(old,'effectiveHydration(env.qa_hydration[i],env.depth_km,env.temperature)')
pos=s.index('fn aquaticSubmergence(')
s=s[:pos]+'''pub fn effectiveHydration(h:f32,depth:f32,temp:f32)f32{
 if(!std.math.isFinite(h) or !std.math.isFinite(depth) or !std.math.isFinite(temp) or depth<0 or temp<=273.15 or temp>=355)return 0;
 return std.math.clamp(h,0,1)*(1-aquaticSubmergence(depth));
}
'''+s[pos:]
Path('src/experimental/hydration_continuous_core.zig').write_text(s)
