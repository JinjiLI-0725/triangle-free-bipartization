"""Fixed symbolic fixtures and direct-accounting checks, not graph search."""
import unittest
import csv
import json
from pathlib import Path
from itertools import product


def exact_frontier(edges, Y, n=10):
    H=set(range(n))-Y
    rows=[]
    for colors in product((0,1),repeat=n-1):
        c=(0,)+colors
        core=sum(c[u]==c[v] for u,v in edges if u in H and v in H)
        total=sum(c[u]==c[v] for u,v in edges)
        rows.append((core,total))
    dh=min(c for c,t in rows);dg=min(t for c,t in rows)
    frontier=[None]*(max(c for c,t in rows)-dh+1)
    for c,t in rows:
        j=c-dh;cost=t-c
        if frontier[j] is None or cost<frontier[j]:frontier[j]=cost
    assert min(j+x for j,x in enumerate(frontier) if x is not None)==dg-dh
    return frontier,dg,dh


class FrontierTests(unittest.TestCase):
    def test_one_step_failure(self):
        edges=[(0,1),(1,2),(0,3),(3,4),(4,2),(0,5),(5,6),(6,2)]
        F,dg,dh=exact_frontier(edges,{3,4,5,6,7})
        self.assertEqual((F,dg,dh),([2,0,2],1,0))
        self.assertLess(F[1],F[0]-1)

    def test_h0_without_adjacent_lipschitz_or_convexity(self):
        edges=[(0,1),(1,2),(2,3),(0,4),(4,5),(5,3),(0,6),(6,7),(7,3)]
        F,dg,dh=exact_frontier(edges,{4,5,6,7,8})
        self.assertEqual((F,dg,dh),([0,2,0,2],0,0))
        self.assertTrue(all(j+x>=F[0] for j,x in enumerate(F)))
        self.assertLess(F[2],F[1]-1)
        self.assertLess(F[2]+F[0],2*F[1])

    def test_missing_layers_and_critical_cycle(self):
        edges=[(i,(i+1)%9) for i in range(9)]
        self.assertEqual(exact_frontier(edges,{4,5,6,7,8}),([1,0,1,0],1,0))
        edges=[(i,(i+1)%5) for i in range(5)]
        self.assertEqual(exact_frontier(edges,{5,6,7,8,9}),([0,None,0,None,0],1,1))


    def test_saved_witness_frontiers_direct_accounting(self):
        root=Path(__file__).resolve().parents[1]
        out=root/'results/extension_frontier_diagnostic'
        if not (out/'summary.json').exists():
            self.skipTest('saved diagnostic not yet complete')
        summary=json.loads((out/'summary.json').read_text())
        with (out/'frontiers.tsv').open() as stream:
            rows=list(csv.DictReader(stream,delimiter='\t'))
        chosen={r['id']:r for r in (rows[0],rows[-1])}
        for key in ('adjacent_lower_lipschitz','convex_finite_triples','F_min_at_zero'):
            r=summary['first_failures'][key]
            if r is not None:chosen[r['id']]=r
        for r in chosen.values():
            g6=r['graph6'];edges=[];bit=0
            for j in range(1,15):
                for i in range(j):
                    if ((ord(g6[1+bit//6])-63)>>(5-bit%6))&1:edges.append((i,j))
                    bit+=1
            Y={v for v in range(15) if int(r['Y_mask'])>>v&1}
            F,dg,dh=exact_frontier(edges,Y,15)
            expected=[None if x=='NA' else int(x) for x in r['F'].split(',')]
            self.assertEqual((F,dg,dh),(expected,int(r['dG']),int(r['dH'])))
            masks=r['attaining_global_masks'].split(',')
            for j,value in enumerate(F):
                if value is None:
                    self.assertEqual(masks[j],'NA')
                    continue
                mask=int(masks[j]);H=set(range(15))-Y
                mono=lambda u,v: ((mask>>u)&1)==((mask>>v)&1)
                core=sum(mono(u,v) for u,v in edges if u in H and v in H)
                total=sum(mono(u,v) for u,v in edges)
                self.assertEqual((core,total-core),(dh+j,value))



if __name__=='__main__':unittest.main()
