"""Fixed symbolic fixtures only: no graph search or corpus audit."""
import itertools
import unittest


def gamma(edges, colors, S):
    return sum((1 if colors[u]==colors[v] else -1)
               for u,v in edges if (u in S)!=(v in S))

def weight(edges, colors, A, B):
    return sum((1 if colors[u]==colors[v] else -1) for u,v in edges
               if (u in A and v in B) or (v in A and u in B))

def subsets(vs):
    vs=list(vs)
    return [{v for j,v in enumerate(vs) if mask>>j&1} for mask in range(1<<len(vs))]

class OptimalRestrictionIdentities(unittest.TestCase):
    def setUp(self):
        self.es=[(0,1),(1,2),(2,3),(3,4),(4,0)]
        self.c=[0,1,0,1,0]

    def test_deletion_identity_every_C5_deletion_and_support(self):
        V=set(range(5))
        for Y in subsets(V):
            he=[e for e in self.es if not set(e)&Y]
            for S in subsets(V-Y):
                self.assertEqual(gamma(he,self.c,S),gamma(self.es,self.c,S)-weight(self.es,self.c,S,Y))

    def test_both_signed_uncrossing_identities(self):
        V=set(range(5))
        for S in subsets(V):
            for T in subsets(V):
                lhs=gamma(self.es,self.c,S)+gamma(self.es,self.c,T)
                self.assertEqual(lhs-gamma(self.es,self.c,S&T)-gamma(self.es,self.c,S|T),2*weight(self.es,self.c,S-T,T-S))
                self.assertEqual(lhs-gamma(self.es,self.c,S-T)-gamma(self.es,self.c,T-S),2*weight(self.es,self.c,S&T,V-(S|T)))
        self.assertLess(gamma(self.es,self.c,{0})+gamma(self.es,self.c,{1}),gamma(self.es,self.c,{0,1}))
        self.assertGreater(gamma(self.es,self.c,{0})+gamma(self.es,self.c,{4}),gamma(self.es,self.c,{0,4}))

    def test_crossing_minimal_profitable_supports_in_critical_cactus(self):
        cycles=[[0,1,6,7,3],[1,2,8,9,4],[2,10,11,12,5]]
        es=[(cy[j],cy[(j+1)%5]) for cy in cycles for j in range(5)]
        c=[0,1,0,0,1,0,0,1,1,0,1,0,1,0,0]
        Y={6,8,10,13,14};he=[e for e in es if not set(e)&Y]
        self.assertEqual(sum(c[u]==c[v] for u,v in es),3)
        for S in ({0,1},{1,2}):
            self.assertEqual(gamma(he,c,S),1)
            self.assertTrue(all(gamma(he,c,A)<=0 for A in subsets(S) if A!=S))
        self.assertEqual([gamma(he,c,S) for S in ({1},{0},{2},{0,1,2})],[-1,0,0,3])
        adj={i:set() for i in range(15)}
        for u,v in es:adj[u].add(v);adj[v].add(u)
        self.assertTrue(all(not adj[u]&adj[v] for u,v in es))

    def test_sharp_large_support_fixed_odd_cycle(self):
        # One fixed C15 fixture, not a search over graphs.
        n=15;es=[(i,(i+1)%n) for i in range(n)];c=[i%2 for i in range(n)]
        Y=set(range(5,10));he=[e for e in es if not set(e)&Y]
        for S in (set(range(5)),set(range(10,15))):
            self.assertEqual(gamma(he,c,S),1)
            self.assertTrue(all(gamma(he,c,A)<=0 for A in subsets(S) if A!=S))

    def test_nonmonotone_preservation(self):
        def preserves(Y):
            he=[e for e in self.es if not set(e)&Y]
            return max(gamma(he,self.c,S) for S in subsets(set(range(5))-Y))==0
        self.assertTrue(preserves(set()))
        self.assertFalse(preserves({1}))
        self.assertTrue(preserves({1,4}))

if __name__=='__main__':unittest.main()
