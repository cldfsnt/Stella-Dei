from pathlib import Path
import sys,shutil
r=Path(__file__).resolve().parents[2];dst=Path(sys.argv[1]);assert (dst/'main.zig').exists();assert not (dst/'combined_recovery.zig').exists();shutil.copyfile(r/'web/tests/combined-recovery.zig',dst/'combined_recovery.zig');p=dst/'main.zig';p.write_text(p.read_text()+(r/'web/tests/combined-recovery-api.txt').read_text())
