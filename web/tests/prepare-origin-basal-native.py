from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];base=r.parent/'site-tmp/origin-basal-native';src=r.parent/'site-tmp/origin-basal/src';o=base/'src';assert not o.exists();shutil.copytree(src,o)
# Reuse already-verified deterministic, cooperative EGL restore harness only.
old=r.parent/'site-tmp/origin-land-gate/candidate/src'
for name in ['main.zig','audio.zig','loop.zig','states/play.zig']:shutil.copyfile(old/name,o/name)
p=o/'main.zig';s=p.read_text();needle='    const initial=try std.json.stringifyAlloc'
s=s.replace(needle,'''    // Explicit QA-only migration, never a public enable action or automatic load.
    if(std.posix.getenv("QA_BASAL_MIGRATE")!=null){std.debug.assert(state.planet.landBeta.enabled and state.planet.landBeta.physiology_law==1);state.planet.landBeta.physiology_law=2;}
'''+needle,1)
s=s.replace('        std.debug.print("LAND_NATIVE beginOrigin_idempotent=true invalid_version_law_atomic=true\\n",.{});','''        invalid=owned.value;invalid.beta_origin.?.config.physiology_law=99;
        if(saves.apply(state,invalid)) |_| unreachable else |_| {}
        std.debug.assert(std.mem.eql(u8,initial,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
        if(state.planet.landBeta.physiology_law==2){invalid=owned.value;invalid.version=8;invalid.beta_origin.?.format=.origin_land_beta_v1;
            if(saves.apply(state,invalid)) |_| unreachable else |_| {}
            std.debug.assert(std.mem.eql(u8,initial,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
        }
        std.debug.print("LAND_NATIVE beginOrigin_idempotent=true invalid_version_law_atomic=true physiology_atomic=true\\n",.{});''')
s=s.replace('    const ending=try std.json.stringifyAlloc','''    if(state.planet.landBeta.enabled and state.planet.landBeta.physiology_law==2 and ticks>0){
        const M=@import("simulation/microbes.zig");const Soil=@import("simulation/shared_soil.zig");std.debug.assert(M.qa_immersion_steps>0 and Soil.qa_basal_demands>0);
        std.debug.print("BASAL_ROUTE actual_physiology={} actual_root_demand_evaluations={}\\n",.{M.qa_immersion_steps,Soil.qa_basal_demands});
    }
    const ending=try std.json.stringifyAlloc''',1);p.write_text(s)
p=o/'simulation/microbes.zig';s=p.read_text();s+='\npub var qa_immersion_steps:u64=0;\n';s=s.replace('    const days=elapsed/86400;','    if(env.immersion_physiology)qa_immersion_steps+=1;\n    const days=elapsed/86400;',1);p.write_text(s)
p=o/'simulation/shared_soil.zig';s=p.read_text();s+='\npub var qa_basal_demands:u64=0;\n';s=s.replace('  const height=@as(f64,M.producerHeightMeters(c));','  if(env.immersion_physiology)qa_basal_demands+=1;\n  const height=@as(f64,M.producerHeightMeters(c));');p.write_text(s)
(base/'source-sha256.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest() for p in o.rglob('*.zig')},indent=2)+'\n');print(base)
