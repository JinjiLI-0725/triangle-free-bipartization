# Optimal-face projection and inherited optimum counts

## Conventions and scope

**PROVED:** the equivalences, extension formulas, face-intersection identity, and counting identities below. **NOT PROVED:** existence of a low-q inherited deletion under the full counterexample hypotheses.

G is finite and simple. A coloring is considered modulo simultaneous global reversal, not modulo independent component reversals. For a five-set Y put H=G-Y and q_Y=d(G)-d(H). Work first with H nonempty; an anchor in H gives unique representatives of both global and remainder coloring classes. All 32 assignments on Y then give distinct extensions of an anchored remainder coloring. If n=5, the only Y is V(G); its empty restriction is optimal and a triangle-free G has d(G)<=1, so the desired universal conclusion holds directly.

**Important change of notation:** in this task

    I(Y)=|Res_Y(G) intersect Opt(H)|

counts DISTINCT remainder coloring classes. Earlier inherited-count notes and saved columns named `inherited_optimum_count` count extending GLOBAL optimal cuts instead. Denote that earlier quantity by J(Y). Generally I(Y) != J(Y), although their positivity is equivalent.

## 1. The exact equivalence theorem — PROVED

For every such G,Y the following are equivalent:

1. Some global optimal coloring restricts optimally to H (H0).
2. Res_Y(G) intersect Opt(H) is nonempty.
3. F_Y(0)=q_Y.
4. min_j[j+F_Y(j)] is attained at j=0.
5. The projection of the global optimal face, in the complete cut-coordinate representation defined below, intersects the remainder optimal face.

Proof of 1 iff 2 is the definition. For any remainder coloring h and assignment a on Y let C_Y(h,a) count monochromatic edges touching Y, with internal Y edges counted once. Every global coloring splits uniquely into these two parts and has cost

    mono_H(h)+C_Y(h,a).

Writing j=mono_H(h)-d(H), minimizing over all h,a gives

    q_Y=min_j[j+F_Y(j)].

All finite minima are attained. A minimum at j=0 is exactly an optimal remainder coloring with a global-optimal extension, proving 1 iff 3 iff 4. Missing remainder-cost layers have F=+infinity. The range 0<=j<=|E(H)|-d(H) suffices. The proof of 5 is given in Section 4 and needs no polyhedral theorem beyond convex combinations and linearity.

## 2. Extension fibers and the distinct count — PROVED

For h in Opt(H) define

    E(Y,h)=#{f in Opt(G): f|H=h}.

These are fiber sizes of the restriction map. Thus

    I(Y)=sum_(h in Opt(H)) 1_{E(Y,h)>0},
    J(Y)=sum_(h in Opt(H)) E(Y,h),
    I(Y)<=J(Y)<=32 I(Y).                                (1)

In particular I(Y)=sum_h E(Y,h) would be false with the NEW definition of I.

Use signs a_i,h_v in {-1,+1}, write z=e(Y,H), e_Y=e(G[Y]), and

    b_i(h)=sum_(v in N_H(y_i)) h_v.

Direct accounting yields

    C_Y(h,a)=(z+e_Y)/2
       +(1/2)sum_i b_i(h)a_i
       +(1/2)sum_(y_i y_l in E(Y)) a_i a_l.              (2)

For optimal h every C_Y(h,a)>=q_Y, since its extension is a coloring of G. Consequently

    E(Y,h)=#{a in {-1,+1}^5: C_Y(h,a)=q_Y}
          =[t^q_Y] sum_a t^C_Y(h,a).                   (3)

A minimum-cost extension of h is global-optimal exactly when its extension cost equals q_Y. Merely being a best extension of h is not enough. Formula (3) is a complete 32-assignment characterization; it introduces no restricted flip family.

### A concrete multiplicity distinction

Take P3 with edges 01,12 and seven isolates 3,...,9. Let Y={1,3,4,5,6}. Anchor vertex 0 in the edgeless remainder H={0,2,7,8,9}. Every global optimum colors vertices 0 and 2 alike. The three remaining isolate colors give eight distinct inherited remainder classes. For each, the middle vertex's color is forced and the four deleted isolates have 16 assignments. Hence

    I(Y)=8, J(Y)=128, E(Y,h)=16 for each inherited h.

Opt(H) has 16 coloring classes. Its edge-only cut vectors would ALL be identical because H has no edges. This is why the polyhedral counting model must preserve complete cut coordinates rather than collapse disconnected colorings to their edge-incidence vectors. The example is not a full-hypothesis counterexample.

## 3. Exact projection double counts — PROVED

Let

    D={(Y,h): |Y|=5, h in Opt(H), E(Y,h)>0},
    P={(f,Y): f in Opt(G), f|H in Opt(H)}.

Then |D|=sum_Y I(Y), whereas |P|=sum_Y J(Y)=sum_f |P_f|. For each inherited pair assign weight

    w(f,Y)=1/E(Y,f|H).

Each fiber sums to one, giving the exact reindexing

    sum_Y I(Y)
      =sum_(f in Opt(G)) sum_(Y in P_f) 1/E(Y,f|H).     (4)

For any family A of five-sets, including A={Y:q_Y<=2k-1},

    sum_(Y in A) I(Y)
      =sum_f sum_(Y in A intersect P_f) 1/E(Y,f|H).    (5)

For an inherited pair R_f(Y)=q_Y, so

    sum_Y I(Y) q_Y
      =sum_f sum_(Y in P_f) R_f(Y)/E(Y,f|H).           (6)

One may double count defect-edge incidences as well: define

    N*_f(e)=sum_(Y in P_f, Y touches e) 1/E(Y,f|H).

Then (6) equals sum_f sum_(e monochromatic under f) N*_f(e). Restricting all sums to A gives the same identity for any chosen deletion family.

The unweighted old pair count remains useful for POSITIVITY:

    sum_(Y in A) I(Y)>0 iff sum_(Y in A) J(Y)>0,
    (1/32)sum_(Y in A) J(Y)<=sum_(Y in A) I(Y)
                                  <=sum_(Y in A) J(Y). (7)

But means weighted by I and J can differ. Counts from the old audit cannot be relabeled as distinct projection counts.

There is also an exact collision formula. Put

    K(Y)=sum_(h in Opt(H)) E(Y,h)^2.

This counts ordered global-optimum pairs whose restrictions coincide AND are optimal. Cauchy's inequality gives, when J(Y)>0,

    I(Y)>=J(Y)^2/K(Y).

To verify without invoking a theorem, apply nonnegativity of the sum of squared differences of the I positive fiber sizes, obtaining (sum E)^2<=I sum E^2. This quantifies distinctness once compatible extensions exist; it does not force J(Y)>0. Inclusion-exclusion over the singleton restrictions gives another exact count but likewise requires collision information, not just |Opt(G)|.

## 4. The optimal-face formulation — PROVED from first principles

Use the complete cut polytope

    C_V=conv{delta_f: f a coloring of V modulo reversal},
    (delta_f)_(uv)=1_{f(u)!=f(v)} for EVERY pair uv.

Fixing an anchor r, the coordinates delta_(rv) recover every vertex color relative to r. Thus these vectors identify coloring classes faithfully, even for disconnected graphs.

The graph G specifies an objective w_G with coefficient 1 on its edges and 0 on other pairs. Define its optimal face

    M_G={x in C_V: w_G dot x=MaxCut(G)}.

Every distinct cut vector is a vertex: if a 0/1 vector is a convex combination of 0/1 vectors, each positive-weight term must agree in each coordinate. Conversely a vertex of a finite convex hull is one of its generators. Linearity therefore gives

    M_G=conv{delta_f: f in Opt(G)}.

Opt(G) itself is the finite vertex set, not the whole continuous face.

Let pi_Y retain all pair coordinates within H. Every coloring of H extends, hence pi_Y(C_V)=C_H. Put Q_Y=pi_Y(M_G). Then

    Q_Y=conv{delta_h: h in Res_Y(G)}.                   (8)

Its distinct generating vectors are vertices of C_H, so none is redundant as a vertex of Q_Y. Thus this complete-coordinate model preserves the DISTINCT coloring count, including disconnected remainders.

Let M_H be the face maximizing w_H over C_H. Every generator in (8) has w_H dot delta_h<=MaxCut(H). If a convex combination attains equality, every positive-weight generator attains equality. It follows exactly that

    Q_Y intersect M_H
      =conv{delta_h: h in Res_Y(G) intersect Opt(H)}.   (9)

The convex hull of the empty set is empty. This proves equivalence 5 in the theorem. In particular a fractional intersection cannot exist without an inherited discrete cut. When nonempty, the intersection has exactly I(Y) vertices. It is a face of Q_Y, obtained by maximizing w_H there.

Equation (9) uses the exposed-face equality, not a generic rule that convex hull commutes with intersections. Such a generic rule would be invalid. Projection alone does not make the global optimal face optimal for the restricted objective.

The exact support-function gap is

    MaxCut(H)-max_(x in Q_Y) w_H dot x
      =min_(f in Opt(G)) [mono_f(H)-d(H)]
      =Delta_min(Y)
      =q_Y-max_(f in Opt(G)) R_f(Y).                  (10)

Because the vertices are integral cut vectors, a nonempty Q_Y that misses M_H satisfies the exact separating inequality w_H dot x<=MaxCut(H)-1 for EVERY x in Q_Y. Conversely that inequality excludes intersection. The projected face cannot miss by a positive objective gap smaller than one.

Thus projection turns inheritance into an exact zero-gap condition, with no relaxation error. It does not supply an upper bound forcing that gap to zero for a good Y.

## 5. Triangle-freeness and criticality in this representation

Triangle-freeness restricts which pairs have objective coefficient 1. It does not remove the complete pair coordinates used to identify coloring classes, nor does it make objective contributions across Y disappear. The earlier explicit triangle-free example of three internally disjoint paths of lengths 2,3,3, with the long-path interiors deleted, has F(0)=2 and q=1; its projected optimal face is disjoint from M_H. Therefore triangle-freeness alone cannot ensure intersection for every Y.

For a graph edge e, d-criticality is equivalent to existence of a global optimum making e monochromatic, or

    min_(x in M_G) x_e=0.                              (11)

Proof: deleting a monochromatic edge from an optimal coloring lowers its cost by one, and deletion cannot lower d by more than one. Conversely, an optimal coloring after a critical deletion must make the restored edge monochromatic; otherwise it would beat d(G). This proves (11).

For e in H, (11) passes to Q_Y. But separate coordinate minima may be attained by different points; these conditions do not prove that w_H reaches MaxCut(H) on Q_Y. Full criticality also gives |E(G)|<=|Opt(G)|d(G) by covering all edges with the optimum defect sets. This bounds the number of global optima, not their intersections with M_H.

One valid conditional inheritance statement is: if EVERY global optimum restricts optimally on H and G is d-critical, then H is d-critical. For each edge of H, restrict a global optimum making it monochromatic. The premise is much stronger than nonempty intersection and is not established for a suitable Y.

No heavy polyhedral result, integrality assertion about an outer relaxation, or special face-intersection property has been assumed. All claims above concern the exact convex hull and follow from explicit convex combinations.

## Verification and diagnostic companion

Four exact tests passed in `tests/test_optimal_face_projection.py`. The saved-corpus counts and their scope are in `OPTIMAL_FACE_COUNTING_ATTEMPT.md`. In particular, graph 8814 supplies an exact saved fixed-Y nonintersection even with triangle-freeness and d-criticality; it does not satisfy FULL's d(G)=10 and does not refute existential selection. No universal positivity statement is inferred from the diagnostic.
