"""Narrow navigation/identity patch. No ecology or historical load changes."""
from pathlib import Path
import sys
p=Path(sys.argv[1])
def replace(file,a,b):
 f=p/file;s=f.read_text();assert s.count(a)==1,(file,a);f.write_text(s.replace(a,b))
replace('states/main_menu.zig','    upload_no: u8 = 0,','    upload_no: u8 = 0,\n    advancedWorlds: bool = false,')
replace('states/main_menu.zig','"Origin: simple life")) {\n                game.startOriginNext = true;\n                game.setState(PlayState);','"Play: evolving world")) {\n                _ = @import("../main.zig").combinedOptionsNewForGame(game, @import("../performance_details.zig").world_serial, true, true);')
replace('states/main_menu.zig','            if (ui.button(vg, game, "web-new-planet", x, startY + 62, width, 52, "Sandbox: plants & rabbits")) {','            if (ui.button(vg, game, "web-advanced-worlds", x, startY + 62, width, 44, if(self.advancedWorlds) "Advanced worlds: hide" else "Advanced worlds")) self.advancedWorlds = !self.advancedWorlds;\n            if (self.advancedWorlds and ui.button(vg, game, "web-new-planet", x, startY + 116, width, 44, "Sandbox: plants & rabbits")) {')
replace('states/main_menu.zig','                game.startOriginNext = false;\n                game.setState(GameIntroState);','                game.startOriginNext = false;game.startWetlandsNext=false;game.startCombinedNext=false;game.startCalmNext=false;game.startProtectionNext=false;\n                game.setState(GameIntroState);')
replace('states/main_menu.zig','setupY+124,"New planets only; saved worlds unchanged"','setupY+124,"New planets only; saved worlds unchanged"') if False else None
replace('states/main_menu.zig','startY+124,"New planets only; saved worlds unchanged"','startY+(if(self.advancedWorlds) @as(f32,170) else @as(f32,116)),"New planets only; saved worlds unchanged"')
replace('combined_view.zig',' if(p.windDispersal.enabled)return if(p.worldMode==.origin and p.landBeta.valid() and p.landBeta.enabled and p.landBeta.physiology_law==3)(if(p.groundThermalLaw==1)14 else 13) else 0;',' if(p.windDispersal.enabled){if(p.worldMode!=.origin or !p.landBeta.valid())return 0;if(!p.landBeta.enabled)return if(p.groundThermalLaw==0)11 else 0;return if(p.landBeta.physiology_law==3)(if(p.groundThermalLaw==1)14 else 13) else 0;}')
replace('combined_view.zig','else if(writer==10)"wetlands"','else if(writer==11)"wind" else if(writer==10)"wetlands"')

replace('states/main_menu.zig','    advancedWorlds: bool = false,','    advancedWorlds: bool = false,\n    newWorldBusy: bool = false,')
replace('states/main_menu.zig','                _ = @import("../main.zig").combinedOptionsNewForGame(game, @import("../performance_details.zig").world_serial, true, true);','                const result = @import("../main.zig").combinedOptionsNewForGame(game, @import("../performance_details.zig").world_serial, true, true);\n                if(result != 1) self.newWorldBusy = result == -3;')
replace('states/main_menu.zig','"New planets only; saved worlds unchanged"','if(self.newWorldBusy) "Preparing world... try again shortly" else "New planets only; saved worlds unchanged"')
