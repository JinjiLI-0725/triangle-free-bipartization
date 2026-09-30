# Global cut landscape: bounded n=15 discovery experiment

**Exact computation on a deterministic sample; no universal theorem is claimed.**

Analyzed 40 saved graphs and all 120,120 five-sets. For each graph all 16,384 cuts modulo reversal were checked; for every remainder all 512 cuts modulo reversal were checked. The code also computes redundant reversed costs to verify invariance. All 615,615 global-optimum/five-set identities passed.

## Selection and scope

The maximum observed d is 9; none of these graphs satisfies the genuine-counterexample equation d=10 at k=3. This is a discovery experiment about selection and compatibility, not a test of an existing full-hypothesis counterexample.

The frozen manifest records every selection reason. It includes requested IDs 401, 1676, 6132, 10116; B3; saved critical witnesses; the top eight saved d values by ID; representatives for every saved hard L level; and additional d and (L,d) strata, stopping at 40. Input graphs come exclusively from the saved canonical corpus. No graph was generated.

The three-layer 35-edge fixed-Y construction was not found in the saved corpus by its necessary degree and component signature; not generated.

Criticality was recomputed from exact optimal cuts: every edge must be monochromatic in at least one optimum. Saved flags were only selection metadata. Discrepancies are listed below and in JSON; historical files were not modified.

## Main observations

H0 survives: **True**. First failure: **none**. Maximum, over sampled graphs, of minimum rho among good five-sets: **0**.

Good-Y rho distribution: `{0: 86497, 1: 4049, 2: 2774, 3: 1752, 4: 1795, 5: 603}`.
Bad-Y rho distribution: `{0: 18233, 1: 1871, 2: 1401, 3: 745, 4: 238, 5: 162}`.

The primary empirical hypothesis is: every graph in the intended hard domain admits a good five-set whose remainder has an optimal coloring inherited from an optimal coloring of the full graph. The experiment supports this only to the extent recorded by H0; no claim is made for all saved classes or full counterexample hypotheses.

Restricting to d(G)>=6 gives 20 nontrivial graphs; H0 survives all of them. Their good-Y rho histogram is `{0: 29848, 1: 2824, 2: 2426, 3: 1090, 4: 1054, 5: 168}`. All four exactly critical sampled graphs also satisfy H0.

Selection matters: some nontrivial good deletions have rho=5 even though Delta_min=1. The first such recorded witness is `{'id': 1649, 'Y_mask': 13441, 'q': 4, 'rho': 5, 'delta_min': 1, 'f_witness': 31856, 'h_witness_local': 63, 'S_mask': 18446, 'Delta_witness': 1}`. Thus a small reoptimization gain does not imply a small switching distance. No bounded-radius claim for arbitrary good Y is supported.

If H0 survives, the minimum-rho switching family is exactly the empty set, for every minimum-distance witness pair. This is selection-dependent compatibility, not evidence that arbitrary deletions require only small local repairs. Nonempty witnesses below describe other good deletions.

A compatible deletion also attains the minimum q over all five-sets in **40/40** sampled graphs. This stronger sample observation is recorded without replacing H0 as the primary hypothesis.

## Per-graph exact results

| ID | d | L | Opt(G) | critical | min q | good Y | min rho (good) | min Delta_min (good) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 401 | 6 | 11 | 4 | 0 | 3 | 2526 | 0 | 0 |
| 1676 | 6 | 11 | 4 | 0 | 3 | 2742 | 0 | 0 |
| 6132 | 6 | 11 | 6 | 0 | 3 | 2722 | 0 | 0 |
| 10116 | 6 | 11 | 3 | 0 | 3 | 2886 | 0 | 0 |
| 19269 | 9 | 18 | 35 | 1 | 5 | 243 | 0 | 0 |
| 8814 | 7 | 13 | 5 | 1 | 4 | 2628 | 0 | 0 |
| 9965 | 8 | 12 | 27 | 1 | 5 | 321 | 0 | 0 |
| 8600 | 8 | 17 | 7 | 0 | 4 | 243 | 0 | 0 |
| 19082 | 8 | 12 | 30 | 1 | 4 | 218 | 0 | 0 |
| 1292 | 7 | 12 | 10 | 0 | 4 | 1834 | 0 | 0 |
| 1301 | 7 | 12 | 4 | 0 | 3 | 1827 | 0 | 0 |
| 1352 | 7 | 11 | 10 | 0 | 4 | 1827 | 0 | 0 |
| 1355 | 7 | 12 | 4 | 0 | 3 | 1964 | 0 | 0 |
| 964 | 0 | 25 | 1 | 0 | 0 | 3003 | 0 | 0 |
| 333 | 0 | 24 | 1 | 0 | 0 | 3003 | 0 | 0 |
| 15071 | 0 | 23 | 1 | 0 | 0 | 3003 | 0 | 0 |
| 132 | 0 | 22 | 1 | 0 | 0 | 3003 | 0 | 0 |
| 314 | 0 | 21 | 1 | 0 | 0 | 3003 | 0 | 0 |
| 326 | 0 | 20 | 1 | 0 | 0 | 3003 | 0 | 0 |
| 2368 | 1 | 19 | 1 | 0 | 0 | 3003 | 0 | 0 |
| 264 | 0 | 18 | 1 | 0 | 0 | 3003 | 0 | 0 |
| 254 | 0 | 17 | 1 | 0 | 0 | 3003 | 0 | 0 |
| 900 | 2 | 16 | 1 | 0 | 0 | 3003 | 0 | 0 |
| 275 | 1 | 15 | 1 | 0 | 0 | 3003 | 0 | 0 |
| 108 | 1 | 14 | 1 | 0 | 0 | 3003 | 0 | 0 |
| 82 | 1 | 13 | 1 | 0 | 0 | 3003 | 0 | 0 |
| 120 | 2 | 12 | 1 | 0 | 0 | 3003 | 0 | 0 |
| 89 | 2 | 11 | 1 | 0 | 0 | 3003 | 0 | 0 |
| 398 | 6 | 10 | 3 | 0 | 3 | 2526 | 0 | 0 |
| 148 | 5 | 10 | 8 | 0 | 2 | 3003 | 0 | 0 |
| 78 | 4 | 9 | 2 | 0 | 2 | 3003 | 0 | 0 |
| 56 | 3 | 7 | 3 | 0 | 0 | 3003 | 0 | 0 |
| 15 | 2 | 5 | 1 | 0 | 0 | 3003 | 0 | 0 |
| 0 | 1 | 7 | 1 | 0 | 0 | 3003 | 0 | 0 |
| 2564 | 7 | 15 | 2 | 0 | 3 | 1942 | 0 | 0 |
| 2282 | 7 | 14 | 8 | 0 | 3 | 1693 | 0 | 0 |
| 2134 | 7 | 13 | 9 | 0 | 3 | 1656 | 0 | 0 |
| 1649 | 6 | 15 | 1 | 0 | 2 | 2511 | 0 | 0 |
| 614 | 6 | 14 | 1 | 0 | 2 | 2356 | 0 | 0 |
| 1290 | 6 | 13 | 2 | 0 | 2 | 2745 | 0 | 0 |

## Good versus bad distributions

These are exact histograms pooled over five-sets; the JSON retains per-graph q and Delta histograms. Pooling does not establish causal structure. Every individual row remains available in fiveset_summary.tsv.

- delta_min: good `{0: 86497, 1: 7568, 2: 2868, 3: 148, 4: 277, 5: 112}`; bad `{0: 18233, 1: 2174, 2: 1385, 3: 371, 4: 304, 5: 39, 6: 144}`.
- optH_count: good `{1: 64240, 2: 14140, 3: 4838, 4: 3980, 5: 3374, 6: 1635, 7: 670, 8: 498, 9: 877, 10: 186, 11: 198, 12: 382, 13: 107, 14: 62, 15: 1007, 16: 309, 17: 1, 18: 3, 20: 155, 22: 1, 24: 27, 26: 2, 32: 335, 40: 4, 44: 1, 64: 241, 128: 100, 256: 11, 512: 86}`; bad `{1: 14772, 2: 5098, 3: 912, 4: 1140, 5: 300, 6: 139, 7: 30, 8: 157, 9: 28, 10: 5, 11: 5, 12: 22, 16: 34, 20: 1, 25: 2, 32: 3, 64: 2}`.
- ell: good `{5: 1, 7: 31, 8: 24, 9: 267, 10: 1099, 11: 1284, 12: 1988, 13: 2696, 14: 5091, 15: 7604, 16: 8033, 17: 8020, 18: 9492, 19: 7135, 20: 7681, 21: 6046, 22: 7229, 23: 6030, 24: 5482, 25: 4913, 26: 2320, 27: 1569, 28: 1398, 29: 385, 30: 435, 31: 556, 32: 178, 33: 81, 34: 178, 35: 83, 36: 2, 37: 57, 38: 17, 39: 8, 40: 36, 41: 4, 42: 7, 43: 3, 45: 6, 50: 1}`; bad `{12: 31, 13: 200, 14: 669, 15: 1398, 16: 2057, 17: 2586, 18: 3105, 19: 2567, 20: 2855, 21: 1870, 22: 2749, 23: 591, 24: 530, 25: 452, 26: 545, 27: 140, 28: 166, 29: 54, 30: 57, 31: 20, 32: 6, 34: 1, 35: 1}`.
- degree_sum: good `{10: 848, 11: 210, 12: 308, 13: 364, 14: 224, 15: 1628, 16: 729, 17: 737, 18: 1249, 19: 1623, 20: 4129, 21: 3949, 22: 6224, 23: 7500, 24: 6786, 25: 6794, 26: 6507, 27: 5063, 28: 5013, 29: 4311, 30: 5404, 31: 3353, 32: 3599, 33: 3450, 34: 3180, 35: 3653, 36: 3917, 37: 2774, 38: 1821, 39: 1268, 40: 607, 41: 33, 42: 145, 43: 13, 45: 56, 50: 1}`; bad `{18: 3, 19: 7, 20: 58, 21: 249, 22: 931, 23: 2504, 24: 2912, 25: 2344, 26: 2091, 27: 1828, 28: 1879, 29: 2428, 30: 4629, 31: 385, 32: 215, 33: 123, 34: 50, 35: 11, 36: 3}`.
- compatible_optG: good `{0: 10973, 1: 64614, 2: 10184, 3: 4720, 4: 2822, 5: 1604, 6: 642, 7: 614, 8: 423, 9: 142, 10: 105, 11: 18, 12: 44, 13: 44, 14: 46, 15: 52, 16: 30, 17: 42, 18: 45, 19: 8, 20: 28, 21: 12, 22: 8, 24: 6, 30: 1, 35: 243}`; bad `{0: 4417, 1: 3503, 2: 3524, 3: 2324, 4: 2123, 5: 2755, 6: 693, 7: 1077, 8: 360, 9: 496, 10: 1024, 11: 90, 12: 56, 13: 46, 14: 145, 15: 8, 16: 7, 20: 2}`.
- optG_count: good `{1: 55918, 2: 7690, 3: 8415, 4: 9059, 5: 2628, 6: 2722, 7: 243, 8: 4696, 9: 1656, 10: 3661, 27: 321, 30: 218, 35: 243}`; bad `{1: 1139, 2: 1319, 3: 594, 4: 2953, 5: 375, 6: 281, 7: 2760, 8: 1310, 9: 1347, 10: 2345, 27: 2682, 30: 2785, 35: 2760}`.

Induced five-set types are exact isomorphism classes: the minimum ten-bit adjacency code over all 120 permutations. Their good/bad histograms are in summary.json; this avoids conflating nonisomorphic degree sequences.

## Minimum positive-rho good witnesses

One deterministic witness is shown per graph having a positive-rho good deletion. The TSV gives actual vertex sets, both cuts, and all boundary counts for every positive-rho deletion, good or bad. H boundary counts are under the selected global optimum; their difference is exactly Delta for that witness.

| ID | Y mask | rho | switch vertices | induced edges | degrees | independent | connected | path | star | H boundary M/C | Y boundary M/C | Delta |
|---:|---:|---:|---|---:|---|---:|---:|---:|---:|---|---|---:|
| 401 | 1795 | 1 | 6 | 0 | 0 | 1 | 1 | 1 | 1 | 1/0 | 0/3 | 1 |
| 1676 | 107 | 1 | 12 | 0 | 0 | 1 | 1 | 1 | 1 | 2/1 | 0/2 | 1 |
| 6132 | 167 | 1 | 13 | 0 | 0 | 1 | 1 | 1 | 1 | 2/1 | 0/3 | 1 |
| 10116 | 229 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1/0 | 0/2 | 1 |
| 8814 | 121 | 1 | 14 | 0 | 0 | 1 | 1 | 1 | 1 | 1/0 | 0/4 | 1 |
| 1292 | 110 | 1 | 9 | 0 | 0 | 1 | 1 | 1 | 1 | 2/1 | 0/2 | 1 |
| 1301 | 143 | 1 | 14 | 0 | 0 | 1 | 1 | 1 | 1 | 2/1 | 0/4 | 1 |
| 1352 | 155 | 1 | 12 | 0 | 0 | 1 | 1 | 1 | 1 | 1/0 | 1/4 | 1 |
| 1355 | 155 | 1 | 11 | 0 | 0 | 1 | 1 | 1 | 1 | 1/0 | 0/5 | 1 |
| 2368 | 398 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1/0 | 0/2 | 1 |
| 900 | 3596 | 1 | 8 | 0 | 0 | 1 | 1 | 1 | 1 | 2/1 | 0/3 | 1 |
| 275 | 1550 | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1/0 | 0/2 | 1 |
| 108 | 62 | 1 | 11 | 0 | 0 | 1 | 1 | 1 | 1 | 1/0 | 0/5 | 1 |
| 82 | 961 | 1 | 10 | 0 | 0 | 1 | 1 | 1 | 1 | 1/0 | 0/4 | 1 |
| 120 | 31 | 1 | 10 | 0 | 0 | 1 | 1 | 1 | 1 | 2/0 | 0/3 | 2 |
| 89 | 31 | 1 | 12 | 0 | 0 | 1 | 1 | 1 | 1 | 2/0 | 0/5 | 2 |
| 398 | 1039 | 1 | 12 | 0 | 0 | 1 | 1 | 1 | 1 | 2/0 | 0/4 | 2 |
| 148 | 31 | 1 | 12 | 0 | 0 | 1 | 1 | 1 | 1 | 3/0 | 0/4 | 3 |
| 78 | 31 | 1 | 14 | 0 | 0 | 1 | 1 | 1 | 1 | 4/1 | 0/5 | 3 |
| 56 | 20487 | 1 | 7 | 0 | 0 | 1 | 1 | 1 | 1 | 1/0 | 0/2 | 1 |
| 15 | 3841 | 1 | 12 | 0 | 0 | 1 | 1 | 1 | 1 | 1/0 | 0/3 | 1 |
| 0 | 16414 | 3 | 5,6,13 | 2 | 1,1,2 | 0 | 1 | 1 | 1 | 1/0 | 0/6 | 1 |
| 2564 | 1574 | 1 | 6 | 0 | 0 | 1 | 1 | 1 | 1 | 2/1 | 0/2 | 1 |
| 2282 | 2465 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 2/1 | 0/2 | 1 |
| 2134 | 2691 | 1 | 2 | 0 | 0 | 1 | 1 | 1 | 1 | 2/1 | 0/2 | 1 |
| 1649 | 433 | 1 | 6 | 0 | 0 | 1 | 1 | 1 | 1 | 2/1 | 0/2 | 1 |
| 614 | 880 | 1 | 10 | 0 | 0 | 1 | 1 | 1 | 1 | 2/1 | 0/3 | 1 |
| 1290 | 47 | 1 | 14 | 0 | 0 | 1 | 1 | 1 | 1 | 2/1 | 0/4 | 1 |

For all chosen nearest nonempty good witnesses, the shape histogram is:

```json
{
  "n=1,m=0,degrees=0,connected=1,bipartite=1": 4049,
  "n=2,m=0,degrees=0,0,connected=0,bipartite=1": 1186,
  "n=2,m=1,degrees=1,1,connected=1,bipartite=1": 1588,
  "n=3,m=0,degrees=0,0,0,connected=0,bipartite=1": 81,
  "n=3,m=1,degrees=0,1,1,connected=0,bipartite=1": 25,
  "n=3,m=2,degrees=1,1,2,connected=1,bipartite=1": 1646,
  "n=4,m=2,degrees=0,1,1,2,connected=0,bipartite=1": 1,
  "n=4,m=3,degrees=1,1,1,3,connected=1,bipartite=1": 946,
  "n=4,m=3,degrees=1,1,2,2,connected=1,bipartite=1": 26,
  "n=4,m=4,degrees=2,2,2,2,connected=1,bipartite=1": 822,
  "n=5,m=4,degrees=1,1,1,1,4,connected=1,bipartite=1": 435,
  "n=5,m=6,degrees=2,2,2,3,3,connected=1,bipartite=1": 168
}
```

H3 is not formulated: this run classifies one deterministic nearest pair per Y, not every tied nearest pair. The exact boundary gain identity alone is not an empirical uniform inequality that controls selection.

## Metadata discrepancies

```json
[
  {
    "id": 19269,
    "field": "critical",
    "saved": "0",
    "exact": 1
  },
  {
    "id": 19082,
    "field": "critical",
    "saved": "0",
    "exact": 1
  }
]
```

## Reproducibility, distance, and checkpointing

Masks use source vertex labels 0 through 14. Global optimal masks fix vertex 0 to color 0. Local core masks use the increasing list of vertices outside Y, fixing the first local bit to 0 in the stored Opt(H) list. Witness h masks may use the reversed orientation to realize the smaller Hamming distance. Both orientations seed an exact multisource BFS on the ten-dimensional cube, giving nearest distances without repeated pairwise comparisons.

For every global optimum, its restricted cost is checked against d(H); Delta_min and the number of compatible global optima are computed independently of the BFS. rho=0 iff Delta_min=0 iff that count is positive is asserted for every Y. The witness minimizing rho need not minimize Delta; both quantities are recorded separately.

Each completed graph has atomic per-graph TSV checkpoints and a completion marker. Rerunning the checker resumes only incomplete graphs. The summary records hashes of the sample and outputs. Final aggregate files are not silently overwritten.

Commands:

```sh
python3 scripts/select_global_cut_landscape_n15.py
g++ -std=c++17 -O3 -o /tmp/analyze_global_cut_landscape_n15 scripts/analyze_global_cut_landscape_n15.cpp
/tmp/analyze_global_cut_landscape_n15 results/global_cut_landscape_n15/sample_input.txt results/global_cut_landscape_n15
python3 scripts/report_global_cut_landscape_n15.py
python3 -m unittest discover -s tests -p test_global_cut_landscape_n15.py -v
```

**Next step:** SCALE_TO_FULL_CORPUS. This is a recommendation only; the present run stops at the frozen sample.
