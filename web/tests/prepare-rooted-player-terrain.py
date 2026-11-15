"""Same fixed rooted-player experiment; integration parity only, no new ecology scope."""
from pathlib import Path
r=Path(__file__).resolve().parents[2]
s=(r/'web/tests/prepare-rooted-player.py').read_text()
s=s.replace("b=t/'rooted-player'", "b=t/'rooted-player-terrain'")
# Do not supply the old QA full-refresh repair: validate actual action-time geometry.
s=s.replace("(r/'web/tests/rooted-player-qa.txt').read_text()", "(r/'web/tests/rooted-player-qa.txt').read_text().replace('state.planet.refreshTransformedPoints(state.axialTilt);var geometry_copy=', 'var geometry_copy=')")
exec(compile(s,str(r/'web/tests/prepare-rooted-player.py'),'exec'))
