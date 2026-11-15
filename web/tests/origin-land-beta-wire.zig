// QA-only old wire adapter: reflect actual legacy fields without beta extensions.
fn legacyWire(value:anytype,writer:anytype) @TypeOf(writer.*).Error!void {
 const T=@TypeOf(value);
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
