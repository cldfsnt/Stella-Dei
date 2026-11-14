const std=@import("std");const M=@import("reserve_model.zig");
const Row=struct{time:f64,index:usize,dt:f32,temp:f32,depth:f32,light:f32,carbon:f32,oxygen:f32};
pub fn main()!void{
 const a=std.heap.page_allocator;const args=try std.process.argsAlloc(a);const bytes=try std.fs.cwd().readFileAlloc(a,args[1],16*1024*1024);
 var rows=std.ArrayList(Row).init(a);var lines=std.mem.tokenizeScalar(u8,bytes,'\n');
 while(lines.next())|line|{if(!std.mem.startsWith(u8,line,"RETENTION_TRACE,"))continue;var v=std.mem.splitScalar(u8,line,',');_=v.next();try rows.append(.{.time=try std.fmt.parseFloat(f64,v.next().?),.index=try std.fmt.parseInt(usize,v.next().?,10),.dt=try std.fmt.parseFloat(f32,v.next().?),.temp=try std.fmt.parseFloat(f32,v.next().?),.depth=try std.fmt.parseFloat(f32,v.next().?),.light=try std.fmt.parseFloat(f32,v.next().?),.carbon=try std.fmt.parseFloat(f32,v.next().?),.oxygen=try std.fmt.parseFloat(f32,v.next().?)});}
 for([_]usize{35503,6787,30111})|site|for([_]f32{285,303})|optimum|for([_]f32{0,0.5,1})|retention|for([_]bool{false,true})|enabled|{
 var cell=M.initialized(1);cell.cohorts[0]=.{.biomass=0.1,.support_mass=0.004,.organization=0.04,.structure=0.15,.optimum=optimum,.water_retention=retention,.lineage=1};
 const carbon0=M.carbon(cell);const nitrogen0=M.nutrientTotal(cell);
 var surface:f64=0;var vapor:f64=0;var exchange:f64=0;var fixed:f64=0;var recycled:f64=0;var dryfixed:f64=0;var uptake:f64=0;var peakerror:f64=0;var deathday:f64=-1;var n:usize=0;var dry:usize=0;var frost:usize=0;var warmdrylight:usize=0;
 for(rows.items)|r|{if(r.index!=site)continue;n+=1;const measured=@as(f64,r.depth)*1e6;exchange+=measured-surface;surface=measured;
 const previous=M.storedWater(cell);const f=M.step(&cell,.{.temperature=r.temp,.depth_km=r.depth,.light=r.light,.carbon_available=r.carbon,.oxygen_carbon_capacity=r.oxygen,.liquid_available=surface,.reserve_enabled=enabled},r.dt);
 surface+=f.water_returned-f.water_taken;vapor+=f.water_evaporated;fixed+=f.fixed;recycled+=f.recycled;uptake+=f.water_taken;
 if(r.depth==0){dry+=1;dryfixed+=f.fixed;if(previous==0)std.debug.assert(f.fixed==0);if(r.light>0 and r.temp>273.15)warmdrylight+=1;}
 if(r.temp<=273.15){frost+=1;std.debug.assert(f.fixed==0);}
 peakerror=@max(peakerror,@abs(surface+vapor+M.storedWater(cell)-exchange));
 std.debug.assert(surface>=-1e-8);std.debug.assert(M.validCell(cell,2));
 if(deathday<0 and M.biomass(cell)==0)deathday=r.time/86400;
 }
 const cerr=@abs(@as(f64,carbon0)+fixed-recycled-M.carbon(cell));const nerr=@abs(nitrogen0-M.nutrientTotal(cell));
 std.debug.assert(peakerror<1e-7 and cerr<0.0001 and nerr<0.0001);
 std.debug.print("REPLAY site={d} optimum={d} retention={d} reserve={} n={d} dry={d} frost={d} warm_dry_lit={d} final_biomass={d} fixed={d} dry_fixed={d} water_uptake={d} final_reserve={d} death_day={d} water_error={d} carbon_error={d} nutrient_error={d}\n",.{site,optimum,retention,enabled,n,dry,frost,warmdrylight,M.biomass(cell),fixed,dryfixed,uptake,M.storedWater(cell),deathday,peakerror,cerr,nerr});
 };
}
