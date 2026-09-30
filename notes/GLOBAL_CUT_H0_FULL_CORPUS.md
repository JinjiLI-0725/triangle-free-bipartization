# Full saved-corpus H0 audit

**Exact finite computation:** 19,270/19,270 canonical saved graphs; 57,867,810 five-sets. H0 passes 19,270 graphs. First failure: none.

This is the same frozen canonical corpus as the 40-graph discovery experiment, assembled from saved records. It is not all triangle-free graphs on 15 vertices. No new graphs, n=20 cases, or local certificate families were generated. The genuine-counterexample condition d=10 is not present in this corpus.

## Priority subsets

| Subset | Analyzed | H0 passes | Failures |
|---|---:|---:|---|
| all_saved_canonical_n15 | 19270 | 19270 | none |
| global_L_ge_12 | 5337 | 5337 | none |
| d_gt_5 | 2103 | 2103 | none |
| d_edge_critical | 7 | 7 | none |
| previous_40_graph_sample | 40 | 40 | none |
| requested_witness_ids | 4 | 4 | none |
| previous_critical_witness_ids | 3 | 3 | none |
| B3 | 1 | 1 | none |

Maximum, over analyzed graphs, of min Delta_min among good Y: **0**. The corresponding maximum of min rho is **0**. Sentinel 99 means no good five-set, if encountered.

## Exact computation and storage

For every graph the checker enumerates all 16,384 global cuts modulo reversal, retains every optimum, and recomputes d-edge-criticality by whether every edge is monochromatic in some optimum. For every one of the 3,003 five-sets it evaluates all 512 core cuts modulo reversal, computes d(H), q, and Delta_min, and checks q=R+Delta for every global optimum.

The core has 45 possible edges. Its monochromatic cost is e(H)-popcount(edge_mask & cut_mask), with all 512 cut masks precomputed. This is exact cut enumeration. If Delta_min=0, rho=0 follows from a directly verified compatible optimum. Otherwise the checker searches Hamming shells of radii 1 through 5 over all restricted global optima, identifying reversal on the core. The first shell containing any optimal core coloring gives the exact rho.

Total global-optimum/five-set identity checks: 142,147,005. No early H0 success skips other five-sets. A failure stops processing immediately after its full 3,003-row landscape is saved; no later graph is started.

Each graph is checkpointed atomically. Its `.landscape.bin` contains 3,003 triples of unsigned bytes (dH, Delta_min, rho), in ascending Y-mask order among masks with five bits. q=dG-dH. Every global optimum is saved in `.opt.txt`. Thus all requested per-five-set quantities remain recoverable even for passing graphs, without enormous text output. The first failure, if any, also receives a graph6 file and full textual landscape.

The witness table records the first successful Y in ascending mask order and the first compatible global optimum. f uses the original 15 vertex labels, with vertex 0 fixed to color zero. h uses the ascending core vertex order and the inherited orientation. Its cost is exactly d(H), with Delta=rho=0.

## Validation and historical metadata

The full driver was checked against every five-set of all 40 validated sample graphs: all d(H), Delta_min, rho, complete Opt(G) lists, and graph summaries agree. Independent Python checks verify all saved H0 witnesses, including a separate 512-cut recurrence for every witness core. The same tests check full completion and output counts.

All recomputed d and saved hard-regime L values agree with their previous exact audits. Criticality is recomputed rather than inherited. Historical critical-flag corrections: `[{'id': 19082, 'old': '0', 'exact': '1'}, {'id': 19083, 'old': '0', 'exact': '1'}, {'id': 19269, 'old': '0', 'exact': '1'}]`. Historical files were not overwritten.

## Interpretation

If H0 survives, this is exhaustive evidence for the full saved corpus only. It does not prove Candidate A, the Erdős bound, or H0 for all triangle-free graphs. No symbolic lemma is attempted during this audit.

NEXT_THEOREM_TARGET = Prove existence of a five-set Y such that q(Y)<=2k-1 and some global optimal cut of G restricts optimally to G-Y.

## Reproduction

```sh
g++ -std=c++17 -O3 -march=native -o /tmp/analyze_global_cut_h0_full scripts/analyze_global_cut_h0_full.cpp
/tmp/analyze_global_cut_h0_full results/zero_margin_tightness/corpus.txt results/global_cut_landscape_n15_full
python3 scripts/report_global_cut_h0_full.py
python3 -m unittest discover -s tests -p test_global_cut_h0_full.py -v
```

The manifest pins the source corpus hash. Summary hashes pin the inputs, checker, tests, and aggregate outputs. Rerunning the checker resumes completed checkpoints; an existing failure marker prevents continuation beyond a failure.

Final validation: **3 tests passed, no failures, errors, or skips**. Every saved H0 witness core optimum was independently recomputed. Details: `results/global_cut_landscape_n15_full/validation.json`.
