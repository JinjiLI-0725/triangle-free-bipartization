#!/usr/bin/env python3
"""Assemble a completed audit, or the exact prefix ending at first failure."""
import csv,hashlib,json
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results/global_cut_landscape_n15_full'

def rows(p):
    with p.open() as f:return list(csv.DictReader(f,delimiter='\t'))
def main():
    manifest=json.loads((OUT/'manifest.json').read_text())
    src=ROOT/manifest['corpus']
    assert hashlib.sha256(src.read_bytes()).hexdigest()==manifest['corpus_sha256']
    input_order=[];encodings={}
    with src.open() as f:
        while line:=f.readline():
            i,g,n,m,_=line.split();i=int(i);assert i not in encodings
            input_order.append(i);encodings[i]=g
            for _ in range(int(m)):f.readline()
    assert len(input_order)==19270
    done={int(p.stem) for p in (OUT/'checkpoints').glob('*.done')}
    ids=[i for i in input_order if i in done]
    assert ids==input_order[:len(ids)],'Non-prefix audit cannot certify first failure'
    first=int((OUT/'FIRST_FAILURE').read_text()) if (OUT/'FIRST_FAILURE').exists() else None
    assert (len(ids)==19270 and first is None) or (first is not None and ids[-1]==first)
    graphs=[];witnesses=[];fails=[];digest=hashlib.sha256();hists={k:Counter() for k in ('d','L','critical','good_min_delta','good_min_rho')}
    header=None;wh=None
    for i in ids:
        cp=OUT/'checkpoints';rr=rows(cp/f'{i}.summary.tsv');assert len(rr)==1
        r=rr[0];assert r['graph6']==encodings[i];graphs.append(r)
        ws=rows(cp/f'{i}.witness.tsv');assert len(ws)<=1;witnesses.extend(ws)
        if not ws:fails.append(r)
        blob=(cp/f'{i}.landscape.bin').read_bytes();assert len(blob)==9009
        digest.update(i.to_bytes(4,'little'));digest.update(blob)
        assert sum(int(r[f'good_rho{j}']) for j in range(6))==int(r['good_count'])
        assert (int(r['good_rho0'])>0)==bool(ws)
        for key,field in [('d','dG'),('L','L'),('critical','d_edge_critical'),('good_min_delta','good_min_delta'),('good_min_rho','good_min_rho')]:hists[key][int(r[field])]+=1
    assert len(fails)==(first is not None)
    if fails:assert int(fails[0]['id'])==first
    def write_table(name,rs,keys):
        path=OUT/name
        if path.exists():raise RuntimeError('Refusing to overwrite '+str(path))
        with path.open('w') as f:
            w=csv.DictWriter(f,fieldnames=keys,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rs)
    write_table('graph_summary.tsv',graphs,list(graphs[0]))
    if witnesses:wkeys=list(witnesses[0])
    else:wkeys=list(csv.DictReader((OUT/'checkpoints'/f'{ids[0]}.witness.tsv').open(),delimiter='\t').fieldnames)
    write_table('h0_witnesses.tsv',witnesses,wkeys)
    write_table('failures.tsv',fails,list(graphs[0]))
    complete=len(ids)==19270
    sample_ids={int(r['corpus_id']) for r in rows(ROOT/'results/global_cut_landscape_n15/sample_manifest.tsv')}
    requested={401,1676,6132,10116};priorcrit={8814,9965,19082};b3={19269}
    def group(pred,expected=None):
        rs=[r for r in graphs if pred(r)];bad=[int(r['id']) for r in rs if not int(r['good_rho0'])]
        return {'analyzed':len(rs),'expected':expected,'h0_pass':len(rs)-len(bad),'failures':bad,
                'survives':False if bad else True if complete or expected==len(rs) else None}
    subsets={
      'all_saved_canonical_n15':group(lambda r:True,19270),
      'global_L_ge_12':group(lambda r:int(r['L'])>=12,5337),
      'd_gt_5':group(lambda r:int(r['dG'])>5,2103),
      'd_edge_critical':group(lambda r:int(r['d_edge_critical'])==1),
      'previous_40_graph_sample':group(lambda r:int(r['id']) in sample_ids,40),
      'requested_witness_ids':group(lambda r:int(r['id']) in requested,4),
      'previous_critical_witness_ids':group(lambda r:int(r['id']) in priorcrit,3),
      'B3':group(lambda r:int(r['id']) in b3,1)}
    oldd=dict(map(lambda s:map(int,s.split()),(ROOT/'results/hard_regime_L_n15/d.tsv').read_text().splitlines()))
    oldhard={int(r['id']):r for r in rows(ROOT/'results/hard_regime_L_n15/hard_classes.tsv')}
    mismatches=[];critical_changes=[]
    for r in graphs:
        i=int(r['id'])
        if int(r['dG'])!=oldd[i]:mismatches.append({'id':i,'field':'d'})
        if i in oldhard:
            if r['L']!=oldhard[i]['L']:mismatches.append({'id':i,'field':'L'})
            if r['d_edge_critical']!=oldhard[i]['d_edge_critical']:critical_changes.append({'id':i,'old':oldhard[i]['d_edge_critical'],'exact':r['d_edge_critical']})
    assert not mismatches,mismatches
    s={'scope':manifest['scope'],'graphs_analyzed':len(ids),'expected_graphs':19270,'complete':complete,
       'five_sets_analyzed':len(ids)*3003,'global_cuts_per_graph':16384,'core_cuts_per_five_set':512,
       'all_cut_computations_exact':True,'h0_pass_count':len(witnesses),'h0_survives_full_saved_corpus':complete and not fails,
       'first_failure':first,'first_failure_graph6':encodings[first] if first is not None else None,
       'priority_subsets':subsets,'max_min_delta_good':max(int(r['good_min_delta']) for r in graphs),
       'max_min_rho_good':max(int(r['good_min_rho']) for r in graphs),'histograms':hists,
       'critical_ids':[int(r['id']) for r in graphs if int(r['d_edge_critical'])],
       'global_identity_checks':sum(int(r['identities_checked']) for r in graphs),
       'all_fiveset_binary_sha256':digest.hexdigest(),'prior_d_L_mismatches':mismatches,
       'prior_critical_flag_corrections':critical_changes,
       'validation':'Every one of the 120120 sample five-sets compared to prior validated BFS landscape; independent recurrence verifies every saved H0 witness core optimum.',
       'no_good_Y_sentinel':99,
       'next_theorem_target':'Prove existence of a five-set Y such that q(Y)<=2k-1 and some global optimal cut of G restricts optimally to G-Y.' if complete and not fails else None}
    s['sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [src,ROOT/'scripts/analyze_global_cut_landscape_n15.cpp',ROOT/'scripts/analyze_global_cut_h0_full.cpp',ROOT/'scripts/report_global_cut_h0_full.py',ROOT/'tests/test_global_cut_h0_full.py',OUT/'graph_summary.tsv',OUT/'h0_witnesses.tsv',OUT/'failures.tsv']}
    (OUT/'summary.json').write_text(json.dumps(s,indent=2,sort_keys=True)+'\n')
    note=['# Full saved-corpus H0 audit','',f"**Exact finite computation:** {len(ids):,}/{19270:,} canonical saved graphs; {len(ids)*3003:,} five-sets. H0 passes {len(witnesses):,} graphs. First failure: {first if first is not None else 'none'}.",'',
      'This is the same frozen canonical corpus as the 40-graph discovery experiment, assembled from saved records. It is not all triangle-free graphs on 15 vertices. No new graphs, n=20 cases, or local certificate families were generated. The genuine-counterexample condition d=10 is not present in this corpus.','',
      '## Priority subsets','', '| Subset | Analyzed | H0 passes | Failures |','|---|---:|---:|---|']
    for name,g in subsets.items():note.append(f"| {name} | {g['analyzed']} | {g['h0_pass']} | {g['failures'] or 'none'} |")
    note+=['',f"Maximum, over analyzed graphs, of min Delta_min among good Y: **{s['max_min_delta_good']}**. The corresponding maximum of min rho is **{s['max_min_rho_good']}**. Sentinel 99 means no good five-set, if encountered.",'',
      '## Exact computation and storage','',
      'For every graph the checker enumerates all 16,384 global cuts modulo reversal, retains every optimum, and recomputes d-edge-criticality by whether every edge is monochromatic in some optimum. For every one of the 3,003 five-sets it evaluates all 512 core cuts modulo reversal, computes d(H), q, and Delta_min, and checks q=R+Delta for every global optimum.',
      '',
      'The core has 45 possible edges. Its monochromatic cost is e(H)-popcount(edge_mask & cut_mask), with all 512 cut masks precomputed. This is exact cut enumeration. If Delta_min=0, rho=0 follows from a directly verified compatible optimum. Otherwise the checker searches Hamming shells of radii 1 through 5 over all restricted global optima, identifying reversal on the core. The first shell containing any optimal core coloring gives the exact rho.',
      '',
      f"Total global-optimum/five-set identity checks: {s['global_identity_checks']:,}. No early H0 success skips other five-sets. A failure stops processing immediately after its full 3,003-row landscape is saved; no later graph is started.",
      '',
      'Each graph is checkpointed atomically. Its `.landscape.bin` contains 3,003 triples of unsigned bytes (dH, Delta_min, rho), in ascending Y-mask order among masks with five bits. q=dG-dH. Every global optimum is saved in `.opt.txt`. Thus all requested per-five-set quantities remain recoverable even for passing graphs, without enormous text output. The first failure, if any, also receives a graph6 file and full textual landscape.',
      '',
      'The witness table records the first successful Y in ascending mask order and the first compatible global optimum. f uses the original 15 vertex labels, with vertex 0 fixed to color zero. h uses the ascending core vertex order and the inherited orientation. Its cost is exactly d(H), with Delta=rho=0.',
      '',
      '## Validation and historical metadata','',
      'The full driver was checked against every five-set of all 40 validated sample graphs: all d(H), Delta_min, rho, complete Opt(G) lists, and graph summaries agree. Independent Python checks verify all saved H0 witnesses, including a separate 512-cut recurrence for every witness core. The same tests check full completion and output counts.',
      '',f"All recomputed d and saved hard-regime L values agree with their previous exact audits. Criticality is recomputed rather than inherited. Historical critical-flag corrections: `{critical_changes}`. Historical files were not overwritten.",
      '',
      '## Interpretation','',
      'If H0 survives, this is exhaustive evidence for the full saved corpus only. It does not prove Candidate A, the Erdős bound, or H0 for all triangle-free graphs. No symbolic lemma is attempted during this audit.',
      '',f"NEXT_THEOREM_TARGET = {s['next_theorem_target']}",
      '', '## Reproduction','', '```sh',
      'g++ -std=c++17 -O3 -march=native -o /tmp/analyze_global_cut_h0_full scripts/analyze_global_cut_h0_full.cpp',
      '/tmp/analyze_global_cut_h0_full results/zero_margin_tightness/corpus.txt results/global_cut_landscape_n15_full',
      'python3 scripts/report_global_cut_h0_full.py',
      'python3 -m unittest discover -s tests -p test_global_cut_h0_full.py -v','```',
      '', 'The manifest pins the source corpus hash. Summary hashes pin the inputs, checker, tests, and aggregate outputs. Rerunning the checker resumes completed checkpoints; an existing failure marker prevents continuation beyond a failure.']
    (ROOT/'notes/GLOBAL_CUT_H0_FULL_CORPUS.md').write_text('\n'.join(note)+'\n')
    print(json.dumps({k:s[k] for k in ['graphs_analyzed','h0_survives_full_saved_corpus','first_failure','priority_subsets','max_min_delta_good','max_min_rho_good']}))
if __name__=='__main__':main()
