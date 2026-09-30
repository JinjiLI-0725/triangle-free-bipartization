# Extension frontier: exact identities

**Status: symbolic proof.** G is a finite simple graph, Y is a five-set, H=G-Y. These identities do not require triangle-freeness or criticality. A coloring assigns one of two colors to every vertex. Write m_H=|E(H)| and mu_H(h) for its monochromatic-edge count.

For each integer j>=0 let

    C_j(H)={h: mu_H(h)=d(H)+j}.

For a coloring a of Y define C_Y(h,a) as the number of monochromatic edges having at least one endpoint in Y, counting internal Y edges once. Define

    ext(Y,h)=min_a C_Y(h,a),
    F_Y(j)=min_(h in C_j(H)) ext(Y,h),

with min(empty)=+infinity. In particular F_Y(0) is finite. Colorings can instead be counted modulo global reversal, anchored at any vertex of nonempty H; the minima are identical. If H is empty there is one empty coloring and only j=0.

## Identity and inheritance

Every coloring of G is uniquely a pair (h,a), and its cost is

    mu_G(h,a)=mu_H(h)+C_Y(h,a).

Taking minima on both sides gives

    d(G)=d(H)+min_(j>=0) [j+F_Y(j)],
    q(Y)=min_(j>=0) [j+F_Y(j)].                         (1)

All finite minima are attained. In particular q(Y)<=F_Y(0). Equality holds exactly when an optimal h on H has an extension of cost d(G). Thus

    I(Y)>0  iff  F_Y(0)=q(Y)
            iff  F_Y(j)>=F_Y(0)-j for every j>=1.      (2)

Ties at j>0 are allowed: some global optima may have nonoptimal restrictions even when an inherited optimum exists. Neither uniqueness nor strict inequality is needed.

Consequently the request to find a violation of F_Y(j)>=F_Y(0)-j at an H0 witness is logically impossible under the definitions. That inequality and j+F_Y(j)>=F_Y(0) are the SAME condition, not a strong condition and a weaker replacement. An adjacent-level slope condition is different; it can fail at an H0 witness.

## Finite range and holes

Since d(H)<=mu_H(h)<=m_H, every attainable j lies in

    0<=j<=J_max=m_H-d(H).

The upper endpoint is attainable by a constant coloring, but intermediate layers can be absent. For instance, for H=C5 the attainable j are 0,2,4. Record missing layers as +infinity, never as zero or as interpolated values.

Put b=d(G[Y]). Every extension has C_Y(h,a)>=b, hence F_Y(j)>=b on all attainable layers. Therefore evaluating (1), including all possible ties at level F_Y(0), needs only

    0<=j<=min(J_max,F_Y(0)-b).                          (3)

For deciding whether H0 fails, only the positive integers

    1<=j<=min(J_max,F_Y(0)-b-1)                         (4)

can witness a strict improvement, by integrality. Higher layers have j+F_Y(j)>=F_Y(0). In particular F_Y(0)<=b+1 forces inheritance, although it does not ensure existence of a Y with such a small F_Y(0).

For triangle-free G and |Y|=5, b is 1 if G[Y]=C5 and 0 otherwise. Averaging an optimal coloring of G[Y] and its reversal gives

    b<=F_Y(0)<=b+floor(e(Y,H)/2).

This is an upper bound on the finite range in (3); it is not a proof that the minimum of (1) is attained at zero.

## Boolean representation

Use signs a_i,h_v in {-1,+1}, and write z=e(Y,H), e_Y=e(G[Y]),

    b_i(h)=sum_(v in N_H(y_i)) h_v.

Then exactly

    C_Y(h,a)=(z+e_Y)/2
       +(1/2)sum_i b_i(h)a_i
       +(1/2)sum_(y_i y_l in E(Y)) a_i a_l.             (5)

Thus each ext is a 32-assignment integer minimum. F_Y(j) minimizes that value over the exact remainder-cost layer, not just over optimal remainders. Equation (5) alone does not prescribe how the possible field vectors b(h) are distributed across those layers.
