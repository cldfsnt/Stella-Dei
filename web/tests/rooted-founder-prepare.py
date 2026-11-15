from pathlib import Path
import shutil,sys
src=Path(sys.argv[1]);dst=Path(sys.argv[2]);assert not dst.exists();shutil.copytree(src,dst)
shutil.copyfile(Path(__file__).with_name('rooted-founder-helper.zig'),dst/'rooted_founder.zig')
print(dst)

p=dst/"main.zig";p.write_text(p.read_text()+Path(__file__).with_name("rooted-founder-api.txt").read_text())

p=dst/"save_game.zig";s=p.read_text().replace('    @import("world_ecology.zig").reset();','    @import("rooted_founder.zig").invalidate();\n    @import("world_ecology.zig").reset();',1);p.write_text(s)
