//! Simplified phototrophic colonies. Carbon is kg C/m²; nutrient is kg/m².
//! ISOLATED grazing capability prototype, not production or animal taxonomy.
const std = @import("std");
pub const nutrient_per_carbon:f32=0.1;
pub const Mode=enum{sandbox,origin};
pub const Cohort=struct {
    biomass:f32=0, optimum:f32=303, efficiency:f32=1, structure:f32=0, feeding:f32=0,
    generation:u32=0, lineage:u64=0, parent:u64=0, reproduction_credit:f32=0,
};
pub const Cell=struct { cohorts:[4]Cohort=.{.{},.{},.{},.{}}, nutrient:f32=0.02, detritus:f32=0, rng:u64=1 };
pub const Stats=struct { next_lineage:u64=1,births:u64=0,fixed_carbon:f64=0,recycled_carbon:f64=0, nutrient_added:f64=0, failed_patches:u64=0 };
pub const Environment=struct {temperature:f32,depth_km:f32,light:f32,carbon_available:f32,oxygen_carbon_capacity:f32};
pub const Flux=struct{fixed:f32=0,recycled:f32=0,failed_patches:u32=0,grazed:f32=0};
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
        const mortality:f32=if(dry) 4*(1-0.85*c.structure)+0.10*c.structure else if(!habitable(env.depth_km,env.temperature)) 4 else 0.04+(1-fitness)*0.7+0.10*c.structure+0.10*c.feeding;
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
        const rate=@max(0,3*fitness*light*c.efficiency*(1-0.5*c.structure)*(1-0.7*c.feeding)-0.15*c.efficiency*c.efficiency);
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
        result.grazed=grazing.consumed;grazing_respired=grazing.respired;
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
    var child=parent.*;child.biomass=amount;child.parent=parent.lineage;child.lineage=stats.next_lineage;child.generation=parent.generation+|1;child.reproduction_credit=0;
    if(mutate){
        const r=@as(f32,@floatFromInt(random(&donor.rng)>>40))/16777216;
        const q=@as(f32,@floatFromInt(random(&donor.rng)>>40))/16777216;
        child.optimum=std.math.clamp(child.optimum+(r-0.5)*6,270,335);
        child.efficiency=std.math.clamp(child.efficiency+(q-0.5)*0.12,0.5,1.3);
        const r_structure=@as(f32,@floatFromInt(random(&donor.rng)>>40))/16777216;
        child.structure=std.math.clamp(child.structure+(r_structure-0.5)*0.2,0,1);
        const r_feeding=@as(f32,@floatFromInt(random(&donor.rng)>>40))/16777216;
        child.feeding=std.math.clamp(child.feeding+(r_feeding-0.5)*0.2,0,1);
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
    for(&cell.cohorts,0..)|*c,i|{c.biomass=@max(0,c.biomass-losses[i]+gains[i]);c.reproduction_credit+=gains[i];}
    cell.detritus+=total*0.25;cell.nutrient+=total*0.5*nutrient_per_carbon;
    return .{.consumed=total,.respired=total*0.25};
}
const good=Environment{.temperature=303,.depth_km=0.002,.light=1,.carbon_available=100,.oxygen_carbon_capacity=100};
fn grazingDaughter() !Cell {
    var c=initialized(42);var stats:Stats=.{};_=seed(&c,&stats,100);
    for(0..48)|_|_=step(&c,good,3600);
    for(1..100)|seed_value|{
        var candidate=c;candidate.rng=seed_value;var next=stats;
        if(reproduce(&candidate,0,&candidate,&next,true) and candidate.cohorts[1].feeding>0.08)return candidate;
    }
    return error.NoFixture;
}
test "real inherited grazing consumes prey and funds offspring in darkness, unlike controls" {
    var fed=try grazingDaughter();var disabled=fed;disabled.cohorts[1].feeding=0;
    var starved=fed;starved.cohorts[0]=.{};
    const initial_pred=fed.cohorts[1].biomass;const initial_carbon=carbon(fed);const initial_n=nutrientTotal(fed);
    var dark=good;dark.light=0;var recycled:f64=0;var fixed:f64=0;var eaten:f64=0;
    for(0..24*18)|_|{
        const flux=step(&fed,dark,3600);recycled+=flux.recycled;fixed+=flux.fixed;eaten+=flux.grazed;
        _=step(&disabled,dark,3600);_=step(&starved,dark,3600);
    }
    std.debug.print("GRAZING feeding={d} predator {d}->{d}, disabled={d}, preyfree={d}, prey={d}, eaten={d}\n",.{fed.cohorts[1].feeding,initial_pred,fed.cohorts[1].biomass,disabled.cohorts[1].biomass,starved.cohorts[1].biomass,fed.cohorts[0].biomass,eaten});
    try std.testing.expect(fed.cohorts[1].biomass>initial_pred*2 and eaten>0);
    try std.testing.expect(disabled.cohorts[1].biomass<initial_pred and starved.cohorts[1].biomass<initial_pred);
    try std.testing.expect(fed.cohorts[0].biomass<disabled.cohorts[0].biomass);
    try std.testing.expectApproxEqAbs(@as(f64,initial_carbon)+fixed-recycled,@as(f64,carbon(fed)),0.00001);
    try std.testing.expectApproxEqAbs(initial_n,nutrientTotal(fed),0.000002);
    var stats:Stats=.{.next_lineage=3};const before=carbon(fed);
    try std.testing.expect(reproduce(&fed,1,&fed,&stats,false));
    const child_index:usize=if(fed.cohorts[0].parent==2)0 else 2;
    try std.testing.expectEqual(@as(u32,2),fed.cohorts[child_index].generation);
    try std.testing.expectEqual(fed.cohorts[1].feeding,fed.cohorts[child_index].feeding);
    try std.testing.expectApproxEqAbs(before,carbon(fed),0.000001);
}
test "grazing is bounded, order independent, and conservative" {
    var a=initialized(7);a.cohorts=.{.{.biomass=0.1,.feeding=0.8,.lineage=1},.{.biomass=0.02,.feeding=0.4,.lineage=2},.{.biomass=0.06,.lineage=3},.{}};
    var b=a;b.cohorts=.{a.cohorts[2],a.cohorts[0],a.cohorts[1],.{}};
    const carbon_before=carbon(a);const n=nutrientTotal(a);
    const flux=graze(&a,20,100);_=graze(&b,20,100);
    try std.testing.expectApproxEqAbs(carbon_before-flux.respired,carbon(a),0.000001);
    try std.testing.expectApproxEqAbs(n,nutrientTotal(a),0.000001);
    try std.testing.expectApproxEqAbs(a.cohorts[0].biomass,b.cohorts[1].biomass,0.000001);
    try std.testing.expectApproxEqAbs(a.cohorts[1].biomass,b.cohorts[2].biomass,0.000001);
    for(a.cohorts)|c|try std.testing.expect(c.biomass>=0);
}
test "feeding investment costs photosynthesis and requires oxygen for grazing" {
    var feeding=try grazingDaughter();feeding.cohorts[0]=.{};feeding.nutrient=0.02; // resource-replete photosynthesis comparison
    var cheap=feeding;cheap.cohorts[1].feeding=0;
    for(0..12)|_|{_=step(&feeding,good,3600);_=step(&cheap,good,3600);}
    try std.testing.expect(feeding.cohorts[1].biomass<cheap.cohorts[1].biomass);
    var no_oxygen=try grazingDaughter();var dark=good;dark.light=0;dark.oxygen_carbon_capacity=0;
    const before=carbon(no_oxygen);const flux=step(&no_oxygen,dark,3600);
    try std.testing.expectEqual(@as(f32,0),flux.grazed);
    try std.testing.expectEqual(@as(f32,0),flux.recycled);
    try std.testing.expectApproxEqAbs(before,carbon(no_oxygen),0.000001);
    var limited=try grazingDaughter();const limited_flux=graze(&limited,20,0.0001);
    try std.testing.expect(limited_flux.respired<=0.00010001);
}
test "bounded day night food web keeps accounting through repeated real births" {
    var c=try grazingDaughter();var stats:Stats=.{.next_lineage=3};
    const before=carbon(c);const nutrients=nutrientTotal(c);var fixed:f64=0;var recycled:f64=0;var eaten:f64=0;var gen:u32=0;
    for(0..24*120)|hour|{
        var env=good;if(hour%24>=12)env.light=0;
        const flux=step(&c,env,3600);fixed+=flux.fixed;recycled+=flux.recycled;eaten+=flux.grazed;
        if(hour%24==0){const start=random(&c.rng)%4;for(0..4)|offset|{_=reproduce(&c,(start+offset)%4,&c,&stats,true);}}
        try std.testing.expect(validCell(c,stats.next_lineage));
        for(c.cohorts)|co|gen=@max(gen,co.generation);
    }
    try std.testing.expectApproxEqAbs(@as(f64,before)+fixed-recycled,@as(f64,carbon(c)),0.0001);
    try std.testing.expectApproxEqAbs(nutrients,nutrientTotal(c),0.00001);
    try std.testing.expect(eaten>0 and stats.births>0);
    std.debug.print("FOOD_WEB120 biomass={d} births={d} gen={d} grazed={d} cell_bytes={d}\n",.{biomass(c),stats.births,gen,eaten,@sizeOf(Cell)});
}
