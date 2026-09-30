#!/usr/bin/env python3
"""Summarize only the frozen 40-graph experiment; no graph search."""
from collections import Counter,defaultdict
import csv,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'results/global_cut_landscape_n15'

def rows(path):
    with path.open() as f:return list(csv.DictReader(f,delimiter='\t'))
def numeric(r,exclude=()):
    return {k:(int(v) if k not in exclude and v.lstrip('-').isdigit() else v) for k,v in r.items()}
def combine(ids,kind,target):
    if target.exists():
        # Resume reporting only if the existing aggregate is byte-identical
        # to the completed per-graph checkpoints.
        digest=hashlib.sha256()
        for j,i in enumerate(ids):
            with (OUT/'checkpoints'/f'{i}.{kind}.tsv').open('rb') as f:
                head=f.readline()
                if j==0:digest.update(head)
                for chunk in iter(lambda:f.read(1<<20),b''):digest.update(chunk)
        if digest.hexdigest()!=hashlib.sha256(target.read_bytes()).hexdigest():
            raise RuntimeError(f'Existing aggregate differs: {target}')
        return
    with target.open('w') as out:
        for j,i in enumerate(ids):
            with (OUT/'checkpoints'/f'{i}.{kind}.tsv').open() as f:
                head=f.readline()
                if j==0:out.write(head)
                for line in f:out.write(line)
def main():
    manifest=rows(OUT/'sample_manifest.tsv'); ids=[int(r['corpus_id']) for r in manifest]
    assert 20<=len(ids)<=50 and len(set(ids))==len(ids)
    assert all((OUT/'checkpoints'/f'{i}.done').exists() for i in ids)
    for kind,file in [('summary','graph_summary.tsv'),('five','fiveset_summary.tsv'),('witness','reoptimization_witnesses.tsv'),('cuts','global_optimal_cuts.tsv')]:combine(ids,kind,OUT/file)
    gs=[numeric(r,('graph6',)) for r in rows(OUT/'graph_summary.tsv')]
    byid={r['id']:r for r in gs}; metrics=['q','rho','delta_min','optH_count','ell','Y_type','degree_sum','compatible_optG']
    hist={name:{metric:Counter() for metric in metrics} for name in ('good','bad')}
    qhist=defaultdict(Counter); delta=defaultdict(Counter); observed=Counter(); total=0
    hard_ids={i for i,g in byid.items() if g['dG']>=6}
    hard_rho=Counter(); minq_compatible=set(); first_hard_rho5=None
    minpositive={}; canonical_min={}
    with (OUT/'fiveset_summary.tsv').open() as f:
        for rr in csv.DictReader(f,delimiter='\t'):
            r=numeric(rr,('optH_masks_local',));i=r['id']; total+=1;observed[i]+=1
            group='good' if r['good'] else 'bad'
            for key in metrics:hist[group][key][r[key]]+=1
            qhist[i][r['q']]+=1;delta[i][r['delta_min']]+=1
            if r['q']==byid[i]['min_q'] and r['rho']==0:minq_compatible.add(i)
            if i in hard_ids and r['good']:
                hard_rho[r['rho']]+=1
                if r['rho']==5 and first_hard_rho5 is None:
                    first_hard_rho5={k:r[k] for k in ['id','Y_mask','q','rho','delta_min','f_witness','h_witness_local','S_mask','Delta_witness']}
            assert r['q']==r['R_witness']+r['Delta_witness']
            assert (r['rho']==0)==(r['delta_min']==0)==(r['compatible_optG']>0)
            if r['good'] and (i not in canonical_min or (r['rho'],r['Y_mask'])<(canonical_min[i]['rho'],canonical_min[i]['Y_mask'])):canonical_min[i]=r
            if r['good'] and r['rho']>0 and (i not in minpositive or (r['rho'],r['Y_mask'])<(minpositive[i]['rho'],minpositive[i]['Y_mask'])):minpositive[i]=r
    assert all(observed[i]==3003 for i in ids)
    shapes=Counter(); witnesses=[]; witness_bykey={}
    for rr in rows(OUT/'reoptimization_witnesses.tsv'):
        r=numeric(rr,('S_vertices','S_degrees'));key=(r['id'],r['Y_mask']);witness_bykey[key]=r
        if r['good']:
            label=f"n={r['S_size']},m={r['S_edges']},degrees={r['S_degrees']},connected={r['connected']},bipartite={r['bipartite']}"
            shapes[label]+=1
    for i in ids:
        if i in minpositive:witnesses.append(witness_bykey[(i,minpositive[i]['Y_mask'])])
    fail=[i for i in ids if byid[i]['good_rho0']==0]
    discrepancy=[]
    for r in manifest:
        i=int(r['corpus_id']);g=byid[i]
        if r['saved_critical'] not in ('unknown',str(g['d_edge_critical'])):discrepancy.append({'id':i,'field':'critical','saved':r['saved_critical'],'exact':g['d_edge_critical']})
        if int(r['saved_d'])!=g['dG']:discrepancy.append({'id':i,'field':'d','saved':r['saved_d'],'exact':g['dG']})
        if r['saved_L'].isdigit() and int(r['saved_L'])!=g['L']:discrepancy.append({'id':i,'field':'L','saved':r['saved_L'],'exact':g['L']})
    maxrho=max(g['good_min_rho'] for g in gs)
    for group in hist:
        hist[group]['optG_count']=Counter()
        for g in gs:hist[group]['optG_count'][g['optG_count']]+=g[group+'_count']
    summary={'scope':'40 deterministic representatives from SAVED n=15 corpus; not all n=15 graphs and not all saved classes',
      'graphs_analyzed':len(ids),'five_sets':total,'all_cuts_exact':True,
      'global_cuts_modulo_reversal_per_graph':16384,'core_cuts_modulo_reversal_per_Y':512,
      'global_identity_checks':sum(g['identities_checked'] for g in gs),
      'nontrivial_graph_count':len(hard_ids),'nontrivial_ids':sorted(hard_ids),
      'nontrivial_H0_survives':all(byid[i]['good_rho0']>0 for i in hard_ids),
      'nontrivial_good_rho':dict(sorted(hard_rho.items())),
      'first_nontrivial_good_rho5_witness':first_hard_rho5,
      'graphs_with_compatible_min_q_deletion':sorted(minq_compatible),
      'H0_survives':not fail,'H0_first_failure':fail[0] if fail else None,'H0_failures':fail,
      'max_min_rho_good':maxrho,'first_universal_sample_rho_bound':maxrho,
      'rho_good':dict(sorted(hist['good']['rho'].items())),'rho_bad':dict(sorted(hist['bad']['rho'].items())),
      'good_bad_histograms':hist,'q_histograms_per_graph':qhist,'delta_min_histograms_per_graph':delta,
      'canonical_min_rho_good_witnesses':canonical_min,'min_positive_rho_good_witnesses':witnesses,
      'chosen_nearest_nonempty_good_switch_shapes':shapes,
      'H2_scope':'All minimum-rho good switches are empty if H0 holds. Other shape counts cover ONE deterministic nearest pair per Y, not all tied nearest pairs.',
      'H3':'Not formulated: all nearest-pair ties have not been structurally classified; gain=monochromatic boundary minus bichromatic boundary is an identity, not a discovered selection inequality.',
      'metadata_discrepancies':discrepancy,'exact_critical_ids':[g['id'] for g in gs if g['d_edge_critical']],
      'validation':{'test_command':'python3 -m unittest discover -s tests -p test_global_cut_landscape_n15.py -v','tests_passed':5},
      'selection':json.loads((OUT/'selection.json').read_text()),
      'next_step':'SCALE_TO_FULL_CORPUS' if not fail else 'FORMULATE_GLOBAL_LEMMA'}
    summary['sha256']={name:hashlib.sha256((OUT/name).read_bytes()).hexdigest() for name in ['sample_manifest.tsv','sample_input.txt','graph_summary.tsv','fiveset_summary.tsv','reoptimization_witnesses.tsv','global_optimal_cuts.tsv']}
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    note=['# Global cut landscape: bounded n=15 discovery experiment','',
      '**Exact computation on a deterministic sample; no universal theorem is claimed.**','',
      f"Analyzed {len(ids)} saved graphs and all {total:,} five-sets. For each graph all 16,384 cuts modulo reversal were checked; for every remainder all 512 cuts modulo reversal were checked. The code also computes redundant reversed costs to verify invariance. All {summary['global_identity_checks']:,} global-optimum/five-set identities passed.",'',
      '## Selection and scope','',
      'The maximum observed d is 9; none of these graphs satisfies the genuine-counterexample equation d=10 at k=3. This is a discovery experiment about selection and compatibility, not a test of an existing full-hypothesis counterexample.','',
      'The frozen manifest records every selection reason. It includes requested IDs 401, 1676, 6132, 10116; B3; saved critical witnesses; the top eight saved d values by ID; representatives for every saved hard L level; and additional d and (L,d) strata, stopping at 40. Input graphs come exclusively from the saved canonical corpus. No graph was generated.',
      '',summary['selection']['missing_previous_obstruction'],'',
      'Criticality was recomputed from exact optimal cuts: every edge must be monochromatic in at least one optimum. Saved flags were only selection metadata. Discrepancies are listed below and in JSON; historical files were not modified.','',
      '## Main observations','',
      f"H0 survives: **{not fail}**. First failure: **{fail[0] if fail else 'none'}**. Maximum, over sampled graphs, of minimum rho among good five-sets: **{maxrho}**.",'',
      f"Good-Y rho distribution: `{dict(sorted(hist['good']['rho'].items()))}`.",
      f"Bad-Y rho distribution: `{dict(sorted(hist['bad']['rho'].items()))}`.",'',
      'The primary empirical hypothesis is: every graph in the intended hard domain admits a good five-set whose remainder has an optimal coloring inherited from an optimal coloring of the full graph. The experiment supports this only to the extent recorded by H0; no claim is made for all saved classes or full counterexample hypotheses.',
      '',
      f"Restricting to d(G)>=6 gives {len(hard_ids)} nontrivial graphs; H0 survives all of them. Their good-Y rho histogram is `{dict(sorted(hard_rho.items()))}`. All four exactly critical sampled graphs also satisfy H0.",
      '',
      f"Selection matters: some nontrivial good deletions have rho=5 even though Delta_min=1. The first such recorded witness is `{first_hard_rho5}`. Thus a small reoptimization gain does not imply a small switching distance. No bounded-radius claim for arbitrary good Y is supported.",
      '',
      'If H0 survives, the minimum-rho switching family is exactly the empty set, for every minimum-distance witness pair. This is selection-dependent compatibility, not evidence that arbitrary deletions require only small local repairs. Nonempty witnesses below describe other good deletions.',
      '',
      f"A compatible deletion also attains the minimum q over all five-sets in {len(minq_compatible)}/{len(ids)} sampled graphs. This stronger sample observation is recorded without replacing H0 as the primary hypothesis.",'',
      '## Per-graph exact results','',
      '| ID | d | L | Opt(G) | critical | min q | good Y | min rho (good) | min Delta_min (good) |',
      '|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for g in gs:note.append('| '+' | '.join(str(g[k]) for k in ['id','dG','L','optG_count','d_edge_critical','min_q','good_count','good_min_rho','good_min_delta'])+' |')
    note += ['', '## Good versus bad distributions','', 'These are exact histograms pooled over five-sets; the JSON retains per-graph q and Delta histograms. Pooling does not establish causal structure. Every individual row remains available in fiveset_summary.tsv.','']
    for key in ['delta_min','optH_count','ell','degree_sum','compatible_optG','optG_count']:
        note += [f'- {key}: good `{dict(sorted(hist["good"][key].items()))}`; bad `{dict(sorted(hist["bad"][key].items()))}`.']
    note += ['', 'Induced five-set types are exact isomorphism classes: the minimum ten-bit adjacency code over all 120 permutations. Their good/bad histograms are in summary.json; this avoids conflating nonisomorphic degree sequences.','',
      '## Minimum positive-rho good witnesses','',
      'One deterministic witness is shown per graph having a positive-rho good deletion. The TSV gives actual vertex sets, both cuts, and all boundary counts for every positive-rho deletion, good or bad. H boundary counts are under the selected global optimum; their difference is exactly Delta for that witness.','',
      '| ID | Y mask | rho | switch vertices | induced edges | degrees | independent | connected | path | star | H boundary M/C | Y boundary M/C | Delta |',
      '|---:|---:|---:|---|---:|---|---:|---:|---:|---:|---|---|---:|']
    for w in witnesses:note.append(f"| {w['id']} | {w['Y_mask']} | {w['rho']} | {w['S_vertices']} | {w['S_edges']} | {w['S_degrees']} | {w['independent']} | {w['connected']} | {w['path']} | {w['star']} | {w['H_boundary_M']}/{w['H_boundary_C']} | {w['Y_boundary_M']}/{w['Y_boundary_C']} | {w['Delta']} |")
    note += ['', 'For all chosen nearest nonempty good witnesses, the shape histogram is:', '', '```json', json.dumps(shapes,indent=2,sort_keys=True),'```','',
      'H3 is not formulated: this run classifies one deterministic nearest pair per Y, not every tied nearest pair. The exact boundary gain identity alone is not an empirical uniform inequality that controls selection.','',
      '## Metadata discrepancies','', '```json',json.dumps(discrepancy,indent=2),'```','',
      '## Reproducibility, distance, and checkpointing','',
      'Masks use source vertex labels 0 through 14. Global optimal masks fix vertex 0 to color 0. Local core masks use the increasing list of vertices outside Y, fixing the first local bit to 0 in the stored Opt(H) list. Witness h masks may use the reversed orientation to realize the smaller Hamming distance. Both orientations seed an exact multisource BFS on the ten-dimensional cube, giving nearest distances without repeated pairwise comparisons.',
      '',
      'For every global optimum, its restricted cost is checked against d(H); Delta_min and the number of compatible global optima are computed independently of the BFS. rho=0 iff Delta_min=0 iff that count is positive is asserted for every Y. The witness minimizing rho need not minimize Delta; both quantities are recorded separately.',
      '',
      'Each completed graph has atomic per-graph TSV checkpoints and a completion marker. Rerunning the checker resumes only incomplete graphs. The summary records hashes of the sample and outputs. Final aggregate files are not silently overwritten.',
      '',
      'Commands:','',
      '```sh',
      'python3 scripts/select_global_cut_landscape_n15.py',
      'g++ -std=c++17 -O3 -o /tmp/analyze_global_cut_landscape_n15 scripts/analyze_global_cut_landscape_n15.cpp',
      '/tmp/analyze_global_cut_landscape_n15 results/global_cut_landscape_n15/sample_input.txt results/global_cut_landscape_n15',
      'python3 scripts/report_global_cut_landscape_n15.py',
      'python3 -m unittest discover -s tests -p test_global_cut_landscape_n15.py -v',
      '```','',
      '**Next step:** '+summary['next_step']+'. This is a recommendation only; the present run stops at the frozen sample.']
    (ROOT/'notes/GLOBAL_CUT_LANDSCAPE_N15.md').write_text('\n'.join(note)+'\n')
    print(json.dumps({k:summary[k] for k in ['graphs_analyzed','five_sets','H0_survives','H0_first_failure','max_min_rho_good','rho_good','rho_bad','metadata_discrepancies']}))
if __name__=='__main__':main()
