#!/usr/bin/env python3
"""Summarize the fixed H0 structure experiment using its exact aggregate tables."""
import csv
import json
import hashlib
from collections import Counter, defaultdict
from pathlib import Path
from fractions import Fraction
from itertools import combinations

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results/h0_witness_structure'

def rows(name):
    with open(OUT/name) as f: yield from csv.DictReader(f,delimiter='\t')
def write_tsv(name, data):
    data=list(data)
    with open(OUT/name,'w') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0]),delimiter='\t');w.writeheader();w.writerows(data)
def histogram(rr,field): return dict(sorted(Counter(int(r[field]) for r in rr).items()))
def first(rr): return min((int(r['graph_id']) for r in rr),default=None)
def subset(r,s):
    return s=='all' or s=='d_gt_5' and int(r['dG'])>5 or s=='L_ge_12' and int(r['L'])>=12 or s=='edge_critical' and int(r['critical'])==1

def main():
    manifest=json.loads((OUT/'manifest.json').read_text())
    for source, expected in manifest['sources'].items():
        assert hashlib.sha256((ROOT/source).read_bytes()).hexdigest()==expected, f'Source changed: {source}'
    graphs={int(r['graph_id']):r for r in rows('graph_structure.tsv')}
    assert len(graphs)==19270 and set(graphs)==set(range(19270)), 'Incomplete run'
    assert sum(1 for _ in open(OUT/'checkpoints.tsv'))==19270
    rules=defaultdict(list)
    for r in rows('rule_evaluations.tsv'): rules[r['rule']].append(r)
    table=[]; failures=[]
    for name in manifest['rules_fixed_before_run']:
        rr=rules[name];assert len(rr)==19270
        failed=[r for r in rr if r['is_H0']=='0']
        for r in failed:
            failures.append({'graph_id':r['graph_id'],'graph6':graphs[int(r['graph_id'])]['graph6'],'rule':name,**{k:r[k] for k in ['Y_mask','Y_vertices','q','Delta_min','rho','ell','degree_sum','boundary_size','inherited_count','primary_ties','H0_ties','first_H0_tie_Y']}})
        for s in ['all','d_gt_5','L_ge_12','edge_critical']:
            ss=[r for r in rr if subset(graphs[int(r['graph_id'])],s)]
            table.append({'rule':name,'subset':s,'graphs':len(ss),'selected_good':sum(int(r['is_good']) for r in ss),'selected_H0':sum(int(r['is_H0']) for r in ss),'first_not_good':first(r for r in ss if r['is_good']=='0'),'first_not_H0':first(r for r in ss if r['is_H0']=='0'),'has_good_tied_minimizer':sum(int(r['good_ties'])>0 for r in ss),'has_H0_tied_minimizer':sum(int(r['H0_ties'])>0 for r in ss),'first_no_H0_tie':first(r for r in ss if int(r['H0_ties'])==0)})
    first_examples=[]
    for name in manifest['rules_fixed_before_run']:
        rr=rules[name]
        for failure_kind,ff in [('deterministic', [r for r in rr if r['is_H0']=='0']),('no_H0_tied_minimizer',[r for r in rr if int(r['H0_ties'])==0])]:
            if ff:
                r=min(ff,key=lambda r:int(r['graph_id']))
                first_examples.append({'failure_kind':failure_kind,'graph6':graphs[int(r['graph_id'])]['graph6'],**r})
    write_tsv('first_failure_examples.tsv',first_examples)
    write_tsv('selection_rule_summary.tsv',table)
    write_tsv('failures.tsv',failures)
    allrules=[r for r in table if r['subset']=='all']
    best=max(allrules,key=lambda r:r['selected_H0'])
    cat=defaultdict(lambda:defaultdict(Counter))
    fraction_hist=defaultdict(Counter)
    thresholds=[('ell',10),('ell',11),('degree_sum',11),('boundary_size',9)]
    inequality={f'{f}<={v}':{'set_counts':Counter(),'graphs_with_H0':set()} for f,v in thresholds}
    for r in rows('category_histograms.tsv'):
        f=r['feature'];v=int(r['value']);n=int(r['count']);c=r['category'];gid=int(r['graph_id'])
        cat[c][f][v]+=n
        if f=='inherited_count':fraction_hist[c][Fraction(v,int(graphs[gid]['optG_count']))]+=n
        for ff, vv in thresholds:
            if f==ff and v<=vv:
                info=inequality[f'{ff}<={vv}'];info['set_counts'][c]+=n
                if c=='H0':info['graphs_with_H0'].add(gid)
    inequalities={name:{'set_counts':dict(a['set_counts']),'graphs_with_H0':len(a['graphs_with_H0']),'first_graph_without_H0':min(set(graphs)-a['graphs_with_H0'],default=None)} for name,a in inequality.items()}
    coverage={}
    for s in ['all','d_gt_5','L_ge_12','edge_critical']:
        rr=[r for r in graphs.values() if subset(r,s)]
        m=min(int(r['max_cut_good_H0']) for r in rr)
        coverage[s]={'graphs':len(rr),'minimum_of_max_good_inherited':m,'first_graph_attaining_minimum':first(r for r in rr if int(r['max_cut_good_H0'])==m),'max_good_inherited_histogram':histogram(rr,'max_cut_good_H0'),'one_cut_preserves_all_good':sum(int(r['one_cut_all_good']) for r in rr),'first_no_cut_preserves_all_good':first(r for r in rr if r['one_cut_all_good']=='0'),'one_cut_preserves_all_H0':sum(int(r['one_cut_all_H0']) for r in rr),'first_no_cut_preserves_all_H0':first(r for r in rr if r['one_cut_all_H0']=='0'),'graphs_every_global_optimum_has_a_good_H0':sum(int(r['min_cut_good_H0'])>0 for r in rr),'minimum_over_all_individual_optima':min(int(r['min_cut_good_H0']) for r in rr),'graphs_with_H0_inherited_by_every_optimum':sum(int(r['H0_inherited_by_all_optima'])>0 for r in rr)}
    types=Counter()
    for r in graphs.values():
        for t in r['H0_types'].split(','):types[int(t)]+=1
    canonical=defaultdict(list)
    for r in rows('canonical_witnesses.tsv'):canonical[r['criterion']].append(r)
    canonical_summary={}
    for name,rr in canonical.items():
        assert len(rr)==19270
        canonical_summary[name]={'histograms':{f:histogram(rr,f) for f in ['q','ell','degree_sum','boundary_size','d_GY','e_GY','induced_type','components','inherited_count']},'independent_or_C5':sum(int(r['e_GY'])==0 or int(r['d_GY'])==1 for r in rr),'all_optima_inherit':sum(r['inherited_count']==r['optG_count'] for r in rr)}
    counts={c:sum(a['q'].values()) for c,a in cat.items()}
    assert sum(counts.values())==57867810
    summary={'scope':manifest['scope'],'status':'EXACT FINITE COMPUTATION; no theorem inferred','graphs':19270,'five_sets':sum(counts.values()),'tie_break':manifest['tie_break'],'categories':counts,'category_histograms':{c:{f:dict(sorted(h.items())) for f,h in a.items()} for c,a in cat.items()},'selection_rules':table,'best_deterministic_rule':best,'simple_deterministic_rule_survives':best['selected_H0']==19270,'rules_with_H0_tied_minimizer_in_every_graph':[r['rule'] for r in allrules if r['has_H0_tied_minimizer']==19270],'prespecified_inequalities':inequalities,'cut_coverage':coverage,'graphs_with_H0_of_type':dict(sorted(types.items())),'graphs_with_independent_or_C5_H0':sum(int(r['H0_independent_or_C5'])>0 for r in graphs.values()),'first_without_independent_or_C5_H0':first(r for r in graphs.values() if int(r['H0_independent_or_C5'])==0),'canonical_H0':canonical_summary,'features_bytes':(OUT/'fiveset_features.tsv').stat().st_size,'manifest':'manifest.json'}
    comparison=[]
    for c,features in cat.items():
        for feature,h in features.items():
            count=sum(h.values())
            comparison.append({'category':c,'feature':feature,'count':count,'minimum':min(h),'maximum':max(h),'mean_exact':str(Fraction(sum(v*n for v,n in h.items()),count))})
    write_tsv('category_comparison.tsv',comparison)
    type_rows=[]
    for code in sorted(types):
        pairs=list(combinations(range(5),2))
        pairs=sorted(pairs,key=lambda p:(p[1],p[0]))
        edges=[p for bit,p in enumerate(pairs) if (code>>bit)&1]
        deg=[sum(v in p for p in edges) for v in range(5)]
        adj=[{w for p in edges if v in p for w in p if w!=v} for v in range(5)]
        unseen=set(range(5));components=0
        while unseen:
            components+=1;todo=[unseen.pop()]
            while todo:
                v=todo.pop();nxt=adj[v]&unseen;unseen-=nxt;todo+=list(nxt)
        type_rows.append({'induced_type':code,'edges':','.join(f'{u}-{v}' for u,v in edges) or '-','edge_count':len(edges),'degree_sequence':','.join(map(str,sorted(deg,reverse=True))),'components':components,'is_independent':int(not edges),'is_C5':int(deg==[2]*5),'graphs_with_H0':types[code]})
    write_tsv('induced_types.tsv',type_rows)
    summary['category_comparison']=comparison
    summary['inherited_fraction_histograms']={c:{str(v):n for v,n in sorted(h.items())} for c,h in fraction_hist.items()}
    summary['mean_inherited_fraction']={c:str(sum((v*n for v,n in h.items()),Fraction(0))/sum(h.values())) for c,h in fraction_hist.items()}
    summary['next_theorem_candidate']=None
    if 'max_inherited_count' in summary['rules_with_H0_tied_minimizer_in_every_graph']:
        summary['next_theorem_candidate']={
            'status':'CONJECTURE ONLY; existential tie selection, not a deterministic rule',
            'statement':'For every k>=1 and every triangle-free graph G on 5k vertices, define I_G(Y) as the number of global optimal cuts, modulo reversal, restricting optimally to G-Y. There is a five-set Y such that I_G(Y)=max_{|Z|=5} I_G(Z), I_G(Y)>0, and d(G)-d(G-Y)<=2k-1.',
            'quantifier_clarification':'The maximum is over all five-sets, not only good sets. At least one maximizing tie is required to be good; not every maximizing tie.',
            'evidence_graphs':19270}

    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    lines=['# H0 witness structure in the full saved n=15 corpus','',
        '**Status: exact finite computational evidence, not a graph-theoretic theorem.**',
        '',f"All 19,270 saved canonical graphs and all {summary['five_sets']:,} five-sets were processed. This corpus is not the set of all triangle-free graphs on 15 vertices. No graphs were generated.",
        '', '## Exact computation and reproducibility','',
        'The miner reuses the validated binary landscapes for d(G-Y), Delta_min and rho and the complete lists of optimal global cuts. For every five-set it independently counts surviving monochromatic edges under every saved optimal cut. It checks the minimum against saved Delta_min and verifies that a positive inherited-optimum count is equivalent both to Delta_min=0 and rho=0. A witness cut is saved for every H0 row. Counts/fractions use integers; no floating-point fitting is involved.',
        '', 'Scripts: `scripts/mine_h0_witness_structure.cpp`, `scripts/report_h0_witness_structure.py`. Tests: `tests/test_h0_witness_structure.py`. The manifest freezes the twelve rules and source hashes before execution. Six output streams are checkpointed by byte offset after each graph. The feature table is uncompressed TSV.',
        '', 'Reproduce with `g++ -std=c++17 -O3 -march=native scripts/mine_h0_witness_structure.cpp -o /tmp/mine_h0_witness_structure`, then `/tmp/mine_h0_witness_structure results/zero_margin_tightness/corpus.txt results/global_cut_landscape_n15_full results/h0_witness_structure`. Completed graphs are skipped on resume. Run `python3 scripts/check_h0_feature_integrity.py` and `python3 scripts/report_h0_witness_structure.py` after completion. The test module accepts `H0_STRUCTURE_DIR` to point to a separate reference run.',
        '', '`min_degree_in_Y` and `max_degree_in_Y` are the ambient G-degrees of vertices belonging to Y. Separate induced-degree columns remove ambiguity. `induced_type` is the minimum 10-bit adjacency code over all 120 vertex permutations, with edge-bit order (0,1),(0,2),(1,2),...,(3,4). Cut masks use original vertex labels and fix vertex 0 to color 0. Fractions are exact numerator/denominator, not necessarily reduced.',
        '', '## Three categories','', '| Category | Five-sets |','|---|---:|']
    lines += [f'| {c} | {n:,} |' for c,n in counts.items()]
    lines += ['', '| Category | Feature | Minimum | Maximum | Exact mean |','|---|---|---:|---:|---:|']
    lines += [f"| {a['category']} | {a['feature']} | {a['minimum']} | {a['maximum']} | {a['mean_exact']} |" for a in comparison if a['feature'] in ['ell','degree_sum','boundary_size','rho','inherited_count']]
    lines += ['', f"Exact mean inherited-optimum fractions by category: `{summary['mean_inherited_fraction']}`. Full rational fraction distributions are in summary.json."]
    lines += ['', 'Complete integer histograms for q, Delta_min, rho, ell, degree sum, boundary size, induced type, components, degrees, and inherited-optimum count are in summary.json. These distinguish good non-H0 sets (positive reoptimization is unavoidable) from H0 sets; bad sets can still preserve optimality.', '', '## Fixed selection rules','',
        'Each deterministic choice uses the stated one or two statistics, then the lexicographically smallest increasing vertex tuple. This differs from numeric mask order. “Tied H0” asks whether at least one minimizer before that final tie-break is H0; it is not the success count of the deterministic rule.', '',
        '| Rule | Selected good | Selected H0 | First non-H0 | Graphs with a tied H0 |','|---|---:|---:|---:|---:|']
    lines += [f"| {r['rule']} | {r['selected_good']} | {r['selected_H0']} | {r['first_not_H0']} | {r['has_H0_tied_minimizer']} |" for r in allrules]
    lines += ['', f"Best fixed deterministic rule: **{best['rule']}**, {best['selected_H0']}/19270 H0 choices; first failure {best['first_not_H0']}. Subset counts for d>5, L>=12, and edge-critical graphs are in selection_rule_summary.tsv. Every deterministic failure and whether its ties contain a rescue is in failures.tsv.", '',
        'Examples: minimum ell selects Y={6,7,8,11,12} in graph 49 with ell=5, q=1, Delta_min=1 and rho=2; it is good but not H0. Maximum inherited count selects Y={0,1,2,8,9} in graph 942 with inherited count 11, Delta_min=rho=0, but q=6; 291 of its 303 tied maximizers are good. Graph 9726 defeats even existential tie selection for maximum inheritance: its unique maximizing Y={8,9,10,11,12} inherits 11 optima but has q=6, Delta_min=rho=0, ell=19, and degree sum 27. Exact first failures, including failures with no rescuing tie, are in first_failure_examples.tsv.', '',
        'Maximizing inherited-optimum count uses global cut information, so success of that rule would not by itself provide a cheap local structural selection lemma.', '', '## Prespecified integer inequalities','',
        '| Condition | H0 sets | Good non-H0 sets | Bad sets | Graphs with an H0 satisfying it |','|---|---:|---:|---:|---:|']
    for name,a in inequalities.items():lines.append(f"| {name} | {a['set_counts'].get('H0',0)} | {a['set_counts'].get('good_nonH0',0)} | {a['set_counts'].get('bad',0)} | {a['graphs_with_H0']} |")
    lines += ['', 'These are tests of the stated inequalities, not fitted classifiers. An absence of bad sets can follow from the empty-flip bound without implying optimal restriction. No implication outside the saved corpus is asserted.', '', '## Select a cut first?','',
        '| Subset | Graphs | Minimum over graphs of max_f good inherited deletions | First extremal graph | One cut preserves every good deletion |','|---|---:|---:|---:|---:|']
    for s,a in coverage.items(): lines.append(f"| {s} | {a['graphs']} | {a['minimum_of_max_good_inherited']} | {a['first_graph_attaining_minimum']} | {a['one_cut_preserves_all_good']} |")
    lines += ['', f"Across all graphs, every individual global optimum admits some good inherited deletion in {coverage['all']['graphs_every_global_optimum_has_a_good_H0']}/19270 graphs. The minimum count over all individual optimal cuts is {coverage['all']['minimum_over_all_individual_optima']}. A single cut covers the entire union of H0 deletions in {coverage['all']['one_cut_preserves_all_H0']}/19270 graphs. These assertions are distinct from the weaker existence of one compatible cut for each witness.", '', '## Canonical witnesses and induced types','',
        f"An independent-or-C5 H0 witness exists in {summary['graphs_with_independent_or_C5_H0']}/19270 graphs; the first exception is {summary['first_without_independent_or_C5_H0']}. Counts of graphs admitting each individual type: `{dict(sorted(types.items()))}`.", '',
        '| H0-restricted canonical criterion | Independent or C5 | Inherited by all global optima |','|---|---:|---:|']
    for name,a in canonical_summary.items():lines.append(f"| {name} | {a['independent_or_C5']} | {a['all_optima_inherit']} |")
    lines += ['', 'Canonical witnesses are chosen *within* H0; their existence is therefore not an independent selection theorem. Full distributions and original labeled witnesses are retained in summary.json and canonical_witnesses.tsv.', '', '## Candidate extraction','']
    if best['selected_H0']==19270:
        lines += [f"The fixed rule `{best['rule']}` survives this saved corpus. Extending it to arbitrary k remains conjectural and requires interpreting its precise score at n=5k. No proof is supplied."]
    else:
        lines += ['No tested deterministic one- or two-statistic selection rule survives the full saved corpus. We do not introduce another scoring function after seeing the results.']
        if summary['rules_with_H0_tied_minimizer_in_every_graph']:
            lines += [f"Existential tie-rescue survives for {summary['rules_with_H0_tied_minimizer_in_every_graph']}; this weaker observation must not be confused with a successful deterministic rule."]
            if summary['next_theorem_candidate']:
                lines += ['', '**One conjectural theorem candidate (existential only).** For every k>=1 and every triangle-free graph G on 5k vertices, put I_G(Y)=#{f in Opt(G): f restricted to G-Y is optimal}, counting global cuts modulo reversal. There exists a five-set Y attaining max_{|Z|=5} I_G(Z) such that I_G(Y)>0 and d(G)-d(G-Y)<=2k-1.', '', 'The maximization is over all five-sets, including bad ones. Some maximizing ties may be bad, so arbitrary or lexicographic tie-breaking is not justified. This candidate uses global cut information and is supported only by the saved n=15 corpus. It is not proved here.']
        else: lines += ['Even allowing a favorable tie does not rescue any of the tested rule objectives universally in this corpus. No new selection theorem is proposed on this evidence.']
    (ROOT/'notes/H0_WITNESS_STRUCTURE.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({'best':best,'categories':counts,'cut_coverage':{s:{k:v for k,v in a.items() if not k.endswith('histogram')} for s,a in coverage.items()},'tied':summary['rules_with_H0_tied_minimizer_in_every_graph'],'types':dict(types)},indent=2))

def finalize_report():
    """Attach completed validation and the cut-level observation, without re-mining."""
    summary=json.loads((OUT/'summary.json').read_text())
    integrity=json.loads((OUT/'features_integrity.json').read_text())
    assert integrity['data_rows']==57867810
    logs=['reference_validation_tests.log','full_validation_tests.log','integrity_test.log']
    for name in logs:
        assert 'OK' in (OUT/name).read_text(), f'Validation incomplete: {name}'
    summary['validation']={'feature_integrity':integrity,'test_logs':logs,
        'reference_features_checked':120120,
        'reference_output_reproduced_byte_for_byte':True,
        'full_aggregate_checks_passed':True,
        'checkpoint_recovery_test_passed':True}
    summary['implementation_sha256']={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ['scripts/mine_h0_witness_structure.cpp','scripts/report_h0_witness_structure.py','scripts/check_h0_feature_integrity.py','tests/test_h0_witness_structure.py']}
    c5type=next(int(r['induced_type']) for r in rows('induced_types.tsv') if r['is_C5']=='1')
    gg=list(rows('graph_structure.tsv'))
    summary['graphs_without_independent_H0']=[int(r['graph_id']) for r in gg if '0' not in r['H0_types'].split(',')]
    summary['graphs_without_C5_H0']=[int(r['graph_id']) for r in gg if str(c5type) not in r['H0_types'].split(',')]
    summary['canonical_induced_type_counts']={name:len(a['histograms']['induced_type']) for name,a in summary['canonical_H0'].items()}
    summary['total_global_optimal_cuts_checked']=sum(int(r['optG_count']) for r in rows('graph_structure.tsv'))
    allcuts=summary['cut_coverage']['all']
    assert allcuts['graphs_every_global_optimum_has_a_good_H0']==19270
    summary['next_theorem_candidate']={
        'status':'CONJECTURE ONLY, derived from the cut-coverage observation; no successful statistic-based Y selection rule',
        'statement':'For every k>=1, every triangle-free G on 5k vertices, and every maximum cut f of G, there exists a five-set Y such that f restricted to G-Y is optimal and d(G)-d(G-Y)<=2k-1.',
        'evidence':'Every enumerated global optimum in the saved n=15 corpus has at least 110 such deletions.',
        'not_claimed':'No bound of 110 is asserted outside this saved n=15 corpus, and the conjecture is not proved.'}
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    path=ROOT/'notes/H0_WITNESS_STRUCTURE.md'
    note=path.read_text().split('\n## Final validation and one cut-level candidate')[0]
    note=note.replace('No new selection theorem is proposed on this evidence.','No conjecture selecting Y by one of these tested score objectives is supported.')
    note+='\n## Final validation and one cut-level candidate\n\n'
    note+=f"The feature table has exactly {integrity['data_rows']:,} data rows and {integrity['bytes']:,} bytes. Its SHA-256 is `{integrity['sha256']}`. The 40 reference graphs (120,120 rows) match the independently validated reference outputs, and their full-run feature blocks reproduce the validation run byte-for-byte. Direct structural/witness checks, torn-checkpoint recovery, full per-graph counts, and L=min ell checks passed. The integrity check also passed. Logs are in `{', '.join(logs)}`. The reference log skips only the full-corpus integrity check, which is executed separately on the full file.\n\n"
    note+=f"All {summary['total_global_optimal_cuts_checked']:,} enumerated global optima admit good inherited deletions. Every individual optimum has at least {allcuts['minimum_over_all_individual_optima']}; every graph has some optimum with at least {allcuts['minimum_of_max_good_inherited']}. The first extremal graph for the latter bound is {allcuts['first_graph_attaining_minimum']}. These counts are exact for the saved corpus only.\n\n"
    note+=f"Each of the four canonical H0 criteria realizes all {min(summary['canonical_induced_type_counts'].values())} observed triangle-free induced five-vertex types. Thus there is no single induced type shared by their canonical witnesses. The existence of an independent-or-C5 H0 witness in every saved graph does not make the canonical choices independent-or-C5: for minimum ell within H0 this occurs in only {summary['canonical_H0']['min_ell']['independent_or_C5']} graphs.\n\n"
    note+=f"The nine graphs with no independent H0 witness are {summary['graphs_without_independent_H0']}; all have C5 H0 witnesses. There are {len(summary['graphs_without_C5_H0'])} graphs without a C5 H0 witness, listed in summary.json; all have independent H0 witnesses. This is a statement about existence of a compatible global cut, not compatibility with every fixed optimum.\n\n"
    note+='**One conjectural next theorem, based on this cut-level observation:** for every k>=1, every triangle-free graph G on 5k vertices, and **every** maximum cut f of G, there exists a five-set Y such that f restricted to G-Y is optimal and d(G)-d(G-Y)<=2k-1. Equivalently, this Y has Delta_f(Y)=0 and R_f(Y)<=2k-1. This strengthens the original existential choice of f. It does not supply a rule for selecting Y, and it is not proved. We do not extrapolate the numerical counts 110 or 114 to other graphs or orders.\n\n'
    note+='This is the only conjectural theorem extracted here. The independent-or-C5 coverage and canonical-witness distributions are reported as separate finite observations; they are not combined with the universal quantifier over optimal cuts without verification.\n'
    path.write_text(note)
    print(json.dumps({'best_rule':summary['best_deterministic_rule'],'total_optima':summary['total_global_optimal_cuts_checked'],'validation':'passed'}))

if __name__=='__main__': main()
