# AGENTS.md

Scope: This file applies to the entire repository.

Read this before starting any task, and update `internals.md` after every task.

## Working Agreement

- Always read `internals.md` first to understand current datasets, schema locations, and conventions.
- After completing any task (docs, code, data changes), update `internals.md` to reflect what changed and where. Include:
  - What changed (files, tables, columns, docs).
  - Where the new or updated assets live (paths).
  - Any usage notes, migration considerations, or next steps.
- When touching a dataset, keep `SCHEMA.md` and `SCHEMA.json` in sync with the actual files (headers, types, keys).

## Style & Safety

- Be concise and surgical: make the smallest change that fully solves the task.
- Preserve existing structure and naming; avoid unrelated refactors.
- Treat IDs as 64‑bit; do not down‑cast.
- Do not invent schemas; derive from the actual headers and the dataset’s standard (e.g., OMOP CDM).

## Common Tasks

- Adding a dataset: create `datasets/<NAME>/`, add files, then author `derived/<NAME>/SCHEMA.md` and `derived/<NAME>/SCHEMA.json`. Document the dataset in `internals.md`.
- Updating a schema: adjust both `SCHEMA.md` and `SCHEMA.json`, and summarize the changes in `internals.md`.
- Generating DDL or validators: prefer deriving from `SCHEMA.json`.

## Pointers

- Dataset overview and conventions: `internals.md`
- Example schema: `derived/MIMIC_5.3/SCHEMA.md` and `derived/MIMIC_5.3/SCHEMA.json`
