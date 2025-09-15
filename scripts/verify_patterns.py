#!/usr/bin/env python3
"""
Compute regex match counts for each column in a dataset based on patterns
declared in derived/<DATASET_ID>/SCHEMA.json.

Usage examples:
  - python scripts/verify_patterns.py MIMIC_5.3
  - python scripts/verify_patterns.py MIMIC_5.3 --format json
  - python scripts/verify_patterns.py MIMIC_5.3 \
        --schema derived/MIMIC_5.3/SCHEMA.json \
        --dataset-path datasets/MIMIC_5.3 \
        --strict-nulls

Outputs TSV to stdout by default with columns:
  dataset\ttable\tcolumn\ttotal_non_empty\tmatches\tmismatches\thit_rate\tpattern

Notes:
  - Only columns with a "pattern" in SCHEMA.json are evaluated.
  - Values are stripped of surrounding whitespace prior to evaluation.
  - When --strict-nulls is set, the values 'NULL', 'NA', 'NAN', 'NONE' (case-insensitive)
    are treated as NULLs (ignored) in addition to empty strings.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from typing import Dict, List, Optional, Tuple


STRICT_NULL_TOKENS = {"NULL", "NA", "NAN", "NONE"}


def load_schema(schema_path: str) -> dict:
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)


def compile_patterns(schema: dict) -> Dict[str, Dict[str, re.Pattern]]:
    """
    Return mapping: table_name -> { column_name -> compiled_regex }
    Only includes columns with a non-empty 'pattern' string.
    """
    compiled: Dict[str, Dict[str, re.Pattern]] = {}
    for table in schema.get("tables", []):
        tname = table.get("name")
        cols = table.get("columns", [])
        col_map: Dict[str, re.Pattern] = {}
        for col in cols:
            pat = col.get("pattern")
            cname = col.get("name")
            if not cname or not pat or not isinstance(pat, str):
                continue
            try:
                # Use fullmatch later; patterns should already be anchored but we don't assume.
                col_map[cname] = re.compile(pat)
            except re.error as e:
                print(
                    f"warning: invalid regex for {tname}.{cname}: {pat!r} ({e})",
                    file=sys.stderr,
                )
        if col_map:
            compiled[tname] = col_map
    return compiled


def is_effectively_null(value: str, strict_nulls: bool) -> bool:
    if value == "":
        return True
    if strict_nulls and value.upper() in STRICT_NULL_TOKENS:
        return True
    return False


def scan_table(
    csv_path: str,
    col_patterns: Dict[str, re.Pattern],
    strict_nulls: bool,
) -> Dict[str, Tuple[int, int, int]]:
    """
    Scan a single CSV file and return per-column counts mapping:
      column_name -> (total_non_empty, matches, mismatches)
    Only columns present in both the file header and col_patterns are evaluated.
    """
    counts: Dict[str, Tuple[int, int, int]] = {}
    # Initialize counters
    for cname in col_patterns:
        counts[cname] = (0, 0, 0)

    if not os.path.exists(csv_path):
        return counts

    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            return counts
        name_to_idx = {name: idx for idx, name in enumerate(header)}

        # Keep only columns present in the file
        active_cols = [
            (cname, name_to_idx[cname], col_patterns[cname])
            for cname in col_patterns
            if cname in name_to_idx
        ]
        # If none present, return as-is
        if not active_cols:
            return counts

        # Mutable dict for performance
        tnm: Dict[str, List[int]] = {c[0]: [0, 0, 0] for c in active_cols}

        for row in reader:
            # Guard against ragged rows
            for cname, idx, rgx in active_cols:
                if idx >= len(row):
                    continue
                raw = row[idx]
                val = raw.strip() if isinstance(raw, str) else ""
                if is_effectively_null(val, strict_nulls):
                    continue
                stats = tnm[cname]
                stats[0] += 1  # total_non_empty
                if rgx.fullmatch(val) is not None:
                    stats[1] += 1  # matches
                else:
                    stats[2] += 1  # mismatches

        # Freeze back to tuples
        for cname in tnm:
            t, m, mm = tnm[cname]
            counts[cname] = (t, m, mm)

    return counts


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Regex hit-rate validator from derived SCHEMA.json")
    ap.add_argument(
        "dataset_id",
        help="Dataset identifier (e.g., MIMIC_5.3); resolves paths under derived/ and datasets/",
    )
    ap.add_argument(
        "--schema",
        default=None,
        help="Path to SCHEMA.json (default: derived/<dataset_id>/SCHEMA.json)",
    )
    ap.add_argument(
        "--dataset-path",
        default=None,
        help="Path to dataset folder with CSVs (default: datasets/<dataset_id>)",
    )
    ap.add_argument(
        "--format",
        choices=["tsv", "json"],
        default="tsv",
        help="Output format (default: tsv)",
    )
    ap.add_argument(
        "--strict-nulls",
        action="store_true",
        help="Treat NULL/NA/NAN/NONE (case-insensitive) as NULLs (ignored)",
    )

    args = ap.parse_args(argv)

    dataset_id: str = args.dataset_id
    schema_path = args.schema or os.path.join("derived", dataset_id, "SCHEMA.json")
    dataset_path = args.dataset_path or os.path.join("datasets", dataset_id)

    if not os.path.exists(schema_path):
        print(f"error: schema file not found: {schema_path}", file=sys.stderr)
        return 2
    if not os.path.isdir(dataset_path):
        print(f"error: dataset path not found: {dataset_path}", file=sys.stderr)
        return 2

    schema = load_schema(schema_path)
    patmap = compile_patterns(schema)
    results = []

    for table_name, col_patterns in patmap.items():
        csv_path = os.path.join(dataset_path, f"{table_name}.csv")
        counts = scan_table(csv_path, col_patterns, strict_nulls=args.strict_nulls)
        for col, (total, matches, mismatches) in counts.items():
            # If a column was not present in the CSV, total will be 0
            pattern = col_patterns[col].pattern
            hit_rate = (matches / total) if total > 0 else 0.0
            results.append(
                {
                    "dataset": dataset_id,
                    "table": table_name,
                    "column": col,
                    "total_non_empty": total,
                    "matches": matches,
                    "mismatches": mismatches,
                    "hit_rate": hit_rate,
                    "pattern": pattern,
                }
            )

    # Output
    if args.format == "json":
        json.dump(results, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        # TSV header
        print(
            "\t".join(
                [
                    "dataset",
                    "table",
                    "column",
                    "total_non_empty",
                    "matches",
                    "mismatches",
                    "hit_rate",
                    "pattern",
                ]
            )
        )
        for r in results:
            print(
                "\t".join(
                    [
                        str(r["dataset"]),
                        str(r["table"]),
                        str(r["column"]),
                        str(r["total_non_empty"]),
                        str(r["matches"]),
                        str(r["mismatches"]),
                        f"{r['hit_rate']:.6f}",
                        str(r["pattern"]),
                    ]
                )
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
