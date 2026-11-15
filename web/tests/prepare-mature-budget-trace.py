#!/usr/bin/env python3
from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];src=r.parent/'site-tmp/mature-soil/src';o=r.parent/'site-tmp/mature-budget/src';shutil.copytree(src,o,dirs_exist_ok=True)
p=o/'simulation/microbes.zig';s=p.read_text();s=s.replace('const std', 'pub var qa_budget_trace:bool=false;\nconst std',1)
needle='        const wanted_dead=c.biomass*(1-@exp(-(effective_mortality+3*exposed*(1-hydrated))*days));';assert s.count(needle)==1
s=s.replace(needle,needle+'''\n        if(qa_budget_trace)std.debug.print("BUDGET_LOSS {s}\\n",.{std.json.stringifyAlloc(std.heap.page_allocator,.{.id=c.lineage,.env=env,.upkeep=upkeep,.post_upkeep=c.*,.fitness=fitness,.film=film,.protection=protection,.contact=contact,.dry_mortality=dry_mortality,.film_mortality=film_mortality,.effective_mortality=effective_mortality,.hydrated=hydrated,.exposed=exposed,.wanted_dead=wanted_dead},.{}) catch unreachable});''')
needle='        potentials[i]=frondMass(c)*(@exp(@min(20,rate*days))-1)*space;';assert s.count(needle)==1
s=s.replace(needle,needle+'''\n        if(qa_budget_trace)std.debug.print("BUDGET_POTENTIAL {s}\\n",.{std.json.stringifyAlloc(std.heap.page_allocator,.{.id=c.lineage,.habitat=effective_habitat,.fitness=fitness,.available_light=light,.rate=rate,.fronds=frondMass(c),.space=space,.potential=potentials[i]},.{}) catch unreachable});''')
needle='    const growth=@min(potential,@min(space,@min(available,cell.nutrient/nutrient_per_carbon)));';assert s.count(needle)==1
s=s.replace(needle,needle+'''\n    if(qa_budget_trace)std.debug.print("BUDGET_CAP {s}\\n",.{std.json.stringifyAlloc(std.heap.page_allocator,.{.potential=potential,.space=space,.carbon=available,.nutrient_carbon=cell.nutrient/nutrient_per_carbon,.growth=growth},.{}) catch unreachable});''');p.write_text(s)
p=o/'simulation/planet.zig';s=p.read_text();s='pub var qa_budget_enabled:bool=false;\n'+s
needle='            const flux = Microbes.step(cell, environment, dt);';assert s.count(needle)==1
s=s.replace(needle,'''            Microbes.qa_budget_trace=qa_budget_enabled and i==3121;
'''+needle+'''
            if(Microbes.qa_budget_trace)std.debug.print("BUDGET_FLUX {s}\\n",.{std.json.stringifyAlloc(self.allocator,.{.flux=flux,.after=cell.*},.{}) catch unreachable});
            Microbes.qa_budget_trace=false;''');p.write_text(s)
p=o/'main.zig';s=p.read_text();s=s.replace('for(0..2)|arm|{','for(0..4)|arm|{\n            @import("simulation/planet.zig").qa_budget_enabled=arm>=2;')
needle='            const ending=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});';assert s.count(needle)==1
s=s.replace(needle,needle+'''var hash:[32]u8=undefined;std.crypto.hash.sha2.Sha256.hash(ending,&hash,.{});std.debug.print("BUDGET_END arm={} sha={s}\\n",.{arm,std.fmt.fmtSliceHexLower(&hash)});''');p.write_text(s)
(o.parent/'provenance.json').write_text(json.dumps({'baseline_files':{str(p.relative_to(src)):hashlib.sha256(p.read_bytes()).hexdigest()for p in src.rglob('*.zig')},'trace_files':{str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')}},indent=2)+'\n')
