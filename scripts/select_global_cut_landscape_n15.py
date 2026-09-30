#!/usr/bin/env python3
"""Deterministic bounded selection from saved records, no graph generation."""
import csv, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results/global_cut_landscape_n15'
CORPUS=ROOT/'results/zero_margin_tightness/corpus.txt'

def main():
    OUT.mkdir(exist_ok=True)
    if (OUT/'sample_manifest.tsv').exists(): raise SystemExit('Manifest exists; refusing to replace sample')
    records={}
    with CORPUS.open() as f:
        while line:=f.readline():
            i,g,n,m,_=line.split(); edges=[tuple(map(int,f.readline().split())) for _ in range(int(m))]
            records[int(i)]={'id':int(i),'graph6':g,'edges':edges,'n':int(n),'m':int(m)}
    hard={int(r['id']):r for r in csv.DictReader((ROOT/'results/hard_regime_L_n15/hard_classes.tsv').open(),delimiter='\t')}
    ds=dict(map(lambda s:map(int,s.split()),(ROOT/'results/hard_regime_L_n15/d.tsv').read_text().splitlines()))
    reasons={}
    def add(i,why):
        if i not in reasons and len(reasons)>=40: return
        reasons.setdefault(i,[]).append(why)
    for i in (401,1676,6132,10116):
        if i in records: add(i,'explicit_requested_previous_witness')
    # Identify B3 from saved adjacency only: five twin classes of size three,
    # degree six, quotient degree two and connected.
    b3=[]
    for i,r in records.items():
        if r['m']!=45:continue
        adj=[set() for _ in range(15)]
        for u,v in r['edges']:adj[u].add(v);adj[v].add(u)
        classes={tuple(sorted(a)) for a in adj}
        if len(classes)==5 and all(len(a)==6 for a in adj) and all(sum(tuple(sorted(a))==c for a in adj)==3 for c in classes):
            seen={0}; stack=[0]
            while stack:
                for v in adj[stack.pop()]-seen:seen.add(v);stack.append(v)
            if len(seen)==15:b3.append(i);add(i,'B3_verified_twin_class_signature')
    for i,r in sorted(hard.items()):
        if r['d_edge_critical']=='1':add(i,'saved_d_edge_critical_flag')
    for i in sorted(records,key=lambda i:(-ds[i],i))[:8]:add(i,'top_8_saved_d_then_id')
    for L in sorted({int(r['L']) for r in hard.values()},reverse=True):
        ids=[i for i,r in hard.items() if int(r['L'])==L]
        add(min(ids),'first_id_at_saved_L_'+str(L))
    for d in sorted(set(ds.values()),reverse=True):
        add(min(i for i in records if ds[i]==d),'first_id_at_saved_d_'+str(d))
    strata=sorted({(int(r['L']),int(r['d'])) for r in hard.values()},key=lambda t:(-t[1],-t[0]))
    for L,d in strata:
        add(min(i for i,r in hard.items() if (int(r['L']),int(r['d']))==(L,d)),f'first_id_in_stratum_L{L}_d{d}')
        if len(reasons)==40:break
    assert 20<=len(reasons)<=50
    with (OUT/'sample_manifest.tsv').open('w') as f, (OUT/'sample_input.txt').open('w') as inp:
        w=csv.writer(f,delimiter='\t',lineterminator='\n')
        w.writerow(['sample_index','corpus_id','graph6','saved_L','saved_d','saved_critical','selection_reasons','source'])
        for j,(i,why) in enumerate(reasons.items()):
            r=records[i]; hr=hard.get(i,{})
            w.writerow([j,i,r['graph6'],hr.get('L','<=10'),ds[i],hr.get('d_edge_critical','unknown'),';'.join(why),'results/zero_margin_tightness/corpus.txt'])
            inp.write(f"{i} {r['graph6']} 15 {r['m']} -1\n")
            for u,v in r['edges']:inp.write(f'{u} {v}\n')
    meta={'count':len(reasons),'B3_ids':b3,'sampling':'Deterministic, bounded, non-random; saved corpus only',
          'source_sha256':hashlib.sha256(CORPUS.read_bytes()).hexdigest(),
          'missing_previous_obstruction':'The three-layer 35-edge fixed-Y construction was not found in the saved corpus by its necessary degree and component signature; not generated.',
          'warning':'Saved critical flags are selection metadata only; exact criticality is recomputed.'}
    (OUT/'selection.json').write_text(json.dumps(meta,indent=2)+'\n')
    print(json.dumps(meta))
if __name__=='__main__':main()
