from pathlib import Path
import json,hashlib
r=Path(__file__).resolve().parents[2];t=r.parent/'site-tmp';source=t/'root-wind-combined/src'
# Pin current model to owner freeze; native main may differ only in QA owner copy.
expected=json.loads((r/'web/tests/continuation-review/combined-wind-save/source-hashes.json').read_text())
expected.update(json.loads((r/'web/tests/continuation-review/root-wind-combined/core-source-hashes.json').read_text()))
for n,h in expected.items():assert hashlib.sha256((source/n).read_bytes()).hexdigest()==h,n
print('capturing owner freeze',len(list(source.rglob('*.zig'))))
qa=(r/'web/tests/wind-bulk-qa.txt').read_text()
qa=qa.replace('const arm=if(pioneer)"pioneer"else "ordinary";', 'const seed_label=std.posix.getenv("QA_SEED") orelse "42";const arm=try std.fmt.allocPrint(a,"{s}-{s}",.{seed_label,if(pioneer)"pioneer"else "ordinary"});')
qa=qa.replace('std.debug.assert(state.planet.windDispersal.enabled);','std.debug.assert(state.planet.windDispersal.enabled==pioneer and state.planet.landBeta.physiology_law==3);')
qa=qa.replace('      A.enabled=false;', '      if(std.posix.getenv("QA_PREFLIGHT")!=null){std.debug.print("PREFLIGHT_ONLY_COMPLETE\\n",.{});std.process.exit(0);}\n      A.enabled=false;')
qa=qa.replace('A.enabled=false;', 'A.enabled=false;@import("simulation/land_journey_audit.zig").enabled=false;').replace('A.enabled=true;', 'A.enabled=true;@import("simulation/land_journey_audit.zig").enabled=true;')
qa=qa.replace('qaWindEmit("TICK_START",', '@import("simulation/land_journey_audit.zig").tick=tick+1;qaWindEmit("TICK_START",')
s=(r/'web/tests/prepare-rooted-player.py').read_text().split('# Reuse frozen observational hooks')[0]
s=s.replace("b=t/'rooted-player'","b=t/'combined-strategy'").replace("src=t/'rooted-founder/src'","src=t/'root-wind-combined/src'").replace("(r/'web/tests/rooted-player-qa.txt').read_text()",'qa')
exec(compile(s,str(r/'web/tests/prepare-rooted-player.py'),'exec'))
p=o/'states/play.zig';v=p.read_text().replace('std.rand.DefaultPrng.init(42)','std.rand.DefaultPrng.init(std.fmt.parseInt(u64,std.posix.getenv("QA_SEED") orelse "42",10) catch unreachable)');needle='.{.water_preset=preset,.land_beta=wetlands,.land_beta_physiology=if(wetlands)3 else 1}';assert needle in v;v=v.replace(needle,'.{.water_preset=preset,.land_beta=true,.land_beta_physiology=3,.combined_wind=std.posix.getenv("QA_PIONEER")!=null}').replace('        var randomPrng =','        _=wetlands;\n        var randomPrng =');p.write_text(v)
p=o/'simulation/planet.zig';v=p.read_text();needle='        const receipt=@import("wind_packet.zig").launchCombined';assert v.count(needle)==1;v=v.replace(needle,'        const qa_source_before=self.microbeCells[index];const qa_target_before=self.microbeCells[route.index];\n'+needle);needle='        if(receipt.arrived){self.propaguleArrivals';v=v.replace(needle,'        @import("wind_audit.zig").endpoints(.{.time=time,.event=event,.from=index,.to=route.index,.area=self.getMeanPointArea(),.before_donor=qa_source_before,.after_donor=self.microbeCells[index],.before_target=qa_target_before,.after_target=self.microbeCells[route.index],.receipt=receipt});\n'+needle);p.write_text(v)
p=o/'simulation/wind_audit.zig';p.write_text(p.read_text().replace('[4096]u8','[32768]u8')+'\npub fn endpoints(v:anytype)void{write("WIND_ENDPOINT",v);}\n')
old=t/'704-growth-trial/src/simulation';p=o/'simulation/land_journey_audit.zig';p.write_text((old/'land_journey_audit.zig').read_text())
p=o/'simulation/microbes.zig';v=p.read_text().replace('fundedHydration(c.*,env,elapsed,i,interval_demand[i])','qaFundedHydration(c.*,env,elapsed,i,interval_demand[i],"mortality")').replace('fundedHydration(c,env,elapsed,i,interval_demand[i])','qaFundedHydration(c,env,elapsed,i,interval_demand[i],"growth")');prior=(old/'microbes.zig').read_text();v+=prior[prior.index('\nfn qaFundedHydration'):].replace('c.lineage==704','c.root_fraction>0');p.write_text(v)
p=o/'simulation/shared_soil.zig';v=p.read_text();line=next(l for l in(old/'shared_soil.zig').read_text().splitlines()if '.emit("ROOT_WATER"'in l);assert v.count(' return out;')==1;v=v.replace(' return out;',line+'\n return out;');p.write_text(v)
(b/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},indent=2))
