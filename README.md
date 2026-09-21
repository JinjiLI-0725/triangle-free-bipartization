# Triangle-Free Bipartization

Reproducible computational and structural study of an inductive approach to triangle-free graph bipartization.

## Main certified result

For all 3,436 canonical graph classes in the saved n=15 hard-regime corpus with global L(G)=11, the recorded five-set X admits a 3-for-3 exchange Y satisfying |X ∩ Y| = 2 and d(G) - d(G-Y) <= 5.

Among these classes, 762 have d(G) > 5 and require a nontrivial exact exchange search:

- 701 classes with d(G)=6
- 61 classes with d(G)=7

All 762 pass.

## Scope

This repository provides exact computational certificates and structural analysis for one induction mechanism.

It does **not** claim to solve the full Erdős triangle-free bipartization conjecture.

## Paper

See `paper/triangle_free_paper_v1.pdf`.

## Reproducibility

The repository includes the exact C++ checker, deterministic input builder, independent scope verifier, regression test, source corpus records, full audit output, and SHA-256 manifest.

Scope verification:
`python3 scripts/verify_L11_3for3_scope.py`

Checksum verification:
`sha256sum -c results/hard_regime_L_n15/L11_3for3_SHA256SUMS.txt`
