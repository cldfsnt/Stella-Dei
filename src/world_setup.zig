const std=@import("std");
/// New-world configuration only. Not a command to alter the active planet.
pub const Preset=enum{random,continents};
pub const Choice=struct{
    preset:Preset=.random,
    pub fn select(self:*Choice,preset:Preset)void{self.preset=preset;}
};
pub const Layout=struct{left:f32,width:f32,top:f32,button_height:f32=44,
    pub fn at(width:f32,height:f32)Layout{
        const w=@min(@max(width-24,0),320);
        // Fit a 224px control stack below the logo, including short landscape.
        return .{.left=(width-w)/2,.width=w,.top=@max(66,@min(height*0.32,height-230))};
    }
};
test "selection is explicit, reversible and does not generate a world"{
 var choice=Choice{};try std.testing.expectEqual(Preset.random,choice.preset);
 choice.select(.continents);try std.testing.expectEqual(Preset.continents,choice.preset);
 choice.select(.random);try std.testing.expectEqual(Preset.random,choice.preset);
}
test "mobile menu controls stay within supported portrait and landscape sizes"{
 for([_][2]f32{.{360,640},.{390,844},.{640,360},.{844,390},.{320,568}})|size|{
 const l=Layout.at(size[0],size[1]);try std.testing.expect(l.left>=0 and l.left+l.width<=size[0]);
 try std.testing.expect(l.top+220<=size[1]);try std.testing.expect(l.button_height>=44);
 }
}
