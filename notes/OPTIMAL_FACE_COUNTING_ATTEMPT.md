# Optimal-face counting: attempted low-q selection

## Status

**PROVED:** distinct-fiber counting identities, the exact face-intersection theorem, and the low-defect-pair lower bound below. **UNPROVED:** positivity of the low-q intersection sum under FULL. No full-hypothesis counterexample is produced.

Here I(Y) counts distinct inherited optimal REMAINDER cuts. J(Y) counts extending GLOBAL optima. Their exact relation and the inverse-fiber weights are in `OPTIMAL_FACE_PROJECTION.md`. This difference must be retained when interpreting the older saved data.

FULL means G triangle-free, n=5k, d(G)=k^2+1, and every edge d-critical. It is impossible at k=1, so take k>=2. Let O=|Opt(G)| and C=binom(5k,5).

## 1. The target sum and what double counting really gives

Define

    W_good=sum_(Y:q_Y<=2k-1) I(Y).

For a global optimum f, let R_f(Y) count its monochromatic edges touching Y. Define the family of low-defect global-cut/deletion pairs

    B={(f,Y): f in Opt(G), |Y|=5, R_f(Y)<=2k-1}.

For inherited pairs R_f(Y)=q_Y. Therefore

    W_good=sum_( (f,Y) in B, f|H optimal ) 1/E(Y,f|H).   (1)

Equivalently, using the 32-assignment extension polynomials of the projection note,

    W_good=sum_(Y:q_Y<=2k-1) sum_(h in Opt(H))
        1_{ [t^q_Y]sum_a t^C_Y(h,a) > 0 }.             (2)

The summands are nonnegative integers. Formula (2) is an exact characterization, not a lower bound that forces positivity. Replacing its indicator by the coefficient counts J rather than I; that changes counts and weighted means, but not whether the total is positive.

## 2. A nonempty supply of candidate pairs under FULL — PROVED

For any fixed global optimum, every defect edge touches a uniform five-set with probability 10(5k-3)/(5k(5k-1)). Hence

    average_Y R_f(Y)
      =(k^2+1)10(5k-3)/(5k(5k-1))
      =2k-eta_k,
    eta_k=2(2k-3)(k-1)/(k(5k-1))>0.

If b_f five-sets have R_f(Y)<=2k-1, all the other C-b_f sets contribute at least 2k to the sum of R, and R is nonnegative. Thus

    b_f>=ceil(C eta_k/(2k)),
    |B|>=O ceil(C eta_k/(2k))>0.                       (3)

For k=3 this is at least 143 low-defect deletions for every optimum. This is a proof using FULL's exact d(G), not a corpus observation. It supplies potential pairs, not inherited ones: q_Y can exceed R_f(Y) when the restriction is suboptimal.

## 3. The single missing incidence inequality

Let

    B_bad={(f,Y) in B: f|H is NOT optimal on H}.

Then W_good>0 if and only if

    |B_bad| < |B|.                                     (BLOCKER)

Indeed B\B_bad consists exactly of low-q inherited global-cut/deletion pairs; each contributes a strictly positive inverse-fiber weight in (1). More quantitatively,

    (|B|-|B_bad|)/32 <= W_good <= |B|-|B_bad|.           (4)

This is the precise missing inequality in the double-counting framework. We have proved a positive lower bound for |B| but no upper bound on |B_bad| strictly below it. The face formulation identifies the failure exactly as a positive support-function gap at the projected restriction. Criticality gives coordinatewise coverage of defect edges across global optima; it does not bound how often that failure occurs on B.

In particular, the reindexing does not manufacture positivity: summing over remainder optima, or passing from J to distinct I, cannot create an inherited pair absent from B. The collision identities can bound multiplicities after such pairs exist, not prove they exist in the needed deletion range.

## 4. Other rigorous counts and their limits

If a five-set covers every defect edge of a fixed global optimum, its restricted coloring is proper and therefore optimal. If those defects have a vertex cover C0 of size t<=5, this proves at least binom(n-t,5-t) five-sets with I(Y)>0. When d(G)<=5, selecting one endpoint of each defect supplies such a cover after omitting repetitions.

But under FULL all these cover-based witnesses have d(H)=0 and q_Y=k^2+1>=2k. They establish nonempty projected intersections in the wrong cost range. They do not help (BLOCKER).

If there are at least five isolated vertices, deleting five of them gives q=0 and an inherited optimum. This is a valid easy subcase; no such isolates are forced under FULL.

If sum_Y I(Y)>0, the distinct-projection weighted mean is

    sum_Y I(Y)q_Y / sum_Y I(Y).

A value below 2k suffices, but is stronger than W_good>0. The earlier J-weighted mean is different. Neither averaging convention has a proved sufficient bound under FULL here; a previously observed failure for the J-weighted mean cannot automatically be quoted as a failure for this I-weighted mean.

## 5. Saved-data diagnostic: scope before results

Script `scripts/diagnose_optimal_face_projection.py` uses saved outputs only. It makes no MaxCut calls and generates no graphs.

- For all 19,270 saved graphs, positivity I(Y)>0 is read from the already-computed Delta_min=0 marginal histograms. Positivity is unaffected by the change from J to I. This provides the number of preserved five-sets and of low-q preserved five-sets for every graph.
- Exact DISTINCT I(Y) is recomputed by set intersection only for the existing 40-graph landscape sample, over its 120,120 already-saved five-sets. Both complete global optimum lists and complete remainder optimum lists exist there. Restrictions are normalized modulo global reversal, then deduplicated.
- The old `compatible_optG` counts are independently recovered as J(Y), and the new distinct counts satisfy I<=J<=32I. Inverse-fiber counting (1) is checked exactly with rational arithmetic.
- Counts and exact conditional means of I by q, and signs of within-graph covariance, describe this saved sample only. No fitted model or inference to all triangle-free graphs is made.

The full-corpus saved marginal counts do not contain projection fibers, so they cannot recover the full-corpus DISTRIBUTION of distinct I. That distribution is reported only for the 40-graph sample where the required cuts were already saved. No new full-corpus optimization audit is initiated to fill that distinction.

Outputs are `results/optimal_face_projection/full_graph_counts.tsv`, `sample_fivesets.tsv`, and `summary.json`.


## 6. Completed exact diagnostic

**EXACT FINITE EVIDENCE, not a general theorem.** All 19,270 saved graphs have positive low-q intersection counts. Across the saved corpus there are 43,974,928 five-sets with I(Y)>0, including 43,510,199 with q<=5. Every saved graph has at least 844 preserved five-sets, and at least 218 low-q preserved five-sets. The minimum 218 is attained by graph 19082. Per-graph counts are saved in `full_graph_counts.tsv`; none of these graphs is asserted to satisfy the full counterexample hypotheses.

For the existing 40-graph sample, all 120,120 saved five-sets were reindexed exactly. Both counts below are available; they must not be conflated:

| Distinct I(Y) | All preserved five-sets | Low-q preserved five-sets |
|---:|---:|---:|
| 1 | 84235 | 71933 |
| 2 | 12566 | 8652 |
| 3 | 3873 | 3060 |
| 4 | 2027 | 1170 |
| 5 | 996 | 795 |
| 6 | 356 | 283 |
| 7 | 179 | 146 |
| 8 | 92 | 54 |
| 9 | 68 | 68 |
| 10 | 29 | 29 |
| 11 | 12 | 12 |
| 12 | 18 | 18 |
| 13 | 34 | 34 |
| 15 | 243 | 243 |
| 16 | 2 | 0 |

The first observed multiplicity collision is graph 401, Y_mask=87, q=3: I=1 but J=2. Two distinct global optima extend the same optimal remainder coloring.

Exact sample means by q, including I=0 sets, are:

| q | Five-sets | Sets with I>0 | Mean I |
|---:|---:|---:|---:|
| 0 | 31362 | 31362 | 5234/5227 |
| 1 | 13742 | 12219 | 6302/6871 |
| 2 | 8830 | 7371 | 8707/8830 |
| 3 | 4177 | 3933 | 6586/4177 |
| 4 | 17063 | 13600 | 23789/17063 |
| 5 | 22296 | 18012 | 32471/22296 |
| 6 | 15144 | 11544 | 19237/15144 |
| 7 | 6280 | 5639 | 1929/1570 |
| 8 | 896 | 720 | 181/224 |
| 9 | 330 | 330 | 1 |

Within individual sample graphs, Cov(q,I) is negative for 32 graphs and zero for eight; none is positive. This is an exact descriptive association, not a selection theorem. Pooled means are not monotone in q, and mixing different graphs changes the comparison. No model is fitted.

### Distinct weighting does not rescue the generic conditioned-mean bound

The I-weighted mean of q is below six in 39 sample graphs but above six in B3 (saved graph 19269). Its exact value is 3141/508>6. In particular, the NEW distinct weighting also does not justify a generic mean bound from triangle-freeness and criticality alone.

For B3, sum_Y I(Y)=7620 and sum_Y q(Y)I(Y)=47115. B3 nevertheless has 243 good preserved five-sets, each with I=15. Its d(G)=9, not the FULL value 10. The failure of this stronger mean bound is therefore not a counterexample to the target, nor to a FULL-specific bound. These new distinct-count totals are exact saved-cut computations, separate from earlier J-weighted totals.

### Criticality does not force a fixed good deletion to intersect

The first saved critical fixed-Y failure in the sample is graph 8814, graph6 `N?BDCaGWYdHWLHJQBq?`, Y_mask=121 (vertices 0,3,4,5,6). It has d(G)=7, q=5, and I=0. Thus its projected global optimal face misses the remainder optimum face despite the deletion being good. The saved complete cut lists permit exact verification of triangle-freeness, an optimum defect witness for every edge, and absence of an inherited restriction.

This is a FIXED-Y obstruction only. The graph has other good inherited deletions, and d(G)=7 differs from the full counterexample value 10. It is not a counterexample to the existential target. It shows why coordinatewise criticality of the optimal face cannot be promoted to intersection for every good Y.

## 7. Verdict and reproducibility

The equivalence theorem and inverse-fiber double counts are proved. The low-q intersection sum is positive in the saved data but remains unproved under FULL. The single missing inequality is (BLOCKER), |B_bad|<|B|. No full-hypothesis counterexample is established.

The original diagnostic completed every saved-cut comparison and wrote both result tables. Its final aggregation had a redundant repeated minimum calculation; that operation was interrupted after table completion. The routine was fixed, and `scripts/report_optimal_face_projection.py` produced the final summary by a linear pass over the completed tables. No cut computation was repeated and no prior results were overwritten.

Verification: `python3 -m unittest discover -s tests -p 'test_optimal_face_projection.py' -v` — **4 tests passed**. The tests distinguish I from J on a disconnected example, check the sharp fiber bound 32, verify a disjoint projected-face example, and directly verify triangle-freeness, defect-edge coverage, and noninheritance for the saved critical witness 8814 using its saved complete optimum lists. The diagnostic itself checked inverse-fiber identities and agreement with prior positivity counts for all 120,120 sample five-sets.
