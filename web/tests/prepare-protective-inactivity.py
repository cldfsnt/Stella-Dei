from pathlib import Path
import shutil,json,hashlib
r=Path('/workspace/scratch/f67c3ac60ca3/stella-independent-review'); out=r.parent/'site-tmp/protective-inactivity'; src=r.parent/'site-tmp/shoreline-climate-feasibility/src';shutil.copytree(src,out/'src',dirs_exist_ok=True)
p=out/'src/simulation/microbes.zig';s=p.read_text()
def rep(a,b):
 global s
 assert s.count(a)==1,(a,s.count(a));s=s.replace(a,b)
rep('pub const Cohort=struct {','pub const Cohort=struct {\n    inactive:bool=false, // EXPERIMENT ONLY, not saved or inherited\n')
rep('return c.support_mass*0.12*','return (if(c.inactive) @as(f32,0.1) else 1)*c.support_mass*0.12*')
rep('pub fn rootDemand(c:Cohort,env:Environment,dt:f32)f64 {','pub fn rootDemand(c:Cohort,env:Environment,dt:f32)f64 {\n    if(c.inactive)return 0;')
rep('const wanted_dead=c.biomass*(1-@exp(-(effective_mortality+3*exposed*(1-hydrated))*days));','const ordinary_hazard=effective_mortality+3*exposed*(1-hydrated);\n         const hazard=if(c.inactive and env.temperature>=253 and env.temperature<=333) @max(@as(f32,0.08),ordinary_hazard*0.1) else ordinary_hazard;\n         const wanted_dead=c.biomass*(1-@exp(-hazard*days));')
rep('if(c.biomass<=0 or effective_habitat<=0)continue;','if(c.inactive or c.biomass<=0 or effective_habitat<=0)continue;')
rep('if(pred.biomass<=0 or pred.feeding<=0)continue;','if(pred.inactive or pred.biomass<=0 or pred.feeding<=0)continue;')
rep('if(parent.biomass<min_parent or parent.reproduction_credit<credit)return false;','if(parent.inactive or parent.biomass<min_parent or parent.reproduction_credit<credit)return false;')
p.write_text(s)
q=out/'src/simulation/shared_soil.zig';t=q.read_text();assert t.count('if(!root_eligible or c.biomass<=0')==1;t=t.replace('if(!root_eligible or c.biomass<=0','if(c.inactive or !root_eligible or c.biomass<=0');q.write_text(t)

e=r/'web/tests/continuation-review/protective-inactivity';e.mkdir(parents=True,exist_ok=True)
(e/'PREREG.md').write_text('''# One fixed protective inactivity candidate, experiment only
No production/save/inheritance edits. Copied current law3 plus transient whole-cohort flag.
Entry on T<278K or T>323K or depth==0 costs2% actual represented carbon, finite oxygen; cannot cross .0025 cutoff. Cost CO2+released bound N. Inactivity blocks fixation, feeding, reproduction, root demand, not occupancy or being eaten. Support maintenance10%; hazard max(.08/day,10% existing) only253..333K, unchanged outside. Wake after2 continuous favorable hours (283..318K, depth>0), with entire wake interval inactive. No replenishment/resurrection or lowered extinction cutoff.
Numbers are prospective uncalibrated game abstraction; no sensitivity search or automatic promotion. Seven-day local forced conditions, standard rooted founder vs identical active competitor sharing one finite cell/soil/C/N/O2. Stable; wet day1 then dry day2 then wet; wet day1 then263K day2 then warm; permanent240K; permanent400K. Slot swaps. Additional forced-paid-entry stable control reveals opportunity cost, not spontaneous dormancy in stable climate. Actual rooted founder fixture, .02C each, N.02/C.2/O2.2/soil.7101186. Existing day/night light and no soil refill. No global hydrology/rain/evaporation or descendants in ecological assay. Unit checks cover zeroO2 refusal, inactive feeding/birth/root suppression, edible tissue, extinction and wake delay. Accounting C/N1e-5 per local seven-day run; no threshold widening. Results report all, including failure.
''')
(e/'source-hashes.json').write_text(json.dumps({str(x.relative_to(out/'src')):hashlib.sha256(x.read_bytes()).hexdigest() for x in (out/'src').rglob('*.zig')},indent=2))
shutil.copy2(r/'web/tests/protective-inactivity.zig',out/'src/inactivity_qa.zig')
