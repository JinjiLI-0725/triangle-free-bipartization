# Inherited-optimum counts through five-vertex extensions

## Outcome and scope

**SYMBOLICALLY PROVED:** exact incidence identities; a 32-assignment extension polynomial; coefficient formulas for inherited optima and their defect contribution; a Fourier representation and exact finite LP; and the precise distinction between a cheap extension and an inherited optimum.

**NOT PROVED:** existence of a good inherited pair under the full counterexample hypotheses. No counterexample satisfying those hypotheses is supplied. No graph search, corpus audit, feature mining, or new restricted flip family is used.

FULL means: G is finite, simple, triangle-free, has n=5k vertices, d(G)=k^2+1, and d(G-e)=d(G)-1 for every edge e. General identities below do not require FULL. For FULL, k=1 is impossible since a triangle-free five-vertex graph has d<=1. We therefore use k>=2 so every remainder is nonempty. At k=1 the whole vertex set is the required deletion in the universal triangle-free statement.

Count cuts modulo simultaneous global color reversal, not independent reversal of components. For each Y fix one anchor vertex of H=G-Y and represent every cut of H, and every cut of G for this calculation, by the coloring with that anchor colored +1. Restriction then has no normalization ambiguity. Every remainder cut has exactly 32 extensions. The choice of anchor can depend on Y; the underlying cut classes and all counts are unchanged.

## 1. Incidence double counts — PROVED

Write O=|Opt(G)|, q_Y=d(G)-d(H), and

    P={(f,Y): f in Opt(G), |Y|=5, f|H in Opt(H)}.

With P_f and I(Y) as in the question,

    |P| = sum_f |P_f| = sum_Y I(Y).                         (1)

For an inherited pair, mono_f(H)=d(H), hence R_f(Y)=q_Y. Therefore

    sum_(f,Y in P) R_f(Y)
      = sum_Y I(Y) q_Y
      = sum_f sum_(e monochromatic under f) N_f(e),         (2)

where N_f(e) counts the preserved five-sets touching e. This is a double count of triples (f,Y,e).

If |P|>0, the proposed pair average is exactly

    sum_Y I(Y) q_Y / sum_Y I(Y).                           (3)

A value below 2k suffices by integrality; it is not necessary for the existence of one good pair. If |P|=0, the conditional average is undefined. None of (1)--(3) proves nonemptiness.

## 2. Exact five-variable extension cost — PROVED

Label Y={y_1,...,y_5}. Fix any anchored coloring h of H, initially not necessarily optimal. For each i let

    b_i(h)=sum_(v in N_H(y_i)) h_v,
    z=e(Y,H), e_Y=e(G[Y]), a=(a_1,...,a_5) in {+1,-1}^5.

The number of monochromatic edges involving Y in the extension (h,a) is exactly

    C_h(a)=(z+e_Y)/2
           + (1/2) sum_i b_i(h) a_i
           + (1/2) sum_(y_i y_j in E(G[Y])) a_i a_j.       (4)

Every boundary and internal edge contributes (1+product of its endpoint signs)/2, proving the formula and its integrality. Internal edges are counted once. Define

    ext(Y,h)=min_a C_h(a),
    P_(Y,h)(t)=sum_a t^C_h(a).                            (5)

This is an ordinary polynomial with nonnegative integer coefficients and exactly 32 terms counted with multiplicity. Its degree is at most z+e_Y. It encodes all required extension information without assuming any remainder cut extends optimally.

If h is optimal on H, every extension is a coloring of G, so

    C_h(a)>=q_Y, and ext(Y,h)>=q_Y.                       (6)

Thus the exact extension count is

    E(Y,h)=[t^q_Y] P_(Y,h)(t)
      = #{a: C_h(a)=q_Y}.                                (7)

Equivalently, E=0 if ext>q_Y; if ext=q_Y, E is the number of minimum-cost extensions. In particular, the number of best extensions of h is always positive, whereas the number of GLOBAL-optimal extensions can be zero. Confusing these two numbers would invalidate the argument.

Summing (7) over optimal remainder cuts gives

    I(Y)=sum_(h in Opt(H)) [t^q_Y]P_(Y,h)(t),             (8)
    0<=I(Y)<=min(O,32|Opt(H)|).

No reversal factor is missing, because h was anchored and its 32 assignments yield distinct anchored global cuts.

For each h, the total removed-defect contribution among its GLOBAL-optimal extensions is

    sum_(a: C_h(a)=q_Y) C_h(a)
        = q_Y E(Y,h)
        = [t^q_Y] t P'_(Y,h)(t).                         (9)

If only monochromatic BOUNDARY edges, excluding internal Y edges, are requested, define the bivariate polynomial

    P_(Y,h)(t,u)=sum_a t^C_h(a) u^mono_boundary(h,a).

Then that boundary total is [t^q_Y](partial P/partial u)(t,1). It need not equal q_Y E, since q_Y counts internal edges as well.

## 3. What choosing the remainder first does and does not solve

For a fixed Y define

    epsilon_Y=min_(h in Opt(H)) ext(Y,h)-q_Y >=0.          (10)

Then I(Y)>0 if and only if epsilon_Y=0. Consequently the target is exactly

    some Y has q_Y<=2k-1 and epsilon_Y=0.                (11)

A proof that ext(Y,h)<=2k-1 gives q_Y<=2k-1, so it already gives Candidate A for that Y. It does NOT give epsilon_Y=0 or inheritance. The inequality d(G)<=d(H)+ext has the wrong direction to force equality. Even minimizing ext over all optimal h leaves epsilon_Y potentially positive; no equality theorem for that minimum is proved here.

Here is a fixed elementary example showing the issue for a specified h, with no claim about FULL. Let G be the path u-v-w plus seven isolated vertices, so n=10 and k=2. Take Y={v} plus four isolates. The remainder is edgeless. Color u and w oppositely in an optimal h. Every color for v makes exactly one of uv,vw monochromatic; thus ext=1<=3 while q_Y=d(G)-d(H)=0. There are 32 best extensions, none globally optimal. Other remainder optima, coloring u and w alike, do extend globally. This example only refutes forced equality for a chosen cheap h; it does not refute (11), FULL, or minimization over h.

## 4. All remainder layers: where the global optimum can escape — PROVED

The distinction in (10) has a precise nonnegative-polynomial description. Let C_j(H) be all anchored colorings h with mono_h(H)=d(H)+j, and put

    Q_(Y,j)(t)=sum_(h in C_j(H)) P_(Y,h)(t).

Let Z_G(t) count anchored global colorings by their monochromatic cost. Decomposing every coloring uniquely into h and a gives

    Z_G(t)=t^d(H) sum_(j>=0) t^j Q_(Y,j)(t).             (12)

All coefficients are nonnegative, so there is no cancellation. In particular,

    q_Y=min_(j,h in C_j(H)) [j+ext(Y,h)],                (13)
    O=sum_(j=0)^q_Y [t^(q_Y-j)]Q_(Y,j)(t),              (14)
    I(Y)=[t^q_Y]Q_(Y,0)(t).                             (15)

Every polynomial t^j Q_(Y,j) has no terms below degree q_Y. If I(Y)=0, the leading coefficient in (12) comes entirely from j>=1: every global optimum pays a strictly positive excess in its remainder, compensated by a cheaper cost on edges involving Y. The five-variable problem describes that compensation exactly but does not exclude it.

Thus switching the order of optimization does not remove reoptimization. It restricts the outer minimization in (13) to j=0; proving that this restriction preserves the minimum is precisely the unresolved issue.

Combining (1), (2), and (15) gives fully explicit formulas using extension polynomials:

    |P|=sum_Y [t^q_Y]Q_(Y,0)(t),
    sum_(f,Y in P) R_f(Y)=sum_Y [t^q_Y]t Q'_(Y,0)(t).   (16)

## 5. Assignment averages and the double average — PROVED bounds

Uniform independent signs on Y annihilate all nonconstant terms of (4), giving

    average_a C_h(a)=(z+e_Y)/2.

For triangle-free G[Y] a sharper distribution suffices: choose any optimal coloring a0 of G[Y], and average a0 with its global reversal. The internal cost is always d(G[Y]) and every boundary edge is monochromatic with probability 1/2. Therefore for EVERY h,

    q_Y <= ext(Y,h) <= floor(z/2+d(G[Y]))               (17)

when h is optimal on H. The right inequality does not need h optimal. On five vertices a triangle-free graph is nonbipartite exactly when it is C5, so d(G[Y])=1_C5(Y).

Let C=binom(n,5), m=|E(G)|, and c5 be the number of induced C5 vertex sets. For the precise average in the question, uniform Y followed by uniform optimal anchored h,

    bar_ext = (1/C) sum_Y (1/|Opt(H)|) sum_h ext(Y,h),

we obtain

    d(G) - (1/C)sum_Y d(G-Y)
       <= bar_ext
       <= (1/C)sum_Y floor(z(Y)/2+1_C5(Y))
       <= 5(n-5)m/[n(n-1)] + c5/C.                    (18)

Proof: each edge crosses Y,H with probability 10(n-5)/[n(n-1)]. The C5 expectation is c5/C. Averaging minima over h or Y cannot be replaced by a minimum of averages with the opposite inequality. Uniform averaging over all (Y,h) pairs, instead, would weight each Y by |Opt(H)|; that is a different distribution.

No bound bar_ext<2k under FULL has been derived. Such a bound alone would prove Candidate A by (17), but would still not supply inheritance for its selected Y.

### A symbolic obstruction to a generic double-average bound

Even triangle-freeness plus edge-criticality does not imply bar_ext<2k. Use B3, the balanced C5 blow-up with five independent parts of size three. It has d=9, not the FULL value 10.

For a C5 blow-up with remaining part sizes a_i, one can make each part monochromatic without worsening a cut: its vertices have identical neighbors and no internal edges, so choose a common best color. The resulting weighted cycle has minimum monochromatic cost min_i a_i a_(i+1). Hence d(B3)=9, and after a five-set deletion d(H)=min_i a_i a_(i+1). Every edge is critical because a uniform lifted maximum cut can put its entire part-pair among the defects.

Exactly 3^5=243 deletions remove one vertex from each part. These have d(H)=4 and q=5. Every other deletion removes at least two vertices from some part, leaving an adjacent product at most 1*3=3; thus q>=6. Among these, exactly 5*binom(12,2)=330 deletions remove an entire part; they have q=9. The five choices of entirely removed part cannot overlap in a five-set.

It follows without any computation or graph search that

    sum_Y (q_Y-6) >= -243 + 330*3 = 747,
    average_Y q_Y >= 6+747/3003 = 6+249/1001 >6.

By ext>=q for every optimal h, the requested double average is also strictly greater than six. This does not refute a FULL-specific inequality or the existence target: B3 has 243 good inherited deletions. It rules out a proof using only generic triangle-freeness and criticality. The separate pair-conditioned mean proposal is likewise false generically on B3, as symbolically proved in `ABUNDANCE_COUNTING_PROOF_ATTEMPT.md`, Sections 2--3; no saved numerical audit is needed for that fact.

## 6. Exact Fourier and LP formulations — PROVED

Equation (4) is the complete Boolean Fourier expansion: only the constant, five linear boundary fields, and quadratic terms on G[Y] occur. In particular,

    2 ext(Y,h)=z+e_Y
       + min_(a in {+1,-1}^5)
          [sum_i b_i(h)a_i + sum_(ij in E(Y))a_i a_j].   (19)

This includes all 32 assignments, not a newly restricted certificate family. Triangle-freeness makes G[Y] triangle-free and makes N_Y(v) independent for each core vertex v. Those restrictions do not determine the joint distribution of the fields b_i(h) among optimal h.

An exact rational LP is

    minimize sum_a p_a C_h(a)
    subject to p_a>=0 and sum_a p_a=1.                  (20)

Its dual is

    maximize lambda
    subject to lambda<=C_h(a) for all 32 assignments.  (21)

These have common optimum ext(Y,h): a point mass on a minimizing assignment proves exactness directly. Equivalently, (20) optimizes the affine Fourier expression over the convex hull of all vectors (a_i,a_i a_j). Replacing that hull by only separate coordinate bounds is a relaxation and is not justified as an exact replacement.

For optimal h, lambda=q_Y is dual-feasible by (6). An inherited extension exists exactly when that dual lower bound is tight. A distribution of assignments of mean cost <=q_Y would force equality, since every individual cost is >=q_Y. The known assignment distribution gives only the upper bound in (17), not <=q_Y. The LP dual gives a LOWER bound on extension cost; using it as an upper bound or as automatic equality would be incorrect.

Averaging dual constraints over h preserves lower bounds. Averaging explicit primal distributions gives the upper bounds already stated. Neither operation proves that the optimum occurs in the zero-excess remainder layer of (12).

## 7. What FULL and criticality add, and what is still absent

Under FULL, q_Y=k^2+1-d(H). The good-set condition becomes

    d(H)>=k^2+1-(2k-1)=(k-1)^2+1.

Thus proving the target under FULL would produce a smaller counterexample for an induction; this is the intended contradiction, not an independently available estimate on d(H).

Criticality says each edge is monochromatic in at least one global optimum. To express its content in extension counts exactly, for each edge e define

    Z_(G,e)(t)=sum_(anchored global cuts f)
                  1_{e monochromatic under f} t^mono_f(G).

Then FULL implies [t^(k^2+1)]Z_(G,e)(t)>=1 for every e. Each such marked polynomial has the same remainder decomposition as (12), with an additional indicator in each summand. These positive leading coefficients may come from j>=1 for a given Y. No established identity forces any to come from j=0 for a good Y.

More generally criticality gives |E(G)|<=O(k^2+1), by covering all edges with the O defect sets. It proves a multiplicity lower bound on O, not positivity of (15). Formula (14) shows exactly why having many global optima alone does not locate them in the required remainder layer.

Neither FULL nor its previously proved private-cycle and cut-optimality consequences have here yielded a bound on epsilon_Y or a useful sign for the coefficient-weighted mean (3). No weaker hypothesis is substituted for FULL in claiming a conclusion.

## 8. One exact blocker and hard stop

The unresolved extension-count assertion is the single coefficient-positivity inequality

    sum_(Y: |Y|=5, q_Y<=2k-1)
         [t^q_Y]Q_(Y,0)(t) > 0.                       (BLOCKER)

Its obstruction is explicit in (12)--(15): for every good Y, the global minimum could, as far as the proved bounds show, be realized entirely by positive-excess remainder layers j>=1, with

    min_(h optimal on H) ext(Y,h) >= q_Y+1.

This is an algebraic possibility not excluded by the argument, not a constructed FULL graph. If there are no good Y, the same sum is empty; no independent existence of good Y under FULL has been assumed.

The stronger sufficient pair-mean inequality would be

    sum_Y (2k-q_Y)[t^q_Y]Q_(Y,0)(t)>0,

but it is not necessary for BLOCKER and fails under generic hypotheses. We do not replace the target by that stronger unproved assertion.

The 32-assignment extension problem is solved exactly by (4)--(7). The remaining gap concerns WHICH remainder optima can attain global optimality jointly with a small q, not the optimization over five deleted vertices. No proof or full-hypothesis counterexample has been obtained. A proof of BLOCKER would imply Candidate A on the stated domain and close the corresponding induction route. Stop here.

## Verification

`tests/test_inherited_optimum_count.py` checks (4), (7)--(9), and (12) by direct integer accounting on two fixed labeled fixtures: P3 plus seven isolates and C5 plus five isolates. It also checks the specified cheap but nonglobal extension. These are identity regression tests, not a search over graphs or evidence for FULL.

Command: `python3 -m unittest discover -s tests -p 'test_inherited_optimum_count.py' -v`.

Result: **3 tests passed**. No existing results were overwritten.
