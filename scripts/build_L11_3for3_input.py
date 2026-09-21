#!/usr/bin/env python3

import argparse
import json
from collections import Counter
from pathlib import Path

def decode_graph6(s: str):
    vals = [ord(c) - 63 for c in s.strip()]
    if not vals:
        raise ValueError("empty graph6 string")

    n = vals[0]
    bits = []

    for x in vals[1:]:
        for k in range(5, -1, -1):
            bits.append((x >> k) & 1)

    edges = []
    pos = 0

    for v in range(1, n):
        for u in range(v):
            if bits[pos]:
                edges.append((u, v))
            pos += 1

    return n, edges

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--source",
        default="results/hard_regime_L_n15/L11_exchange.jsonl",
    )
    ap.add_argument(
        "--output",
        default="results/hard_regime_L_n15/L11_3for3_input.txt",
    )
    args = ap.parse_args()

    rows = [
        json.loads(line)
        for line in Path(args.source).read_text().splitlines()
        if line.strip()
    ]

    seen = set()
    ell_dist = Counter()

    with open(args.output, "w") as f:
        f.write(f"{len(rows)}\n")

        for r in rows:
            rid = int(r["id"])

            assert rid not in seen
            seen.add(rid)

            X = list(map(int, r["X"]))
            assert len(X) == 5
            assert len(set(X)) == 5

            ell_dist[int(r["ell"])] += 1

            n, edges = decode_graph6(r["graph6"])
            assert n == 15

            f.write(
                f"{rid} {int(r['dG'])} "
                + " ".join(map(str, X))
                + f" {len(edges)}\n"
            )

            for u, v in edges:
                f.write(f"{u} {v}\n")

    print("records =", len(rows))
    print("unique_ids =", len(seen))
    print("ell distribution =", dict(sorted(ell_dist.items())))
    print("output =", args.output)

if __name__ == "__main__":
    main()
