from pathlib import Path
import shutil,subprocess,sys
r=Path(__file__).resolve().parents[2];out=Path(sys.argv[1]) if len(sys.argv)>1 else r.parent/'site-tmp/wind-dispersal-rebuilt';assert not out.exists();shutil.copytree(r/'src',out/'src')
subprocess.run(['patch','-p1','-d',str(out)],input=(r/'web/tests/wind-core.patch').read_bytes(),check=True)
for n in ['wind_genetics.zig','wind_packet.zig','wind_audit.zig']:shutil.copy2(r/'web/tests'/('prototype-'+n),out/'src/simulation'/n)
shutil.copy2(r/'src/experimental/wind_dispersal.zig',out/'src/simulation/wind_dispersal.zig')
