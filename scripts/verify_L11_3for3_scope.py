#!/usr/bin/env python3

import json
from pathlib import Path

L_RECORDS = Path("results/hard_regime_L_n15/L_records.tsv")
EXCHANGE = Path("results/hard_regime_L_n15/L11_exchange.jsonl")
AUDIT = Path("results/hard_regime_L_n15/L11_3for3_full_audit.tsv")

def load_global_L11():
    out = {}
    for line in L_RECORDS.read_text().splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        rid = int(parts[0])
        graph6 = parts[1]
        L = int(parts[3])
        if L == 11:
            out[rid] = graph6
    return out

def load_exchange():
    rows = [
        json.loads(x)
        for x in EXCHANGE.read_text().splitlines()
        if x.strip()
    ]
    return {int(r["id"]): r["graph6"] for r in rows}

def load_audit_ids():
    lines = [
        x for x in AUDIT.read_text().splitlines()
        if x.strip()
    ]

    header = lines[0].split("\t")
    id_col = header.index("id")
    pass_col = header.index("pass")

    ids = set()
    failures = []

    for line in lines[1:]:
        parts = line.split("\t")
        rid = int(parts[id_col])
        ok = parts[pass_col].lower() in {"1", "true", "yes"}
        ids.add(rid)
        if not ok:
            failures.append(rid)

    return ids, failures

def main():
    L11 = load_global_L11()
    E = load_exchange()
    audit_ids, failures = load_audit_ids()

    same_ids = set(L11) == set(E)
    missing = sorted(set(L11) - set(E))
    extra = sorted(set(E) - set(L11))
    mismatches = sorted(
        rid for rid in set(L11) & set(E)
        if L11[rid] != E[rid]
    )

    audit_same_ids = audit_ids == set(E)

    print("L_records global L=11:", len(L11))
    print("L11_exchange records:", len(E))
    print("same ID set:", same_ids)
    print("missing:", missing, "count =", len(missing))
    print("extra:", extra, "count =", len(extra))
    print("graph6 mismatches:", mismatches, "count =", len(mismatches))
    print("audit ID set matches:", audit_same_ids)
    print("audit failures:", failures)

    ok = (
        len(L11) == 3436
        and len(E) == 3436
        and same_ids
        and not missing
        and not extra
        and not mismatches
        and audit_same_ids
        and not failures
    )

    print()
    print("SCOPE_CERTIFICATE=PASS" if ok else "SCOPE_CERTIFICATE=FAIL")

    raise SystemExit(0 if ok else 1)

if __name__ == "__main__":
    main()
