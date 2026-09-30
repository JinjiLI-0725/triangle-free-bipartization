"""Re-index saved optimal cuts; no MaxCut calls and no graph generation."""
import csv,json
from collections import Counter,defaultdict
from fractions import Fraction
from pathlib import Path
root=Path(__file__).resolve().parents[1]
out=root/'results/optimal_face_projection'
out.mkdir(exist_ok=True)

def read(path):
    with (root/path).open() as f:return list(csv.DictReader(f,delimiter='\t'))

graphs=read('results/h0_witness_structure/graph_structure.tsv')
positive=Counter();good=Counter()
# Filter saved marginal histograms before parsing: no full feature-table scan.
with (root/'results/h0_witness_structure/category_histograms.tsv').open() as f:
    for line in f:
        if '\tDelta_min\t0\t' not in line:continue
        gid,cat,feature,value,count=line.rstrip().split('\t')
        positive[int(gid)]+=int(count)
        if cat=='H0':good[int(gid)]+=int(count)
with (out/'full_graph_counts.tsv').open('x') as f:
    w=csv.writer(f,delimiter='\t');w.writerow(['id','dG','L','critical','Y_with_I_positive','good_Y_with_I_positive'])
    for r in graphs:
        gid=int(r['graph_id']);assert good[gid]==int(r['H0_count'])
        w.writerow([gid,r['dG'],r['L'],r['critical'],positive[gid],good[gid]])
print('Full saved marginal counts read',len(graphs),flush=True)
opt={int(r['id']):[int(x) for x in r['optG_masks'].split(',')]
     for r in read('results/global_cut_landscape_n15/global_optimal_cuts.tsv')}
geom={int(r['id']):r for r in read('results/global_cut_landscape_n15/graph_summary.tsv')}
hist=Counter();hist_good=Counter();hist_preserved=Counter();byq=defaultdict(Counter)
per=defaultdict(Counter);first_collision=None;first_critical_failure=None
Hdata={}
with (out/'sample_fivesets.tsv').open('x') as target:
    writer=csv.writer(target,delimiter='\t')
    writer.writerow(['id','Y_mask','q','I_distinct_remainder_optima','J_global_extensions','optH_count'])
    with (root/'results/global_cut_landscape_n15/fiveset_summary.tsv').open() as source:
        for r in csv.DictReader(source,delimiter='\t'):
            gid=int(r['id']);Y=int(r['Y_mask']);H=32767^Y;q=int(r['q'])
            if Y not in Hdata:Hdata[Y]=[v for v in range(15) if H>>v&1]
            hv=Hdata[Y]
            local=[int(x) for x in r['optH_masks_local'].split(',')]
            core=set()
            for h in local:
                mask=sum((1<<v) for j,v in enumerate(hv) if h>>j&1)
                core.add(min(mask,H^mask))
            assert len(core)==int(r['optH_count'])
            fibers=Counter(min(f&H,(f&H)^H) for f in opt[gid])
            inherited={h:count for h,count in fibers.items() if h in core}
            I=len(inherited);J=sum(inherited.values())
            assert J==int(r['compatible_optG'])
            assert (I>0)==(int(r['delta_min'])==0)
            assert I<=J<=32*I
            assert sum((Fraction(1,inherited[min(f&H,(f&H)^H)]) for f in opt[gid]
                        if min(f&H,(f&H)^H) in inherited),Fraction())==I
            writer.writerow([gid,Y,q,I,J,len(core)])
            hist[I]+=1
            if I:hist_preserved[I]+=1
            if I and q<=5:hist_good[I]+=1
            a=byq[q];a['sets']+=1;a['sum_I']+=I;a['positive']+=I>0
            p=per[gid];p['sets']+=1;p['sum_I']+=I;p['sum_q']+=q;p['sum_qI']+=q*I
            p['positive']+=I>0;p['good_positive']+=I>0 and q<=5
            p['good_I_sum']+=I if q<=5 else 0
            if I<J and first_collision is None:
                first_collision={'id':gid,'Y_mask':Y,'q':q,'I':I,'J':J,'extension_counts':sorted(inherited.values())}
            if not I and geom[gid]['d_edge_critical']=='1' and first_critical_failure is None:
                first_critical_failure={'id':gid,'graph6':geom[gid]['graph6'],'Y_mask':Y,'q':q,
                                        'dG':geom[gid]['dG'],'delta_min':r['delta_min']}
for gid,p in per.items():
    assert p['sets']==3003
    assert p['positive']==positive[gid] and p['good_positive']==good[gid]
    p['covariance_numerator']=p['sets']*p['sum_qI']-p['sum_q']*p['sum_I']
for q,a in byq.items():a['mean_I']=str(Fraction(a['sum_I'],a['sets']))
minimum_good_count=min(good.values())
summary={'scope':'Full saved corpus positivity counts from saved marginals; DISTINCT I counts only on existing 40-graph landscape sample, all its saved five-sets',
         'full_graphs':len(graphs),'full_Y_positive':sum(positive.values()),'full_good_Y_positive':sum(good.values()),
         'minimum_positive_Y_per_graph':min(positive.values()),'minimum_good_positive_Y_per_graph':minimum_good_count,
         'minimum_good_ids':[g for g in good if good[g]==minimum_good_count],
         'sample_graphs':len(per),'sample_fivesets':sum(hist.values()),
         'I_histogram_all':dict(sorted(hist.items())),'I_histogram_preserved':dict(sorted(hist_preserved.items())),
         'I_histogram_good_H0':dict(sorted(hist_good.items())),'by_q':dict(sorted(byq.items())),
         'sample_per_graph':dict(sorted(per.items())),
         'within_graph_covariance_signs':dict(Counter('negative' if p['covariance_numerator']<0 else 'positive' if p['covariance_numerator']>0 else 'zero' for p in per.values())),
         'first_projection_collision':first_collision,'first_sample_critical_nonintersection':first_critical_failure}
with (out/'summary.json').open('x') as f:json.dump(summary,f,indent=2);f.write('\n')
print(json.dumps({k:summary[k] for k in ['full_graphs','full_Y_positive','full_good_Y_positive','minimum_positive_Y_per_graph','minimum_good_positive_Y_per_graph','sample_graphs','sample_fivesets','within_graph_covariance_signs','first_projection_collision','first_sample_critical_nonintersection']},indent=2))
