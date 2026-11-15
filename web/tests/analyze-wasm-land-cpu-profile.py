from pathlib import Path
import json,collections,hashlib
r=Path(__file__).resolve().parents[2];o=r.parent/'site-tmp/wasm-land-cpu-profile';p=json.loads((o/'beta.cpuprofile').read_text());nodes={n['id']:n for n in p['nodes']};parents={c:n['id']for n in p['nodes']for c in n.get('children',[])}
counts=collections.Counter(p['samples']);categories=collections.Counter();leaf=collections.Counter();rows=[]
for nid,count in counts.items():
 names=[];v=nid
 while v in nodes:names.append(nodes[v]['callFrame']['functionName']);v=parents.get(v,0)
 text='|'.join(names)
 if 'json.stringify' in text:category='serialization_stack'
 elif 'json.static.' in text:category='json_parse_stack'
 elif 'save_schema.Save.validate' in text:category='save_validation_stack'
 elif any('simulation.' in x or 'loop.Job(' in x for x in names):category='named_simulation_stack'
 elif 'main' not in names:category='outside_wasm_main'
 else:category='main_or_inlined_unresolved'
 categories[category]+=count;leaf[names[0]]+=count;rows.append({'samples':count,'category':category,'stack':names})
result={'samples':len(p['samples']),'sampling_interval_us':1000,'categories':dict(categories),'leaf_counts':dict(leaf.most_common()),'stacks':sorted(rows,key=lambda x:-x['samples']),'endpoint_sha256':hashlib.sha256((o/'endpoint.json').read_bytes()).hexdigest(),'scope':'whole process including all72ticks, warmup/startup/parsing/save; counts not measured per-phase durations'}
(o/'analysis.json').write_text(json.dumps(result,indent=2)+'\n');print(categories)
