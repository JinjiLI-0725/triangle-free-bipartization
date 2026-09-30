"""Summarize only the already-computed saved-witness frontier table."""
import csv
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
out=root/'results/extension_frontier_diagnostic'
rows=list(csv.DictReader((out/'frontiers.tsv').open(),delimiter='\t'))
source=root/'results/global_cut_landscape_n15_full/h0_witnesses.tsv'
saved=list(csv.DictReader(source.open(),delimiter='\t'))
assert [(r['id'],r['Y_mask']) for r in rows]==[(r['id'],r['Y_mask']) for r in saved]
keys=['contiguous','adjacent_lower_lipschitz','convex_finite_triples','F_min_at_zero',
      'F_nondecreasing','combined_nondecreasing','convex_interval_domain']
# Check monotonicity across ALL attainable layers, including gaps.
# The C++ adjacent flags are additionally retained in the raw table.
for r in rows:
    pairs=[(j,int(x)) for j,x in enumerate(r['F'].split(',')) if x!='NA']
    r['convex_interval_domain']=str(int(r['contiguous']=='1' and r['convex_finite_triples']=='1'))
    r['F_nondecreasing']=str(int(all(v>=u for (_,u),(_,v) in zip(pairs,pairs[1:]))))
    r['combined_nondecreasing']=str(int(all(j+v>=i+u for (i,u),(j,v) in zip(pairs,pairs[1:]))))
with (out/'frontiers_validated.tsv').open('x') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t')
    writer.writeheader();writer.writerows(rows)
stats={key:sum(int(r[key]) for r in rows) for key in keys}
first={key:next((r for r in rows if r[key]=='0'),None) for key in keys}
for r in rows:
    F=[None if x=='NA' else int(x) for x in r['F'].split(',')]
    assert F[0]==int(r['q'])<=5
    assert all(j+v>=F[0] for j,v in enumerate(F) if v is not None)
    assert min(j+v for j,v in enumerate(F) if v is not None)==int(r['q'])
summary={'scope':'one existing recorded H0 witness per saved graph; no new Y selection',
         'records':len(rows),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
         'all_H0_identities_pass':True,'property_pass_counts':stats,'first_failures':first,
         'warning':'finite corpus diagnostic, not a universal theorem; adjacency/triples skip missing layers'}
with (out/'summary.json').open('x') as f:json.dump(summary,f,indent=2);f.write('\n')
print(json.dumps({'records':len(rows),'property_pass_counts':stats,
                  'first_failure_ids':{k:None if v is None else v['id'] for k,v in first.items()}},indent=2))
