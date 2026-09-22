# Novelty audit for the triangle-free bipartization project (v2)

Date: 2026-09-22

## Executive conclusion

The project contains several correct and useful structural identities and reproducible computational certificates, but the current literature check does **not** support presenting the work as a solution of the Erdős triangle-free bipartization conjecture or as a new theory of frustration-critical signed graphs.

The most defensible publication angle is a **computational/structural research note on a five-vertex induction strategy**: exact flip identities, exact reduced-state certificates, explicit failure modes for stronger fixed-set lemmas, and a reproducible exchange audit. The v1 framing of `L(G)=11` as part of the genuinely hard `n=15` regime must be corrected: because of the floor in the selection inequality, the empty flip already proves Candidate A whenever `L(G) <= 4k-1`, so at `k=3` the automatic range is `L(G) <= 11`.

A stronger journal-style novelty claim would require at least one nontrivial general theorem beyond the elementary identities and finite-corpus certificates.

## Claim-by-claim audit

### 1. Erdős triangle-free bipartization conjecture

**Status:** known problem; not new.

Balogh, Clemen and Lidický describe the conjecture as a well-known conjecture of Erdős and prove the sharp `n^2/25` bound in two density ranges together with the global `n^2/23.5` bound. Ferudun (2026) gives a computer-assisted proof of the sharp value for multiples of five up to `N=200`.

**Implication for this project:** finite checks at `n=10` or `n=15` are validation/structure-finding results, not new extremal evaluations.

### 2. Edge bipartization = MaxCut defect = odd-cycle edge transversal

**Status:** standard.

The identity `d(G) = |E(G)| - MaxCut(G)` and the equivalent formulation as a minimum edge set meeting every odd cycle are classical MaxCut / odd-cycle-cover facts.

**Novelty claim:** none.

### 3. Frustration-critical / edge-critical language

**Status:** established literature.

Cappello and Steffen study `k`-critical signed graphs, where deleting any edge lowers the frustration index. Their 2022 paper develops structural results and explicitly uses the same criticality concept in the signed-graph setting.

**Implication:** statements such as "every edge deletion lowers the frustration index" must be cited as part of the existing frustration-critical framework, not presented as a new concept.

### 4. Every critical edge lies in a minimum transversal

**Status:** elementary consequence of the definitions; likely standard.

For an edge `e`, `d(G-e)=d(G)-1` iff there is a minimum odd-cycle edge transversal of `G` containing `e`.

This is useful in the project but is too elementary to support a novelty claim by itself.

### 5. Private odd-cycle witness for an edge of a minimum transversal

**Status:** elementary minimal-hitting-set fact; not a plausible novelty claim.

If `T` is an inclusion-minimal odd-cycle edge transversal and `e in T`, there is an odd cycle `C_e` with `C_e ∩ T = {e}`. In a triangle-free graph, `|C_e| >= 5`.

**Novelty claim:** none; use as a lemma with proof for completeness.

### 6. Weakly bipartite signed graphs / odd-K5 obstruction

**Status:** known theorem of Guenin; short proof by Schrijver; related packing result by Geelen--Guenin.

Guenin's theorem characterizes weakly bipartite signed graphs by exclusion of an odd-`K5` minor. This is exactly the literature framework for integrality of the odd-circuit-cover polyhedron.

**Implication:** any LP-integrality / odd-`K5` discussion in the paper must be explicitly presented as an application of known signed-graph theory, not as a new theorem unless the project proves a new triangle-free consequence beyond Guenin's characterization.

### 7. Coordinated-flip identity

**Status:** algebraically elementary; exact five-set formulation appears project-specific, but novelty is not established by this search.

The identity `g_c(a,S) = sum_{v in S}(w_a(v)-sigma_c(v)) + 2 e(H[S]) - 4 m_c(S)` is a direct edge-accounting formula. The project-specific value is how it is embedded into a five-vertex induction and averaged over optimal assignments.

**Defensible claim:** "we formulate and use" this identity in the induction framework.

**Avoid:** claiming the raw identity itself is a new theorem without a broader literature search.

### 8. Bichromatic edge/star/biclique interaction identities

**Status:** direct corollaries of the coordinated-flip identity.

For an induced complete bipartite support `S=A∪B` whose internal edges are bichromatic, `g_c(a,S) = sum_{v in S} x_a(v) + 2|A||B|`, with `x_a(v)=w_a(v)-sigma_c(v)`.

The edge and star cases follow immediately.

**Defensible claim:** useful exact corollaries / bookkeeping lemmas.

**Novelty claim:** weak on their own.

### 9. Empty-flip threshold

**Status:** elementary correction; not new.

From `q(Y) <= floor(ell(Y)/2 - Phi_Y)` and `Phi_Y >= 0`, Candidate A follows whenever `ell(Y) <= 4k-1`.

Thus at `k=3` the automatic threshold is `L(G) <= 11`, not `L(G) <= 10`.

**Publication consequence:** v1 must be corrected. The global-`L=11` exchange experiment is still a valid computational observation, but it is not needed to establish Candidate A in that regime.

### 10. Balanced-extension and mixed `t=2` exact certificates

**Status:** original computational artifacts of this project, subject to reproducibility and scope.

These are potentially publishable as exact finite certificates for explicitly defined reduced models. Their value is methodological/structural, not that they settle new finite values of the Erdős extremal function.

### 11. `3-for-3` exchange audit on the saved global-`L=11` corpus

**Status:** original computational experiment, but mathematically weaker after the threshold correction.

The exact audit remains useful evidence that changing the five-set repairs obstructions to stronger fixed-set statements. However, because `L=11` is automatic for Candidate A, this should be framed as **exchange-structure evidence**, not as a necessary certificate for the induction bound.

### 12. Fixed-set obstruction / falsification results

**Status:** useful negative computational/structural information.

The project explicitly finds realizable configurations falsifying stronger fixed-set gain statements while the existential five-set target still holds. This is a coherent methodological contribution: it identifies which induction strengthenings are false.

## Recommended publication claims

The revised note can safely claim the following:

1. A five-vertex induction framework for the Erdős triangle-free bipartization conjecture.
2. An exact coordinated-flip selection inequality.
3. Exact edge/star/biclique corollaries inside that framework.
4. Exact reduced-state computational certificates for the balanced and mixed `t=2` models.
5. An explicit correction of the automatic threshold to `L(G) <= 4k-1`.
6. Reproducible computational evidence showing that fixed-set strengthenings can fail while a small exchange of the five-set succeeds.
7. A carefully scoped `3-for-3` exchange audit, reframed as structural evidence rather than a needed proof at `L=11`.
8. A connection to established frustration-critical and weakly-bipartite signed-graph theory, with proper attribution.

## Claims to avoid

Do not claim:

- the Erdős conjecture is solved;
- Candidate A is proved in general;
- the `n=15` finite extremal value is new;
- frustration-criticality is a new concept;
- the private odd-cycle lemma is novel;
- Guenin's odd-`K5` obstruction is new;
- the `L=11` corpus is a genuinely hard Candidate-A regime;
- the saved corpus is all triangle-free graphs on 15 vertices unless a separate exhaustive-generation proof is supplied.

## Publication recommendation

### arXiv / Zenodo

**Yes, after correction.** A v2 research note is appropriate if it is framed as a reproducible computational/structural investigation rather than a claimed resolution.

### Journal submission

**Not yet recommended as a strong theorem paper.** Before journal submission, add at least one nontrivial general theorem whose conclusion is not a direct algebraic identity, a standard criticality fact, or a finite-corpus statement.

## Key literature checked

- J. Balogh, F. C. Clemen, B. Lidický, *Max Cuts in Triangle-Free Graphs* (2021).
- A. Ferudun, *The Erdős n^2/25 max-cut conjecture for small multiples of five...* (2026).
- C. Cappello, E. Steffen, *Frustration-critical signed graphs*, Discrete Applied Mathematics 322 (2022), 183--193.
- A. Schrijver, *A short proof of Guenin's characterization of weakly bipartite graphs*.
- J. F. Geelen, B. Guenin, *Packing Odd Circuits in Eulerian Graphs* (2002), including the weakly-bipartite / odd-`K5` framework.
