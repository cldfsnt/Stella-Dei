#!/usr/bin/env python3
"""Real MainMenu button smoke: only platform/audio/entrypoint adapters."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2]
out=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/stella-origin-menu-src')
subprocess.run([sys.executable,str(root/'web/tests/egl-prepare.py'),str(out),'--mobile','--paused'],check=True)
p=out/'main.zig'
s=p.read_text().replace('nosuspend game.setState(PlayState);','nosuspend game.setState(MainMenuState);')
s=s.replace('            const i = state.selectedPoint;', '            std.debug.print("MENU_RESULT mode={s} plants={d} animals={d}\\n", .{@tagName(state.planet.worldMode),state.planet.vegetation[state.selectedPoint],state.planet.lifeforms.items.len});\n            const i = state.selectedPoint;')
p.write_text(s)
p=out/'states/main_menu.zig'
p.write_text(p.read_text().replace('@import("builtin").target.cpu.arch == .wasm32','true'))
