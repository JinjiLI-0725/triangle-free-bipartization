# Extension frontier: slopes, exact counterexamples, and saved-witness diagnostic

The definitions and proof of q(Y)=min_j(j+F_Y(j)) are in `EXTENSION_FRONTIER_IDENTITY.md`. Missing layers have value +infinity. Statements about adjacent slopes below explicitly require the two layers to be attainable; ordinary discrete convexity also requires an interval domain.

## 1. Distinguish three properties

1. **Anchored inequality:** F(j)>=F(0)-j for every attainable j. This is exactly H0, by the identity; it is not a conjectured additional regularity property of H0 witnesses.
2. **Adjacent lower 1-Lipschitz inequality:** F(j+1)>=F(j)-1 on consecutive attainable layers. This implies that j+F(j) is nondecreasing on an interval of attainable layers, and then implies H0. With holes, adjacent checks alone need not compare every attainable layer to zero.
3. **Discrete convexity:** F(j+2)-F(j+1)>=F(j+1)-F(j) on an interval domain. This does not alone imply H0: the first slope might be less than -1.

Properties 2 and 3 are false in general, including at triangle-free H0 witnesses. Property 1 cannot fail at an H0 witness. A minimum of F at zero is sufficient but not necessary; what matters is a minimum of j+F(j) at zero, with ties allowed.

## 2. Exact mechanism for a one-level saving greater than one

Fix a coloring h0 of H with mu_H(h0)=d(H) and ext(Y,h0)=F(0). Every coloring in layer j is h0 with some S subset V(H) reversed. Define

    D_h0(S)=# crossing H edges across S - # monochromatic H edges across S.

Then mu_H(h0 reversed on S)=d(H)+D_h0(S). For a fixed assignment a on Y, put

    B_a(S)=sum_(v in S, y_i adjacent v) a_i (h0)_v,
    p(a)=C_Y(h0,a)-F(0)>=0.

Only boundary edges incident with S change their extension cost, giving EXACTLY

    C_Y(h0 reversed on S,a)=C_Y(h0,a)-B_a(S),
    F(j)-F(0)=min_(S: D_h0(S)=j, a) [p(a)-B_a(S)].    (1)

This is an identity over all remainder colorings, not a restricted flip certificate. In particular,

    F(1)<F(0)-1

holds exactly when there is a unit-slack remainder change D_h0(S)=1 and an assignment a for which B_a(S)>=p(a)+2. Such a change loses one unit inside H but saves at least two net units in the optimized extension. It need not resemble a one-vertex change.

For each fixed a,S, write b=e(S,Y). Then B_a(S) is an integer in {-b,-b+2,...,b}; it counts same-colored boundary edges minus differently colored boundary edges before the change. The cost change is exactly -B_a(S). No internal Y edge changes in this comparison. In field notation from the identity note,

    b_i(h0 reversed on S)=b_i(h0)-2 sum_(v in S intersect N_H(y_i)) (h0)_v.

Together with the 32 assignments, this describes every possible cost change. Taking minima over assignments can change the minimizer, so neither a fixed-assignment parity nor a unit-step slope for the optimized costs follows automatically.

For any two remainder colorings h,h' differing on S,

    |ext(Y,h')-ext(Y,h)|<=e(S,Y).                       (2)

This follows by applying the fixed-assignment bound in both directions and taking minima. One can replace the right side by min(e(S,Y),e(H\S,Y)), because reversing all of h' leaves ext unchanged. The bound concerns changed boundary edges, not the difference of the remainder costs. A unit difference in remainder cost does not bound that boundary size.

There is a general range bound, rather than a unit slope bound: if b0=d(G[Y]) and z=e(Y,H), every finite frontier value lies in [b0,b0+floor(z/2)]. The lower endpoint follows from internal Y edges; the upper endpoint follows by averaging an optimal Y coloring and its reversal, for each fixed h. Thus any two finite frontier values differ by at most floor(z/2), irrespective of their layer separation. This does not give a bound by one.

Triangle-freeness ensures N_Y(v) is independent in G[Y], and N_H(y_i) is independent in H; adjacent core vertices cannot share a Y-neighbor. These statements hold in the counterexamples below and do not stop (1) from being at most -2. Five deleted vertices do not mean five boundary edges.

## 3. Symbolic counterexample to the first slope

Take three internally disjoint u-v paths of lengths 2,3,3. Label their edges

    01,12; 03,34,42; 05,56,62,

where u=0,v=2. Add isolated vertices 7,8,9, and let

    Y={3,4,5,6,7}, H={0,1,2,8,9}.

All cycles have length five or six, so the graph is triangle-free on ten vertices. The remainder is a two-edge path and two isolates, with d(H)=0. If its coloring has j monochromatic edges, u and v have equal colors exactly when j is even. Each external length-three path has minimum cost one for equal endpoint colors and zero for opposite colors. The paths' internal vertices can be optimized independently. Hence exactly

    F=(2,0,2), G(j)=j+F(j)=(2,1,4).

Thus d(G)=1, q=1, F(1)=0<F(0)-1=1, and Y is not inherited. This is a symbolic calculation, not graph-search evidence. It does NOT satisfy FULL: at k=2 the full counterexample value would be d=5.

## 4. H0 does not imply adjacent Lipschitz or convexity

Take three internally disjoint u-v paths all of length three, with edges

    01,12,23; 04,45,53; 06,67,73.

Add isolates 8,9, and take

    Y={4,5,6,7,8}, H={0,1,2,3,9}.

The graph is bipartite and therefore triangle-free, with d(G)=d(H)=0. Along the three-edge core path, endpoints differ exactly when j is even. Each of the two external three-edge paths costs zero for differing endpoints and one for equal endpoints. Thus

    F=(0,2,0,2), G=(0,3,2,5).

Here H0 holds and q=0, but F(2)-F(1)=-2. Also the first two slopes are 2,-2, violating convexity. Even G need not be nondecreasing: it drops from 3 to 2 while never dropping below its initial value zero. This disproves adjacent Lipschitz and convexity for generic H0 witnesses, not the FULL selection statement. The example is not d-critical.

Convexity can fail even in a d-critical triangle-free graph with an inherited Y. Use C9 plus one isolate (vertex 9), with cycle order 0,...,8 and Y={4,5,6,7,8}. The remainder is a three-edge path and an isolate; the deleted segment is a six-edge path between its endpoints. The same endpoint-parity argument gives

    F=(1,0,1,0), G=(1,1,3,3).

Every C9 edge is d-critical, d(G)=1, H0 holds, and convexity fails. Again d(G) is not the FULL value 5. This example also shows that F need not attain its own minimum at zero in an inherited witness.

## 5. A rigorous sufficient condition for adjacent slope control

The following **layer-repair condition** is sufficient. For every coloring h in a nonempty layer j+1, suppose there is a coloring h' in layer j differing on a set S with e(S,Y)<=1. Then choose h attaining F(j+1) and apply (2):

    F(j)<=ext(Y,h')<=ext(Y,h)+1=F(j+1)+1.

Thus the adjacent lower 1-Lipschitz inequality holds. In fact it suffices that this repair exists for at least one extension-minimizing h in each layer j+1. This weaker version is still only a sufficient structural condition: other colorings could prove the slope bound without such a small-boundary repair.

For a concrete structural class, suppose H is a matching with isolates, and each matching edge has an endpoint with at most one Y-neighbor. Every coloring of cost j+1 has a monochromatic matching edge; reversing that endpoint removes exactly one remainder defect and touches at most one boundary edge. All layers are attainable, so the frontier satisfies the adjacent bound and H0. This is a conditional theorem, not a claimed structural description of minimal counterexamples.

There is no canonical ordering of all possible structural hypotheses in which a unique 'weakest' condition has been identified. The exact anchored condition is already equivalent to inheritance. No non-tautological weakest structural hypothesis, or theorem forcing the repair condition for some Y under FULL, has been established.

## 6. Diagnostic scope and exact implementation

Input is ONLY `results/global_cut_landscape_n15_full/h0_witnesses.tsv`: one previously saved witness Y per graph, not all possible H0 sets. Script `scripts/analyze_extension_frontiers.cpp` decodes each saved graph6, checks triangle-freeness, and computes the complete frontier for that fixed Y. It does not select a new Y or generate any graph.

For every cut of G modulo reversal (16384 cuts), compute its global cost c and restricted cost c_H. The entry for j=c_H-d(H) receives the candidate cost c-c_H. Minimizing these candidates is exactly the definition of F. A bitmask recurrence computes both costs without repeated MaxCut calls. The script verifies the saved d(G), d(H), q, and inherited cut, checks F(0)=q<=5, and checks j+F(j)>=F(0) at every attainable layer. Every finite entry also records an attaining global coloring mask. Missing layers are output as NA.

The diagnostic is exact finite evidence about these saved witnesses only. In particular, verifying the anchored inequality at an H0 witness confirms the identity; it is not new evidence for a stronger shape law.


## 7. Completed exact saved-witness results

**COMPUTATIONALLY VERIFIED:** all 19,270 input records were processed, using exactly one previously saved H0 witness per graph. All saved d(G), d(H), inherited-cut checks, frontier identities, and anchored inequalities passed. This is the saved corpus, not all triangle-free graphs on 15 vertices.

| Property | Passing saved witnesses / 19,270 |
|---|---:|
| j+F(j) minimized at j=0 (H0) | 19,270 |
| Attainable layers form an interval | 2,711 |
| Adjacent lower 1-Lipschitz, testing only pairs of finite consecutive layers | 7,745 |
| Convexity inequalities on finite consecutive triples only | 1,257 |
| Convexity with an interval domain | 37 |
| F itself minimized at zero | 2,405 |
| F nondecreasing across all attainable layers | 331 |
| j+F(j) nondecreasing across all attainable layers | 6,589 |

The distinction between finite adjacent checks and an interval domain is essential. In particular the 7,745 passing adjacent checks are not a proof of the anchored inequality across holes. That anchored inequality was checked separately and holds for all witnesses. A flat-then-increasing shape is not universal either, since even nondecreasing F fails.

The first slope and convexity failure is saved graph 0, Y_mask=31, d(G)=d(H)=1, q=0, graph6 `N???????????_^^_~~_`. Its entire frontier is

    0,4,0,4,0,4,0,4,0,4,0,4,0,NA,0.

The step from j=1 to j=2 drops by four. Its combined cost drops from five to two but never below zero. Thus this is a genuine saved H0 witness refuting both stronger shape laws, not an H0 failure.

The first saved witness where F itself is not minimized at zero is graph 31, Y_mask=31, graph6 `N?????????W?N~N~^~?`, d(G)=2, d(H)=0, q=2. Its frontier is

    2,NA,0,2,NA,0,2,3,0,2,3,0,2,3,0,2,NA,0,2,NA,0.

These observations concern the recorded Y, not all H0 witnesses of each graph. They do not rule out selecting a different Y with a stronger shape, and no new Y selection was attempted. The only tested combined-cost property surviving universally here is its minimum at zero, which is exactly H0, not a newly discovered structural theorem.

Artifacts:

- `results/extension_frontier_diagnostic/frontiers.tsv`: raw exact frontier values and attaining masks; its monotonicity flags check consecutive finite indices.
- `results/extension_frontier_diagnostic/frontiers_validated.tsv`: authoritative shape table, with monotonicity evaluated across ALL attainable layers and interval-domain convexity recorded separately.
- `results/extension_frontier_diagnostic/summary.json`: exact counts, first failures, scope, and source SHA-256.
- `scripts/analyze_extension_frontiers.cpp` and `scripts/report_extension_frontiers.py`: reproducible computation and summary; both refuse to overwrite their result files.

Reproduction (choose fresh output paths/directories for a rerun): compile with `g++ -O3 -std=c++17 scripts/analyze_extension_frontiers.cpp -o /tmp/analyze_extension_frontiers`; invoke it with the saved `h0_witnesses.tsv` and a new output TSV path. The reporting script expects the documented diagnostic directory. No graph generation or corpus-wide five-set selection is involved.

## Verification

`python3 -m unittest discover -s tests -p 'test_extension_frontier.py' -v`: **4 tests passed**. Tests verify the symbolic theta examples, the critical C9 example, and absent layers. Independent direct edge accounting reproduces every frontier entry for saved graphs 0, 31, and 19269, and verifies their recorded attaining masks. A file-handle ResourceWarning in the test reader was subsequently fixed by using a context manager; the mathematical checks were unchanged.

This separates symbolic proofs and counterexamples (Sections 1--5) from exact finite diagnostic evidence (Sections 6--7). No FULL-specific existential theorem has been proved.
