#!/usr/bin/env python3
"""Actual native session-display toggle gate on unmodified natural Sunlit14 save."""
from pathlib import Path
import subprocess,sys,hashlib,json
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve();subprocess.run([sys.executable,str(r/'web/tests/egl-sunlit-journey-prepare.py'),str(o)],check=True)
p=o/'main.zig';s=p.read_text();a=s.index('          _=pm;_=pw;');b=s.index('\n        std.debug.print("SUNLIT_PUBLIC_PASS',a)
s=s[:a]+r'''
          _=pm;_=pw;state.paused=true;state.showEscapeMenu=false;state.showPointDetails=false;state.showPlanetControl=false;state.selectedPoint=29254;state.selectedTool=.PlaceVegetation;state.watchLifeView=true;
          std.debug.assert(state.fitLivingClusterResult(390,700)==1);state.update(&game,0);render(window);gl.finish();window.swapBuffers();
          const original=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const baseline=try std.json.parseFromSlice(saves.schema.Save,a,original,.{.allocate=.alloc_always});
          std.debug.assert(stella_seed_targets(-1)==1 and state.seedTargets.count>0 and state.visibleSprouts>0);
          const shown=state.seedTargets;const colonies=state.visibleSprouts;
          qa_capture("OUTPUT/shown.ppm");
          std.debug.assert(stella_seed_targets(0)==0 and state.seedTargets.count==0);
          for(shown.items[0..shown.count])|hit|std.debug.assert(state.pickSeedTarget(hit.x,hit.y)==null);
          std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          render(window);gl.finish();window.swapBuffers();qa_capture("OUTPUT/hidden.ppm");
          std.debug.assert(state.seedTargets.count==0 and state.visibleSprouts==colonies);
          std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.assert(stella_seed_targets(1)==1 and state.seedTargets.count==0);
          render(window);gl.finish();window.swapBuffers();qa_capture("OUTPUT/restored.ppm");
          std.debug.assert(state.seedTargets.count==shown.count and state.visibleSprouts==colonies);
          for(shown.items[0..shown.count],state.seedTargets.items[0..state.seedTargets.count])|old,new|{std.debug.assert(std.meta.eql(old,new));std.debug.assert(state.pickSeedTarget(old.x,old.y)==old.cell);}
          std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.assert(stella_seed_targets(2)==-1 and stella_seed_targets(-1)==1);
          // Actual hidden click must re-raycast, not use an intentionally stale snapped selection.
          _=stella_seed_targets(0);const hit=shown.items[0];qa_pointer(hit.x,hit.y,0);
          state.mouseMoved(&game,hit.x,hit.y,0,0);const ray_cell=state.selectedPoint;const ray_on=state.pointerOnPlanet;
          const stale=(ray_cell+1)%state.planet.microbeCells.len;state.selectedPoint=stale;state.pointerOnPlanet=true;
          state.mousePressed(&game,.left);
          std.debug.assert(state.pointerOnPlanet==ray_on);if(ray_on)std.debug.assert(state.selectedPoint==ray_cell);
          std.debug.print("SEED_TARGET_CLICK old_hint={} stale_selection={} actual_ray={} ray_on={} hidden_pick_null={}\n",.{hit.cell,stale,ray_cell,ray_on,state.pickSeedTarget(hit.x,hit.y)==null});
          try saves.apply(state,baseline.value);std.debug.assert(std.mem.eql(u8,original,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.print("SEED_TARGET_PASS shown={} hidden=0 restored={} colonies={} full_save_rng_exact=true immediate_cache_clear=true hidden_actual_click_recasts=true original_restored=true\n",.{shown.count,shown.count,colonies});
        }
''' .replace('OUTPUT',str(o.parent))+s[b:]
s=s.replace('SUNLIT_PUBLIC_PASS','SEED_TARGET_COMPLETE');p.write_text(s)
subprocess.run([sys.executable,str(r/'web/tests/audit-zig-exports.py'),str(r/'src/main.zig'),str(p)],check=True,stdout=(o.parent/'export-audit.json').open('w'))
(o.parent/'toggle-provenance.json').write_text(json.dumps({'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip(),'input_sha256':hashlib.sha256((r.parent/'site-tmp/sunlit14/day-14.json').read_bytes()).hexdigest(),'source':{f:{'production':hashlib.sha256((r/'src'/f).read_bytes()).hexdigest(),'copy':hashlib.sha256((o/f).read_bytes()).hexdigest()}for f in ['main.zig','states/play.zig','simulation/planet.zig','simulation/microbes.zig']}},indent=2)+'\n')
