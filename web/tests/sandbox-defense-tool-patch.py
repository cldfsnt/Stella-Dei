#!/usr/bin/env python3
"""Narrow follow-up on already prepared isolated integration, never production."""
from pathlib import Path
import sys
root=Path(sys.argv[1]);p=root/'states/play.zig';s=p.read_text()
old='if (ui.button(vg, game, name, x, y, bw, 44, name)) {self.selectedTool = tool;self.defensePlantKind=if(self.planet.sandboxDefense.enabled)0 else -1;}'
assert old in s
s=s.replace(old,'if (ui.button(vg, game, name, x, y, bw, 44, name)) self.selectGameTool(tool);')
needle='    pub fn testAction(self: *PlayState, tool_id: i32) bool {'
s=s.replace(needle,'''    pub fn selectGameTool(self: *PlayState, tool: GameTool) void {
        self.selectedTool = tool;
        if (tool == .PlaceVegetation and self.planet.worldMode == .sandbox and self.planet.sandboxDefense.enabled and (self.defensePlantKind < 0 or self.defensePlantKind > 1)) self.defensePlantKind = 0;
    }

'''+needle)
# Desktop/native legacy toolbar shares the same choice rule.
start=s.index('            if (ui.toolButton(vg, game, "no-tool"');end=s.index('\n        if (self.debug_showMoreInfo)',start)
part=s[start:end]
import re
part=re.sub(r'self.selectedTool = (\.[A-Za-z]+);',r'self.selectGameTool(\1);',part)
s=s[:start]+part+s[end:];s=s.replace('Handling resistance: {d:.3}','Plant toughness: {d:.3}');p.write_text(s)
p=root/'main.zig';s=p.read_text().replace('v.defensePlantKind=action-1;v.selectedTool=.PlaceVegetation;','v.defensePlantKind=action-1;v.selectGameTool(.PlaceVegetation);');p.write_text(s)
