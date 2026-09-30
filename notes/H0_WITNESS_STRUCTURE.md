# H0 witness structure in the full saved n=15 corpus

**Status: exact finite computational evidence, not a graph-theoretic theorem.**

All 19,270 saved canonical graphs and all 57,867,810 five-sets were processed. This corpus is not the set of all triangle-free graphs on 15 vertices. No graphs were generated.

## Exact computation and reproducibility

The miner reuses the validated binary landscapes for d(G-Y), Delta_min and rho and the complete lists of optimal global cuts. For every five-set it independently counts surviving monochromatic edges under every saved optimal cut. It checks the minimum against saved Delta_min and verifies that a positive inherited-optimum count is equivalent both to Delta_min=0 and rho=0. A witness cut is saved for every H0 row. Counts/fractions use integers; no floating-point fitting is involved.

Scripts: `scripts/mine_h0_witness_structure.cpp`, `scripts/report_h0_witness_structure.py`. Tests: `tests/test_h0_witness_structure.py`. The manifest freezes the twelve rules and source hashes before execution. Six output streams are checkpointed by byte offset after each graph. The feature table is uncompressed TSV.

Reproduce with `g++ -std=c++17 -O3 -march=native scripts/mine_h0_witness_structure.cpp -o /tmp/mine_h0_witness_structure`, then `/tmp/mine_h0_witness_structure results/zero_margin_tightness/corpus.txt results/global_cut_landscape_n15_full results/h0_witness_structure`. Completed graphs are skipped on resume. Run `python3 scripts/check_h0_feature_integrity.py` and `python3 scripts/report_h0_witness_structure.py` after completion. The test module accepts `H0_STRUCTURE_DIR` to point to a separate reference run.

`min_degree_in_Y` and `max_degree_in_Y` are the ambient G-degrees of vertices belonging to Y. Separate induced-degree columns remove ambiguity. `induced_type` is the minimum 10-bit adjacency code over all 120 vertex permutations, with edge-bit order (0,1),(0,2),(1,2),...,(3,4). Cut masks use original vertex labels and fix vertex 0 to color 0. Fractions are exact numerator/denominator, not necessarily reduced.

## Three categories

| Category | Five-sets |
|---|---:|
| H0 | 43,510,199 |
| good_nonH0 | 13,693,349 |
| bad | 664,262 |

| Category | Feature | Minimum | Maximum | Exact mean |
|---|---|---:|---:|---:|
| H0 | rho | 0 | 0 | 0 |
| H0 | ell | 2 | 50 | 686478534/43510199 |
| H0 | degree_sum | 3 | 50 | 958977522/43510199 |
| H0 | boundary_size | 2 | 50 | 684486516/43510199 |
| H0 | inherited_count | 1 | 42 | 72812610/43510199 |
| good_nonH0 | rho | 1 | 5 | 28660794/13693349 |
| good_nonH0 | ell | 4 | 45 | 221724210/13693349 |
| good_nonH0 | degree_sum | 5 | 45 | 309672454/13693349 |
| good_nonH0 | boundary_size | 4 | 45 | 221165112/13693349 |
| good_nonH0 | inherited_count | 0 | 0 | 0 |
| bad | rho | 0 | 5 | 179509/332131 |
| bad | ell | 12 | 37 | 6256179/332131 |
| bad | degree_sum | 16 | 37 | 8364059/332131 |
| bad | boundary_size | 10 | 37 | 6237791/332131 |
| bad | inherited_count | 0 | 20 | 1074935/664262 |

Exact mean inherited-optimum fractions by category: `{'H0': '20340341123209782149/25334787591562749300', 'good_nonH0': '0', 'bad': '89563484885731/289941096545100'}`. Full rational fraction distributions are in summary.json.

Complete integer histograms for q, Delta_min, rho, ell, degree sum, boundary size, induced type, components, degrees, and inherited-optimum count are in summary.json. These distinguish good non-H0 sets (positive reoptimization is unavoidable) from H0 sets; bad sets can still preserve optimality.

## Fixed selection rules

Each deterministic choice uses the stated one or two statistics, then the lexicographically smallest increasing vertex tuple. This differs from numeric mask order. “Tied H0” asks whether at least one minimizer before that final tie-break is H0; it is not the success count of the deterministic rule.

| Rule | Selected good | Selected H0 | First non-H0 | Graphs with a tied H0 |
|---|---:|---:|---:|---:|
| min_ell | 19088 | 17868 | 49 | 18860 |
| min_degree_sum | 18686 | 14768 | 1 | 18066 |
| min_boundary | 19080 | 17870 | 49 | 18869 |
| max_inherited_count | 19124 | 19124 | 942 | 19269 |
| min_ell_then_max_inherited | 19010 | 18693 | 166 | 18760 |
| min_degree_sum_then_max_inherited | 18898 | 17956 | 26 | 18056 |
| min_boundary_then_max_inherited | 19004 | 18697 | 166 | 18762 |
| max_inherited_then_min_ell | 18959 | 18959 | 403 | 19073 |
| max_inherited_then_min_degree_sum | 19133 | 19133 | 807 | 19212 |
| max_inherited_then_min_boundary | 18936 | 18936 | 403 | 19062 |
| min_ell_then_min_degree_sum | 19082 | 17918 | 49 | 18572 |
| min_boundary_then_min_degree_sum | 19074 | 17915 | 49 | 18588 |

Best fixed deterministic rule: **max_inherited_then_min_degree_sum**, 19133/19270 H0 choices; first failure 807. Subset counts for d>5, L>=12, and edge-critical graphs are in selection_rule_summary.tsv. Every deterministic failure and whether its ties contain a rescue is in failures.tsv.

Examples: minimum ell selects Y={6,7,8,11,12} in graph 49 with ell=5, q=1, Delta_min=1 and rho=2; it is good but not H0. Maximum inherited count selects Y={0,1,2,8,9} in graph 942 with inherited count 11, Delta_min=rho=0, but q=6; 291 of its 303 tied maximizers are good. Graph 9726 defeats even existential tie selection for maximum inheritance: its unique maximizing Y={8,9,10,11,12} inherits 11 optima but has q=6, Delta_min=rho=0, ell=19, and degree sum 27. Exact first failures, including failures with no rescuing tie, are in first_failure_examples.tsv.

Maximizing inherited-optimum count uses global cut information, so success of that rule would not by itself provide a cheap local structural selection lemma.

## Prespecified integer inequalities

| Condition | H0 sets | Good non-H0 sets | Bad sets | Graphs with an H0 satisfying it |
|---|---:|---:|---:|---:|
| ell<=10 | 3272396 | 563072 | 0 | 10437 |
| ell<=11 | 5491953 | 1100279 | 0 | 13853 |
| degree_sum<=11 | 308499 | 34087 | 0 | 2709 |
| boundary_size<=9 | 1679848 | 239423 | 0 | 8053 |

These are tests of the stated inequalities, not fitted classifiers. An absence of bad sets can follow from the empty-flip bound without implying optimal restriction. No implication outside the saved corpus is asserted.

## Select a cut first?

| Subset | Graphs | Minimum over graphs of max_f good inherited deletions | First extremal graph | One cut preserves every good deletion |
|---|---:|---:|---:|---:|
| all | 19270 | 114 | 19082 | 124 |
| d_gt_5 | 2103 | 114 | 19082 | 2 |
| L_ge_12 | 5337 | 114 | 19082 | 43 |
| edge_critical | 7 | 114 | 19082 | 1 |

Across all graphs, every individual global optimum admits some good inherited deletion in 19270/19270 graphs. The minimum count over all individual optimal cuts is 110. A single cut covers the entire union of H0 deletions in 8639/19270 graphs. These assertions are distinct from the weaker existence of one compatible cut for each witness.

## Canonical witnesses and induced types

An independent-or-C5 H0 witness exists in 19270/19270 graphs; the first exception is None. Counts of graphs admitting each individual type: `{0: 19261, 1: 19245, 3: 19255, 11: 19259, 12: 18344, 13: 19145, 30: 19249, 75: 19216, 76: 19147, 77: 19261, 86: 19155, 94: 19263, 222: 18704, 236: 18663}`.

| H0-restricted canonical criterion | Independent or C5 | Inherited by all global optima |
|---|---:|---:|
| min_ell | 20 | 14340 |
| min_degree_sum | 8108 | 13753 |
| min_boundary | 1495 | 14433 |
| lex_vertices | 7942 | 13671 |

Canonical witnesses are chosen *within* H0; their existence is therefore not an independent selection theorem. Full distributions and original labeled witnesses are retained in summary.json and canonical_witnesses.tsv.

## Candidate extraction

No tested deterministic one- or two-statistic selection rule survives the full saved corpus. We do not introduce another scoring function after seeing the results.
Even allowing a favorable tie does not rescue any of the tested rule objectives universally in this corpus. No conjecture selecting Y by one of these tested score objectives is supported.

## Final validation and one cut-level candidate

The feature table has exactly 57,867,810 data rows and 6,207,068,497 bytes. Its SHA-256 is `d387462c0a778cc847d51640614589b85d645fdee237101b2923dc66ccf34568`. The 40 reference graphs (120,120 rows) match the independently validated reference outputs, and their full-run feature blocks reproduce the validation run byte-for-byte. Direct structural/witness checks, torn-checkpoint recovery, full per-graph counts, and L=min ell checks passed. The integrity check also passed. Logs are in `reference_validation_tests.log, full_validation_tests.log, integrity_test.log`. The reference log skips only the full-corpus integrity check, which is executed separately on the full file.

All 47,335 enumerated global optima admit good inherited deletions. Every individual optimum has at least 110; every graph has some optimum with at least 114. The first extremal graph for the latter bound is 19082. These counts are exact for the saved corpus only.

Each of the four canonical H0 criteria realizes all 14 observed triangle-free induced five-vertex types. Thus there is no single induced type shared by their canonical witnesses. The existence of an independent-or-C5 H0 witness in every saved graph does not make the canonical choices independent-or-C5: for minimum ell within H0 this occurs in only 20 graphs.

The nine graphs with no independent H0 witness are [5448, 8600, 9965, 17209, 18951, 19082, 19083, 19248, 19269]; all have C5 H0 witnesses. There are 607 graphs without a C5 H0 witness, listed in summary.json; all have independent H0 witnesses. This is a statement about existence of a compatible global cut, not compatibility with every fixed optimum.

**One conjectural next theorem, based on this cut-level observation:** for every k>=1, every triangle-free graph G on 5k vertices, and **every** maximum cut f of G, there exists a five-set Y such that f restricted to G-Y is optimal and d(G)-d(G-Y)<=2k-1. Equivalently, this Y has Delta_f(Y)=0 and R_f(Y)<=2k-1. This strengthens the original existential choice of f. It does not supply a rule for selecting Y, and it is not proved. We do not extrapolate the numerical counts 110 or 114 to other graphs or orders.

This is the only conjectural theorem extracted here. The independent-or-C5 coverage and canonical-witness distributions are reported as separate finite observations; they are not combined with the universal quantifier over optimal cuts without verification.
