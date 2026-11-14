//! Simplified phototrophic colonies. Carbon is kg C/m²; nutrient is kg/m².
//! Inherited coarse-patch motility; not individual animal taxonomy.
const std = @import("std");
pub const nutrient_per_carbon:f32=0.1;
pub const Mode=enum{sandbox,origin};
pub const Cohort=struct {
    biomass:f32=0, water_reserve:f64=0, water_retention:f32=0, organization:f32=0, support_mass:f32=0, optimum:f32=303, efficiency:f32=1, structure:f32=0, feeding:f32=0, mobility:f32=0, relocations:u32=0, last_from:u32=0, last_to:u32=0, last_move_time:f64=0, lifetime_grazed:f32=0,
    generation:u32=0, lineage:u64=0, parent:u64=0, reproduction_credit:f32=0,
};
pub const Cell=struct { surface_water_carry:f64=0, vapor_water_carry:f64=0, cohorts:[4]Cohort=.{.{},.{},.{},.{}}, nutrient:f32=0.02, detritus:f32=0, rng:u64=1 };
pub const Stats=struct { next_lineage:u64=1,births:u64=0,fixed_carbon:f64=0,recycled_carbon:f64=0, nutrient_added:f64=0, failed_patches:u64=0, grazed_carbon:f64=0, grazing_respired_carbon:f64=0, relocations:u64=0, movement_respired_carbon:f64=0 };
pub const Environment=struct {temperature:f32,depth_km:f32,light:f32,carbon_available:f32,oxygen_carbon_capacity:f32,liquid_available:?f64=null,reserve_enabled:bool=true};
pub const Flux=struct{water_taken:f64=0,water_evaporated:f64=0,water_returned:f64=0,fixed:f32=0,recycled:f32=0,failed_patches:u32=0,grazed:f32=0,grazing_respired:f32=0};
pub fn random(state:*u64) u64 {state.* +%= 0x9e3779b97f4a7c15;if(state.*==0)state.*=1;var z=state.*;z=(z^(z>>30))*%0xbf58476d1ce4e5b9;z=(z^(z>>27))*%0x94d049bb133111eb;return z^(z>>31);}
pub fn initialized(initial_seed:u64) Cell{return .{.rng=if(initial_seed==0) 1 else initial_seed};}
pub fn biomass(cell:Cell) f32{var total:f32=0;for(cell.cohorts)|c|total+=c.biomass;return total;}
pub fn carbon(cell:Cell) f32{return biomass(cell)+cell.detritus;}
pub fn nutrientTotal(cell:Cell) f32{return cell.nutrient+biomass(cell)*nutrient_per_carbon;}
pub fn thermalFitness(temp:f32,optimum:f32) f32{return std.math.clamp(1-@abs(temp-optimum)/40,0,1);}
pub fn availableLight(surface:f32,depth_km:f32) f32{return std.math.clamp(surface,0,2)*@exp(-@max(0,depth_km)/0.02);}
/// Support is a subset of total biomass, never additional carbon.
pub fn frondMass(c:Cohort) f32{return @max(0,c.biomass-c.support_mass);}
/// Aquatic growth forms, not taxonomic species or a claim of land plants.
/// Classification is a read-only view of inherited traits and actual tissue.
pub const ProducerForm=enum { mat, cushion, rosette, ribbon, branching, canopy };
pub fn producerForm(c:Cohort) ProducerForm {
    if(c.biomass<=0 or c.support_mass<=0 or frondMass(c)<=0)return .mat;
    if(c.organization<0.025)return .cushion;
    if(c.structure>=0.12)return .branching;
    if(c.efficiency>=1.04)return .canopy;
    if(c.efficiency<0.97)return .ribbon;
    return .rosette;
}
pub fn producerFormName(form:ProducerForm) []const u8 {return switch(form){
    .mat=>"Microbial mat",.cushion=>"Cushion",.rosette=>"Rosette",.ribbon=>"Ribbon",.branching=>"Branching",.canopy=>"Canopy",
};}
/// Continuous architecture avoids growth jumps at display-category boundaries.
/// Toughness makes shorter, denser branching; efficient collectors spread wider.
pub fn producerSpread(c:Cohort) f32 {
    const tissue=std.math.clamp(c.support_mass/@max(c.biomass,0.000001),0,1);
    return 1+tissue*(0.8*(c.efficiency-1)-0.3*c.structure);
}
pub fn producerHeightMeters(c:Cohort) f32 {
    const slenderness=1+0.6*(1-c.efficiency)-0.3*c.structure;
    return @min(0.5,0.2*c.support_mass/(frondMass(c)+0.01)*slenderness);
}
/// Potential daily maintenance demand, not a historical measured flux.
pub fn supportMaintenancePerDay(c:Cohort) f32{return c.support_mass*0.12*(1+0.4*@max(0,c.efficiency-1));}
/// Fraction of reference surface daylight currently intercepted by each cohort.
/// Read-only, finite shared photons; equal-height layers share proportionally.
pub fn producerLightShares(cell:Cell,surface:f32,depth_km:f32) [4]f32 {
    var shares=[_]f32{0,0,0,0};var leaves:f32=0;var weighted:f32=0;
    for(cell.cohorts,0..)|c,i|{const fronds=frondMass(c);leaves+=fronds;shares[i]=fronds*producerSpread(c)*@exp(producerHeightMeters(c)/0.1);weighted+=shares[i];}
    const absorbed=availableLight(surface,depth_km)*(1-@exp(-20*leaves));
    if(weighted>0)for(&shares)|*share|{share.*=absorbed*share.*/weighted;};
    return shares;
}
pub fn habitable(depth:f32,temp:f32) bool{return depth>=0.0002 and depth<=0.05 and temp>260 and temp<355;}
/// Moist-shore protection requires inherited toughness AND paid living tissue.
/// This is a water-film biofilm, not roots/soil or vascular land vegetation.
/// Phenomenological hydration capacity: kg H2O/m²; carbon remains separate.
pub fn waterCapacity(c:Cohort) f64{return @as(f64,@max(0,c.biomass))*20+@as(f64,@max(0,c.support_mass))*60;}
pub fn storedWater(cell:Cell) f64{var water:f64=0;for(cell.cohorts)|c|water+=c.water_reserve;return water;}
pub fn waterUsePerCarbon(c:Cohort) f64{return 50*(1-0.5*@as(f64,c.water_retention));}
fn returnOverflow(c:*Cohort) f64{const old=c.water_reserve;c.water_reserve=@min(old,waterCapacity(c.*));return old-c.water_reserve;}
fn liquidAvailable(env:Environment) f64 {
    if(env.temperature<=273.15 or env.temperature>=373.15)return 0;
    const amount=env.liquid_available orelse @as(f64,env.depth_km)*1000000;
    return if(std.math.isFinite(amount)) @max(0,amount) else 0;
}
pub fn shoreProtection(c:Cohort) f32 {
    if(c.biomass<=0 or frondMass(c)<=0)return 0;
    return std.math.clamp(c.structure/0.15,0,1)*std.math.clamp(c.support_mass/c.biomass/0.03,0,1);
}
pub fn shoreCapable(c:Cohort) bool{return shoreProtection(c)>=0.7;}
/// Water is the actual liquid field; zero water never becomes hidden moisture.
pub fn habitatFitness(c:Cohort,depth:f32,temp:f32) f32 {
    if(!std.math.isFinite(depth) or !std.math.isFinite(temp))return 0;
    if(habitable(depth,temp))return 1;
    if(depth<0 or depth>=0.0002 or temp<=273.15 or temp>=335)return 0;
    const reserve:f32=if(waterCapacity(c)>0) @floatCast(c.water_reserve/waterCapacity(c)) else 0;
    return shoreProtection(c)*std.math.clamp(@max(depth/0.00002,reserve),0,1);
}
pub fn canEstablish(c:Cohort,depth:f32,temp:f32) bool{return habitatFitness(c,depth,temp)>0;}
/// A propagule may arrive here; this does not guarantee its establishment.
/// Mutation happens during paid reproduction, so test actual offspring later.
pub fn dispersalHabitat(depth:f32,temp:f32) bool {
    return std.math.isFinite(depth) and std.math.isFinite(temp) and
        (habitable(depth,temp) or (depth>0 and depth<0.0002 and temp>273.15 and temp<335));
}
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
    const liquid=liquidAvailable(env);
    var uptake_demand:f64=0;
    for(&cell.cohorts)|*c|{result.water_returned+=returnOverflow(c);if(c.biomass>0 and env.reserve_enabled)uptake_demand+=@max(0,waterCapacity(c.*)-c.water_reserve);}
    if(uptake_demand>0){const scale=@min(@as(f64,1),liquid/uptake_demand);for(&cell.cohorts)|*c|{if(c.biomass<=0)continue;var taken=@min(@max(0,liquid-result.water_taken),@max(0,waterCapacity(c.*)-c.water_reserve)*scale);if(result.water_taken+taken>liquid)taken=std.math.nextAfter(f64,taken,0);c.water_reserve+=taken;result.water_taken+=taken;}}
    // Actual stored water is lost to the atmosphere, never silently erased.
    if(env.temperature>273.15)for(&cell.cohorts)|*c|{
        const rate=0.20*(1-0.8*c.water_retention)*(0.25+@max(0,env.light))*std.math.clamp((env.temperature-260)/40,0.1,2);
        const lost=c.water_reserve*(-std.math.expm1(-@as(f64,rate)*days));c.water_reserve-=lost;result.water_evaporated+=lost;
    };
    const available=@max(0,env.carbon_available);
    var potentials=[_]f32{0,0,0,0};
    const light=availableLight(env.light,env.depth_km);
    var support_demand:f32=0;for(cell.cohorts)|c|support_demand+=supportMaintenancePerDay(c)*days;
    const support_scale=if(support_demand>0)@min(@as(f32,1),@max(0,env.oxygen_carbon_capacity)/support_demand) else 0;
    var support_respired:f32=0;
    for(&cell.cohorts) |*c| {
        if(c.biomass<=0)continue;
        const upkeep=@min(c.biomass,supportMaintenancePerDay(c.*)*days*support_scale);
        if(upkeep>0){const factor=1-upkeep/c.biomass;c.biomass-=upkeep;c.support_mass=@min(c.biomass,c.support_mass*factor);cell.nutrient+=upkeep*nutrient_per_carbon;support_respired+=upkeep;}
        const fitness=thermalFitness(env.temperature,c.optimum);
        const dry=env.depth_km<0.0002 and env.temperature>260 and env.temperature<355;
        const habitat=habitatFitness(c.*,env.depth_km,env.temperature);
        const baseline:f32=0.04+(1-fitness)*0.7+0.10*c.structure+0.10*c.feeding+0.05*c.mobility;
        const desiccation:f32=4*(1-0.85*c.structure)+0.10*c.structure;
        // Paid protective tissue remains protective while dormant; it does not
        // supply water or permit carbon fixation. Drought still consumes life.
        // Coarse protection tapers toward the existing lethal 260 K bound.
        // Frozen films never permit fixation; this is finite dormancy, not
        // frost immunity or a validated species-specific thermal model.
        const cold_fraction=std.math.clamp((273.15-env.temperature)/13.15,0,1);
        const protection=if(dry and env.temperature>260 and env.temperature<335) shoreProtection(c.*)*(1-cold_fraction) else 0;
        const deficit=1-protection;
        const dormant=desiccation*deficit*deficit+(0.03+0.10*c.structure)*protection+0.8*cold_fraction;
        const mortality:f32=if(dry) dormant*(1-habitat)+baseline*habitat else if(!habitable(env.depth_km,env.temperature)) 4 else baseline;
        const exposed=std.math.clamp((producerHeightMeters(c.*)-env.depth_km*1000)/0.1,0,1);
        const exposure_protection=if(env.depth_km<0.0002) protection else 0;
        const dead=c.biomass*(1-@exp(-(mortality+3*exposed*(1-exposure_protection))*days));
        if(c.biomass>0)c.support_mass*=1-dead/c.biomass;
        c.biomass-=dead;c.support_mass=@min(c.support_mass,c.biomass);cell.detritus+=dead;cell.nutrient+=dead*nutrient_per_carbon;
        // Below 25% of one propagule, recycle unresolved failed establishment.
        if(c.biomass<0.0025){result.failed_patches+=1;cell.detritus+=c.biomass;cell.nutrient+=c.biomass*nutrient_per_carbon;result.water_returned+=c.water_reserve;c.*=.{};continue;}
        if(!habitable(env.depth_km,env.temperature))continue;
    }
    const space=@max(0,1-biomass(cell.*));
    var organized=false;for(cell.cohorts)|c|{if(c.support_mass>0)organized=true;}

    for(cell.cohorts,0..) |c,i| {
        if(c.biomass<=0 or env.temperature<=273.15 or !canEstablish(c,env.depth_km,env.temperature))continue;
        const fitness=thermalFitness(env.temperature,c.optimum);
        // Higher light efficiency carries maintenance cost; not a free upgrade.
        const rate=@max(0,3*fitness*light*c.efficiency*(1-0.3*c.water_retention)*(1-0.5*c.structure)*(1-0.7*c.feeding)*(1-0.3*c.mobility)-0.15*c.efficiency*c.efficiency);
        potentials[i]=frondMass(c)*(@exp(@min(20,rate*habitatFitness(c,env.depth_km,env.temperature)*days))-1)*space;
    }
    // Smooth competition: height redistributes, never increases the existing
    // unshaded photosynthetic budget. No tiny-tissue cell-wide model switch.
    // The phenomenological uptake response/20m attenuation remain compatible.
    if(organized){
        var budget:f32=0;var weighted:f32=0;
        for(&potentials,cell.cohorts)|*value,c|{budget+=value.*;value.* *= producerSpread(c)*@exp(producerHeightMeters(c)/0.1);weighted+=value.*;}
        if(weighted>0)for(&potentials)|*value|{value.* *= budget/weighted;};
    }
    var water_demand:f64=0;
    for(&potentials,cell.cohorts)|*v,c|{if(env.reserve_enabled)v.*=@floatCast(@min(@as(f64,v.*),c.water_reserve/waterUsePerCarbon(c)));water_demand+=@as(f64,v.*) * waterUsePerCarbon(c);}
    if(!env.reserve_enabled and water_demand>0){const scale:f32=@floatCast(@min(@as(f64,1),liquid/water_demand));for(&potentials)|*v|v.* *= scale;}
    var potential:f32=0;for(potentials)|v|potential+=v;
    const growth=@min(potential,@min(space,@min(available,cell.nutrient/nutrient_per_carbon)));
    var actual_growth:f32=0;var direct_remaining=liquid-result.water_taken;
    if(potential>0)for(&cell.cohorts,0..) |*c,i| {
        var share=growth*potentials[i]/potential;
        const budget=if(env.reserve_enabled)c.water_reserve else direct_remaining;
        const cost=waterUsePerCarbon(c.*);
        var bound:f32=@floatCast(@min(@as(f64,share),budget/cost));
        if(@as(f64,bound)*cost>budget and bound>0)bound=@bitCast(@as(u32,@bitCast(bound))-1);
        share=@min(share,bound);const water_used=@as(f64,share)*cost;actual_growth+=share;
        if(env.reserve_enabled)c.water_reserve-=water_used else {result.water_taken+=water_used;direct_remaining-=water_used;}
        result.water_evaporated+=water_used;c.biomass+=share;c.support_mass=@min(c.biomass,c.support_mass+share*c.organization);c.reproduction_credit+=share;
    };
    cell.nutrient=@max(0,cell.nutrient-actual_growth*nutrient_per_carbon);result.fixed=actual_growth;
    var grazing_respired:f32=0;
    if(habitable(env.depth_km,env.temperature)){
        const grazing=graze(cell,days,@max(0,env.oxygen_carbon_capacity-support_respired));
        result.water_returned+=grazing.water_returned;result.grazed=grazing.consumed;result.grazing_respired=grazing.respired;grazing_respired=grazing.respired;
    }
    const recycled=@min(cell.detritus*(1-@exp(-0.1*days)),@max(0,env.oxygen_carbon_capacity-grazing_respired-support_respired));
    cell.detritus-=recycled;result.recycled=recycled+grazing_respired+support_respired;
    for(&cell.cohorts)|*c|result.water_returned+=returnOverflow(c);
    return result;
}
/// Donor-funded propagule. Empty cohort slots preserve distinct competitors;
/// full slots reject colonization rather than silently overwrite a population.
pub fn reproduce(donor:*Cell,which:usize,destination:*Cell,stats:*Stats,mutate:bool) bool {
    return reproduceSized(donor,which,destination,stats,mutate,0.01,0.03,0.04);
}
/// Small exploratory offspring: fully funded from parent mass and earned growth.
/// Destination need not be habitable; normal physiology decides survival there.
pub fn propagate(donor:*Cell,which:usize,destination:*Cell,stats:*Stats) bool {
    return reproduceSized(donor,which,destination,stats,true,0.004,0.02,0.01);
}
fn reproduceSized(donor:*Cell,which:usize,destination:*Cell,stats:*Stats,mutate:bool,amount:f32,min_parent:f32,credit:f32) bool {
    if(which>=4)return false;
    const parent=&donor.cohorts[which];
    if(parent.biomass<min_parent or parent.reproduction_credit<credit)return false;
    var slot:?usize=null;for(destination.cohorts,0..) |c,i|{if(c.biomass==0){slot=i;break;}}
    const i=slot orelse return false;
    if(biomass(destination.*)>0.99)return false;
    var child=parent.*;child.water_reserve=parent.water_reserve*(@as(f64,amount)/parent.biomass);child.support_mass=@min(amount,parent.support_mass*(amount/parent.biomass));child.biomass=amount;child.parent=parent.lineage;child.lineage=stats.next_lineage;child.generation=parent.generation+|1;child.reproduction_credit=0;child.lifetime_grazed=0;child.relocations=0;child.last_from=0;child.last_to=0;child.last_move_time=0;
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
        const r_organization=@as(f32,@floatFromInt(random(&donor.rng)>>40))/16777216;
        child.organization=std.math.clamp(child.organization+(r_organization-0.5)*0.12,0,0.7);
        const r_retention=@as(f32,@floatFromInt(random(&donor.rng)>>40))/16777216;
        child.water_retention=std.math.clamp(child.water_retention+(r_retention-0.5)*0.12,0,1);
    }
    parent.water_reserve-=child.water_reserve;parent.support_mass-=child.support_mass;parent.biomass-=amount;parent.support_mass=std.math.clamp(parent.support_mass,0,parent.biomass);parent.reproduction_credit-=credit;destination.cohorts[i]=child;
    stats.next_lineage+=1;stats.births+=1;
    return true;
}
pub fn validCell(cell:Cell,next_lineage:u64) bool {
    if(cell.rng==0)return false;
    if(!std.math.isFinite(cell.surface_water_carry) or cell.surface_water_carry<0 or !std.math.isFinite(cell.vapor_water_carry) or cell.vapor_water_carry<0)return false;
    if(!std.math.isFinite(cell.nutrient) or cell.nutrient<0 or !std.math.isFinite(cell.detritus) or cell.detritus<0)return false;
    if(biomass(cell)>1.0001)return false;
    for(cell.cohorts) |c| {
        if(!std.math.isFinite(c.water_reserve) or c.water_reserve<0 or c.water_reserve>waterCapacity(c)+0.00001 or !std.math.isFinite(c.water_retention) or c.water_retention<0 or c.water_retention>1)return false;
        if(!std.math.isFinite(c.biomass) or c.biomass<0 or !std.math.isFinite(c.optimum) or c.optimum<270 or c.optimum>335 or !std.math.isFinite(c.efficiency) or c.efficiency<0.5 or c.efficiency>1.3 or !std.math.isFinite(c.reproduction_credit) or c.reproduction_credit<0)return false;
        if(!std.math.isFinite(c.organization) or c.organization<0 or c.organization>0.7 or !std.math.isFinite(c.support_mass) or c.support_mass<0 or c.support_mass>c.biomass)return false;
        if(!std.math.isFinite(c.structure) or c.structure<0 or c.structure>1)return false;
        if(!std.math.isFinite(c.feeding) or c.feeding<0 or c.feeding>1)return false;
        if(!std.math.isFinite(c.lifetime_grazed) or c.lifetime_grazed<0)return false;
        if(!std.math.isFinite(c.mobility) or c.mobility<0 or c.mobility>1)return false;
        if(!std.math.isFinite(c.last_move_time) or c.last_move_time<0)return false;
        if(c.biomass>0 and (c.lineage==0 or c.lineage>=next_lineage or c.parent>=c.lineage))return false;
    }
    return true;
}

/// Simultaneous predator-prey demands prevent iteration-order feeding advantage.
/// Only other live cohorts are edible. Half consumed carbon is assimilated;
/// one quarter is respired (oxygen-limited), one quarter enters detritus.
/// Nutrient bound in both waste streams returns locally.
pub const GrazingFlux=struct{consumed:f32=0,respired:f32=0,water_returned:f64=0};
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
    var water_gains=[_]f64{0,0,0,0};var water_losses=[_]f64{0,0,0,0};
    var gains=[_]f32{0,0,0,0};var losses=[_]f32{0,0,0,0};var total:f32=0;
    for(snapshot,0..)|prey,j|{
        var wanted:f32=0;for(demand)|row|wanted+=row[j];
        const scale=if(wanted>0)@min(@as(f32,1),prey.biomass/wanted) else 0;
        for(0..4)|i|{const consumed=demand[i][j]*scale*oxygen_scale;gains[i]+=consumed*0.5;losses[j]+=consumed;total+=consumed;const water=if(prey.biomass>0)prey.water_reserve*(consumed/prey.biomass) else 0;water_gains[i]+=water;water_losses[j]+=water;}
    }
    var water_returned:f64=0;
    for(&cell.cohorts,0..)|*c,i|{c.water_reserve=@max(0,c.water_reserve-water_losses[i]+water_gains[i]);if(c.biomass>0)c.support_mass*=@max(0,1-losses[i]/c.biomass);c.support_mass+=gains[i]*c.organization;c.biomass=@max(0,c.biomass-losses[i]+gains[i]);c.support_mass=std.math.clamp(c.support_mass,0,c.biomass);c.reproduction_credit+=gains[i];c.lifetime_grazed+=gains[i]*2;water_returned+=returnOverflow(c);}
    cell.detritus+=total*0.25;cell.nutrient+=total*0.5*nutrient_per_carbon;
    return .{.consumed=total,.respired=total*0.25,.water_returned=water_returned};
}
/// Whole resident cohort relocates, preserving identity/history and avoiding
/// fractional duplicate lineage bookkeeping. The caller supplies actual adjacent
/// patches, not an unrestricted search. Cost is respired carbon, oxygen-limited.
pub const Movement=struct{moved:bool=false,to:usize=0,respired:f32=0,water_returned:f64=0};
pub const Neighbor=struct{index:usize,environment:Environment};
pub const RelocationReason = enum {
    invalid, no_living_cohort, no_grazing, no_mobility, source_unsuitable,
    already_moved, no_suitable_neighbor, no_better_prey, no_capacity,
    insufficient_oxygen, insufficient_fragment, eligible,
};
pub const RelocationOpportunity = struct {
    reason: RelocationReason,
    destination: ?usize = null,
    slot: usize = 0,
    respired_cost: f32 = 0,
};
/// Read-only explanation of the exact movement predicate. Eligibility does not
/// guarantee a move: relocate still draws its elapsed-time-dependent chance.
/// No allocation, PRNG advancement, resource change or persistent UI state.
pub fn evaluateRelocation(cells: []const Cell, from: usize, which: usize, current: Environment, neighbors: []const Neighbor, game_time: f64) RelocationOpportunity {
    if (from >= cells.len or which >= 4 or !std.math.isFinite(game_time) or game_time < 0) return .{ .reason = .invalid };
    const parent = cells[from].cohorts[which];
    if (parent.biomass <= 0) return .{ .reason = .no_living_cohort };
    if (parent.feeding <= 0) return .{ .reason = .no_grazing };
    if (parent.mobility <= 0) return .{ .reason = .no_mobility };
    if (!habitable(current.depth_km, current.temperature)) return .{ .reason = .source_unsuitable };
    if (parent.relocations > 0 and parent.last_move_time == game_time) return .{ .reason = .already_moved };
    const fragment=frondMass(parent);
    if(fragment*(1-0.02*parent.mobility)<0.0025)return .{.reason=.insufficient_fragment};
    var here_food: f32 = 0;
    for (cells[from].cohorts, 0..) |co, i| { if (i != which) here_food += co.biomass; }
    var best_food = here_food + 0.005;
    var target: ?usize = null;
    var slot: usize = 0;
    var suitable = false;
    var better_prey = false;
    for (neighbors) |neighbor| {
        const n = neighbor.index;
        if (n >= cells.len or n == from or !habitable(neighbor.environment.depth_km, neighbor.environment.temperature)) continue;
        suitable = true;
        const food = biomass(cells[n]);
        if (food > here_food + 0.005) better_prey = true;
        var empty: ?usize = null;
        for (cells[n].cohorts, 0..) |co, i| { if (co.biomass == 0) { empty = i; break; } }
        if (empty == null or food + fragment > 1) continue;
        if (food > best_food) { best_food = food; target = n; slot = empty.?; }
    }
    if (!suitable) return .{ .reason = .no_suitable_neighbor };
    if (!better_prey) return .{ .reason = .no_better_prey };
    const destination = target orelse return .{ .reason = .no_capacity };
    const cost = fragment * 0.02 * parent.mobility;
    if (current.oxygen_carbon_capacity < cost) return .{ .reason = .insufficient_oxygen, .destination = destination, .slot = slot, .respired_cost = cost };
    return .{ .reason = .eligible, .destination = destination, .slot = slot, .respired_cost = cost };
}
pub fn relocate(cells:[]Cell,from:usize,which:usize,current:Environment,neighbors:[]const Neighbor,elapsed:f32,game_time:f64) Movement {
    const days=elapsed/86400;
    if(!std.math.isFinite(elapsed) or days<=0)return .{};
    const opportunity=evaluateRelocation(cells,from,which,current,neighbors,game_time);
    if(opportunity.reason!=.eligible)return .{};
    const parent=cells[from].cohorts[which];
    const destination=opportunity.destination.?;
    const slot=opportunity.slot;
    const cost=opportunity.respired_cost;
    const chance=1-@exp(-0.5*parent.mobility*days);
    const draw=@as(f32,@floatFromInt(random(&cells[from].rng)>>40))/16777216;
    if(draw>=chance)return .{};
    var moved=parent;moved.biomass=frondMass(parent)-cost;moved.support_mass=0;moved.water_reserve=parent.water_reserve*(moved.biomass/parent.biomass);
    var water_returned=parent.water_reserve-moved.water_reserve;water_returned+=returnOverflow(&moved);
    cells[from].detritus+=parent.support_mass;cells[from].nutrient+=parent.support_mass*nutrient_per_carbon;
    cells[from].cohorts[which]=.{};
    cells[from].nutrient+=cost*nutrient_per_carbon;
    moved.relocations +|=1;moved.last_from=@intCast(from);moved.last_to=@intCast(destination);moved.last_move_time=game_time;
    cells[destination].cohorts[slot]=moved;

    return .{.moved=true,.to=destination,.respired=cost,.water_returned=water_returned};
}
// Test adapter: the real Planet applies returned respiratory flux to atmosphere.
fn tryMove(cells:[]Cell,environments:[]Environment,from:usize,which:usize,neighbors:[]const usize,days:f32) Movement {
    if(from>=environments.len or neighbors.len>6)return .{};
    var records:[6]Neighbor=undefined;
    for(neighbors,0..)|n,i|{if(n>=environments.len)return .{};records[i]=.{.index=n,.environment=environments[n]};}
    const result=relocate(cells,from,which,environments[from],records[0..neighbors.len],days*86400,0);
    if(result.moved){environments[from].oxygen_carbon_capacity-=result.respired;environments[from].carbon_available+=result.respired;}
    return result;
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
            for(&cells)|*c|for(c.cohorts,0..)|co,i|{if(co.biomass>0 and co.lineage==descendant.lineage){if(control==0 and reproduce(c,i,c,&stats,false)){births+=1;var inherited=false;for(c.cohorts)|child|{if(child.parent==descendant.lineage and child.generation==2 and child.mobility==descendant.mobility){inherited=true;try std.testing.expectEqual(@as(u32,0),child.relocations);try std.testing.expectEqual(@as(f64,0),child.last_move_time);}}try std.testing.expect(inherited);}}};
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
    try std.testing.expectEqual(@as(u32,1),cells[1].cohorts[1].relocations);
    try std.testing.expectEqual(@as(u32,0),cells[1].cohorts[1].last_from);
    try std.testing.expectEqual(@as(u32,1),cells[1].cohorts[1].last_to);
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

fn grazingDaughter() !Cell {
    var c=initialized(42);var stats:Stats=.{};_=seed(&c,&stats,100);
    for(0..48)|_|_=step(&c,good,3600);
    for(1..100)|seed_value|{
        var candidate=c;candidate.rng=seed_value;var next=stats;
        if(reproduce(&candidate,0,&candidate,&next,true) and candidate.cohorts[1].feeding>0.08){candidate.cohorts[1].mobility=0;return candidate;} // isolate grazing from motility cost
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
    try std.testing.expect(fed.cohorts[1].lifetime_grazed>0);
    try std.testing.expectEqual(@as(f32,0),fed.cohorts[child_index].lifetime_grazed);
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

test "carbon and nutrients conserved across growth death recycling and transfer" {
    var c=initialized(42);var stats:Stats=.{};const seeded=seed(&c,&stats,100);
    const n=nutrientTotal(c);var fixed:f32=seeded;var recycled:f32=0;
    for(0..200) |_| {const flux=step(&c,good,3600);fixed+=flux.fixed;recycled+=flux.recycled;}
    try std.testing.expect(biomass(c)>0.02);
    try std.testing.expectApproxEqAbs(fixed-recycled,carbon(c),0.00002);
    try std.testing.expectApproxEqAbs(n,nutrientTotal(c),0.000002);
    var child=initialized(5);const before=carbon(c)+carbon(child);const nutrients=nutrientTotal(c)+nutrientTotal(child);
    try std.testing.expect(reproduce(&c,0,&child,&stats,true));
    try std.testing.expectApproxEqAbs(before,carbon(c)+carbon(child),0.000001);
    try std.testing.expectApproxEqAbs(nutrients,nutrientTotal(c)+nutrientTotal(child),0.000001);
    try std.testing.expectEqual(@as(u32,1),child.cohorts[0].generation);
    try std.testing.expect(child.cohorts[0].optimum!=c.cohorts[0].optimum);
    try std.testing.expect(validCell(c,stats.next_lineage) and validCell(child,stats.next_lineage));
}
test "darkness carbon starvation and drying do not create growth" {
    for(0..3) |condition| {
        var c=initialized(7);var stats:Stats=.{};_=seed(&c,&stats,100);
        var env=good;
        if(condition==0)env.light=0 else if(condition==1)env.carbon_available=0 else env.depth_km=0;
        const flux=step(&c,env,86400);
        try std.testing.expectEqual(@as(f32,0),flux.fixed);
        try std.testing.expect(biomass(c)<0.02);
    }
}
test "live competing trait distribution responds to environment, order independent" {
    var a=initialized(99);a.cohorts=.{.{.biomass=0.05,.optimum=285,.lineage=1},.{.biomass=0.05,.optimum=315,.lineage=2},.{},.{}};
    a.nutrient=0.09;var b=a;b.cohorts=.{a.cohorts[1],a.cohorts[0],.{},.{}};
    var hot=good;hot.temperature=315;
    for(0..240) |_| { _=step(&a,hot,3600);_=step(&b,hot,3600); }
    try std.testing.expect(a.cohorts[1].biomass>a.cohorts[0].biomass*3);
    try std.testing.expectApproxEqAbs(a.cohorts[0].biomass,b.cohorts[1].biomass,0.00001);
    try std.testing.expectApproxEqAbs(a.cohorts[1].biomass,b.cohorts[0].biomass,0.00001);
}
test "full cohort slots reject propagule without dropping mass or replacing lineage" {
    var a=initialized(1);var b=initialized(2);var stats:Stats=.{};_=seed(&a,&stats,100);_=seed(&b,&stats,100);_=seed(&b,&stats,100);_=seed(&b,&stats,100);_=seed(&b,&stats,100);
    a.cohorts[0].biomass=0.1;a.cohorts[0].reproduction_credit=0.1;const before=a;const dest=b;
    try std.testing.expect(!reproduce(&a,0,&b,&stats,true));try std.testing.expectEqualDeep(before,a);try std.testing.expectEqualDeep(dest,b);
}
test "feeding remains finite and conservative at exposed simulated step sizes" {
    for([_]u32{60,1440,3600})|seconds|{
        var c=try grazingDaughter();var env=good;env.light=0;
        const before=carbon(c);const nutrients=nutrientTotal(c);var recycled:f64=0;var eaten:f64=0;
        for(0..(18*86400/seconds))|_|{
            const flux=step(&c,env,@floatFromInt(seconds));recycled+=flux.recycled;eaten+=flux.grazed;
            try std.testing.expect(validCell(c,3));
        }
        try std.testing.expectApproxEqAbs(@as(f64,before)-recycled,@as(f64,carbon(c)),0.0001);
        try std.testing.expectApproxEqAbs(nutrients,nutrientTotal(c),0.00001);
        try std.testing.expect(c.cohorts[1].biomass>0.02 and eaten>0);
        std.debug.print("GRAZING_STEP seconds={d} predator={d} eaten={d}\n",.{seconds,c.cohorts[1].biomass,eaten});
    }
}
test "one coarse relocation per simulation instant with no ghost cohort" {
    var cells=[_]Cell{initialized(1),initialized(2),initialized(3)};cells[0].cohorts[0]=try inheritedMotileGrazer();
    cells[1].cohorts[0]=.{.biomass=0.1,.lineage=3};cells[2].cohorts[0]=.{.biomass=0.3,.lineage=4};
    const identity=cells[0].cohorts[0].lineage;
    const first=relocate(&cells,0,0,good,&.{.{.index=1,.environment=good}},86400000,17);
    try std.testing.expect(first.moved);
    const same_tick=relocate(&cells,1,1,good,&.{.{.index=2,.environment=good}},86400000,17);
    try std.testing.expect(!same_tick.moved);
    const next_tick=relocate(&cells,1,1,good,&.{.{.index=2,.environment=good}},86400000,18);
    try std.testing.expect(next_tick.moved);
    var copies:usize=0;for(cells)|c|for(c.cohorts)|co|{if(co.biomass>0 and co.lineage==identity)copies+=1;};
    try std.testing.expectEqual(@as(usize,1),copies);
    try std.testing.expectEqual(@as(u32,2),cells[2].cohorts[1].relocations);
    try std.testing.expectEqual(@as(f64,18),cells[2].cohorts[1].last_move_time);
}

test "read-only relocation explanations share actual eligibility without advancing randomness" {
    var cells = [_]Cell{ initialized(1), initialized(2) };
    const adjacent = [_]Neighbor{.{ .index = 1, .environment = good }};
    try std.testing.expectEqual(RelocationReason.invalid, evaluateRelocation(&cells, 2, 0, good, &adjacent, 1).reason);
    try std.testing.expectEqual(RelocationReason.no_living_cohort, evaluateRelocation(&cells, 0, 0, good, &adjacent, 1).reason);
    cells[0].cohorts[0] = .{ .biomass = 0.02, .lineage = 1 };
    try std.testing.expectEqual(RelocationReason.no_grazing, evaluateRelocation(&cells, 0, 0, good, &adjacent, 1).reason);
    cells[0].cohorts[0].feeding = 0.2;
    try std.testing.expectEqual(RelocationReason.no_mobility, evaluateRelocation(&cells, 0, 0, good, &adjacent, 1).reason);
    cells[0].cohorts[0].mobility = 0.2;
    var dry = good; dry.depth_km = 0;
    try std.testing.expectEqual(RelocationReason.source_unsuitable, evaluateRelocation(&cells, 0, 0, dry, &adjacent, 1).reason);
    try std.testing.expectEqual(RelocationReason.no_suitable_neighbor, evaluateRelocation(&cells, 0, 0, good, &.{.{ .index = 1, .environment = dry }}, 1).reason);
    try std.testing.expectEqual(RelocationReason.no_better_prey, evaluateRelocation(&cells, 0, 0, good, &adjacent, 1).reason);
    for (&cells[1].cohorts) |*co| co.* = .{ .biomass = 0.02, .lineage = 2 };
    try std.testing.expectEqual(RelocationReason.no_capacity, evaluateRelocation(&cells, 0, 0, good, &adjacent, 1).reason);
    cells[1].cohorts[3] = .{};
    var no_oxygen = good; no_oxygen.oxygen_carbon_capacity = 0;
    try std.testing.expectEqual(RelocationReason.insufficient_oxygen, evaluateRelocation(&cells, 0, 0, no_oxygen, &adjacent, 1).reason);
    const before = cells;
    const opportunity = evaluateRelocation(&cells, 0, 0, good, &adjacent, 1);
    try std.testing.expectEqual(RelocationReason.eligible, opportunity.reason);
    try std.testing.expectEqual(@as(?usize, 1), opportunity.destination);
    try std.testing.expectEqual(@as(usize, 3), opportunity.slot);
    try std.testing.expectEqualDeep(before, cells);
    const moved = relocate(&cells, 0, 0, good, &adjacent, 86400000, 1);
    try std.testing.expect(moved.moved);
    try std.testing.expectEqual(opportunity.respired_cost, moved.respired);
    try std.testing.expectEqual(RelocationReason.already_moved, evaluateRelocation(&cells, 1, 3, good, &.{.{ .index = 0, .environment = good }}, 1).reason);
}

test "producer tissue is conserved subset through growth grazing reproduction and movement" {
    var cell=initialized(20);var stats:Stats=.{};_=seed(&cell,&stats,100);
    cell.cohorts[0].organization=0.4;
    var env=good;env.depth_km=0.0003;
    const initialC=@as(f64,carbon(cell))+env.carbon_available;const initialN=nutrientTotal(cell);
    for(0..240)|_|{
        const f=step(&cell,env,3600);env.carbon_available+=f.recycled-f.fixed;env.oxygen_carbon_capacity+=f.fixed-f.recycled;
        try std.testing.expect(validCell(cell,stats.next_lineage));
    }
    try std.testing.expect(cell.cohorts[0].support_mass>0 and frondMass(cell.cohorts[0])>0);
    try std.testing.expect(reproduce(&cell,0,&cell,&stats,true));
    try std.testing.expect(cell.cohorts[1].support_mass>0 and cell.cohorts[1].generation==1);
    try std.testing.expectApproxEqAbs(initialC,@as(f64,carbon(cell))+env.carbon_available,0.0001);
    try std.testing.expectApproxEqAbs(initialN,nutrientTotal(cell),0.000001);
    cell.cohorts[1].feeding=0.5;
    const beforeC=carbon(cell);const beforeN=nutrientTotal(cell);const feeding=graze(&cell,0.1,100);
    try std.testing.expectApproxEqAbs(beforeC,carbon(cell)+feeding.respired,0.000001);
    try std.testing.expectApproxEqAbs(beforeN,nutrientTotal(cell),0.000001);
    try std.testing.expect(validCell(cell,stats.next_lineage));
    var cells=[_]Cell{initialized(1),initialized(2)};
    cells[0].cohorts[0]=.{.biomass=0.08,.support_mass=0.03,.organization=0.4,.feeding=0.5,.mobility=0.5,.lineage=1};
    cells[1].cohorts[0]=.{.biomass=0.2,.lineage=2};
    const old=carbon(cells[0])+carbon(cells[1]);const oldN=nutrientTotal(cells[0])+nutrientTotal(cells[1]);
    const movement=relocate(&cells,0,0,good,&.{.{.index=1,.environment=good}},86400000,1);
    try std.testing.expect(movement.moved);
    try std.testing.expectEqual(@as(f32,0),cells[1].cohorts[1].support_mass);
    try std.testing.expectApproxEqAbs(@as(f32,0.03),cells[0].detritus,0.000001);
    try std.testing.expectApproxEqAbs(old,carbon(cells[0])+carbon(cells[1])+movement.respired,0.000001);
    try std.testing.expectApproxEqAbs(oldN,nutrientTotal(cells[0])+nutrientTotal(cells[1]),0.000001);
    cells[0].cohorts[0]=.{.biomass=0.08,.support_mass=0.079,.feeding=1,.mobility=1,.lineage=3};
    try std.testing.expectEqual(RelocationReason.insufficient_fragment,evaluateRelocation(&cells,0,0,good,&.{.{.index=1,.environment=good}},2).reason);
}
test "real inherited organization grows support with finite light and fair sharing" {
    var expressed:u32=0;
    for(1..33)|initial_seed|{
        var cell=initialized(initial_seed);var stats:Stats=.{};_=seed(&cell,&stats,100);
        var env=good;env.depth_km=0.0003;const originalN=nutrientTotal(cell);
        var ledger:f64=carbon(cell);
        for(0..720)|_|{
            const f=step(&cell,env,3600);ledger+=f.fixed-f.recycled;
            for(0..4)|i|_=reproduce(&cell,i,&cell,&stats,true);
            try std.testing.expect(validCell(cell,stats.next_lineage));
            const photons=producerLightShares(cell,env.light,env.depth_km);var sum:f32=0;for(photons)|x|sum+=x;
            try std.testing.expect(sum<=env.light+0.000001);
        }
        var found=false;for(cell.cohorts)|c|{if(c.generation>0 and c.support_mass>0)found=true;}
        if(found)expressed+=1;
        try std.testing.expectApproxEqAbs(ledger,@as(f64,carbon(cell)),0.00001);
        try std.testing.expectApproxEqAbs(originalN,nutrientTotal(cell),0.000001);
    }
    try std.testing.expect(expressed>0);
    std.debug.print("PRODUCER32 expressed={d}\n",.{expressed});
    var equal=initialized(1);equal.cohorts[0]=.{.biomass=0.1,.support_mass=0.03};equal.cohorts[1]=equal.cohorts[0];
    const shares=producerLightShares(equal,1,0.0003);try std.testing.expectApproxEqAbs(shares[0],shares[1],0.000001);
}
test "infinitesimal producer tissue is continuous with zero-support baseline" {
    var baseline=initialized(1);baseline.cohorts[0]=.{.biomass=0.08,.lineage=1};baseline.cohorts[1]=.{.biomass=0.08,.lineage=2};
    var tiny=baseline;tiny.cohorts[0].support_mass=1e-10;
    const old=step(&baseline,good,3600);const new=step(&tiny,good,3600);
    try std.testing.expectApproxEqAbs(old.fixed,new.fixed,0.0000001);
    try std.testing.expectApproxEqAbs(baseline.cohorts[1].biomass,tiny.cohorts[1].biomass,0.0000001);
    const shares=producerLightShares(tiny,1,0.002);
    try std.testing.expectApproxEqAbs(shares[0],shares[1],0.0000001);
}
test "production organization trades open-water growth for continuous crowded light competition" {
    var grown:[2]f32=undefined;
    for(0..2)|control|{
        var cell=initialized(1);cell.nutrient=1;
        cell.cohorts[0]=.{.biomass=0.08,.organization=if(control==0)0.4 else 0,.support_mass=if(control==0)0.032 else 0,.lineage=1};
        for(0..240)|_|_=step(&cell,good,3600);
        grown[control]=cell.cohorts[0].biomass;
    }
    try std.testing.expect(grown[0]<grown[1]);
    var competition=initialized(1);competition.nutrient=1;
    competition.cohorts[0]=.{.biomass=0.08,.organization=0.4,.support_mass=0.032,.lineage=1};
    competition.cohorts[1]=.{.biomass=0.08,.lineage=2};
    for(0..240)|_|_=step(&competition,good,3600);
    std.debug.print("PRODUCER_CONTROL open_support={d} open_flat={d} crowded_support={d} crowded_flat={d}\n",.{grown[0],grown[1],competition.cohorts[0].biomass,competition.cohorts[1].biomass});
    try std.testing.expect(competition.cohorts[0].biomass>competition.cohorts[1].biomass);
}
test "all-support and rounded daughter subsets remain valid without changing carbon" {
    for([_]f32{0.031234567,0.08,0.33333334,0.98})|mass|{
        var cell=initialized(1);var stats:Stats=.{.next_lineage=2};
        cell.cohorts[0]=.{.biomass=mass,.support_mass=mass,.organization=0.7,.lineage=1,.reproduction_credit=0.1,.feeding=0.5,.mobility=1};
        const old=carbon(cell);const n=nutrientTotal(cell);
        try std.testing.expectEqual(@as(f32,0),frondMass(cell.cohorts[0]));
        var cells=[_]Cell{cell,initialized(2)};cells[1].cohorts[0]=.{.biomass=0.1,.lineage=2};
        try std.testing.expectEqual(RelocationReason.insufficient_fragment,evaluateRelocation(&cells,0,0,good,&.{.{.index=1,.environment=good}},1).reason);
        try std.testing.expect(reproduce(&cell,0,&cell,&stats,false));
        try std.testing.expect(validCell(cell,stats.next_lineage));
        try std.testing.expectApproxEqAbs(old,carbon(cell),0.000001);
        const f=step(&cell,good,1440);
        try std.testing.expect(validCell(cell,stats.next_lineage));
        try std.testing.expectApproxEqAbs(old+f.fixed,carbon(cell)+f.recycled,0.000001);
        try std.testing.expectApproxEqAbs(n,nutrientTotal(cell),0.000001);
    }
}

test "aquatic growth forms require actual tissue and follow inherited traits" {
    const base:Cohort=.{.biomass=0.1,.support_mass=0.01,.organization=0.04,.lineage=1};
    var c=base;c.support_mass=0;try std.testing.expectEqual(ProducerForm.mat,producerForm(c));
    c=base;c.organization=0.01;try std.testing.expectEqual(ProducerForm.cushion,producerForm(c));
    c=base;try std.testing.expectEqual(ProducerForm.rosette,producerForm(c));
    c=base;c.efficiency=0.95;try std.testing.expectEqual(ProducerForm.ribbon,producerForm(c));
    c=base;c.structure=0.15;try std.testing.expectEqual(ProducerForm.branching,producerForm(c));
    c=base;c.efficiency=1.06;try std.testing.expectEqual(ProducerForm.canopy,producerForm(c));
    c.biomass=0;try std.testing.expectEqual(ProducerForm.mat,producerForm(c));
}
test "producer architecture is functional continuous and resource conserving" {
    const base:Cohort=.{.biomass=0.1,.support_mass=0.03,.organization=0.3,.lineage=1};
    var ribbon=base;ribbon.efficiency=0.9;
    var canopy=base;canopy.efficiency=1.1;
    var branching=base;branching.structure=0.2;
    try std.testing.expect(producerHeightMeters(ribbon)>producerHeightMeters(canopy));
    try std.testing.expect(producerSpread(canopy)>producerSpread(ribbon));
    try std.testing.expect(supportMaintenancePerDay(canopy)>supportMaintenancePerDay(ribbon));
    try std.testing.expect(producerHeightMeters(branching)<producerHeightMeters(base));
    for([_]Cohort{base,ribbon,canopy,branching})|candidate|{
        var cell=initialized(37);cell.cohorts[0]=candidate;
        const initial=carbon(cell);const n=nutrientTotal(cell);var fixed:f32=0;var recycled:f32=0;
        for(0..48)|_|{const f=step(&cell,good,3600);fixed+=f.fixed;recycled+=f.recycled;try std.testing.expect(validCell(cell,2));}
        try std.testing.expectApproxEqAbs(initial+fixed,carbon(cell)+recycled,0.00001);
        try std.testing.expectApproxEqAbs(n,nutrientTotal(cell),0.00001);
    }
    var low=base;low.efficiency=1.039999;var high=base;high.efficiency=1.040001;
    try std.testing.expectApproxEqAbs(producerHeightMeters(low),producerHeightMeters(high),0.000001);
    try std.testing.expectApproxEqAbs(producerSpread(low),producerSpread(high),0.000001);
}
test "simple seeded colonies evolve multiple real aquatic forms without assigned traits" {
    var seen=[_]bool{false} ** 6;
    var counts=[_]u32{0} ** 6;
    for(1..129)|initial_seed|{
        var cell=initialized(initial_seed);var stats:Stats=.{};_=seed(&cell,&stats,100);
        var env=good;env.depth_km=0.002;
        for(0..1440)|_|{
            _=step(&cell,env,3600);
            for(0..4)|i|_=reproduce(&cell,i,&cell,&stats,true);
            for(cell.cohorts)|c|if(c.biomass>0){const idx=@intFromEnum(producerForm(c));seen[idx]=true;counts[idx]+=1;};
            try std.testing.expect(validCell(cell,stats.next_lineage));
        }
    }
    std.debug.print("EVOLVED_FORMS observed={any} counts={any}\n",.{seen,counts});
    for(seen)|found|try std.testing.expect(found);
}

test "shore adaptation requires real tissue liquid film and tolerable temperature" {
    var c:Cohort=.{.biomass=0.1,.support_mass=0.004,.structure=0.15,.organization=0.04,.lineage=1};
    try std.testing.expect(shoreCapable(c));
    try std.testing.expectEqual(@as(f32,1),habitatFitness(c,0.00005,303));
    for([_]f32{0,-1,0.1})|depth|try std.testing.expectEqual(@as(f32,0),habitatFitness(c,depth,303));
    try std.testing.expectEqual(@as(f32,0),habitatFitness(c,0.00005,270));
    try std.testing.expectEqual(@as(f32,0),habitatFitness(c,0.00005,340));
    c.support_mass=0;try std.testing.expect(!shoreCapable(c));try std.testing.expect(!canEstablish(c,0.00005,303));
    c.support_mass=0.004;c.structure=0;try std.testing.expect(!canEstablish(c,0.00005,303));
}
test "moist shore growth and drying conserve carbon nutrients and support" {
    var cell=initialized(31);cell.cohorts[0]=.{.biomass=0.1,.support_mass=0.004,.structure=0.15,.organization=0.04,.lineage=1};
    var env=good;env.depth_km=0.00005;env.reserve_enabled=false;
    const beforeC=@as(f64,carbon(cell));const beforeN=nutrientTotal(cell);var total_fixed:f64=0;var total_recycled:f64=0;
    for(0..24*160)|hour|{
        if(hour==24*10)env.depth_km=0;
        const f=step(&cell,env,3600);total_fixed+=f.fixed;total_recycled+=f.recycled;env.carbon_available+=f.recycled-f.fixed;env.oxygen_carbon_capacity+=f.fixed-f.recycled;
        if(hour==24*9)try std.testing.expect(biomass(cell)>0.1);
        if(hour>=24*10)try std.testing.expectEqual(@as(f32,0),f.fixed);
        try std.testing.expect(validCell(cell,2));
    }
    try std.testing.expectEqual(@as(f32,0),biomass(cell));
    try std.testing.expectApproxEqAbs(beforeC+total_fixed,@as(f64,carbon(cell))+total_recycled,0.00001);
    try std.testing.expectApproxEqAbs(beforeN,nutrientTotal(cell),0.00001);
}
test "ordinary aquatic descendants can establish on moist shore unlike ancestors" {
    var established:u32=0;
    for(1..129)|initial_seed|{
        var donor=initialized(initial_seed);var stats:Stats=.{};_=seed(&donor,&stats,100);
        var shores=[_]Cell{initialized(500),initialized(501),initialized(502),initialized(503)};
        var env=good;env.depth_km=0.00005;
        for(0..24*90)|_|{
            _=step(&donor,good,3600);
            for(&shores)|*shore|_=step(shore,env,3600);
            for(0..4)|i|{
                _=reproduce(&donor,i,&donor,&stats,true);
                for(&shores)|*shore|_=reproduce(&donor,i,shore,&stats,true);
            }
            for(shores)|shore|for(shore.cohorts)|c|{if(c.biomass>0.03 and c.reproduction_credit>0.02 and shoreCapable(c))established+=1;};
            if(established>0)break;
        }
        if(established>0)break;
    }
    std.debug.print("EVOLVED_SHORE successful_founder_paths={d}\n",.{established});
    try std.testing.expect(established>0);
}

test "unprotected shore propagules fail and transfer exact donor resources" {
    var donor=initialized(1);var stats:Stats=.{};_=seed(&donor,&stats,100);
    for(0..48)|_|_=step(&donor,good,3600);
    var shore=initialized(2);const beforeC=carbon(donor)+carbon(shore);const beforeN=nutrientTotal(donor)+nutrientTotal(shore);
    try std.testing.expect(reproduce(&donor,0,&shore,&stats,false));
    try std.testing.expectApproxEqAbs(beforeC,carbon(donor)+carbon(shore),0.000001);
    try std.testing.expectApproxEqAbs(beforeN,nutrientTotal(donor)+nutrientTotal(shore),0.000001);
    var env=good;env.depth_km=0.00005;
    for(0..48)|_|{const f=step(&shore,env,3600);try std.testing.expectEqual(@as(f32,0),f.fixed);}
    try std.testing.expectEqual(@as(f32,0),biomass(shore));
    try std.testing.expect(dispersalHabitat(0.00005,303));
    try std.testing.expect(!dispersalHabitat(0,303));try std.testing.expect(!dispersalHabitat(0.1,303));
}

/// Existing saved cell PRNG chooses bounded adjacent dispersal priority.
/// This changes placement only, never reproduction thresholds or donor funding.
pub fn neighborFirst(rng:*u64) bool{return random(rng)%4==0;}
test "neighbor priority is bounded reproducible and does not fund extra births" {
    var a:u64=1;var b:u64=1;var count:usize=0;
    for(0..4096)|_|{const choice=neighborFirst(&a);try std.testing.expectEqual(choice,neighborFirst(&b));if(choice)count+=1;}
    try std.testing.expect(count>800 and count<1250);
    var donor=initialized(1);var dest=initialized(2);var stats:Stats=.{};_=seed(&donor,&stats,100);
    try std.testing.expect(!reproduce(&donor,0,&dest,&stats,true));
    try std.testing.expectEqual(@as(u64,0),stats.births);
}

test "paid protective tissue survives cyclic film without fixing carbon during drought" {
    var adapted=initialized(1);adapted.cohorts[0]=.{.biomass=0.02,.support_mass=0.0008,.structure=0.15,.organization=0.04,.lineage=1};
    var naked=initialized(2);naked.cohorts[0]=.{.biomass=0.02,.lineage=1};
    const beforeC=carbon(adapted);const beforeN=nutrientTotal(adapted);var fixed:f32=0;var recycled:f32=0;
    for(0..24*30)|hour|{
        var env=good;env.reserve_enabled=false;env.depth_km=if(hour%24<8) 0.00005 else 0;env.light=if(hour%24<12) 1 else 0;
        const f=step(&adapted,env,3600);_=step(&naked,env,3600);fixed+=f.fixed;recycled+=f.recycled;
        if(env.depth_km==0)try std.testing.expectEqual(@as(f32,0),f.fixed);
        try std.testing.expect(validCell(adapted,2));
    }
    try std.testing.expect(biomass(adapted)>0.02);try std.testing.expectEqual(@as(f32,0),biomass(naked));
    try std.testing.expectApproxEqAbs(beforeC+fixed,carbon(adapted)+recycled,0.00001);
    try std.testing.expectApproxEqAbs(beforeN,nutrientTotal(adapted),0.00001);
}

test "brief frost protection is graded and prolonged frozen film kills without fixation" {
    var adapted=initialized(1);adapted.cohorts[0]=.{.biomass=0.02,.support_mass=0.0008,.structure=0.15,.organization=0.04,.lineage=1};
    var naked=initialized(2);naked.cohorts[0]=.{.biomass=0.02,.lineage=1};
    var env=good;env.depth_km=0.00005;env.temperature=272;
    var fixed:f64=0;var recycled:f64=0;const carbon_start=carbon(adapted);const n_start=nutrientTotal(adapted);
    for(0..24*30)|hour|{
        const f=step(&adapted,env,3600);_=step(&naked,env,3600);fixed+=f.fixed;recycled+=f.recycled;
        try std.testing.expectEqual(@as(f32,0),f.fixed);
        if(hour==3){try std.testing.expect(biomass(adapted)>biomass(naked));try std.testing.expect(biomass(adapted)<0.02);}
    }
    try std.testing.expectEqual(@as(f32,0),biomass(adapted));
    try std.testing.expectApproxEqAbs(@as(f64,carbon_start)+fixed,@as(f64,carbon(adapted))+recycled,0.00001);
    try std.testing.expectApproxEqAbs(n_start,nutrientTotal(adapted),0.00001);
}

fn reserveFixture(retention:f32) Cohort {
    var c:Cohort=.{.biomass=0.1,.support_mass=0.004,.organization=0.04,.structure=0.15,.water_retention=retention,.lineage=1};
    c.water_reserve=waterCapacity(c);return c;
}
test "water ledger closes through uptake growth maintenance drought and death" {
    var cell=initialized(2);cell.cohorts[0]=reserveFixture(0.4);cell.cohorts[0].water_reserve=0;
    var surface:f64=2000;var vapor:f64=0;const water_before=surface;const carbon_before=carbon(cell);const n_before=nutrientTotal(cell);
    var fixed:f64=0;var recycled:f64=0;
    for(0..24*180)|hour|{
        if(hour==48){vapor+=surface;surface=0;} // explicit physical environmental drying, not deletion
        var env=good;env.depth_km=@floatCast(surface/1000000);env.liquid_available=@floatCast(surface);
        const previous_water=storedWater(cell);const f=step(&cell,env,3600);
        surface+=@as(f64,f.water_returned)-f.water_taken;vapor+=f.water_evaporated;fixed+=f.fixed;recycled+=f.recycled;
        try std.testing.expect(surface>=-0.00001);try std.testing.expect(validCell(cell,2));
        try std.testing.expectApproxEqAbs(water_before,surface+vapor+storedWater(cell),0.0001);
        if(env.depth_km==0 and previous_water==0)try std.testing.expectEqual(@as(f32,0),f.fixed);
    }
    try std.testing.expectEqual(@as(f32,0),biomass(cell));try std.testing.expectEqual(@as(f64,0),storedWater(cell));
    try std.testing.expectApproxEqAbs(@as(f64,carbon_before)+fixed,@as(f64,carbon(cell))+recycled,0.00002);
    try std.testing.expectApproxEqAbs(n_before,nutrientTotal(cell),0.00001);
}
test "reserve uptake fairly shares finite real liquid and frozen reserves cannot fix carbon" {
    var a=initialized(2);a.cohorts[0]=reserveFixture(0);a.cohorts[1]=reserveFixture(0.8);a.cohorts[1].lineage=2;
    for(&a.cohorts)|*c|c.water_reserve=0;
    var b=a;std.mem.swap(Cohort,&b.cohorts[0],&b.cohorts[1]);
    var env=good;env.liquid_available=0.05;env.light=0;
    const fa=step(&a,env,60);const fb=step(&b,env,60);
    try std.testing.expect(fa.water_taken<=0.050001);try std.testing.expectApproxEqAbs(fa.water_taken,fb.water_taken,0.000001);
    try std.testing.expectApproxEqAbs(a.cohorts[0].water_reserve,b.cohorts[1].water_reserve,0.000001);
    try std.testing.expectApproxEqAbs(a.cohorts[1].water_reserve,b.cohorts[0].water_reserve,0.000001);
    env.temperature=270;env.light=1;const ice=step(&a,env,3600);
    try std.testing.expectEqual(@as(f32,0),ice.fixed);try std.testing.expectEqual(@as(f64,0),ice.water_taken);
}
test "reproduction grazing and supported relocation conserve water without cloning" {
    var donor=initialized(3);donor.cohorts[0]=reserveFixture(0.4);donor.cohorts[0].reproduction_credit=0.1;
    var dest=initialized(4);var stats:Stats=.{.next_lineage=2};const water=storedWater(donor);
    try std.testing.expect(reproduce(&donor,0,&dest,&stats,true));
    try std.testing.expectApproxEqAbs(water,storedWater(donor)+storedWater(dest),0.000001);
    try std.testing.expect(validCell(donor,stats.next_lineage));try std.testing.expect(validCell(dest,stats.next_lineage));
    var feed=initialized(5);feed.cohorts[0]=reserveFixture(0);feed.cohorts[0].feeding=1;feed.cohorts[1]=reserveFixture(1);feed.cohorts[1].lineage=2;
    const before=storedWater(feed);const g=graze(&feed,0.2,100);
    try std.testing.expectApproxEqAbs(before,storedWater(feed)+g.water_returned,0.000001);try std.testing.expect(validCell(feed,3));
    var cells=[_]Cell{initialized(6),initialized(7)};cells[0].cohorts[0]=reserveFixture(0.4);cells[0].cohorts[0].feeding=1;cells[0].cohorts[0].mobility=1;
    cells[1].cohorts[0]=.{.biomass=0.2,.lineage=2};const before_move=storedWater(cells[0])+storedWater(cells[1]);
    const moved=relocate(&cells,0,0,good,&.{.{.index=1,.environment=good}},86400*1000,1);
    try std.testing.expect(moved.moved);
    try std.testing.expectApproxEqAbs(before_move,storedWater(cells[0])+storedWater(cells[1])+moved.water_returned,0.000001);
    try std.testing.expect(validCell(cells[0],3));try std.testing.expect(validCell(cells[1],3));
}
test "retention trades wet growth speed for dry water economy" {
    var wet_fast=initialized(1);wet_fast.cohorts[0]=reserveFixture(0);
    var wet_slow=initialized(2);wet_slow.cohorts[0]=reserveFixture(1);
    const fast=step(&wet_fast,good,3600);const slow=step(&wet_slow,good,3600);
    try std.testing.expect(fast.fixed>slow.fixed);
    var dry_fast=initialized(3);dry_fast.cohorts[0]=reserveFixture(0);
    var dry_slow=initialized(4);dry_slow.cohorts[0]=reserveFixture(1);
    var env=good;env.depth_km=0;env.liquid_available=0;var low_fixed:f64=0;var high_fixed:f64=0;
    for(0..72)|_|{const f=step(&dry_fast,env,3600);const h=step(&dry_slow,env,3600);low_fixed+=f.fixed;high_fixed+=h.fixed;}
    std.debug.print("RETENTION dry_fixed_low={d} high={d}\n",.{low_fixed,high_fixed});
    try std.testing.expect(high_fixed>low_fixed);
}

test "exploratory propagule is paid conserved and cannot chain without new growth" {
    var donor=Cell{};var target=Cell{};var beyond=Cell{};var stats=Stats{};
    _=seed(&donor,&stats,1);
    try std.testing.expect(!propagate(&donor,0,&target,&stats));
    const env=Environment{.depth_km=0.001,.temperature=303,.light=1,.carbon_available=1,.oxygen_carbon_capacity=1};
    for(0..24)|_|{_=step(&donor,env,3600);if(donor.cohorts[0].reproduction_credit>=0.01)break;}
    const before=carbon(donor)+carbon(target);const nutrient=nutrientTotal(donor)+nutrientTotal(target);
    try std.testing.expect(propagate(&donor,0,&target,&stats));
    try std.testing.expectApproxEqAbs(before,carbon(donor)+carbon(target),0.000001);
    try std.testing.expectApproxEqAbs(nutrient,nutrientTotal(donor)+nutrientTotal(target),0.000001);
    try std.testing.expectEqual(@as(f32,0),target.cohorts[0].reproduction_credit);
    try std.testing.expect(!propagate(&target,0,&beyond,&stats));
    const wet=target;const c_before=carbon(target);const n_before=nutrientTotal(target);
    _=step(&target,.{.depth_km=0,.temperature=303,.light=1,.carbon_available=1,.oxygen_carbon_capacity=0},86400);
    try std.testing.expectEqual(@as(f32,0),biomass(target));
    try std.testing.expectApproxEqAbs(c_before,carbon(target),0.000001);
    try std.testing.expectApproxEqAbs(n_before,nutrientTotal(target),0.000001);
    var favorable=wet;_=step(&favorable,env,86400);try std.testing.expect(biomass(favorable)>0.004);
}

test "small exploratory propagules proportionally transfer f64 stored water without free water" {
 var donor=initialized(19);var target=initialized(20);var stats:Stats=.{.next_lineage=2};
 donor.cohorts[0]=.{.biomass=0.04,.support_mass=0.004,.organization=0.2,.structure=0.4,.water_retention=0.3,.water_reserve=0.8,.reproduction_credit=0.02,.lineage=1};
 const before=storedWater(donor)+storedWater(target);
 const mass=biomass(donor)+biomass(target);const support=donor.cohorts[0].support_mass;
 try std.testing.expect(propagate(&donor,0,&target,&stats));
 try std.testing.expectApproxEqAbs(before,storedWater(donor)+storedWater(target),1e-15);
 try std.testing.expectApproxEqAbs(before*(@as(f64,@as(f32,0.004))/@as(f32,0.04)),target.cohorts[0].water_reserve,1e-15);
 try std.testing.expectApproxEqAbs(mass,biomass(donor)+biomass(target),1e-7);
 try std.testing.expectApproxEqAbs(support,donor.cohorts[0].support_mass+target.cohorts[0].support_mass,1e-7);
 try std.testing.expect(validCell(donor,stats.next_lineage) and validCell(target,stats.next_lineage));
 try std.testing.expectEqual(@as(f32,0),target.cohorts[0].reproduction_credit);
}


test "tiny carry-only uptake never overdrafts aggregate liquid budget" {
 const tiny:f64=0.0000009480795576247094;
 for(1..10000)|initial_seed|{
  var c=initialized(initial_seed);
  for(&c.cohorts,0..)|*co,i|co.*=.{.biomass=0.01+@as(f32,@floatFromInt((initial_seed*(i+1))%97))/1000,.lineage=i+1};
  const f=step(&c,.{.temperature=303,.depth_km=0,.liquid_available=tiny,.light=0,.carbon_available=100,.oxygen_carbon_capacity=100},1);
  try std.testing.expect(f.water_taken<=tiny);
  try std.testing.expectApproxEqAbs(tiny,tiny-f.water_taken+f.water_returned+f.water_evaporated+storedWater(c),1e-18);
 }
}
