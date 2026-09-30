# Extension frontier: existential proof attempt and exact stopping point

## What is proved

For every five-set Y in any finite graph,

    q(Y)=min_j(j+F_Y(j)),
    I(Y)>0 iff q(Y)=F_Y(0).

An inherited good Y is therefore exactly a Y with

    F_Y(0)<=2k-1 and F_Y(j)>=F_Y(0)-j for all j.

These are exact equivalences proved in `EXTENSION_FRONTIER_IDENTITY.md`. They do not themselves establish existence of such a Y.

The apparently stronger inequality F_Y(j)>=F_Y(0)-j is not stronger than the requested combined-cost inequality; the two are algebraically identical. Task 6 therefore cannot produce a weaker substitute for a violation at an H0 witness. At an H0 witness there is no violation. Adjacent slope control and convexity are genuinely stronger shape proposals, and both have symbolic triangle-free counterexamples in `EXTENSION_FRONTIER_ANALYSIS.md`.

## Attempt to exploit the first layer

For an optimal remainder h0 whose extension cost is F_Y(0), formula (1) of the analysis note gives

    F_Y(j)-F_Y(0)=min_(S:D_h0(S)=j,a) [p(a)-B_a(S)].

Thus the anchored inequality would follow from B_a(S)<=p(a)+D_h0(S) for every S,a. But this means exactly that the coloring obtained by extending h0 optimally is already globally optimal: it controls every simultaneous change of the remainder and Y. It is not a new estimate from triangle-freeness. The explicit theta example has a unit-slack change saving two extension units, so unit remainder slack cannot alone supply this bound.

Moreover checking j=1 alone is insufficient. Layers can be missing (for example the odd cycle remainder), and an improvement could first occur at some larger attainable j. The exact finite truncation from the identity note is useful bookkeeping: only j<=F_Y(0)-d(G[Y])-1 can strictly defeat layer zero. It does not force those finitely many inequalities for a suitable Y.

## What FULL does and does not supply

FULL is precisely triangle-freeness, n=5k, d(G)=k^2+1, and d-criticality of every edge. No example given in these notes satisfies FULL; no claim under FULL is falsified by an auxiliary example.

Under FULL, the desired conclusion implies

    d(G-Y)>=k^2+1-(2k-1)=(k-1)^2+1.

If the bound has been proved at the previous induction order, this is the contradiction that would close the proof. It cannot be used as an available lower bound on some remainder without proving selection.

Criticality says every edge is monochromatic in some global optimum. In frontier language those global optima attain min_j(j+F_Y(j)), but their attaining layers may all have j>0 for a particular Y. Criticality gives no established restriction forcing one good Y to have an attaining cut in layer zero. Private-cycle witnesses and the triangle-free restrictions on the five boundary neighborhoods likewise give no bound tying a layer-j extension saving to j for a selected Y.

The matching layer-repair proposition in the analysis note is a rigorous sufficient structural condition for slope control. No argument forces that condition, or an adequate replacement, for some five-set under FULL. We do not assume that it does.

## The one exact obstruction

The still-unexcluded obstruction under FULL is:

    for every five-set Y, either F_Y(0)>=2k,
    or there is an attainable integer j with
        1<=j<=F_Y(0)-d(G[Y])-1
    such that
        F_Y(j)<=F_Y(0)-j-1.                            (BLOCKER)

This is exactly the negation of existence of the requested good inherited Y, expressed as a strict integer frontier improvement with its finite possible range. It is an unexcluded configuration of frontiers, not a constructed FULL graph. A cheap layer-zero extension already implies q(Y)<=2k-1 and hence Candidate A for that Y; the second alternative prevents inferring the stronger inherited-optimum conclusion for that same Y.

No proof eliminating BLOCKER and no full-hypothesis counterexample is established. The saved diagnostic tests shapes only at previously certified witnesses, where the anchored condition holds by definition. It cannot supply the missing general selection theorem.

**Hard stop:** no further frontier regularity conjecture, local certificate family, graph search, or n=20 computation is initiated. Proving the existential frontier target would imply Candidate A on its hypothesis domain; it remains unproved here.

## Completed diagnostic and validation

All 19,270 existing saved witness frontiers were computed exactly. The anchored inequality holds throughout, as H0 requires. Adjacent finite-layer slope control passes only 7,745 witnesses; F itself is minimized at zero for only 2,405. No tested stronger shape is universal. These failures concern the recorded witnesses and do not rule out different selections. Full counts and exact first failures are in `EXTENSION_FRONTIER_ANALYSIS.md` and `results/extension_frontier_diagnostic/summary.json`.

Four tests passed, including independent direct-accounting reproduction of the complete profiles and attaining masks for saved graphs 0, 31, and 19269. The diagnostic adds no proof eliminating BLOCKER. The existential target remains unproved, with no full-hypothesis counterexample established.
