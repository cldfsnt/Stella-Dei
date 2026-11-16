from pathlib import Path
import shutil,subprocess,sys
r=Path(__file__).resolve().parents[2];out=Path(sys.argv[1]).resolve();assert not out.exists()
shutil.copytree(r.parent/'site-tmp/unified-game/src',out)
subprocess.run(['patch','-p1','-i',str(r/'web/tests/mobile-native.patch')],cwd=out,check=True)
