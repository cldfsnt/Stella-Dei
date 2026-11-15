from pathlib import Path
r=Path(__file__).resolve().parents[2];s=(r/'src/experimental/shared_pace_core.zig').read_text()
s=s.replace('const upkeep=@min(c.biomass,supportMaintenancePerDay(c.*)*days*support_scale);','const wanted_upkeep=@min(c.biomass,supportMaintenancePerDay(c.*)*days*support_scale);\n        const upkeep=actualDecrease(c.biomass,wanted_upkeep);')
s=s.replace('const dead=c.biomass*(1-@exp(-(mortality+3*exposed)*days));','const wanted_dead=c.biomass*(1-@exp(-(mortality+3*exposed)*days));\n        const dead=actualDecrease(c.biomass,wanted_dead);')
a=s.index('    if(potential>0)for(&cell.cohorts,0..)');b=s.index('    var grazing_respired',a)
s=s[:a]+'''    var actual_growth:f64=0;
    if(potential>0)for(&cell.cohorts,0..) |*c,i| {
        const budget=@min(@as(f64,growth)-actual_growth,@as(f64,growth)*potentials[i]/potential);
        var after:f32=@floatCast(@as(f64,c.biomass)+@max(0,budget));
        if(@as(f64,after)-c.biomass>budget)after=std.math.nextAfter(f32,after,c.biomass);
        const share=after-c.biomass;c.biomass=after;actual_growth+=share;
        c.support_mass=@min(c.biomass,boundedAdd(c.support_mass,@as(f64,share)*c.organization));c.reproduction_credit=boundedAdd(c.reproduction_credit,share);
    };
    cell.nutrient=@max(0,cell.nutrient-@as(f32,@floatCast(actual_growth*nutrient_per_carbon)));result.fixed=@floatCast(actual_growth);
'''+s[b:]
s+='''
fn boundedAdd(old:f32,budget:f64)f32{
 var after:f32=@floatCast(@as(f64,old)+budget);
 if(@as(f64,after)-old>budget)after=std.math.nextAfter(f32,after,old);
 return after;
}
fn actualDecrease(old:f32,wanted:f32)f32{
 var after=old-wanted;
 if(@as(f64,old)-after>@as(f64,wanted))after=std.math.nextAfter(f32,after,old);
 return old-after;
}
'''
(r/'src/experimental/realized_receipt_core.zig').write_text(s)
s=(r/'src/experimental/shared_pace.zig').read_text().replace('shared_pace_core.zig','realized_receipt_core.zig');(r/'src/experimental/realized_receipt_pace.zig').write_text(s)
s=(r/'src/qa_shared_pace_cycles.zig').read_text().replace('experimental/shared_pace.zig','experimental/realized_receipt_pace.zig');(r/'src/qa_realized_receipt_cycles.zig').write_text(s)
