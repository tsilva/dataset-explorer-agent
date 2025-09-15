# Dataset Agents

A small repository of self-contained datasets and their derived schemas for experimentation. The main utility here is a simple regex hit-rate validator for dataset columns.

## Quick Start

- Validate patterns for MIMIC 5.3 and print TSV (default):
  - `python scripts/verify_patterns.py MIMIC_5.3`
- Emit CSV or JSON instead:
  - `python scripts/verify_patterns.py MIMIC_5.3 --format csv`
  - `python scripts/verify_patterns.py MIMIC_5.3 --format json`
- Save CSV results to a file (e.g., `audit.csv`):
  - `python scripts/verify_patterns.py MIMIC_5.3 --format csv > audit.csv`

## Validator Details

- Script: `scripts/verify_patterns.py`
- Purpose: For each column with a `pattern` in `derived/<DATASET>/SCHEMA.json`, count how many non-empty values match vs. do not match.
- Default dataset layout:
  - Schema: `derived/MIMIC_5.3/SCHEMA.json`
  - Data: `datasets/MIMIC_5.3/*.csv`
- Output columns: `dataset`, `table`, `column`, `total_non_empty`, `matches`, `mismatches`, `hit_rate`, `pattern`.
- Hit-rate semantics: if a column has zero non-empty values, `hit_rate` is reported as `1.0` (trivially satisfied).

## Options

- `--schema <path>`: Path to `SCHEMA.json`. Default: `derived/<DATASET>/SCHEMA.json`.
- `--dataset-path <path>`: Path to dataset folder with CSVs. Default: `datasets/<DATASET>`.
- `--format tsv|csv|json`: Output format (default: `tsv`).
- `--strict-nulls`: Treat `NULL/NA/NAN/NONE` (case-insensitive) as NULL and ignore them when computing hit rates.

## Examples

- Validate with strict NULL handling and JSON output:
  - `python scripts/verify_patterns.py MIMIC_5.3 --strict-nulls --format json`
- Validate a different dataset/root (custom paths):
  - `python scripts/verify_patterns.py MIMIC_5.3 --schema derived/MIMIC_5.3/SCHEMA.json --dataset-path datasets/MIMIC_5.3 --format csv`

## Notes

- Performance: Large tables (e.g., `measurement.csv`) will take longer as the validator scans all rows.
- Python: Uses the standard library; Python 3.8+ recommended.
