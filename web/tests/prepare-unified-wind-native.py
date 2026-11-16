from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];t=r.parent/'site-tmp'
for kind,owner in [('reference','wind-dispersal'),('candidate','unified-game')]:
 b=t/('unified-wind-'+kind);o=b/'src';src=t/owner/'src';assert not o.exists();shutil.copytree(src,o)
 (b/'owner-hashes.json').write_text(json.dumps({str(p.relative_to(src)):hashlib.sha256(p.read_bytes()).hexdigest()for p in src.rglob('*.zig')},indent=2))
 p=o/'states/play.zig';s=p.read_text().replace('var randomPrng = std.rand.DefaultPrng.init(@as(u64, @bitCast(std.time.milliTimestamp())));','var randomPrng = std.rand.DefaultPrng.init(42);').replace('const subdivisions: usize = if (@import("builtin").target.cpu.arch == .wasm32 or @import("builtin").mode == .Debug) 6 else 7;','const subdivisions: usize = 6;').replace('@import("builtin").target.cpu.arch == .wasm32','true').replace('@import("builtin").target.cpu.arch != .wasm32','false');p.write_text(s)
 p=o/'audio.zig';p.write_text(p.read_text().replace('if (c.ma_engine_init(null, engine)','var config = c.ma_engine_config_init();config.noDevice=c.MA_TRUE;config.channels=2;config.sampleRate=48000;\n        if (c.ma_engine_init(&config, engine)'))
 p=o/'loop.zig';p.write_text(p.read_text().replace('const is_web = @import("builtin").target.cpu.arch == .wasm32;','const is_web = true;'))
 for name in ['save_game.zig','combined_recovery.zig']:
  p=o/name
  if p.exists():
   s=p.read_text()
   for v in ['/wetlands-saves','/wind-saves','/saves']:s=s.replace('"'+v,'"'+str(b/'disk')+v)
   p.write_text(s)
 p=o/'main.zig';s=p.read_text().replace('nosuspend game.setState(MainMenuState);','game.startOriginNext=true;nosuspend game.setState(PlayState);').replace('nosuspend game.setState(SplashScreenState);','game.startOriginNext=true;nosuspend game.setState(PlayState);');a=s.index('    std.log.debug("Creating update loop job.."');e=s.index('\nconst expect =',a);s=s[:a]+(r/'web/tests/unified-wind-qa.txt').read_text().replace('OUTPUT',str(b)).replace('INPUT',str(t/'wind-bulk/pioneer-day7.json'))+s[e:];
 if kind=='reference':s='\n'.join(line for line in s.split('\n') if 'if(comptime @hasField' not in line)
 p.write_text(s)
 (b/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},indent=2))
