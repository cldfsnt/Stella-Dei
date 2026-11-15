// QA-only old wire adapter: reflect actual legacy fields without beta extensions.
fn legacyWire(value:anytype,writer:anytype) @TypeOf(writer.*).Error!void {
 const T=@TypeOf(value);
 if(comptime T==SavedCell){
  // Match the original cell wire contract: exactly one cohort encoding field.
  try writer.beginObject();
  if(value.sparse)|entries|{try writer.objectField("sparse");try legacyWire(entries,writer);}
  else {try writer.objectField("cohorts");try legacyWire(value.cohorts,writer);}
  try writer.objectField("nutrient");try writer.write(value.nutrient);
  try writer.objectField("detritus");try writer.write(value.detritus);
  try writer.objectField("rng");try writer.write(value.rng);
  try writer.endObject();return;
 }
 switch(@typeInfo(T)){
  .Optional=>if(value)|v|{try legacyWire(v,writer);}else try writer.write(null),
  .Struct=>{
   try writer.beginObject();
   inline for(std.meta.fields(T))|field|{
    if(comptime std.mem.eql(u8,field.name,"root_fraction")){
     std.debug.assert(@as(u32,@bitCast(@field(value,field.name)))==0);
    }else if(comptime !std.mem.eql(u8,field.name,"beta_origin")){
     try writer.objectField(field.name);try legacyWire(@field(value,field.name),writer);
    }
   }
   try writer.endObject();
  },
  .Array=>{try writer.beginArray();for(value)|v|try legacyWire(v,writer);try writer.endArray();},
  .Pointer=>|ptr|{if(comptime ptr.size==.Slice and ptr.child!=u8){try writer.beginArray();for(value)|v|try legacyWire(v,writer);try writer.endArray();}else try writer.write(value);},
  else=>try writer.write(value),
 }
}
