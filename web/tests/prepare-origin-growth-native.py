from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/root-growth-normalization';o=b/'native-src';assert not o.exists();shutil.copytree(b/'src',o)
a=r.parent/'site-tmp/origin-land-gate/candidate/src'
for n in ['main.zig','audio.zig','loop.zig','states/play.zig']:shutil.copyfile(a/n,o/n)
p=o/'main.zig';s=p.read_text();needle='    const initial=try std.json.stringifyAlloc';s=s.replace(needle,'''    if(std.posix.getenv("QA_GROWTH_MIGRATE")!=null){std.debug.assert(state.planet.landBeta.physiology_law==3);state.planet.landBeta.physiology_law=4;}
'''+needle,1);s=s.replace('        std.debug.print("LAND_NATIVE beginOrigin_idempotent=true invalid_version_law_atomic=true\\n",.{});','''        invalid=owned.value;invalid.beta_origin.?.config.physiology_law=99;
        if(saves.apply(state,invalid)) |_| unreachable else |_| {}
        std.debug.assert(std.mem.eql(u8,initial,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
        if(state.planet.landBeta.physiology_law==4){invalid=owned.value;invalid.version=10;invalid.beta_origin.?.format=.origin_land_beta_v3;
            if(saves.apply(state,invalid)) |_| unreachable else |_| {}
            std.debug.assert(std.mem.eql(u8,initial,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
        }
        state.planet.landRootH[0][0]=0.123;state.planet.landRootOwner[0][0]=42;try saves.apply(state,owned.value);
        for(state.planet.landRootH)|row|for(row)|v|std.debug.assert(v==0);
        for(state.planet.landRootOwner)|row|for(row)|v|std.debug.assert(v==0);
        std.debug.print("GROWTH_NATIVE invalid_identity_atomic=true receipt_reset=true\\n",.{});''');p.write_text(s)
(b/'native-source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},indent=2)+'\n')
