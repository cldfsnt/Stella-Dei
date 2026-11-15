#!/usr/bin/env python3
"""Fixed full-scheduler reciprocal mosaic; isolated copied source only."""
from pathlib import Path
import sys,subprocess,shutil,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve();baseline='--baseline' in sys.argv
subprocess.run([sys.executable,str(r/'web/tests/egl-foraging-production-prepare.py'),str(o)],check=True)
if not baseline:
 frozen=r.parent/'site-tmp/sandbox-toughness/candidate/src'
 for f in ['simulation/ecology.zig','simulation/foraging.zig','simulation/planet.zig','simulation/life.zig']:
  shutil.copy2(frozen/f,o/f)
 shutil.copy2(r/'web/tests/sandbox-toughness-save.zig',o/'toughness_save.zig')
 p=o/'simulation/planet.zig';s=p.read_text().replace('self.plantTraits[i] = child;', '''std.debug.print("MOSAIC_COLONIZE destination={} source={} vacant={} old_d={d} new_d={d} old_cover={d} time={d}\\n",.{i,n,cover<0.0001,self.plantTraits[i].toughness,child.toughness,cover,options.gameTime});
                        self.plantTraits[i] = child;''');p.write_text(s)
 p=o/'simulation/life.zig';s=p.read_text().replace('pub var qa_removed:f64=0;','pub var qa_patch:[]f64=&.{};pub var qa_removed:f64=0;').replace('qa_removed+=bite.eaten;','qa_removed+=bite.eaten;if(idx<qa_patch.len)qa_patch[idx]+=bite.eaten;');p.write_text(s)
p=o/'main.zig';s=p.read_text();a=s.index('          _=pm;_=pw;');b=s.index('\n        std.debug.print("FORAGING_PRODUCTION_COMPLETE',a)
common=r'''
          _=pm;_=pw;std.debug.assert(state.planet.worldMode==.sandbox);
          const original=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const initial=try std.json.parseFromSlice(saves.schema.Save,a,original,.{.allocate=.alloc_always});
          for(0..10)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
          try std.fs.cwd().writeFile(.{.sub_path="OUTPUT/off-ten.json",.data=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})});
          try saves.apply(state,initial.value);
'''
body=r'''
          const TS=@import("toughness_save.zig");const Life=@import("simulation/life.zig");
          try TS.applyLegacy(state,initial.value);
          const n=state.planet.vegetation.len;const ranked=try a.alloc(usize,n);var nr:usize=0;
          for(state.planet.vegetation,0..)|v,i|if(v>0){ranked[nr]=i;nr+=1;};
          std.mem.sort(usize,ranked[0..nr],state.planet.vegetation,struct{fn less(v:[]f32,l:usize,rr:usize)bool{return v[l]>v[rr] or (v[l]==v[rr] and l<rr);}}.less);
          Life.qa_patch=try a.alloc(f64,n);
          const previous=try a.alloc(f32,n);
          for(0..if(std.posix.getenv("QA_MOSAIC_RUN")!=null) @as(usize,4) else @as(usize,0))|arm|{
            try TS.applyLegacy(state,initial.value);
            for(state.planet.plantTraits)|*trait|trait.toughness=0;
            for(0..nr/2)|pair|{const reverse=(pair+arm%2)%2;state.planet.plantTraits[ranked[pair*2+reverse]].toughness=0.5;}
            if(arm>=2)state.planet.lifeforms.clearRetainingCapacity();
            Life.qa_removed=0;Life.qa_credit=0;Life.qa_error=0;@memset(Life.qa_patch,0);
            const stocked=state.planet.lifeforms.items.len;const births0=state.planet.rabbitBirths;const deaths0=state.planet.rabbitDeaths;
            const before=try std.json.stringifyAlloc(a,try TS.capture(a,state),.{});
            try std.fs.cwd().writeFile(.{.sub_path=try std.fmt.allocPrint(a,"OUTPUT/arm-{}-start.json",.{arm}),.data=before});
            const owned=try std.json.parseFromSlice(TS.Envelope,a,before,.{.allocate=.alloc_always});
            // All refusal checks precede biological outcomes and compare complete saved state.
            var invalid=owned.value;invalid.law=255;
            if(TS.apply(state,invalid)) |_| return error.InvalidLawAccepted else |_| {}
            invalid=owned.value;invalid.mutation_enabled=true;
            if(TS.apply(state,invalid)) |_| return error.MutationAccepted else |_| {}
            invalid=owned.value;invalid.state.mode=.origin;
            if(TS.apply(state,invalid)) |_| return error.OriginAccepted else |_| {}
            var empty:usize=0;while(state.planet.vegetation[empty]>0):(empty+=1){}
            const old=owned.value.state.plants[empty].toughness;
            @constCast(owned.value.state.plants)[empty].toughness=std.math.nan(f32);
            if(TS.apply(state,owned.value)) |_| return error.InvalidTraitAccepted else |_| {}
            @constCast(owned.value.state.plants)[empty].toughness=1.01;
            if(TS.apply(state,owned.value)) |_| return error.RangeAccepted else |_| {}
            @constCast(owned.value.state.plants)[empty].toughness=old;
            if(TS.applyLegacy(state,owned.value.state)) |_| return error.DisguisedLegacyAccepted else |_| {}
            std.debug.assert(std.mem.eql(u8,before,try std.json.stringifyAlloc(a,try TS.capture(a,state),.{})));
            // Empty-cell genotype is owned state, not omitted because cover is zero.
            @constCast(owned.value.state.plants)[empty].toughness=0.25;try TS.apply(state,owned.value);
            std.debug.assert((try TS.capture(a,state)).state.plants[empty].toughness==0.25);
            @constCast(owned.value.state.plants)[empty].toughness=old;try TS.apply(state,owned.value);
            std.debug.assert(std.mem.eql(u8,before,try std.json.stringifyAlloc(a,try TS.capture(a,state),.{})));
            std.debug.print("MOSAIC_GATES arm={} invalid_atomic=true empty_trait_roundtrip=true\n",.{arm});
            var extinct:usize=0;var colonized:usize=0;var peak=stocked;
            for(0..7)|day|{
              @memset(Life.qa_patch,0);
              for(0..60)|_|{
                @memcpy(previous,state.planet.vegetation);
                loop.pump(16);state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;loop.pump(16);
                for(previous,state.planet.vegetation)|oldcover,v|{if(oldcover>0 and v==0)extinct+=1;if(oldcover==0 and v>0)colonized+=1;}
                peak=@max(peak,state.planet.lifeforms.items.len);
                std.debug.assert(stocked+state.planet.rabbitBirths-births0-(state.planet.rabbitDeaths-deaths0)==state.planet.lifeforms.items.len);
              }
              var cover=[_]f64{0,0};var count=[_]usize{0,0};
              for(state.planet.vegetation,state.planet.plantTraits,0..)|v,t,i|{
                std.debug.assert(t.toughness==0 or t.toughness==0.5);const k:usize=if(t.toughness==0)0 else 1;cover[k]+=v;if(v>0)count[k]+=1;
                if(v>0 or Life.qa_patch[i]>0)std.debug.print("MOSAIC_PATCH {s}\n",.{try std.json.stringifyAlloc(a,.{.arm=arm,.day=day+1,.patch=i,.cover=v,.toughness=t.toughness,.generation=t.generation,.temperature=state.planet.temperature[i],.depth_m=state.planet.waterMass[i]*state.planet.getKmPerWaterMass()*1000,.grazed=Life.qa_patch[i]},.{})});
              }
              std.debug.print("MOSAIC_DAY {s}\n",.{try std.json.stringifyAlloc(a,.{.arm=arm,.day=day+1,.cover=cover,.patches=count,.rabbits=state.planet.lifeforms.items.len,.peak=peak,.births=state.planet.rabbitBirths-births0,.deaths=state.planet.rabbitDeaths-deaths0,.extinctions=extinct,.colonizations=colonized,.removed=Life.qa_removed,.credit=Life.qa_credit,.credit_error=Life.qa_error},.{})});
            }
            const endpoint_bytes=try std.json.stringifyAlloc(a,try TS.capture(a,state),.{});
            try std.fs.cwd().writeFile(.{.sub_path=try std.fmt.allocPrint(a,"OUTPUT/arm-{}-end.json",.{arm}),.data=endpoint_bytes});
            const endpoint=try std.json.parseFromSlice(TS.Envelope,a,endpoint_bytes,.{.allocate=.alloc_always});
            for(0..10)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
            const uninterrupted=try std.json.stringifyAlloc(a,try TS.capture(a,state),.{});
            try TS.applyLegacy(state,initial.value);state.axialTilt=45;state.planet.elevation[436]+=0.01;render(window);gl.finish();window.swapBuffers();
            try TS.apply(state,endpoint.value);
            std.debug.assert(std.mem.eql(u8,endpoint_bytes,try std.json.stringifyAlloc(a,try TS.capture(a,state),.{})));
            for(0..10)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
            std.debug.assert(std.mem.eql(u8,uninterrupted,try std.json.stringifyAlloc(a,try TS.capture(a,state),.{})));
            std.debug.print("MOSAIC_PASS arm={} exact_full_traits_reload=true true_continuation=true\n",.{arm});
          }
          try TS.applyLegacy(state,initial.value);
          std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.print("MOSAIC_ORIGINAL_RESTORED\n",.{});
'''
s=s[:a]+(common+('' if baseline else body)).replace('OUTPUT',str(o.parent))+'\n        }\n'+s[b:];p.write_text(s)
subprocess.run([sys.executable,str(r/'web/tests/audit-zig-exports.py'),str(r/'src/main.zig'),str(p)],check=True,stdout=(o.parent/'export-audit.json').open('w'))
(o.parent/'source-hashes.json').write_text(json.dumps({str(f.relative_to(o)):hashlib.sha256(f.read_bytes()).hexdigest()for f in o.rglob('*.zig')},indent=2)+'\n')
