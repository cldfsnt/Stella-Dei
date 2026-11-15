#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,struct,re,sys
p=Path(sys.argv[1]);summary={'preview':json.loads((p/'preview.json').read_text())}
def rows(path,tag):
 with path.open() as f:
  for line in f:
   if line.startswith(tag+' '):yield json.loads(line[len(tag)+1:])
seed=list(rows(p/'preview.log','SEED_ROW'));summary['seed_rows']=len(seed);summary['seed_successes']=sum(x['ok'] for x in seed)
assert summary['seed_successes']==summary['preview']['planted']
for x in seed:
 assert x['before']['rng']==x['after']['rng']
 for co in x['after']['cohorts']:assert co['root_fraction']==co['support_mass']==co['reproduction_credit']==0
assert summary['preview']['eligible']==len(seed)
carbon=F(0);nutrient=F(0);gas=F(0)
for x in seed:
 carbon+=sum(F(c['biomass'])for c in x['after']['cohorts'])-sum(F(c['biomass'])for c in x['before']['cohorts'])
 nutrient+=F(x['before']['nutrient'])-F(x['after']['nutrient'])
 gas+=(F(x['co2_before'])-F(x['co2_after']))*10**9*x['cells']*12/(44*F(x['area']))
summary['seed_ledger']={'carbon_density_sum':float(carbon),'nutrient_density_debit_sum':float(nutrient),'represented_gas_carbon_density_sum':float(gas),'carbon_minus_represented_gas':float(carbon-gas),'relative_carbon_minus_gas':float((carbon-gas)/carbon)}

mask=2**64-1
def advance(s):
 for _ in range(6):s=(s+0x9e3779b97f4a7c15)&mask;s=s or 1
 return s
def proposal(c):
 cfg=c['config'];child=c['child'];b=b'STELLA-ROOT1'+b'\0'*4+struct.pack('<QQQI',cfg['stream_seed'],child['parent'],child['lineage'],child['generation']);h=hashlib.sha256(b).digest();return (1/32 if h[1]&1==0 else -1/32) if h[0]&63==0 else 0
birth_count=0;proposals={'positive':0,'negative':0,'zero':0,'clipped_negative_at_zero':0};positive_ids=set();mutant_ids=set();root_children=set();max_carbon_residual=F(0);max_support_residual=F(0)
for x in rows(p/'main.log','BIRTH'):
 birth_count+=1;old=x['parent_before'];child=x['child'];after=x['parent_after'];q=proposal(x)
 assert x['rng_after']==advance(x['rng_before']);assert child['root_fraction']==max(0,min(1,old['root_fraction']+q));assert after['root_fraction']==old['root_fraction'];assert child['parent']==old['lineage'] and child['generation']==min(2**32-1,old['generation']+1)
 assert after['biomass']<old['biomass'] and after['reproduction_credit']<old['reproduction_credit'] and child['reproduction_credit']==0
 max_carbon_residual=max(max_carbon_residual,abs(F(old['biomass'])-F(after['biomass'])-F(child['biomass'])));max_support_residual=max(max_support_residual,abs(F(old['support_mass'])-F(after['support_mass'])-F(child['support_mass'])))
 proposals['positive' if q>0 else 'negative' if q<0 else 'zero']+=1
 if q<0 and old['root_fraction']==0:proposals['clipped_negative_at_zero']+=1
 if child['root_fraction']>0:root_children.add(child['lineage'])
 if old['root_fraction']==0 and child['root_fraction']>0:positive_ids.add(child['lineage'])
 if child['root_fraction']!=old['root_fraction']:mutant_ids.add(child['lineage'])
summary.update(birth_events=birth_count,proposals=proposals,positive_from_zero=len(positive_ids),root_born_lineages=len(root_children),changed_mutation_lineages=len(mutant_ids),max_existing_birth_carbon_residual=float(max_carbon_residual),max_existing_birth_support_residual=float(max_support_residual))
water_events=0;positive_credit=0;credit=0.;max_h=0.;min_depth=None;paid_ids=set()
for x in rows(p/'main.log','ROOT_WATER'):
 water_events+=1;assert x['credit']>=0 and x['credit']<=x['demand'];assert F(x['h'])*F(x['demand'])<=F(x['credit'])
 if x['credit']>0:positive_credit+=1;paid_ids.add(x['lineage'])
 credit+=x['credit'];max_h=max(max_h,x['h']);d=x['environment']['depth_km']*1000;min_depth=d if min_depth is None else min(min_depth,d)
summary.update(root_water_events=water_events,positive_root_water_events=positive_credit,root_water_density_sum=credit,paid_root_lineages=len(paid_ids),max_h=max_h,min_root_phase_depth_m=min_depth)
last={};first={}
for x in rows(p/'main.log','ROOT_FATE'):
 identity=x['cohort']['lineage'];first.setdefault(identity,x);last[identity]=x
summary['root_fates']=[{'lineage':i,'first_tick':first[i]['tick'],'last_tick':last[i]['tick'],'last_cell':last[i]['cell'],'last_mass':last[i]['cohort']['biomass'],'last_support':last[i]['cohort']['support_mass'],'root_fraction':last[i]['cohort']['root_fraction'],'alive_at_end':last[i]['tick']==420,'paid_water':i in paid_ids}for i in sorted(last)]
tick_lines=[line for line in (p/'main.log').read_text().splitlines() if line.startswith('TICK ')]
assert len(tick_lines)==420 and int(re.search(r'births=(\d+)',tick_lines[-1])[1])==birth_count
summary['daily']=[line.strip() for line in (p/'main.log').read_text().splitlines() if line.startswith('TICK ') and int(re.search(r'tick=(\d+)',line)[1])%60==0]
end=p/'day-7.json';restart=p/'resume-day-7.json';summary['fresh_process_continuation_exact']=end.read_bytes()==restart.read_bytes();assert summary['fresh_process_continuation_exact']
for tag in ['BIRTH','ROOT_FATE','ROOT_WATER']:
 original=[x for x in rows(p/'main.log',tag)if x['tick']>180];continued=list(rows(p/'resume.log',tag));assert original==continued;summary['restart_'+tag.lower()+'_events_exact']=len(original)
for day in range(4,8):assert(p/f'day-{day}.json').read_bytes()==(p/f'resume-day-{day}.json').read_bytes()
summary['all_day4_to7_snapshots_exact']=True
summary['endpoint_sha256']=hashlib.sha256(end.read_bytes()).hexdigest();(p/'analysis.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items()if k!='root_fates'},indent=2))
