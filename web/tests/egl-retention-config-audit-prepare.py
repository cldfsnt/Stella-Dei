"""Independent config-only adversarial native fixture; copy frozen candidate, no edits to it."""
from pathlib import Path
import shutil,sys,hashlib,json
src=Path(sys.argv[1]);out=Path(sys.argv[2]);shutil.copytree(src,out,dirs_exist_ok=True)
p=out/'main.zig';s=p.read_text();needle='          const keys=[_]u64{0,1,42};';assert s.count(needle)==1
extra=r'''
          for([_]bool{false,true})|enabled|{
            var gate_arena=std.heap.ArenaAllocator.init(allocator);defer gate_arena.deinit();const ga=gate_arena.allocator();
            try saves.apply(state,baseline.value);state.planet.retentionMutation=.{.law=1,.enabled=enabled,.stream_seed=std.math.maxInt(u64)};
            const wire=try std.json.stringifyAlloc(ga,try saves.capture(ga,state),.{});const loaded=try std.json.parseFromSlice(saves.schema.Save,ga,wire,.{.allocate=.alloc_always});
            state.planet.retentionMutation=.{};try saves.apply(state,loaded.value);
            std.debug.assert(state.planet.retentionMutation.stream_seed==std.math.maxInt(u64) and state.planet.retentionMutation.enabled==enabled and state.planet.retentionMutation.law==1);
            std.debug.assert(std.mem.eql(u8,wire,try std.json.stringifyAlloc(ga,try saves.capture(ga,state),.{})));
          }
          try saves.apply(state,parsed.value);
          for([_]micro.RetentionConfig{.{.law=0,.enabled=true},.{.law=0,.stream_seed=1},.{.law=255},.{.law=2,.enabled=true,.stream_seed=42}})|bad|{
            var ga_arena=std.heap.ArenaAllocator.init(allocator);defer ga_arena.deinit();const ga=ga_arena.allocator();
            var wrong=baseline.value;wrong.origin.?.retention_mutation=bad;var refused=false;
            saves.apply(state,wrong) catch |err| {std.debug.assert(err==error.InvalidValue);refused=true;};std.debug.assert(refused);
            std.debug.assert(std.mem.eql(u8,configured,try std.json.stringifyAlloc(ga,try saves.capture(ga,state),.{})));
          }
          for(2..8)|version|{
            var wrong=parsed.value;wrong.version=@intCast(version);wrong.origin.?.model_revision=@intCast(version-1);var refused=false;
            saves.apply(state,wrong) catch |err|{std.debug.assert(err==error.IncompatibleSave);refused=true;};std.debug.assert(refused);
            std.debug.assert(std.meta.eql(state.planet.retentionMutation,parsed.value.origin.?.retention_mutation));
          }
          for([_]u32{6,7})|version|{
            try saves.apply(state,parsed.value);var old=baseline.value;old.version=version;old.origin.?.model_revision=version-1;try saves.apply(state,old);
            std.debug.assert(std.meta.eql(state.planet.retentionMutation,micro.RetentionConfig{}));
          }
          try saves.apply(state,parsed.value);
          var empty_sandbox=baseline.value;empty_sandbox.mode=.sandbox;empty_sandbox.origin=null;try saves.apply(state,empty_sandbox);
          // Deliberate stale config tests the new-Origin reset independently of load reset.
          state.planet.retentionMutation=.{.law=1,.enabled=true,.stream_seed=std.math.maxInt(u64)};
          try state.planet.beginOrigin();std.debug.assert(std.meta.eql(state.planet.retentionMutation,micro.RetentionConfig{}));
          try saves.apply(state,baseline.value);
          std.debug.print("RETENTION_CONFIG_AUDIT_PASS max_u64_on_off_exact=true four_invalid_atomic=true v2_v7_disguises_refused=true v6_v7_reset=true new_origin_reset=true\n",.{});
'''
s=s.replace(needle,extra+needle);p.write_text(s)
(out.parent/'audit-provenance.json').write_text(json.dumps({'base_files':{str(x.relative_to(src)):hashlib.sha256(x.read_bytes()).hexdigest() for x in [src/'main.zig',src/'save_schema.zig',src/'save_game.zig',src/'simulation/planet.zig',src/'simulation/microbes.zig']},'audit_main':hashlib.sha256(p.read_bytes()).hexdigest()},indent=2)+'\n')
