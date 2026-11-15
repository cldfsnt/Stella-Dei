from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/wetlands-day21';o=b/'src';src=r.parent/'site-tmp/growth-form-native/src';assert not o.exists();shutil.copytree(src,o)
# This is the final v74 preview UI adapter; all model files must still match prior release physics.
old=json.loads((r/'web/tests/continuation-review/wetlands-preview/native/provenance.json').read_text())['owner_sources']
for p in (o/'simulation').rglob('*.zig'):
 name=str(p.relative_to(o));assert hashlib.sha256(p.read_bytes()).hexdigest()==old[name],name
shutil.copyfile(r.parent/'site-tmp/wetlands-journey/src/simulation/wetlands_audit.zig',o/'simulation/wetlands_audit.zig')
for name in ['planet.zig','microbes.zig']:
 p=o/'simulation'/name;s=p.read_text();prior=(r.parent/'site-tmp/wetlands-journey/src/simulation'/name).read_text()
 if name=='planet.zig':
  needle='            const flux = Microbes.step(cell, env, dt);';s=s.replace(needle,'            const qa=@import("wetlands_audit.zig");if(qa.enabled)for(env.root_credit)|credit|{qa.credits+=credit;};\n'+needle)
 else:
  needle='    return @import("final_demand.zig").signal(env.root_credit[slot],env.root_owner[slot],c.lineage,@max(entry_demand,current));';a=prior.index('    const h=@import("final_demand.zig").signal');e=prior.index('\n}',a);s=s.replace(needle,prior[a:e])
 assert s==prior,name+' instrumentation differs';p.write_text(s)
s=(r/'web/tests/wetlands-journey-qa.txt').read_text();a=s.index('    if(!resumed){');e=s.index('    const Location=',a)
s=s[:a]+'''    const input=if(resumed)"OUTPUT/day-14.json"else "DAY7";const bytes=try std.fs.cwd().readFileAlloc(a,input,128*1024*1024);const parsed=try saves.schema.parse(a,bytes);try saves.apply(state,parsed.value);std.debug.assert(std.mem.eql(u8,bytes,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
'''+s[e:]
s=s.replace('for(if(resumed)@as(usize,180)else 0..420)','for(if(resumed)@as(usize,840)else 420..1260)').replace('(tick+1)==180 or (tick+1)==420','(tick+1)==840 or (tick+1)==1260').replace('.root_credit=A.credits,','.grazed_carbon=state.planet.microbeStats.grazed_carbon,.grazing_respired_carbon=state.planet.microbeStats.grazing_respired_carbon,.fixed_carbon=state.planet.microbeStats.fixed_carbon,.recycled_carbon=state.planet.microbeStats.recycled_carbon,.root_credit=A.credits,')
a=s.index('    if(!resumed){loop.pump');e=s.index('    std.debug.print("WETLANDS_JOURNEY_COMPLETE',a)
s=s[:a]+'''    if(!resumed){
      const before=try saves.capture(a,state);const exact=try std.json.stringifyAlloc(a,before,.{});var root_id:u64=std.math.maxInt(u64);var feed_id:u64=std.math.maxInt(u64);var root_cell:usize=0;var feed_cell:usize=0;var root_form:u32=0;var feed_form:u32=0;
      for(state.planet.microbeCells,0..)|cell,i|for(cell.cohorts)|c|{if(c.biomass<=0)continue;if(c.root_fraction>0 and c.support_mass>0 and c.lineage<root_id){root_id=c.lineage;root_cell=i;root_form=@intFromEnum(M.producerForm(c));}if(c.lifetime_grazed>0 and c.lineage<feed_id){feed_id=c.lineage;feed_cell=i;feed_form=@intFromEnum(M.producerForm(c));}};
      if(root_id!=std.math.maxInt(u64) or feed_id!=std.math.maxInt(u64)){
        const rooted=root_id!=std.math.maxInt(u64);const point=if(rooted)root_cell else feed_cell;const requested_id=if(rooted)root_id else feed_id;const form=if(rooted)root_form else feed_form;state.targetCameraPos=state.planet.transformedPoints[point].norm();const result=stella_visit_growth_form(PerformanceDetails.world_serial,form);std.debug.print("DAY21_VISIT criterion_rooted={} candidate_cell={} candidate_id={} form={} result={} actual_cell={} actual_id={}\\n",.{rooted,point,requested_id,form,result,state.selectedPoint,state.colonyPeek.focused});
        if(result==1){state.cameraPos=state.targetCameraPos.norm().scale(state.targetCameraDistance);state.cameraDistance=state.targetCameraDistance;loop.pump(4096);render(window);gl.finish();window.swapBuffers();qa_capture("OUTPUT/day-21-visit.ppm");try std.fs.cwd().writeFile(.{.sub_path="OUTPUT/day-21-life.json",.data=std.mem.span(stella_life_snapshot())});qa_pointer(100,676,1);render(window);qa_pointer(100,676,0);render(window);std.debug.assert(state.showPointDetails);gl.finish();window.swapBuffers();qa_capture("OUTPUT/day-21-details.ppm");}
      }else{std.debug.print("DAY21_VISIT no_supported_root_or_recorded_feeding=true\\n",.{});loop.pump(4096);render(window);gl.finish();window.swapBuffers();qa_capture("OUTPUT/day-21-none.ppm");}
      var after=try saves.capture(a,state);after.camera=before.camera;after.camera_target=before.camera_target;after.camera_distance=before.camera_distance;after.target_distance=before.target_distance;std.debug.assert(std.mem.eql(u8,exact,try std.json.stringifyAlloc(a,after,.{})));
    }
'''+s[e:]
s=s.replace('if(resumed)@as(usize,240)else 420','if(resumed)@as(usize,420)else 840')
(r/'web/tests/wetlands-day21-qa.txt').write_text(s)
p=o/'main.zig';main=p.read_text();a=main.index('    const saves=@import("save_game.zig");const M=');e=main.index('\nconst expect =',a);main=main[:a]+s.replace('OUTPUT',str(b)).replace('DAY7',str(r.parent/'site-tmp/wetlands-journey/day-7.json'))+main[e:];p.write_text(main)
(b/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},indent=2))
