//! Simplified phototrophic colonies. Carbon is kg C/m²; nutrient is kg/m².
//! ISOLATED motile-grazer prototype. Coarse patch relocation, not animal taxonomy.
const std = @import("std");
pub const nutrient_per_carbon:f32=0.1;
pub const Mode=enum{sandbox,origin};
pub const Cohort=struct {
    biomass:f32=0, optimum:f32=303, efficiency:f32=1, structure:f32=0, feeding:f32=0, mobility:f32=0, lifetime_grazed:f32=0,
    generation:u32=0, lineage:u64=0, parent:u64=0, reproduction_credit:f32=0,
};
pub const Cell=struct { cohorts:[4]Cohort=.{.{},.{},.{},.{}}, nutrient:f32=0.02, detritus:f32=0, rng:u64=1 };
pub const Stats=struct { next_lineage:u64=1,births:u64=0,fixed_carbon:f64=0,recycled_carbon:f64=0, nutrient_added:f64=0, failed_patches:u64=0, grazed_carbon:f64=0, grazing_respired_carbon:f64=0 };
pub const Environment=struct {temperature:f32,depth_km:f32,light:f32,carbon_available:f32,oxygen_carbon_capacity:f32};
pub const Flux=struct{fixed:f32=0,recycled:f32=0,failed_patches:u32=0,grazed:f32=0,grazing_respired:f32=0};
pub fn random(state:*u64) u64 {state.* +%= 0x9e3779b97f4a7c15;if(state.*==0)state.*=1;var z=state.*;z=(z^(z>>30))*%0xbf58476d1ce4e5b9;z=(z^(z>>27))*%0x94d049bb133111eb;return z^(z>>31);}
pub fn initialized(initial_seed:u64) Cell{return .{.rng=if(initial_seed==0) 1 else initial_seed};}
pub fn biomass(cell:Cell) f32{var total:f32=0;for(cell.cohorts)|c|total+=c.biomass;return total;}
pub fn carbon(cell:Cell) f32{return biomass(cell)+cell.detritus;}
pub fn nutrientTotal(cell:Cell) f32{return cell.nutrient+biomass(cell)*nutrient_per_carbon;}
pub fn thermalFitness(temp:f32,optimum:f32) f32{return std.math.clamp(1-@abs(temp-optimum)/40,0,1);}
pub fn availableLight(surface:f32,depth_km:f32) f32{return std.math.clamp(surface,0,2)*@exp(-@max(0,depth_km)/0.02);}
pub fn habitable(depth:f32,temp:f32) bool{return depth>=0.0002 and depth<=0.05 and temp>260 and temp<355;}
pub fn seed(cell:*Cell,stats:*Stats,available_carbon:f32) f32 {
    var slot:?usize=null;for(cell.cohorts,0..) |c,i| {if(c.biomass==0){slot=i;break;}}
    const i=slot orelse return 0;
    const amount=@min(0.02,@min(@max(0,available_carbon),cell.nutrient/nutrient_per_carbon));
    if(amount<=0)return 0;
    cell.cohorts[i]=.{.biomass=amount,.lineage=stats.next_lineage};stats.next_lineage+=1;
    cell.nutrient-=amount*nutrient_per_carbon;
    return amount;
}
/// A bounded analytic update. Mortality becomes organic matter; aerobic decay
/// returns carbon to atmosphere only when oxygen is available. Nutrients recycle.
pub fn step(cell:*Cell,env:Environment,elapsed:f32) Flux {
    var result:Flux=.{};
    if(!std.math.isFinite(elapsed) or elapsed<=0)return result;
    const days=elapsed/86400;
    const available=@max(0,env.carbon_available);
    var potentials=[_]f32{0,0,0,0};
    const light=availableLight(env.light,env.depth_km);
    for(&cell.cohorts) |*c| {
        if(c.biomass<=0)continue;
        const fitness=thermalFitness(env.temperature,c.optimum);
        const dry=env.depth_km<0.0002 and env.temperature>260 and env.temperature<355;
        const mortality:f32=if(dry) 4*(1-0.85*c.structure)+0.10*c.structure else if(!habitable(env.depth_km,env.temperature)) 4 else 0.04+(1-fitness)*0.7+0.10*c.structure+0.10*c.feeding+0.05*c.mobility;
        const dead=c.biomass*(1-@exp(-mortality*days));
        c.biomass-=dead;cell.detritus+=dead;cell.nutrient+=dead*nutrient_per_carbon;
        // Below 25% of one propagule, recycle unresolved failed establishment.
        if(c.biomass<0.0025){result.failed_patches+=1;cell.detritus+=c.biomass;cell.nutrient+=c.biomass*nutrient_per_carbon;c.*=.{};continue;}
        if(!habitable(env.depth_km,env.temperature))continue;
    }
    const space=@max(0,1-biomass(cell.*));
    for(cell.cohorts,0..) |c,i| {
        if(c.biomass<=0 or !habitable(env.depth_km,env.temperature))continue;
        const fitness=thermalFitness(env.temperature,c.optimum);
        // Higher light efficiency carries maintenance cost; not a free upgrade.
        const rate=@max(0,3*fitness*light*c.efficiency*(1-0.5*c.structure)*(1-0.7*c.feeding)*(1-0.3*c.mobility)-0.15*c.efficiency*c.efficiency);
        potentials[i]=c.biomass*(@exp(@min(20,rate*days))-1)*space;
    }
    var potential:f32=0;for(potentials)|v|potential+=v;
    const growth=@min(potential,@min(space,@min(available,cell.nutrient/nutrient_per_carbon)));
    if(potential>0)for(&cell.cohorts,0..) |*c,i| {
        const share=growth*potentials[i]/potential;c.biomass+=share;c.reproduction_credit+=share;
    };
    cell.nutrient=@max(0,cell.nutrient-growth*nutrient_per_carbon);result.fixed=growth;
    var grazing_respired:f32=0;
    if(habitable(env.depth_km,env.temperature)){
        const grazing=graze(cell,days,env.oxygen_carbon_capacity);
        result.grazed=grazing.consumed;result.grazing_respired=grazing.respired;grazing_respired=grazing.respired;
    }
    const recycled=@min(cell.detritus*(1-@exp(-0.1*days)),@max(0,env.oxygen_carbon_capacity-grazing_respired));
    cell.detritus-=recycled;result.recycled=recycled+grazing_respired;
    return result;
}
/// Donor-funded propagule. Empty cohort slots preserve distinct competitors;
/// full slots reject colonization rather than silently overwrite a population.
pub fn reproduce(donor:*Cell,which:usize,destination:*Cell,stats:*Stats,mutate:bool) bool {
    if(which>=4)return false;
    const parent=&donor.cohorts[which];
    if(parent.biomass<0.03 or parent.reproduction_credit<0.04)return false;
    var slot:?usize=null;for(destination.cohorts,0..) |c,i|{if(c.biomass==0){slot=i;break;}}
    const i=slot orelse return false;
    if(biomass(destination.*)>0.99)return false;
    const amount:@TypeOf(parent.biomass)=0.01;
    var child=parent.*;child.biomass=amount;child.parent=parent.lineage;child.lineage=stats.next_lineage;child.generation=parent.generation+|1;child.reproduction_credit=0;child.lifetime_grazed=0;
    if(mutate){
        const r=@as(f32,@floatFromInt(random(&donor.rng)>>40))/16777216;
        const q=@as(f32,@floatFromInt(random(&donor.rng)>>40))/16777216;
        child.optimum=std.math.clamp(child.optimum+(r-0.5)*6,270,335);
        child.efficiency=std.math.clamp(child.efficiency+(q-0.5)*0.12,0.5,1.3);
        const r_structure=@as(f32,@floatFromInt(random(&donor.rng)>>40))/16777216;
        child.structure=std.math.clamp(child.structure+(r_structure-0.5)*0.2,0,1);
        const r_feeding=@as(f32,@floatFromInt(random(&donor.rng)>>40))/16777216;
        child.feeding=std.math.clamp(child.feeding+(r_feeding-0.5)*0.2,0,1);
        const r_mobility=@as(f32,@floatFromInt(random(&donor.rng)>>40))/16777216;
        child.mobility=std.math.clamp(child.mobility+(r_mobility-0.5)*0.2,0,1);
    }
    parent.biomass-=amount;parent.reproduction_credit-=0.04;destination.cohorts[i]=child;
    stats.next_lineage+=1;stats.births+=1;
    return true;
}
pub fn validCell(cell:Cell,next_lineage:u64) bool {
    if(cell.rng==0)return false;
    if(!std.math.isFinite(cell.nutrient) or cell.nutrient<0 or !std.math.isFinite(cell.detritus) or cell.detritus<0)return false;
    if(biomass(cell)>1.0001)return false;
    for(cell.cohorts) |c| {
        if(!std.math.isFinite(c.biomass) or c.biomass<0 or !std.math.isFinite(c.optimum) or c.optimum<270 or c.optimum>335 or !std.math.isFinite(c.efficiency) or c.efficiency<0.5 or c.efficiency>1.3 or !std.math.isFinite(c.reproduction_credit) or c.reproduction_credit<0)return false;
        if(!std.math.isFinite(c.structure) or c.structure<0 or c.structure>1)return false;
        if(!std.math.isFinite(c.feeding) or c.feeding<0 or c.feeding>1)return false;
        if(!std.math.isFinite(c.lifetime_grazed) or c.lifetime_grazed<0)return false;
        if(!std.math.isFinite(c.mobility) or c.mobility<0 or c.mobility>1)return false;
        if(c.biomass>0 and (c.lineage==0 or c.lineage>=next_lineage or c.parent>=c.lineage))return false;
    }
    return true;
}

/// Simultaneous predator-prey demands prevent iteration-order feeding advantage.
/// Only other live cohorts are edible. Half consumed carbon is assimilated;
/// one quarter is respired (oxygen-limited), one quarter enters detritus.
/// Nutrient bound in both waste streams returns locally.
pub const GrazingFlux=struct{consumed:f32=0,respired:f32=0};
pub fn graze(cell:*Cell,days:f32,oxygen_capacity:f32) GrazingFlux {
    if(days<=0 or oxygen_capacity<=0)return .{};
    const snapshot=cell.cohorts;
    var demand:[4][4]f32=.{.{0,0,0,0},.{0,0,0,0},.{0,0,0,0},.{0,0,0,0}};
    for(snapshot,0..)|pred,i|{
        if(pred.biomass<=0 or pred.feeding<=0)continue;
        var food:f32=0;for(snapshot,0..)|prey,j|{if(i!=j)food+=prey.biomass;}
        if(food<=0)continue;
        const desired=@min(food,pred.biomass*3*pred.feeding*days);
        for(snapshot,0..)|prey,j|{if(i!=j)demand[i][j]=desired*prey.biomass/food;}
    }
    var requested:f32=0;for(demand)|row|for(row)|v|{requested+=v;};
    const oxygen_scale=if(requested>0)@min(@as(f32,1),@max(0,oxygen_capacity)/(requested*0.25)) else 0;
    var gains=[_]f32{0,0,0,0};var losses=[_]f32{0,0,0,0};var total:f32=0;
    for(snapshot,0..)|prey,j|{
        var wanted:f32=0;for(demand)|row|wanted+=row[j];
        const scale=if(wanted>0)@min(@as(f32,1),prey.biomass/wanted) else 0;
        for(0..4)|i|{const consumed=demand[i][j]*scale*oxygen_scale;gains[i]+=consumed*0.5;losses[j]+=consumed;total+=consumed;}
    }
    for(&cell.cohorts,0..)|*c,i|{c.biomass=@max(0,c.biomass-losses[i]+gains[i]);c.reproduction_credit+=gains[i];c.lifetime_grazed+=gains[i]*2;}
    cell.detritus+=total*0.25;cell.nutrient+=total*0.5*nutrient_per_carbon;
    return .{.consumed=total,.respired=total*0.25};
}
/// Whole resident cohort relocates, preserving identity/history and avoiding
/// fractional duplicate lineage bookkeeping. The caller supplies actual adjacent
/// patches, not an unrestricted search. Cost is respired carbon, oxygen-limited.
pub const Movement=struct{moved:bool=false,to:usize=0,respired:f32=0};
pub fn tryMove(cells:[]Cell,environments:[]Environment,from:usize,which:usize,neighbors:[]const usize,days:f32) Movement {
    if(from>=cells.len or which>=4 or environments.len!=cells.len or days<=0)return .{};
    const parent=cells[from].cohorts[which];
    if(parent.biomass<=0 or parent.feeding<=0 or parent.mobility<=0)return .{};
    var here_food:f32=0;for(cells[from].cohorts,0..)|co,i|{if(i!=which)here_food+=co.biomass;}
    var best_food=here_food+0.005;var target:?usize=null;var slot:usize=0;
    for(neighbors)|n|{
        if(n>=cells.len or n==from or !habitable(environments[n].depth_km,environments[n].temperature))continue;
        var empty:?usize=null;for(cells[n].cohorts,0..)|co,i|{if(co.biomass==0){empty=i;break;}}
        if(empty==null or biomass(cells[n])+parent.biomass>1)continue;
        const food=biomass(cells[n]);
        if(food>best_food){best_food=food;target=n;slot=empty.?;}
    }
    const destination=target orelse return .{};
    const cost=parent.biomass*0.02*parent.mobility;
    if(environments[from].oxygen_carbon_capacity<cost)return .{};
    const chance=1-@exp(-0.5*parent.mobility*days);
    const draw=@as(f32,@floatFromInt(random(&cells[from].rng)>>40))/16777216;
    if(draw>=chance)return .{};
    var moved=parent;moved.biomass-=cost;
    cells[from].cohorts[which]=.{};
    cells[from].nutrient+=cost*nutrient_per_carbon;
    cells[destination].cohorts[slot]=moved;
    environments[from].oxygen_carbon_capacity-=cost;
    environments[from].carbon_available+=cost;
    return .{.moved=true,.to=destination,.respired=cost};
}
const good=Environment{.temperature=303,.depth_km=0.002,.light=1,.carbon_available=100,.oxygen_carbon_capacity=100};
fn inheritedMotileGrazer() !Cohort {
    var parent=initialized(42);var stats:Stats=.{};_=seed(&parent,&stats,100);
    for(0..48)|_|_=step(&parent,good,3600);
    for(1..1000)|seed_value|{
        var candidate=parent;candidate.rng=seed_value;var next=stats;
        if(reproduce(&candidate,0,&candidate,&next,true) and candidate.cohorts[1].feeding>0.08 and candidate.cohorts[1].mobility>0.08)return candidate.cohorts[1];
    }
    return error.NoFixture;
}
fn totalCarbon(cells:[]const Cell,envs:[]const Environment) f64 {
    var total:f64=0;for(cells,envs)|c,e|total+=@as(f64,carbon(c))+e.carbon_available;return total;
}
fn totalN(cells:[]const Cell) f64{var n:f64=0;for(cells)|c|n+=nutrientTotal(c);return n;}
test "inherited motility finds real adjacent prey without duplicates and improves survival versus immobile control" {
    const descendant=try inheritedMotileGrazer();var mobile_survivors:u32=0;var still_survivors:u32=0;var moves:u32=0;var births:u32=0;
    for(0..32)|replicate|{
        for(0..2)|control|{
            var cells=[_]Cell{initialized(replicate+1),initialized(200),initialized(300)};
            cells[0].cohorts[0]=descendant;if(control==1)cells[0].cohorts[0].mobility=0;
            var stats:Stats=.{.next_lineage=3};_=seed(&cells[1],&stats,100);
            for(0..48)|_|_=step(&cells[1],good,3600);
            var envs=[_]Environment{good,good,good};for(&envs)|*e|e.light=0;
            const carbon_before=totalCarbon(&cells,&envs);const n_before=totalN(&cells);
            for(0..24*30)|_|{
                const move=tryMove(&cells,&envs,0,0,&.{1},1.0/24.0);if(move.moved)moves+=1;
                for(&cells,&envs)|*c,*e|{const flux=step(c,e.*,3600);e.carbon_available+=flux.recycled-flux.fixed;e.oxygen_carbon_capacity+=flux.fixed-flux.recycled;}
                var count:usize=0;for(cells)|c|for(c.cohorts)|co|{if(co.biomass>0 and co.lineage==descendant.lineage)count+=1;};
                try std.testing.expect(count<=1);
            }
            var found=false;for(cells)|c|for(c.cohorts)|co|{if(co.biomass>0 and co.lineage==descendant.lineage){found=true;try std.testing.expect(co.lifetime_grazed>0);}};
            if(found){if(control==0)mobile_survivors+=1 else still_survivors+=1;}
            // Return daylight after the search/feeding selection phase; surviving
            // actual lineages can rebuild and fund offspring, never respawned.
            for(&envs)|*e|e.light=1;
            for(0..96)|_|for(&cells,&envs)|*c,*e|{const f=step(c,e.*,3600);e.carbon_available+=f.recycled-f.fixed;e.oxygen_carbon_capacity+=f.fixed-f.recycled;};
            for(&cells)|*c|for(c.cohorts,0..)|co,i|{if(co.biomass>0 and co.lineage==descendant.lineage){if(control==0 and reproduce(c,i,c,&stats,false)){births+=1;var inherited=false;for(c.cohorts)|child|{if(child.parent==descendant.lineage and child.generation==2 and child.mobility==descendant.mobility)inherited=true;}try std.testing.expect(inherited);}}};
            try std.testing.expectApproxEqAbs(carbon_before,totalCarbon(&cells,&envs),0.002);
            try std.testing.expectApproxEqAbs(n_before,totalN(&cells),0.00001);
        }
    }
    std.debug.print("MOTILITY32 mobility={d} feeding={d} mobile_survivors={d} immobile_survivors={d} moves={d} inherited_births={d}\n",.{descendant.mobility,descendant.feeding,mobile_survivors,still_survivors,moves,births});
    try std.testing.expect(mobile_survivors>still_survivors and moves>0 and births>0);
}
test "movement respects adjacency habitat occupancy oxygen and charges exact resource cost" {
    var cells=[_]Cell{initialized(1),initialized(2),initialized(3)};cells[0].cohorts[0]=try inheritedMotileGrazer();cells[1].cohorts[0]=.{.biomass=0.2,.lineage=3};
    var envs=[_]Environment{good,good,good};const before=cells;const gases=envs;
    try std.testing.expect(!tryMove(&cells,&envs,0,0,&.{2},1000).moved);try std.testing.expectEqualDeep(before,cells);
    envs[1].depth_km=0;try std.testing.expect(!tryMove(&cells,&envs,0,0,&.{1},1000).moved);envs=gases;
    envs[0].oxygen_carbon_capacity=0;try std.testing.expect(!tryMove(&cells,&envs,0,0,&.{1},1000).moved);envs=gases;
    const carbon_before=totalCarbon(&cells,&envs);const n=totalN(&cells);const identity=cells[0].cohorts[0];
    const moved=tryMove(&cells,&envs,0,0,&.{1},1000);try std.testing.expect(moved.moved and moved.respired>0);
    try std.testing.expectEqual(@as(f32,0),cells[0].cohorts[0].biomass);
    try std.testing.expectEqual(identity.lineage,cells[1].cohorts[1].lineage);
    try std.testing.expectEqual(identity.generation,cells[1].cohorts[1].generation);
    try std.testing.expectEqual(identity.lifetime_grazed,cells[1].cohorts[1].lifetime_grazed);
    try std.testing.expectApproxEqAbs(carbon_before,totalCarbon(&cells,&envs),0.0001);
    try std.testing.expectApproxEqAbs(n,totalN(&cells),0.000001);
}
test "motility has a benign photosynthetic cost and cannot overwrite full patches" {
    var active=initialized(3);active.cohorts[0]=try inheritedMotileGrazer();active.nutrient=0.02;
    var cheap=active;cheap.cohorts[0].mobility=0;
    for(0..12)|_|{_=step(&active,good,3600);_=step(&cheap,good,3600);}
    try std.testing.expect(active.cohorts[0].biomass<cheap.cohorts[0].biomass);
    var cells=[_]Cell{active,initialized(4)};for(&cells[1].cohorts,0..)|*co,i|co.*=.{.biomass=0.05,.lineage=i+3};
    var envs=[_]Environment{good,good};const before=cells;const gas=envs;
    try std.testing.expect(!tryMove(&cells,&envs,0,0,&.{1},1000).moved);
    try std.testing.expectEqualDeep(before,cells);try std.testing.expectEqualDeep(gas,envs);
}
