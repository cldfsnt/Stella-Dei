//! Read-only current traits/soil. Never a claim of last-step uptake.
const std=@import("std");
var buffer:[2048]u8=undefined;
pub fn snapshot(state:anytype,world:u32)[*:0]const u8{
 var out=std.io.fixedBufferStream(buffer[0..buffer.len-1]);
 if(state)|s|{
  const p=&s.planet;const cell=s.selectedPoint;
  if(p.landBeta.enabled and p.worldMode==.origin and cell<p.microbeCells.len and cell<p.landSoil.len){
   const Entry=struct{id:[]const u8,living:bool,fraction:f32,root_tissue_kg_c_m2:f64};var entries:[4]Entry=undefined;var ids:[4][20]u8=undefined;
   if(!std.math.isFinite(p.landSoil[cell]))return "{\"status\":\"unavailable\"}";
   for(p.microbeCells[cell].cohorts,0..)|c,i|{if(!std.math.isFinite(c.root_fraction) or !std.math.isFinite(c.support_mass))return "{\"status\":\"unavailable\"}";entries[i]=.{.id=std.fmt.bufPrint(&ids[i],"{d}",.{c.lineage}) catch "",.living=c.biomass>0 and c.lineage!=0,.fraction=c.root_fraction,.root_tissue_kg_c_m2=@as(f64,c.support_mass)*c.root_fraction};}
   std.json.stringify(.{.status=if(p.landBeta.physiology_law==3)"wetlands" else "historical_beta",.enabled=true,.world_serial=world,.cell=cell,.physiology_law=p.landBeta.physiology_law,.soil_kg_m2=p.landSoil[cell],.root_allocations=entries,.receipt_available=false},.{},out.writer()) catch return "{}";
  }else{std.json.stringify(.{.status="legacy",.enabled=false,.world_serial=world,.cell=cell,.receipt_available=false},.{},out.writer()) catch return "{}";}
 }else{std.json.stringify(.{.status="unavailable",.enabled=false,.world_serial=world,.receipt_available=false},.{},out.writer()) catch return "{}";}
 buffer[out.pos]=0;return @ptrCast(&buffer);
}
