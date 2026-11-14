//! Isolated functional organization prototype, not production biology.
//! Carbon pools kg C/m²; support and frond are real tissue, not visual counters.
const std = @import("std");
const N:f64=0.1;
const Tissue=struct {
    frond:f64=0, support:f64=0, allocation:f64=0,
    credit:f64=0, lineage:u64=0, parent:u64=0, generation:u32=0,
    fn mass(c:Tissue) f64{return c.frond+c.support;}
    fn height(c:Tissue) f64{return @min(0.5,0.2*c.support/(c.frond+0.01));}
};
const World=struct {
    colonies:[4]Tissue=.{.{},.{},.{},.{}}, carbon:f64=10, oxygen:f64=10,
    nutrient:f64=1, detritus:f64=0, fixed:f64=0, respired:f64=0,
    broken:f64=0, births:u32=0, next:u64=2, rng:u64=42,
    fn organic(w:World) f64{var x=w.detritus;for(w.colonies)|c|x+=c.mass();return x;}
    fn totalC(w:World) f64{return w.carbon+w.organic();}
    fn totalN(w:World) f64{var x=w.nutrient;for(w.colonies)|c|x+=N*c.mass();return x;}
};
const Environment=struct{depth:f64=0.3,light:f64=1,disturbance:f64=0};
const Flux=struct{photons:f64=0,fixed:f64=0};
fn initialize(allocation:f64) World {
    var w:World=.{};const mass=0.08;
    w.colonies[0]=.{.frond=mass*(1-allocation),.support=mass*allocation,.allocation=allocation,.lineage=1};
    w.carbon-=mass;w.nutrient-=mass*N;return w;
}
fn random(w:*World) f64 {w.rng=w.rng*%6364136223846793005+%1442695040888963407;return @as(f64,@floatFromInt(w.rng>>11))/9007199254740992.0;}
fn step(w:*World,e:Environment,days:f64) Flux {
    var result:Flux=.{};
    if(days<=0 or !std.math.isFinite(days))return result;
    // Maintenance is oxygen-limited respiration; physical loss becomes detritus.
    var requested_upkeep:f64=0;for(w.colonies)|c|requested_upkeep+=(c.frond*0.03+c.support*0.12)*days;
    const upkeep_scale=if(requested_upkeep>0)@min(1,w.oxygen/requested_upkeep) else 0;
    for(&w.colonies)|*c| {
        const old=c.mass();if(old<=0)continue;
        const upkeep=(c.frond*0.03+c.support*0.12)*days*upkeep_scale;
        const cost=@min(old,upkeep);const remaining=1-cost/old;
        c.frond*=remaining;c.support*=remaining;
        w.oxygen-=cost;w.carbon+=cost;w.nutrient+=cost*N;w.respired+=cost;
        const exposure=if(e.depth<0) 1 else std.math.clamp((c.height()-e.depth)/0.1,0,1);
        const hazard=0.01+exposure*3+@max(0,e.disturbance)*c.height()*8;
        const loss=c.mass()*(1-@exp(-hazard*days));const fraction=if(c.mass()>0)loss/c.mass() else 0;
        c.frond*=1-fraction;c.support*=1-fraction;
        w.detritus+=loss;w.nutrient+=loss*N;w.broken+=loss;
    }
    // Highest fronds receive light first. Equal-height colonies share a layer,
    // eliminating array-order privilege. Unabsorbed light reaches lower layers.
    var order=[_]usize{0,1,2,3};
    for(0..4)|i|for(i+1..4)|j|{if(w.colonies[order[j]].height()>w.colonies[order[i]].height())std.mem.swap(usize,&order[i],&order[j]);};
    var light=@max(0,e.light);var previous=@max(0,e.depth);var start:usize=0;
    while(start<4){
        const height=w.colonies[order[start]].height();var end=start+1;
        while(end<4 and @abs(w.colonies[order[end]].height()-height)<1e-10): (end+=1){}
        light*=@exp(-@max(0,previous-height)/3.0);previous=height;
        var leaves:f64=0;for(order[start..end])|i|leaves+=w.colonies[i].frond;
        const absorbed=light*(1-@exp(-20*leaves));light-=absorbed;
        result.photons+=absorbed;
        if(leaves>0 and e.depth>=0){
          const layer_growth=@min(0.15*absorbed*days,@min(w.carbon,w.nutrient/N));
          for(order[start..end])|i|{
            var c=&w.colonies[i];const growth=layer_growth*c.frond/leaves;
            c.frond+=growth*(1-c.allocation);c.support+=growth*c.allocation;c.credit+=growth;
            w.carbon-=growth;w.oxygen+=growth;w.nutrient-=growth*N;w.fixed+=growth;result.fixed+=growth;
        }}
        start=end;
    }
    const recycled=@min(w.oxygen,w.detritus*(1-@exp(-0.05*days)));
    w.detritus-=recycled;w.carbon+=recycled;w.oxygen-=recycled;w.respired+=recycled;
    return result;
}
fn reproduce(w:*World,index:usize) bool {
    const parent=w.colonies[index];if(parent.mass()<0.04 or parent.credit<0.03)return false;
    var empty:?usize=null;for(w.colonies,0..)|c,i|if(c.mass()==0){empty=i;break;};
    const slot=empty orelse return false;const fraction=0.01/parent.mass();
    var child=parent;child.frond*=fraction;child.support*=fraction;
    child.allocation=std.math.clamp(parent.allocation+(random(w)-0.5)*0.24,0,0.7);
    child.credit=0;child.parent=parent.lineage;child.lineage=w.next;child.generation=parent.generation+1;
    w.next+=1;w.births+=1;w.colonies[index].frond-=child.frond;w.colonies[index].support-=child.support;
    w.colonies[index].credit-=0.03;w.colonies[slot]=child;return true;
}
test "finite light carbon nutrients and donor-funded inherited tissue" {
    var w=initialize(0);const carbon=w.totalC();const nutrient=w.totalN();
    for(0..240)|_|{const f=step(&w,.{},0.1);try std.testing.expect(f.photons<=1.0000001);try std.testing.expect(f.fixed<=0.0150001);_=reproduce(&w,0);}
    try std.testing.expect(w.births>0);var changed=false;
    for(w.colonies)|c|if(c.parent==1 and c.allocation>0 and c.support>0){changed=true;};
    try std.testing.expect(changed);
    try std.testing.expectApproxEqAbs(carbon,w.totalC(),1e-10);try std.testing.expectApproxEqAbs(nutrient,w.totalN(),1e-10);
    std.debug.print("COLONIAL births={d} fixed={d} carbon_error={e}\n",.{w.births,w.fixed,@abs(carbon-w.totalC())});
}
test "support has context-dependent benefit and cost not a free upgrade" {
    var structured=initialize(0.4);var flat=initialize(0);
    for(0..200)|_|{_=step(&structured,.{.depth=0.3},0.1);_=step(&flat,.{.depth=0.3},0.1);}
    std.debug.print("OPEN structured={d} flat={d}\n",.{structured.colonies[0].mass(),flat.colonies[0].mass()});
    try std.testing.expect(structured.colonies[0].mass()<flat.colonies[0].mass());
    var crowded=initialize(0.4);crowded.colonies[1]=.{.frond=0.08,.lineage=2};crowded.carbon-=0.08;crowded.nutrient-=0.008;
    for(0..200)|_|_=step(&crowded,.{.depth=0.3},0.1);
    std.debug.print("CROWDED structured={d} flat={d}\n",.{crowded.colonies[0].mass(),crowded.colonies[1].mass()});
    try std.testing.expect(crowded.colonies[0].mass()>crowded.colonies[1].mass());
}
test "water and disturbance act on actual tissue and recycle damage" {
    var w=initialize(0.4);for(0..100)|_|_=step(&w,.{},0.1);
    const before=w.colonies[0].mass();const carbon=w.totalC();const nutrient=w.totalN();const broken=w.broken;
    for(0..20)|_|_=step(&w,.{.depth=0,.disturbance=2},0.1);
    try std.testing.expect(w.colonies[0].mass()<before and w.broken>broken);
    try std.testing.expectApproxEqAbs(carbon,w.totalC(),1e-10);try std.testing.expectApproxEqAbs(nutrient,w.totalN(),1e-10);
    const injured=w.colonies[0].mass();for(0..200)|_|_=step(&w,.{},0.1);
    try std.testing.expect(w.colonies[0].mass()>injured);
    std.debug.print("DAMAGE before={d} injured={d} recovered={d}\n",.{before,injured,w.colonies[0].mass()});
}
test "founder without support yields a functional reproducing organized descendant" {
    var nursery=initialize(0);
    for(0..100)|_|{_=step(&nursery,.{},0.1);_=reproduce(&nursery,0);}
    var daughter:?Tissue=null;
    for(nursery.colonies)|c|{if(c.parent==1 and c.allocation>0){daughter=c;break;}}
    const inherited=daughter orelse return error.NoInheritedAllocation;
    try std.testing.expect(inherited.support>0 and inherited.generation==1);
    var outcomes:[2]f64=undefined;
    for(0..2)|control|{
        var w:World=.{};w.next=100;w.colonies[0]=inherited;
        if(control==1){w.colonies[0].frond+=w.colonies[0].support;w.colonies[0].support=0;w.colonies[0].allocation=0;}
        w.colonies[1]=.{.frond=0.08,.lineage=99};
        w.carbon-=w.organic();w.nutrient-=(w.organic()*N);
        const carbon=w.totalC();const nutrients=w.totalN();
        for(0..300)|_|_=step(&w,.{},0.1);
        outcomes[control]=w.colonies[0].mass();
        if(control==0){
            try std.testing.expect(reproduce(&w,0));
            try std.testing.expect(w.colonies[2].generation==2 and w.colonies[2].parent==inherited.lineage);
            try std.testing.expect(w.colonies[2].support>0);
        }
        try std.testing.expectApproxEqAbs(carbon,w.totalC(),1e-10);
        try std.testing.expectApproxEqAbs(nutrients,w.totalN(),1e-10);
    }
    std.debug.print("INHERITED allocation={d} support={d} organized={d} disabled={d} generation2=true\n",.{inherited.allocation,inherited.support,outcomes[0],outcomes[1]});
    try std.testing.expect(outcomes[0]>outcomes[1]);
}
test "equal-height light sharing has no array-order advantage and resources limit growth" {
    var w=initialize(0);w.colonies[1]=w.colonies[0];w.carbon-=0.08;w.nutrient-=0.008;
    for(0..100)|_|_=step(&w,.{},0.1);
    try std.testing.expectApproxEqAbs(w.colonies[0].mass(),w.colonies[1].mass(),1e-12);
    w.carbon=0;const no_carbon=step(&w,.{.light=1},0.1);
    // Maintenance can supply a little carbon, but there is no unbounded source.
    try std.testing.expect(no_carbon.fixed<=w.respired);
    w.nutrient=0;const n_before=w.totalN();_=step(&w,.{},0.1);
    try std.testing.expectApproxEqAbs(n_before,w.totalN(),1e-10);
}
