"""Exact identities on two fixed fixtures; no graph generation or search."""
from collections import Counter, defaultdict
from itertools import product
from fractions import Fraction
import unittest


def colorings(vertices, anchor=None):
    free = [v for v in sorted(vertices) if v != anchor]
    for signs in product((-1, 1), repeat=len(free)):
        h = dict(zip(free, signs))
        if anchor is not None:
            h[anchor] = 1
        yield h


def mono(edges, h):
    return sum(h[u] == h[v] for u, v in edges)


class ExtensionIdentities(unittest.TestCase):
    def check_fixture(self, edges, Y):
        V = set(range(10)); H = V-Y; anchor = min(H)
        inner = [(u,v) for u,v in edges if u in H and v in H]
        removed = [(u,v) for u,v in edges if u in Y or v in Y]
        eY = sum(u in Y and v in Y for u,v in edges)
        z = len(removed)-eY
        hs = list(colorings(H, anchor))
        dH = min(mono(inner,h) for h in hs)
        layers = defaultdict(Counter)
        extension_counts = {}
        for idx,h in enumerate(hs):
            fields = {u: sum(h[v] for v in H if (u,v) in edges or (v,u) in edges)
                      for u in Y}
            P = Counter()
            for a in colorings(Y):
                f = h | a
                cost = mono(removed,f)
                twice = z+eY+sum(fields[u]*a[u] for u in Y)
                twice += sum(a[u]*a[v] for u,v in edges if u in Y and v in Y)
                self.assertEqual(twice,2*cost)
                P[cost] += 1
            self.assertEqual(sum(P.values()),32)
            layers[mono(inner,h)-dH].update(P)
            extension_counts[idx] = P
        direct = Counter(mono(edges,f) for f in colorings(V,anchor))
        reconstructed = Counter()
        for j,P in layers.items():
            for cost,num in P.items():
                reconstructed[dH+j+cost] += num
        self.assertEqual(direct,reconstructed)
        dG = min(direct); q = dG-dH
        inherited = [f for f in colorings(V,anchor)
                     if mono(edges,f)==dG and mono(inner,f)==dH]
        self.assertEqual(layers[0][q],len(inherited))
        self.assertEqual(sum(mono(removed,f) for f in inherited),q*len(inherited))
        for idx,h in enumerate(hs):
            if mono(inner,h)==dH:
                self.assertGreaterEqual(min(extension_counts[idx]),q)
        return q

    def test_partition_and_fourier_path(self):
        self.assertEqual(self.check_fixture([(0,1),(1,2)],{1,3,4,5,6}),0)

    def test_partition_and_fourier_cycle(self):
        self.assertEqual(self.check_fixture([(i,(i+1)%5) for i in range(5)],
                                           {0,1,5,6,7}),1)

    def test_cheap_extension_not_equality(self):
        edges = [(0,1),(1,2)]; Y={1,3,4,5,6}
        h={0:1,2:-1,7:1,8:1,9:1}
        P=Counter(mono(edges,h|a) for a in colorings(Y))
        self.assertEqual(P,Counter({1:32}))
        self.assertEqual(P[0],0)
        self.assertEqual(Fraction(747,3003),Fraction(249,1001))


if __name__ == '__main__':
    unittest.main()
