"""Portable validation for the full H0 audit.

Lightweight release checks use compact summary/witness artifacts.
Checkpoint-heavy cross-checks run only when the corresponding checkpoint
directories are present.
"""
import csv
import json
import os
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(
    os.environ.get(
        "H0_FULL_DIR",
        str(ROOT / "results/global_cut_landscape_n15_full"),
    )
)
REF = ROOT / "results/global_cut_landscape_n15"


def rows(path):
    with path.open() as f:
        return list(csv.DictReader(f, delimiter="\t"))


class FullH0(unittest.TestCase):
    def test_every_sample_fiveset_matches_reference(self):
        """Exact sample cross-check when full checkpoints are available."""
        out_cp = OUT / "checkpoints"
        ref_cp = REF / "checkpoints"

        if not out_cp.exists():
            self.skipTest(
                "Full-corpus checkpoint directory not included in lightweight release"
            )

        ids = [int(r["corpus_id"]) for r in rows(REF / "sample_manifest.tsv")]

        for i in ids:
            path = out_cp / f"{i}.landscape.bin"
            if not path.exists():
                self.skipTest(
                    f"Full checkpoint fixture {path.name} not included"
                )

            data = path.read_bytes()
            self.assertEqual(len(data), 9009)

            rr = rows(ref_cp / f"{i}.five.tsv")
            self.assertEqual(len(rr), 3003)

            for j, r in enumerate(rr):
                self.assertEqual(
                    tuple(data[3 * j : 3 * j + 3]),
                    tuple(int(r[k]) for k in ("dH", "delta_min", "rho")),
                    (i, r["Y_mask"]),
                )

            self.assertEqual(
                rows(out_cp / f"{i}.summary.tsv"),
                rows(ref_cp / f"{i}.summary.tsv"),
            )
            self.assertEqual(
                (out_cp / f"{i}.opt.txt").read_text().strip(),
                rows(ref_cp / f"{i}.cuts.tsv")[0]["optG_masks"],
            )

    def test_h0_witnesses_compact_release(self):
        """Validate released H0 witness table without 531 MB checkpoints."""
        corpus = ROOT / "results/zero_margin_tightness/corpus.txt"
        witness_file = OUT / "h0_witnesses.tsv"

        self.assertTrue(corpus.exists())
        self.assertTrue(witness_file.exists())

        witnesses = rows(witness_file)
        self.assertGreater(len(witnesses), 0)

        by_id = {int(r["id"]): r for r in witnesses}

        with corpus.open() as f:
            while line := f.readline():
                i, g, n, m, _ = line.split()
                i = int(i)
                m = int(m)

                es = [
                    tuple(map(int, f.readline().split()))
                    for _ in range(m)
                ]

                if i not in by_id:
                    continue

                w = by_id[i]
                Y = int(w["Y_mask"])
                cut = int(w["f_mask"])

                self.assertEqual(Y.bit_count(), 5)

                mono = lambda ee, cc: sum(
                    (((cc >> u) ^ (cc >> v)) & 1) == 0
                    for u, v in ee
                )

                raw = mono(es, cut)
                he = [
                    (u, v)
                    for u, v in es
                    if not (Y >> u & 1 or Y >> v & 1)
                ]

                self.assertEqual(raw, int(w["dG"]))
                self.assertEqual(mono(he, cut), int(w["dH"]))
                self.assertEqual(raw - mono(he, cut), int(w["q"]))
                self.assertLessEqual(int(w["q"]), 5)
                self.assertEqual((w["Delta"], w["rho"]), ("0", "0"))

                # Independent exact recurrence verifies the witness core optimum.
                hv = [v for v in range(15) if not (Y >> v & 1)]
                loc = {v: j for j, v in enumerate(hv)}
                adj = [0] * 10

                for u, v in he:
                    adj[loc[u]] |= 1 << loc[v]
                    adj[loc[v]] |= 1 << loc[u]

                cost = [len(he)] * 512
                for mask in range(1, 512):
                    bit = (mask & -mask).bit_length() - 1
                    v = bit + 1
                    prev = mask ^ (1 << bit)
                    cost[mask] = (
                        cost[prev]
                        - adj[v].bit_count()
                        + 2 * (adj[v] & (prev << 1)).bit_count()
                    )

                self.assertEqual(min(cost), int(w["dH"]))

    def test_full_completion_or_exact_failure(self):
        path = OUT / "summary.json"
        self.assertTrue(path.exists())

        s = json.loads(path.read_text())

        if s["first_failure"] is None:
            self.assertEqual(s["graphs_analyzed"], 19270)
        else:
            self.assertTrue((OUT / "failures.tsv").exists())

        self.assertEqual(
            s["five_sets_analyzed"],
            3003 * s["graphs_analyzed"],
        )
        self.assertEqual(
            len(rows(OUT / "graph_summary.tsv")),
            s["graphs_analyzed"],
        )
        self.assertEqual(
            len(rows(OUT / "h0_witnesses.tsv")),
            s["h0_pass_count"],
        )


if __name__ == "__main__":
    unittest.main()
