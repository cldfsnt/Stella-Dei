from pathlib import Path
import json, gzip
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
D=Path(__file__).resolve().parent
rows=json.loads(gzip.decompress((D/'results.json.gz').read_bytes()))['CYCLES']
fig,axes=plt.subplots(2,3,figsize=(14,7),sharex=True,sharey=True)
for ri,crowded in enumerate(['false','true']):
 for hi,hab in enumerate(['0','1','2']):
  ax=axes[ri,hi];r=[x for x in rows if x['rate']=='0.6' and x['slow']=='0.5' and x['swap']=='0' and x['habitat']==hab and x['crowded']==crowded]
  ax.plot([int(x['day']) for x in r],[float(x['fast']) for x in r],label='Fast activity 1',color='#d95f02',lw=2)
  ax.plot([int(x['day']) for x in r],[float(x['slow_mass']) for x in r],label='Slow activity 0.5',color='#168a75',lw=2)
  if hab!='0':
   for day in range(2,40,4):ax.axvspan(day,day+2,color='black',alpha=.06)
   ax.axvline(40,color='#555',ls='--',lw=1)
  ax.set_title(['Stable light','Alternating darkness','Dark + limited shared resources'][hi]+'\n'+('Crowded start' if crowded=='true' else 'Sparse start'))
  ax.set_ylim(0,1);ax.grid(alpha=.2)
  if ri==1:ax.set_xlabel('Simulated day (constant light after day 40)')
  if hi==0:ax.set_ylabel('Living carbon (kg C/m²)')
axes[0,0].legend(fontsize=9)
fig.suptitle('Shared-resource trajectories: lower demand is not lasting dominance\nEqual total initial C/N across densities; basal 0.6/day; fixed phenotypes, no inheritance',fontsize=14)
fig.text(.5,.015,'Experimental uncalibrated physiology. These plotted cases meet ledger tolerances; full sweep fails 4 equal-activity controls on nutrient drift.',ha='center',fontsize=9)
fig.tight_layout(rect=(0,.04,1,.91));fig.savefig(D/'trajectories.png',dpi=140);fig.savefig(D/'trajectories.svg')
