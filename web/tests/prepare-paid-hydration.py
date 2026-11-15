from pathlib import Path
import json,hashlib,subprocess
r=Path(__file__).resolve().parents[2];s=(r/'src/simulation/microbes.zig').read_text();original=s
s=s.replace('biomass:f32=0, organization:', 'qa_retention:f32=0, biomass:f32=0, organization:',1)
s=s.replace('pub const Environment=struct {temperature:', 'pub const Environment=struct {qa_hydration:[4]f32=.{0,0,0,0},temperature:',1)
s=s.replace('const tissue=std.math.clamp(c.support_mass/', 'const tissue=std.math.clamp((c.support_mass*(1-c.qa_retention))/',1)
s=s.replace('0.2*c.support_mass/(frondMass(c)+0.01)', '0.2*(c.support_mass*(1-c.qa_retention))/(frondMass(c)+0.01)',1)
# Only height/spread/film allocation; support maintenance remains on all tissue.
start=s.index('pub fn filmProtection');end=s.index('\n}',start)+2
part=s[start:end];part=part.replace('c.support_mass/', '(c.support_mass*(1-c.qa_retention))/');s=s[:start]+part+s[end:]
start=s.index('pub fn step(');end=s.index('\npub fn reproduce(',start);part=s[start:end]
part=part.replace('for(&cell.cohorts) |*c| {','for(&cell.cohorts,0..) |*c,i| {',1)
needle='const wanted_dead=c.biomass*(1-@exp(-(mortality+3*exposed)*days));'
assert needle in part
part=part.replace(needle,'''const hydrated=if(env.depth_km==0 and env.temperature>273.15 and env.temperature<355) std.math.clamp(env.qa_hydration[i],0,1) else @as(f32,0);
        const wet_mortality=0.04+(1-fitness)*0.7+0.10*c.structure+0.10*c.feeding+0.05*c.mobility;
        const effective_mortality=if(hydrated>0) mortality*(1-hydrated)+wet_mortality*hydrated else mortality;
        const wanted_dead=c.biomass*(1-@exp(-(effective_mortality+3*exposed*(1-hydrated))*days));''')
needle='if(c.biomass<=0 or photosyntheticHabitat(c,env.depth_km,env.temperature)<=0)continue;'
assert needle in part
part=part.replace(needle,'''const hydrated=if(env.depth_km==0 and env.temperature>273.15 and env.temperature<355) std.math.clamp(env.qa_hydration[i],0,1) else @as(f32,0);
        const effective_habitat=@max(photosyntheticHabitat(c,env.depth_km,env.temperature),hydrated);
        if(c.biomass<=0 or effective_habitat<=0)continue;''').replace('3*photosyntheticHabitat(c,env.depth_km,env.temperature)*fitness','3*effective_habitat*fitness')
s=s[:start]+part+s[end:];out=r/'src/experimental/paid_hydration_core.zig';out.write_text(s)
e=r/'web/tests/continuation-review/paid-hydration';(e/'provenance.json').write_text(json.dumps({'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip(),'production_sha256':hashlib.sha256(original.encode()).hexdigest(),'candidate_sha256':hashlib.sha256(s.encode()).hexdigest()},indent=2)+'\n')
