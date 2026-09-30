"""Linear-time aggregation of completed projection tables; no cut computation."""
import csv,json
from collections import Counter,defaultdict
from fractions import Fraction
from pathlib import Path
root=Path(__file__).resolve().parents[1];out=root/'results/optimal_face_projection'
with (out/'full_graph_counts.tsv').open() as f:full=list(csv.DictReader(f,delimiter='\t'))
full_by={int(r['id']):r for r in full}
with (root/'results/global_cut_landscape_n15/graph_summary.tsv').open() as f:
    geom={int(r['id']):r for r in csv.DictReader(f,delimiter='\t')}
hist=Counter();hist_good=Counter();hist_preserved=Counter();byq=defaultdict(Counter);per=defaultdict(Counter)
collision=None;critical_failure=None
with (out/'sample_fivesets.tsv').open() as f:
    for r in csv.DictReader(f,delimiter='\t'):
        gid=int(r['id']);Y=int(r['Y_mask']);q=int(r['q']);I=int(r['I_distinct_remainder_optima']);J=int(r['J_global_extensions'])
        assert I<=J<=32*I
        hist[I]+=1
        if I:hist_preserved[I]+=1
        if I and q<=5:hist_good[I]+=1
        a=byq[q];a['sets']+=1;a['sum_I']+=I;a['positive']+=I>0
        p=per[gid];p['sets']+=1;p['sum_I']+=I;p['sum_q']+=q;p['sum_qI']+=q*I
        p['positive']+=I>0;p['good_positive']+=I>0 and q<=5;p['good_I_sum']+=I if q<=5 else 0
        if I<J and collision is None:collision={'id':gid,'Y_mask':Y,'q':q,'I':I,'J':J}
        if not I and geom[gid]['d_edge_critical']=='1' and critical_failure is None:
            critical_failure={'id':gid,'graph6':geom[gid]['graph6'],'Y_mask':Y,'q':q,'dG':geom[gid]['dG']}
assert len(per)==40 and sum(hist.values())==120120
for gid,p in per.items():
    assert p['sets']==3003
    assert p['positive']==int(full_by[gid]['Y_with_I_positive'])
    assert p['good_positive']==int(full_by[gid]['good_Y_with_I_positive'])
    p['covariance_numerator']=p['sets']*p['sum_qI']-p['sum_q']*p['sum_I']
    p['I_weighted_mean_q']=str(Fraction(p['sum_qI'],p['sum_I']))
for q,a in byq.items():a['mean_I']=str(Fraction(a['sum_I'],a['sets']))
mg=min(int(r['good_Y_with_I_positive']) for r in full)
summary={'scope':'Full saved corpus positivity from saved marginals; distinct I on existing 40-graph landscape sample only',
         'aggregation':'linear-time reindexing of completed tables after stopping redundant quadratic minimum calculation',
         'full_graphs':len(full),'full_Y_positive':sum(int(r['Y_with_I_positive']) for r in full),
         'full_good_Y_positive':sum(int(r['good_Y_with_I_positive']) for r in full),
         'minimum_positive_Y_per_graph':min(int(r['Y_with_I_positive']) for r in full),
         'minimum_good_positive_Y_per_graph':mg,
         'minimum_good_ids':[int(r['id']) for r in full if int(r['good_Y_with_I_positive'])==mg],
         'sample_graphs':len(per),'sample_fivesets':sum(hist.values()),
         'I_histogram_all':dict(sorted(hist.items())),'I_histogram_preserved':dict(sorted(hist_preserved.items())),
         'I_histogram_good_H0':dict(sorted(hist_good.items())),'by_q':dict(sorted(byq.items())),
         'sample_per_graph':dict(sorted(per.items())),
         'within_graph_covariance_signs':dict(Counter('negative' if p['covariance_numerator']<0 else 'positive' if p['covariance_numerator']>0 else 'zero' for p in per.values())),
         'I_weighted_mean_q_compared_with_6':dict(Counter('below' if p['sum_qI']<6*p['sum_I'] else 'above' if p['sum_qI']>6*p['sum_I'] else 'equal' for p in per.values())),
         'first_projection_collision':collision,'first_sample_critical_nonintersection':critical_failure}
with (out/'summary.json').open('x') as f:json.dump(summary,f,indent=2);f.write('\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ('sample_per_graph','I_histogram_all','I_histogram_preserved','I_histogram_good_H0','by_q')},indent=2))
