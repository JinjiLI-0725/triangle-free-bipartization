"""Exact counting on explicit fixed examples, not graph search."""
import unittest
import csv,json
from pathlib import Path
from itertools import product
from collections import Counter
from fractions import Fraction


def data(edges,Y):
    V=set(range(10));H=sorted(V-Y)
    allcuts=[(0,)+x for x in product((0,1),repeat=9)]
    cost=lambda f,ee:sum(f[u]==f[v] for u,v in ee)
    he=[(u,v) for u,v in edges if u in H and v in H]
    dg=min(cost(f,edges) for f in allcuts);dh=min(cost(f,he) for f in allcuts)
    opt=[f for f in allcuts if cost(f,edges)==dg]
    normalize=lambda f:min(tuple(f[v] for v in H),tuple(1-f[v] for v in H))
    core={normalize(f) for f in allcuts if cost(f,he)==dh}
    fibers=Counter(normalize(f) for f in opt)
    inherited={h:e for h,e in fibers.items() if h in core}
    return dg,dh,opt,core,fibers,inherited,normalize,he


class ProjectionTests(unittest.TestCase):
    def test_distinct_vs_extension_count(self):
        dg,dh,opt,core,fibers,inherit,norm,he=data([(0,1),(1,2)],{1,3,4,5,6})
        self.assertEqual((dg,dh,len(opt),len(core),len(inherit)),(0,0,128,16,8))
        self.assertEqual(set(inherit.values()),{16})
        self.assertEqual(sum((Fraction(1,inherit[norm(f)]) for f in opt),Fraction()),8)
        self.assertEqual(len({tuple() for h in inherit}),1) # H has no edge coordinates.

    def test_disjoint_faces_triangle_free_example(self):
        edges=[(0,1),(1,2),(0,3),(3,4),(4,2),(0,5),(5,6),(6,2)]
        dg,dh,opt,core,fibers,inherit,norm,he=data(edges,{3,4,5,6,7})
        self.assertEqual((dg,dh,len(inherit)),(1,0,0))
        best_restricted_cut=max(sum(f[u]!=f[v] for u,v in he) for f in opt)
        gap=len(he)-dh-best_restricted_cut
        self.assertEqual(gap,1)
        self.assertTrue(all(sum(f[u]==f[v] for u,v in he)-dh==1 for f in opt))

    def test_maximum_fiber_size(self):
        dg,dh,opt,core,fibers,inherit,norm,he=data([],{1,3,4,5,6})
        self.assertEqual((len(opt),len(inherit)),(512,16))
        self.assertEqual(set(inherit.values()),{32})
        self.assertEqual(sum(inherit.values()),32*len(inherit))


    def test_saved_critical_projection_failure(self):
        root=Path(__file__).resolve().parents[1]
        summary_path=root/'results/optimal_face_projection/summary.json'
        if not summary_path.exists():self.skipTest('diagnostic not yet available')
        p=json.loads(summary_path.read_text())['first_sample_critical_nonintersection']
        self.assertIsNotNone(p)
        with (root/'results/global_cut_landscape_n15/global_optimal_cuts.tsv').open() as stream:
            r=next(r for r in csv.DictReader(stream,delimiter='\t') if int(r['id'])==p['id'])
        cuts=[int(x) for x in r['optG_masks'].split(',')]
        g6=p['graph6'];edges=[];adj=[set() for _ in range(15)];bit=0
        for v in range(1,15):
            for u in range(v):
                if ((ord(g6[1+bit//6])-63)>>(5-bit%6))&1:
                    edges.append((u,v));adj[u].add(v);adj[v].add(u)
                bit+=1
        self.assertTrue(all(not (adj[u]&adj[v]) for u,v in edges))
        mono=lambda f,u,v: ((f>>u)&1)==((f>>v)&1)
        self.assertTrue(all(sum(mono(f,u,v) for u,v in edges)==int(p['dG']) for f in cuts))
        self.assertTrue(all(any(mono(f,u,v) for f in cuts) for u,v in edges))
        with (root/'results/global_cut_landscape_n15/fiveset_summary.tsv').open() as stream:
            r=next(r for r in csv.DictReader(stream,delimiter='\t')
                   if int(r['id'])==p['id'] and int(r['Y_mask'])==p['Y_mask'])
        dh=int(r['dH']);H=32767^p['Y_mask']
        core_costs=[sum(mono(f,u,v) for u,v in edges if H>>u&1 and H>>v&1) for f in cuts]
        self.assertGreater(min(core_costs),dh)
        self.assertEqual(int(p['dG'])-dh,p['q'])
        self.assertLessEqual(p['q'],5)


if __name__=='__main__':unittest.main()
