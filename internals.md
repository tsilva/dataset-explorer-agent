# Dataset Agents — Internals

This repository hosts small, self‑contained datasets and their schemas for downstream experimentation. Start here to understand what datasets exist, where their schemas live, and how to work with or extend them.

Last updated: 2025-09-15

## Updates (2025-09-15)

- MIMIC_5.3 schema tuning — regex patterns
  - Updated `datasets/MIMIC_5.3/SCHEMA.json` to add a `pattern` on every column. For numeric/date types we applied standard patterns; for string columns we inferred patterns from actual CSV values to cover ≥99% of non-empty entries (sampling up to 200k rows per table).
  - Examples:
    - `person.person_source_value`: `^\d{8}$` (all non-empty values are 8 digits).
    - `person.gender_source_value`: `^(?:M|F)$` (low-cardinality controlled values).
    - `race_source_value`, `ethnicity_source_value`: uppercase with separators (e.g., `^[A-Z /-]+$`).
  - Method: For each string column, we detected if values are fixed-length digits (then used `^\d{N}$` or range), otherwise derived a character class from observed characters; we only enumerated exact values when there were ≤5 distinct values and ≥100 non-empty samples. For `integer`, `number`, `date`, `datetime` we applied type-appropriate patterns.
  - Scope: 313 columns now include a `pattern`. No headers, types, PK/FK changed.
  - Notes: The current MCP validator (`validate_column`) enforces `type` only. If needed, we can extend it to also check `pattern`.

- New script: Pattern hit-rate validator
  - Path: `servers/schema_validator_mcp/verify_patterns.py`
  - Purpose: Scans all CSVs and computes, for every column with a `pattern` in `SCHEMA.json`, how many non-empty values match vs. do not match, yielding a hit rate per column.
  - Usage:
    - `python servers/schema_validator_mcp/verify_patterns.py --dataset datasets/MIMIC_5.3 --schema SCHEMA.json --format tsv`
    - Options:
      - `--strict-nulls`: treat `NULL/NA/NAN/NONE` (case-insensitive) as NULL and ignore.
      - `--format tsv|json`: output format (default tsv).
      - `--max-examples N`: number of example mismatched values to retain per column (default 10).
  - Output columns (tsv): `table`, `column`, `hit_rate`, `total_non_empty`, `matches`, `mismatches`, `pattern`.
  - Notes: Processes entire files row-by-row; running on large tables (e.g., `measurement.csv`) is compute-intensive.

## Dataset Inventory

- MIMIC_5.3 (OMOP CDM v5.3)
  - Path: `datasets/MIMIC_5.3/`
  - Format: CSV files in OMOP CDM v5.3 layout (de‑identified). Dates are shifted; identifiers are 64‑bit integers.
  - Schema files:
    - Human-readable: `datasets/MIMIC_5.3/SCHEMA.md`
    - Machine-readable: `datasets/MIMIC_5.3/SCHEMA.json`
  - Contents include core OMOP tables such as `person`, `visit_occurrence`, `condition_occurrence`, `drug_exposure`, `measurement`, `observation`, `specimen`, `note`, `note_nlp`, eras (`condition_era`, `drug_era`, `dose_era`), vocabulary (`concept`, `concept_relationship`, `vocabulary`), and admin tables (`provider`, `care_site`, `location`, `cdm_source`, `metadata`, cohorts, etc.).

## MCP Servers

- Schema Validator MCP
  - Path: `servers/schema_validator_mcp/`
  - Entry: `python servers/schema_validator_mcp/server.py`
  - Tool: `validate_column` — scans a single table/column and checks datatype compliance against `SCHEMA.json`.
  - Inputs: `table`, `column`, optional `datasetPath`, `schemaFile`, `strictNulls`, `maxExamples`.
  - Output: JSON summary with counts and example invalid values.
  - Setup: `pip install mcp` (see README in that folder).

### Using with Codex CLI

- Client spawn (stdio): point Codex CLI to `mcp.json` in the repo root so it can launch the server on demand.
  - The mapping registers server name `schema-validator-mcp` to run `python servers/schema_validator_mcp/server.py --transport stdio`.
  - This repo includes `codex.sh` which already wires the config automatically:
    - If Codex supports `--mcp-config`, it uses that flag.
    - Otherwise it falls back to setting `MCP_CONFIG=./mcp.json` before launching Codex.
- If your client only supports HTTP/SSE MCP endpoints, let us know — we can add an SSE/HTTP runner to the server.

## Where The Schema Lives

- Each dataset folder should contain a pair of schema files:
  - `SCHEMA.md`: data dictionary with table descriptions, per‑column fields, types, and key relationships.
  - `SCHEMA.json`: structured schema with `tables[]`, each listing `columns`, `primaryKey`, and `foreignKeys`.
- These two files are the source of truth for documentation and automation (DDL generation, integrity checks, loaders).

## Schema Conventions

- Types: `integer` (64‑bit), `number` (float/decimal), `string`, `date` (YYYY‑MM‑DD), `datetime` (YYYY‑MM‑DD HH:MM:SS).
- Keys: Primary keys are declared per table; foreign keys are explicit in `SCHEMA.md` and `SCHEMA.json`.
- Concepts: Any column ending with `_concept_id` is a foreign key to `concept.concept_id` unless stated otherwise.
- IDs: Treat identifiers as 64‑bit integers; use `BIGINT` or equivalent in warehouses.
- Dates: Do not coerce `date` into `datetime` or vice versa; preserve fidelity.

## How To Use The Schema

- Human readers: Start with `SCHEMA.md` for each dataset; it provides context and definitions.
- Automation: Consume `SCHEMA.json` to generate DDL, build loaders, or run integrity checks.
  - Example consumers: ad‑hoc scripts to emit Postgres/BigQuery DDL; data validation scripts to verify FK integrity.

## Typical Agent Tasks

1) Add a new dataset
- Create `datasets/<NAME>/` and place raw files (CSV/Parquet).
- Create `SCHEMA.md` and `SCHEMA.json` in that folder mirroring the actual columns and relationships.
- Document the dataset in this `internals.md` under “Dataset Inventory”.

2) Update an existing dataset or schema
- If files/columns changed, update both `SCHEMA.md` and `SCHEMA.json` to match headers and intended types.
- Note important changes and migration tips here in `internals.md` (e.g., new tables, renamed columns).

3) Expose/extend MCP tools
- Add tools to existing MCP servers in `servers/*` or create new ones alongside datasets.
- Document the new tool signature and usage here.

3) Optional checks (recommended for changes)
- Header sanity: `head -n 1 <file>.csv` to confirm column order.
- Row counts (approximate size tracking): `wc -l <file>.csv`.
- Spot values: `sed -n '2,6p' <file>.csv` to peek at samples.
- Foreign key integrity (ad‑hoc): sample join checks in your tool of choice using `SCHEMA.json` as a reference.

## Directory Layout

```
datasets/
  MIMIC_5.3/
    *.csv           # OMOP CDM tables
    SCHEMA.md       # Human data dictionary
    SCHEMA.json     # Machine schema (tables, columns, PK/FK)
servers/
  schema_validator_mcp/
    server.py       # MCP server (stdio)
    README.md       # Usage and tool docs
```

## Notes & Caveats

- De‑identification: Dates are shifted; do not attempt to reverse or cross‑link with external sources.
- Polymorphic references: Some OMOP tables (e.g., `cost`, `fact_relationship`) reference events via domain + ID pairs; see notes in `SCHEMA.*`.
- Load order: For warehouses, prefer loading vocabulary and reference tables first, then `person` and visits, then clinical events, then eras and utilities.
