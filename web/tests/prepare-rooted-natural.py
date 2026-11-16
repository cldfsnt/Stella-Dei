"""Fixed two-site natural player journey, actual paid action, no environmental edits."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[2]
qa=(r/'web/tests/rooted-player-qa.txt').read_text()
a=qa.index('      const original=');z=qa.index('      const preseed=',a)
qa=qa[:a]+qa[z:]
qa=qa.replace('      if(arm==1)state.planet.microbeCells[6].cohorts[0].root_fraction=0;','')
qa=re.sub(r'\b6\b','point',qa)
qa=qa.replace('if(arm>1)return error.InvalidArm;','if(arm>1)return error.InvalidArm;const point:u32=if(arm==0)126 else 1845;')
qa=qa.replace('      const preseed=', '      const dep=state.planet.waterMass[point]*state.planet.getKmPerWaterMass()*1000;std.debug.assert(state.planet.temperature[point]>=293.15 and state.planet.temperature[point]<=313.15 and state.planet.landSoil[point]>0);std.debug.assert(if(arm==0)dep==0 else dep>0 and dep<0.02);Audit.emit("INITIAL_ENV",.{.cell=point,.depth_m=dep,.temperature=state.planet.temperature[point],.soil=state.planet.landSoil[point],.area=state.planet.getMeanPointArea()});\n      const preseed=')
s=(r/'web/tests/prepare-rooted-player.py').read_text().replace("b=t/'rooted-player'", "b=t/'rooted-natural'").replace("src=t/'rooted-founder/src'","src=t/'rooted-natural-owner/src'").replace("(r/'web/tests/rooted-player-qa.txt').read_text()",'qa')
exec(compile(s,str(r/'web/tests/prepare-rooted-player.py'),'exec'))
