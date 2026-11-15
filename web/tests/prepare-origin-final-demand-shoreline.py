from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];tmp=r.parent/'site-tmp';src=tmp/'origin-final-demand/src';prior=tmp/'origin-basal-shoreline/src';b=tmp/'origin-final-demand-shoreline';o=b/'src';assert not o.exists();shutil.copytree(src,o)
for name in ['main.zig','audio.zig','loop.zig','states/play.zig','simulation/land_journey_audit.zig']:shutil.copyfile(prior/name,o/name)
p=o/'main.zig';s=p.read_text().replace(str(prior.parent),str(b)).replace(str(tmp/'origin-basal-native/law2-initial.json'),str(tmp/'origin-final-demand-native/law3-initial.json'));s=s.replace('if(depth_index>=4)', 'if(depth_index!=0 and depth_index!=1 and depth_index!=3)');s=s.replace('    const input=','    if(ablated)return error.UnrequestedAblation;\n    const input=',1)
s=s.replace('      Audit.emit("PATCH",', '      for(state.planet.landRootH)|row|for(row)|v|std.debug.assert(v==0);for(state.planet.landRootOwner)|row|for(row)|v|std.debug.assert(v==0);\n      Audit.emit("PATCH",',1);p.write_text(s)
p=o/'simulation/microbes.zig';s=p.read_text();s=s.replace('    var child=parent.*;', '    const qa_parent=parent.*;const qa_rng=donor.rng;\n    var child=parent.*;',1);line=next(l for l in(prior/'simulation/microbes.zig').read_text().splitlines()if '.emit("BIRTH"'in l);s=s.replace('    stats.next_lineage+=1;stats.births+=1;','    stats.next_lineage+=1;stats.births+=1;\n'+line,1)
s=s.replace('fundedHydration(c.*,env,elapsed,i,interval_demand[i])','qaFundedHydration(c.*,env,elapsed,i,interval_demand[i],"mortality")').replace('fundedHydration(c,env,elapsed,i,interval_demand[i])','qaFundedHydration(c,env,elapsed,i,interval_demand[i],"growth")')
s+='''
fn qaFundedHydration(c:Cohort,env:Environment,dt:f32,slot:usize,entry:f64,stage:[]const u8)f32{
 const h=fundedHydration(c,env,dt,slot,entry);
 if(c.lineage==524)@import("land_journey_audit.zig").emit("USED_H",.{.tick=@import("land_journey_audit.zig").tick,.stage=stage,.lineage=c.lineage,.owner=env.root_owner[slot],.slot=slot,.credit=env.root_credit[slot],.entry_demand=entry,.current_demand=rootDemand(c,env,dt),.denominator=@max(entry,rootDemand(c,env,dt)),.h=h,.effective_h=effectiveHydration(h,env.depth_km,env.temperature),.cohort=c,.depth_km=env.depth_km,.light=env.light,.temperature=env.temperature});
 return h;
}
''';p.write_text(s)
p=o/'simulation/shared_soil.zig';s=p.read_text();line=next(l for l in(prior/'simulation/shared_soil.zig').read_text().splitlines()if '.emit("ROOT_WATER"'in l);s=s.replace(' return out;',line+'\n return out;',1);p.write_text(s)
a=json.loads((tmp/'origin-land-day30/day-30.json').read_text());v=json.loads((tmp/'origin-final-demand-native/law3-initial.json').read_text());a['version']=10;a['beta_origin']['format']='origin_land_beta_v3';a['beta_origin']['config']['physiology_law']=3;assert a==v
(b/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},indent=2));(b/'migration-proof.json').write_text(json.dumps({'identity_only':True,'input_sha256':hashlib.sha256((tmp/'origin-final-demand-native/law3-initial.json').read_bytes()).hexdigest(),'source':'012cd08'}))
