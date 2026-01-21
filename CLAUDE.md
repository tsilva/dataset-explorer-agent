# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository hosts self-contained datasets (currently MIMIC 5.3 in OMOP CDM v5.3 format) with derived schemas for data quality validation and experimentation. The primary tool is a regex pattern validator that computes hit rates for dataset columns.

## Commands

**Pattern validation (primary utility):**
```bash
# Validate patterns for MIMIC 5.3 (TSV output)
python scripts/verify_patterns.py MIMIC_5.3

# CSV output (for saving to file)
python scripts/verify_patterns.py MIMIC_5.3 --format csv > audit.csv

# JSON output
python scripts/verify_patterns.py MIMIC_5.3 --format json

# Strict NULL handling
python scripts/verify_patterns.py MIMIC_5.3 --strict-nulls

# Custom paths
python scripts/verify_patterns.py MIMIC_5.3 \
  --schema derived/MIMIC_5.3/SCHEMA.json \
  --dataset-path datasets/MIMIC_5.3
```

**No build, lint, or test commands** — this is a data repository with a single Python validation script.

## Architecture

### Data and Schema Separation
The repository maintains a strict separation between raw data and derived metadata:

- **`datasets/<DATASET_NAME>/`** — Raw CSV files (e.g., `datasets/MIMIC_5.3/*.csv`)
- **`derived/<DATASET_NAME>/`** — Inferred schema metadata:
  - `SCHEMA.json` — Machine-readable schema with tables, columns, types, PK/FK, and regex patterns
  - `SCHEMA.md` — Human-readable data dictionary

This separation allows raw data to remain untouched while schemas evolve through validation and refinement.

### Schema Structure
`SCHEMA.json` is the source of truth for automation. Key elements:

- **Tables array**: Each table has `name`, `columns[]`, `primaryKey`, and `foreignKeys[]`
- **Column patterns**: Each column can declare a `pattern` (regex) for validation
- **Types**: `integer` (64-bit), `number`, `string`, `date` (YYYY-MM-DD), `datetime` (YYYY-MM-DD HH:MM:SS)
- **Concept IDs**: Columns ending with `_concept_id` are foreign keys to `concept.concept_id`

### Pattern Validator (`scripts/verify_patterns.py`)
The core utility scans all CSV files and computes per-column regex match statistics:

1. Loads `SCHEMA.json` and compiles all `pattern` regexes
2. For each table CSV, scans all rows and tests values against declared patterns
3. Outputs: `dataset`, `table`, `column`, `total_non_empty`, `matches`, `mismatches`, `hit_rate`, `pattern`
4. Hit-rate semantics: columns with zero non-empty values report `hit_rate = 1.0` (trivially satisfied)

**Performance note**: Large tables (e.g., `measurement.csv` with millions of rows) take time to scan.

## Workflow and Conventions

### Always Read and Update `internals.md`
Before starting any task:
1. Read `AGENTS.md` (working agreement) and `internals.md` (current state)
2. After completing any task, update `internals.md` with what changed, where, and any migration notes

### Schema Synchronization
When modifying datasets or schemas:
- Keep `SCHEMA.md` and `SCHEMA.json` in perfect sync
- Derive schemas from actual CSV headers and OMOP CDM standards
- Never invent structure — always reflect reality

### Adding a New Dataset
1. Create `datasets/<NAME>/` with raw files
2. Create `derived/<NAME>/SCHEMA.md` and `derived/<NAME>/SCHEMA.json`
3. Document in `internals.md` under "Dataset Inventory"

### Modifying Schemas or Patterns
- Update both `SCHEMA.md` and `SCHEMA.json`
- Test changes with `python scripts/verify_patterns.py <DATASET>`
- Document pattern fixes or schema changes in `internals.md` with root cause and validation results

### Data Integrity
- IDs are 64-bit integers (use `BIGINT` in warehouses)
- Dates are shifted for de-identification — never attempt to reverse
- Preserve type fidelity: don't coerce `date` to `datetime` or vice versa
- Polymorphic references (e.g., `cost`, `fact_relationship`) use domain + ID pairs

## Python Environment

- **Python 3.8+** recommended
- **No external dependencies** — uses only standard library (`argparse`, `csv`, `json`, `re`)
- No virtual environment or package manager needed

## README.md Maintenance

**IMPORTANT**: README.md must be kept up to date with any significant project changes. When updating documentation, ensure the README accurately reflects:
- Current dataset structure and locations
- Command usage and examples
- Available options and features
- Output formats and semantics

Always use the `readme-generator` skill to author or update README files.

## Current Datasets

**MIMIC_5.3** (OMOP CDM v5.3):
- Path: `datasets/MIMIC_5.3/*.csv`
- Schema: `derived/MIMIC_5.3/SCHEMA.{md,json}`
- 33 tables including core OMOP entities (person, visit_occurrence, condition_occurrence, drug_exposure, measurement, observation, specimen, note, note_nlp), eras, vocabulary, and admin tables
- 313 columns with regex patterns (≥99% hit rate target)
- De-identified, date-shifted clinical data

## Notes

- **No MCP servers**: The `internals.md` references a Schema Validator MCP at `servers/schema_validator_mcp/`, but this directory does not exist in the current repository. Ignore references to MCP tooling.
- **Be surgical**: Make minimal changes that fully solve the task. Avoid refactoring unrelated code.
- **Regex escaping**: When authoring patterns for `SCHEMA.json`, remember JSON string escaping (e.g., `\\d` for `\d`, `\\\\` for `\`).
