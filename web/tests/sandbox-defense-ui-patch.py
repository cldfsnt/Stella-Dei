#!/usr/bin/env python3
"""Isolated Play/main/web integration; never edits production checkout files."""
from pathlib import Path
import sys,shutil
r=Path(__file__).resolve().parents[2];src=Path(sys.argv[1]).resolve();web=src.parent/'web';shutil.copytree(r/'web',web,ignore=shutil.ignore_patterns('dist','tests'),dirs_exist_ok=True)
p=src/'states/play.zig';s=p.read_text();assert 'defensePlantKind:' not in s
s=s.replace('pub const PlayState = struct {','pub const PlayState = struct {\n    defensePlantKind:i32=-1,')
needle='        if (tool == .None or tool == .PlaceLife) return false;'
s=s.replace(needle,'''        if(self.planet.worldMode==.sandbox and tool==.PlaceVegetation and self.planet.sandboxDefense.enabled){
            if(!tap)return false;
            const receipt=@import("../sandbox_defense.zig").plantDefended(&self.planet,self.selectedPoint,if(self.defensePlantKind==1)0.5 else 0);
            self.mobileFeedback=switch(receipt.status){
                .planted=>if(self.defensePlantKind==1) "Tough founder planted: external cover added" else "Tender founder planted: external cover added",
                .occupied=>"Existing plants retained. Choose an empty patch",
                .water=>"Choose dry or shallow ground (at most 0.5 m water)",
                .disabled=>"Enable inherited defenses first",
                else=>"Planting refused; world unchanged",
            };self.mobileFeedbackSeconds=5;return receipt.status==.planted;
        }
'''+needle,1)
s=s.replace('if (ui.button(vg, game, name, x, y, bw, 44, name)) self.selectedTool = tool;','if (ui.button(vg, game, name, x, y, bw, 44, name)) {self.selectedTool = tool;self.defensePlantKind=if(self.planet.sandboxDefense.enabled)0 else -1;}')
s=s.replace('if (origin) "Seed" else "Plants",','if (origin) "Seed" else if(self.planet.sandboxDefense.enabled) (if(self.defensePlantKind==1) "Tough" else "Tender") else "Plants",')
s=s.replace('.PlaceVegetation => guidance.plantWarning(depth) orelse "Paint mode: drag to plant food",','.PlaceVegetation => if(self.planet.sandboxDefense.enabled) "Tap empty dry/shallow ground; existing plants retained" else guidance.plantWarning(depth) orelse "Paint mode: drag to plant food",')
# Exact previously rendered candidate helper, and exact zero-trait dispatch.
visual=(r.parent/'site-tmp/toughness-visual/src/states/play.zig').read_text();a=visual.index('    // Prescribed handling-resistance illustration');b=visual.index('    fn renderProducerGlyph(',a)
helper=visual[a:b];s=s.replace('    fn renderProducerGlyph(',helper+'    fn renderProducerGlyph(',1)
s=s.replace('renderProducerGlyph(vg,"branching",color);','renderToughnessGlyph(vg,self.planet.plantTraits[index].toughness,color);',1)
needle='                    mobileDetailLabel(vg, game, "Adapted to: {d:.1}°C", .{self.planet.plantTraits[point].optimum - 273.15}, px + 16, py + 232, pw - 32);'
s=s.replace(needle,needle+'\n                    if(self.planet.sandboxDefense.enabled)mobileDetailLabel(vg,game,"Handling resistance: {d:.3}",.{self.planet.plantTraits[point].toughness},px+16,py+262,pw-32);')
p.write_text(s)
p=src/'main.zig';s=p.read_text();a=s.index('var advance_json:')
s=s[:a]+'''var defense_json:[768]u8=undefined;
pub fn defenseSnapshot(state:?*PlayState,status:[]const u8)[*:0]const u8 {
 const v=state orelse return "{\\"status\\":\\"unavailable\\"}";
 var out=std.io.fixedBufferStream(&defense_json);
 const preview=@import("sandbox_defense.zig").previewPlantDefended(&v.planet,v.selectedPoint,if(v.defensePlantKind==1)0.5 else 0);
 std.json.stringify(.{.eligibility=@tagName(preview.status),.depth_m=preview.depth_m,.status=status,.world=PerformanceDetails.world_serial,.cell=v.selectedPoint,.mode=if(v.planet.worldMode==.sandbox) "sandbox" else "origin",.enabled=v.planet.sandboxDefense.enabled,.kind=v.defensePlantKind},.{},out.writer()) catch return "{}";
 const n=out.pos;defense_json[n]=0;return defense_json[0..n:0].ptr;
}
export fn stella_defense_status()[*:0]const u8 {return defenseSnapshot(webPlayState(),"ready");}
export fn stella_defense_action(world:u32,cell:u32,action:i32)[*:0]const u8 {
 const v=webEditableState() orelse return defenseSnapshot(null,"unavailable");
 if(world!=PerformanceDetails.world_serial or cell!=v.selectedPoint)return defenseSnapshot(v,"stale");
 if(v.planet.worldMode!=.sandbox)return defenseSnapshot(v,"wrong_mode");
 if(action==0){const receipt=@import("sandbox_defense.zig").enableDefenses(&v.planet);return defenseSnapshot(v,@tagName(receipt.status));}
 if(action==3){v.defensePlantKind=-1;v.selectedTool=.None;return defenseSnapshot(v,"cancelled");}
 if(action!=1 and action!=2)return defenseSnapshot(v,"invalid");
 if(!v.planet.sandboxDefense.enabled)return defenseSnapshot(v,"disabled");
 v.defensePlantKind=action-1;v.selectedTool=.PlaceVegetation;v.showPointDetails=false;v.showPlanetControl=false;v.showEscapeMenu=false;
 return defenseSnapshot(v,"selected");
}
''' +s[a:];p.write_text(s)
p=web/'build.sh';s=p.read_text().replace('_stella_world_mode,','_stella_defense_status,_stella_defense_action,_stella_world_mode,');s+='\ncp web/sandbox-defense.js web/dist/\n';p.write_text(s)
shutil.copy2(r/'web/tests/sandbox-defense-controller.js',web/'sandbox-defense.js')
p=web/'shell.html';s=p.read_text();needle='<button id="help-toggle">Sandbox guide</button></section>'
assert needle in s
panel='''<section id="sandbox-defense-panel" hidden><h3>Inherited plant defenses</h3><button id="defense-land">Find land</button><p id="defense-policy">Optional: enable rare inherited defense variation in future offspring worldwide. Tough plants grow and spread slower and take longer to graze. Existing plants stay unchanged. Save first to restore the earlier rules.</p><button id="defense-enable">Enable inherited defenses</button><div id="defense-choices" hidden><button id="defense-tender">Plant tender</button><button id="defense-tough">Plant tough</button><button id="defense-cancel">Cancel planting</button><p>Tap an empty dry or shallow patch (up to 0.5 m water). Adds a founder with 35% cover; not natural evolution. Existing plants are retained. Toughness does not guarantee survival.</p></div><p id="defense-status" role="status" aria-live="polite"></p></section>'''
s=s.replace(needle,panel+needle);s=s.replace('<script src="world-ecology.js"></script>','<script src="world-ecology.js"></script><script src="sandbox-defense.js"></script>')
needle='function syncWorldMode(){';s=s.replace(needle,'''const defenseUI=SandboxDefense.create({
 read:()=>{if(!Module.started||Module.failed)return null;return JSON.parse(Module.ccall('stella_defense_status','string',[],[]));},
 act:(world,cell,action)=>JSON.parse(Module.ccall('stella_defense_action','string',['number','number','number'],[world,cell,action])),
 render:(v,message)=>{document.getElementById('sandbox-defense-panel').hidden=!v||v.mode!=='sandbox';document.getElementById('defense-enable').hidden=!!v?.enabled;document.getElementById('defense-choices').hidden=!v?.enabled;document.getElementById('defense-status').textContent=(message||(v?.enabled?'Inherited defenses enabled. No automatic replanting.':'Classic rules: inherited defenses are off.'))+(v?.enabled?' Patch '+v.cell+': '+({eligible:'empty dry or shallow ground',occupied:'existing plants retained; choose an empty patch',water:'too deep; at most 0.5 m water',invalid:'invalid conditions',disabled:'defenses off'}[v.eligibility]||'refresh target')+'.':'');},
 focus:()=>{document.getElementById('more-menu').close();canvas.focus();}
});
document.getElementById('defense-land').onclick=()=>{const result=gameAction('_stella_focus_land');if(result===1){document.getElementById('more-menu').close();canvas.focus();}else document.getElementById('defense-status').textContent='No suitable land found. Use Land + or inspect water depth.';};
for(const [id,action]of [['defense-enable',0],['defense-tender',1],['defense-tough',2],['defense-cancel',3]])document.getElementById(id).onclick=()=>defenseUI.action(action);
function syncWorldMode(){defenseUI.refresh();''',1)
# Keep the complete Origin-only action and its explanation out of Sandbox.
s=s.replace('<button id="auto-seed-open" disabled>', '<div id="origin-auto-seed" hidden><button id="auto-seed-open" disabled>',1)
s=s.replace('No ongoing automatic seeding.</p>', 'No ongoing automatic seeding.</p></div>',1)
s=s.replace("const origin=gameAction('_stella_world_mode')===1;", "const origin=gameAction('_stella_world_mode')===1;document.getElementById('origin-auto-seed').hidden=!origin;",1)
p.write_text(s)
