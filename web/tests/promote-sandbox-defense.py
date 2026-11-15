#!/usr/bin/env python3
"""Explicit production allowlist for accepted defense candidate; no QA copies."""
from pathlib import Path
import shutil,sys
r=Path(__file__).resolve().parents[2];c=Path(sys.argv[1]).resolve()
files=['src/simulation/ecology.zig','src/simulation/foraging.zig','src/simulation/life.zig','src/simulation/planet.zig','src/toughness_mutation.zig','src/sandbox_defense.zig','src/save_schema.zig','src/save_game.zig','src/states/play.zig','src/main.zig','web/shell.html','web/build.sh','web/sandbox-defense.js']
for f in files:
 assert (c/f).is_file(),f
for f in files:shutil.copy2(c/f,r/f)
print('\n'.join(files))
