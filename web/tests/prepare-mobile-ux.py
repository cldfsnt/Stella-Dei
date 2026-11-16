#!/usr/bin/env python3
"""Frontend only: preserve controller IDs/transaction code, replace navigation chrome."""
from pathlib import Path
import re, shutil
R=Path(__file__).resolve().parents[2]; W=R.parent/'site-tmp/mobile-ux/web'; BASE=R.parent/'site-tmp/unified-ui/web'
s=(BASE/'shell.html').read_text()
s=s.replace('</head>','<link rel="stylesheet" href="mobile-navigation.css"></head>',1)
dock='<nav id="mobile-dock" aria-label="Planet navigation">'+''.join(f'<button id="dock-{id}" type="button" aria-label="{label}"'+(' aria-expanded="false" aria-haspopup="dialog"' if id!='pause' else '')+f'><span class="dock-icon" aria-hidden="true">{icon}</span><span class="dock-label">{label}</span></button>' for id,label,icon in [('pause','Play','▶'),('speed','Speed','◷'),('seed','Seed','♧'),('god','God','✦'),('stats','Stats','▥'),('world','World','◎')])+'</nav>'
s=s.replace('<div id="help">',dock+'<p id="mobile-status" role="status"></p><div id="mobile-brush" hidden><span id="mobile-brush-label"></span><button id="mobile-brush-cancel">Explore</button></div><div id="help">',1)
s=s.replace('<nav id="menu-groups"','<nav hidden id="menu-groups"',1)
s=s.replace('Pause above the planet','Play / Pause in the bottom dock').replace('Tools → Speed → Speed / fast-forward','Speed').replace('More → God tools','God').replace('Tools → World','World')
s=s.replace('Tap menu buttons and the tool buttons inside the game. Choose a tool, then touch the planet to use it.','Use the bottom dock. God opens deliberate tools; choose a brush, then touch the planet. Explore cancels the brush.')
s=s.replace('Pause, settings and tool details are now in the game, above the planet.','Pause, speed and world controls are in the bottom dock.')
s=s.replace('function openToolGroup(group){','function openToolGroup(group){document.getElementById("more-title").textContent=({plant:"Seed life",observe:"Life on this planet",world:"Your world"})[group]||"Planet";',1)
# Existing dialog actions and cancellation listeners stay authoritative.
s=s.replace('</script>{{{ SCRIPT }}}','</script><script src="mobile-navigation.js"></script><script src="mobile-navigation-bindings.js"></script>{{{ SCRIPT }}}',1)
s=s.replace("function showWelcome(){if(!welcomeSeen())document.getElementById('welcome-tip').hidden=false;}","function showWelcome(){document.getElementById('welcome-tip').hidden=true;}")
s=s.replace("document.getElementById('world-ecology-readout').textContent=text;","document.getElementById('world-ecology-readout').textContent=text;const compact=document.getElementById('mobile-community-total');if(compact){const lines=text.split('\\n');compact.textContent=lines.filter((line,i)=>i===0||/births.*deaths|^Recent events unavailable/.test(line)).map(line=>line.replace(/Living growth forms.*$/, '').replace(/by summed biomass.*$/, '')).join(' ');}")
(W/'shell.html').write_text(s)
for f in ['mobile-navigation.css','mobile-navigation.js','mobile-navigation-bindings.js']:
 if (R/'web'/f).exists():shutil.copy2(R/'web'/f,W/f)
print(W/'shell.html')

# Only intentionally changed chrome assertions; retain all rabbit rendering/purity checks.
p=W/'tests/rabbit-marker-scale.test.cjs'
t=(BASE/'tests/rabbit-marker-scale.test.cjs').read_text().replace("assert(block.includes('y > height - 90'));", "assert(block.includes('y > height - self.mobileBottomInset()-6'));assert(s.includes('if(!shell.enabled)return 84;'));")
p.write_text(t)
p=W/'tests/shell.test.cjs'
t=(BASE/'tests/shell.test.cjs').read_text().replace("assert.equal(el('welcome-tip').hidden,false)","assert.equal(el('welcome-tip').hidden,true)")
p.write_text(t)

p=W/'build.sh'
b=p.read_text();line='cp web/mobile-navigation.js web/mobile-navigation-bindings.js web/mobile-navigation.css web/dist/'
if line not in b:p.write_text(b+'\n'+line+'\n')
