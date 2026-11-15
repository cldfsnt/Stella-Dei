#!/usr/bin/env python3
"""Read-only exact graph snapshot from real loaded Planet, no route intervention."""
from pathlib import Path
import subprocess,sys,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]);subprocess.run([sys.executable,str(r/'web/tests/egl-ecology-pulse-prepare.py'),str(o)],check=True)
p=o/'main.zig';s=p.read_text();prod=(r/'src/main.zig').read_text();begin='export fn stella_make_pond(';end='export fn stella_test_action('
s=s[:s.index(begin)]+prod[prod.index(begin):prod.index(end)]+s[s.index(end):]
a=s.index('          var found=state.findRecordedFeeding(true);');b=s.index('\n        try originSaveCheck',a)
s=s[:a]+r'''
          _=pw;_=pm;const M=@import("simulation/microbes.zig");
          const frozen=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const graph_path="/workspace/scratch/f67c3ac60ca3/site-tmp/propagule-graph/graph.jsonl";
          var graph_file=try std.fs.cwd().createFile(graph_path,.{});defer graph_file.close();
          try std.json.stringify(.{.kind="metadata",.cells=state.planet.microbeCells.len,.radius_km=state.planet.radius,.area_m2=state.planet.getMeanPointArea(),.game_time=state.gameTime},.{},graph_file.writer());try graph_file.writeAll("\n");
          for(state.planet.microbeCells,0..)|cell,i|{
            const depth=state.planet.waterMass[i]*state.planet.getKmPerWaterMass();
            try std.json.stringify(.{.kind="cell",.cell=i,.neighbors=state.planet.getNeighbours(i),.point=state.planet.vertices[i].data,.depth_m=depth*1000,.temperature=state.planet.temperature[i],.habitable=M.habitable(depth,state.planet.temperature[i]),.nutrient=cell.nutrient,.biomass=M.biomass(cell),.cohorts=cell.cohorts},.{},graph_file.writer());try graph_file.writeAll("\n");
          }
          std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.print("PROPAGULE_GRAPH_PASS exact_native_adjacency=true exact_habitat_predicate=true frozen_save_unchanged=true simulation_ticks=0\n",.{});
        }
'''+s[b:];p.write_text(s)
subprocess.run([sys.executable,str(r/'web/tests/audit-zig-exports.py'),str(r/'src/main.zig'),str(p),'--output',str(o.parent/'export-audit.json')],check=True)
files=['main.zig','simulation/microbes.zig','simulation/planet.zig','states/play.zig'];prov={'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip(),'save_sha256':hashlib.sha256((r.parent/'site-tmp/natural60-day60.json').read_bytes()).hexdigest(),'production':{},'copied':{}}
for f in files:prov['production'][f]=hashlib.sha256((r/'src'/f).read_bytes()).hexdigest();prov['copied'][f]=hashlib.sha256((o/f).read_bytes()).hexdigest()
(o.parent/'provenance.json').write_text(json.dumps(prov,indent=2)+'\n')
