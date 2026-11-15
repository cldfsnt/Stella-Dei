from pathlib import Path
s=Path('src/experimental/paid_hydration_core.zig').read_text().replace('qa_retention','retention_allocation')
s=s.replace('retention_allocation:f32=0, biomass','retention_allocation:f32=0, stored_water:f64=0, biomass')
s=s.replace('pub const Cell=struct { cohorts:', 'pub const Cell=struct { liquid_return:f64=0, vapor_return:f64=0, cohorts:')
pos=s.index('pub fn random(')
s=s[:pos]+'''/// Experimental ownership only. Mutation of allocation disabled. Water kg/m².
pub fn waterCapacity(c:Cohort)f64{return if(c.biomass>0) @as(f64,c.support_mass)*c.retention_allocation*10 else 0;}
pub fn settleWater(cell:*Cell)void{for(&cell.cohorts)|*c|{const cap=waterCapacity(c.*);if(c.stored_water>cap){cell.liquid_return+=c.stored_water-cap;c.stored_water=cap;}}}
fn releaseFraction(c:*Cohort,fraction:f64,escrow:*f64)void{const before=c.stored_water;c.stored_water=@max(0,before*(1-std.math.clamp(fraction,0,1)));escrow.*+=before-c.stored_water;}
pub fn waterTotal(cell:Cell)f64{var w=cell.liquid_return+cell.vapor_return;for(cell.cohorts)|c|w+=c.stored_water;return w;}
''' +s[pos:]
s=s.replace('const days=elapsed/86400;\n    const available', 'settleWater(cell);\n    const days=elapsed/86400;\n    const available',1)
s=s.replace('if(c.biomass<0.0025){result.failed_patches', 'if(c.biomass<0.0025){cell.liquid_return+=c.stored_water;c.stored_water=0;result.failed_patches',1)
s=s.replace('    const space=@max(0,1-biomass(cell.*));','    settleWater(cell);\n    const space=@max(0,1-biomass(cell.*));',1)
s=s.replace('    return result;\n}\n/// Donor-funded','    settleWater(cell);\n    return result;\n}\n/// Donor-funded',1)
s=s.replace('if(c.biomass==0){slot=i;break;}','if(c.biomass==0 and c.stored_water==0){slot=i;break;}',1)
s=s.replace('    parent.support_mass-=child.support_mass;', '''    // Transfer represented parental water associated with actual paid support.
    const old_water=parent.stored_water;
    const portion=if(parent.support_mass>0) std.math.clamp(@as(f64,child.support_mass)/parent.support_mass,0,1) else 0;
    parent.stored_water=old_water*(1-portion);child.stored_water=old_water-parent.stored_water;
    parent.support_mass-=child.support_mass;''',1)
s=s.replace('    stats.next_lineage+=1;stats.births+=1;','    settleWater(donor);settleWater(destination);\n    stats.next_lineage+=1;stats.births+=1;',1)
s=s.replace('for(&cell.cohorts,0..)|*c,i|{if(c.biomass>0)c.support_mass', 'for(&cell.cohorts,0..)|*c,i|{if(snapshot[i].biomass>0)releaseFraction(c,@as(f64,losses[i])/snapshot[i].biomass,&cell.liquid_return);if(c.biomass>0)c.support_mass',1)
s=s.replace('    cell.detritus+=total*0.25;', '    settleWater(cell);\n    cell.detritus+=total*0.25;',1)
s=s.replace('    cells[from].cohorts[which]=.{};', '    cells[from].liquid_return+=parent.stored_water;moved.stored_water=0;\n    cells[from].cohorts[which]=.{};',1)
s=s.replace('    if(cell.rng==0)return false;', '    if(!std.math.isFinite(cell.liquid_return) or cell.liquid_return<0 or !std.math.isFinite(cell.vapor_return) or cell.vapor_return<0)return false;\n    if(cell.rng==0)return false;',1)
s=s.replace('    for(cell.cohorts) |c| {\n', '    for(cell.cohorts) |c| {\n        if(!std.math.isFinite(c.retention_allocation) or c.retention_allocation<0 or c.retention_allocation>1 or !std.math.isFinite(c.stored_water) or c.stored_water<0 or c.stored_water>waterCapacity(c))return false;\n',1)
Path('src/experimental/hydration_lifecycle_core.zig').write_text(s)
