<div align="center">
  <img src="logo.png" alt="dataset-explorer-agent" width="512" />

  [![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
  [![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
  [![No Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen.svg)](#)

  **🔍 Validate dataset schemas with regex pattern hit-rate analysis — zero dependencies, instant results ⚡**

  [Quick Start](#quick-start) · [Usage](#usage) · [Schema Format](#schema-format)
</div>

---

## Overview

A lightweight Python tool for validating dataset columns against regex patterns defined in JSON schemas. Computes per-column match statistics (hit rates) to identify data quality issues in CSV datasets.

Built for the OMOP CDM v5.3 format but works with any CSV dataset that has an accompanying schema.

### Features

- **Zero dependencies** - Uses only Python standard library
- **Multiple output formats** - TSV (default), CSV, or JSON
- **Flexible NULL handling** - Optional strict mode for `NULL/NA/NAN/NONE` values
- **Clear statistics** - Reports matches, mismatches, and hit rates per column
- **Custom paths** - Override default schema and dataset locations

## Quick Start

```bash
# Validate patterns for MIMIC 5.3 dataset
python scripts/verify_patterns.py MIMIC_5.3
```

Output (TSV):
```
dataset   table       column              total_non_empty  matches  mismatches  hit_rate  pattern
MIMIC_5.3 person      person_id           1000             1000     0           1.000000  ^\d+$
MIMIC_5.3 person      birth_datetime      1000             1000     0           1.000000  ^\d{4}-\d{2}-\d{2}.*
...
```

## Installation

No installation required. Clone and run:

```bash
git clone https://github.com/tsilva/dataset-explorer-agent.git
cd dataset-explorer-agent
python scripts/verify_patterns.py MIMIC_5.3
```

**Requirements:** Python 3.8+

## Usage

### Basic Commands

```bash
# TSV output (default)
python scripts/verify_patterns.py MIMIC_5.3

# CSV output
python scripts/verify_patterns.py MIMIC_5.3 --format csv

# JSON output
python scripts/verify_patterns.py MIMIC_5.3 --format json

# Save results to file
python scripts/verify_patterns.py MIMIC_5.3 --format csv > audit.csv
```

### Options

| Option | Description |
|--------|-------------|
| `--schema <path>` | Path to `SCHEMA.json` (default: `derived/<DATASET>/SCHEMA.json`) |
| `--dataset-path <path>` | Path to dataset folder with CSVs (default: `datasets/<DATASET>`) |
| `--format tsv\|csv\|json` | Output format (default: `tsv`) |
| `--strict-nulls` | Treat `NULL/NA/NAN/NONE` (case-insensitive) as NULL values |

### Advanced Examples

```bash
# Strict NULL handling with JSON output
python scripts/verify_patterns.py MIMIC_5.3 --strict-nulls --format json

# Custom schema and dataset paths
python scripts/verify_patterns.py MIMIC_5.3 \
  --schema derived/MIMIC_5.3/SCHEMA.json \
  --dataset-path datasets/MIMIC_5.3
```

## Output Columns

| Column | Description |
|--------|-------------|
| `dataset` | Dataset identifier (e.g., `MIMIC_5.3`) |
| `table` | Table name from schema |
| `column` | Column name being validated |
| `total_non_empty` | Count of non-empty values |
| `matches` | Values matching the pattern |
| `mismatches` | Values not matching the pattern |
| `hit_rate` | `matches / total_non_empty` (1.0 if no values) |
| `pattern` | Regex pattern from schema |

**Hit-rate semantics:** Columns with zero non-empty values report `hit_rate = 1.0` (trivially satisfied).

## Schema Format

Schemas are JSON files defining tables, columns, and validation patterns:

```json
{
  "tables": [
    {
      "name": "person",
      "columns": [
        { "name": "person_id", "type": "integer", "pattern": "^\\d+$" },
        { "name": "birth_datetime", "type": "datetime", "pattern": "^\\d{4}-\\d{2}-\\d{2}.*" }
      ],
      "primaryKey": "person_id",
      "foreignKeys": []
    }
  ]
}
```

### Supported Types

| Type | Format |
|------|--------|
| `integer` | 64-bit integer |
| `number` | Numeric value |
| `string` | Text |
| `date` | `YYYY-MM-DD` |
| `datetime` | `YYYY-MM-DD HH:MM:SS` |

## Project Structure

```
dataset-explorer-agent/
├── datasets/
│   └── MIMIC_5.3/          # Raw CSV files
│       ├── person.csv
│       ├── visit_occurrence.csv
│       └── ...
├── derived/
│   └── MIMIC_5.3/          # Schema metadata
│       ├── SCHEMA.json     # Machine-readable schema
│       └── SCHEMA.md       # Human-readable data dictionary
└── scripts/
    └── verify_patterns.py  # Pattern validator
```

## Current Datasets

**MIMIC_5.3** (OMOP CDM v5.3):
- 33 tables including core OMOP entities
- 313 columns with regex patterns
- Target: ≥99% hit rate
- De-identified, date-shifted clinical data

## Contributing

1. Add raw data to `datasets/<NAME>/`
2. Create schema files in `derived/<NAME>/`
3. Run validation: `python scripts/verify_patterns.py <NAME>`

## License

MIT
