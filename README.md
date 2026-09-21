# Triangle-Free Bipartization

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22876896.svg)](https://doi.org/10.5281/zenodo.22876896)
[![Latest Release](https://img.shields.io/github/v/release/JinjiLI-0725/triangle-free-bipartization)](https://github.com/JinjiLI-0725/triangle-free-bipartization/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Reproducible computational and structural study of an inductive approach to triangle-free graph bipartization.

**Paper:** [Exchange Certificates for an Inductive Approach to Triangle-Free Graph Bipartization](paper/triangle_free_paper_v1.pdf)  
**Latest release:** [v0.1.2 — Zenodo Archival Release](https://github.com/JinjiLI-0725/triangle-free-bipartization/releases/tag/v0.1.2)  
**Zenodo DOI:** [10.5281/zenodo.22876896](https://doi.org/10.5281/zenodo.22876896)

## Main certified result

For all 3,436 canonical graph classes in the saved (n=15) hard-regime corpus with global (L(G)=11), the recorded five-set (X) admits a 3-for-3 exchange (Y) satisfying

[
|X \cap Y| = 2
]

and

[
d(G)-d(G-Y) \le 5.
]

Among these classes, 762 have (d(G)>5) and require a nontrivial exact exchange search:

- 701 classes with (d(G)=6)
- 61 classes with (d(G)=7)

All 762 pass.

## Scope

This repository provides exact computational certificates and structural analysis for one induction mechanism.

It **does not** claim an exhaustive classification of all triangle-free graphs on 15 vertices, and it **does not** claim to prove the full Erdős triangle-free bipartization conjecture.

## Repository contents

- `paper/` — preprint PDF, LaTeX source, and bibliography
- `scripts/` — deterministic input builder, exact C++ checker, and scope verifier
- `tests/` — regression test for the scope certificate
- `results/hard_regime_L_n15/` — source records, full audit, certificate input, and SHA-256 manifest
- `CITATION.cff` — machine-readable citation metadata
- `.zenodo.json` — Zenodo metadata
- `LICENSE` — MIT license

## Reproducibility

Run the scope verifier:

```bash
python3 scripts/verify_L11_3for3_scope.py
```

Verify the release files:

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

If you use the code, data, or computational certificate, please cite the Zenodo release:

```bibtex
@software{li_2026_triangle_free_bipartization,
  author  = {Jinji Li},
  title   = {Exchange Certificates for an Inductive Approach to Triangle-Free Graph Bipartization},
  year    = {2026},
  version = {0.1.2},
  doi     = {10.5281/zenodo.22876896},
  url     = {https://doi.org/10.5281/zenodo.22876896}
}
```

GitHub can also generate citation information directly from [`CITATION.cff`](CITATION.cff).
