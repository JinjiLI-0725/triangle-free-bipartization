# Triangle-Free Bipartization

[![Latest Release](https://img.shields.io/github/v/release/JinjiLI-0725/triangle-free-bipartization)](https://github.com/JinjiLI-0725/triangle-free-bipartization/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Reproducible computational and structural study of a five-vertex induction approach to triangle-free graph bipartization.

**Corrected v2 paper:** [PDF](paper/triangle_free_paper_v2.pdf) · [LaTeX source](paper/triangle_free_paper_v2.tex)  
**Novelty audit:** [paper/NOVELTY_AUDIT_V2.md](paper/NOVELTY_AUDIT_V2.md)  
**Archived v0.1.2 Zenodo record:** [10.5281/zenodo.22876896](https://doi.org/10.5281/zenodo.22876896)  
**Next release:** v0.2.0 (corrected paper and metadata)

## Important correction to v1

For a five-set (X), define

[
ell(X)=2d(G[X])+e(X,G-X).
]

The coordinated-flip selection inequality gives

[
d(G)-d(G-X)le
leftlfloor rac{ell(X)}2-Phi_Xightfloor.
]

Since (Phi_Xge0), the five-set induction target is automatic whenever

[
ell(X)le 4k-1.
]

Thus at (k=3), the automatic range is (L(G)le11), not (L(G)le10). The saved global-(L=11) 3-for-3 audit remains a valid structural computation, but it is **not needed** to establish Candidate A in that regime.

## What the project currently contributes

- a five-vertex induction framework for the Erdős triangle-free bipartization conjecture;
- an exact coordinated-flip identity and selection inequality;
- exact edge/star/biclique interaction corollaries;
- exact balanced-extension and mixed-(t=2) reduced-state certificates;
- explicit computational diagnostics showing that stronger fixed-set statements can fail while changing the five-set repairs the obstruction;
- a reproducible 3-for-3 exchange audit on the saved global-(L=11) corpus;
- a literature audit connecting the project to established frustration-critical and weakly-bipartite signed-graph theory.

The full Erdős conjecture remains open.

## Saved global-L=11 exchange audit

The saved corpus contains 3,436 canonical records with global (L(G)=11). Relative to the distinguished recorded five-set, each admits a 3-for-3 exchange (Y) satisfying

[
|Xcap Y|=2,
qquad
d(G)-d(G-Y)le5.
]

Among these records, 762 have (d(G)>5) and require a nontrivial search; all 762 pass.

After the threshold correction, this result should be interpreted as **exchange-structure evidence**, not as a necessary proof certificate for Candidate A.

## Scope

This repository does **not** claim:

- a proof of the Erdős triangle-free bipartization conjecture;
- a new extremal evaluation at (n=10) or (n=15);
- that the saved (n=15) corpus is the complete universe of triangle-free graphs on 15 vertices;
- that frustration-criticality or the odd-(K_5) weakly-bipartite characterization is new.

See [paper/NOVELTY_AUDIT_V2.md](paper/NOVELTY_AUDIT_V2.md) for the claim-by-claim literature audit.

## Reproducibility

Run the scope verifier:

```bash
python3 scripts/verify_L11_3for3_scope.py
```

Verify the archived release files:

```bash
sha256sum -c results/hard_regime_L_n15/L11_3for3_SHA256SUMS.txt
```

The certified scope check reports:

```text
missing: [] count = 0
extra: [] count = 0
graph6 mismatches: [] count = 0
audit ID set matches: True
audit failures: []
SCOPE_CERTIFICATE=PASS
```

## Citation

The corrected release will be version **0.2.0**. The DOI above refers to the archived v0.1.2 Zenodo record; the v0.2.0 DOI will be added after Zenodo archives the corrected release.
