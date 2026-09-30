# Triangle-Free Bipartization

[![Latest Release](https://img.shields.io/github/v/release/JinjiLI-0725/triangle-free-bipartization)](https://github.com/JinjiLI-0725/triangle-free-bipartization/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Reproducible computational and structural study of five-vertex induction and global cut stability in triangle-free graph bipartization.

**Current v3 paper:** [PDF](paper/triangle_free_paper_v3.pdf) · [LaTeX source](paper/triangle_free_paper_v3.tex)  
**v3 reproducibility code/data:** `scripts/`, `tests/`, and compact result tables under `results/`  
**Previous v0.2.0 Zenodo record:** [10.5281/zenodo.22894110](https://doi.org/10.5281/zenodo.22894110)  
**Next release:** v0.3.0

## Main v3 phenomenon

For a graph \(G\), write

\[
d(G)=|E(G)|-\operatorname{MaxCut}(G).
\]

For a five-set \(Y\) and a maximum cut \(f\) of \(G\), let \(R_f(Y)\) be the number of monochromatic edges under \(f\) incident with \(Y\), and let \(\Delta_f(Y)\) be the additional improvement obtained by reoptimizing the cut on \(G-Y\). Then exactly

\[
d(G)-d(G-Y)=R_f(Y)+\Delta_f(Y).
\]

The v3 exact saved-corpus audit finds that every one of the **19,270 saved canonical \(n=15\) graphs** has a five-set \(Y\) satisfying

\[
d(G)-d(G-Y)\le 5
\]

and, for some maximum cut \(f\) of \(G\),

\[
\Delta_f(Y)=0.
\]

Equivalently, some global maximum cut of \(G\) restricts to a maximum cut of \(G-Y\).

The same property holds for all:

- 5,337 saved graphs with \(L(G)\ge 12\),
- 2,103 saved graphs with \(d(G)>5\),
- 7 exactly identified edge-critical saved graphs.

No failure was found in the saved corpus.

## Important scope note

This is an exact statement about the saved corpus used by the project. The repository does **not** claim:

- a proof of the Erdős triangle-free bipartization conjecture;
- a proof of the five-set induction target for all graphs;
- that the saved 19,270 graphs are the complete universe of triangle-free graphs on 15 vertices;
- that the finite \(n=15\) extremal value is new.

The full Erdős conjecture remains open.

## Corrected automatic threshold

For a five-set \(Y\), define

\[
\ell(Y)=2d(G[Y])+e(Y,G-Y).
\]

The coordinated-flip selection inequality implies

\[
d(G)-d(G-Y)\le
\left\lfloor \frac{\ell(Y)}2-\Phi_Y\right\rfloor.
\]

Since \(\Phi_Y\ge0\), the five-set induction target is automatic whenever

\[
\ell(Y)\le 4k-1.
\]

Thus at \(k=3\), the automatic range extends through \(L(G)\le 11\). This corrects the threshold used in the original v1 draft.

## Global cut stability viewpoints

### Optimal-face projection

Let \(\operatorname{Opt}(G)\) be the set of maximum-cut colorings of \(G\), modulo global reversal, and define

\[
\operatorname{Res}_Y(G)=\{f|_{G-Y}: f\in\operatorname{Opt}(G)\}.
\]

Optimal restriction for \(Y\) is exactly

\[
\operatorname{Res}_Y(G)\cap\operatorname{Opt}(G-Y)\neq\varnothing.
\]

### Extension frontier

For \(H=G-Y\), define \(F_Y(j)\) as the minimum extension cost over \(Y\) among colorings of \(H\) having \(d(H)+j\) monochromatic edges. Then

\[
d(G)-d(G-Y)=\min_{j\ge0}\bigl(j+F_Y(j)\bigr).
\]

Optimal restriction holds exactly when this minimum is attained at \(j=0\).

The saved data falsifies stronger frontier-shape guesses such as monotonicity, one-step Lipschitz behavior, and discrete convexity. The surviving phenomenon is the weaker global statement that, for some useful five-set \(Y\), the combined cost \(j+F_Y(j)\) is minimized at \(j=0\).

## Reproducibility

The public v3 package includes exact global-cut landscape code, the full saved-corpus H0 audit code, compact witness tables and summaries, sample checkpoint data, extension-frontier diagnostics, optimal-face projection diagnostics, and portable release tests.

The lightweight public test suite intentionally excludes the 5.8 GB raw five-set feature table and the 531 MB full-corpus checkpoint directory.

Portable v3 tests:

    PYTHONPATH=.:src python3 -m pytest -q \
      tests/test_optimal_restriction_identities.py \
      tests/test_optimal_face_projection.py \
      tests/test_extension_frontier.py \
      tests/test_inherited_optimum_count.py \
      tests/test_global_cut_landscape_n15.py \
      tests/test_global_cut_h0_full.py

Release validation result: `21 passed, 3 skipped`.

## Citation

Version 0.3.0 is the current corrected research-note release. The version-specific Zenodo DOI will be added after Zenodo archives the GitHub v0.3.0 release.