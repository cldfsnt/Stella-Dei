#!/usr/bin/env python3
"""Isolated preregistered feeding benefit/cost factorial, never production."""
from pathlib import Path
import subprocess,sys,hashlib,json
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1]);subprocess.run([sys.executable,str(root/'web/tests/egl-grazing-coupled-prepare.py'),str(out)],check=True)
p=out/'simulation/microbes.zig';s=p.read_text().replace('pub var qa_disable_grazing:bool=false;','pub var qa_disable_grazing:bool=false;\npub var qa_disable_feeding_costs:bool=false;');assert s.count('0.10*c.feeding')==2;assert s.count('(1-0.7*c.feeding)')==1
s=s.replace('0.10*c.feeding','(if(qa_disable_feeding_costs) @as(f32,0) else 0.10*c.feeding)').replace('(1-0.7*c.feeding)','(if(qa_disable_feeding_costs) @as(f32,1) else (1-0.7*c.feeding))');p.write_text(s)
p=out/'main.zig';s=p.read_text().replace('for(0..2)|arm|{','for(0..4)|arm|{').replace('micro.qa_disable_grazing=arm==1;','micro.qa_disable_grazing=arm%2==1;micro.qa_disable_feeding_costs=arm>=2;').replace('for(0..1801)|tick|{','for(0..601)|tick|{').replace('if(arm==1){std.debug.assert(state.planet.microbeStats.grazed_carbon','if(arm%2==1){std.debug.assert(state.planet.microbeStats.grazed_carbon').replace('if(tick!=0 and tick!=180 and tick!=600 and tick!=1200 and tick!=1800)continue;','if(tick%60!=0)continue;').replace('if(tick==1800){','if(tick==600){').replace('site-tmp/grazing-coupled/arm-{d}-day90.json','site-tmp/feeding-cost/arm-{d}-day70.json').replace('GRAZING_COUPLED','FEEDING_COST').replace('micro.qa_disable_grazing=false;try saves.apply','micro.qa_disable_grazing=false;micro.qa_disable_feeding_costs=false;try saves.apply')
s=s.replace('const initial_stats=state.planet.microbeStats;',r'''const initial_stats=state.planet.microbeStats;
            const roots=[_]u64{1092,120};
            var families=[_]std.AutoHashMap(u64,void){std.AutoHashMap(u64,void).init(a),std.AutoHashMap(u64,void).init(a)};
            for(roots,0..)|id,fi|try families[fi].put(id,{});
''')
needle='              if(tick%60!=0)continue;'
s=s.replace(needle,r'''              // Establish only observed connected descendants; never assign unseen causes.
              var changed=true;
              while(changed){changed=false;for(state.planet.microbeCells)|pc|for(pc.cohorts)|co|{if(co.biomass<=0 or co.lineage<next_baseline)continue;for(&families)|*family|{if(family.contains(co.parent) and !family.contains(co.lineage)){try family.put(co.lineage,{});changed=true;}}};}
'''+needle)
s=s.replace('              const st=state.planet.microbeStats;',r'''              const st=state.planet.microbeStats;
              for(roots,0..)|rootid,fi|{
                var family_mass:f64=0;var family_count:usize=0;var root_cell:?usize=null;var root_cohort:micro.Cohort=.{};
                for(state.planet.microbeCells,0..)|pc,ci|for(pc.cohorts)|co|{if(co.biomass<=0)continue;if(families[fi].contains(co.lineage)){family_count+=1;family_mass+=co.biomass;}if(co.lineage==rootid){root_cell=ci;root_cohort=co;}};
                const original_cell:usize=if(fi==0)13670 else 12344;const ci=root_cell orelse original_cell;var food:f64=0;
                for(state.planet.microbeCells[ci].cohorts)|co|{if(co.biomass>0 and co.lineage!=rootid)food+=co.biomass;}
                std.debug.print("FEEDING_FOCAL {s}\n",.{try std.json.stringifyAlloc(a,.{.arm=arm,.tick=tick,.day=60+tick/60,.root=rootid,.root_present=root_cell!=null,.observed_connected_mass=family_mass,.observed_connected_count=family_count,.observed_descendants=families[fi].count()-1,.world_mass_share=if(mass>0)family_mass/mass else 0,.root_cohort=root_cohort,.measured_cell=ci,.original_cell=original_cell,.other_biomass=food,.temperature=state.planet.temperature[ci],.water_mass_1e9kg=state.planet.waterMass[ci],.free_nutrient=state.planet.microbeCells[ci].nutrient},.{})});
              }
''')
p.write_text(s)
files=['simulation/microbes.zig','simulation/planet.zig','main.zig','states/play.zig'];prov={'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'save_sha256':hashlib.sha256((root.parent/'site-tmp/natural60-day60.json').read_bytes()).hexdigest(),'production':{},'copied':{}}
for f in files:prov['production'][f]=hashlib.sha256((root/'src'/f).read_bytes()).hexdigest();prov['copied'][f]=hashlib.sha256((out/f).read_bytes()).hexdigest()
(out.parent/'provenance.json').write_text(json.dumps(prov,indent=2)+'\n')
