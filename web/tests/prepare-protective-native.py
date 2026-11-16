from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];t=r.parent/'site-tmp';b=t/'protective-native';o=b/'src';src=t/'protective-integration/src';assert not o.exists();shutil.copytree(src,o)
(b/'owner-hashes.json').write_text(json.dumps({str(p.relative_to(src)):hashlib.sha256(p.read_bytes()).hexdigest()for p in src.rglob('*.zig')},indent=2))
p=o/'states/play.zig';s=p.read_text().replace('var randomPrng = std.rand.DefaultPrng.init(@as(u64, @bitCast(std.time.milliTimestamp())));','var randomPrng = std.rand.DefaultPrng.init(42);').replace('const subdivisions: usize = if (@import("builtin").target.cpu.arch == .wasm32 or @import("builtin").mode == .Debug) 6 else 7;','const subdivisions: usize = 6;').replace('@import("builtin").target.cpu.arch == .wasm32','true').replace('@import("builtin").target.cpu.arch != .wasm32','false');p.write_text(s)
p=o/'audio.zig';p.write_text(p.read_text().replace('if (c.ma_engine_init(null, engine)','var config = c.ma_engine_config_init();config.noDevice=c.MA_TRUE;config.channels=2;config.sampleRate=48000;\n        if (c.ma_engine_init(&config, engine)'))
p=o/'loop.zig';p.write_text(p.read_text().replace('const is_web = @import("builtin").target.cpu.arch == .wasm32;','const is_web = true;'))
p=o/'save_game.zig';p.write_text(p.read_text().replace('/wetlands-saves',str(b/'disk/wetlands-saves')))
p=o/'main.zig';s='extern fn qa_capture(path:[*:0]const u8) void; extern fn qa_pointer(x:f64,y:f64,down:c_int) void;\n'+p.read_text();s=s.replace('if (!is_web or !web_initialized or !game.state_init)','if (!web_initialized or !game.state_init)').replace('if(!is_web or !web_initialized)','if(!web_initialized)').replace('nosuspend game.setState(MainMenuState);','game.startOriginNext=true;nosuspend game.setState(PlayState);').replace('nosuspend game.setState(SplashScreenState);','game.startOriginNext=true;nosuspend game.setState(PlayState);');a=s.index('    std.log.debug("Creating update loop job.."');e=s.index('\nconst expect =',a);s=s[:a]+(r/'web/tests/protective-native-qa.txt').read_text().replace('OUTPUT',str(b)).replace('INPUT',str(t/'wetlands-day21/day-21.json'))+s[e:];p.write_text(s)

(b/"source-hashes.json").write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob("*.zig")},indent=2))

p=o/"combined_recovery.zig";p.write_text(p.read_text().replace("/wetlands-saves",str(b/"disk/wetlands-saves")))
