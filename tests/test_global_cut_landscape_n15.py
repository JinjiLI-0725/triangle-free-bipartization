"""Independent exact regressions for the frozen global landscape sample."""
import csv,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'results/global_cut_landscape_n15'

def read(path):
    with path.open() as f:return list(csv.DictReader(f,delimiter='\t'))
def mono(edges,c):return sum(((c>>u)^(c>>v))&1==0 for u,v in edges)
def bits(mask,n=15):return [v for v in range(n) if mask>>v&1]
def pack(mask,vs):return sum(((mask>>v)&1)<<i for i,v in enumerate(vs))

class GlobalCutLandscape(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graphs={}
        with (OUT/'sample_input.txt').open() as f:
            while line:=f.readline():
                i,g,n,m,_=line.split()
                cls.graphs[int(i)]=[tuple(map(int,f.readline().split())) for _ in range(int(m))]
        cls.summary=json.loads((OUT/'summary.json').read_text())
        cls.gs={int(r['id']):r for r in read(OUT/'graph_summary.tsv')}
        cls.opts={int(r['id']):list(map(int,r['optG_masks'].split(','))) for r in read(OUT/'global_optimal_cuts.tsv')}

    def test_all_saved_rows_and_identity_counts(self):
        counts={i:0 for i in self.graphs}
        with (OUT/'fiveset_summary.tsv').open() as f:
            for r in csv.DictReader(f,delimiter='\t'):
                i=int(r['id']);counts[i]+=1
                self.assertEqual(int(r['q']),int(r['R_witness'])+int(r['Delta_witness']))
                self.assertEqual(int(r['rho'])==0,int(r['delta_min'])==0)
                self.assertEqual(int(r['rho'])==0,int(r['compatible_optG'])>0)
                self.assertEqual(int(r['S_mask']).bit_count(),int(r['rho']))
                self.assertEqual(int(r['optH_count']),len(r['optH_masks_local'].split(',')))
        self.assertEqual(set(counts.values()),{3003})
        self.assertEqual(sum(counts.values()),self.summary['five_sets'])
        for i,r in self.gs.items():self.assertEqual(int(r['identities_checked']),3003*len(self.opts[i]))

    def test_full_global_cut_enumeration_independent(self):
        for i in (401,9965,19269):
            es=self.graphs[i]
            vals=[(mono(es,c),c) for c in range(0,1<<15,2)]
            d=min(v for v,c in vals)
            self.assertEqual(d,int(self.gs[i]['dG']))
            self.assertEqual([c for v,c in vals if v==d],self.opts[i])
            self.assertTrue(all(mono(es,c)==mono(es,c^32767) for c in self.opts[i]))

    def test_core_optima_and_bruteforce_rho_pairs(self):
        chosen=[]
        for i in (401,1676,6132,10116,8814,9965,19269,1649):
            rs=read(OUT/'checkpoints'/f'{i}.five.tsv')
            # Fixed positions plus first witness of each observed rho value.
            take={0,100,1000,3002}
            for rho in {int(r['rho']) for r in rs}:take.add(next(j for j,r in enumerate(rs) if int(r['rho'])==rho))
            chosen += [rs[j] for j in sorted(take)]
        for r in chosen:
            i=int(r['id']);Y=int(r['Y_mask']);hv=bits(Y^32767);es=self.graphs[i]
            local={v:j for j,v in enumerate(hv)}
            he=[(local[u],local[v]) for u,v in es if u in local and v in local]
            hc=[mono(he,h) for h in range(1024)];dH=min(hc)
            oh=[h for h in range(0,1024,2) if hc[h]==dH]
            self.assertEqual(oh,list(map(int,r['optH_masks_local'].split(','))))
            self.assertEqual(dH,int(r['dH']))
            restrictions=[pack(f,hv) for f in self.opts[i]]
            dm=min(hc[p]-dH for p in restrictions)
            rho=min(min((p^h).bit_count(),10-(p^h).bit_count()) for p in restrictions for h in oh)
            self.assertEqual((dm,rho),(int(r['delta_min']),int(r['rho'])))
            self.assertTrue(all(hc[h]==hc[h^1023] for h in range(1024)))
            f=int(r['f_witness']);h=int(r['h_witness_local']);p=pack(f,hv)
            self.assertEqual((p^h).bit_count(),rho)
            self.assertEqual(hc[h],dH)
            self.assertEqual(hc[p]-dH,int(r['Delta_witness']))
            R=sum(((f>>u)^(f>>v))&1==0 for u,v in es if Y>>u&1 or Y>>v&1)
            self.assertEqual(R,int(r['R_witness']))

    def test_B3_sanity(self):
        i=19269;g=self.gs[i];es=self.graphs[i]
        adj=[{v if u==j else u for u,v in es if j in (u,v)} for j in range(15)]
        self.assertEqual({len(x) for x in adj},{6})
        self.assertEqual(len({tuple(sorted(x)) for x in adj}),5)
        self.assertEqual(int(g['dG']),9)
        self.assertEqual(int(g['min_q']),5)
        self.assertEqual(int(g['good_count']),3**5)
        self.assertEqual(int(g['good_rho0']),3**5)
        self.assertEqual(int(g['d_edge_critical']),1)
        self.assertTrue(all(any(((f>>u)^(f>>v))&1==0 for f in self.opts[i]) for u,v in es))

    def test_switch_gain_and_boundary_statistics(self):
        rs=read(OUT/'reoptimization_witnesses.tsv')
        for r in rs:
            self.assertEqual(int(r['H_boundary_M'])-int(r['H_boundary_C']),int(r['Delta']))
        # Direct edge-based checks on one witness per graph and each size.
        seen=set()
        for r in rs:
            key=(int(r['id']),int(r['S_size']))
            if key in seen:continue
            seen.add(key);i=key[0];Y=int(r['Y_mask']);S=int(r['S_mask']);f=int(r['f_mask'])
            gain=0
            for u,v in self.graphs[i]:
                if not (Y>>u&1 or Y>>v&1) and bool(S>>u&1)!=bool(S>>v&1):
                    gain+=1 if ((f>>u)^(f>>v))&1==0 else -1
            self.assertEqual(gain,int(r['Delta']))

if __name__=='__main__':unittest.main()
