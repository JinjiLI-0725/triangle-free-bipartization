import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

EXCHANGE = (
    ROOT
    / "results/hard_regime_L_n15/L11_exchange.jsonl"
)

AUDIT = (
    ROOT
    / "results/hard_regime_L_n15/"
      "L11_3for3_full_audit.tsv"
)


def test_L11_3for3_certificate():
    rows = [
        json.loads(x)
        for x in EXCHANGE.read_text().splitlines()
        if x.strip()
    ]

    assert len(rows) == 3436
    assert len({int(r["id"]) for r in rows}) == 3436
    assert all(int(r["ell"]) == 11 for r in rows)

    audit = list(
        csv.DictReader(AUDIT.open(), delimiter="\t")
    )

    assert len(audit) == 3436

    assert {
        int(r["id"]) for r in audit
    } == {
        int(r["id"]) for r in rows
    }

    assert all(r["pass"] == "1" for r in audit)

    nontrivial = [
        r for r in audit
        if int(r["dG"]) > 5
    ]

    assert len(nontrivial) == 762

    assert Counter(
        int(r["dG"]) for r in audit
    ) == Counter({
        5: 1132,
        4: 856,
        6: 701,
        3: 472,
        2: 160,
        7: 61,
        1: 49,
        0: 5,
    })

    assert Counter(
        int(r["q_found"])
        for r in nontrivial
    ) == Counter({
        5: 429,
        4: 307,
        3: 26,
    })
