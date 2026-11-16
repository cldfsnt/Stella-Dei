from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];t=r.parent/'site-tmp';o=t/'heritable-inactivity';assert not (o/'src').exists();shutil.copytree(t/'protective-inactivity/src',o/'src')
p=o/'src/simulation/microbes.zig';s=p.read_text();s=s.replace('pub const Cohort=struct {','pub var qa_activity_law:bool=false;\npub fn isInactive(c:Cohort)bool{return qa_activity_law and c.inactive;}\npub const Cohort=struct {\n    protective_investment:f32=0, recovery_seconds:f32=0,')
s=s.replace('if(c.inactive)', 'if(isInactive(c))').replace('if(c.inactive and', 'if(isInactive(c) and').replace('if(c.inactive or','if(isInactive(c) or').replace('if(pred.inactive or','if(isInactive(pred) or').replace('if(parent.inactive or','if(isInactive(parent.*) or')
s=s.replace('if(isInactive(c) and env.temperature','if(isInactive(c.*) and env.temperature')
s=s.replace('ordinary_hazard*0.1','ordinary_hazard*(1-0.9*c.protective_investment)')
needle='potentials[i]=frondMass(c)*(@exp(@min(20,rate*days))-1)*space;';assert s.count(needle)==1;s=s.replace(needle,needle+'\n        if(qa_activity_law and c.protective_investment>0)potentials[i]*=1-0.1*c.protective_investment;')
needle='var child=parent.*;';assert s.count(needle)==1;s=s.replace(needle,needle+'child.inactive=false;child.recovery_seconds=0;')
# Deliberately faithful inheritance only: no invented mutation distribution or extra random draws.
p.write_text(s)
p=o/'src/simulation/shared_soil.zig';s=p.read_text().replace('if(c.inactive or','if(M.isInactive(c) or');p.write_text(s)
shutil.copy2(t/'shoreline-climate-feasibility/src/simulation/microbes.zig',o/'src/simulation/legacy_microbes.zig')
s=(r/'web/tests/protective-inactivity.zig').read_text()
s=s[:s.index('test "inactive finite')]
s=s.replace('if(c.inactive or c.biomass<=0)','if(!M.qa_activity_law or c.protective_investment<=0 or c.inactive or c.biomass<=0)')
s=s.replace('s.recovery','c.recovery_seconds')
# Wake reset occurs outside local c scope.
s=s.replace('s.wakes+=1;c.recovery_seconds=0','s.wakes+=1;s.cell.cohorts[slot].recovery_seconds=0')
s=s.replace('fn run(kind:usize,slot:usize)!void','fn run(kind:usize,slot:usize,p:f32)!void')
s=s.replace('s.cell.cohorts[1-slot].lineage+=10000;','s.cell.cohorts[1-slot].lineage+=10000;s.cell.cohorts[slot].protective_investment=p;')
s=s.replace('if(kind==5)try std.testing.expect(enter(&s,slot));','if(kind==5 and p>0)try std.testing.expect(enter(&s,slot));')
s=s.replace('DAY kind={} slot={} day={}', 'DAY p={d} kind={} slot={} day={}').replace('.{kind,slot,(tick+1)/60', '.{p,kind,slot,(tick+1)/60')
s=s.replace('for(0..6)|k|for(0..2)|slot|try run(k,slot);','M.qa_activity_law=true;defer M.qa_activity_law=false;for([_]f32{0,0.5,1})|p|for(0..6)|k|for(0..2)|slot|try run(k,slot,p);')
(o/'src/investment_qa.zig').write_text(s+(r/'web/tests/heritable-inactivity-extra.zig').read_text())
e=r/'web/tests/continuation-review/heritable-inactivity';e.mkdir(parents=True,exist_ok=True)
(e/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o/'src')):hashlib.sha256(p.read_bytes()).hexdigest() for p in (o/'src').rglob('*.zig')},indent=2)+'\n')
