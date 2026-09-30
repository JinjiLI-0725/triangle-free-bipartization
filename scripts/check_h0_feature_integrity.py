#!/usr/bin/env python3
"""Single sequential pass to count and hash the committed full feature table."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results/h0_witness_structure'
check=[list(map(int,line.split())) for line in (OUT/'checkpoints.tsv').read_text().splitlines()]
assert len(check)==19270 and {a[0] for a in check}==set(range(19270))
path=OUT/'fiveset_features.tsv'
assert path.stat().st_size==check[-1][1]
hash=hashlib.sha256();lines=0;size=0
with path.open('rb') as f:
    while block:=f.read(8*1024*1024):
        hash.update(block);lines+=block.count(b'\n');size+=len(block)
assert lines==19270*3003+1
result={'bytes':size,'data_rows':lines-1,'sha256':hash.hexdigest(),'committed_graphs':len(check)}
(OUT/'features_integrity.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
